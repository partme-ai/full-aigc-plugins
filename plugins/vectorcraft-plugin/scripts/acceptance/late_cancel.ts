/** 同epoch迟到的真实完成交付回执隔离；原位置核验后才cancelled，并隔离旧epoch再次到达。 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,cpSync,existsSync,openSync,closeSync,lstatSync} from 'node:fs';
import {join,resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {spawn} from 'node:child_process';
import {createHash} from 'node:crypto';
import {executionIdentity} from './execution_identity.ts';
const fingerprints=executionIdentity(),config=JSON.parse(readFileSync(process.argv[2],'utf8')),root=resolve(config.output);
assert.equal(existsSync(root),false);mkdirSync(root,{recursive:true});
const implementationRoot=resolve(config.implementationRoot??join(dirname(fileURLToPath(import.meta.url)),'../..'));
const {Controller,skillDigest}=await import(pathToFileURL(join(implementationRoot,'src/harness/controller.ts')).href);
const source=join(root,'source');cpSync(config.source,source,{recursive:true});const sourceDigest=skillDigest(source),projectHash=createHash('sha256').update(readFileSync(join(source,'project.vectorcraft'))).digest('hex');
const plan=join(root,'plan.json');writeFileSync(plan,JSON.stringify({expectedProjectSha256:projectHash,operations:[{command:'swatch.edit',params:{name:'Brand Primary',color:config.targetColor}}]}));
const request={key:'late-delivery',skill:config.skill,expectedSkillSha256:skillDigest(config.skill),plan,source,output:join(root,'original-output'),runtimeHome:config.runtimeHome,python:config.python,estimatedBytes:10000000,
 authorization:{...config.authorization,budgetId:'late-native-delivery',deadline:Date.now()+180000,maxAttempts:1,maxBytes:10000000,readRoots:[root],writeRoots:[root,config.runtimeHome]}};
const database=join(root,'state.sqlite'),marker=join(root,'marker.json'),actorConfig=join(root,'actor.json');writeFileSync(actorConfig,JSON.stringify({database,implementationRoot,request,marker}));
const fd=openSync(join(root,'actor.log'),'wx'),actor=spawn(process.execPath,[join(dirname(fileURLToPath(import.meta.url)),'late_cancel_child.ts'),actorConfig],{detached:true,stdio:['ignore',fd,fd]});closeSync(fd);
let exited=false,controller:any;const exit=new Promise<any>((accept,reject)=>{actor.on('error',reject);actor.on('exit',(code,signal)=>{exited=true;accept({code,signal});});});
try{
 const parentExit=await Promise.race([exit,new Promise((_,reject)=>{const timer=setTimeout(()=>reject(new Error('late_delivery_actor_timeout')),45000);timer.unref();})]);assert.equal(parentExit.signal,'SIGKILL');
 const recorded=JSON.parse(readFileSync(marker,'utf8'));assert.equal(recorded.state,'quarantined');controller=new Controller(database);const task=controller.ledger.get(recorded.task);assert.equal(task.state,'cancel_requested');
 const step=controller.ledger.db.prepare('SELECT state,result FROM steps WHERE task=? AND n=0').get(task.id) as any;assert.equal(step.state,'quarantined');assert.deepEqual(JSON.parse(step.result),recorded.result);
 const manifest=controller.verifyDelivery(request.output,task.binding.runtimeIdentity),outputDigest=skillDigest(request.output),inode=lstatSync(request.output).ino;assert.equal(manifest.outputs.length,9);
 const resumed=await controller.run(request);assert.equal(resumed.state,'cancel_requested');assert.equal(resumed.attempts,1);assert.equal(resumed.bytes,task.bytes);
 const recovered=await controller.reconcileOriginal(task.id,1);assert.equal(recovered.task.state,'cancelled');assert.equal(recovered.task.epoch,2);assert.equal(recovered.proof.stage,request.output);
 assert.equal(skillDigest(request.output),outputDigest);assert.equal(lstatSync(request.output).ino,inode);assert.equal(skillDigest(source),sourceDigest);
 assert.throws(()=>controller.ledger.receipt(task.id,1,0,recorded.result),/stale_epoch/);const late=controller.ledger.db.prepare('SELECT result FROM late_receipts WHERE task=?').get(task.id) as any;assert.deepEqual(JSON.parse(late.result),recorded.result);
 for(const row of controller.ledger.db.prepare('SELECT task,epoch FROM native_processes').all() as any[])assert.equal(controller.processes.observe(row.task,row.epoch).stopped,true);
 const proof={result:'PASS',fingerprints,scope:'actual native saved/reopened/exported delivery then cancellation before durable receipt; same-epoch completed receipt quarantined, original output readonly verified before cancelled, old-epoch actual receipt quarantined again',skillSha256:skillDigest(config.skill),runtimeIdentity:task.binding.runtimeIdentity,
  parentExit,taskId:task.id,originalEpoch:1,exportCount:9,sameEpochActualReceiptQuarantined:true,lateOldEpochActualReceiptQuarantined:true,sourceUnchanged:true,outputUnchanged:true,outputInodePreserved:true,noAutomaticReplay:true,attemptsPreserved:true,bytesPreserved:true,allRegisteredGroupsStopped:true,recovery:recovered.proof,settledState:recovered.task.state,settledEpoch:recovered.task.epoch};
 writeFileSync(join(root,'proof.json'),JSON.stringify(proof,null,2)+'\n');console.log(JSON.stringify({result:'PASS',state:proof.settledState,exports:9}));
}finally{
 if(!exited){try{process.kill(actor.pid!,'SIGKILL');}catch{}await exit;}
 if(!controller)controller=new Controller(database);
 for(const row of controller.ledger.db.prepare('SELECT task,epoch FROM native_processes').all() as any[])if(!controller.processes.observe(row.task,row.epoch).stopped)await controller.processes.stop(row.task,row.epoch,50);
 controller.close();
}
