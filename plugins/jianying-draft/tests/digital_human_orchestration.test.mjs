import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import {fileURLToPath} from 'node:url';

import {
  buildDigitalHumanPreviewPlan,
  buildDigitalHumanRequest,
  refreshDigitalHumanTask,
  searchDigitalHumanCatalog,
  submitOrResumeDigitalHumanTask,
  verifyDigitalHumanArtifact,
} from '../scripts/digital_human_orchestration.mjs';
import {validateSchema} from '../scripts/workflow_data.mjs';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const persona={kind:'persona',resource_id:'persona-host-1',name:'知识主播',categories:['knowledge'],edition:'professional',
  allowed_usages:['personal','commercial'],rank:1,cost_microunits:10};
const voice={kind:'voice',resource_id:'voice-cn-1',name:'清晰女声',categories:['knowledge'],edition:'professional',
  allowed_usages:['personal','commercial'],languages:['zh-CN'],styles:['clear'],rank:1,cost_microunits:20};
const catalog={schema:'jianying-digital-human-catalog/v1',editor_identity:{bundle_id:'com.lemon.lvpro',version:'11.5.13243'},
  edition_observation:{edition:'professional',status:'active'},personas:[persona],voices:[voice],
  observed_at:'2026-09-22T02:00:00.000Z'};

function stockRequest(overrides={}) {
  return buildDigitalHumanRequest({workflowId:'workflow-course',selection:{persona:{source:'stock',resource_id:persona.resource_id},
    voice:{source:'stock',resource_id:voice.resource_id,rate:1,pitch:0}},script:{text:'欢迎学习本课程',language:'zh-CN',reviewed:true},
    background:{kind:'color',value:'#101820'},usage:{purpose:'commercial',channel:'douyin'},
    entitlement:{edition:'professional',status:'active'},budget:{currency:'CNY',maximum_microunits:100},
    provider:'jianying-cloud',...overrides});
}

test('stock catalog search selects a compatible persona and voice then builds a no-submit preview plan',()=>{
  const selection=searchDigitalHumanCatalog({catalog,query:{category:'knowledge',usage:'commercial',language:'zh-CN',
    voice_style:'clear',edition:'professional',maximum_cost_microunits:100}});
  assert.equal(selection.selected.persona.resource_id,persona.resource_id);
  assert.equal(selection.selected.voice.resource_id,voice.resource_id);
  const request=stockRequest();
  const preview=buildDigitalHumanPreviewPlan({request});
  assert.equal(preview.submit_allowed,false);
  assert.equal(preview.upload_required,false);
  for(const [name,value] of [['digital-human-catalog.v1.schema.json',catalog],
    ['digital-human-request.v1.schema.json',request],['digital-human-preview-plan.v1.schema.json',preview]]) {
    const schema=JSON.parse(fs.readFileSync(path.join(ROOT,'schemas',name),'utf8'));
    assert.doesNotThrow(()=>validateSchema(value,schema));
  }
});

test('custom likeness and voice require exact portrait, voice and upload approvals',()=>{
  const common={workflowId:'workflow-custom',selection:{persona:{source:'custom'},voice:{source:'custom'}},
    script:{text:'授权测试',language:'zh-CN',reviewed:true},background:{kind:'transparent'},
    usage:{purpose:'commercial',channel:'douyin'},entitlement:{edition:'professional',status:'active'},
    budget:{currency:'CNY',maximum_microunits:100},provider:'jianying-cloud',
    customAssets:{likeness:['portrait-sha'],voice:['voice-sha']},now:1_795_000_000_000};
  assert.throws(()=>buildDigitalHumanRequest(common),error=>error.code==='digital_human_approval_required');
  const approval=(type,id,asset_ids)=>({schema:'jianying-digital-human-approval/v1',type,status:'approved',approval_id:id,
    asset_ids,provider:'jianying-cloud',purpose:'commercial:douyin',expires_at:'2099-01-01T00:00:00.000Z'});
  const request=buildDigitalHumanRequest({...common,approvals:[approval('portrait_rights','portrait-rights',['portrait-sha']),
    approval('voice_rights','voice-rights',['voice-sha']),approval('upload','portrait-upload',['portrait-sha']),
    approval('upload','voice-upload',['voice-sha'])]});
  assert.deepEqual(request.approval_ids,['portrait-rights','portrait-upload','voice-rights','voice-upload']);
  assert.equal(buildDigitalHumanPreviewPlan({request}).upload_required,true);
});

test('digital human request attaches as inventory, preview, approval, submit, resume and verify subgraph',async()=>{
  const {attachDigitalHumanWorkflow,validateWorkflowPlan}=await import('../scripts/workflow_plan.mjs');
  const request=stockRequest();
  const plan={schema:'jianying-workflow-plan/v1',workflow_id:'workflow-course',revision:1,
    catalog_ref:{schema:'jianying-planning-catalog/v2',digest:'c'.repeat(64)},tool_requirements:{capabilities:['timeline.edit']},
    brief:{request_id:'course'},assets:[],route:{kind:'known'},outputs:[],steps:[],limits:{maximum_revisions:3},
    risk_requirements:[],proof_requirements:[],metadata:{}};
  const attached=attachDigitalHumanWorkflow(plan,request);
  assert.deepEqual(attached.steps.map(step=>step.type),['digital_human_inventory','digital_human_preview',
    'digital_human_approve','digital_human_submit','digital_human_resume','digital_human_verify']);
  assert.ok(attached.tool_requirements.capabilities.includes('runtime.digital_human'));
  assert.deepEqual(attached.steps[3].approval_requirements.map(item=>item.type),['human_confirmation','external_service']);
  assert.equal(attached.steps[3].retry.maximum_attempts,1);
  assert.equal(validateWorkflowPlan(attached).valid,true);
  const bypass=structuredClone(attached); bypass.steps[4].depends_on=[];
  assert.throws(()=>validateWorkflowPlan(bypass),error=>error.code==='workflow_graph_invalid');
});

