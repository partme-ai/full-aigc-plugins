import {canonical,fail,sha256} from './workflow_data.mjs';
import {qualityContractDigest,validateQualityContract} from './quality_contracts.mjs';

const READ_ONLY_CRITIC_TOOLS=['artifact.inspect','evidence.read','quality.profile.read'];
const RECORD_TYPES=new Set(['approval','context','verdict','evidence']);

const requireString=(value,name)=>{
  if(typeof value!=='string' || !value.trim()) fail('quality_comparison_invalid',`${name} is required`);
};

const proxyDigest=input=>{
  const proxy=input.artifacts.find(item=>item.type==='proxy_media');
  if(!proxy) fail('quality_comparison_binding_mismatch','evaluation input lacks proxy media');
  return proxy.digest;
};

/** 构建与一个 CreativeTarget 精确绑定的视觉参考集，不授予文件或执行权限。 */
export function buildVisualReferenceSet({target,outputId,references,metadata={}}={}) {
  validateQualityContract(target);
  if(target.schema!=='jianying-creative-target/v1')
    fail('quality_visual_reference_invalid','a creative target is required');
  requireString(outputId,'outputId');
  if(!target.quality_profiles.some(item=>item.output_id===outputId))
    fail('quality_visual_reference_invalid','output is not bound to the creative target');
  if(!Array.isArray(references) || !references.length)
    fail('quality_visual_reference_invalid','at least one visual reference is required');
  const targetDigest=qualityContractDigest(target);
  const value={schema:'jianying-visual-reference-set/v1',
    reference_set_id:`reference-set-${sha256(canonical({workflow_id:target.workflow_id,revision:target.revision,
      output_id:outputId,target_digest:targetDigest,references})).slice(0,20)}`,
    workflow_id:target.workflow_id,revision:target.revision,output_id:outputId,target_digest:targetDigest,
    references:structuredClone(references),metadata:structuredClone(metadata)};
  validateQualityContract(value);
  return value;
}

/** 构建目标、当前版本和上一版本三方比较上下文；Critic 永远只有固定只读工具。 */
export function buildComparativeEvaluationContext({target,references,currentInput,previousInput,previousVerdict,
  criticSessionId,usedCriticSessionIds=[]}={}) {
  for(const value of [target,references,currentInput,previousInput,previousVerdict]) validateQualityContract(value);
  if(target.schema!=='jianying-creative-target/v1' || references.schema!=='jianying-visual-reference-set/v1' ||
    currentInput.schema!=='jianying-evaluation-input/v1' || previousInput.schema!=='jianying-evaluation-input/v1' ||
    previousVerdict.schema!=='jianying-evaluation-verdict/v1')
    fail('quality_comparison_invalid','target, references, two inputs and previous verdict are required');
  requireString(criticSessionId,'criticSessionId');
  if(!Array.isArray(usedCriticSessionIds) || usedCriticSessionIds.includes(criticSessionId))
    fail('quality_critic_session_reused','critic session must be new for every comparison');
  const targetDigest=qualityContractDigest(target);
  const previousInputDigest=qualityContractDigest(previousInput);
  const sameIdentity=[references,currentInput,previousInput,previousVerdict].every(item=>
    item.workflow_id===target.workflow_id && item.output_id===references.output_id);
  if(!sameIdentity || target.revision!==currentInput.revision || references.revision!==target.revision ||
    references.target_digest!==targetDigest || currentInput.target_digest!==targetDigest ||
    previousInput.revision!==currentInput.revision-1 || previousVerdict.revision!==previousInput.revision ||
    previousVerdict.input_digest!==previousInputDigest || previousInput.profile_digest!==currentInput.profile_digest)
    fail('quality_comparison_binding_mismatch','comparison inputs do not describe consecutive bound revisions');
  const referenceSetDigest=qualityContractDigest(references);
  const currentInputDigest=qualityContractDigest(currentInput);
  const previousVerdictDigest=qualityContractDigest(previousVerdict);
  const value={schema:'jianying-comparative-evaluation-context/v1',
    context_id:`comparison-${sha256(canonical({targetDigest,referenceSetDigest,currentInputDigest,
      previousInputDigest,previousVerdictDigest,criticSessionId})).slice(0,20)}`,
    workflow_id:target.workflow_id,revision:currentInput.revision,output_id:currentInput.output_id,
    target_digest:targetDigest,profile_digest:currentInput.profile_digest,reference_set_digest:referenceSetDigest,
    current:{evaluation_input_digest:currentInputDigest,proxy_digest:proxyDigest(currentInput)},
    previous:{revision:previousInput.revision,evaluation_input_digest:previousInputDigest,
      proxy_digest:proxyDigest(previousInput),verdict_digest:previousVerdictDigest},
    comparison_dimensions:['absolute_quality','target_gap','prior_delta'],
    critic:{session_id:criticSessionId,fresh_context:true,write_access:false,allowed_tools:[...READ_ONLY_CRITIC_TOOLS]},
    metadata:{}};
  validateQualityContract(value);
  return value;
}

