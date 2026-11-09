import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';

import {
  applyNativeResource,
  nativeResourceRequestDigest,
  removeNativeResource,
} from '../scripts/native_resource_application.mjs';
import {
  attachNativeResourceAcquisition,
  attachNativeResourceApplicationWorkflow,
  validateWorkflowPlan,
} from '../scripts/workflow_plan.mjs';
import {validateSchema} from '../scripts/workflow_data.mjs';

function assertSchema(name,value) {
  const schema=JSON.parse(fs.readFileSync(new URL(`../schemas/${name}`,import.meta.url),'utf8'));
  assert.doesNotThrow(()=>validateSchema(value,schema));
}

const acquisition={schema:'jianying-native-resource-acquisition/v1',request_id:'acquire-sticker',state:'ready',
  adapter:{kind:'fake_gui',editor_bundle:'com.lemon.lvpro',editor_version:'11.5.13243',adapter_version:'1'},
  candidates:{accepted:[],rejected:[]},selected:{resource_id:'sticker-vlog-1',domain:'sticker'},download_trace:[],
  receipt:{schema_version:'jianying-official-resource-receipt/v1',asset_id:'sticker-vlog-1'},
  native_action_evidence:{},cli:{register:{status:'registered'},preflight:{status:'ready'}},artifacts:{}};

function applicationRequest(root) {
  return {schema:'jianying-native-resource-application-request/v1',request_id:'apply-sticker',
    acquisition_request_id:'acquire-sticker',resource_id:'sticker-vlog-1',domain:'sticker',
    draft_path:path.join(root,'draft'),target:{track_id:'stickers',start_ms:1_000,duration_ms:2_000}};
}

function approval(request,id='approval-1') {
  return {schema:'jianying-native-resource-approval/v1',status:'approved',approval_id:id,
    request_digest:nativeResourceRequestDigest(request),expires_at:'2099-01-01T00:00:00.000Z'};
}

function adapter({applyStatus='applied',removeStatus='removed',inspectStatus='present'}={}) {
  const calls=[];
  return {calls,access_token:'must-never-be-persisted',
    identity:{kind:'fake_gui',editor_bundle:'com.lemon.lvpro',editor_version:'11.5.13243',adapter_version:'1'},
    async preview(){calls.push('preview');return {status:'ready',artifact_digest:'a'.repeat(64)};},
    async snapshot(){calls.push('snapshot');return {snapshot_id:`snapshot-${calls.length}`};},
    async apply(){calls.push('apply');return {status:applyStatus,application_id:'application-1'};},
    async inspect(_request,{expected}){calls.push('inspect');return {status:inspectStatus,
      resource_id:expected.resource_id,target_digest:expected.target_digest};},
    async remove(){calls.push('remove');return {status:removeStatus,removal_id:'removal-1'};},
    async restore(){calls.push('restore');return {status:'restored'};}};
}

test('preview snapshot apply and inspect persist a secret-free verified application',async t=>{
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'jianying-resource-apply-'));
  t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  const request=applicationRequest(root),gui=adapter();
  const result=await applyNativeResource({acquisition,request,approval:approval(request),adapter:gui,stateRoot:root});
  assert.equal(result.schema,'jianying-native-resource-application/v1');
  assert.equal(result.state,'verified');
  assert.deepEqual(gui.calls,['preview','snapshot','apply','inspect']);
  assert.deepEqual(result.actions.map(item=>item.action),['preview','apply','inspect']);
  assertSchema('native-resource-application.v1.schema.json',result);
  const persisted=fs.readFileSync(result.artifacts.application_path,'utf8');
  assert.doesNotMatch(persisted,/must-never-be-persisted|access_token/i);
});

test('ambiguous application restores the pre-apply snapshot and never reports success',async t=>{
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'jianying-resource-ambiguous-'));
  t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  const request=applicationRequest(root),gui=adapter({applyStatus:'ambiguous'});
  await assert.rejects(()=>applyNativeResource({acquisition,request,approval:approval(request),adapter:gui,stateRoot:root}),error=>{
    assert.equal(error.code,'native_resource_apply_ambiguous');
    assert.equal(error.details.recovered,true);
    return true;
  });
  assert.deepEqual(gui.calls,['preview','snapshot','apply','restore']);
});

