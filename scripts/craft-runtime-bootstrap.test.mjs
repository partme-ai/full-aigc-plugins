import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp, readFile, rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {gzipSync} from 'node:zlib';
import {extractRuntime, verifyRuntime} from './templates/craft-runtime-bootstrap.mjs';
import {createHash} from 'node:crypto';
function archive(name, value, type='0') {
 const h=Buffer.alloc(512);h.write(name);h.write('0000644\0',100);h.write(value.length.toString(8).padStart(11,'0')+'\0',124);h.fill(32,148,156);h.write(type,156);h.write('ustar\0',257);let sum=0;for(const b of h)sum+=b;h.write(sum.toString(8).padStart(6,'0')+'\0 ',148);
 return gzipSync(Buffer.concat([h,Buffer.from(value),Buffer.alloc((512-value.length%512)%512),Buffer.alloc(1024)]));
}
test('verified extraction works in Chinese and space paths and detects subsequent corruption',async()=>{
 const p=await mkdtemp(join(tmpdir(),'Craft 中文 '));try{await extractRuntime(archive('adapter.mjs','ok'),p);assert.equal(await readFile(join(p,'adapter.mjs'),'utf8'),'ok');const files={'adapter.mjs':createHash('sha256').update('ok').digest('hex')};assert.equal(await verifyRuntime(p,files),true);assert.equal(await verifyRuntime(p,{'adapter.mjs':'0'.repeat(64)}),false);}finally{await rm(p,{recursive:true,force:true});}
});
for(const path of ['../outside','/outside','C:/outside','a/../../outside','a\\outside'])test('reject tar path '+path,async()=>{const p=await mkdtemp(join(tmpdir(),'craft-'));try{await assert.rejects(extractRuntime(archive(path,'bad'),p));}finally{await rm(p,{recursive:true,force:true});}});
test('reject archive symlinks',async()=>{const p=await mkdtemp(join(tmpdir(),'craft-'));try{await assert.rejects(extractRuntime(archive('link','bad','2'),p));}finally{await rm(p,{recursive:true,force:true});}});
