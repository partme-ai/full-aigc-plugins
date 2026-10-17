import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync,writeFileSync,rmSync,readFileSync,mkdirSync,chmodSync,cpSync,realpathSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { checkerFiles } from '../src/evaluation/checker_bundle.ts';
import { canonical } from '../src/strict_json.ts';
import { RevisionCycle } from '../src/evaluation/revision_cycle.ts';
import { ReviewStore } from '../src/evaluation/review_store.ts';

const hash=(v:string)=>createHash('sha256').update(v).digest('hex');
function fixture(){
 const root=mkdtempSync(join(tmpdir(),'bounded vector review ')),native=join(root,'project.vectorcraft'),preview=join(root,'preview.png'),brief=join(root,'brief.txt'),rubric=join(root,'rubric.json');
 for(const [p,v] of [[native,'native'],[preview,'pixels'],[brief,'brand'],[rubric,'{}']])writeFileSync(p,v);
 const store=new ReviewStore(join(root,'reviews.sqlite'),[root]);
 const input={native,projectRevision:hash('native'),runtimeIdentity:'a'.repeat(64),candidates:[preview],targets:[{path:brief,role:'target'}],rubric,exchangeLoss:rubric,technicalStatus:'PASS',authorization:{objects:[2],fields:['paint.color'],deadline:Date.now()+60000,maxAttempts:20,maxBytes:16*1024*1024,budgetId:'bounded-test',readRoots:[root],writeRoots:[root]}};
 const request=store.request(input);store.importReceipt({schema:'vectorcraft-review-receipt/v1',requestId:request.id,bindingHash:request.bindingHash,reviewer:{kind:'human',identity:'fixture only',contextOrigin:'test',independenceEvidence:null},verdict:'revise',issues:[{objectId:2,field:'paint.color',message:'fixture',evidence:['preview.png']}],scores:{structure:2,text:2,brand:2,layout:2,legibility:2}});
 return {root,store,input,request,close:()=>{try{store.close();}catch{}rmSync(root,{recursive:true,force:true});}};
}

test('a review assigned to a durable bounded cycle cannot bypass it through legacy revision',()=>{
 const f=fixture();try{
  f.store.db.exec('CREATE TABLE revision_members(review TEXT PRIMARY KEY,cycle TEXT NOT NULL);');
  f.store.db.prepare('INSERT INTO revision_members(review,cycle) VALUES(?,?)').run(f.request.id,'round-limit-reached');
  assert.throws(()=>f.store.revision(f.request.id,[{objectId:2,field:'paint.color',value:'#fff'}]),/revision_cycle_required/);
 }finally{f.close();}
});