test('local removal verifies absence and an ambiguous removal restores its snapshot',async t=>{
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'jianying-resource-remove-'));
  t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  const request=applicationRequest(root),appliedGui=adapter();
  const application=await applyNativeResource({acquisition,request,approval:approval(request),adapter:appliedGui,stateRoot:root});
  const removal={schema:'jianying-native-resource-removal-request/v1',request_id:'remove-sticker',
    resource_id:application.resource_id,draft_path:application.draft_path,target_digest:application.target_digest,
    application_digest:application.application_digest};
  const removalGui=adapter({inspectStatus:'absent'});
  const removed=await removeNativeResource({application,request:removal,approval:approval(removal,'approval-remove'),
    adapter:removalGui,stateRoot:root});
  assert.equal(removed.state,'verified_removed');
  assert.deepEqual(removalGui.calls,['snapshot','remove','inspect']);
  assertSchema('native-resource-removal.v1.schema.json',removed);

  const ambiguousGui=adapter({removeStatus:'ambiguous'});
  await assert.rejects(()=>removeNativeResource({application,request:{...removal,request_id:'remove-again'},
    approval:approval({...removal,request_id:'remove-again'},'approval-remove-again'),adapter:ambiguousGui,stateRoot:root}),error=>{
    assert.equal(error.code,'native_resource_remove_ambiguous');
    assert.equal(error.details.recovered,true);
    return true;
  });
  assert.deepEqual(ambiguousGui.calls,['snapshot','remove','restore']);
});

test('WorkflowPlan hands an acquired receipt to approved application and independent inspection',()=>{
  const plan={schema:'jianying-workflow-plan/v1',workflow_id:'workflow-resource-application',revision:1,
    catalog_ref:{schema:'jianying-planning-catalog/v2',digest:'c'.repeat(64)},tool_requirements:{capabilities:[]},
    brief:{request_id:'resource-application'},assets:[],route:{kind:'known'},outputs:[],steps:[],
    limits:{maximum_revisions:3},risk_requirements:[],proof_requirements:[],metadata:{}};
  const query={schema:'jianying-native-resource-query/v1',request_id:'acquire-sticker',domain:'sticker',
    keywords:['生活 Vlog'],filters:{maximum_cost_microunits:0},selection:{strategy:'ranked',maximum_candidates:5}};
  const acquired=attachNativeResourceAcquisition(plan,query);
  const request=applicationRequest('/tmp/jianying-native-resource-workflow');
  const bound=attachNativeResourceApplicationWorkflow(acquired,request);

  assert.deepEqual(bound.steps.map(step=>step.type),[
    'native_resource_search','native_resource_filter','native_resource_acquire',
    'native_resource_apply','native_resource_inspect',
  ]);
  const acquireStep=bound.steps[2],applyStep=bound.steps[3],inspectStep=bound.steps[4];
  assert.deepEqual(applyStep.depends_on,[acquireStep.id]);
  assert.equal(applyStep.inputs[0].artifact_ref,acquireStep.outputs[0].artifact_ref);
  assert.ok(applyStep.capabilities.includes('media.official_resource_apply'));
  assert.deepEqual(applyStep.approval_requirements,[
    {type:'human_confirmation',scope:'native resource apply-sticker'},
  ]);
  assert.deepEqual(inspectStep.depends_on,[applyStep.id]);
  assert.equal(inspectStep.inputs[0].artifact_ref,applyStep.outputs[0].artifact_ref);
  assert.equal(validateWorkflowPlan(bound).valid,true);

  const bypass=structuredClone(bound);
  bypass.steps[4].depends_on=[];
  assert.throws(()=>validateWorkflowPlan(bypass),error=>error.code==='workflow_graph_invalid');
});
