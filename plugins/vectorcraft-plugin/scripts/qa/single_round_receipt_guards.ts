/** 当前原生单轮回执的失败／重启验收；创作分数复用已实际观察且同摘要的评审。 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,cpSync} from 'node:fs';
import {join} from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
const c=JSON.parse(readFileSync(process.argv[2],'utf8'));mkdirSync(c.output,{recursive:true});const source=join(c.output,'source');cpSync(c.source,source,{recursive:true});
const read=(p:string)=>JSON.parse(readFileSync(p,'utf8')),sha=(v:Buffer)=>createHash('sha256').update(v).digest('hex');
const {ReviewStore}=await import(pathToFileURL(join(c.installed,'src/evaluation/review_store.ts')).href),{TechnicalReview}=await import(pathToFileURL(join(c.installed,'src/evaluation/technical_review.ts')).href),{skillDigest}=await import(pathToFileURL(join(c.installed,'src/harness/controller.ts')).href);
const original=skillDigest(source),brief=join(c.output,'brief.txt'),rubric=join(c.output,'rubric.json'),reference=join(c.output,'judge-only.txt');
cpSync(c.brief,brief);cpSync(c.rubric,rubric);writeFileSync(reference,'Assessment context only; this is not target artwork and grants no edit authorization.');
const database=join(c.output,'state.sqlite'),roots=[c.output,c.runtime],manifest=read(join(source,'manifest.json'));
const input={native:join(source,'project.vectorcraft'),projectRevision:manifest.files['project.vectorcraft'],runtimeIdentity:manifest.runtimeSha256,candidates:manifest.outputs.map((x:any)=>join(source,x.path)),targets:[{path:brief,role:'target'},{path:reference,role:'judge-reference'}],rubric,exchangeLoss:join(source,'exchange-loss.json'),technicalStatus:'PASS',authorization:{objects:[2],fields:['appearance.items.0.paint'],deadline:Date.now()+120000,maxAttempts:3,maxBytes:64*1024*1024,budgetId:'single-round-receipt-guards',readRoots:roots,writeRoots:roots}};
let store=new ReviewStore(database,roots);const records:any[]=[];
const attempts=()=>Number((store.db.prepare('SELECT attempts FROM budgets WHERE id=?').get(input.authorization.budgetId) as any).attempts);
try{
 const request=await new TechnicalReview(store).request(input,{python:c.python});assert.equal(request.input.technicalStatus,'PASS');const count=Number((store.db.prepare('SELECT COUNT(*) AS n FROM reviews').get() as any).n);assert.equal(attempts(),1);
 store.close();store=new ReviewStore(database,roots);assert.equal(store.current(request.id).state,'pending');assert.equal(attempts(),1);assert.equal(Number((store.db.prepare('SELECT COUNT(*) AS n FROM reviews').get() as any).n),count);
 const reused=await new TechnicalReview(store).request(input,{python:c.python});assert.equal(reused.id,request.id);assert.equal(reused.state,'pending');assert.equal(attempts(),1);
 const assessment=read(c.assessment);assert.equal(assessment.projectRevision,input.projectRevision);assert.equal(assessment.previewSha256,sha(readFileSync(join(source,'artboard-1.png'))));
 const receipt={schema:'vectorcraft-review-receipt/v1',requestId:request.id,bindingHash:request.bindingHash,reviewer:assessment.reviewer,verdict:assessment.verdict,issues:assessment.issues,scores:assessment.scores};
 function refused(name:string,value:any,pattern:RegExp){const before=attempts(),events=Number((store.db.prepare('SELECT COUNT(*) AS n FROM review_events').get() as any).n);assert.throws(()=>store.importReceipt(value),pattern);assert.equal(attempts(),before);assert.equal(Number((store.db.prepare('SELECT COUNT(*) AS n FROM review_events').get() as any).n),events+1);records.push({case:name,result:'PASS',attemptsBefore:before,attemptsAfter:attempts(),rejectionPersisted:true});}
 refused('malformed-json','{"password":"synthetic-malformed-secret",',/invalid_review_json/);
 refused('duplicate-json-key','{"schema":"x","schema":"y"}',/invalid_review_json/);
 refused('schema-extra-field',{...receipt,unexpected:true},/invalid_review_receipt/);
 refused('binding-hash-mismatch',{...receipt,bindingHash:'0'.repeat(64)},/stale_review_binding/);
 for(const [name,path] of [['source',input.native],['candidate',join(source,'artboard-1.png')],['target',brief],['rubric',rubric]] as [string,string][]){const before=readFileSync(path);writeFileSync(path,Buffer.concat([before,Buffer.from('\nsynthetic mismatch')]));refused('stale-'+name,receipt,/stale_review_binding/);writeFileSync(path,before);assert.equal(store.current(request.id).state,'pending');}
 assert.equal(store.importReceipt(receipt).state,'revision_proposed');refused('duplicate-receipt',receipt,/duplicate_review_receipt/);
 assert.equal(skillDigest(source),original);assert.equal(attempts(),1);
 const events=store.db.prepare('SELECT request,reason,receipt FROM review_events ORDER BY n').all();assert(!JSON.stringify(events).includes('synthetic-malformed-secret'));
 const proof={schema:'vectorcraft-single-round-receipt-guards/v1',result:'PASS',pluginVersion:read(join(c.installed,'plugin.json')).version,sourceRef:read(join(c.installed,'skills.lock.json')).sources[0].ref,driverSha256:sha(readFileSync(process.argv[1])),request,records,events,pendingRecovered:true,pendingRequestReused:true,restartCreatedNewReview:false,sharedAttempts:attempts(),sourceUnchanged:true,targetRoleSeparated:true,scope:'Actual checked native input and current receipt handler; deliberate invalid/stale payload injection,not fresh creative scoring or independent model routing'};
 let encoded=JSON.stringify(proof,null,2)+'\n';for(const [from,to] of [[c.runtime,'RUNTIME'],[c.output,'GUARD_ROOT'],[c.installed,'PLUGIN']])encoded=encoded.split(from).join(to);writeFileSync(join(c.output,'proof.json'),encoded);console.log(JSON.stringify({result:'PASS',refusals:records.length,sharedAttempts:attempts()}));
}finally{store.close();}