// 仅用作状态机单元测试的可信数据库种子，不证明真实解码或原生工程接受。
function seedChecked(f:any,score=2,revision='native',directory=f.root){
 const native=join(directory,'project.vectorcraft'),preview=join(directory,'preview.png'),model=join(directory,'native.json'),manifest=join(directory,'manifest.json');
 writeFileSync(native,revision);writeFileSync(preview,'unit preview');writeFileSync(model,JSON.stringify({layers:[{id:2,paint:{color:'#000'}}]}));
 const digest=(p:string)=>createHash('sha256').update(readFileSync(p)).digest('hex');
 const files=Object.fromEntries([native,preview,model].map(p=>[p.slice(directory.length+1),digest(p)]));
 writeFileSync(manifest,JSON.stringify({schema:'vectorcraft-delivery/v1',runtimeSha256:f.input.runtimeIdentity,sourceProjectSha256:hash('native'),files,outputs:[{path:'preview.png'}],fontDependencies:[]}));
 const request=f.store.request({...f.input,native,projectRevision:digest(native),candidates:[preview]});
 f.store.importReceipt({schema:'vectorcraft-review-receipt/v1',requestId:request.id,bindingHash:request.bindingHash,reviewer:{kind:'human',identity:'unit fixture only',contextOrigin:'trusted SQL fixture',independenceEvidence:null},verdict:'revise',issues:[{objectId:2,field:'paint.color',message:'unit issue',evidence:['preview.png']}],scores:{structure:score,text:score,brand:score,layout:score,legibility:score}});
 const input={...request.input,technicalEvidenceOrigin:'checked-decoder',technicalEvidence:{checkerFiles:checkerFiles(),artifactIntegrityStatus:'PASS',technicalStatus:'PASS',engineeringStatus:'NOT_RUN',checkerSha256:digest(fileURLToPath(new URL('../src/evaluation/delivery_quality.py',import.meta.url))),launcherSha256:digest(fileURLToPath(new URL('../scripts/harness/process_runner.py',import.meta.url)))}};
 const fingerprints={...request.fingerprints,[native]:digest(native),[preview]:digest(preview),[model]:digest(model),[manifest]:digest(manifest)};
 f.store.db.prepare('UPDATE reviews SET input=?,fingerprints=?,binding_hash=? WHERE id=?').run(canonical(input),canonical(fingerprints),hash(canonical({input,fingerprints})),request.id);
 return request.id;
}
function advance(f:any,cycle:RevisionCycle,proposal:any,score:number){
 const directory=join(f.root,'next');mkdirSync(directory);const id=seedChecked(f,score,'next-native',directory);
 const task=cycle.ledger.claim('unit executed native',join(f.root,'project.vectorcraft'),directory,{planHash:'b'.repeat(64),inputHashes:{},projectRevision:hash('native'),runtimeIdentity:f.input.runtimeIdentity,authorization:proposal.authorization});
 cycle.ledger.intent(task.id,task.epoch,0,{kind:'unit execution fixture'},0);cycle.ledger.receipt(task.id,task.epoch,0,{unit:true});cycle.ledger.verified(task.id,task.epoch,{path:join(directory,'project.vectorcraft'),sha256:hash('next-native')});
 f.store.db.prepare("UPDATE revision_proposals SET execution=?,state='awaiting_review' WHERE id=?").run(task.id,proposal.id);return id;
}
const changes=[{objectId:2,field:'paint.color',value:'#fff'}];
const policy={maxRounds:2,stagnationLimit:1,minImprovement:0.1};

test('bounded cycles require checked evidence and immutable valid policy',()=>{
 const f=fixture(),cycle=new RevisionCycle(f.store);try{
  assert.throws(()=>cycle.open({id:'cycle',requestId:f.request.id,policy}),/checked_review_required/);
  const id=seedChecked(f);assert.throws(()=>cycle.open({id:'cycle',requestId:id,policy:{...policy,maxRounds:0}}),/invalid_revision_policy/);
  cycle.open({id:'cycle',requestId:id,policy});assert.throws(()=>cycle.open({id:'cycle',requestId:id,policy:{...policy,maxRounds:3}}),/revision_cycle_conflict/);
  assert.throws(()=>cycle.open({id:'another',requestId:id,policy}),/revision_budget_already_bound/);
 }finally{cycle.close();f.close();}
});

test('round reservations are idempotent, cannot overlap, and preserve shared budget across restart',()=>{
 const f=fixture();let cycle=new RevisionCycle(f.store);try{
  const id=seedChecked(f);cycle.open({id:'cycle',requestId:id,policy});const first=cycle.propose('cycle',id,changes,'one');
  assert.equal(cycle.propose('cycle',id,changes,'one').id,first.id);assert.equal(cycle.get('cycle').rounds,1);
  assert.throws(()=>cycle.propose('cycle',id,changes,'two'),/revision_round_pending/);
  assert.throws(()=>f.store.revision(id,changes),/revision_cycle_required/);
  const used=(cycle.ledger.db.prepare('SELECT attempts FROM budgets WHERE id=?').get('bounded-test') as any).attempts;
  cycle.close();cycle=new RevisionCycle(f.store);assert.equal(cycle.get('cycle').rounds,1);
  assert.equal((cycle.ledger.db.prepare('SELECT attempts FROM budgets WHERE id=?').get('bounded-test') as any).attempts,used);
  assert.equal(cycle.propose('cycle',id,changes,'one').authorization.budgetId,'bounded-test');
 }finally{cycle.close();f.close();}
});

