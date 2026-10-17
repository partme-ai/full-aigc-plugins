/** 原位置非空链接依赖恢复；真实检查点、进程停止及缺失／改动拒绝。 */
import assert from 'node:assert/strict';
import {mkdirSync,readFileSync,writeFileSync,existsSync,openSync,closeSync,renameSync,lstatSync,utimesSync} from 'node:fs';
import {join,resolve,dirname,relative,isAbsolute} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';
import {createHash} from 'node:crypto';
import {executionIdentity} from './execution_identity.ts';
const fingerprints=executionIdentity(),config=JSON.parse(readFileSync(process.argv[2],'utf8'));
const root=resolve(config.output),implementationRoot=resolve(config.implementationRoot??join(dirname(fileURLToPath(import.meta.url)),'../..'));
const {Controller,skillDigest}=await import(pathToFileURL(join(implementationRoot,'src/harness/controller.ts')).href);
const {Recovery}=await import(pathToFileURL(join(implementationRoot,'src/harness/recovery.ts')).href);
const hash=(p:string)=>createHash('sha256').update(readFileSync(p)).digest('hex');
const inside=(parent:string,p:string)=>{const part=relative(parent,p);return !isAbsolute(part)&&part!=='..'&&!part.startsWith('../');};
assert.equal(existsSync(root),false,'fresh root required');mkdirSync(root,{recursive:true});
const source=resolve(config.source),skill=resolve(config.skill),runtime=resolve(config.runtimeHome);
const sourceDigest=skillDigest(source),sourceSha256=hash(join(source,'project.vectorcraft'));
const originalManifest=JSON.parse(readFileSync(join(source,'manifest.json'),'utf8'));
assert.equal(originalManifest.assets.referenceRaster.linked,true);
const plan=join(root,'plan.json');writeFileSync(plan,JSON.stringify({expectedProjectSha256:sourceSha256,operations:Array.from({length:1000},()=>({command:'swatch.edit',params:{name:'Brand Primary',color:config.targetColor}}))}));
const request={key:'linked-interruption',skill,expectedSkillSha256:skillDigest(skill),plan,source,output:join(root,'original-output'),runtimeHome:runtime,python:config.python,estimatedBytes:10000000,
 authorization:{...config.authorization,deadline:Date.now()+180000,maxAttempts:1,maxBytes:10000000,readRoots:[root,source],writeRoots:[root,runtime]}};
