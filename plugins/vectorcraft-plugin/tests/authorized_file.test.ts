/** 批量安全摘要须保持原文件大小语义；大文件使用稀疏夹具，不写入用户媒体。 */
import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,writeFileSync,openSync,ftruncateSync,closeSync,rmSync,mkdirSync,realpathSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import {authorizedRead,authorizedDigests} from '../scripts/harness/authorized_file.ts';
const hash=(bytes:Buffer)=>createHash('sha256').update(bytes).digest('hex');
test('batch fingerprints preserve binary bytes,duplicates,chunking and files above64MiB',()=>{
 const root=mkdtempSync(join(tmpdir(),'vectorcraft-batch-read-'));try{
  const small=join(root,'binary.dat'),large=join(root,'large.dat'),data=Buffer.from([0,255,13,10,128]);writeFileSync(small,data);
  const fd=openSync(large,'wx');try{ftruncateSync(fd,65*1024*1024);}finally{closeSync(fd);}
  const expected=createHash('sha256'),block=Buffer.alloc(1024*1024);for(let i=0;i<65;i++)expected.update(block);
  const actual=authorizedDigests([small,large,...Array(4096).fill(small)],[realpathSync(root)]);
  assert.deepEqual({...actual},{[small]:hash(data),[large]:expected.digest('hex')});
  assert.deepEqual(authorizedRead(small,[realpathSync(root)]),data);
  assert.throws(()=>authorizedRead(large,[realpathSync(root)]),/asset_digest_mismatch/);
 }finally{rmSync(root,{recursive:true,force:true});}
});
test('batch read refuses a file outside the frozen root without returning its content',()=>{
 const root=mkdtempSync(join(tmpdir(),'vectorcraft-batch-scope-')),allowed=join(root,'allowed');mkdirSync(allowed);
 try{const file=join(root,'outside.txt');writeFileSync(file,'synthetic outside sentinel');assert.throws(()=>authorizedDigests([file],[realpathSync(allowed)]),error=>/asset_read_outside_root/.test(String(error))&&!String(error).includes('synthetic outside sentinel'));}
 finally{rmSync(root,{recursive:true,force:true});}
});
