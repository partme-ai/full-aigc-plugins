import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {AdapterError} from './runtime_adapter.mjs';
import {canonical,sha256,parseStrictJson,readBounded} from './workflow_data.mjs';
import {qualityContractDigest,validateQualityContract} from './quality_contracts.mjs';
import {enforceIterationPolicy} from './quality_iteration.mjs';

function atomicJson(file,value) {
  fs.mkdirSync(path.dirname(file),{recursive:true});
  const temporary=`${file}.${process.pid}.tmp`;
  fs.writeFileSync(temporary,`${JSON.stringify(value,null,2)}\n`,{encoding:'utf8',mode:0o600});
  fs.renameSync(temporary,file);
}

const fail=(code,message)=>{throw new AdapterError(code,message);};
const digest=value=>typeof value==='string' && /^[a-f0-9]{64}$/.test(value);

function validateCompilation(compilation) {
  if(compilation?.schema!=='jianying-workflow-compilation/v1' || !compilation.can_compile || !compilation.receipt)
    fail('compilation_not_ready','a successful compilation receipt is required');
  if(!digest(compilation.plan_digest) || !digest(compilation.receipt.execution_digest))
    fail('compilation_not_ready','compilation digests are required');
}

function qualityState(receipt,budget) {
  const quality=receipt.quality_contracts;
  if(quality===undefined) return null;
  if(!quality || Object.keys(quality).some(key=>!['workflow_id','revision','target_digests','profile_digests','iteration_policy_digest'].includes(key)) ||
    typeof quality.workflow_id!=='string' || !quality.workflow_id.trim() || !Number.isSafeInteger(quality.revision) || quality.revision<1 ||
    !Array.isArray(quality.target_digests) || !quality.target_digests.length ||
    !Array.isArray(quality.profile_digests) || quality.profile_digests.length!==quality.target_digests.length ||
    [...quality.target_digests,...quality.profile_digests,quality.iteration_policy_digest].some(value=>!digest(value)))
    fail('quality_binding_invalid','compilation has incomplete quality contract digests');
  return {...structuredClone(quality),verdict_digest:null,revision_request_digest:null,
    accumulated_budget:{currency:budget.currency,amount:0},evaluator_scope:null};
}

export class WorkflowRuntime {
  constructor({stateRoot,executor,verifier,now,checkpoint}={}) {
    this.stateRoot=path.resolve(stateRoot);
    this.executor=executor??(()=>fail('executor_unavailable','no registered workflow executor'));
    this.verifier=verifier??(()=>fail('verifier_unavailable','no registered artifact verifier'));
    this.now=now??(()=>Date.now());
    this.checkpoint=checkpoint??(()=>{});
  }

  start({compilation,revision,budget,failure_policy='stop_all',maximum_revisions=3,iterationPolicy}={}) {
    validateCompilation(compilation);
    if(!Number.isSafeInteger(revision) || revision<1) fail('workflow_revision_invalid','revision must be positive');
    if(!['stop_all','continue_independent'].includes(failure_policy)) fail('failure_policy_invalid','unknown failure policy');
    if(!Number.isSafeInteger(maximum_revisions) || maximum_revisions<1) fail('workflow_revision_invalid','revision limit must be positive');
    const runId=`run-${sha256(canonical({execution:compilation.receipt.execution_digest,revision})).slice(0,20)}`;
    const file=this.file(runId);
    if(fs.existsSync(file)) return this.show(runId);
    const blockedOutputs=compilation.job_bindings.filter(binding=>(binding.blockers??[]).length).map(binding=>binding.output_id);
    const independentlyRunnable=compilation.job_bindings.filter(binding=>!(binding.blockers??[]).length).map(binding=>binding.output_id);
    const runnableOutputs=blockedOutputs.length&&failure_policy==='stop_all'?[]:independentlyRunnable;
    const stage=blockedOutputs.length&&failure_policy==='stop_all'?'blocked':'awaiting_approval';
    const boundQuality=qualityState(compilation.receipt,budget);
    if(boundQuality) {
      if(!iterationPolicy) fail('quality_binding_invalid','runtime iteration policy is required');
      validateQualityContract(iterationPolicy);
      if(iterationPolicy.schema!=='jianying-iteration-policy/v1' ||
        qualityContractDigest(iterationPolicy)!==boundQuality.iteration_policy_digest)
        fail('quality_binding_invalid','runtime iteration policy does not match the compilation receipt');
      maximum_revisions=Math.min(maximum_revisions,iterationPolicy.maximum_revisions);
    } else if(iterationPolicy!==undefined) fail('quality_binding_invalid','iteration policy requires a quality compilation');
    const state={schema:'jianying-workflow-run/v1',run_id:runId,revision,attempt:1,epoch:0,stage,
      terminal_state:null,compilation,plan_digest:compilation.plan_digest,execution_digest:compilation.receipt.execution_digest,
      budget,failure_policy,maximum_revisions,quality_contracts:boundQuality,
      iteration_policy:boundQuality?structuredClone(iterationPolicy):null,model_calls:0,completed_human_reviews:[],
      approval:null,lease:null,results:[],evidence:[],history:[],
      runnable_outputs:runnableOutputs,blocked_outputs:blockedOutputs};
    this.record(state,'run.started'); this.save(state); return state;
  }

