import {canonical,fail,sha256} from './workflow_data.mjs';
import {qualityContractDigest,validateQualityContract} from './quality_contracts.mjs';
import {validateWorkflowPlan} from './workflow_plan.mjs';

export {
  applyRetargetProposal,
  buildComparativeEvaluationContext,
  buildMacroRevisionRequest,
  buildRetargetProposal,
  buildVisualReferenceSet,
} from './comparative_quality_loop.mjs';

const ACTION_CAPABILITIES=new Map([
  ['trim',['timeline.edit']],
  ['reorder',['timeline.edit']],
  ['replace_clip',['timeline.edit']],
  ['adjust_volume',['timeline.volume']],
  ['caption_edit',['timeline.text']],
  ['crop',['timeline.transform']],
  ['scale',['timeline.transform']],
  ['color_adjust',['timeline.color']],
  ['music_edit',['timeline.audio']],
]);

/** 将可执行 finding 编译为受约束的返工请求；不会生成命令或执行草稿写入。 */
export function buildRevisionRequest({verdict,allowedActions,availableCapabilities}) {
  validateQualityContract(verdict);
  if(verdict.schema!=='jianying-evaluation-verdict/v1') fail('quality_revision_invalid','an evaluation verdict is required');
  if(verdict.decision!=='revise') fail('quality_revision_not_required',`verdict decision ${verdict.decision} does not request revision`);
  if(!Array.isArray(allowedActions) || !Array.isArray(availableCapabilities))
    fail('quality_revision_invalid','allowed actions and available capabilities are required');
  const allowed=new Set(allowedActions),available=new Set(availableCapabilities),actions=[],unsupported=[];
  for(const finding of verdict.findings) {
    const capabilityIds=ACTION_CAPABILITIES.get(finding.suggested_action);
    if(!allowed.has(finding.suggested_action) || !capabilityIds || capabilityIds.some(id=>!available.has(id))) {
      unsupported.push(`${finding.code}:${finding.suggested_action}`); continue;
    }
    actions.push({action_id:`action-${sha256(canonical({code:finding.code,range:finding.time_range,output:finding.output_id})).slice(0,16)}`,
      type:finding.suggested_action,output_id:finding.output_id,
      target:`time:${finding.time_range.start_us}-${finding.time_range.end_us}`,
      constraints:[finding.observation,`rule:${finding.rule_id}`]});
  }
  if(!actions.length) fail('quality_revision_blocked','no registered and currently supported revision action is available');
  const requiredCapabilities=[...new Set(actions.flatMap(action=>ACTION_CAPABILITIES.get(action.type)))].sort();
  const request={schema:'jianying-revision-request/v1',workflow_id:verdict.workflow_id,from_revision:verdict.revision,
    to_revision:verdict.revision+1,verdict_digest:qualityContractDigest(verdict),actions,
    unsupported_suggestions:unsupported,required_capabilities:requiredCapabilities,required_approvals:['draft_write'],metadata:{}};
  validateQualityContract(request);
  return request;
}

/** 由已验证 verdict/request 生成新的计划 revision；不修改旧计划，也不执行动作。 */
export function createWorkflowRevision({plan,verdict,revisionRequest}) {
  validateWorkflowPlan(plan); validateQualityContract(verdict); validateQualityContract(revisionRequest);
  if(verdict.schema!=='jianying-evaluation-verdict/v1' || revisionRequest.schema!=='jianying-revision-request/v1')
    fail('quality_revision_invalid','a verdict and revision request are required');
  const verdictDigest=qualityContractDigest(verdict);
  if(plan.workflow_id!==verdict.workflow_id || plan.workflow_id!==revisionRequest.workflow_id ||
    plan.revision!==verdict.revision || plan.revision!==revisionRequest.from_revision ||
    revisionRequest.to_revision!==plan.revision+1 || revisionRequest.verdict_digest!==verdictDigest)
    fail('quality_revision_binding_mismatch','plan, verdict and revision request must describe one exact revision');
  if(!plan.creative_targets || !plan.iteration_policy)
    fail('quality_revision_invalid','quality contracts are not attached to the plan');
  const maximum=Math.min(plan.limits?.maximum_revisions??Number.MAX_SAFE_INTEGER,
    plan.iteration_policy.maximum_revisions);
  if(revisionRequest.to_revision>maximum) fail('quality_revision_limit','revision exceeds the bounded sequence');
  const outputs=new Set(plan.outputs.map(item=>item.output_id));
  if(revisionRequest.actions.some(action=>!outputs.has(action.output_id)))
    fail('quality_revision_binding_mismatch','revision action references an unknown output');
  const result=structuredClone(plan);
  result.revision=revisionRequest.to_revision;
  result.creative_targets=result.creative_targets.map(target=>({...target,revision:result.revision}));
  result.metadata={...result.metadata,
    'partme.previous_plan_digest':sha256(canonical(plan)),
    'partme.verdict_digest':verdictDigest,
    'partme.revision_request_digest':qualityContractDigest(revisionRequest)};
  validateWorkflowPlan(result);
  return result;
}

