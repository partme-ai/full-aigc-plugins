/** 真实协调器SIGKILL覆盖GO前持久化边界；已授权GO无暂存时保守拒绝。 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,existsSync,openSync,closeSync} from 'node:fs';
import {join,dirname,resolve} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';
import {createHash} from 'node:crypto';
import {executionIdentity} from './execution_identity.ts';
const config=JSON.parse(readFileSync(process.argv[2],'utf8')),fingerprints=executionIdentity();
const implementationRoot=resolve(config.implementationRoot??join(dirname(fileURLToPath(import.meta.url)),'../..'));
const {Controller,skillDigest}=await import(pathToFileURL(join(implementationRoot,'src/harness/controller.ts')).href);
const {Recovery}=await import(pathToFileURL(join(implementationRoot,'src/harness/recovery.ts')).href);
const root=resolve(config.output);assert.equal(existsSync(root),false);mkdirSync(root,{recursive:true});
const source=config.source?resolve(config.source):null,sourceBefore=source?skillDigest(source):null;
const plan=join(root,'plan.json');writeFileSync(plan,source?JSON.stringify({expectedProjectSha256:createHash('sha256').update(readFileSync(join(source,'project.vectorcraft'))).digest('hex'),operations:[{command:'swatch.edit',params:{name:'Brand Primary',color:'#175cce'}}]}):JSON.stringify({operations:[]}));
const request={key:'before-native-launch',skill:config.skill,expectedSkillSha256:skillDigest(config.skill),plan,...(source?{source}:{}),output:join(root,'original-output'),runtimeHome:config.runtimeHome,python:config.python,estimatedBytes:10000000,
 authorization:{...config.authorization,deadline:Date.now()+180000,maxAttempts:1,maxBytes:10000000,readRoots:[root,...(source?[source]:[])],writeRoots:[root,config.runtimeHome]}};
const database=join(root,'tasks.sqlite'),marker=join(root,'crash.json'),actorConfig=join(root,'actor.json');writeFileSync(actorConfig,JSON.stringify({database,marker,request,point:config.point,implementationRoot}));
const fd=openSync(join(root,'actor.log'),'wx'),actor=spawn(process.execPath,[join(dirname(fileURLToPath(import.meta.url)),'task_launch_child.ts'),actorConfig],{detached:true,stdio:['ignore',fd,fd]});closeSync(fd);
let exited=false,controller:any;
const exit=new Promise<any>((accept,reject)=>{actor.on('error',reject);actor.on('exit',(code,signal)=>{exited=true;accept({code,signal});});});
try{
 const parentExit=await Promise.race([exit,new Promise((_,reject)=>{const timer=setTimeout(()=>reject(new Error('launch_actor_timeout')),45000);timer.unref();})]);assert.equal(parentExit.signal,'SIGKILL');
 const crash=JSON.parse(readFileSync(marker,'utf8'));controller=new Controller(database);const before=controller.ledger.get(crash.task);
 const submitted=['intent','registered','authorized'].includes(config.point);assert.equal(before.state,submitted?'running':'ready');assert.equal(before.attempts,submitted?1:0);
 const registered=controller.ledger.db.prepare('SELECT task FROM native_processes WHERE task=? AND epoch=?').get(before.id,1);
 if(registered){const deadline=Date.now()+3000;while(!controller.processes.observe(before.id,1).stopped&&Date.now()<deadline)await new Promise(r=>setTimeout(r,25));assert.equal(controller.processes.observe(before.id,1).stopped,true);}
 const resumed=await controller.run(request);assert.equal(resumed.state,before.state);assert.equal(resumed.attempts,before.attempts);assert.equal(resumed.bytes,before.bytes);assert.equal(existsSync(request.output),false);
 await assert.rejects(()=>controller.run({...request,output:join(root,'redirected')}),/idempotency_conflict/);
 await assert.rejects(()=>controller.run({...request,key:'duplicate'}),/resource_busy|output_busy/);
 let proof:any=null,settled:any=null,authorizedRefused=false,postInspectionSourceChangeRefused=false;
 const recovery=new Recovery(controller.ledger,controller.processes);
 if(config.point==='authorized'){
  controller.ledger.unknown(before.id,1,'QA: coordinator killed after durable GO authorization before stdin');
  await assert.rejects(()=>recovery.inspect(before.id,1),/original_stage_identity_missing/);authorizedRefused=true;assert.equal(controller.ledger.get(before.id).state,'reconciling');
 }else{
  proof=await recovery.inspect(before.id,1);assert.equal(proof.schema,'vectorcraft-unlaunched-inspection/v1');assert.equal(proof.nativeInspection,source?'readonly-original-source':'not-applicable-no-source');
  if(source){assert.equal(proof.reopened.dependencies.missing,0);assert.equal(proof.reopened.dependencies.modified,0);assert.ok(proof.reopened.layers>0);}
  if(source){
   const asset=Object.keys(proof.validation.files).find(path=>path.endsWith('/Links/referenceRaster.png'))??join(source,'manifest.json');
   const original=readFileSync(asset);
   try{writeFileSync(asset,Buffer.concat([original,Buffer.from('QA-change')]));assert.throws(()=>recovery.settle(before.id,1,proof.checkId),/recovery_input_mismatch|revision_conflict|unlaunched_input_changed/);assert.equal(controller.ledger.get(before.id).epoch,1);postInspectionSourceChangeRefused=true;}
   finally{writeFileSync(asset,original);}
   proof=await recovery.inspect(before.id,1);
  }
  assert.throws(()=>controller.ledger.authorizeLaunch(before.id,1),/launch_not_authorized/);
  assert.throws(()=>controller.ledger.intent(before.id,1,1,{},0),/reconcile_required/);
  settled=recovery.settle(before.id,1,proof.checkId);assert.equal(settled.state,'interrupted_verified');assert.equal(settled.epoch,2);assert.equal(settled.attempts,before.attempts);assert.equal(settled.bytes,before.bytes);
 }
 if(source)assert.equal(skillDigest(source),sourceBefore);assert.equal(existsSync(request.output),false);
 const result={result:'PASS',scope:'real coordinator SIGKILL and actual native readonly original-source inspection where a source exists; no synthetic native artifact; full VC-TX-002 remains open',fingerprints,point:config.point,parentExit,
  sourcePresent:!!source,sourceUnchanged:true,sourceDigest:sourceBefore,skillSha256:request.expectedSkillSha256,runtimeIdentity:before.binding.runtimeIdentity,
  originalState:before.state,attemptsPreserved:true,bytesPreserved:true,outputAbsent:true,noAutomaticReplay:true,changedOutputRefused:true,duplicateRefused:true,
  authorizedWithoutEventsRefused:authorizedRefused,postInspectionSourceChangeRefused,proof,settledState:settled?.state??null,settledEpoch:settled?.epoch??null};
 writeFileSync(join(root,'proof.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({result:'PASS',point:config.point,sourcePresent:!!source,settledState:result.settledState}));
}finally{
 if(!exited){try{process.kill(actor.pid!,'SIGKILL');}catch{}await exit;}
 if(!controller)controller=new Controller(database);
 for(const row of controller.ledger.db.prepare('SELECT task,epoch FROM native_processes').all() as any[])if(!controller.processes.observe(row.task,row.epoch).stopped)await controller.processes.stop(row.task,row.epoch,50);
 controller.close();
}
