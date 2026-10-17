/** 安全快照复制保留大工程语义，并保护已存在或越界目标。 */
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {createHash} from 'node:crypto';
import {authorizedCopy,authorizedDigest} from '../scripts/harness/authorized_file.ts';
function fixture(){const root=fs.realpathSync(fs.mkdtempSync(join(tmpdir(),'vectorcraft-copy-')));for(const part of ['input','output','outside'])fs.mkdirSync(join(root,part));return root;}
test('stream copy preserves a 65MiB project, digest and readonly mode',()=>{
 const root=fixture();try{
  const source=join(root,'input','large.dat'),target=join(root,'output','large.dat'),fd=fs.openSync(source,'wx');try{fs.ftruncateSync(fd,65*1024*1024);}finally{fs.closeSync(fd);}
  const expected=authorizedDigest(source,[join(root,'input')]);authorizedCopy(source,[join(root,'input')],target,join(root,'output'),expected);
  assert.equal(authorizedDigest(target,[join(root,'output')]),expected);assert.equal(fs.statSync(target).size,65*1024*1024);assert.equal(fs.statSync(target).mode&0o777,0o400);
 }finally{fs.rmSync(root,{recursive:true,force:true});}
});
test('copy rejects digest drift and removes only the newly created target',()=>{
 const root=fixture();try{
  const source=join(root,'input','source'),target=join(root,'output','snapshot');fs.writeFileSync(source,'synthetic input');
  assert.throws(()=>authorizedCopy(source,[join(root,'input')],target,join(root,'output'),'0'.repeat(64)),/stale_source_dependencies/);assert(!fs.existsSync(target));
  fs.writeFileSync(target,'existing snapshot');assert.throws(()=>authorizedCopy(source,[join(root,'input')],target,join(root,'output'),authorizedDigest(source,[root])));
  assert.equal(fs.readFileSync(target,'utf8'),'existing snapshot');
 }finally{fs.rmSync(root,{recursive:true,force:true});}
});
test('copy rejects source and destination links and a target outside the frozen write root',()=>{
 const root=fixture();try{
  const source=join(root,'input','source');fs.writeFileSync(source,'synthetic input');const expected=createHash('sha256').update('synthetic input').digest('hex');
  fs.symlinkSync(join(root,'outside'),join(root,'output','redirect'),'dir');
  assert.throws(()=>authorizedCopy(source,[join(root,'input')],join(root,'output','redirect','copy'),join(root,'output'),expected));
  assert.throws(()=>authorizedCopy(source,[join(root,'input')],join(root,'outside','copy'),join(root,'output'),expected),/snapshot_write_outside_root/);
  fs.renameSync(join(root,'input'),join(root,'original'));fs.symlinkSync(join(root,'original'),join(root,'input'),'dir');
  assert.throws(()=>authorizedCopy(source,[join(root,'input')],join(root,'output','copy'),join(root,'output'),expected),/asset_read_outside_root/);
  assert.deepEqual(fs.readdirSync(join(root,'outside')),[]);assert(!fs.existsSync(join(root,'output','copy')));
 }finally{fs.rmSync(root,{recursive:true,force:true});}
});