/** 在任何下一轮副作用前检查轮次、调用、预算、截止时间和人工复核门禁。 */
export function enforceIterationPolicy({policy,state,now=new Date().toISOString()}) {
  validateQualityContract(policy);
  if(policy.schema!=='jianying-iteration-policy/v1' || !state || typeof state!=='object')
    fail('quality_iteration_invalid','iteration policy and state are required');
  const current=state.current_revision,modelCalls=state.model_calls,requestedCalls=state.requested_model_calls??1;
  if(!Number.isSafeInteger(current) || current<1 || current>=policy.maximum_revisions)
    fail('quality_revision_limit','maximum revision reached before side effects');
  if(!Number.isSafeInteger(modelCalls) || modelCalls<0 || !Number.isSafeInteger(requestedCalls) || requestedCalls<0 ||
    modelCalls+requestedCalls>policy.maximum_model_calls)
    fail('quality_model_call_limit','maximum model calls would be exceeded');
  const spent=state.accumulated_budget;
  if(!spent || spent.currency!==policy.maximum_budget.currency || !Number.isFinite(spent.amount) || spent.amount<0 ||
    spent.amount+(state.requested_budget??0)>policy.maximum_budget.amount)
    fail('quality_budget_limit','maximum iteration budget would be exceeded');
  const instant=Date.parse(now);
  if(!Number.isFinite(instant) || instant>=Date.parse(policy.deadline))
    fail('quality_deadline_exceeded','iteration deadline passed');
  const completed=new Set(state.completed_human_reviews??[]);
  if(policy.required_human_review_points.some(point=>!completed.has(point)))
    fail('quality_human_review_required','required human review is incomplete');
  return {allowed:true,next_revision:current+1};
}

/** 比较连续 verdict，检测无实质提升、重复问题、硬门禁回退和评分回退。 */
export function detectIterationStall({policy,previousVerdict,currentVerdict,findingHistory=[]}) {
  validateQualityContract(policy); validateQualityContract(previousVerdict); validateQualityContract(currentVerdict);
  if(previousVerdict.schema!=='jianying-evaluation-verdict/v1' || currentVerdict.schema!=='jianying-evaluation-verdict/v1' ||
    previousVerdict.workflow_id!==currentVerdict.workflow_id || previousVerdict.output_id!==currentVerdict.output_id ||
    currentVerdict.revision!==previousVerdict.revision+1)
    fail('quality_iteration_invalid','verdicts must be consecutive and describe the same output');
  const reasons=[];
  const previousScores=new Map(previousVerdict.scores.map(item=>[item.dimension_id,item]));
  const improvements=currentVerdict.scores.filter(item=>previousScores.has(item.dimension_id))
    .map(item=>({value:item.value-previousScores.get(item.dimension_id).value,
      critical:!item.passed || !previousScores.get(item.dimension_id).passed}));
  const critical=improvements.filter(item=>item.critical).map(item=>item.value);
  const material=critical.length?Math.min(...critical):0;
  if(material<policy.minimum_material_improvement) reasons.push('minimum_material_improvement');
  const previousGates=new Map(previousVerdict.hard_gates.map(item=>[item.rule_id,item.passed]));
  if(currentVerdict.hard_gates.some(item=>previousGates.get(item.rule_id)===true && !item.passed))
    reasons.push('hard_gate_regression');
  if(improvements.some(item=>item.value < -policy.regression_tolerance)) reasons.push('score_regression');
  const serious=currentVerdict.findings.filter(item=>['major','critical'].includes(item.severity)).map(item=>item.code);
  if(serious.some(code=>findingHistory.filter(items=>items.includes(code)).length+1>=policy.repeated_finding_limit))
    reasons.push('repeated_finding');
  return {stopped:reasons.length>0,reasons,material_improvement:material};
}
