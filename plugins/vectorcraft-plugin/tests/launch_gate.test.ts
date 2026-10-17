import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,realpathSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {Ledger} from '../scripts/harness/ledger.ts';
const binding={launchProtocol:'registered-go/v1',launchContext:{skill:'/fixture/skill',plan:'/fixture/plan',runtimeHome:'/fixture/runtime',python:'python3',source:null},planHash:'a'.repeat(64),inputHashes:{},projectRevision:null,runtimeIdentity:'b'.repeat(64),authorization:{objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:2,maxBytes:1000}};
function fixture(){const root=realpathSync(mkdtempSync(join(tmpdir(),'vector-launch-'))),ledger=new Ledger(join(root,'state.sqlite'));const task=ledger.claim('one',join(root,'output/project.vectorcraft'),join(root,'output'),binding as any);ledger.db.exec('CREATE TABLE IF NOT EXISTS native_processes(task TEXT,epoch INTEGER,identity TEXT)');return {ledger,task,close(){ledger.close();rmSync(root,{recursive:true,force:true});}};}
test('unlaunched ready task can be sealed and late intent cannot reserve budget',()=>{const f=fixture();try{
 const gate=f.ledger.sealUnlaunched(f.task.id,1);assert.equal(gate.state,'sealed');assert.equal(f.ledger.get(f.task.id).state,'reconciling');
 assert.throws(()=>f.ledger.intent(f.task.id,1,0,{},100),/reconcile_required/);assert.equal(f.ledger.get(f.task.id).attempts,0);
 assert.throws(()=>f.ledger.authorizeLaunch(f.task.id,1),/launch_not_authorized/);
}finally{f.close();}});
test('GO needs registered process and intent; authorized GO cannot become unlaunched',()=>{const f=fixture();try{
 assert.throws(()=>f.ledger.authorizeLaunch(f.task.id,1),/launch_not_authorized/);
 f.ledger.intent(f.task.id,1,0,{original:true},100);assert.throws(()=>f.ledger.authorizeLaunch(f.task.id,1),/native_process_identity_missing/);
 f.ledger.db.prepare('INSERT INTO native_processes VALUES(?,?,?)').run(f.task.id,1,'unit fixture; not native stop evidence');
 f.ledger.authorizeLaunch(f.task.id,1);assert.equal(f.ledger.sealUnlaunched(f.task.id,1),null);
 assert.throws(()=>f.ledger.authorizeLaunch(f.task.id,1),/launch_not_authorized/);assert.equal(f.ledger.get(f.task.id).attempts,1);
}finally{f.close();}});
test('sealing submitted task retains reservation and prevents late GO',()=>{const f=fixture();try{
 f.ledger.intent(f.task.id,1,0,{original:true},100);const gate=f.ledger.sealUnlaunched(f.task.id,1);assert.equal(gate.state,'sealed');
 assert.throws(()=>f.ledger.authorizeLaunch(f.task.id,1),/launch_not_authorized/);assert.equal(f.ledger.get(f.task.id).attempts,1);assert.equal(f.ledger.get(f.task.id).bytes,100);
 assert.throws(()=>f.ledger.sealUnlaunched(f.task.id,2),/stale_epoch/);
}finally{f.close();}});
test('missing new protocol gate is not proof of no native execution',()=>{const f=fixture();try{
 f.ledger.db.prepare('DELETE FROM native_launches WHERE task=?').run(f.task.id);assert.throws(()=>f.ledger.sealUnlaunched(f.task.id,1),/recovery_launch_identity_missing/);
}finally{f.close();}});
test('independent SQLite connections serialize sealing against GO authorization',()=>{const f=fixture();const other=new Ledger((f.ledger.db.prepare('PRAGMA database_list').get() as any).file);try{
 f.ledger.intent(f.task.id,1,0,{original:true},100);f.ledger.db.prepare('INSERT INTO native_processes VALUES(?,?,?)').run(f.task.id,1,'unit registration fixture');
 other.sealUnlaunched(f.task.id,1);assert.throws(()=>f.ledger.authorizeLaunch(f.task.id,1),/launch_not_authorized/);assert.equal(f.ledger.get(f.task.id).attempts,1);
}finally{other.close();f.close();}});
test('legacy tasks do not acquire a no-GO conclusion retroactively',()=>{const f=fixture();try{
 const legacy={...binding};delete (legacy as any).launchProtocol;delete (legacy as any).launchContext;
 const task=f.ledger.claim('legacy','/fixture/legacy.vectorcraft','/fixture/legacy-output',legacy as any);assert.equal(f.ledger.sealUnlaunched(task.id,1),null);
}finally{f.close();}});
test('deadline expiry between intent and GO refuses launch without resetting consumed budget',()=>{const f=fixture();const now=Date.now;try{
 f.ledger.intent(f.task.id,1,0,{original:true},100);f.ledger.db.prepare('INSERT INTO native_processes VALUES(?,?,?)').run(f.task.id,1,'unit registration fixture');
 Date.now=()=>binding.authorization.deadline+1;assert.throws(()=>f.ledger.authorizeLaunch(f.task.id,1),/launch_not_authorized/);assert.equal(f.ledger.get(f.task.id).attempts,1);
}finally{Date.now=now;f.close();}});
