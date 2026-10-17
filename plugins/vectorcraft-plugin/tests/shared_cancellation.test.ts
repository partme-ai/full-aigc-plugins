import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,realpathSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {Ledger} from '../scripts/harness/ledger.ts';
function fixture(){const root=realpathSync(mkdtempSync(join(tmpdir(),'vector-budget-'))),path=join(root,'state.sqlite'),ledger=new Ledger(path),binding={planHash:'a'.repeat(64),runtimeIdentity:'b'.repeat(64),projectRevision:null,inputHashes:{},authorization:{budgetId:'workflow-one',deadline:Date.now()+60000,maxAttempts:3,maxBytes:1000,objects:[],fields:[]}};
 const claim=(key:string,b= binding)=>ledger.claim(key,join(root,key+'.vectorcraft'),join(root,key),b);
 return {root,path,ledger,binding,claim,close(){ledger.close();rmSync(root,{recursive:true,force:true});}};}
test('shared cancellation reaches running and ready children, fences future admission and retains budget across restart',()=>{const f=fixture();try{
 const parent=f.claim('parent'),child=f.claim('child'),ready=f.claim('ready');f.ledger.intent(parent.id,1,0,{},100);f.ledger.intent(child.id,1,0,{},200);
 f.ledger.cancel(parent.id,1,false);for(const task of [parent,child,ready])assert.equal(f.ledger.get(task.id).state,'cancel_requested');
 const restarted=new Ledger(f.path);try{
  assert.throws(()=>restarted.claim('later',join(f.root,'later.vectorcraft'),join(f.root,'later'),f.binding),/budget_cancel_requested/);
  assert.throws(()=>restarted.intent(child.id,1,1,{},100),/cancel_requested/);assert.equal(restarted.get(child.id).attempts,1);
  assert.equal((restarted.db.prepare('SELECT bytes FROM budgets WHERE id=?').get('workflow-one') as any).bytes,300);
  assert.equal(restarted.receipt(child.id,1,0,{late:true}).state,'quarantined');
 }finally{restarted.close();}
}finally{f.close();}});
test('private cancellation leaves independent and already reviewed tasks untouched',()=>{const f=fixture();try{
 const parent=f.claim('parent'),reviewed=f.claim('reviewed'),other=f.claim('other',{...f.binding,authorization:{...f.binding.authorization,budgetId:'workflow-two'}});
 f.ledger.db.prepare("UPDATE tasks SET state='review_ready' WHERE id=?").run(reviewed.id);
 f.ledger.cancel(parent.id,1,false);assert.equal(f.ledger.get(other.id).state,'ready');assert.equal(f.ledger.get(reviewed.id).state,'review_ready');
 assert.equal(f.ledger.get(parent.id).epoch,1);
}finally{f.close();}});
test('database guards reject stale readers admitting cancelled-budget tasks or native steps',()=>{const f=fixture();try{
 const parent=f.claim('parent'),child=f.claim('child');const reader=new Ledger(f.path);try{
  f.ledger.cancel(parent.id,1,false);
  assert.throws(()=>reader.db.prepare('INSERT INTO steps(task,n,intent,state) VALUES(?,0,?,?)').run(child.id,'{}','submitted'),/budget_cancel_requested/);
  const original=reader.db.prepare('SELECT * FROM tasks WHERE id=?').get(parent.id) as any;
  assert.throws(()=>reader.db.prepare('INSERT INTO tasks(id,key,resource,output,binding_hash,binding,state) VALUES(?,?,?,?,?,?,?)').run('stale','stale','/stale/source','/stale/out',original.binding_hash,original.binding,'ready'),/budget_cancel_requested/);
 }finally{reader.close();}
}finally{f.close();}});
test('spent shared output budget rejects a new dependent task before admission',()=>{const f=fixture();try{
 const task=f.claim('first');f.ledger.intent(task.id,1,0,{},1000);assert.throws(()=>f.claim('second'),/budget_exceeded/);
 assert.equal((f.ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,1);
}finally{f.close();}});
test('one failed stop observation still persists cancellation and attempts the other group',async()=>{const f=fixture();const {Controller}=await import('../scripts/harness/controller.ts');const controller=new Controller(f.path);try{
 const parent=f.claim('parent'),child=f.claim('child');controller.ledger.db.prepare('INSERT INTO native_processes(task,epoch,identity) VALUES(?,1,?)').run(parent.id,'unit parent');controller.ledger.db.prepare('INSERT INTO native_processes(task,epoch,identity) VALUES(?,1,?)').run(child.id,'unit child');
 const calls:string[]=[];controller.processes.signal=(task:string)=>{calls.push(task);if(task===parent.id)throw new Error('unit observation failed');};
 assert.equal(controller.requestCancel(parent.id,1).state,'cancel_requested');assert.deepEqual(new Set(calls),new Set([parent.id,child.id]));assert.match(controller.ledger.get(parent.id).reason,/native_stop_unconfirmed/);assert.equal(controller.ledger.get(child.id).state,'cancel_requested');
}finally{controller.close();f.close();}});
