/** 固定公开副本的原生几何QA；驱动器身份与被测发布代码身份分别记录。 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,existsSync} from 'node:fs';
import {join,resolve} from 'node:path';
import {pathToFileURL,fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const config=JSON.parse(readFileSync(process.argv[2],'utf8')),root=resolve(config.output),implementationRoot=resolve(config.implementationRoot);
assert.equal(existsSync(root),false);mkdirSync(root,{recursive:true});
const {Controller,skillDigest}=await import(pathToFileURL(join(implementationRoot,'src/harness/controller.ts')).href);
const {executionIdentity}=await import(pathToFileURL(join(implementationRoot,'scripts/acceptance/execution_identity.ts')).href);
const fingerprints=executionIdentity(),sha=(data:string|Buffer)=>createHash('sha256').update(data).digest('hex');
const lock=JSON.parse(readFileSync(join(implementationRoot,'skills.lock.json'),'utf8')).sources[0],expectedSkillSha256=lock.sha256['vectorcraft-use'];assert.equal(skillDigest(config.skill),expectedSkillSha256);
const cases:any[]=[];
for(const name of ['pixels-local','points-document-open','closed-mismatch','units-mismatch','control-mismatch','stroke-mismatch']){
 const work=join(root,name);mkdirSync(work);const units=name==='points-document-open'?'Points':'Pixels',local=name!=='points-document-open',closed=name!=='points-document-open';
 const plan={document:{name:'Fixed native geometry QA',width:200,height:120,units},operations:[
  {command:'artboard.new',params:{x:300,y:40,width:200,height:120,name:'Offset'}},
  {command:'path.create',params:{anchors:[{x:320,y:60,out:[340,60]},{x:450,y:60,in:[430,60]},{x:450,y:130}],closed},as:'curve'},
  {command:'paint.setStroke',params:{ids:[{$ref:'curve.id'}],color:'#000000'}},
  {command:'native.command',params:{command:'stroke.set',params:{ids:[{$ref:'curve.id'}],weight:3}}}
 ],exports:[{format:'svg',artboard:1},{format:'png',artboard:1},{format:'pdf',artboard:1}]};
 const path=join(work,'plan.json');writeFileSync(path,JSON.stringify(plan));
 const anchors=local?[{p:[20,20],out:[40,20]},{p:[150,20],in:[130,20]},{p:[150,90]}]:[{p:[320,60],out:[340,60]},{p:[450,60],in:[430,60]},{p:[450,130]}];
 const geometryContract:any={schema:'vectorcraft-geometry-contract/v1',units,coordinateSpace:local?'artboard-local':'document',tolerance:0.000001,artboards:[{id:2,rect:[300,40,500,160]}],paths:[{binding:'curve.id',artboardId:2,subpaths:[{closed,anchors}],strokes:[{width:3,paint:{type:'solid',color:{model:'rgb',r:0,g:0,b:0}}}]}]};
 const failures:Record<string,string>={'closed-mismatch':'path_closed_mismatch','units-mismatch':'units_mismatch','control-mismatch':'path_control_point_mismatch','stroke-mismatch':'stroke_mismatch'};
 if(name==='closed-mismatch')geometryContract.paths[0].subpaths[0].closed=false;
 if(name==='units-mismatch')geometryContract.units='Points';
 if(name==='control-mismatch')geometryContract.paths[0].subpaths[0].anchors[0].out=[41,20];
 if(name==='stroke-mismatch')geometryContract.paths[0].strokes[0].width=4;
 const controller=new Controller(join(work,'state.sqlite')),output=join(work,'delivery');
 const request={key:name,skill:config.skill,expectedSkillSha256,plan:path,output,runtimeHome:config.runtimeHome,python:config.python,estimatedBytes:8000000,geometryContract,
  authorization:{objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:1,maxBytes:16000000,readRoots:[work],writeRoots:[work,config.runtimeHome]}};
 try{
  let failure:any;
  if(failures[name])await assert.rejects(()=>controller.run(request),(error:any)=>{assert.match(error.message,/geometry_acceptance_failed/);failure=JSON.parse(error.message.split('geometry_acceptance_failed: ')[1]);assert.ok(failure.issues.some((v:any)=>v.reason===failures[name]));return true;});
  else {const task=await controller.run(request);assert.equal(task.state,'review_ready');assert.equal(task.geometryVerification.status,'PASS');}
  const row=controller.ledger.db.prepare('SELECT id FROM tasks WHERE key=?').get(name) as any,task=controller.ledger.get(row.id),manifest=JSON.parse(readFileSync(join(output,'manifest.json'),'utf8')),objectId=manifest.bindings.curve.id;
  assert.ok(Number.isSafeInteger(objectId));assert.equal(manifest.outputs.length,3);assert.deepEqual(manifest.outputs.map((v:any)=>v.artboardId),[2,2,2]);
  for(const [file,digest] of Object.entries(manifest.files))assert.equal(sha(readFileSync(join(output,file))),digest);
  const outputDigest=skillDigest(output),before=JSON.stringify(controller.ledger.db.prepare('SELECT attempts,bytes FROM budgets').all());
  const resumed=await controller.run(request);assert.equal(resumed.id,task.id);assert.equal(resumed.state,failures[name]?'reconciling':'review_ready');assert.equal(resumed.attempts,1);assert.equal(skillDigest(output),outputDigest);assert.equal(JSON.stringify(controller.ledger.db.prepare('SELECT attempts,bytes FROM budgets').all()),before);
  await assert.rejects(()=>controller.run({...request,geometryContract:{...geometryContract,tolerance:0}}),/idempotency_conflict/);
  const groups=controller.ledger.db.prepare('SELECT task,epoch FROM native_processes').all() as any[];assert.ok(groups.length);for(const row of groups)assert.equal(controller.processes.observe(row.task,row.epoch).stopped,true);
  const step=controller.ledger.db.prepare('SELECT result FROM steps WHERE task=? AND n=0').get(task.id) as any;
  const receipt=step.result?JSON.parse(step.result):null;
  if(failures[name]){assert.ok(failure.issues.every((v:any)=>v.objectId===objectId));assert.equal(failure.projectRevision,manifest.files['project.vectorcraft']);assert.equal(failure.nativeSha256,manifest.files['native.json']);}
  else {assert.equal(receipt.geometryVerification.status,'PASS');assert.equal(receipt.geometryVerification.projectRevision,manifest.files['project.vectorcraft']);assert.equal(receipt.geometryVerification.nativeSha256,manifest.files['native.json']);}
  cases.push({name,result:'PASS',expectedFailure:failures[name]??null,objectId,state:resumed.state,planSha256:sha(readFileSync(path)),contract:geometryContract,plan,manifestSha256:sha(readFileSync(join(output,'manifest.json'))),files:manifest.files,outputs:manifest.outputs,runtimeIdentity:task.binding.runtimeIdentity,planHash:task.binding.planHash,inputHashes:task.binding.inputHashes,geometryVerification:failure??receipt.geometryVerification,receiptPersisted:!failures[name],originalOutputRetained:true,replayRefused:true,changedContractRejected:true,budgetUnchangedOnResume:true,registeredGroups:groups.length,allRegisteredGroupsStopped:true});
 }finally{controller.close();}
}
// 真实固定控制器在非法预览空间请求上不得登记任务、安装或创建产物。
const work=join(root,'invalid-preview');mkdirSync(work);const controller=new Controller(join(work,'state.sqlite'));try{
 const plan=join(work,'plan.json');writeFileSync(plan,'{"operations":[]}');await assert.rejects(()=>controller.run({key:'preview',skill:config.skill,expectedSkillSha256,plan,output:join(work,'delivery'),runtimeHome:config.runtimeHome,python:config.python,estimatedBytes:1,authorization:{objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:1,maxBytes:100,readRoots:[work],writeRoots:[work]},geometryContract:{schema:'vectorcraft-geometry-contract/v1',units:'Millimeters',coordinateSpace:'preview-pixels'}}),/invalid_geometry_contract/);
 assert.equal((controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,0);assert.equal(existsSync(join(work,'delivery')),false);
}finally{controller.close();}
assert.deepEqual(executionIdentity(),fingerprints);assert.equal(skillDigest(config.skill),expectedSkillSha256);
const proof={schema:'vectorcraft-geometry-fixed-qa/v1',result:'PASS',level:config.level??'external-qa-against-fixed-install',fingerprints,driverSha256:sha(readFileSync(fileURLToPath(import.meta.url))),pluginVersion:JSON.parse(readFileSync(join(implementationRoot,'plugin.json'),'utf8')).version,sourceRef:lock.ref,sourceCommit:lock.sha,skillSha256:expectedSkillSha256,platform:process.platform+'-'+process.arch,cases,invalidPreviewRejectedBeforeEffects:true,
 scope:'six real native saves/reopens with manifest-bound geometry and SVG/PNG/PDF; two healthy units/spaces, four actual geometry contract refusals; no GUI, arbitrary transforms, pixels-as-geometry or creative claim'};
writeFileSync(join(root,'proof.json'),JSON.stringify(proof,null,2)+'\n');console.log(JSON.stringify({result:'PASS',cases:cases.length,scope:proof.scope}));