  approvalBinding(runId) {
    const state=this.show(runId);
    const bindings=state.compilation.job_bindings.filter(binding=>state.runnable_outputs.includes(binding.output_id));
    return {run_id:state.run_id,revision:state.revision,plan_digest:state.plan_digest,
      execution_digest:state.execution_digest,job_digests:bindings.map(binding=>binding.job_digest),
      cli_sha256:state.compilation.receipt.cli.sha256,purposes:bindings.map(binding=>binding.purpose),
      targets:bindings.map(binding=>binding.output_path),budget:state.budget,
      ...(state.quality_contracts?{quality_contracts:structuredClone(state.quality_contracts)}:{}),expires_scope:'single_attempt'};
  }

  approve(runId,approval) {
    const state=this.show(runId),expected=this.approvalBinding(runId);
    if(state.stage==='blocked') fail('workflow_blocked','stop_all requires every output to be unblocked');
    for(const [key,value] of Object.entries(expected))
      if(canonical(approval[key])!==canonical(value)) fail('approval_scope_mismatch',`${key} differs from current run`);
    if(typeof approval.user_id!=='string' || !approval.user_id.trim()) fail('approval_scope_mismatch','user identity required');
    if(!Number.isFinite(Date.parse(approval.expires_at)) || Date.parse(approval.expires_at)<=this.now())
      fail('approval_expired','approval expired');
    state.approval={...approval,used:false,revoked:false}; state.stage='ready';
    this.record(state,'approval.granted'); this.save(state); return state;
  }

  revokeApproval(runId,{user_id}={}) {
    const state=this.show(runId);
    if(!state.approval || state.approval.used) fail('approval_not_revocable','no unused approval can be revoked');
    if(typeof user_id!=='string' || !user_id.trim()) fail('approval_scope_mismatch','revoking user identity required');
    state.approval={...state.approval,revoked:true,revoked_by:user_id}; state.stage='awaiting_approval';
    this.record(state,'approval.revoked',{user_id}); this.save(state); return state;
  }

