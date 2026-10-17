import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, writeFileSync, rmSync, symlinkSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import { Ledger } from '../scripts/harness/ledger.ts';
import { ReviewStore } from '../src/evaluation/review_store.ts';
import { strictJson } from '../src/strict_json.ts';

function fixture() {
  const root=mkdtempSync(join(tmpdir(),'vectorcraft-ledger-'));
  const source=join(root,'source.vectorcraft');writeFileSync(source,'native');
  const ledger=new Ledger(join(root,'state.sqlite'));
  const binding={planHash:'a'.repeat(64),inputHashes:{},projectRevision:createHash('sha256').update('native').digest('hex'),runtimeIdentity:'c'.repeat(64),
    authorization:{objects:[2],fields:['paint.color'],deadline:Date.now()+60000,maxAttempts:2,maxBytes:1000}};
  return {root,source,ledger,binding,close(){ledger.close();rmSync(root,{recursive:true,force:true});}};
}

test('single writer keys the source resource, not output path; epochs fence old writers',()=>{
  const f=fixture();try {
    const a=f.ledger.claim('one',f.source,join(f.root,'out1'),f.binding);
    assert.throws(()=>f.ledger.claim('two',f.source,join(f.root,'out2'),f.binding),/resource_busy/);
    const alias=join(f.root,'alias.vectorcraft');symlinkSync(f.source,alias);
    assert.throws(()=>f.ledger.claim('three',alias,join(f.root,'out3'),f.binding),/resource_busy/);
    f.ledger.intent(a.id,a.epoch,0,{command:'save'},100);
    f.ledger.unknown(a.id,a.epoch,'response lost');
    f.ledger.close();
    const reopened=new Ledger(join(f.root,'state.sqlite'));
    assert.equal(reopened.get(a.id).state,'reconciling');
    assert.throws(()=>reopened.intent(a.id,a.epoch,0,{command:'save'},100),/reconcile_required/);
    assert.throws(()=>reopened.reconcile(a.id,a.epoch,{stopped:false,verified:true}),/native_stop_unconfirmed/);
    assert.throws(()=>reopened.reconcile(a.id,a.epoch,{stopped:true,verified:true}),/native_observation_required/);
    assert.equal(reopened.get(a.id).state,'reconciling');
    assert.throws(()=>reopened.claim('unsafe-release',f.source,join(f.root,'unsafe'),f.binding),/resource_busy/);
    reopened.close();
  } finally {f.close();}
});

test('idempotency binds input, authorization and runtime; budget and cancellation persist',()=>{
  const f=fixture();try {
    const a=f.ledger.claim('one',f.source,join(f.root,'out'),f.binding);
    assert.equal(f.ledger.claim('one',f.source,join(f.root,'out'),f.binding).id,a.id);
    assert.throws(()=>f.ledger.claim('one',f.source,join(f.root,'out'),{...f.binding,runtimeIdentity:'d'.repeat(64)}),/idempotency_conflict/);
    f.ledger.intent(a.id,a.epoch,0,{command:'edit'},600);
    f.ledger.receipt(a.id,a.epoch,0,{saved:true});
    assert.throws(()=>f.ledger.intent(a.id,a.epoch,1,{command:'edit'},600),/budget_exceeded/);
    f.ledger.cancel(a.id,a.epoch,false);
    assert.equal(f.ledger.get(a.id).state,'cancel_requested');
    assert.throws(()=>f.ledger.intent(a.id,a.epoch,1,{command:'edit'},1),/cancel_requested/);
    assert.throws(()=>f.ledger.cancel(a.id,a.epoch,true),/native_observation_required/);
    assert.equal(f.ledger.get(a.id).state,'cancel_requested');
    assert.equal(f.ledger.get(a.id).bytesReserved,600);
  } finally {f.close();}
});

