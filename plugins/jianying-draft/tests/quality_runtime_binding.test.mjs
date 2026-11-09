import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import {WorkflowRuntime} from '../scripts/workflow_runtime.mjs';
import {buildRevisionRequest} from '../scripts/quality_iteration.mjs';
import {qualityContractDigest} from '../scripts/quality_contracts.mjs';

const ROOT=path.resolve(import.meta.dirname,'..');
const CONTRACTS=JSON.parse(fs.readFileSync(path.join(ROOT,'tests/fixtures/quality-loop/contracts.json'),'utf8'));

const POLICY=structuredClone(CONTRACTS.iteration_policy);
POLICY.maximum_budget.amount=10;
const quality={workflow_id:'VLOG-01',revision:1,target_digests:['1'.repeat(64)],profile_digests:['2'.repeat(64)],
  iteration_policy_digest:qualityContractDigest(POLICY)};
const compilation={schema:'jianying-workflow-compilation/v1',can_compile:true,can_execute:false,
  plan_digest:'4'.repeat(64),blockers:[{code:'approval_required'}],
  job_bindings:[{output_id:'main',purpose:'personal',output_path:'/tmp/output-main',job_digest:'5'.repeat(64),blockers:[],
    job:{schema:'jianying-job/v2',operation:'create'}}],
  receipt:{schema:'jianying-compilation-receipt/v1',execution_digest:'6'.repeat(64),semantic_digest:'7'.repeat(64),
    quality_contracts:quality,cli:{version:'1.6.14',sha256:'8'.repeat(64),job_schema:'jianying-job/v2'}}};

function runtime(t) {
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'jy-quality-runtime-'));
  t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  return new WorkflowRuntime({stateRoot:root});
}

function executableRuntime(t) {
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'jy-quality-state-'));
  t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  return new WorkflowRuntime({stateRoot:root,executor:()=>({artifacts:[{output_id:'main',path:'/tmp/output-main'}]}),
    verifier:()=>({ok:true,evidence:[{level:'structural',sha256:'9'.repeat(64)}]})});
}

function reachEvaluating(t) {
  const run=executableRuntime(t);
  const state=run.start({compilation,revision:1,budget:{currency:'CNY',maximum:10},iterationPolicy:POLICY});
  const binding=run.approvalBinding(state.run_id);
  run.approve(state.run_id,{...binding,user_id:'u',expires_at:'2999-01-01T00:00:00Z'});
  assert.equal(run.execute(state.run_id).stage,'rendering_proxy');
  const base={schema:'jianying-evidence-bundle/v1',workflow_id:'VLOG-01',revision:1,output_id:'main',
    artifact_digest:'4'.repeat(64),items:[
      {evidence_id:'proxy-main',type:'proxy',digest:'5'.repeat(64),validator:'probe/v1',environment:'fixture',
        observed_at:'2026-09-21T00:00:00Z',passed:true,artifact_ref:'proxy-main',limitations:[]},
      {evidence_id:'technical-main',type:'technical',digest:'6'.repeat(64),validator:'probe/v1',environment:'fixture',
        observed_at:'2026-09-21T00:00:00Z',passed:true,artifact_ref:'proxy-main',limitations:[]},
    ],conclusion:'incomplete',metadata:{}};
  assert.equal(run.recordProxyEvidence(state.run_id,base).stage,'evaluating');
  return {run,runId:state.run_id};
}

test('quality approval binds targets profiles policy verdict request cost and evaluator scope',t=>{
  const run=runtime(t);
  const state=run.start({compilation,revision:1,budget:{currency:'CNY',maximum:10},iterationPolicy:POLICY});
  const initial=run.approvalBinding(state.run_id);
  assert.deepEqual(initial.quality_contracts,{...quality,verdict_digest:null,revision_request_digest:null,
    accumulated_budget:{currency:'CNY',amount:0},evaluator_scope:null});
  for(const key of ['target_digests','profile_digests','iteration_policy_digest','accumulated_budget']) {
    const changed=structuredClone(initial);
    changed.quality_contracts[key]=key.endsWith('digests')?['9'.repeat(64)]:key==='iteration_policy_digest'?'9'.repeat(64):
      {currency:'CNY',amount:1};
    assert.throws(()=>run.approve(state.run_id,{...changed,user_id:'u',expires_at:'2999-01-01T00:00:00Z'}),
      error=>error.code==='approval_scope_mismatch');
  }
});