test('stable request ID submits once, resumes by remote task ID and verifies the artifact',async t=>{
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'jianying-digital-human-')); t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  const request=stockRequest(),records=new Map(); let submits=0,statusCalls=0;
  const ledger={async load(id){return records.get(id)??null;},async save(id,value){records.set(id,structuredClone(value));}};
  const artifactPath=path.join(root,'avatar.mp4'); fs.writeFileSync(artifactPath,'digital-human-video');
  const artifact={schema:'jianying-digital-human-artifact/v1',request_id:request.request_id,path:artifactPath,
    sha256:crypto.createHash('sha256').update('digital-human-video').digest('hex'),
    byte_length:fs.statSync(artifactPath).size,duration_ms:5_000,canvas:{width:1080,height:1920}};
  const provider={name:'jianying-cloud',version:'1',async estimate(){return {cost_microunits:50};},
    async submit(_request,options){submits+=1; assert.equal(options.idempotency_key,request.request_id);
      return {vendor_request_id:'vendor-1',remote_task_id:'task-1',status:'submitted'};},
    async status(remoteTaskId){statusCalls+=1; assert.equal(remoteTaskId,'task-1');
      return {status:'completed',actual_cost_microunits:48,artifact};}};
  const first=await submitOrResumeDigitalHumanTask({request,provider,ledger});
  const second=await submitOrResumeDigitalHumanTask({request,provider,ledger});
  assert.equal(first.action,'submitted'); assert.equal(second.action,'resume'); assert.equal(submits,1);
  const completed=await refreshDigitalHumanTask({request,provider,ledger});
  assert.equal(completed.status,'completed'); assert.equal(statusCalls,1);
  const evidence=verifyDigitalHumanArtifact({request,task:completed});
  assert.equal(evidence.status,'verified');
  for(const [name,value] of [['digital-human-artifact.v1.schema.json',artifact],
    ['digital-human-evidence.v1.schema.json',evidence]]) {
    const schema=JSON.parse(fs.readFileSync(path.join(ROOT,'schemas',name),'utf8'));
    assert.doesNotThrow(()=>validateSchema(value,schema));
  }
});

test('over-budget and ambiguous submission never silently resubmit',async()=>{
  const request=stockRequest(),records=new Map(); let submits=0;
  const ledger={async load(id){return records.get(id)??null;},async save(id,value){records.set(id,structuredClone(value));}};
  const expensive={name:'jianying-cloud',version:'1',async estimate(){return {cost_microunits:101};},
    async submit(){submits+=1;},async status(){return {status:'running'};}};
  await assert.rejects(()=>submitOrResumeDigitalHumanTask({request,provider:expensive,ledger}),
    error=>error.code==='digital_human_budget_exceeded');
  assert.equal(submits,0);
  const ambiguous={name:'jianying-cloud',version:'1',async estimate(){return {cost_microunits:50};},
    async submit(){submits+=1; return {vendor_request_id:'vendor-ambiguous',status:'submitted'};},
    async status(){return {status:'running'};}};
  await assert.rejects(()=>submitOrResumeDigitalHumanTask({request,provider:ambiguous,ledger}),error=>{
    assert.equal(error.code,'digital_human_submit_ambiguous'); assert.equal(error.details.resubmit_allowed,false); return true;
  });
  await assert.rejects(()=>submitOrResumeDigitalHumanTask({request,provider:ambiguous,ledger}),
    error=>error.code==='digital_human_submit_ambiguous');
  assert.equal(submits,1);
});

test('status ambiguity is persisted and requires reconciliation instead of submit',async()=>{
  const request=stockRequest(),records=new Map(); let submits=0;
  const ledger={async load(id){return records.get(id)??null;},async save(id,value){records.set(id,structuredClone(value));}};
  const provider={name:'jianying-cloud',version:'1',async estimate(){return {cost_microunits:50};},
    async submit(){submits+=1; return {vendor_request_id:'vendor-2',remote_task_id:'task-2',status:'running'};},
    async status(){return {status:'ambiguous'};}};
  await submitOrResumeDigitalHumanTask({request,provider,ledger});
  await assert.rejects(()=>refreshDigitalHumanTask({request,provider,ledger}),
    error=>error.code==='digital_human_status_ambiguous');
  assert.equal((await ledger.load(request.request_id)).status,'ambiguous');
  await assert.rejects(()=>submitOrResumeDigitalHumanTask({request,provider,ledger}),
    error=>error.code==='digital_human_submit_ambiguous');
  assert.equal(submits,1);
});
