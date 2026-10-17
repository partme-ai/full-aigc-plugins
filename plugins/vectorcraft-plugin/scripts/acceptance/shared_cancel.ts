/** 共享预算下两个真实原生组与一个ready任务；协调器退出后取消仍持久传播。 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,cpSync,existsSync,openSync,closeSync} from 'node:fs';
import {join,resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';
import {createHash} from 'node:crypto';
import {executionIdentity} from './execution_identity.ts';
const fingerprints=executionIdentity(),config=JSON.parse(readFileSync(process.argv[2],'utf8'));
const root=resolve(config.output),implementationRoot=resolve(config.implementationRoot??join(dirname(fileURLToPath(import.meta.url)),'../..'));
const {Controller,skillDigest}=await import(pathToFileURL(join(implementationRoot,'src/harness/controller.ts')).href);
assert.equal(existsSync(root),false);mkdirSync(root,{recursive:true});
const database=join(root,'state.sqlite'),deadline=Date.now()+(config.expire?12000:180000),budgetId='shared-native-workflow';
let controller=new Controller(database);const actors:any[]=[],members:any[]=[];
try{
 for(const [index,key] of ['parent','child','ready'].entries()){
  if(config.expire&&key==='ready')break;
  const source=join(root,key+'-source');cpSync(config.source,source,{recursive:true});const sourceDigest=skillDigest(source),projectHash=createHash('sha256').update(readFileSync(join(source,'project.vectorcraft'))).digest('hex');
  const plan=join(root,key+'-plan.json');writeFileSync(plan,JSON.stringify({expectedProjectSha256:projectHash,operations:Array.from({length:1000},()=>({command:'swatch.edit',params:{name:'Brand Primary',color:config.targetColor}}))}));
  const request={key,skill:config.skill,expectedSkillSha256:skillDigest(config.skill),plan,source,output:join(root,key+'-output'),runtimeHome:config.runtimeHome,python:config.python,estimatedBytes:5000000,
   authorization:{...config.authorization,budgetId,deadline,maxAttempts:3,maxBytes:15000000,readRoots:[root],writeRoots:[root,config.runtimeHome]}};
  const marker=join(root,key+'-marker.json'),actorConfig=join(root,key+'-actor.json');writeFileSync(actorConfig,JSON.stringify({database,implementationRoot,request,actorResult:join(root,key+'-result.json'),point:'ready',marker}));
  const fd=openSync(join(root,key+'-actor.log'),'wx'),actor=spawn(process.execPath,[join(dirname(fileURLToPath(import.meta.url)),key==='ready'?'task_launch_child.ts':'task_crash_child.ts'),actorConfig],{detached:true,stdio:['ignore',fd,fd]});closeSync(fd);
  const record:any={actor,exited:false};record.exit=new Promise((accept,reject)=>{actor.on('error',reject);actor.on('exit',(code,signal)=>{record.exited=true;accept({code,signal});});});actors.push(record);
  let task:any,eventFile='',checkpoint:any;
  const until=Date.now()+30000;
  while(Date.now()<until&&!checkpoint&&!(key==='ready'&&existsSync(marker))&&!record.exited){
   const row=controller.ledger.db.prepare('SELECT id FROM tasks WHERE key=?').get(key) as any;
   if(row){task=controller.ledger.get(row.id);eventFile=join(controller.snapshotRoot,task.id+'-events.jsonl');if(existsSync(eventFile))checkpoint=readFileSync(eventFile,'utf8').split('\n').filter(Boolean).map(line=>JSON.parse(line)).find(row=>row.event==='revision_checkpoint');}
   if(!checkpoint)await new Promise(r=>setTimeout(r,10));
  }
  if(key==='ready'){
   const parentExit=await record.exit;assert.equal(parentExit.signal,'SIGKILL');const crash=JSON.parse(readFileSync(marker,'utf8'));task=controller.ledger.get(crash.task);assert.equal(task.state,'ready');
  }else{
   assert.ok(task&&checkpoint&&!record.exited,'real checkpoint and live owned actor required');controller.processes.signal(task.id,1,'SIGSTOP');process.kill(actor.pid!,'SIGKILL');const parentExit=await record.exit;assert.equal(parentExit.signal,'SIGKILL');assert.equal(controller.processes.observe(task.id,1).stopped,false);
  }
  members.push({key,task,request,source,sourceDigest,eventFile,checkpoint});
 }
 controller.close();controller=new Controller(database);
 const before=controller.ledger.db.prepare('SELECT attempts,bytes FROM budgets WHERE id=?').get(budgetId) as any;assert.deepEqual({...before},{attempts:2,bytes:10000000});
 let waitedPastOriginalDeadline=false;
 if(config.expire){
  while(Date.now()<=deadline)await new Promise(r=>setTimeout(r,Math.min(100,deadline-Date.now()+1)));
  const resumed=await controller.run(members[0].request);assert.equal(resumed.state,'cancel_requested');waitedPastOriginalDeadline=true;
 }else assert.equal(controller.requestCancel(members[0].task.id,1).state,'cancel_requested');
 const liveMembers=members.filter(member=>member.key!=='ready');
 for(const member of members)assert.equal(controller.ledger.get(member.task.id).state,'cancel_requested');
 for(const member of liveMembers){
  assert.equal(controller.processes.observe(member.task.id,1).stopped,false);
  await assert.rejects(()=>controller.reconcileOriginal(member.task.id,1),/native_stop_unconfirmed/);
 }
 const other=join(root,'other.vectorcraft');writeFileSync(other,'admission sentinel only, never opened as native');
 assert.throws(()=>controller.ledger.claim('late-child',other,join(root,'late-child-output'),members[0].task.binding),config.expire?/budget_exceeded|budget_cancel_requested/:/budget_cancel_requested/);
 for(const member of members)assert.throws(()=>controller.ledger.intent(member.task.id,1,1,{},1),/cancel_requested/);
 const recovered:any[]=[];
 for(const member of members){
  if(member.key!=='ready')await controller.processes.stop(member.task.id,1,50);
  const value=await controller.reconcileOriginal(member.task.id,1);assert.equal(value.task.state,'cancelled');assert.equal(value.task.epoch,2);assert.equal(value.task.attempts,member.key==='ready'?0:1);assert.equal(skillDigest(member.source),member.sourceDigest);
  assert.equal(existsSync(member.request.output),false);recovered.push({key:member.key,task:value.task.id,epoch:value.task.epoch,state:value.task.state,sourceUnchanged:true,inspection:value.proof});
  if(member.key!=='ready'){
   const events=readFileSync(member.eventFile,'utf8').split('\n').filter(Boolean).map(line=>JSON.parse(line));const reply=events.find(event=>event.event==='reply_received');assert.ok(reply?.replySha256);
   assert.throws(()=>controller.ledger.receipt(member.task.id,1,0,{originalNativeReplyRecord:reply}),/stale_epoch/);
   assert.equal((controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM late_receipts WHERE task=?').get(member.task.id) as any).n,1);
  }
 }
 const after=controller.ledger.db.prepare('SELECT attempts,bytes FROM budgets WHERE id=?').get(budgetId);assert.deepEqual({...after},{...before});
 const processes=controller.ledger.db.prepare('SELECT task,epoch FROM native_processes').all() as any[];for(const row of processes)assert.equal(controller.processes.observe(row.task,row.epoch).stopped,true);
 const proof={result:'PASS',fingerprints,scope:'actual shared-budget native parent/child groups remain alive across coordinator SIGKILL; durable cancellation, readonly original recovery and old native reply quarantine; fixed install recorded separately',mode:config.expire?'deadline-restart':'explicit-cancel',runtimeIdentity:members[0].task.binding.runtimeIdentity,skillSha256:skillDigest(config.skill),budgetId,originalDeadline:deadline,waitedPastOriginalDeadline,
  members:members.length,liveNativeGroupsAtCancellation:2,allCancelRequestedBeforeStop:true,aliveGroupsRefusedSettlement:true,newDependentRejected:true,newStepsRejected:true,budgetBefore:before,budgetAfter:after,lateOriginalNativeReplyRecordsQuarantined:2,allRegisteredGroupsStopped:true,recovered};
 writeFileSync(join(root,'proof.json'),JSON.stringify(proof,null,2)+'\n');console.log(JSON.stringify({result:'PASS',mode:proof.mode,members:members.length,budget:after}));
}finally{
 for(const record of actors)if(!record.exited){try{process.kill(record.actor.pid,'SIGKILL');}catch{}await record.exit;}
 for(const row of controller.ledger.db.prepare('SELECT task,epoch FROM native_processes').all() as any[])if(!controller.processes.observe(row.task,row.epoch).stopped)await controller.processes.stop(row.task,row.epoch,50);
 controller.close();
}
