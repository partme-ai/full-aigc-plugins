/** 评审父进程必须在读取清单前授权，且不能在目录替换后读取外部字节。 */
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {syncBuiltinESMExports} from 'node:module';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {ReviewStore} from '../src/evaluation/review_store.ts';
import {TechnicalReview} from '../src/evaluation/technical_review.ts';

for(const mode of ['unauthorized-manifest','replaced-manifest','replaced-review-input'])test(`review refuses ${mode} before external bytes are read`,async()=>{
 const root=fs.mkdtempSync(join(tmpdir(),'vectorcraft-review-read-')),allowed=join(root,'allowed'),outside=join(root,'outside');
 fs.mkdirSync(allowed);fs.mkdirSync(outside);
 const name=mode==='replaced-review-input'?'brief.txt':'manifest.json',path=join(allowed,name);
 const manifest=JSON.stringify({schema:'vectorcraft-delivery/v1',runtimeSha256:'a'.repeat(64),files:{'project.vectorcraft':'b'.repeat(64)},outputs:[]});
 fs.writeFileSync(path,name==='manifest.json'?manifest:'authorized brief');fs.writeFileSync(join(outside,name),name==='manifest.json'?manifest:'outside synthetic sentinel');
 const store=new ReviewStore(join(root,'state.sqlite'),[allowed]);
 const read=fs.readFileSync,real=fs.realpathSync;let swapped=false,externalRead=false;
 try{
  fs.realpathSync=((value:any,...args:any[])=>{
   const resolved=(real as any)(value,...args);
   if(mode!=='unauthorized-manifest'&&String(value)===path&&!swapped){swapped=true;fs.renameSync(allowed,join(root,'original'));fs.symlinkSync(outside,allowed,'dir');}
   return resolved;
  }) as typeof fs.realpathSync;
  fs.readFileSync=((value:any,...args:any[])=>{
   if(String(value).replace('/private/var/','/var/')===path.replace('/private/var/','/var/')&&(mode==='unauthorized-manifest'||swapped))externalRead=true;
   return (read as any)(value,...args);
  }) as typeof fs.readFileSync;syncBuiltinESMExports();
  let error:unknown;
  try{
   if(mode==='replaced-review-input')store.fingerprint(path);
   else await new TechnicalReview(store).request({native:join(allowed,'project.vectorcraft'),runtimeIdentity:'a'.repeat(64),projectRevision:'b'.repeat(64),authorization:{readRoots:mode==='unauthorized-manifest'?[outside]:[allowed]}});
  }catch(caught){error=caught;}
  if(mode!=='unauthorized-manifest')assert(swapped,'must reach actual authorization-to-read boundary');
  assert.equal(externalRead,false,'parent attempted to read bytes beyond frozen authorization');
  assert.match(String(error),/outside_roots|asset_read_outside_root/);
  assert.equal((store.db.prepare('SELECT COUNT(*) AS n FROM reviews').get() as any).n,0);
 }finally{fs.readFileSync=read;fs.realpathSync=real;syncBuiltinESMExports();store.close();fs.rmSync(root,{recursive:true,force:true});}
});
