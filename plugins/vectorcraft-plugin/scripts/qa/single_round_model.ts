/** 分阶段实际会话评审；不内置模型分数，不将故障注入当成创作判断。 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,cpSync,existsSync} from 'node:fs';
import {join} from 'node:path';
import {pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
const c=JSON.parse(readFileSync(process.argv[2],'utf8')),phase=process.argv[3];
const read=(p:string)=>JSON.parse(readFileSync(p,'utf8')),write=(p:string,v:any)=>writeFileSync(p,JSON.stringify(v,null,2)+'\n');
const sha=(v:Buffer)=>createHash('sha256').update(v).digest('hex');
const load=async(p:string)=>import(pathToFileURL(join(c.installed,p)).href);
const {ReviewStore}=await load('src/evaluation/review_store.ts'),{TechnicalReview}=await load('src/evaluation/technical_review.ts'),{RevisionCycle}=await load('src/evaluation/revision_cycle.ts'),{skillDigest}=await load('src/harness/controller.ts');
const source=join(c.output,'source'),database=join(c.output,'state.sqlite'),brief=join(c.output,'brief.txt'),rubric=join(c.output,'rubric.json');
const field='appearance.items.0.paint',value={type:'solid',color:{model:'rgb',r:0,g:1,b:0}};
if(phase==='prepare'){
 assert(!existsSync(c.output));mkdirSync(c.output,{recursive:true});cpSync(c.source,source,{recursive:true});
 writeFileSync(brief,'Acceptance fixture: use solid green #00ff00 for rectangle object2. Preserve editable rectangle topology,stroke,geometry,artboard and all text object3. Inspect actual 128x96,64x48,32x24 native previews; report small-size label limitations honestly. Change only object2 fill paint this round. No automatic follow-up edits.');
 write(rubric,{schema:'vectorcraft-single-round-vector-rubric/v1',dimensions:{structure:'native closed topology,holes,stroke,geometry and editability',text:'live text,fonts and unchanged wording',brand:'rectangle fill must be solid #00ff00',layout:'alignment,spacing and preserved artboard',legibility:'actual128,64,32 pixel previews; unavailable evidence stays unknown'},scale:'0 missing;1 poor;2 limited;3 adequate;4 strong',exchange:'Record lost,observed and unknown separately; no derivative lossless claim',reviewer:'actual current Codex conversation; no independence claim'});
 write(join(c.output,'context.json'),{authorization:{objects:[2],fields:[field],deadline:Date.now()+1200000,maxAttempts:6,maxBytes:128*1024*1024,budgetId:'actual-single-round',readRoots:[c.output,c.runtime],writeRoots:[c.output,c.runtime]},sourceTree:skillDigest(source),originalSourceTree:skillDigest(c.source),pluginVersion:read(join(c.installed,'plugin.json')).version,sourceRef:read(join(c.installed,'skills.lock.json')).sources[0].ref});
}
const context=read(join(c.output,'context.json')),store=new ReviewStore(database,[c.output,c.runtime]),cycle=new RevisionCycle(store);
const input=(directory:string,authorization=context.authorization)=>{const m=read(join(directory,'manifest.json'));return {native:join(directory,'project.vectorcraft'),projectRevision:m.files['project.vectorcraft'],runtimeIdentity:m.runtimeSha256,candidates:m.outputs.map((x:any)=>join(directory,x.path)),targets:[{path:brief,role:'target'}],rubric,exchangeLoss:join(directory,'exchange-loss.json'),technicalStatus:'PASS',authorization};};
const observe=(directory:string,label:string)=>{const config=join(c.output,label+'-native-config.json');write(config,{source:directory,output:join(c.output,label+' previews'),skill:join(c.installed,'skills/vectorcraft-use'),binary:join(c.runtime,'vectorcraft/0.2.0-craft.2/vectorcraft-cli')});const r=spawnSync(c.python,['-I','-B',join(c.installed,'scripts/qa/review_native_views.py'),config],{encoding:'utf8',timeout:30000});assert.equal(r.status,0,r.stdout+r.stderr);return read(join(c.output,label+' previews/proof.json'));};
const importActual=(request:any,file:string)=>{const assessment=read(file);assert.equal(assessment.kind,'actual-current-conversation-model-review');assert.equal(assessment.projectRevision,request.input.projectRevision);assert.equal(assessment.previewSha256,request.fingerprints[join(request.input.native,'..','artboard-1.png')]);const receipt={schema:'vectorcraft-review-receipt/v1',requestId:request.id,bindingHash:request.bindingHash,reviewer:assessment.reviewer,verdict:assessment.verdict,issues:assessment.issues,scores:assessment.scores};return {assessment,receipt,response:store.importReceipt(receipt)};};
try{
 if(phase==='prepare'){
  const observation=observe(source,'initial');const request=await new TechnicalReview(store).request(input(source),{python:c.python});assert.equal(request.input.technicalStatus,'PASS');write(join(c.output,'initial.json'),{request,observation});console.log(JSON.stringify({result:'WAITING_FOR_ACTUAL_MODEL_REVIEW',requestId:request.id,projectRevision:request.input.projectRevision}));
 }else if(phase==='revise'){
  const initial=read(join(c.output,'initial.json')),feedback=importActual(initial.request,c.initialAssessment);assert.equal(feedback.response.state,'revision_proposed');assert.equal(feedback.response.independent,false);
  cycle.open({id:'actual-single-round',requestId:initial.request.id,policy:{maxRounds:2,stagnationLimit:1,minImprovement:1}});
  assert.throws(()=>cycle.propose('actual-single-round',initial.request.id,[{objectId:3,field,value}],'forbidden-object'),/revision_outside_authorization/);
  const proposal=cycle.propose('actual-single-round',initial.request.id,[{objectId:2,field,value}],'explicit-green');
  const plan=join(c.output,'revision.json');write(plan,{expectedProjectSha256:initial.request.input.projectRevision,operations:[{command:'paint.setFill',params:{ids:[2],color:'#00ff00'}}],exports:['svg','pdf','png'].map(format=>({format,artboard:0}))});
  const lock=read(join(c.installed,'skills.lock.json')).sources[0];const execution=await cycle.execute('actual-single-round',proposal.id,{skill:join(c.installed,'skills/vectorcraft-use'),expectedSkillSha256:lock.sha256['vectorcraft-use'],plan,output:join(c.output,'revised'),runtimeHome:c.runtime,python:c.python,estimatedBytes:4000000});
  assert.equal(execution.state,'awaiting_review');assert.throws(()=>cycle.propose('actual-single-round',initial.request.id,[{objectId:2,field,value}],'automatic-next'),/revision_round_pending/);
  const observation=observe(execution.output,'revised'),request=await new TechnicalReview(store).request(input(execution.output),{python:c.python});
  write(join(c.output,'revised.json'),{feedback,proposal,execution,observation,request});console.log(JSON.stringify({result:'WAITING_FOR_ACTUAL_MODEL_REVIEW',requestId:request.id,projectRevision:request.input.projectRevision}));
 }else if(phase==='finish'){
  const revised=read(join(c.output,'revised.json')),feedback=importActual(revised.request,c.revisedAssessment);
  const stopped=cycle.observe('actual-single-round',revised.request.id,revised.proposal.id);assert.equal(stopped.reason,'stagnation');assert.equal(stopped.rounds,1);
  assert.throws(()=>cycle.propose('actual-single-round',revised.request.id,[{objectId:2,field,value}],'implicit-loop'),/revision_cycle_stopped/);
  assert.throws(()=>store.importReceipt(feedback.receipt),/duplicate_review_receipt/);
  const before=read(join(source,'native.json')),after=read(join(revised.execution.output,'native.json'));const object=(model:any,id:number)=>{const walk=(x:any):any=>{if(!x||typeof x!=='object')return;if(x.id===id)return x;for(const y of Object.values(x)){const found=walk(y);if(found)return found;}};return walk(model.layers);};
  assert.deepEqual(object(before,3),object(after,3));assert.deepEqual(before.artboards,after.artboards);assert.deepEqual(object(before,2).kind,object(after,2).kind);assert.deepEqual(object(after,2).appearance.items[0].paint,value);assert.deepEqual(object(before,2).appearance.items[1],object(after,2).appearance.items[1]);
  assert.equal(skillDigest(source),context.sourceTree);assert.equal(skillDigest(c.source),context.originalSourceTree);
  const budget=store.db.prepare('SELECT attempts FROM budgets WHERE id=?').get(context.authorization.budgetId) as any;assert.equal(budget.attempts,5);
  const groups=cycle.ledger.db.prepare('SELECT task,epoch FROM native_processes').all() as any[];const {ProcessRegistry}=await load('src/harness/process_registry.ts');const registry=new ProcessRegistry(store.db);assert(groups.every(g=>registry.observe(g.task,g.epoch).stopped));
  write(join(c.output,'flow-proof.json'),{schema:'vectorcraft-actual-single-round-review/v1',result:'PASS',context,initial:read(join(c.output,'initial.json')),revised:{...revised,feedback},cycle:stopped,best:cycle.best('actual-single-round'),sharedAttempts:budget.attempts,allGroupsStopped:true,sourcePreserved:true,textAndGeometryPreserved:true,oneExplicitRevision:true,scope:'Actual current-conversation image assessments and one explicit native local revision; stops on real score improvement below declared threshold; not independent review,full automatic loop,fixed installation or full V1'});console.log(JSON.stringify({result:'PASS',sharedAttempts:budget.attempts,reason:stopped.reason}));
 }else throw new Error('invalid_phase');
}finally{cycle.close();store.close();}
