import test from 'node:test';
import assert from 'node:assert/strict';

import fs from 'node:fs';
import path from 'node:path';

import {attachQualityLoop,validateWorkflowPlan} from '../scripts/workflow_plan.mjs';
import {compileWorkflow} from '../scripts/workflow_compiler.mjs';

const ROOT=path.resolve(import.meta.dirname,'..');
const QUALITY=JSON.parse(fs.readFileSync(path.join(ROOT,'tests/fixtures/quality-loop/contracts.json'),'utf8'));

const CONTRACTS=[
  ['proxy_render','cli','Draft','ProxyMedia',['render.proxy'],[]],
  ['technical_validation','plugin','ProxyMedia','TechnicalEvidence',[],[]],
  ['creative_evaluation','model','EvaluationInput','EvaluationVerdict',['model.video.evaluate'],['external_service']],
  ['human_review','human','EvaluationInput','ReviewDecision',[],[]],
  ['revision_planning','plugin','EvaluationVerdict','RevisionRequest',[],[]],
  ['native_export','cli','Draft','NativeMedia',['render.native'],['human_confirmation']],
  ['delivery_validation','plugin','EvidenceBundle','DeliveryDecision',[],[]],
];

function plan(type,executor,input,output,capabilities=[],approvalTypes=[]) {
  return {schema:'jianying-workflow-plan/v1',workflow_id:`quality-${type}`,revision:1,
    catalog_ref:{},tool_requirements:{capabilities:[]},brief:{},assets:[],route:{},outputs:[],
    steps:[{id:`step-${type}`,type,type_version:'1',executor,depends_on:[],
      inputs:[{port:'input',data_type:input,artifact_ref:'external-input'}],
      outputs:[{port:'output',data_type:output,artifact_ref:`artifact-${type}`}],
      preconditions:[],capabilities,approval_requirements:approvalTypes.map(type=>({type,scope:`${type}:${type}`})),timeout_ms:300000,
      budget:{currency:'CNY',maximum:0},retry:{maximum_attempts:1,backoff_ms:0},
      reconcile:{strategy:'inspect_before_retry'},validator:{type:'artifact',version:'1',evidence_level:'structural'}}],
    limits:{},risk_requirements:[],proof_requirements:[],metadata:{}};
}

test('quality-loop steps are registered with fixed executors and typed ports',()=>{
  for(const contract of CONTRACTS) {
    assert.equal(validateWorkflowPlan(plan(...contract)).valid,true,contract[0]);
  }
});

test('quality-loop side effects require declared capabilities, approvals and complete policies',()=>{
  const proxy=plan(...CONTRACTS[0]); proxy.steps[0].capabilities=[];
  assert.throws(()=>validateWorkflowPlan(proxy),error=>error.code==='workflow_plan_invalid');
  const model=plan(...CONTRACTS[2]); model.steps[0].approval_requirements=[];
  assert.throws(()=>validateWorkflowPlan(model),error=>error.code==='workflow_plan_invalid');
  const native=plan(...CONTRACTS[5]); native.steps[0].budget.maximum=-1;
  assert.throws(()=>validateWorkflowPlan(native),error=>error.code==='workflow_plan_invalid');
  const wrongReconcile=plan(...CONTRACTS[5]); wrongReconcile.steps[0].reconcile.strategy='recompute';
  assert.throws(()=>validateWorkflowPlan(wrongReconcile),error=>error.code==='workflow_plan_invalid');
  const missingValidator=plan(...CONTRACTS[1]); missingValidator.steps[0].validator={};
  assert.throws(()=>validateWorkflowPlan(missingValidator),error=>error.code==='workflow_plan_invalid');
});

test('quality-loop steps reject executor, port and arbitrary handler overrides',()=>{
  const base=plan(...CONTRACTS[2]);
  for(const mutate of [
    value=>{value.steps[0].executor='cli';},
    value=>{value.steps[0].inputs[0].data_type='Text';},
    value=>{value.steps[0].outputs[0].data_type='JobBundle';},
    value=>{value.steps[0].handler='model://arbitrary';},
  ]) {
    const value=structuredClone(base); mutate(value);
    assert.throws(()=>validateWorkflowPlan(value),error=>['unsupported_step_type','workflow_plan_invalid'].includes(error.code));
  }
});

