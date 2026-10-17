/** 原生桌面修改后拒绝陈旧建议；固定安装，独占桌面进程。 */
import { readFileSync,writeFileSync,mkdirSync,cpSync,existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
const sha=(value:Buffer)=>createHash('sha256').update(value).digest('hex');
const c=JSON.parse(readFileSync(process.argv[2],'utf8'));mkdirSync(c.output,{recursive:true});const originalSource=c.source;const guiRoot=join(c.output,'gui');mkdirSync(guiRoot);cpSync(c.source,join(guiRoot,'source'),{recursive:true});c.source=join(guiRoot,'source');
const load=async(path:string)=>await import(pathToFileURL(join(c.installed,path)).href);
const {skillDigest}=await load('scripts/harness/controller.ts');
const beforeFiles=skillDigest(originalSource);
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
 const attempts=()=>Number((store.db.prepare('SELECT attempts FROM budgets WHERE id=?').get(authorization.budgetId) as any).attempts);
 assert.equal(attempts(),2);const bestBefore=cycle.best('native-cycle');const groupsBefore=cycle.ledger.db.prepare('SELECT task,epoch FROM native_processes').all();
 const edit=spawnSync('/opt/anaconda3/bin/python3',['-I','-B',join(process.cwd(),'scripts/qa/revision_gui_edit.py'),join(c.installed,'skills/vectorcraft-harness'),join(c.runtime,'vectorcraft/0.2.0-craft.2/vectorcraft-cli'),join(c.runtime,'vectorcraft-desktop/0.2.0'),join(c.source,'project.vectorcraft'),join(c.output,'gui')],{encoding:'utf8',timeout:90000});
 writeFileSync(join(c.output,'gui.log.txt'),edit.stdout+'\n'+edit.stderr);assert.equal(edit.status,0,edit.stderr);
 const gui=JSON.parse(readFileSync(join(c.output,'gui/proof.json'),'utf8'));assert.equal(gui.result,'PASS');assert.equal(gui.ownedProcessesStopped,true);assert.equal(gui.listenerOwnedByPID,true);
 let refusal='';try{await cycle.execute('native-cycle',proposal.id,{skill:join(c.installed,'skills/vectorcraft-harness'),expectedSkillSha256:lock.sha256['vectorcraft-harness'],output:join(c.output,'forbidden-output'),runtimeHome:c.runtime,python:'/opt/anaconda3/bin/python3'});}catch(e){refusal=String(e);}
 assert.match(refusal,/stale_review_binding/);assert.equal(attempts(),2);assert.equal(existsSync(join(c.output,'forbidden-output')),false);
 assert.deepEqual(cycle.best('native-cycle'),bestBefore);assert.equal(skillDigest(originalSource),beforeFiles);
 const groups=cycle.ledger.db.prepare('SELECT task,epoch FROM native_processes').all();assert.deepEqual(groups,groupsBefore);const {ProcessRegistry}=await load('scripts/harness/process_registry.ts');const registry=new ProcessRegistry(store.db);assert(groups.every((g:any)=>registry.observe(g.task,g.epoch).stopped));
 const proof={schema:'vectorcraft-revision-stale-gui-native/v1',driverSha256:sha(readFileSync(process.argv[1])),guiDriverSha256:sha(readFileSync('scripts/qa/revision_gui_edit.py')),result:'PASS',pluginVersion:JSON.parse(readFileSync(join(c.installed,'plugin.json'),'utf8')).version,sourceRef:lock.ref,platform:process.platform+'-'+process.arch,initialRequest:request,proposal,gui,refusal,best:bestBefore,sharedAttempts:attempts(),cycle:cycle.get('native-cycle'),originalSourcePreserved:true,newOutputAbsent:true,registeredGroupsBefore:groupsBefore.length,registeredGroupsAfter:groups.length,allGroupsStopped:true,scope:'owned signed desktop GUI source mutation rejects old proposal before native revision effects; preserved best; explicit QA feedback; not full6.6 qualification'};
 let text=JSON.stringify(proof,null,2)+'\n';for(const [from,to] of [[c.source,'QA_SOURCE'],[c.output,'QA_ROOT'],[originalSource,'ORIGINAL_SOURCE'],[c.installed,'INSTALLED_PLUGIN'],[c.runtime,'QA_RUNTIME']])text=text.split(from).join(to);writeFileSync(join(c.output,'proof.json'),text);console.log(JSON.stringify({result:proof.result,refusal,sharedAttempts:attempts()}));
}finally{cycle.close();store.close();}