  revise(runId,{plan_digest,execution_digest,revision,compilation,verdict,revisionRequest,
    accumulatedBudget,evaluatorScope,modelCalls,completedHumanReviews}={}) {
    const state=this.show(runId),next=state.revision+1;
    if(state.stage==='running' || state.stage==='reconciling') fail('workflow_revision_occupied','occupied run cannot be revised');
    if((revision!==undefined && revision!==next) || next>state.maximum_revisions)
      fail('workflow_revision_limit','revision exceeds the bounded sequence');
    if(compilation) {
      validateCompilation(compilation);
      plan_digest=compilation.plan_digest; execution_digest=compilation.receipt.execution_digest;
    }
    if(!digest(plan_digest) || !digest(execution_digest))
      fail('workflow_revision_invalid','revision digests are required');
    if(state.quality_contracts) {
      if(!compilation?.receipt?.quality_contracts || !verdict || !revisionRequest)
        fail('quality_binding_invalid','quality revision requires compilation, verdict and revision request');
      validateQualityContract(verdict); validateQualityContract(revisionRequest);
      const verdictDigest=qualityContractDigest(verdict),requestDigest=qualityContractDigest(revisionRequest);
      if(verdict.schema!=='jianying-evaluation-verdict/v1' || revisionRequest.schema!=='jianying-revision-request/v1' ||
        verdict.revision!==state.revision || revisionRequest.from_revision!==state.revision ||
        revisionRequest.to_revision!==next || revisionRequest.verdict_digest!==verdictDigest)
        fail('quality_binding_invalid','verdict and revision request are not bound to the current revision');
      const base=qualityState(compilation.receipt,state.budget);
      if(base.workflow_id!==verdict.workflow_id || base.revision!==next)
        fail('quality_binding_invalid','replacement compilation does not match the next workflow revision');
      if(!accumulatedBudget || accumulatedBudget.currency!==state.budget.currency ||
        !Number.isFinite(accumulatedBudget.amount) || accumulatedBudget.amount<0 || accumulatedBudget.amount>state.budget.maximum)
        fail('quality_binding_invalid','accumulated budget is invalid');
      if(!evaluatorScope || typeof evaluatorScope.provider!=='string' || !evaluatorScope.provider.trim() ||
        typeof evaluatorScope.model!=='string' || !evaluatorScope.model.trim() || !digest(evaluatorScope.resource_digest) ||
        Object.keys(evaluatorScope).some(key=>!['provider','model','resource_digest'].includes(key)))
        fail('quality_binding_invalid','evaluator resource scope is invalid');
      enforceIterationPolicy({policy:state.iteration_policy,state:{current_revision:state.revision,
        model_calls:modelCalls,requested_model_calls:0,accumulated_budget:accumulatedBudget,requested_budget:0,
        completed_human_reviews:completedHumanReviews}});
      state.quality_contracts={...base,verdict_digest:verdictDigest,revision_request_digest:requestDigest,
        accumulated_budget:structuredClone(accumulatedBudget),evaluator_scope:structuredClone(evaluatorScope)};
      state.model_calls=modelCalls; state.completed_human_reviews=structuredClone(completedHumanReviews);
    } else if(compilation?.receipt?.quality_contracts || verdict || revisionRequest || accumulatedBudget || evaluatorScope) {
      fail('quality_binding_invalid','quality data cannot be added to a non-quality run');
    }
    if(compilation) {
      state.compilation=structuredClone(compilation);
      state.blocked_outputs=compilation.job_bindings.filter(binding=>(binding.blockers??[]).length).map(binding=>binding.output_id);
      const independent=compilation.job_bindings.filter(binding=>!(binding.blockers??[]).length).map(binding=>binding.output_id);
      state.runnable_outputs=state.blocked_outputs.length&&state.failure_policy==='stop_all'?[]:independent;
    }
    state.revision=next; state.plan_digest=plan_digest; state.execution_digest=execution_digest;
    state.approval=null; state.lease=null; state.results=[]; state.evidence=[]; state.terminal_state=null;
    state.stage='awaiting_approval'; state.attempt+=1;
    this.record(state,'run.revised'); this.save(state); return state;
  }

  execute(runId) {
    let state=this.show(runId);
    if(state.terminal_state==='completed') return state;
    if(state.stage==='cancel_requested') fail('cancel_not_confirmed','stop has not been confirmed');
    if(state.terminal_state==='cancelled') fail('task_cancelled','cancelled run requires a new attempt');
    if(state.stage!=='ready' || !state.approval || state.approval.used || state.approval.revoked ||
      Date.parse(state.approval.expires_at)<=this.now()) fail('approval_required','current exact-binding approval required');
    const lock=this.lockFile(runId); let descriptor;
    try {descriptor=fs.openSync(lock,'wx',0o600);} catch(error) {
      if(error.code==='EEXIST') return this.show(runId);
      throw error;
    }
    state.epoch+=1; state.lease={epoch:state.epoch,token:crypto.randomUUID(),acquired_at:new Date(this.now()).toISOString()};
    state.stage='running'; state.approval.used=true; this.record(state,'execution.claimed'); this.save(state);
    fs.writeFileSync(descriptor,JSON.stringify({run_id:runId,epoch:state.epoch,token:state.lease.token})); fs.closeSync(descriptor);
    try {
      const runnableBindings=state.compilation.job_bindings.filter(binding=>state.runnable_outputs.includes(binding.output_id));
      const result=this.executor(runnableBindings,state);
      try {
        this.checkpoint('execution.returned_before_persist',{run_id:runId,epoch:state.epoch,attempt:state.attempt});
      } catch(error) {
        const uncertain=error instanceof Error?error:new Error(String(error));
        uncertain.outcome='unknown';
        throw uncertain;
      }
      state=this.show(runId); state.results=result?.artifacts??[]; state.stage='verifying';
      this.record(state,'execution.returned'); this.save(state);
      const verification=this.verifier(state.results,state);
      state=this.show(runId); state.evidence=verification.evidence??[];
      if(!verification.ok) {state.stage='failed';state.terminal_state='failed';this.record(state,'verification.failed');}
      else if(state.blocked_outputs.length) {state.stage='partially_completed';state.terminal_state='partially_completed';
        this.record(state,'verification.partially_completed',{blocked_outputs:state.blocked_outputs});}
      else if(state.quality_contracts) {state.stage='rendering_proxy';state.terminal_state=null;
        this.record(state,'verification.structural_completed');}
      else {state.stage='completed';state.terminal_state='completed';this.record(state,'verification.completed');}
      this.save(state); this.release(runId); return state;
    } catch(error) {
      state=this.show(runId);
      if(error.outcome==='unknown') {
        state.stage='reconciling';state.terminal_state=null;this.record(state,'execution.outcome_unknown');this.save(state);
        throw new AdapterError('execution_outcome_unknown','side effect requires reconciliation');
      }
      state.stage='failed';state.terminal_state='failed';this.record(state,'execution.failed',{message:error.message});this.save(state);
      this.release(runId); throw error;
    }
  }

