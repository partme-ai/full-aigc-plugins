import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {Ledger} from '../scripts/harness/ledger.ts';

test('selected runtime identity is checked inside the task claim transaction',()=>{
 const root=mkdtempSync(join(tmpdir(),'craft-selection-')),l=new Ledger(join(root,'state.sqlite'));
 try{
  l.db.exec('CREATE TABLE IF NOT EXISTS runtime_selection(id INTEGER PRIMARY KEY,active TEXT NOT NULL,previous TEXT)');
  l.db.prepare('INSERT INTO runtime_selection VALUES(1,?,NULL)').run(JSON.stringify({mode:'headless',binarySha256:'a'.repeat(64)}));
  const binding={planHash:'a'.repeat(64),runtimeIdentity:'b'.repeat(64),inputHashes:{},projectRevision:null,authorization:{objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:1,maxBytes:100}};
  assert.throws(()=>l.claim('wrong','/tmp/craft-wrong-runtime','/tmp/craft-wrong-out',binding),/runtime_selection_mismatch/);
  assert.equal((l.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,0);
 }finally{l.db.close();rmSync(root,{recursive:true,force:true});}
});
