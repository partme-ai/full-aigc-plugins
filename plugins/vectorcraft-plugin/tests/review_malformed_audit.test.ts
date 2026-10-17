/** 无法解析的评审回执保留摘要审计，不能记录可能含秘密的原文。 */
import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,writeFileSync,rmSync} from 'node:fs';
import {join,resolve} from 'node:path';
import {tmpdir} from 'node:os';
import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {ReviewStore} from '../src/evaluation/review_store.ts';
const raw='{"password":"synthetic-malformed-secret",';
for(const entry of ['store','cli'])test(entry+' persists a redacted malformed receipt rejection',()=>{
 const root=mkdtempSync(join(tmpdir(),'vectorcraft-malformed-review-')),database=join(root,'state.sqlite');
 try{
  if(entry==='store'){
   const store=new ReviewStore(database);try{assert.throws(()=>store.importReceipt(raw));}finally{store.close();}
  }else{
   const input=join(root,'receipt.json');writeFileSync(input,raw);
   const result=spawnSync(process.execPath,[resolve('src/cli.ts'),'review-import',database,input],{encoding:'utf8'});
   assert.notEqual(result.status,0);assert(!(result.stdout+result.stderr).includes('synthetic-malformed-secret'));
  }
  const restarted=new ReviewStore(database);try{
   const rows=restarted.db.prepare('SELECT * FROM review_events').all() as any[];assert.equal(rows.length,1,'malformed JSON rejection was not persisted');
   assert.equal(rows[0].reason,'invalid_review_json');assert.equal(rows[0].request,null);
   assert.deepEqual(JSON.parse(rows[0].receipt),{sha256:createHash('sha256').update(raw).digest('hex'),bytes:Buffer.byteLength(raw),withheld:true});
   assert(!JSON.stringify(rows).includes('synthetic-malformed-secret'));
  }finally{restarted.close();}
 }finally{rmSync(root,{recursive:true,force:true});}
});
