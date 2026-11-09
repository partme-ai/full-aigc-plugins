import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import crypto from 'node:crypto';
import os from 'node:os';
import path from 'node:path';
import contracts from './fixtures/quality-loop/contracts.json' with {type:'json'};
import {createRemoteModelEvaluator} from '../scripts/remote_quality_evaluator.mjs';

const root=()=>fs.mkdtempSync(path.join(os.tmpdir(),'jianying-remote-eval-'));
const result={decision:'revise',evidence_refs:['probe-main'],scores:[{dimension_id:'narrative',value:6,passed:false}],
  hard_gates:[],findings:[],limitations:[]};
const budget={currency:'CNY',maximum:1};
const approval=(adapter,input,profile,approvedBudget=budget)=>({schema:'jianying-model-upload-approval/v1',scope:adapter.approvalScope({input,profile,budget:approvedBudget}),
  user_id:'reviewer',expires_at:new Date(Date.now()+60_000).toISOString()});
const digest=value=>crypto.createHash('sha256').update(value).digest('hex');

test('remote provider requires exact upload approval and records bounded cost',async()=>{
  let calls=0;
  const adapter=createRemoteModelEvaluator({provider:'approved-loopback',model:'quality-v1',version:'2026-09-21',
    endpoint:'http://127.0.0.1/evaluate',credential:'secret-never-logged',stateRoot:root(),
    transport:async()=>{calls++;return {status:200,body:JSON.stringify(result),cost:{currency:'CNY',amount:0.2}};}});
  await assert.rejects(()=>adapter.evaluate({input:contracts.evaluation_input,profile:contracts.quality_profile,budget}),
    error=>error.code==='model_upload_approval_required');
  const verdict=await adapter.evaluate({input:contracts.evaluation_input,profile:contracts.quality_profile,budget,
    approval:approval(adapter,contracts.evaluation_input,contracts.quality_profile)});
  assert.equal(verdict.decision,'revise');assert.equal(calls,1);
  const ledgerFile=fs.readdirSync(adapter.ledger.stateRoot).map(name=>path.join(adapter.ledger.stateRoot,name,'ledger.json'))[0];
  const ledger=JSON.parse(fs.readFileSync(ledgerFile));
  assert.equal(ledger.state,'succeeded');assert.deepEqual(ledger.cost,{currency:'CNY',amount:0.2});
  assert.doesNotMatch(JSON.stringify(ledger),/secret-never-logged/);
});

test('OpenAI-compatible request uses model/messages and reconciles provider usage against approved rate card',async()=>{
  let sent;
  const priced={currency:'CNY',maximum:1,rate_card:{version:'provider-price-2026-09-21',
    input_per_million:2,output_per_million:8,cached_input_per_million:0.5}};
  const adapter=createRemoteModelEvaluator({provider:'approved-loopback',model:'quality-v1',version:'1',
    endpoint:'http://localhost/evaluate',credential:'secret',stateRoot:root(),transport:async request=>{sent=request.body;return {
      status:200,body:JSON.stringify({request_id:'dashscope-request-1',choices:[{message:{content:JSON.stringify(result)}}],
        usage:{prompt_tokens:100,completion_tokens:20,prompt_tokens_details:{cached_tokens:40}}})};}});
  const verdict=await adapter.evaluate({input:contracts.evaluation_input,profile:contracts.quality_profile,budget:priced,
    approval:approval(adapter,contracts.evaluation_input,contracts.quality_profile,priced)});
  assert.equal(verdict.decision,'revise');assert.equal(sent.model,'quality-v1');assert.equal(sent.response_format.type,'json_object');
  assert.equal(sent.messages.length,2);assert.equal(Object.hasOwn(sent,'input'),false);
  const ledgerFile=fs.readdirSync(adapter.ledger.stateRoot).map(name=>path.join(adapter.ledger.stateRoot,name,'ledger.json'))[0];
  const ledger=JSON.parse(fs.readFileSync(ledgerFile));
  assert.deepEqual(ledger.cost,{currency:'CNY',amount:0.0003,usage:{prompt_tokens:100,cached_prompt_tokens:40,
    completion_tokens:20},rate_card_version:'provider-price-2026-09-21'});
  assert.equal(ledger.artifact.provider_request_id,'dashscope-request-1');
});

