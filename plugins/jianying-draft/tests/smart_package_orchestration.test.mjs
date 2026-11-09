import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import {fileURLToPath} from 'node:url';

import {
  buildSmartPackageRequest,
  decomposeSmartPackageProposal,
  executeSmartPackageWithRecovery,
  mapSmartPackageOperation,
  mapSmartPackageStyle,
} from '../scripts/smart_package_orchestration.mjs';
import {canonical,sha256,validateSchema} from '../scripts/workflow_data.mjs';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const request=buildSmartPackageRequest({requestId:'smart-vlog-1',workflowId:'workflow-vlog',styleId:'life_vlog',
  inputAssets:['asset-main'],allowedTracks:['video','caption','sticker','audio','effect'],
  protectedContent:{dialogue_ids:['dialogue-1'],brand_claim_ids:['brand-1'],segment_ids:['locked-1']},
  budget:{currency:'CNY',maximum:100},preview:{required:true,human_approval_required:true},maximumDurationMs:30_000});
const change=(change_id,type,track,start_ms=0,duration_ms=1_000,overrides={})=>({change_id,type,action:'add',track,
  start_ms,duration_ms,target_ids:[],content_digest:'a'.repeat(64),...overrides});
const changes=[
  change('broll','b_roll','video'),change('caption','caption','caption'),change('fancy','fancy_text','sticker'),
  change('sound','sound_effect','audio'),change('effect','effect','effect'),change('transition','transition','video'),
];
const proposal={schema:'jianying-smart-package-proposal/v1',request_digest:request.request_digest,
  change_set_id:'changes-vlog-1',status:'preview_ready',preview:{artifact_digest:'b'.repeat(64)},changes,
  unexplained_changes:[],estimated_cost:50};

test('six smart-package styles map to open route tags and unknown styles fail closed',()=>{
  const styles=['smart_recommended','technology','life_vlog','marketing_sales','knowledge','variety_entertainment'];
  for(const style of styles) {
    const mapped=mapSmartPackageStyle(style);
    assert.equal(mapped.style_id,style);
    assert.ok(mapped.route_tags.includes('smart-package'));
  }
  assert.throws(()=>mapSmartPackageStyle('unknown'),error=>error.code==='smart_package_style_unknown');
});

test('smart rough cut and script rough cut expose an explicit five-stage lifecycle',()=>{
  for(const operationId of ['smart_rough_cut','script_rough_cut']) {
    const operation=mapSmartPackageOperation(operationId);
    assert.equal(operation.operation_id,operationId);
    assert.ok(operation.route_tags.includes('rough-cut'));
    const operationRequest=buildSmartPackageRequest({requestId:`request-${operationId}`,workflowId:'workflow-rough-cut',
      operationId,styleId:'knowledge',inputAssets:['asset-main'],allowedTracks:['video','caption','audio'],
      protectedContent:{dialogue_ids:[],brand_claim_ids:[],segment_ids:[]},budget:{currency:'CNY',maximum:0},
      preview:{required:true,human_approval_required:true},maximumDurationMs:60_000});
    assert.equal(operationRequest.operation.operation_id,operationId);
    assert.deepEqual(operationRequest.lifecycle.stages,['plan','preview','approve','apply','verify']);
    assert.deepEqual(operationRequest.lifecycle.failure_recovery,
      {snapshot_before_apply:true,ambiguous_apply:'restore',verification_failure:'restore'});
    const schema=JSON.parse(fs.readFileSync(path.join(ROOT,'schemas','smart-package-request.v1.schema.json'),'utf8'));
    assert.doesNotThrow(()=>validateSchema(operationRequest,schema));
  }
  assert.throws(()=>mapSmartPackageOperation('coordinate_macro'),error=>error.code==='smart_package_operation_unknown');
});

test('request, proposal decomposition and evidence have strict machine contracts',async()=>{
  const changeSet=decomposeSmartPackageProposal({request,proposal});
  assert.equal(changeSet.change_count,6);
  for(const type of ['b_roll','caption','fancy_text','sound_effect','effect','transition'])
    assert.equal(changeSet.groups[type].length,1);
  const approval={schema:'jianying-smart-package-approval/v1',status:'approved',approval_id:'approval-vlog',
    request_digest:request.request_digest,change_set_digest:changeSet.change_set_digest,expires_at:'2099-01-01T00:00:00.000Z'};
  const adapter={async snapshot(){return {snapshot_id:'snapshot-1'};},
    async preview(){return {status:'ready',artifact_digest:proposal.preview.artifact_digest};},
    async apply(){return {status:'applied',application_id:'apply-1'};},
    async inspect(){return {changes:structuredClone(changes),unexplained_changes:[]};},
    async restore(){throw new Error('successful execution must not restore');}};
  const evidence=await executeSmartPackageWithRecovery({request,proposal,approval,adapter});
  assert.equal(evidence.status,'verified');
  assert.deepEqual(evidence.state_trace.map(item=>item.stage),['plan','preview','approve','apply','verify']);
  assert.equal(evidence.state_trace.at(-1).status,'verified');
  assert.equal(evidence.evidence_digest,sha256(canonical({request,changeSet,approval,
    snapshot:{snapshot_id:'snapshot-1'},preview:{status:'ready',artifact_digest:proposal.preview.artifact_digest},
    applied:{status:'applied',application_id:'apply-1'},inspection:{changes,unexplained_changes:[]},
    stateTrace:evidence.state_trace})));
  for(const [name,value] of [['smart-package-request.v1.schema.json',request],['smart-package-proposal.v1.schema.json',proposal],
    ['smart-package-evidence.v1.schema.json',evidence]]) {
    const schema=JSON.parse(fs.readFileSync(path.join(ROOT,'schemas',name),'utf8'));
    assert.doesNotThrow(()=>validateSchema(value,schema));
  }
});

