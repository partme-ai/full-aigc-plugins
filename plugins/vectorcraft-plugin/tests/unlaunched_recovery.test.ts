import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,realpathSync,mkdirSync,writeFileSync,rmSync,existsSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import {Ledger} from '../scripts/harness/ledger.ts';
import {ProcessRegistry} from '../scripts/harness/process_registry.ts';
import {Recovery} from '../scripts/harness/recovery.ts';
import {skillDigest} from '../scripts/harness/skill_digest.ts';
import {canonical} from '../src/strict_json.ts';
const sha=(s:string)=>createHash('sha256').update(s).digest('hex');
function fixture(){
 const root=realpathSync(mkdtempSync(join(tmpdir(),'vector-unlaunched-'))),skill=join(root,'skill'),plan=join(root,'plan.json'),output=join(root,'output');mkdirSync(skill);writeFileSync(join(skill,'SKILL.md'),'unit fixture');writeFileSync(plan,canonical({operations:[]}));
 const ledger=new Ledger(join(root,'state.sqlite')),processes=new ProcessRegistry(ledger.db),binding={launchProtocol:'registered-go/v1',launchContext:{skill,plan,runtimeHome:join(root,'runtime'),python:'python3',source:null},skillSha256:skillDigest(skill),planHash:sha(canonical({operations:[]})),runtimeIdentity:'b'.repeat(64),projectRevision:null,inputHashes:{},authorization:{objects:[],fields:[],maxAttempts:1,maxBytes:10000,deadline:Date.now()+60000,readRoots:[root],writeRoots:[root]}};
 const task=ledger.claim('one',join(output,'project.vectorcraft'),output,binding as any),recovery=new Recovery(ledger,processes);return {root,skill,plan,output,ledger,task,recovery,close(){ledger.close();rmSync(root,{recursive:true,force:true});}};
}
test('ready crash seals launch and verifies no source/no output without inventing native inspection',async()=>{const f=fixture();try{
 const leftover=join(f.root,'partial-snapshot');mkdirSync(leftover);writeFileSync(join(leftover,'preserved'),'partial bytes');
 const proof=await f.recovery.inspect(f.task.id,1);assert.equal(proof.schema,'vectorcraft-unlaunched-inspection/v1');assert.equal(proof.nativeInspection,'not-applicable-no-source');
 assert.equal(proof.owner,null);assert.equal(f.ledger.get(f.task.id).attempts,0);assert.equal(existsSync(f.output),false);
 const result=f.recovery.settle(f.task.id,1,proof.checkId);assert.equal(result.state,'interrupted_verified');assert.equal(result.epoch,2);assert.equal(result.attempts,0);assert.equal(existsSync(leftover),true);
 assert.throws(()=>f.ledger.authorizeLaunch(f.task.id,1),/stale_epoch/);
}finally{f.close();}});
test('unlaunched recovery refuses new output and retains occupation',async()=>{const f=fixture();try{
 mkdirSync(f.output);await assert.rejects(()=>f.recovery.inspect(f.task.id,1),/unlaunched_output_present/);assert.equal(f.ledger.get(f.task.id).state,'reconciling');
 assert.throws(()=>f.ledger.claim('other',join(f.output,'project.vectorcraft'),join(f.root,'other'),f.task.binding),/resource_busy/);
}finally{f.close();}});
test('unlaunched settlement refuses plan or launch gate changed after inspection',async()=>{const f=fixture();try{
 const proof=await f.recovery.inspect(f.task.id,1);writeFileSync(f.plan,canonical({operations:['changed']}));assert.throws(()=>f.recovery.settle(f.task.id,1,proof.checkId),/recovery_plan_mismatch/);assert.equal(f.ledger.get(f.task.id).epoch,1);
 writeFileSync(f.plan,canonical({operations:[]}));f.ledger.db.prepare("UPDATE native_launches SET state='prepared' WHERE task=?").run(f.task.id);assert.throws(()=>f.recovery.settle(f.task.id,1,proof.checkId),/recovery_launch_identity_mismatch/);
}finally{f.close();}});
test('submitted but unlaunched crash still requires recorded execution snapshot identity',async()=>{const f=fixture();try{
 f.ledger.intent(f.task.id,1,0,{},100);await assert.rejects(()=>f.recovery.inspect(f.task.id,1),/recovery_identity_missing/);assert.equal(f.ledger.get(f.task.id).attempts,1);
}finally{f.close();}});
test('cancelling an unlaunched ready task persists state even before snapshot directory creation',async()=>{const f=fixture();const {Controller}=await import('../scripts/harness/controller.ts');const controller=new Controller(join(f.root,'state.sqlite'));try{
 assert.equal(existsSync(controller.snapshotRoot),false);assert.equal(controller.requestCancel(f.task.id,1).state,'cancel_requested');
 const proof=await f.recovery.inspect(f.task.id,1);const task=f.recovery.settle(f.task.id,1,proof.checkId);assert.equal(task.state,'cancelled');assert.equal(task.epoch,2);assert.equal(task.attempts,0);
}finally{controller.close();f.close();}});
