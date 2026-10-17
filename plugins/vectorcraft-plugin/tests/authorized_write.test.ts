/** 快照内容写入保留排他创建、只读权限及原子状态更新语义。 */
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import {authorizedWrite} from '../scripts/harness/authorized_write.ts';
test('exclusive writes return the held identity and preserve existing plan bytes',()=>{
 const root=fs.realpathSync(fs.mkdtempSync(join(tmpdir(),'vectorcraft-safe-write-')));try{
  const path=join(root,'plan.json'),bytes=Buffer.from([0,255,13,10,128]);
  const result=authorizedWrite(path,root,bytes,0o400),stat=fs.statSync(path);
  assert.deepEqual(fs.readFileSync(path),bytes);assert.equal(stat.mode&0o777,0o400);assert.equal(result.device,stat.dev);assert.equal(result.inode,stat.ino);
  assert.equal(result.sha256,createHash('sha256').update(bytes).digest('hex'));
  assert.throws(()=>authorizedWrite(path,root,'replacement',0o400),/authorized_write_failed/);assert.deepEqual(fs.readFileSync(path),bytes);
 }finally{fs.rmSync(root,{recursive:true,force:true});}
});
test('atomic state replaces a final link without following it and leaves no temporary files',()=>{
 const root=fs.realpathSync(fs.mkdtempSync(join(tmpdir(),'vectorcraft-atomic-state-')));try{
  const outside=join(root,'external'),state=join(root,'state.json');fs.writeFileSync(outside,'synthetic external sentinel');fs.symlinkSync(outside,state);
  authorizedWrite(state,root,'first state',0o600,true);authorizedWrite(state,root,'next state',0o600,true);
  assert.equal(fs.readFileSync(state,'utf8'),'next state');assert.equal(fs.readFileSync(outside,'utf8'),'synthetic external sentinel');assert(!fs.lstatSync(state).isSymbolicLink());
  assert.equal(fs.statSync(state).mode&0o777,0o600);assert.deepEqual(fs.readdirSync(root).sort(),['external','state.json']);
 }finally{fs.rmSync(root,{recursive:true,force:true});}
});
test('write refuses traversal, outside targets and linked parents without external effects',()=>{
 const root=fs.realpathSync(fs.mkdtempSync(join(tmpdir(),'vectorcraft-write-scope-'))),allowed=join(root,'allowed'),outside=join(root,'outside');fs.mkdirSync(allowed);fs.mkdirSync(outside);
 try{
  fs.symlinkSync(outside,join(allowed,'link'),'dir');
  assert.throws(()=>authorizedWrite(join(allowed,'link','state'),allowed,'payload',0o600),/authorized_write_failed/);
  assert.throws(()=>authorizedWrite(join(outside,'state'),allowed,'payload',0o600),/authorized_write_outside_root/);
  assert.throws(()=>authorizedWrite(allowed+'/../outside/state',allowed,'payload',0o600),/authorized_write_outside_root/);
  assert.deepEqual(fs.readdirSync(outside),[]);
 }finally{fs.rmSync(root,{recursive:true,force:true});}
});