test('unapproved, unexplained and over-budget package proposals cannot apply',async()=>{
  assert.throws(()=>decomposeSmartPackageProposal({request,proposal:{...proposal,unexplained_changes:[{kind:'mystery'}]}}),
    error=>error.code==='smart_package_unexplained_changes');
  assert.throws(()=>decomposeSmartPackageProposal({request,proposal:{...proposal,estimated_cost:101}}),
    error=>error.code==='smart_package_proposal_invalid');
  let applyCalled=false;
  await assert.rejects(()=>executeSmartPackageWithRecovery({request,proposal,approval:{schema:'jianying-smart-package-approval/v1',
    status:'approved',approval_id:'bad',request_digest:request.request_digest,change_set_digest:'0'.repeat(64),
    expires_at:'2099-01-01T00:00:00.000Z'},adapter:{async apply(){applyCalled=true;}}}),
  error=>error.code==='smart_package_approval_required');
  assert.equal(applyCalled,false);
});

test('smart package request attaches as preview, review, apply and verify WorkflowPlan subgraph',async()=>{
  const {attachSmartPackageWorkflow,validateWorkflowPlan}=await import('../scripts/workflow_plan.mjs');
  const plan={schema:'jianying-workflow-plan/v1',workflow_id:'workflow-vlog',revision:1,
    catalog_ref:{schema:'jianying-planning-catalog/v2',digest:'c'.repeat(64)},tool_requirements:{capabilities:['timeline.edit']},
    brief:{request_id:'vlog'},assets:[],route:{kind:'known'},outputs:[],steps:[],limits:{maximum_revisions:3},
    risk_requirements:[],proof_requirements:[],metadata:{}};
  const attached=attachSmartPackageWorkflow(plan,request);
  assert.deepEqual(attached.steps.map(step=>step.type),['smart_package_preview','smart_package_review',
    'smart_package_apply','smart_package_verify']);
  assert.ok(attached.tool_requirements.capabilities.includes('runtime.smart_package'));
  assert.equal(attached.steps[2].approval_requirements[0].type,'human_confirmation');
  assert.equal(attached.steps[2].reconcile.strategy,'inspect_before_retry');
  assert.equal(validateWorkflowPlan(attached).valid,true);
  const bypass=structuredClone(attached); bypass.steps[2].depends_on=[];
  assert.throws(()=>validateWorkflowPlan(bypass),error=>error.code==='workflow_graph_invalid');
});

test('protected dialogue, brand drift, range overflow and ambiguous apply restore the snapshot',async()=>{
  const changeSet=decomposeSmartPackageProposal({request,proposal});
  const approval={schema:'jianying-smart-package-approval/v1',status:'approved',approval_id:'approval-vlog',
    request_digest:request.request_digest,change_set_digest:changeSet.change_set_digest,expires_at:'2099-01-01T00:00:00.000Z'};
  const cases=[
    {code:'smart_package_protected_dialogue',actual:[...changes,change('bad-dialogue','caption','caption',0,1_000,
      {action:'remove',target_ids:['dialogue-1']})]},
    {code:'smart_package_protected_brand',actual:[...changes,change('bad-brand','fancy_text','sticker',0,1_000,
      {action:'update',target_ids:['brand-1']})]},
    {code:'smart_package_change_invalid',actual:[...changes,change('bad-range','effect','effect',29_500,1_000)]},
  ];
  for(const item of cases) {
    let restored=0;
    const adapter={async snapshot(){return {snapshot_id:`snapshot-${item.code}`};},
      async preview(){return {status:'ready',artifact_digest:proposal.preview.artifact_digest};},
      async apply(){return {status:'applied'};},async inspect(){return {changes:item.actual,unexplained_changes:[]};},
      async restore(){restored+=1; return {status:'restored'};}};
    await assert.rejects(()=>executeSmartPackageWithRecovery({request,proposal,approval,adapter}),error=>{
      assert.equal(error.code,item.code); assert.equal(error.details.recovered,true);
      assert.deepEqual(error.details.state_trace.map(entry=>entry.stage),
        ['plan','preview','approve','apply','verify','recover']);
      assert.equal(error.details.state_trace.at(-1).status,'restored'); return true;
    });
    assert.equal(restored,1);
  }
  let ambiguousRestores=0;
  const ambiguous={async snapshot(){return {snapshot_id:'snapshot-ambiguous'};},
    async preview(){return {status:'ready',artifact_digest:proposal.preview.artifact_digest};},
    async apply(){return {status:'ambiguous'};},async inspect(){throw new Error('must not inspect');},
    async restore(){ambiguousRestores+=1; return {status:'restored'};}};
  await assert.rejects(()=>executeSmartPackageWithRecovery({request,proposal,approval,adapter:ambiguous}),error=>{
    assert.equal(error.code,'smart_package_apply_ambiguous'); assert.equal(error.details.recovered,true);
    assert.deepEqual(error.details.state_trace.map(item=>item.stage),['plan','preview','approve','apply','recover']);
    assert.equal(error.details.state_trace.at(-1).status,'restored'); return true;
  });
  assert.equal(ambiguousRestores,1);
});
