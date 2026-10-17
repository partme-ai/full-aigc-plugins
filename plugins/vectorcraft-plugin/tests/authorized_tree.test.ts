/** 描述符快照树保持现有摘要、文件字节和执行位，拒绝越界或替换已有目标。 */
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {skillDigest} from '../scripts/harness/controller.ts';
import {authorizedDirectory,authorizedTreeCopy,authorizedTreeDigest} from '../scripts/harness/authorized_tree.ts';
function fixture(){return fs.realpathSync(fs.mkdtempSync(join(tmpdir(),'vectorcraft-safe-tree-')));}
test('directory creation stays inside frozen roots and preserves existing exclusive targets',()=>{
 const root=fixture();try{
  const allowed=join(root,'allowed'),outside=join(root,'outside');fs.mkdirSync(allowed);fs.mkdirSync(outside);
  authorizedDirectory(join(allowed,'nested','leaf'),allowed);assert.equal(fs.statSync(join(allowed,'nested','leaf')).mode&0o777,0o700);
  assert.throws(()=>authorizedDirectory(join(allowed,'nested'),allowed,true),/authorized_tree_failed/);
  fs.symlinkSync(outside,join(allowed,'redirect'),'dir');assert.throws(()=>authorizedDirectory(join(allowed,'redirect','leaf'),allowed),/authorized_tree_failed/);
  assert.throws(()=>authorizedDirectory(join(outside,'leaf'),allowed),/authorized_tree_outside_root/);assert.deepEqual(fs.readdirSync(outside),[]);
 }finally{fs.rmSync(root,{recursive:true,force:true});}
});
test('tree copy and digest preserve binary bytes, empty directories, Unicode sorting and executable modes',()=>{
 const root=fixture();try{
  const source=join(root,'source'),target=join(root,'target');fs.mkdirSync(source);fs.mkdirSync(join(source,'empty'));
  for(const name of ['𐀀.bin','\uE000.bin','plain.sh'])fs.writeFileSync(join(source,name),Buffer.from([0,255,13,10,128]),{mode:0o755});
  const expected=skillDigest(source);authorizedTreeCopy(source,target,root,expected);
  assert.equal(authorizedTreeDigest(target),expected);assert.equal(skillDigest(target),expected);assert(fs.statSync(join(target,'empty')).isDirectory());assert.equal(fs.statSync(join(target,'plain.sh')).mode&0o777,0o755);
  assert.throws(()=>authorizedTreeCopy(source,target,root,expected),/authorized_tree_failed/);assert.equal(skillDigest(target),expected);
 }finally{fs.rmSync(root,{recursive:true,force:true});}
});
test('tree snapshot rejects digest drift, source links and replaced snapshot roots',()=>{
 const root=fixture();try{
  const source=join(root,'source');fs.mkdirSync(source);fs.writeFileSync(join(source,'input'),'synthetic source');const expected=skillDigest(source);
  assert.throws(()=>authorizedTreeCopy(source,join(root,'wrong-digest'),root,'0'.repeat(64)),/skill_snapshot_mismatch/);assert.equal(fs.readFileSync(join(root,'wrong-digest','input'),'utf8'),'synthetic source');
  fs.symlinkSync(join(root,'wrong-digest','input'),join(source,'link'));assert.throws(()=>authorizedTreeCopy(source,join(root,'linked-source'),root,expected),/authorized_tree_entry_invalid/);
  fs.symlinkSync(join(root,'wrong-digest'),join(root,'replaced'));assert.throws(()=>authorizedTreeDigest(join(root,'replaced')),/authorized_tree_failed/);
  assert.equal(fs.readFileSync(join(source,'input'),'utf8'),'synthetic source');
 }finally{fs.rmSync(root,{recursive:true,force:true});}
});