test('quality contracts bind WorkflowPlan and compilation receipt without leaking into Job v2',()=>{
  const base={schema:'jianying-workflow-plan/v1',workflow_id:'VLOG-01',revision:1,
    catalog_ref:{schema:'jianying-planning-catalog/v2',digest:'c'.repeat(64)},brief:{},assets:[],route:{},steps:[],
    limits:{},risk_requirements:[],proof_requirements:[],metadata:{},
    outputs:[{output_id:'main',purpose:'personal',format:'video',delivery:'editable_draft',target:{logical_path:'outputs/main'}}],
    tool_requirements:{capabilities:['timeline.edit']}};
  const first=attachQualityLoop(base,{creativeTargets:[QUALITY.creative_target],iterationPolicy:QUALITY.iteration_policy,
    qualityLoopOptIn:true});
  assert.equal(validateWorkflowPlan(first).valid,true);
  const cli={version:'1.6.14',sha256:'a'.repeat(64),jobSchema:'jianying-job/v2',capabilities:[
    {id:'schema.job_v2',status:'supported'},{id:'job.run',status:'supported'},{id:'timeline.edit',status:'supported'}]};
  const args={assetLedger:[{asset_id:'a',path:'/media/a.mp4',state:'verified',sha256:'b'.repeat(64),bytes:10,
    duration_us:6000000,streams:[{type:'video'}]}],decisions:[{output_id:'main',clips:[{asset_id:'a',in_us:0,out_us:3000000}]}],cliIdentity:cli};
  const compiled=compileWorkflow({plan:first,...args});
  assert.equal(compiled.receipt.quality_contracts.workflow_id,'VLOG-01');
  assert.equal(compiled.receipt.quality_contracts.revision,1);
  assert.match(compiled.receipt.quality_contracts.target_digests[0],/^[a-f0-9]{64}$/);
  assert.deepEqual(compiled.receipt.quality_contracts.profile_digests,['2'.repeat(64)]);
  assert.match(compiled.receipt.quality_contracts.iteration_policy_digest,/^[a-f0-9]{64}$/);
  assert.equal(JSON.stringify(compiled.job_bindings[0].job).includes('quality_profile'),false);
  const changed=structuredClone(QUALITY.creative_target); changed.narrative_goal='不同叙事目标';
  const second=compileWorkflow({plan:attachQualityLoop(base,{creativeTargets:[changed],iterationPolicy:QUALITY.iteration_policy,
    qualityLoopOptIn:true}),...args});
  assert.equal(compiled.job_bindings[0].job_digest,second.job_bindings[0].job_digest);
  assert.notEqual(compiled.receipt.semantic_digest,second.receipt.semantic_digest);
});

test('quality-loop attachment rejects output, workflow, revision and policy mismatches',()=>{
  const base={schema:'jianying-workflow-plan/v1',workflow_id:'VLOG-01',revision:1,catalog_ref:{},tool_requirements:{capabilities:[]},
    brief:{},assets:[],route:{},outputs:[{output_id:'main'}],steps:[],limits:{},risk_requirements:[],proof_requirements:[],metadata:{}};
  for(const mutate of [
    target=>{target.workflow_id='different';},
    target=>{target.revision=2;},
    target=>{target.quality_profiles[0].output_id='other';},
  ]) {
    const target=structuredClone(QUALITY.creative_target); mutate(target);
    assert.throws(()=>attachQualityLoop(base,{creativeTargets:[target],iterationPolicy:QUALITY.iteration_policy,
      qualityLoopOptIn:true}),
      error=>error.code==='workflow_plan_invalid');
  }
  assert.throws(()=>attachQualityLoop(base,{creativeTargets:[],iterationPolicy:QUALITY.iteration_policy,
    qualityLoopOptIn:true}),
    error=>error.code==='workflow_plan_invalid');
});