test('stagnation stops the cycle and retains a hash-verifiable best candidate',()=>{
 const f=fixture(),cycle=new RevisionCycle(f.store);try{
  const id=seedChecked(f);cycle.open({id:'cycle',requestId:id,policy});const proposal=cycle.propose('cycle',id,changes,'one'),next=advance(f,cycle,proposal,2.05);
  const stopped=cycle.observe('cycle',next,proposal.id);assert.equal(stopped.reason,'stagnation');assert.equal(cycle.best('cycle').requestId,next);
  assert.throws(()=>cycle.propose('cycle',next,changes,'two'),/revision_cycle_stopped/);
  writeFileSync(join(f.root,'next/project.vectorcraft'),'GUI changed original');assert.equal(cycle.best('cycle').projectRevision,hash('next-native'));
  const kept=join(cycle.best('cycle').path,'project.vectorcraft');chmodSync(kept,0o600);writeFileSync(kept,'tampered best');assert.throws(()=>cycle.best('cycle'),/best_candidate_changed/);
 }finally{cycle.close();f.close();}
});

test('an improving last round still stops at the hard limit and retains the new best',()=>{
 const f=fixture(),cycle=new RevisionCycle(f.store);try{
  const id=seedChecked(f);cycle.open({id:'cycle',requestId:id,policy:{...policy,maxRounds:1}});const proposal=cycle.propose('cycle',id,changes,'one'),next=advance(f,cycle,proposal,3);
  assert.equal(cycle.observe('cycle',next,proposal.id).reason,'round_limit');assert.equal(cycle.best('cycle').requestId,next);
 }finally{cycle.close();f.close();}
});

test('exhausted shared budget stops durably and cannot be revived by restoring the counter',()=>{
 const f=fixture(),cycle=new RevisionCycle(f.store);try{
  const id=seedChecked(f);cycle.open({id:'cycle',requestId:id,policy});
  cycle.ledger.db.prepare('UPDATE budgets SET attempts=? WHERE id=?').run(f.input.authorization.maxAttempts,'bounded-test');
  assert.throws(()=>cycle.propose('cycle',id,changes,'exhausted'),/budget_exceeded/);assert.equal(cycle.get('cycle').rounds,0);
  cycle.ledger.db.prepare('UPDATE budgets SET attempts=1 WHERE id=?').run('bounded-test');
  assert.throws(()=>cycle.propose('cycle',id,changes,'restored-counter'),/revision_cycle_stopped/);assert.equal(cycle.get('cycle').reason,'budget_exceeded');
 }finally{cycle.close();f.close();}
});

test('source edits and duplicate field targets cannot issue a revision',()=>{
 const f=fixture(),cycle=new RevisionCycle(f.store);try{
  const id=seedChecked(f);cycle.open({id:'cycle',requestId:id,policy});
  assert.throws(()=>cycle.propose('cycle',id,[...changes,...changes],'duplicate'),/invalid_revision_targets/);
  writeFileSync(join(f.root,'project.vectorcraft'),'GUI changed');assert.throws(()=>cycle.propose('cycle',id,changes,'stale'),/stale_review_binding/);assert.equal(cycle.get('cycle').rounds,0);
 }finally{cycle.close();f.close();}
});

test('changed goals stop the cycle while its earlier best remains verifiable',()=>{
 const f=fixture(),cycle=new RevisionCycle(f.store);try{
  const id=seedChecked(f);cycle.open({id:'cycle',requestId:id,policy});writeFileSync(join(f.root,'brief.txt'),'new goal');
  const directory=join(f.root,'changed-goal');mkdirSync(directory);const next=seedChecked(f,4,'changed-native',directory);
  assert.equal(cycle.observe('cycle',next).reason,'goal_changed');assert.equal(cycle.best('cycle').requestId,id);
  assert.equal(cycle.best('cycle').latestRequestId,next);assert.equal(cycle.get('cycle').latest,next);
  assert.equal(cycle.observe('cycle',next).reason,'goal_changed');
 }finally{cycle.close();f.close();}
});

test('runtime drift is rejected before execution intent or another shared attempt',async()=>{
 const f=fixture(),cycle=new RevisionCycle(f.store);try{
  const id=seedChecked(f);cycle.open({id:'cycle',requestId:id,policy});const proposal=cycle.propose('cycle',id,changes,'one');
  const skill=join(f.root,'wrong-runtime');mkdirSync(join(skill,'scripts'),{recursive:true});writeFileSync(join(skill,'scripts/runtime.lock.json'),JSON.stringify({artifacts:{'darwin-arm64':{binarySha256:'b'.repeat(64)}}}));
  await assert.rejects(()=>cycle.execute('cycle',proposal.id,{skill}),/revision_runtime_mismatch/);
  assert.equal((cycle.ledger.db.prepare('SELECT attempts FROM budgets WHERE id=?').get('bounded-test') as any).attempts,1);
  assert.equal((cycle.ledger.db.prepare('SELECT state FROM revision_proposals WHERE id=?').get(proposal.id) as any).state,'proposed');
 }finally{cycle.close();f.close();}
});

