import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {Ledger} from '../scripts/harness/ledger.ts';
import {RuntimeGate,validateCapabilities} from '../src/runtime/runtime_gate.ts';
const hash='a'.repeat(64),other='b'.repeat(64);
const report=(identity=hash)=>({schema:'vectorcraft-runtime-probe/v1',mode:'headless',binarySha256:identity,version:'fixture 1',commands:[{id:'document.new',params:'{width,height}'}],tools:[{name:'run_command',inputSchema:{type:'object'}}]});
const requirements={mode:'headless',commands:{'document.new':'{width,height}'},tools:{run_command:{type:'object'}}};
function fixture(fn:(l:Ledger,g:RuntimeGate)=>void){const root=mkdtempSync(join(tmpdir(),'craft-runtime-gate-')),l=new Ledger(join(root,'state.sqlite'));try{fn(l,new RuntimeGate(l));}finally{l.db.close();rmSync(root,{recursive:true,force:true});}}
const binding=(identity=hash)=>({planHash:hash,inputHashes:{},projectRevision:null,runtimeIdentity:identity,authorization:{objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:1,maxBytes:100}});
test('actual schema and mode must match; enabled flags do not substitute for signatures',()=>{
 assert.equal(validateCapabilities(report(),requirements).commandCount,1);
 assert.throws(()=>validateCapabilities(report(),{...requirements,commands:{'document.new':'{width}'}}),/capability_schema_mismatch/);
 assert.throws(()=>validateCapabilities(report(),{...requirements,mode:'bridge'}),/runtime_mode_mismatch/);
 assert.throws(()=>validateCapabilities(report(),{...requirements,commands:{'missing':'{}'}}),/capability_missing/);
 assert.throws(()=>validateCapabilities({...report(),commands:[...report().commands,...report().commands]},requirements),/invalid_runtime_registry/);
 assert.throws(()=>validateCapabilities({...report(),tools:[]},requirements),/capability_missing/);
});
test('activation drains tasks, guards claim atomically, retains previous version and survives restart',()=>fixture((l,g)=>{
 g.activate(report(),requirements,[3]);
 const task=l.claim('one','/tmp/craft-runtime-one','/tmp/craft-runtime-out',binding());
 assert.throws(()=>g.activate(report(other),requirements,[3]),/runtime_tasks_not_drained/);
 assert.equal(g.current().active.binarySha256,hash);
 l.db.prepare("UPDATE tasks SET state='completed' WHERE id=?").run(task.id);
 g.activate(report(other),requirements,[3]);
 g.activate(report(other),requirements,[3]);
 assert.equal(new RuntimeGate(l).current().previous.binarySha256,hash);
 assert.throws(()=>l.claim('two','/tmp/craft-runtime-two','/tmp/craft-runtime-out2',binding()),/runtime_selection_mismatch/);
 assert.equal(l.claim('three','/tmp/craft-runtime-three','/tmp/craft-runtime-out3',binding(other)).state,'ready');
}));
test('incompatible rollback and unconfirmed native groups retain active identity',()=>fixture((l,g)=>{
 g.activate(report(),requirements,[1,2,3]);g.activate(report(other),requirements,[3]);
 assert.throws(()=>g.activate(report(),requirements,[1]),/incompatible_state_schema/);
 l.db.exec('CREATE TABLE native_processes(task TEXT,epoch INTEGER,identity TEXT,stopped_at INTEGER)');
 l.db.prepare('INSERT INTO native_processes VALUES(?,?,?,NULL)').run('old',1,'{}');
 assert.throws(()=>g.activate(report(),requirements,[3]),/runtime_process_stop_unconfirmed/);
 assert.equal(g.current().active.binarySha256,other);
}));
test('bridge selection cannot silently execute a headless Controller task',()=>fixture((l,g)=>{
 g.activate({...report(),mode:'bridge'}, {...requirements,mode:'bridge'},[3]);
 assert.throws(()=>l.claim('one','/tmp/craft-runtime-one','/tmp/craft-runtime-out',binding()),/runtime_mode_mismatch/);
}));

test('every unresolved task state prevents activation',()=>fixture((l,g)=>{
 g.activate(report(),requirements,[3]);const task=l.claim('pending','/tmp/craft-runtime-pending','/tmp/craft-runtime-pending-out',binding());
 for(const state of ['ready','running','reconciling','cancel_requested']){
  l.db.prepare('UPDATE tasks SET state=? WHERE id=?').run(state,task.id);
  assert.throws(()=>g.activate(report(other),requirements,[3]),/runtime_tasks_not_drained/);
 }
}));

test('an explicitly bridge-bound native task registers against its selected bridge runtime',()=>fixture((l,g)=>{
 g.activate({...report(),mode:'bridge'},{...requirements,mode:'bridge'},[3]);
 const task=l.claim('bridge','/tmp/craft-native-bridge','/tmp/craft-native-bridge-out',{...binding(),executionMode:'bridge'});
 assert.equal(task.state,'ready');assert.equal(task.binding.executionMode,'bridge');
 assert.throws(()=>g.activate(report(),requirements,[3]),/runtime_tasks_not_drained/);
}));

test('inherited schema2 selection cannot claim or bypass drain during schema3 initialization',()=>fixture((l,g)=>{
 g.activate(report(),requirements,[3]);const task=l.claim('legacy-policy','/tmp/vector-old-policy','/tmp/vector-old-policy-out',binding());
 l.db.prepare('UPDATE runtime_selection SET active=? WHERE id=1').run(JSON.stringify({...g.current().active,stateSchemas:[2]}));
 assert.throws(()=>l.claim('new-policy','/tmp/vector-new-policy','/tmp/vector-new-policy-out',binding()),/incompatible_state_schema/);
 assert.throws(()=>g.initialize(report(),requirements,[3]),/runtime_tasks_not_drained/);
 l.db.prepare("UPDATE tasks SET state='completed' WHERE id=?").run(task.id);
 assert.deepEqual(g.initialize(report(),requirements,[3]).active.stateSchemas,[3]);
}));
