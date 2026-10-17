import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync,mkdirSync,writeFileSync,readFileSync,rmSync,chmodSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import { ReviewStore } from '../src/evaluation/review_store.ts';
import { TechnicalReview } from '../src/evaluation/technical_review.ts';

const hash=(value:string|Buffer)=>createHash('sha256').update(value).digest('hex');
function fixture(extension='png'){
  const root=mkdtempSync(join(tmpdir(),'vector checked review ')),source=join(root,'delivery');mkdirSync(source);
  const native=join(source,'project.vectorcraft'),candidate=join(source,'preview.'+extension),extra=join(source,'auxiliary.txt');
  writeFileSync(native,'unit native identity, not actual native acceptance');writeFileSync(candidate,extension==='png'?Buffer.from('\x89PNG\r\n\x1a\ncorrupt','binary'):'unsupported format');writeFileSync(extra,'auxiliary');
  const files=Object.fromEntries([native,candidate,extra].map(path=>[path.slice(source.length+1),hash(readFileSync(path))]));
  writeFileSync(join(source,'manifest.json'),JSON.stringify({schema:'vectorcraft-delivery/v1',runtimeSha256:'a'.repeat(64),files,outputs:[{path:candidate.slice(source.length+1)}],fontDependencies:[]}));
  const target=join(root,'brief.txt'),rubric=join(root,'rubric.json'),loss=join(root,'loss.json');writeFileSync(target,'Logo');writeFileSync(rubric,'{}');writeFileSync(loss,'{}');
  const input={projectRevision:files['project.vectorcraft'],runtimeIdentity:'a'.repeat(64),native,candidates:[candidate],targets:[{path:target,role:'target'}],rubric,exchangeLoss:loss,technicalStatus:'PASS',
    authorization:{objects:[2],fields:['paint.color'],deadline:Date.now()+30000,maxAttempts:3,maxBytes:4*1024*1024,budgetId:'shared-review-budget',readRoots:[root],writeRoots:[root]}};
  return {root,source,extra,input,database:join(root,'review.sqlite'),close:()=>rmSync(root,{recursive:true,force:true})};
}
const receipt=(request:any)=>({schema:'vectorcraft-review-receipt/v1',requestId:request.id,bindingHash:request.bindingHash,
  reviewer:{kind:'human',identity:'unit fixture reviewer',contextOrigin:'explicit supplied fixture',independenceEvidence:null},verdict:'accept',issues:[],scores:{structure:4,text:4,brand:4,layout:4,legibility:4}});

test('checked requests use actual decode failures, persist evidence, and cannot be visually promoted',async()=>{
  const f=fixture();let store=new ReviewStore(f.database,[f.root]);
  try{
    const checked=new TechnicalReview(store),request=await checked.request(f.input);
    assert.equal(request.input.technicalStatus,'FAIL');assert.equal(request.input.technicalEvidence.engineeringStatus,'NOT_RUN');
    assert.equal(request.input.technicalEvidenceOrigin,'checked-decoder');
    const second=await checked.request(f.input);assert.equal(second.id,request.id);
    const usage=store.db.prepare('SELECT attempts FROM budgets WHERE id=?').get('shared-review-budget') as any;assert.equal(usage.attempts,1);
    store.close();store=new ReviewStore(f.database,[f.root]);
    const result=store.importReceipt(receipt(request));assert.equal(result.state,'technical_failed');assert.equal(result.acceptanceStatus,'blocked');assert.equal(result.creativeStatus,'PASS');
  }finally{store.close();f.close();}
});

test('unsupported decoding stays pending and all delivered files remain bound',async()=>{
  const f=fixture('unknown');const store=new ReviewStore(f.database,[f.root]);
  try{
    const request=await new TechnicalReview(store).request(f.input);assert.equal(request.input.technicalStatus,'NOT_RUN');
    const result=store.importReceipt(receipt(request));assert.equal(result.state,'technical_pending');assert.equal(result.acceptanceStatus,'pending');
    writeFileSync(f.extra,'changed auxiliary');assert.throws(()=>store.current(request.id),/stale_review_binding/);
  }finally{store.close();f.close();}
});

test('checked evidence cannot be injected through the legacy JSON request entry',()=>{
  const f=fixture();const store=new ReviewStore(f.database,[f.root]);
  try{assert.throws(()=>store.request({...f.input,technicalEvidence:{technicalStatus:'PASS'},technicalEvidenceOrigin:'checked-decoder'}),/technical_evidence_requires_check/);}
  finally{store.close();f.close();}
});

test('readonly decoder cancellation consumes its shared attempt and does not replay after restart',async()=>{
  const f=fixture();let store=new ReviewStore(f.database,[f.root]);
  try{
    const wrapper=join(f.root,'slow-python.sh');writeFileSync(wrapper,'#!/bin/sh\nsleep 10\n');chmodSync(wrapper,0o700);
    f.input.authorization.deadline=Date.now()+700;
    await assert.rejects(()=>new TechnicalReview(store).request(f.input,{python:wrapper}),/technical_check_interrupted/);
    assert.equal((store.db.prepare('SELECT attempts FROM budgets WHERE id=?').get('shared-review-budget') as any).attempts,1);
    store.close();store=new ReviewStore(f.database,[f.root]);
    await assert.rejects(()=>new TechnicalReview(store).request(f.input,{python:wrapper}),/reconcile_required/);
  }finally{store.close();f.close();}
});