// 可信SQL仅构造预算边界；真实执行证据由固定原生验收另行提供。
test('observing a non-improving candidate at the shared budget limit stops durably and retains prior best',()=>{
 const f=fixture(),cycle=new RevisionCycle(f.store);try{
  const id=seedChecked(f);cycle.open({id:'cycle',requestId:id,policy:{...policy,stagnationLimit:5}});
  const proposal=cycle.propose('cycle',id,changes,'one'),next=advance(f,cycle,proposal,1.9);
  cycle.ledger.db.prepare('UPDATE budgets SET attempts=? WHERE id=?').run(f.input.authorization.maxAttempts,'bounded-test');
  assert.equal(cycle.observe('cycle',next,proposal.id).reason,'budget_exceeded');
  assert.equal(cycle.best('cycle').requestId,id);assert.equal(cycle.best('cycle').latestRequestId,next);
  assert.equal(cycle.best('cycle').unresolvedIssues.length,1);
  cycle.ledger.db.prepare('UPDATE budgets SET attempts=1 WHERE id=?').run('bounded-test');
  assert.throws(()=>cycle.propose('cycle',next,changes,'restored-counter'),/revision_cycle_stopped/);
 }finally{cycle.close();f.close();}
});


// 注入只读技术副本及可信检查账本，仅验证预算分支，不充当真实解码证据。
function seedReadonlyTechnicalSnapshot(f:any,cycle:RevisionCycle,id:string){
 const review=f.store.current(id),snapshot=join(f.root,'checked-snapshot'),delivery=join(snapshot,'delivery');mkdirSync(delivery,{recursive:true});
 const source=join(review.input.native,'..'),manifest=JSON.parse(readFileSync(join(source,'manifest.json'),'utf8'));
 for(const name of ['manifest.json',...Object.keys(manifest.files)]){cpSync(join(source,name),join(delivery,name));chmodSync(join(delivery,name),0o400);}
 const task=cycle.ledger.claim('unit checked snapshot',join(snapshot,'unit-source'),snapshot,{planHash:'c'.repeat(64),inputHashes:{},projectRevision:review.input.projectRevision,runtimeIdentity:review.input.runtimeIdentity,authorization:f.input.authorization});
 cycle.ledger.intent(task.id,task.epoch,0,{kind:'explicit unit checked snapshot'},0);cycle.ledger.receipt(task.id,task.epoch,0,{unit:true});cycle.ledger.verified(task.id,task.epoch,{path:join(delivery,'project.vectorcraft'),sha256:review.input.projectRevision});
 const report={...review.input.technicalEvidence,files:manifest.files};
 const input={...review.input,technicalCheckId:task.id,technicalEvidence:report};
 f.store.db.exec('CREATE TABLE IF NOT EXISTS technical_checks(task TEXT PRIMARY KEY,report TEXT,report_sha TEXT,sources TEXT,review_id TEXT);');
 f.store.db.prepare('INSERT INTO technical_checks VALUES(?,?,?,?,?)').run(task.id,canonical(report),hash(canonical(report)),'{}',id);
 f.store.db.prepare('UPDATE reviews SET input=?,binding_hash=? WHERE id=?').run(canonical(input),hash(canonical({input,fingerprints:review.fingerprints})),id);
 return delivery;
}
test('higher score at the budget limit reuses verified readonly native dependencies without another attempt',()=>{
 const f=fixture(),cycle=new RevisionCycle(f.store);try{
  const id=seedChecked(f);cycle.open({id:'cycle',requestId:id,policy:{...policy,stagnationLimit:5}});
  const proposal=cycle.propose('cycle',id,changes,'one'),next=advance(f,cycle,proposal,3),snapshot=seedReadonlyTechnicalSnapshot(f,cycle,next);
  cycle.ledger.db.prepare('UPDATE budgets SET attempts=? WHERE id=?').run(f.input.authorization.maxAttempts,'bounded-test');
  assert.equal(cycle.observe('cycle',next,proposal.id).reason,'budget_exceeded');
  const best=cycle.best('cycle');assert.equal(best.requestId,next);assert.equal(best.path,realpathSync(snapshot));assert.equal(best.score,3);assert.equal(best.latestRequestId,next);assert.equal(best.sharedBudget.attempts,f.input.authorization.maxAttempts);assert.equal(best.acceptanceStatus,'pending');
  writeFileSync(join(f.root,'next/project.vectorcraft'),'original source later changed');assert.equal(cycle.best('cycle').projectRevision,hash('next-native'));
  chmodSync(join(snapshot,'preview.png'),0o600);writeFileSync(join(snapshot,'preview.png'),'tampered');assert.throws(()=>cycle.best('cycle'),/best_candidate_changed/);
 }finally{cycle.close();f.close();}
});