test('single-round review binds fresh source, candidate, target and rubric and rejects duplicates',()=>{
  const f=fixture();const store=new ReviewStore(join(f.root,'review.sqlite'));
  try {
    const candidate=join(f.root,'preview.png'),target=join(f.root,'brief.txt'),rubric=join(f.root,'rubric.json');
    writeFileSync(candidate,'pixels');writeFileSync(target,'Logo');writeFileSync(rubric,'vector rubric');
    const request=store.request({projectRevision:f.binding.projectRevision,runtimeIdentity:f.binding.runtimeIdentity,
      native:f.source,candidates:[candidate],targets:[{path:target,role:'target'}],rubric,exchangeLoss:f.source,
      technicalStatus:'FAIL',authorization:f.binding.authorization});
    const receipt={schema:'vectorcraft-review-receipt/v1',requestId:request.id,bindingHash:request.bindingHash,
      reviewer:{kind:'human',identity:'designer',contextOrigin:'manual',independenceEvidence:null},
      verdict:'accept',issues:[],scores:{structure:4,text:4,brand:4,layout:4,legibility:4}};
    const result=store.importReceipt(receipt);
    assert.equal(result.state,'technical_failed');
    assert.throws(()=>store.importReceipt(receipt),/duplicate_review_receipt/);
    const second=store.request({...request.input,technicalStatus:'PASS'});
    writeFileSync(target,'Changed target');
    assert.throws(()=>store.importReceipt({...receipt,requestId:second.id,bindingHash:second.bindingHash}),/stale_review_binding/);
    assert.throws(()=>store.revision(second.id,[{objectId:3,field:'paint.color',value:'#fff'}]),/stale_review_binding/);
  } finally {store.close();f.close();}
});

test('strict review JSON rejects duplicate keys, overflow, malformed values and accepts business error',()=>{
  for(const value of ['{"a":1,"a":2}','{"a":{"x":1,"x":2}}','{"x":1e999}','{"x":NaN}','{"a":1,}']) {
    assert.throws(()=>strictJson(value),/invalid_json|duplicate_json_key|nonfinite_json_value/);
  }
  assert.deepEqual(strictJson('{"id":2,"error":"business data","items":[true,null,1]}'),{id:2,error:'business data',items:[true,null,1]});
});

test('revision proposals require actual assessed fields and preserve authorization without claiming independence',()=>{
  const f=fixture();const store=new ReviewStore(join(f.root,'reviews.sqlite'));
  try {
    const target=join(f.root,'brief.txt'),rubric=join(f.root,'rubric.json');writeFileSync(target,'logo');writeFileSync(rubric,'rubric');
    const request=store.request({projectRevision:f.binding.projectRevision,runtimeIdentity:f.binding.runtimeIdentity,native:f.source,
      candidates:[f.source],targets:[{path:target,role:'target'}],rubric,exchangeLoss:f.source,technicalStatus:'PASS',authorization:{...f.binding.authorization,fields:['paint.color','text.content']}});
    const receipt={schema:'vectorcraft-review-receipt/v1',requestId:request.id,bindingHash:request.bindingHash,
      reviewer:{kind:'host-model',identity:'test model',contextOrigin:'same test context',independenceEvidence:'self-declaration'},
      verdict:'revise',issues:[{objectId:2,field:'paint.color',message:'adjust brand value',evidence:['candidate']}],
      scores:{structure:4,text:4,brand:2,layout:4,legibility:4}};
    assert.equal(store.importReceipt(receipt).independent,false);
    const proposal=store.revision(request.id,[{objectId:2,field:'paint.color',value:'#175cce'}]);
    assert.equal(proposal.state,'proposed');
    assert.throws(()=>store.revision(request.id,[{objectId:2,field:'text.content',value:'unassessed'}]),/revision_not_assessed/);
    assert.throws(()=>store.revision(request.id,[{objectId:3,field:'paint.color',value:'#175cce'}]),/revision_outside_authorization/);
  }finally{store.close();f.close();}
});


test('child tasks share one durable budget and late cancellation receipts are quarantined',()=>{
  const f=fixture();try {
    const binding={...f.binding,authorization:{...f.binding.authorization,budgetId:'review-round-one',maxAttempts:1,maxBytes:1000}};
    const first=f.ledger.claim('parent',f.source,join(f.root,'parent'),binding);
    const childSource=join(f.root,'child.vectorcraft');writeFileSync(childSource,'child');
    const child=f.ledger.claim('child',childSource,join(f.root,'child'),binding);
    f.ledger.intent(first.id,first.epoch,0,{command:'edit'},600);
    assert.throws(()=>f.ledger.intent(child.id,child.epoch,0,{command:'edit'},100),/budget_exceeded/);
    f.ledger.cancel(first.id,first.epoch,false);
    assert.equal(f.ledger.receipt(first.id,first.epoch,0,{artifact:'late'}).state,'quarantined');
    const step=f.ledger.db.prepare('SELECT state,result FROM steps WHERE task=?').get(first.id) as any;
    assert.equal(step.state,'quarantined');assert.deepEqual(JSON.parse(step.result),{artifact:'late'});
  }finally{f.close();}
});

