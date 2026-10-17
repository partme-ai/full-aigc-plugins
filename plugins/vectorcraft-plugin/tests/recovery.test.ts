import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync,writeFileSync,rmSync,mkdirSync,lstatSync,readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import { Ledger } from '../scripts/harness/ledger.ts';
import { Recovery } from '../scripts/harness/recovery.ts';
import {canonical} from '../src/strict_json.ts';

// 账本提交门禁单元测试；原生重开与真实进程停止由 opt-in 验收另行证明。
function fixture(){
 const root=mkdtempSync(join(tmpdir(),'vectorcraft-recovery-')),ledger=new Ledger(join(root,'state.sqlite'));
 const binding={planHash:'a'.repeat(64),runtimeIdentity:'b'.repeat(64),inputHashes:{},projectRevision:null,authorization:{objects:[4],fields:['paint.color'],deadline:Date.now()+60000,maxAttempts:1,maxBytes:1000}};
 const source=join(root,'source.vectorcraft');writeFileSync(source,'original');
 const task=ledger.claim('one',source,join(root,'out'),binding);ledger.intent(task.id,task.epoch,0,{},10);ledger.cancel(task.id,task.epoch,false);
 const stage=join(root,'stage');mkdirSync(stage);const file=join(stage,'checkpoint.vectorcraft');writeFileSync(file,'fixture');
 const stat=lstatSync(file),stageStat=lstatSync(stage),digest=createHash('sha256').update(readFileSync(file)).digest('hex');
 const recovery=new Recovery(ledger,{observe:()=>({stopped:true})} as any);
 const step=ledger.db.prepare('SELECT intent,state,result FROM steps WHERE task=? AND n=0').get(task.id);
 const stepIdentity=createHash('sha256').update(canonical(step)).digest('hex');
 const proof={stepIdentity,owner:'fixture-inspection',stage,stageInode:stageStat.ino,stageDevice:stageStat.dev,files:{[file]:{sha256:digest,bytes:stat.size,inode:stat.ino}},classification:'verified-interrupted-files; not successful delivery'};
 ledger.db.prepare('INSERT INTO recovery_checks(id,task,epoch,intent,result) VALUES(?,?,?,?,?)').run('inspection',task.id,task.epoch,'{}',JSON.stringify(proof));
 return {root,ledger,task,stage,file,recovery,close(){ledger.close();rmSync(root,{recursive:true,force:true});}};
}
test('settling a verified interruption fences the previous epoch and never claims delivery',()=>{
 const f=fixture();try{
   assert.throws(()=>f.recovery.settle(f.task.id,1,'missing'),/native_inspection_required/);
   const settled=f.recovery.settle(f.task.id,1,'inspection');assert.equal(settled.state,'cancelled');assert.equal(settled.epoch,2);
   assert.throws(()=>f.ledger.receipt(f.task.id,1,0,{late:true}),/stale_epoch/);
   assert.equal((f.ledger.db.prepare('SELECT COUNT(*) AS n FROM late_receipts').get() as any).n,1);
   assert.equal(f.ledger.get(f.task.id).state,'cancelled');
 }finally{f.close();}
});
test('new or changed original files after inspection keep writer occupation',()=>{
 for(const change of ['added','changed']){
  const f=fixture();try{
   if(change==='added')writeFileSync(join(f.stage,'late.vectorcraft'),'late write');else writeFileSync(f.file,'changed');
   assert.throws(()=>f.recovery.settle(f.task.id,1,'inspection'),/original_artifact_changed/);
   assert.equal(f.ledger.get(f.task.id).state,'cancel_requested');
  }finally{f.close();}
 }
});

test('receipt changes after inspection and old proofs without step identity retain occupation',()=>{
 for(const change of ['receipt','legacy-proof']){
  const f=fixture();try{
   if(change==='receipt')f.ledger.db.prepare("UPDATE steps SET result='{}',state='quarantined' WHERE task=?").run(f.task.id);
   else{
    const row=f.ledger.db.prepare('SELECT result FROM recovery_checks WHERE id=?').get('inspection') as any;
    const proof=JSON.parse(row.result);delete proof.stepIdentity;
    f.ledger.db.prepare('UPDATE recovery_checks SET result=? WHERE id=?').run(JSON.stringify(proof),'inspection');
   }
   assert.throws(()=>f.recovery.settle(f.task.id,1,'inspection'),change==='receipt'?/recovery_receipt_changed/:/recovery_receipt_identity_missing/);
   assert.equal(f.ledger.get(f.task.id).state,'cancel_requested');
  }finally{f.close();}
 }
});
