/** 原生执行后目标变化的显式反馈探针；QA评分不代表创作验收。 */
import { readFileSync,writeFileSync,mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
const sha=(value:Buffer)=>createHash('sha256').update(value).digest('hex');
const c=JSON.parse(readFileSync(process.argv[2],'utf8'));mkdirSync(c.output,{recursive:true});const score=3;const expectedReason='goal_changed';
const load=async(path:string)=>await import(pathToFileURL(join(c.installed,path)).href);
const {skillDigest}=await load('scripts/harness/controller.ts');
const beforeFiles=skillDigest(c.source);
const {ReviewStore}=await load('src/evaluation/review_store.ts'),{TechnicalReview}=await load('src/evaluation/technical_review.ts'),{RevisionCycle}=await load('src/evaluation/revision_cycle.ts');
const lock=JSON.parse(readFileSync(join(c.installed,'skills.lock.json'),'utf8')).sources[0],manifest=JSON.parse(readFileSync(join(c.source,'manifest.json'),'utf8'));
const brief=join(c.output,'brief.txt'),rubric=join(c.output,'rubric.json');writeFileSync(brief,'Explicit QA: change gradient object2 to green; preserve text object3.');writeFileSync(rubric,'{}');
const field='appearance.items.0.paint',value={type:'solid',color:{model:'rgb',r:0,g:1,b:0}};
const roots=[c.output,c.source,c.runtime];const authorization={objects:[2,3],fields:[field,'kind.runs.0.text'],deadline:Date.now()+120000,maxAttempts:20,maxBytes:128*1024*1024,budgetId:'native-revision-probe',readRoots:roots,writeRoots:[c.output,c.runtime]};
const store=new ReviewStore(join(c.output,'state.sqlite'),roots),cycle=new RevisionCycle(store);
try{
 const request=await new TechnicalReview(store).request({native:join(c.source,'project.vectorcraft'),projectRevision:manifest.files['project.vectorcraft'],runtimeIdentity:manifest.runtimeSha256,candidates:manifest.outputs.map((x:any)=>join(c.source,x.path)),targets:[{path:brief,role:'target'}],rubric,exchangeLoss:join(c.source,'exchange-loss.json'),technicalStatus:'PASS',authorization},{python:'/opt/anaconda3/bin/python3'});
 assert.equal(request.input.technicalStatus,'PASS');store.importReceipt({schema:'vectorcraft-review-receipt/v1',requestId:request.id,bindingHash:request.bindingHash,reviewer:{kind:'human',identity:'explicit QA feedback fixture',contextOrigin:'same acceptance driver',independenceEvidence:null},verdict:'revise',issues:[{objectId:2,field,message:'QA: test authorized green revision',evidence:['artboard-1.png']}],scores:{structure:2,text:2,brand:2,layout:2,legibility:2}});
 cycle.open({id:'native-cycle',requestId:request.id,policy:{maxRounds:2,stagnationLimit:1,minImprovement:0.1}});
 const proposal=cycle.propose('native-cycle',request.id,[{objectId:2,field,value}],'green');
 assert.deepEqual(cycle.propose('native-cycle',request.id,[{objectId:2,field,value}],'green'),proposal);
 assert.equal(cycle.get('native-cycle').rounds,1);
 assert.throws(()=>cycle.propose('native-cycle',request.id,[{objectId:2,field,value:{}}],'green'),/revision_proposal_conflict/);
 if(c.mode!=='round-limit')assert.throws(()=>cycle.propose('native-cycle',request.id,[{objectId:2,field,value}],'overlap'),/revision_round_pending/);
 const plan=join(c.output,'green.json');writeFileSync(plan,JSON.stringify({expectedProjectSha256:manifest.files['project.vectorcraft'],operations:[{command:'paint.setFill',params:{ids:[2],color:'#00ff00'}}],exports:[{format:'svg',artboard:0},{format:'pdf',artboard:0},{format:'png',artboard:0}]}));
 const result=await cycle.execute('native-cycle',proposal.id,{skill:join(c.installed,'skills/vectorcraft-harness'),expectedSkillSha256:lock.sha256['vectorcraft-harness'],plan,output:join(c.output,'revised'),runtimeHome:c.runtime,python:'/opt/anaconda3/bin/python3',estimatedBytes:4000000});
 assert.equal(cycle.get('native-cycle').latest,request.id);assert.equal(cycle.get('native-cycle').state,'active');
 await assert.rejects(()=>cycle.execute('native-cycle',proposal.id,{}),/revision_execution_requires_new_intent/);
 const revisedManifest=JSON.parse(readFileSync(join(result.output,'manifest.json'),'utf8'));
 writeFileSync(brief,'Explicit QA new goal: preserve green object2 and revise its layout instead.');
 const next=await new TechnicalReview(store).request({native:join(result.output,'project.vectorcraft'),projectRevision:revisedManifest.files['project.vectorcraft'],runtimeIdentity:revisedManifest.runtimeSha256,candidates:revisedManifest.outputs.map((x:any)=>join(result.output,x.path)),targets:[{path:brief,role:'target'}],rubric,exchangeLoss:join(result.output,'exchange-loss.json'),technicalStatus:'PASS',authorization},{python:'/opt/anaconda3/bin/python3'});
 assert.equal(next.input.technicalStatus,'PASS');
 store.importReceipt({schema:'vectorcraft-review-receipt/v1',requestId:next.id,bindingHash:next.bindingHash,reviewer:{kind:'human',identity:'explicit QA feedback fixture; no actual creative assessment',contextOrigin:'same acceptance driver',independenceEvidence:null},verdict:'revise',issues:[{objectId:2,field,message:'QA: further revision pending',evidence:['artboard-1.png']}],scores:{structure:score,text:score,brand:score,layout:score,legibility:score}});
 const attempts=()=>Number((store.db.prepare('SELECT attempts FROM budgets WHERE id=?').get(authorization.budgetId) as any).attempts);
 assert.equal(attempts(),4);assert.equal(cycle.observe('native-cycle',next.id,proposal.id).reason,expectedReason);
 const best=cycle.best('native-cycle');const latestIssues=JSON.parse(store.current(next.id).receipt).issues;const gap=best.latestRequestId!==next.id;
 assert.equal(best.requestId,request.id);assert.equal(best.score,2);assert.equal(best.acceptanceStatus,'pending');assert.equal(attempts(),4);
 if(c.baseline){assert.equal(gap,true);}else{assert.equal(gap,false);assert.deepEqual(best.unresolvedIssues,latestIssues);assert.equal(cycle.observe('native-cycle',next.id,proposal.id).reason,expectedReason);}
 assert.throws(()=>cycle.propose('native-cycle',next.id,[{objectId:2,field,value}],'forbidden-next'),/revision_cycle_stopped/);
 assert.equal(skillDigest(c.source),beforeFiles);
 const before=JSON.parse(readFileSync(join(c.source,'native.json'),'utf8')),after=JSON.parse(readFileSync(join(result.output,'native.json'),'utf8'));
 function object(model:any,id:number):any{const walk=(x:any):any=>{if(!x||typeof x!=='object')return; if(x.id===id)return x;for(const child of Object.values(x)){const found=walk(child);if(found)return found;}};return walk(model.layers);}
 assert.deepEqual(object(before,3),object(after,3));assert.deepEqual(object(after,2).appearance.items[0].paint,value);assert.deepEqual(before.artboards,after.artboards);
 const groups=cycle.ledger.db.prepare('SELECT task,epoch FROM native_processes').all() as any[];const {ProcessRegistry}=await load('scripts/harness/process_registry.ts');const registry=new ProcessRegistry(store.db);assert(groups.every(g=>registry.observe(g.task,g.epoch).stopped));
 const beforeReopen=cycle.get('native-cycle');cycle.close();const restarted=new RevisionCycle(store);
 assert.deepEqual(restarted.get('native-cycle'),beforeReopen);assert.deepEqual(restarted.best('native-cycle'),best);restarted.close();
 const proof={schema:'vectorcraft-revision-goal-native/v1',driverSha256:sha(readFileSync(process.argv[1])),result:gap?'FAIL':'PASS',expectedGapConfirmed:gap,expectedReason,feedbackScore:score,latestIssues,level:c.level??'native-candidate',pluginVersion:JSON.parse(readFileSync(join(c.installed,'plugin.json'),'utf8')).version,sourceRef:lock.ref,platform:process.platform+'-'+process.arch,initialRequest:request,nextRequest:next,proposal,execution:result,best,cycle:beforeReopen,sharedAttempts:attempts(),sourcePreserved:true,controlTextPreserved:true,targetPaint:value,sourceModel:before,revisedModel:after,manifest:revisedManifest,registeredGroups:groups.length,allGroupsStopped:true,scope:'actual native revision and checked changed-goal feedback; best for original goal retained; latest feedback must be reported; QA scores only; not full6.6 qualification'};
 let text=JSON.stringify(proof,null,2)+'\n';for(const [from,to] of [[c.output,'QA_ROOT'],[c.source,'QA_SOURCE'],[c.installed,'INSTALLED_PLUGIN'],[c.runtime,'QA_RUNTIME']])text=text.split(from).join(to);writeFileSync(join(c.output,'proof.json'),text);console.log(JSON.stringify({result:proof.result,expectedGapConfirmed:gap,sharedAttempts:best.sharedBudget.attempts}));
}finally{cycle.close();store.close();}