test('review request rejects a claimed revision that differs from actual native bytes',()=>{
  const f=fixture();const store=new ReviewStore(join(f.root,'reviews.sqlite'));
  try {
    const input={projectRevision:'0'.repeat(64),runtimeIdentity:f.binding.runtimeIdentity,native:f.source,candidates:[f.source],targets:[{path:f.source,role:'target'}],rubric:f.source,exchangeLoss:f.source,technicalStatus:'PASS',authorization:f.binding.authorization};
    assert.throws(()=>store.request(input),/project_revision_mismatch/);
  }finally{store.close();f.close();}
});


test('review binds exchange loss and persists rejection reasons across restart',()=>{
  const f=fixture();let store=new ReviewStore(join(f.root,'reviews.sqlite'));
  try {
    const loss=join(f.root,'loss.json');writeFileSync(loss,'{"lost":[],"unknown":[]}');
    const request=store.request({projectRevision:f.binding.projectRevision,runtimeIdentity:f.binding.runtimeIdentity,native:f.source,candidates:[f.source],targets:[{path:f.source,role:'target'}],rubric:f.source,exchangeLoss:loss,technicalStatus:'PASS',authorization:f.binding.authorization});
    writeFileSync(loss,'{"lost":["editable PDF"],"unknown":[]}');
    const receipt={schema:'vectorcraft-review-receipt/v1',requestId:request.id,bindingHash:request.bindingHash,
      reviewer:{kind:'human',identity:'reviewer',contextOrigin:'manual',independenceEvidence:null},verdict:'accept',issues:[],scores:{structure:4,text:4,brand:4,layout:4,legibility:4}};
    assert.throws(()=>store.importReceipt(receipt),/stale_review_binding/);
    store.close();store=new ReviewStore(join(f.root,'reviews.sqlite'));
    const event=store.db.prepare('SELECT reason FROM review_events WHERE request=?').get(request.id) as any;
    assert.match(event.reason,/stale_review_binding/);
  }finally{store.close();f.close();}
});

test('pending reviews survive restart and any bound source, candidate or rubric replacement invalidates acceptance',()=>{
  const f=fixture();let store=new ReviewStore(join(f.root,'review-freshness.sqlite'));
  try {
    const paths={native:join(f.root,'native.vectorcraft'),candidate:join(f.root,'frame.png'),target:join(f.root,'goal.txt'),rubric:join(f.root,'rubric.json')};
    for(const path of Object.values(paths))writeFileSync(path,'original');
    const input={projectRevision:createHash('sha256').update('original').digest('hex'),runtimeIdentity:f.binding.runtimeIdentity,native:paths.native,candidates:[paths.candidate],targets:[{path:paths.target,role:'target'}],rubric:paths.rubric,exchangeLoss:f.source,technicalStatus:'PASS',authorization:f.binding.authorization};
    for(const path of Object.values(paths)){
      const request=store.request(input);store.close();store=new ReviewStore(join(f.root,'review-freshness.sqlite'));
      assert.equal(store.current(request.id).state,'pending');
      const receipt={schema:'vectorcraft-review-receipt/v1',requestId:request.id,bindingHash:request.bindingHash,reviewer:{kind:'human',identity:'reviewer',contextOrigin:'manual',independenceEvidence:null},verdict:'accept',issues:[],scores:{structure:4,text:4,brand:4,layout:4,legibility:4}};
      assert.throws(()=>store.importReceipt({...receipt,scores:{...receipt.scores,text:5}}),/invalid_review_receipt/);
      assert.equal(store.current(request.id).state,'pending');
      writeFileSync(path,'replaced');assert.throws(()=>store.importReceipt(receipt),/stale_review_binding/);writeFileSync(path,'original');
    }
  }finally{store.close();f.close();}
});

test('review target and authorization schemas reject undeclared target keys and invalid scopes',()=>{
  const f=fixture();const store=new ReviewStore(join(f.root,'schema.sqlite'));
  try{
    const input={projectRevision:f.binding.projectRevision,runtimeIdentity:f.binding.runtimeIdentity,native:f.source,candidates:[f.source],targets:[{path:f.source,role:'target'}],rubric:f.source,exchangeLoss:f.source,technicalStatus:'PASS',authorization:f.binding.authorization};
    assert.throws(()=>store.request({...input,targets:[{...input.targets[0],execute:true}]}),/invalid_review_request/);
    assert.throws(()=>store.request({...input,authorization:{...input.authorization,objects:[-1]}}),/invalid_review_request/);
    assert.throws(()=>store.request({...input,authorization:{...input.authorization,fields:[null]}}),/invalid_review_request/);
  }finally{store.close();f.close();}
});