const database=join(root,'tasks.sqlite'),actorConfig=join(root,'actor.json'),actorResult=join(root,'actor-result.json');
writeFileSync(actorConfig,JSON.stringify({database,implementationRoot,request,actorResult}));
const log=openSync(join(root,'actor.log'),'wx');
const actor=spawn(process.execPath,[join(dirname(fileURLToPath(import.meta.url)),'task_crash_child.ts'),actorConfig],{detached:true,stdio:['ignore',log,log]});closeSync(log);
let exited=false;const exit=new Promise<any>((accept,reject)=>{actor.on('error',reject);actor.on('exit',(code,signal)=>{exited=true;accept({code,signal});});});
let controller=new Controller(database),task:any,checkpoint:any,eventFile:string|undefined;
try{
 const deadline=Date.now()+30000;
 while(Date.now()<deadline&&!checkpoint&&!exited){
  task=controller.ledger.db.prepare("SELECT id,epoch FROM tasks WHERE key='linked-interruption'").get() as any;
  if(task){eventFile=join(controller.snapshotRoot,task.id+'-events.jsonl');
   if(existsSync(eventFile))checkpoint=readFileSync(eventFile,'utf8').split('\n').filter(Boolean).map(line=>JSON.parse(line)).find(event=>event.event==='revision_checkpoint');}
  if(!checkpoint)await new Promise(r=>setTimeout(r,10));
 }
 assert.ok(task&&checkpoint&&!exited,'real linked checkpoint and live coordinator required');
 controller.processes.signal(task.id,task.epoch,'SIGSTOP');
 process.kill(actor.pid!,'SIGKILL');const parentExit=await exit;assert.equal(parentExit.signal,'SIGKILL');
 controller.close();controller=new Controller(database);
 controller.ledger.unknown(task.id,task.epoch,'QA linked checkpoint coordinator killed; unknown native result');
 await controller.processes.stop(task.id,task.epoch,50);assert.equal(controller.processes.observe(task.id,task.epoch).stopped,true);
 const eventsHash=hash(eventFile!),checkpointHash=hash(checkpoint.path),checkpointInode=lstatSync(checkpoint.path).ino;
 assert.equal(checkpointHash,checkpoint.sha256);
 const events=readFileSync(eventFile!,'utf8').split('\n').filter(Boolean).map(line=>JSON.parse(line));
 const originalStage=events.find(event=>event.event==='stage_created');assert.ok(originalStage&&existsSync(originalStage.path));
 const asset=join(originalStage.path,'Assets/referenceRaster.png'),assetBytes=readFileSync(asset),assetStat=lstatSync(asset);
 assert.equal(hash(asset),originalManifest.assets.referenceRaster.sha256);
 const recovery=new Recovery(controller.ledger,controller.processes);
 const refusals:any[]=[];
 for(const kind of ['missing','modified']){
  const removed=join(root,'temporarily-removed-link.png');
  try{
   if(kind==='missing')renameSync(asset,removed);else {writeFileSync(asset,readFileSync(config.changedAsset));assert.notEqual(hash(asset),originalManifest.assets.referenceRaster.sha256);}
   await assert.rejects(()=>recovery.inspect(task.id,task.epoch),/original_dependency_unverified/);
   assert.equal(controller.ledger.get(task.id).state,'reconciling');assert.equal(controller.ledger.get(task.id).attempts,1);
   assert.equal((controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM recovery_checks WHERE result IS NOT NULL').get() as any).n,0);
   await assert.rejects(()=>controller.run({...request,key:'blocked-'+kind,output:join(root,'blocked-'+kind)}),/resource_busy/);
   assert.equal(hash(checkpoint.path),checkpointHash);assert.equal(hash(eventFile!),eventsHash);
   refusals.push({dependency:kind,error:'original_dependency_unverified',sourceWriterRetained:true,noSuccessfulInspection:true,checkpointUnchanged:true});
  }finally{
   if(kind==='missing'&&existsSync(removed))renameSync(removed,asset);
   else if(kind==='modified')writeFileSync(asset,assetBytes);
   utimesSync(asset,assetStat.atime,assetStat.mtime);
  }
 }
 const proof=await recovery.inspect(task.id,task.epoch);
 const links=proof.reopened.flatMap((item:any)=>item.dependencies.links);
 assert.ok(links.length>0);assert.ok(links.every((item:any)=>item.status==='ok'&&inside(originalStage.path,item.path)));
 assert.equal(proof.stage,originalStage.path);assert.equal(proof.stageInode,originalStage.inode);
 // 检查与settle之间再次改动素材也不得释放工程；恢复原字节后再次原生核验。
 writeFileSync(asset,readFileSync(config.changedAsset));
 try{assert.throws(()=>recovery.settle(task.id,task.epoch,proof.checkId),/original_artifact_changed/);}
 finally{writeFileSync(asset,assetBytes);utimesSync(asset,assetStat.atime,assetStat.mtime);}
 assert.equal(controller.ledger.get(task.id).state,'reconciling');
 const finalProof=await recovery.inspect(task.id,task.epoch),settled=recovery.settle(task.id,task.epoch,finalProof.checkId);
 for(const owner of controller.ledger.db.prepare('SELECT task,epoch FROM native_processes').all() as any[])assert.equal(controller.processes.observe(owner.task,owner.epoch).stopped,true);
 assert.equal(settled.state,'interrupted_verified');assert.equal(settled.epoch,task.epoch+1);
 assert.equal(hash(checkpoint.path),checkpointHash);assert.equal(lstatSync(checkpoint.path).ino,checkpointInode);
 assert.equal(lstatSync(asset).ino,assetStat.ino);assert.equal(hash(asset),originalManifest.assets.referenceRaster.sha256);
 assert.equal(skillDigest(source),sourceDigest);assert.equal(hash(eventFile!),eventsHash);
 const report={result:'PASS',fingerprints,scope:'actual public pinned implementation recovery with real linked PNG checkpoint; missing/modified dependency refusal and post-inspection artifact change refusal; original-stage reopening only, no migration or replay; full3.6 remains open',
  skillSha256:skillDigest(skill),runtimeIdentity:controller.ledger.get(task.id).binding.runtimeIdentity,sourceProjectSha256:sourceSha256,
  parentExit,taskId:task.id,epoch:task.epoch,refusals,nonemptyHealthyLinks:links.length,allLinksInsideOriginalStage:true,
  changedAfterInspectionRetainedOccupation:true,allOwnedInspectionGroupsStopped:true,sourceUnchanged:true,checkpointUnchanged:true,checkpointInodePreserved:true,assetInodePreserved:true,
  sourceAssetSha256:originalManifest.assets.referenceRaster.sha256,attempts:controller.ledger.get(task.id).attempts,
  originalStageInode:originalStage.inode,originalStagePath:originalStage.path,recovery:finalProof,settledState:settled.state,settledEpoch:settled.epoch};
 writeFileSync(join(root,'proof.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({result:'PASS',nonemptyHealthyLinks:links.length,dependencyRefusals:refusals.length,settledState:settled.state}));
}finally{
 if(!exited){try{process.kill(actor.pid!,'SIGKILL');}catch{}await exit;}
 if(task){if(!controller.processes.observe(task.id,task.epoch).stopped)await controller.processes.stop(task.id,task.epoch,50);}
 controller.close();
}
