import test from 'node:test';
import assert from 'node:assert/strict';
import {DatabaseSync} from 'node:sqlite';
import {mkdtempSync,rmSync,readFileSync,statSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import {Ledger} from '../scripts/harness/ledger.ts';
const sha=(p:string)=>createHash('sha256').update(readFileSync(p)).digest('hex');
test('legacy v1 migration retains an immutable consistent backup and consumed task budget',()=>{
 const root=mkdtempSync(join(tmpdir(),'vector-state-migration-')),path=join(root,'state.sqlite');let ledger=new Ledger(path);
 try{
  const task=ledger.claim('legacy','/tmp/vector-legacy-project','/tmp/vector-legacy-output',{planHash:'a'.repeat(64),inputHashes:{},projectRevision:null,runtimeIdentity:'b'.repeat(64),authorization:{objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:2,maxBytes:100}});
  ledger.intent(task.id,1,0,{legacy:true},17);ledger.unknown(task.id,1,'legacy interruption');ledger.close();
  const old=new DatabaseSync(path);old.exec('DROP TABLE budgets; DROP TABLE late_receipts; PRAGMA user_version=1');old.close();
  ledger=new Ledger(path);const backup=(ledger as any).schemaBackup;
  assert.ok(backup,'migration must record backup before schema update');assert.equal(backup.fromSchema,1);assert.equal(backup.toSchema,3);assert.equal(backup.sha256,sha(backup.path));assert.equal(statSync(backup.path).mode&0o777,0o400);
  const snapshot=new DatabaseSync(backup.path,{readOnly:true});try{
   assert.equal((snapshot.prepare('PRAGMA user_version').get() as any).user_version,1);
   assert.equal(snapshot.prepare("SELECT name FROM sqlite_master WHERE name='budgets'").get(),undefined);
   assert.equal((snapshot.prepare('SELECT attempts,bytes,state FROM tasks WHERE id=?').get(task.id) as any).attempts,1);
  }finally{snapshot.close();}
  assert.equal(ledger.get(task.id).attempts,1);assert.equal(ledger.get(task.id).bytes,17);assert.equal(ledger.get(task.id).state,'reconciling');assert.equal((ledger.db.prepare('PRAGMA user_version').get() as any).user_version,3);
  const hash=sha(backup.path);ledger.db.prepare('UPDATE tasks SET reason=? WHERE id=?').run('later inspection',task.id);assert.equal(sha(backup.path),hash);
 }finally{try{ledger.close();}catch{}rmSync(root,{recursive:true,force:true});}
});

test('backup directory links are refused before modifying the legacy schema',async()=>{
 const {mkdirSync,symlinkSync,readdirSync}=await import('node:fs');
 const root=mkdtempSync(join(tmpdir(),'vector-backup-refusal-')),path=join(root,'state.sqlite'),user=join(root,'user-files');mkdirSync(user);
 const seed=new DatabaseSync(path);seed.exec('PRAGMA user_version=1; CREATE TABLE original(value TEXT)');seed.prepare('INSERT INTO original VALUES(?)').run('keep');seed.close();
 symlinkSync(user,join(root,'state-schema-backups'));
 try{
  assert.throws(()=>new Ledger(path),/state_backup_failed/);
  const old=new DatabaseSync(path);try{assert.equal((old.prepare('PRAGMA user_version').get() as any).user_version,1);assert.equal((old.prepare('SELECT value FROM original').get() as any).value,'keep');assert.equal(old.prepare("SELECT name FROM sqlite_master WHERE name='budgets'").get(),undefined);}finally{old.close();}
  assert.deepEqual(readdirSync(user),[]);
 }finally{rmSync(root,{recursive:true,force:true});}
});

test('mode-aware state uses a new schema so a schema2-only reader cannot be selected',async()=>{
 const {RuntimeGate}=await import('../src/runtime/runtime_gate.ts');const root=mkdtempSync(join(tmpdir(),'vector-mode-schema-')),ledger=new Ledger(join(root,'state.sqlite'));
 try{
  const report={schema:'vectorcraft-runtime-probe/v1',mode:'headless',binarySha256:'a'.repeat(64),version:'fixture',commands:[{id:'fixture',params:'{}'}],tools:[]};
  assert.throws(()=>new RuntimeGate(ledger).activate(report,{mode:'headless',commands:{},tools:{}},[2]),/incompatible_state_schema/);
  assert.equal((ledger.db.prepare('PRAGMA user_version').get() as any).user_version,3);
 }finally{ledger.close();rmSync(root,{recursive:true,force:true});}
});

test('schema2 upgrades keep selection and budgets; the actual previous reader rejects schema3',async()=>{
 const {Ledger:OldLedger}=await import('../docs/evidence/pre-runtime-boundaries-identity/src/harness/ledger.ts');
 const root=mkdtempSync(join(tmpdir(),'vector-v2-migration-')),path=join(root,'state.sqlite');const old=new OldLedger(path);
 const task=old.claim('v2','/tmp/vector-v2-project','/tmp/vector-v2-output',{planHash:'a'.repeat(64),inputHashes:{},projectRevision:null,runtimeIdentity:'b'.repeat(64),authorization:{objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:2,maxBytes:100}});
 old.intent(task.id,1,0,{v2:true},17);old.close();const ledger=new Ledger(path);
 try{
  assert.equal(ledger.schemaBackup?.fromSchema,2);assert.equal(ledger.schemaBackup?.toSchema,3);
  assert.equal(ledger.get(task.id).attempts,1);assert.equal(ledger.get(task.id).bytes,17);
  assert.throws(()=>new OldLedger(path),/incompatible_state_schema/);
  assert.equal((ledger.db.prepare('PRAGMA user_version').get() as any).user_version,3);
 }finally{ledger.close();rmSync(root,{recursive:true,force:true});}
});
