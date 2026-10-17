import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync,mkdirSync,writeFileSync,readFileSync,rmSync,cpSync,statSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join,dirname } from 'node:path';
import { pathToFileURL,fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
const ROOT=fileURLToPath(new URL('../',import.meta.url));
const hash=(v:string|Buffer)=>createHash('sha256').update(v).digest('hex');
async function fixture(){
 const root=mkdtempSync(join(tmpdir(),'vector isolated checker ')),plugin=join(root,'plugin');mkdirSync(plugin);
 cpSync(join(ROOT,'src'),join(plugin,'src'),{recursive:true});cpSync(join(ROOT,'scripts/harness'),join(plugin,'scripts/harness'),{recursive:true});
 const dependency=join(plugin,'skills/vectorcraft-harness/scripts/exchange_loss.py');mkdirSync(dirname(dependency),{recursive:true});cpSync(join(ROOT,'skills/vectorcraft-harness/scripts/exchange_loss.py'),dependency);cpSync(join(ROOT,'skills/vectorcraft-harness/scripts/asset_reader.py'),join(dirname(dependency),'asset_reader.py'));
 const {ReviewStore}=await import(pathToFileURL(join(plugin,'src/evaluation/review_store.ts')).href);
 const {TechnicalReview}=await import(pathToFileURL(join(plugin,'src/evaluation/technical_review.ts')).href);
 const source=join(root,'delivery');mkdirSync(source);const native=join(source,'project.vectorcraft'),candidate=join(source,'preview.png');
 writeFileSync(native,'unit-native-identity');writeFileSync(candidate,Buffer.from('\x89PNG\r\n\x1a\ncorrupt','binary'));
 const files={'project.vectorcraft':hash(readFileSync(native)),'preview.png':hash(readFileSync(candidate))};writeFileSync(join(source,'manifest.json'),JSON.stringify({schema:'vectorcraft-delivery/v1',runtimeSha256:'a'.repeat(64),files,outputs:[{path:'preview.png'}],fontDependencies:[]}));
 const target=join(root,'brief.txt'),rubric=join(root,'rubric.json'),loss=join(root,'loss.json');writeFileSync(target,'isolated unit checker');writeFileSync(rubric,'{}');writeFileSync(loss,'{}');
 const input={projectRevision:files['project.vectorcraft'],runtimeIdentity:'a'.repeat(64),native,candidates:[candidate],targets:[{path:target,role:'target'}],rubric,exchangeLoss:loss,technicalStatus:'PASS',authorization:{objects:[2],fields:['paint.color'],deadline:Date.now()+30000,maxAttempts:3,maxBytes:4*1024*1024,budgetId:'checker-budget',readRoots:[root],writeRoots:[root]}};
 const path=join(root,'review.sqlite');return {root,plugin,dependency,input,path,ReviewStore,TechnicalReview,close:()=>rmSync(root,{recursive:true,force:true})};
}
for(const changed of ['skills/vectorcraft-harness/scripts/exchange_loss.py','skills/vectorcraft-harness/scripts/asset_reader.py','scripts/harness/asset_digest.py','scripts/harness/authorized_file.ts','scripts/harness/authorized_write.ts','scripts/harness/authorized_write.py','scripts/harness/authorized_tree.ts','scripts/harness/authorized_tree.py'])test(`checked review binds ${changed} and rejects its drift after restart`,async()=>{
 const f=await fixture();let store=new f.ReviewStore(f.path,[f.root]);
 try{
  const request=await new f.TechnicalReview(store).request(f.input);
  assert.equal(request.input.technicalEvidence.checkerFiles['skills/vectorcraft-harness/scripts/exchange_loss.py'],hash(readFileSync(f.dependency)));
  const task=store.db.prepare('SELECT output FROM tasks WHERE id=?').get(request.input.technicalCheckId) as any;
  for(const [name,digest] of Object.entries(request.input.technicalEvidence.checkerFiles)){const path=join(task.output,'checker',name);assert.equal(hash(readFileSync(path)),digest);assert.equal(statSync(path).mode&0o777,0o400);}
  store.close();const dependency=join(f.plugin,changed);writeFileSync(dependency,readFileSync(dependency,'utf8')+'\n// isolated drift\n');store=new f.ReviewStore(f.path,[f.root]);
  assert.throws(()=>store.current(request.id),/stale_review_binding/);
 }finally{store.close();f.close();}
});
test('first checked request cannot settle persisted checked evidence after dependency drift',async()=>{
 const f=await fixture();const store=new f.ReviewStore(f.path,[f.root]);
 try{
  const original=store.requestFromCheck.bind(store);let changed=false;
  store.requestFromCheck=(input:any,id:string)=>{if(!changed){changed=true;writeFileSync(f.dependency,readFileSync(f.dependency,'utf8')+'\n# isolated handoff drift\n');}return original(input,id);};
  await assert.rejects(()=>new f.TechnicalReview(store).request(f.input),/stale_review_binding/);
 }finally{store.close();f.close();}
});

test('older checked evidence without a complete checker bundle must be checked again',async()=>{
 const f=await fixture();const store=new f.ReviewStore(f.path,[f.root]);
 try{
  const request=await new f.TechnicalReview(store).request(f.input);
  const input=JSON.parse(JSON.stringify(request.input));delete input.technicalEvidence.checkerFiles;
  store.db.prepare('UPDATE reviews SET input=? WHERE id=?').run(JSON.stringify(input),request.id);
  assert.throws(()=>store.current(request.id),/stale_review_binding/);
  const row=store.db.prepare('SELECT report FROM technical_checks WHERE task=?').get(request.input.technicalCheckId) as any;
  const report=JSON.parse(row.report);delete report.checkerFiles;const raw=JSON.stringify(report);
  store.db.prepare('UPDATE technical_checks SET report=?,report_sha=?,review_id=NULL WHERE task=?').run(raw,hash(raw),request.input.technicalCheckId);
  assert.throws(()=>store.requestFromCheck(f.input,request.input.technicalCheckId),/stale_review_binding/);
 }finally{store.close();f.close();}
});