test('approved proxy media is digest checked and transmitted as a bounded video data URL',async()=>{
  const stateRoot=root(),mediaRoot=root(),mediaPath=path.join(mediaRoot,'proxy.mp4');
  const bytes=Buffer.from('small-approved-video-proxy');fs.writeFileSync(mediaPath,bytes);
  const input=structuredClone(contracts.evaluation_input);
  input.artifacts[0].digest=digest(bytes);input.artifacts[0].bytes=bytes.length;
  const resources=[{artifact_id:'proxy-main',path:mediaPath,mime_type:'video/mp4'}];
  let sent;
  const adapter=createRemoteModelEvaluator({provider:'approved-loopback',model:'quality-v1',version:'1',
    endpoint:'http://localhost/evaluate',credential:'secret',stateRoot,maxUploadBytes:1024,
    transport:async request=>{sent=request.body;return {status:200,body:JSON.stringify(result),
      provider_request_id:'provider-request-1',cost:{currency:'CNY',amount:0.01}};}});
  const scope=adapter.approvalScope({input,profile:contracts.quality_profile,budget,resources});
  assert.deepEqual(scope.resource_ids,['proxy-main']);assert.deepEqual(scope.resource_digests,[digest(bytes)]);
  assert.deepEqual(scope.resources,[{artifact_id:'proxy-main',digest:digest(bytes),mime_type:'video/mp4',bytes:bytes.length}]);
  const uploadApproval={schema:'jianying-model-upload-approval/v1',scope,user_id:'reviewer',
    expires_at:new Date(Date.now()+60_000).toISOString()};
  const verdict=await adapter.evaluate({input,profile:contracts.quality_profile,budget,resources,approval:uploadApproval});
  assert.equal(verdict.decision,'revise');
  const content=sent.messages[1].content;
  assert.equal(content[0].type,'video_url');assert.equal(content[0].video_url.url,`data:video/mp4;base64,${bytes.toString('base64')}`);
  assert.equal(content.at(-1).type,'text');assert.doesNotMatch(JSON.stringify(sent),new RegExp(mediaPath));
  const ledgerFile=path.join(stateRoot,fs.readdirSync(stateRoot)[0],'ledger.json');
  const ledgerText=fs.readFileSync(ledgerFile,'utf8');
  assert.doesNotMatch(ledgerText,new RegExp(mediaPath));assert.doesNotMatch(ledgerText,/c21hbGwtYXBwcm92ZWQ/);
});

test('changed, oversized, undeclared and symlink upload resources fail before transport',async()=>{
  const mediaRoot=root(),mediaPath=path.join(mediaRoot,'proxy.mp4'),bytes=Buffer.from('approved');fs.writeFileSync(mediaPath,bytes);
  const input=structuredClone(contracts.evaluation_input);input.artifacts[0].digest=digest(bytes);input.artifacts[0].bytes=bytes.length;
  let calls=0;
  const adapter=createRemoteModelEvaluator({provider:'approved-loopback',model:'quality-v1',version:'1',endpoint:'http://localhost/evaluate',
    credential:'secret',stateRoot:root(),maxUploadBytes:8,transport:async()=>{calls++;return {};}});
  const resources=[{artifact_id:'proxy-main',path:mediaPath,mime_type:'video/mp4'}];
  const scope=adapter.approvalScope({input,profile:contracts.quality_profile,budget,resources});
  const uploadApproval={schema:'jianying-model-upload-approval/v1',scope,user_id:'reviewer',expires_at:new Date(Date.now()+60_000).toISOString()};
  fs.writeFileSync(mediaPath,Buffer.from('modified'));
  await assert.rejects(()=>adapter.evaluate({input,profile:contracts.quality_profile,budget,resources,approval:uploadApproval}),
    error=>error.code==='model_upload_resource_changed');
  fs.writeFileSync(mediaPath,bytes);const symlink=path.join(mediaRoot,'proxy-link.mp4');fs.symlinkSync(mediaPath,symlink);
  assert.throws(()=>adapter.approvalScope({input,profile:contracts.quality_profile,budget,
    resources:[{artifact_id:'proxy-main',path:symlink,mime_type:'video/mp4'}]}),error=>error.code==='model_upload_resource_invalid');
  assert.throws(()=>adapter.approvalScope({input,profile:contracts.quality_profile,budget,
    resources:[{artifact_id:'missing',path:mediaPath,mime_type:'video/mp4'}]}),error=>error.code==='model_upload_resource_invalid');
  const tiny=createRemoteModelEvaluator({provider:'approved-loopback',model:'quality-v1',version:'1',endpoint:'http://localhost/evaluate',
    credential:'secret',stateRoot:root(),maxUploadBytes:4,transport:async()=>{calls++;return {};}});
  assert.throws(()=>tiny.approvalScope({input,profile:contracts.quality_profile,budget,resources}),
    error=>error.code==='model_upload_limit_exceeded');
  assert.equal(calls,0);
});

test('timeout stays ambiguous and cannot silently repeat a paid request',async()=>{
  let calls=0;const stateRoot=root();
  const adapter=createRemoteModelEvaluator({provider:'approved-loopback',model:'quality-v1',version:'1',
    endpoint:'http://localhost/evaluate',credential:'secret',stateRoot,transport:async()=>{calls++;throw new Error('timeout token=secret');}});
  const request={input:contracts.evaluation_input,profile:contracts.quality_profile,budget};request.approval=approval(adapter,request.input,request.profile);
  await assert.rejects(()=>adapter.evaluate(request));
  await assert.rejects(()=>adapter.evaluate(request),error=>error.code==='side_effect_reconciliation_required');
  assert.equal(calls,1);assert.doesNotMatch(fs.readFileSync(path.join(stateRoot,fs.readdirSync(stateRoot)[0],'ledger.json'),'utf8'),/token=secret/);
});

test('oversized and provider-specific result fields fail closed',async()=>{
  for(const body of ['x'.repeat(200),JSON.stringify({...result,provider_trace:'forbidden'})]) {
    const adapter=createRemoteModelEvaluator({provider:'approved-loopback',model:'quality-v1',version:'1',endpoint:'http://localhost/evaluate',
      credential:'secret',stateRoot:root(),maxResponseBytes:body.startsWith('x')?64:4096,transport:async()=>({status:200,body})});
    await assert.rejects(()=>adapter.evaluate({input:contracts.evaluation_input,profile:contracts.quality_profile,budget,
      approval:approval(adapter,contracts.evaluation_input,contracts.quality_profile)}));
  }
});
