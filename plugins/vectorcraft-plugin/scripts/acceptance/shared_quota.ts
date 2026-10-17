/** 一次真实原生交付后，以另一真实源请求验证共享次数／预留字节拒绝发生在任务登记前。 */
import assert from 'node:assert/strict';
import {readFileSync,writeFileSync,mkdirSync,cpSync,existsSync} from 'node:fs';
import {join,resolve,dirname} from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
import {executionIdentity} from './execution_identity.ts';
const fingerprints=executionIdentity(),config=JSON.parse(readFileSync(process.argv[2],'utf8')),root=resolve(config.output);
assert.equal(existsSync(root),false);mkdirSync(root,{recursive:true});
const implementationRoot=resolve(config.implementationRoot??join(dirname(fileURLToPath(import.meta.url)),'../..'));
const {Controller,skillDigest}=await import(pathToFileURL(join(implementationRoot,'src/harness/controller.ts')).href);
const database=join(root,'state.sqlite'),source=join(root,'source'),second=join(root,'dependent-source');cpSync(config.source,source,{recursive:true});cpSync(config.source,second,{recursive:true});
const original=skillDigest(source),projectHash=createHash('sha256').update(readFileSync(join(source,'project.vectorcraft'))).digest('hex'),plan=join(root,'plan.json');
writeFileSync(plan,JSON.stringify({expectedProjectSha256:projectHash,operations:[{command:'swatch.edit',params:{name:'Brand Primary',color:config.targetColor}}]}));
const budgetId='quota-'+config.mode,estimatedBytes=5000000,authorization={...config.authorization,budgetId,deadline:Date.now()+180000,maxAttempts:config.mode==='attempt'?1:3,maxBytes:config.mode==='attempt'?20000000:estimatedBytes,readRoots:[root],writeRoots:[root,config.runtimeHome]};
const request={key:'first',skill:config.skill,expectedSkillSha256:skillDigest(config.skill),plan,source,output:join(root,'first-output'),runtimeHome:config.runtimeHome,python:config.python,estimatedBytes,authorization};
let controller=new Controller(database);
try{
 const task=await controller.run(request);assert.equal(task.state,'review_ready');const manifest=controller.verifyDelivery(request.output,task.binding.runtimeIdentity);assert.equal(manifest.outputs.length,9);
 const outputDigest=skillDigest(request.output),before=controller.ledger.db.prepare('SELECT attempts,bytes FROM budgets WHERE id=?').get(budgetId) as any;
 assert.deepEqual({...before},{attempts:1,bytes:estimatedBytes});
 controller.close();controller=new Controller(database);const resumed=await controller.run(request);assert.equal(resumed.state,'review_ready');assert.equal(resumed.attempts,1);
 const processCount=(controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM native_processes').get() as any).n;
 await assert.rejects(()=>controller.run({...request,key:'new-dependent',source:second,output:join(root,'dependent-output')}),/budget_exceeded/);
 assert.equal((controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,1);assert.equal((controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM native_processes').get() as any).n,processCount);
 assert.equal(existsSync(join(root,'dependent-output')),false);assert.equal(skillDigest(request.output),outputDigest);assert.equal(skillDigest(source),original);assert.equal(skillDigest(second),original);
 const after=controller.ledger.db.prepare('SELECT attempts,bytes FROM budgets WHERE id=?').get(budgetId);assert.deepEqual({...before},{...after});assert.equal(controller.processes.observe(task.id,1).stopped,true);
 const proof={result:'PASS',fingerprints,scope:'actual native nine-export delivery followed by shared attempt/reserved-byte denial before new task or native group; reserved quota is not a filesystem hard quota',mode:config.mode,skillSha256:skillDigest(config.skill),runtimeIdentity:task.binding.runtimeIdentity,
  taskId:task.id,budgetId,authorization:{deadline:authorization.deadline,maxAttempts:authorization.maxAttempts,maxBytes:authorization.maxBytes},budgetBefore:before,budgetAfter:after,exportCount:9,sourceUnchanged:true,deliveryUnchanged:true,otherSourceUnchanged:true,
  readonlyResumeNoExtraAttempt:true,newDependentRejected:true,newTaskNotAdmitted:true,newNativeGroupNotStarted:true,dependentOutputAbsent:true,nativeGroupStopped:true};writeFileSync(join(root,'proof.json'),JSON.stringify(proof,null,2)+'\n');console.log(JSON.stringify({result:'PASS',mode:config.mode,exports:9}));
}finally{controller.close();}
