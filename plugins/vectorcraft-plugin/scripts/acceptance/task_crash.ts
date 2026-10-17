/** 原生父进程崩溃、持久占用、只读恢复与源工程交接；仅操作本用例登记的进程组。 */
import assert from 'node:assert/strict';
import {mkdirSync,readFileSync,writeFileSync,existsSync,openSync,closeSync,cpSync} from 'node:fs';
import {join,resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';
import {createHash} from 'node:crypto';
import {executionIdentity} from './execution_identity.ts';
const fingerprints=executionIdentity(),config=JSON.parse(readFileSync(process.argv[2],'utf8'));
const root=resolve(config.output),implementationRoot=resolve(config.implementationRoot??join(dirname(fileURLToPath(import.meta.url)),'../..'));
const {Controller,skillDigest}=await import(pathToFileURL(join(implementationRoot,'src/harness/controller.ts')).href);
const {Recovery}=await import(pathToFileURL(join(implementationRoot,'src/harness/recovery.ts')).href);
const hash=(p:string)=>createHash('sha256').update(readFileSync(p)).digest('hex');
assert.equal(existsSync(root),false,'fresh root required');mkdirSync(root,{recursive:true});
const source=resolve(config.source),skill=resolve(config.skill),runtime=resolve(config.runtimeHome),project=join(source,'project.vectorcraft'),sourceSha256=hash(project);
const plan=join(root,'plan.json');writeFileSync(plan,JSON.stringify({expectedProjectSha256:sourceSha256,operations:Array.from({length:1000},()=>({command:'swatch.edit',params:{name:'Brand Primary',color:config.targetColor}}))}));
const request={key:'crashed-parent',skill,expectedSkillSha256:skillDigest(skill),plan,source,output:join(root,'original-output'),runtimeHome:runtime,python:config.python,estimatedBytes:10000000,
 authorization:{...config.authorization,deadline:Date.now()+180000,maxAttempts:1,maxBytes:10000000,readRoots:[root,source],writeRoots:[root,runtime]}};
const database=join(root,'tasks.sqlite'),actorConfig=join(root,'actor.json'),actorResult=join(root,'actor-result.json');
writeFileSync(actorConfig,JSON.stringify({database,implementationRoot,request,actorResult}));
const log=openSync(join(root,'actor.log'),'wx');
const actor=spawn(process.execPath,[join(dirname(fileURLToPath(import.meta.url)),'task_crash_child.ts'),actorConfig],{detached:true,stdio:['ignore',log,log]});closeSync(log);
let actorExited=false;const exited=new Promise<any>((accept,reject)=>{actor.on('error',reject);actor.on('exit',(code,signal)=>{actorExited=true;accept({code,signal});});});
let controller=new Controller(database),task:any,checkpoint:any,eventFile:string|undefined;
try{
 const until=Date.now()+30000;
 while(Date.now()<until&&!checkpoint&&!actorExited){
  task=controller.ledger.db.prepare("SELECT id,epoch FROM tasks WHERE key='crashed-parent'").get() as any;
  if(task){
   eventFile=join(controller.snapshotRoot,task.id+'-events.jsonl');
   if(existsSync(eventFile))checkpoint=readFileSync(eventFile,'utf8').split('\n').filter(Boolean).map(x=>JSON.parse(x)).find(x=>x.event==='revision_checkpoint');
  }
  if(!checkpoint)await new Promise(r=>setTimeout(r,10));
 }
 assert.ok(task&&checkpoint&&!actorExited,'owned actor must have a real saved checkpoint and still be live');
 controller.processes.signal(task.id,task.epoch,'SIGSTOP');
 const paused=controller.processes.observe(task.id,task.epoch);assert.equal(paused.stopped,false);assert.equal(paused.owned,true);
 process.kill(actor.pid!,'SIGKILL');const parentExit=await exited;assert.equal(parentExit.signal,'SIGKILL');assert.equal(existsSync(actorResult),false);
 const checkpointHash=hash(checkpoint.path),eventHash=hash(eventFile!);assert.equal(checkpointHash,checkpoint.sha256);
 controller.close();controller=new Controller(database);
 const before=controller.ledger.get(task.id),nativeBefore=controller.processes.observe(task.id,task.epoch);assert.equal(before.state,'running');assert.equal(nativeBefore.stopped,false);
 const resumed=await controller.run(request);assert.equal(resumed.state,'running');assert.match(resumed.resumePolicy,/no automatic replay/);
 assert.equal(controller.ledger.get(task.id).attempts,1);assert.equal(hash(eventFile!),eventHash);
 await assert.rejects(()=>controller.run({...request,output:join(root,'bypass-output')}),/idempotency_conflict/);
 await assert.rejects(()=>controller.run({...request,key:'competing',output:join(root,'competing-output')}),/resource_busy/);
 const otherSource=join(root,'different-source');cpSync(source,otherSource,{recursive:true});
 await assert.rejects(()=>controller.run({...request,key:'different-source-same-output',source:otherSource}),/output_busy/);
 assert.equal((controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,1);
 assert.equal((controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM steps').get() as any).n,1);
 controller.ledger.unknown(task.id,task.epoch,'QA verified coordinator SIGKILL; native result unknown');
 const recovery=new Recovery(controller.ledger,controller.processes);
 await assert.rejects(()=>recovery.inspect(task.id,task.epoch),/native_stop_unconfirmed/);
 await controller.processes.stop(task.id,task.epoch,50);assert.equal(controller.processes.observe(task.id,task.epoch).stopped,true);
 const stoppedEventHash=hash(eventFile!),recovered=await controller.reconcileOriginal(task.id,task.epoch);
 assert.equal(recovered.task.state,'interrupted_verified');assert.equal(recovered.task.epoch,task.epoch+1);
 assert.equal(hash(checkpoint.path),checkpointHash);assert.equal(hash(project),sourceSha256);assert.equal(hash(eventFile!),stoppedEventHash);
 const events=readFileSync(eventFile!,'utf8').split('\n').filter(Boolean).map(x=>JSON.parse(x));
 const actualNativeReply=events.find(x=>x.event==='reply_received');assert.ok(actualNativeReply?.replySha256);
 const handoffPlan=join(root,'handoff-plan.json');writeFileSync(handoffPlan,JSON.stringify({expectedProjectSha256:sourceSha256,operations:[{command:'swatch.edit',params:{name:'Brand Primary',color:config.targetColor}}]}));
 const handoff=await controller.run({...request,key:'handoff',plan:handoffPlan,output:join(root,'handoff-output')});assert.equal(handoff.state,'review_ready');
 const manifestHash=hash(join(handoff.output,'manifest.json'));
 assert.throws(()=>controller.ledger.receipt(task.id,task.epoch,0,{nativeReplyRecord:actualNativeReply}),/stale_epoch/);
 assert.equal(hash(join(handoff.output,'manifest.json')),manifestHash);assert.equal(controller.ledger.get(handoff.id).state,'review_ready');
 const late=controller.ledger.db.prepare('SELECT result FROM late_receipts WHERE task=?').get(task.id) as any;assert.deepEqual(JSON.parse(late.result).nativeReplyRecord,actualNativeReply);
 const proof={result:'PASS',fingerprints,scope:'real saved checkpoint then coordinator SIGKILL with paused owned native group; unknown readonly restart, no replay, confirmed group stop, original-file recovery, source handoff and durable late native reply record quarantine; no GUI or complete V1 claim',
  implementationRootIdentity:implementationRoot===resolve(join(dirname(fileURLToPath(import.meta.url)),'../..'))?'current-worktree':'explicit-implementation-root',
  skillSha256:skillDigest(skill),runtimeIdentity:before.binding.runtimeIdentity,sourceSha256,sourceUnchanged:hash(project)===sourceSha256,
  parentExit,taskId:task.id,originalEpoch:task.epoch,checkpoint:{sha256:checkpointHash,path:checkpoint.path},stateAfterRestart:before.state,
  registeredNativeMembersAfterParentCrash:nativeBefore.members.map((x:any)=>({pid:x.pid,pgid:x.pgid,start:x.start,status:x.status})),
  noAutomaticReplay:true,changedOutputRejected:true,secondSourceWriterRejected:true,differentSourceSameOutputRejected:true,competingTaskNotRegistered:true,attemptsAfterRestart:resumed.attempts,
  nativeAliveRefusedRecovery:true,confirmedNativeStopped:true,recovery:recovered.proof,settledState:recovered.task.state,settledEpoch:recovered.task.epoch,
  handoff:{taskId:handoff.id,manifestSha256:manifestHash,state:handoff.state},lateNativeReplyQuarantined:true,lateReceiptPayloadSha256:createHash('sha256').update(late.result).digest('hex')};
 writeFileSync(join(root,'proof.json'),JSON.stringify(proof,null,2)+'\n');console.log(JSON.stringify({result:'PASS',taskId:task.id,settledState:recovered.task.state,handoffState:handoff.state}));
}finally{
 if(task){try{if(!controller.processes.observe(task.id,task.epoch).stopped)await controller.processes.stop(task.id,task.epoch,50);}catch{}}
 if(!actorExited){try{process.kill(actor.pid!,'SIGKILL');}catch{}await exited;}
 controller.close();
}