test('quality revision replaces compilation and requires bound verdict and request digests',t=>{
  const run=runtime(t);
  const state=run.start({compilation,revision:1,budget:{currency:'CNY',maximum:10},maximum_revisions:3,
    iterationPolicy:POLICY});
  const next=structuredClone(compilation);
  next.plan_digest='a'.repeat(64); next.receipt.execution_digest='b'.repeat(64);
  next.receipt.quality_contracts={target_digests:['c'.repeat(64)],profile_digests:['d'.repeat(64)],
    workflow_id:'VLOG-01',revision:2,iteration_policy_digest:qualityContractDigest(POLICY)};
  const request=buildRevisionRequest({verdict:CONTRACTS.evaluation_verdict,
    allowedActions:['trim'],availableCapabilities:['timeline.edit']});
  const revised=run.revise(state.run_id,{compilation:next,revision:2,
    verdict:CONTRACTS.evaluation_verdict,revisionRequest:request,
    accumulatedBudget:{currency:'CNY',amount:2},
    evaluatorScope:{provider:'manual',model:'reviewer',resource_digest:'0'.repeat(64)},
    modelCalls:1,completedHumanReviews:['before_revision_execution']});
  assert.equal(revised.compilation.plan_digest,'a'.repeat(64));
  const binding=run.approvalBinding(state.run_id);
  assert.equal(binding.quality_contracts.verdict_digest,qualityContractDigest(CONTRACTS.evaluation_verdict));
  assert.equal(binding.quality_contracts.revision_request_digest,qualityContractDigest(request));
  assert.equal(binding.quality_contracts.accumulated_budget.amount,2);
  assert.equal(binding.quality_contracts.evaluator_scope.resource_digest,'0'.repeat(64));
  const mutations=[
    value=>{value.plan_digest='1'.repeat(64);},
    value=>{value.execution_digest='1'.repeat(64);},
    value=>{value.job_digests=['1'.repeat(64)];},
    value=>{value.cli_sha256='1'.repeat(64);},
    value=>{value.targets=['/tmp/other'];},
    value=>{value.quality_contracts.target_digests=['1'.repeat(64)];},
    value=>{value.quality_contracts.profile_digests=['1'.repeat(64)];},
    value=>{value.quality_contracts.verdict_digest='1'.repeat(64);},
    value=>{value.quality_contracts.revision_request_digest='1'.repeat(64);},
    value=>{value.quality_contracts.accumulated_budget.amount=3;},
    value=>{value.quality_contracts.evaluator_scope.resource_digest='1'.repeat(64);},
  ];
  for(const mutate of mutations) {
    const changed=structuredClone(binding); mutate(changed);
    assert.throws(()=>run.approve(state.run_id,{...changed,user_id:'u',expires_at:'2999-01-01T00:00:00Z'}),
      error=>error.code==='approval_scope_mismatch');
  }
});

test('quality runtime records proxy evaluation revision human capability and stop states',t=>{
  let flow=reachEvaluating(t);
  assert.equal(flow.run.recordEvaluation(flow.runId,CONTRACTS.evaluation_verdict).stage,'revision_requested');
  assert.equal(flow.run.show(flow.runId).history.at(-1).event,'quality.revision_requested');

  flow=reachEvaluating(t);
  const blocked=structuredClone(CONTRACTS.evaluation_verdict); blocked.decision='blocked'; blocked.findings=[];
  assert.equal(flow.run.recordEvaluation(flow.runId,blocked).stage,'needs_human_review');
  assert.equal(flow.run.stopIteration(flow.runId,{reasons:['human decision required']}).stage,'iteration_stopped');

  flow=reachEvaluating(t);
  assert.equal(flow.run.markCapabilityBlocked(flow.runId,{capability:'timeline.transition',reason:'not supported'}).stage,
    'capability_blocked');
  assert.equal(flow.run.stopIteration(flow.runId,{reasons:['capability unavailable']}).terminal_state,'iteration_stopped');
});
