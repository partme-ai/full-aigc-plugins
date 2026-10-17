import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,rmSync} from 'node:fs';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {DatabaseSync} from 'node:sqlite';
import {Ledger} from '../scripts/harness/ledger.ts';
import {Ledger as PreviousLedger} from '../docs/evidence/pre-runtime-boundaries-identity/src/harness/ledger.ts';
test('migration preserves original WAL selection, consumed shared budget and task rows in both snapshot and schema3',()=>{
 const root=mkdtempSync(join(tmpdir(),'vector-selection-migration-')),path=join(root,'state.sqlite');const previous=new PreviousLedger(path);
 const binding={planHash:'a'.repeat(64),inputHashes:{},projectRevision:null,runtimeIdentity:'b'.repeat(64),authorization:{objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:4,maxBytes:100,budgetId:'retained-budget'}};
 const task=previous.claim('previous','/tmp/retained-state-project','/tmp/retained-state-output',binding);previous.intent(task.id,1,0,{native:'submitted'},17);
 previous.db.exec('CREATE TABLE runtime_selection(id INTEGER PRIMARY KEY,active TEXT NOT NULL,previous TEXT)');
 const active=JSON.stringify({binarySha256:binding.runtimeIdentity,mode:'headless',stateSchemas:[2]}),older=JSON.stringify({version:'retained-older-runtime'});
 previous.db.prepare('INSERT INTO runtime_selection VALUES(1,?,?)').run(active,older);
 const rows=Object.fromEntries(['tasks','steps','budgets','runtime_selection'].map(table=>[table,previous.db.prepare('SELECT * FROM '+table).all()]));
 let migrated:Ledger|undefined;
 try{
  // 保持旧连接和WAL打开，证明快照包含已提交且尚未checkpoint的数据。
  migrated=new Ledger(path);assert.ok(migrated.schemaBackup);const backup=new DatabaseSync(migrated.schemaBackup.path,{readOnly:true});
  try{for(const table of Object.keys(rows)){assert.deepEqual(migrated.db.prepare('SELECT * FROM '+table).all(),rows[table]);assert.deepEqual(backup.prepare('SELECT * FROM '+table).all(),rows[table]);}assert.equal((backup.prepare('PRAGMA user_version').get() as any).user_version,2);}finally{backup.close();}
  assert.equal((migrated.db.prepare('PRAGMA user_version').get() as any).user_version,3);
  assert.throws(()=>migrated!.claim('new','/tmp/retained-new-project','/tmp/retained-new-output',binding),/incompatible_state_schema/);
  assert.throws(()=>previous.claim('already-open-old-reader','/tmp/retained-old-reader-project','/tmp/retained-old-reader-output',binding),/incompatible_state_schema/);
  assert.equal((migrated.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,1);
 }finally{previous.close();migrated?.close();rmSync(root,{recursive:true,force:true});}
});

test('database guard rejects mode, binary and schema bypass through direct legacy SQL',()=>{
 const root=mkdtempSync(join(tmpdir(),'vector-sql-writer-guard-')),ledger=new Ledger(join(root,'state.sqlite'));
 try{
  const binding={runtimeIdentity:'a'.repeat(64)};
  const insert=ledger.db.prepare("INSERT INTO tasks(id,key,resource,output,binding_hash,binding,state) VALUES('legacy','legacy','/tmp/legacy-raw-resource','/tmp/legacy-raw-output','hash',?,'ready')");
  for(const [active,reason] of [[{mode:'bridge',binarySha256:binding.runtimeIdentity,stateSchemas:[3]},/runtime_mode_mismatch/],[{mode:'headless',binarySha256:'b'.repeat(64),stateSchemas:[3]},/runtime_selection_mismatch/],[{mode:'headless',binarySha256:binding.runtimeIdentity,stateSchemas:[2]},/incompatible_state_schema/]] as const){
   ledger.db.prepare('INSERT INTO runtime_selection(id,active) VALUES(1,?) ON CONFLICT(id) DO UPDATE SET active=excluded.active').run(JSON.stringify(active));
   assert.throws(()=>insert.run(JSON.stringify(binding)),reason);assert.equal((ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,0);
  }
 }finally{ledger.close();rmSync(root,{recursive:true,force:true});}
});