  reconcile(runId,{outcome}) {
    const state=this.show(runId);
    if(state.stage!=='reconciling') fail('reconcile_not_required','run is not reconciling');
    if(outcome==='artifact_exists') {
      const verification=this.verifier(state.results,state);
      if(!verification.ok) fail('artifact_verification_failed','existing artifact did not verify');
      state.evidence=verification.evidence??[];state.stage='completed';state.terminal_state='completed';
      this.record(state,'reconcile.existing_artifact');this.save(state);this.release(runId);return state;
    }
    if(outcome==='not_executed') {
      state.stage='awaiting_approval';state.attempt+=1;state.approval=null;state.lease=null;
      this.record(state,'reconcile.not_executed');this.save(state);this.release(runId);return state;
    }
    fail('manual_reconciliation_required','unknown side effect remains occupied');
  }

  recordProxyEvidence(runId,bundle) {
    const state=this.show(runId);
    if(state.stage!=='rendering_proxy' || !state.quality_contracts)
      fail('quality_transition_invalid','proxy evidence is not expected in the current state');
    validateQualityContract(bundle);
    if(bundle.schema!=='jianying-evidence-bundle/v1' || bundle.workflow_id!==state.quality_contracts.workflow_id ||
      bundle.revision!==state.revision || !state.runnable_outputs.includes(bundle.output_id) || bundle.conclusion==='failed' ||
      !['proxy','technical'].every(type=>bundle.items.some(item=>item.type===type&&item.passed)))
      fail('quality_binding_invalid','proxy evidence does not match the current workflow output and revision');
    state.evidence.push(structuredClone(bundle)); state.stage='evaluating';
    this.record(state,'quality.proxy_verified',{output_id:bundle.output_id,artifact_digest:bundle.artifact_digest});
    this.save(state); return state;
  }

  recordEvaluation(runId,verdict,{deliveryEvidence}={}) {
    const state=this.show(runId);
    if(state.stage!=='evaluating' || !state.quality_contracts)
      fail('quality_transition_invalid','evaluation is not expected in the current state');
    validateQualityContract(verdict);
    if(verdict.schema!=='jianying-evaluation-verdict/v1' || verdict.workflow_id!==state.quality_contracts.workflow_id ||
      verdict.revision!==state.revision || !state.runnable_outputs.includes(verdict.output_id))
      fail('quality_binding_invalid','verdict does not match the current workflow output and revision');
    state.verdicts??=[]; state.verdicts.push(structuredClone(verdict));
    if(verdict.decision==='revise') state.stage='revision_requested';
    else if(verdict.decision==='blocked') state.stage='needs_human_review';
    else if(verdict.decision==='stop') {state.stage='iteration_stopped';state.terminal_state='iteration_stopped';}
    else {
      if(deliveryEvidence) {
        validateQualityContract(deliveryEvidence);
        if(deliveryEvidence.schema!=='jianying-evidence-bundle/v1' || deliveryEvidence.workflow_id!==verdict.workflow_id ||
          deliveryEvidence.revision!==verdict.revision || deliveryEvidence.output_id!==verdict.output_id ||
          deliveryEvidence.conclusion!=='passed') fail('quality_binding_invalid','delivery evidence cannot complete this verdict');
        state.evidence.push(structuredClone(deliveryEvidence));state.stage='completed';state.terminal_state='completed';
      } else state.stage='needs_human_review';
    }
    this.record(state,`quality.${state.stage}`,{output_id:verdict.output_id,verdict_digest:qualityContractDigest(verdict)});
    this.save(state); return state;
  }