/** 从已验证停滞生成每个输出最多一次的宏观返工请求；不生成具体命令。 */
export function buildMacroRevisionRequest({context,stall,strategies,priorMacroRequestDigests=[]}={}) {
  validateQualityContract(context);
  if(context.schema!=='jianying-comparative-evaluation-context/v1' || !stall || typeof stall!=='object')
    fail('quality_macro_revision_invalid','comparative context and stall result are required');
  if(stall.stopped!==true || !Array.isArray(stall.reasons) || !stall.reasons.length)
    fail('quality_macro_revision_not_required','macro revision requires a verified stall');
  if(!Array.isArray(priorMacroRequestDigests) || priorMacroRequestDigests.length)
    fail('quality_macro_revision_exhausted','each output permits at most one macro revision');
  if(!Array.isArray(strategies) || !strategies.length)
    fail('quality_macro_revision_invalid','at least one macro strategy is required');
  const contextDigest=qualityContractDigest(context),stallDigest=sha256(canonical(stall));
  const value={schema:'jianying-macro-revision-request/v1',
    request_id:`macro-${sha256(canonical({contextDigest,stallDigest,strategies})).slice(0,20)}`,
    workflow_id:context.workflow_id,output_id:context.output_id,from_revision:context.revision,
    to_revision:context.revision+1,stall_digest:stallDigest,context_digest:contextDigest,
    strategies:[...new Set(strategies)],reason_codes:[...new Set(stall.reasons)],maximum_once:true,
    required_approvals:['human_macro_revision'],metadata:{}};
  validateQualityContract(value);
  return value;
}

/** 提出目标变更；只有 applyRetargetProposal 的精确人工批准才能使其生效。 */
export function buildRetargetProposal({currentTarget,proposedTarget,proposedReferences,reason,evidenceRefs,metadata={}}={}) {
  for(const value of [currentTarget,proposedTarget,proposedReferences]) validateQualityContract(value);
  if(currentTarget.schema!=='jianying-creative-target/v1' || proposedTarget.schema!=='jianying-creative-target/v1' ||
    proposedReferences.schema!=='jianying-visual-reference-set/v1')
    fail('quality_retarget_invalid','current target, proposed target and references are required');
  requireString(reason,'reason');
  if(!Array.isArray(evidenceRefs) || !evidenceRefs.length)
    fail('quality_retarget_invalid','retarget evidence is required');
  const fromTargetDigest=qualityContractDigest(currentTarget),proposedTargetDigest=qualityContractDigest(proposedTarget);
  const currentOutput=currentTarget.quality_profiles[0]?.output_id;
  const proposedOutput=proposedTarget.quality_profiles[0]?.output_id;
  if(currentTarget.workflow_id!==proposedTarget.workflow_id || currentOutput!==proposedOutput ||
    proposedTarget.revision!==currentTarget.revision+1 || proposedReferences.workflow_id!==proposedTarget.workflow_id ||
    proposedReferences.output_id!==proposedOutput || proposedReferences.revision!==proposedTarget.revision ||
    proposedReferences.target_digest!==proposedTargetDigest)
    fail('quality_retarget_binding_mismatch','retarget artifacts do not describe one consecutive output target');
  const referenceDigest=qualityContractDigest(proposedReferences);
  const value={schema:'jianying-retarget-proposal/v1',
    proposal_id:`retarget-${sha256(canonical({fromTargetDigest,proposedTargetDigest,referenceDigest,reason})).slice(0,20)}`,
    workflow_id:currentTarget.workflow_id,output_id:currentOutput,from_revision:currentTarget.revision,
    to_revision:proposedTarget.revision,from_target_digest:fromTargetDigest,proposed_target_digest:proposedTargetDigest,
    proposed_reference_set_digest:referenceDigest,reason,evidence_refs:[...new Set(evidenceRefs)],
    required_approval:'human_retarget',status:'proposed',metadata:structuredClone(metadata)};
  validateQualityContract(value);
  return value;
}

/** 应用精确人工批准并返回确定性失效集合；不修改原合同，也不写草稿。 */
export function applyRetargetProposal({proposal,approval,boundRecords=[],now=new Date().toISOString()}={}) {
  validateQualityContract(proposal);
  if(proposal.schema!=='jianying-retarget-proposal/v1') fail('quality_retarget_invalid','retarget proposal is required');
  const proposalDigest=qualityContractDigest(proposal),instant=Date.parse(now);
  if(!approval || approval.schema!=='jianying-retarget-approval/v1' || approval.status!=='approved' ||
    approval.proposal_digest!==proposalDigest || typeof approval.approval_id!=='string' || !approval.approval_id.trim() ||
    typeof approval.user_id!=='string' || !approval.user_id.trim() || !Number.isFinite(instant) ||
    !Number.isFinite(Date.parse(approval.expires_at)) || Date.parse(approval.expires_at)<=instant)
    fail('quality_retarget_approval_required','exact unexpired human retarget approval is required');
  if(!Array.isArray(boundRecords)) fail('quality_retarget_invalid','boundRecords must be an array');
  const invalidated=boundRecords.filter(record=>record && RECORD_TYPES.has(record.type) &&
    typeof record.id==='string' && record.id.trim() && record.target_digest===proposal.from_target_digest)
    .map(record=>({type:record.type,id:record.id}))
    .sort((left,right)=>left.type.localeCompare(right.type)||left.id.localeCompare(right.id));
  return {schema:'jianying-retarget-result/v1',status:'retarget_applied',workflow_id:proposal.workflow_id,
    output_id:proposal.output_id,revision:proposal.to_revision,target_digest:proposal.proposed_target_digest,
    reference_set_digest:proposal.proposed_reference_set_digest,proposal_digest:proposalDigest,
    approval_id:approval.approval_id,approved_by:approval.user_id,invalidated,
    result_digest:sha256(canonical({proposal_digest:proposalDigest,approval_id:approval.approval_id,invalidated}))};
}
