import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync,mkdirSync,writeFileSync,readFileSync,rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
const cli=fileURLToPath(new URL('../src/cli.ts',import.meta.url));
const hash=(value:string|Buffer)=>createHash('sha256').update(value).digest('hex');

test('public receipt CLI restores persisted checked read roots after restart without allowing receipt roots injection',()=>{
 const root=mkdtempSync(join(tmpdir(),'vector receipt roots ')),delivery=join(root,'delivery'),state=join(root,'state');mkdirSync(delivery);mkdirSync(state);
 try{
  const native=join(delivery,'project.vectorcraft'),preview=join(delivery,'preview.png'),target=join(delivery,'target.txt'),rubric=join(delivery,'rubric.json');
  writeFileSync(native,'explicit unit native identity');writeFileSync(preview,Buffer.from('\x89PNG\r\n\x1a\ncorrupt','binary'));writeFileSync(target,'unit brief');writeFileSync(rubric,'{}');
  const files={'project.vectorcraft':hash(readFileSync(native)),'preview.png':hash(readFileSync(preview))};
  writeFileSync(join(delivery,'manifest.json'),JSON.stringify({schema:'vectorcraft-delivery/v1',runtimeSha256:'a'.repeat(64),files,outputs:[{path:'preview.png'}],fontDependencies:[]}));
  const db=join(state,'reviews.sqlite'),requestFile=join(root,'request.json');
  const call=(action:string,input:any)=>{writeFileSync(requestFile,JSON.stringify(input));return spawnSync(process.execPath,[cli,action,db,requestFile],{encoding:'utf8',timeout:15000});};
  const input={native,candidates:[preview],targets:[{path:target,role:'target'}],rubric,exchangeLoss:rubric,projectRevision:files['project.vectorcraft'],runtimeIdentity:'a'.repeat(64),technicalStatus:'PASS',readRoots:[delivery],authorization:{objects:[2],fields:['paint.color'],deadline:Date.now()+30000,maxAttempts:4,maxBytes:4*1024*1024,budgetId:'roots-unit',readRoots:[delivery],writeRoots:[state]}};
  const checked=call('review-checked',input);assert.equal(checked.status,0,checked.stderr);const request=JSON.parse(checked.stdout);
  const receipt={schema:'vectorcraft-review-receipt/v1',requestId:request.id,bindingHash:request.bindingHash,reviewer:{kind:'human',identity:'explicit unit fixture',contextOrigin:'unit',independenceEvidence:null},verdict:'accept',issues:[],scores:{structure:4,text:4,brand:4,layout:4,legibility:4}};
  const forged=call('review-import',{...receipt,readRoots:[root]});assert.notEqual(forged.status,0);assert.match(forged.stderr,/invalid_review_receipt/);
  const imported=call('review-import',receipt);assert.equal(imported.status,0,imported.stderr);const result=JSON.parse(imported.stdout);
  assert.equal(result.state,'technical_failed');assert.equal(result.acceptanceStatus,'blocked');assert.equal(result.technicalStatus,'FAIL');assert.equal(result.engineeringStatus,'NOT_RUN');
  assert.notEqual(call('review-import',receipt).status,0);
 }finally{rmSync(root,{recursive:true,force:true});}
});