  markCapabilityBlocked(runId,{capability,reason}={}) {
    const state=this.show(runId);
    if(!['rendering_proxy','evaluating','revision_requested'].includes(state.stage) ||
      typeof capability!=='string' || !capability.trim() || typeof reason!=='string' || !reason.trim())
      fail('quality_transition_invalid','a current quality stage, capability and reason are required');
    state.stage='capability_blocked';state.terminal_state=null;
    this.record(state,'quality.capability_blocked',{capability,reason});this.save(state);return state;
  }

  stopIteration(runId,{reasons}={}) {
    const state=this.show(runId);
    if(!state.quality_contracts || !['evaluating','revision_requested','needs_human_review','capability_blocked'].includes(state.stage) ||
      !Array.isArray(reasons) || !reasons.length || reasons.some(reason=>typeof reason!=='string'||!reason.trim()))
      fail('quality_transition_invalid','bounded stop requires explicit reasons in a quality stage');
    state.stage='iteration_stopped';state.terminal_state='iteration_stopped';
    this.record(state,'quality.iteration_stopped',{reasons:structuredClone(reasons)});this.save(state);return state;
  }

  cancel(runId) {
    const state=this.show(runId);
    if(state.terminal_state) fail('task_terminal','terminal run cannot be cancelled');
    state.stage='cancel_requested';this.record(state,'cancel.requested');this.save(state);return state;
  }

  confirmCancelled(runId) {
    const state=this.show(runId);
    if(state.stage!=='cancel_requested') fail('cancel_not_requested','cancel was not requested');
    state.stage='cancelled';state.terminal_state='cancelled';this.record(state,'cancel.confirmed');this.save(state);
    this.release(runId);return state;
  }

  resume(runId) {
    const state=this.show(runId);
    if(state.stage==='cancel_requested') fail('cancel_not_confirmed','stop has not been confirmed');
    if(state.terminal_state==='cancelled') fail('task_cancelled','cancelled run requires a new attempt');
    if(state.stage==='reconciling') fail('manual_reconciliation_required','reconcile before resuming');
    return this.execute(runId);
  }

  show(runId) {return parseStrictJson(readBounded(this.file(runId),8*1024*1024).toString('utf8'));}
  file(runId) {return path.join(this.stateRoot,runId,'state.json');}
  lockFile(runId) {return path.join(this.stateRoot,runId,'execution.lock');}
  save(state) {atomicJson(this.file(state.run_id),state);}
  record(state,event,details={}) {state.history.push({sequence:state.history.length+1,event,details});}
  release(runId) {const file=this.lockFile(runId);if(fs.existsSync(file)) fs.unlinkSync(file);}
}

export function verifyDraftArtifact(root,expected) {
  const issues=[],evidence=[];
  for(const name of ['draft_content.json','draft_meta_info.json']) {
    const file=path.join(root,name);
    if(!fs.existsSync(file) || !fs.statSync(file).isFile()) issues.push({code:'artifact_missing',file:name});
    else evidence.push({file:name,sha256:sha256(fs.readFileSync(file)),bytes:fs.statSync(file).size});
  }
  if(!issues.length) {
    try {
      const content=parseStrictJson(readBounded(path.join(root,'draft_content.json'),64*1024*1024).toString('utf8'));
      if(content.duration!==expected.duration_us) issues.push({code:'duration_mismatch',expected:expected.duration_us,actual:content.duration});
      if(!Array.isArray(content.tracks) || !content.tracks.some(track=>Array.isArray(track.segments) && track.segments.length))
        issues.push({code:'timeline_empty'});
    } catch(error) {issues.push({code:'artifact_invalid',message:error.message});}
  }
  return {ok:issues.length===0,issues,evidence};
}
