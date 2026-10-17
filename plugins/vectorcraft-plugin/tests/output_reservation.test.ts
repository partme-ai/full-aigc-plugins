import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,rmSync,symlinkSync} from 'node:fs';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {DatabaseSync} from 'node:sqlite';
import {Ledger} from '../scripts/harness/ledger.ts';
// 账本／SQL门禁单元用例；原生竞争由task_crash验收脚本覆盖。
function fixture(){const root=mkdtempSync(join(tmpdir(),'vector-output-owner-')),path=join(root,'state.sqlite'),ledger=new Ledger(path);const binding={planHash:'a'.repeat(64),runtimeIdentity:'b'.repeat(64),inputHashes:{},projectRevision:null,authorization:{objects:[1],fields:['paint.color'],deadline:Date.now()+60000,maxAttempts:2,maxBytes:10000}};return {root,path,ledger,binding,close(){ledger.close();rmSync(root,{recursive:true,force:true});}};}
test('different source resources cannot claim one physical output in any unresolved state',()=>{
 for(const state of ['ready','running','reconciling','cancel_requested']){
  const f=fixture();try{
   const output=join(f.root,'output'),task=f.ledger.claim('first',join(f.root,'source-a'),output,f.binding);
   if(state!=='ready')f.ledger.intent(task.id,1,0,{fixture:true},100);
   if(state==='reconciling')f.ledger.unknown(task.id,1,'fixture unknown');if(state==='cancel_requested')f.ledger.cancel(task.id,1,false);
   const alias=join(f.root,'alias');symlinkSync(f.root,alias);
   assert.throws(()=>f.ledger.claim('second',join(f.root,'source-b'),join(alias,'output'),f.binding),/output_busy/);
   assert.equal((f.ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,1);assert.equal((f.ledger.db.prepare('SELECT COUNT(*) AS n FROM budgets').get() as any).n,1);
  }finally{f.close();}
 }
});
test('a separate old SQL connection cannot bypass output occupation',()=>{
 const f=fixture(),old=new DatabaseSync(f.path);try{
  const task=f.ledger.claim('first',join(f.root,'source-a'),join(f.root,'output'),f.binding);
  assert.throws(()=>old.prepare("INSERT INTO tasks(id,key,resource,output,binding_hash,binding,state) VALUES('old','old','different-resource',?,'fixture',?,'ready')").run(task.output,JSON.stringify(f.binding)),/output_busy/);
  assert.equal((f.ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,1);
 }finally{old.close();f.close();}
});
test('output occupation is released only for terminal rows; same-key reads remain idempotent',()=>{
 const f=fixture();try{
  const task=f.ledger.claim('first',join(f.root,'source-a'),join(f.root,'output'),f.binding);assert.equal(f.ledger.claim('first',join(f.root,'source-a'),join(f.root,'output'),f.binding).id,task.id);
  // 仅构造已终结账本状态；不作为真实恢复或进程停止的验收。
  f.ledger.db.prepare("UPDATE tasks SET state='interrupted_verified',epoch=epoch+1 WHERE id=?").run(task.id);
  assert.equal(f.ledger.claim('next',join(f.root,'source-b'),join(f.root,'output'),f.binding).state,'ready');
 }finally{f.close();}
});