test('budget fallback refuses a writable or changed technical snapshot before selecting a new best',()=>{
 const f=fixture(),cycle=new RevisionCycle(f.store);try{
  const id=seedChecked(f);cycle.open({id:'cycle',requestId:id,policy:{...policy,stagnationLimit:5}});
  const proposal=cycle.propose('cycle',id,changes,'one'),next=advance(f,cycle,proposal,3),snapshot=seedReadonlyTechnicalSnapshot(f,cycle,next);
  cycle.ledger.db.prepare('UPDATE budgets SET attempts=? WHERE id=?').run(f.input.authorization.maxAttempts,'bounded-test');
  chmodSync(join(snapshot,'preview.png'),0o600);
  assert.throws(()=>cycle.observe('cycle',next,proposal.id),/technical_snapshot_changed/);assert.equal(cycle.get('cycle').best,id);
  chmodSync(join(snapshot,'preview.png'),0o400);chmodSync(join(snapshot,'project.vectorcraft'),0o600);writeFileSync(join(snapshot,'project.vectorcraft'),'changed checked source');chmodSync(join(snapshot,'project.vectorcraft'),0o400);
  assert.throws(()=>cycle.checkedSnapshot(cycle.get('cycle'),f.store.current(next)),/technical_snapshot_changed/);assert.equal(cycle.get('cycle').best,id);assert.equal(cycle.get('cycle').state,'stopped');
 }finally{cycle.close();f.close();}
});

// 目标变更仍须通过技术来源和原有授权检查；未经检查或超范围回执不能终止现有循环。
test('changed goals cannot bypass checked evidence before stopping the cycle',()=>{
 const f=fixture(),cycle=new RevisionCycle(f.store);try{
  const id=seedChecked(f);cycle.open({id:'cycle',requestId:id,policy});writeFileSync(join(f.root,'brief.txt'),'new goal');
  const input={...f.input,projectRevision:hash('native')};const next=f.store.request(input);
  f.store.importReceipt({schema:'vectorcraft-review-receipt/v1',requestId:next.id,bindingHash:next.bindingHash,reviewer:{kind:'human',identity:'unit unchecked fixture',contextOrigin:'unit',independenceEvidence:null},verdict:'revise',issues:[{objectId:2,field:'paint.color',message:'new goal issue',evidence:['preview.png']}],scores:{structure:2,text:2,brand:2,layout:2,legibility:2}});
  assert.throws(()=>cycle.observe('cycle',next.id),/checked_review_required/);assert.equal(cycle.get('cycle').state,'active');assert.equal(cycle.get('cycle').latest,id);
 }finally{cycle.close();f.close();}
});
test('changed goals cannot replace the immutable cycle authorization',()=>{
 const f=fixture(),cycle=new RevisionCycle(f.store);try{
  const id=seedChecked(f);cycle.open({id:'cycle',requestId:id,policy});writeFileSync(join(f.root,'brief.txt'),'new goal');
  f.input.authorization={...f.input.authorization,maxAttempts:30};const directory=join(f.root,'changed-scope');mkdirSync(directory);const next=seedChecked(f,3,'changed-native',directory);
  assert.throws(()=>cycle.observe('cycle',next),/revision_authorization_changed/);assert.equal(cycle.get('cycle').state,'active');assert.equal(cycle.get('cycle').latest,id);
 }finally{cycle.close();f.close();}
});
