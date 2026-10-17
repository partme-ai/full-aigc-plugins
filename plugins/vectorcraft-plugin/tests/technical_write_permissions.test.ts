/** 技术评审目录、捕获快照和报告写入不得被父目录替换重定向。 */
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import childProcess from 'node:child_process';
import {syncBuiltinESMExports} from 'node:module';
import {tmpdir} from 'node:os';
import {join,dirname} from 'node:path';
import {createHash} from 'node:crypto';
import {ReviewStore} from '../src/evaluation/review_store.ts';
import {TechnicalReview} from '../src/evaluation/technical_review.ts';
const hash=(v:string|Buffer)=>createHash('sha256').update(v).digest('hex');
for(const stage of ['output-directory','delivery-snapshot','report','request-mutation'])test(`technical ${stage} refuses replaced parent without external effects`,async()=>{
 const root=fs.realpathSync(fs.mkdtempSync(join(tmpdir(),'vectorcraft-technical-write-'))),source=join(root,'delivery'),outside=join(root,'outside'),base=join(root,'.technical-checks');fs.mkdirSync(source);fs.mkdirSync(outside);
 fs.writeFileSync(join(source,'project.vectorcraft'),'synthetic native');fs.writeFileSync(join(source,'preview.png'),Buffer.from('\x89PNG\r\n\x1a\ncorrupt','binary'));
 const files=Object.fromEntries(['project.vectorcraft','preview.png'].map(name=>[name,hash(fs.readFileSync(join(source,name)))]));fs.writeFileSync(join(source,'manifest.json'),JSON.stringify({schema:'vectorcraft-delivery/v1',runtimeSha256:'a'.repeat(64),files,outputs:[{path:'preview.png'}],fontDependencies:[]}));
 const brief=join(root,'brief.txt'),rubric=join(root,'rubric.json'),loss=join(root,'loss.json');for(const path of [brief,rubric,loss])fs.writeFileSync(path,'{}');
 const input={native:join(source,'project.vectorcraft'),projectRevision:files['project.vectorcraft'],runtimeIdentity:'a'.repeat(64),candidates:[join(source,'preview.png')],targets:[{path:brief,role:'target'}],rubric,exchangeLoss:loss,technicalStatus:'PASS',authorization:{objects:[2],fields:['paint.color'],deadline:Date.now()+60000,maxAttempts:3,maxBytes:8*1024*1024,readRoots:[root],writeRoots:[root]}};
 const store=new ReviewStore(join(root,'state.sqlite'),[root]),mkdir=fs.mkdirSync,read=fs.readFileSync,spawn=childProcess.spawnSync,launch=childProcess.spawn;let swapped=false;
 const swap=(path:string)=>{if(swapped)return;swapped=true;fs.renameSync(path,path+'-original');fs.symlinkSync(outside,path,'dir');};
 const afterDirectory=(path:string)=>{if(stage==='output-directory'&&path===base||stage==='delivery-snapshot'&&path.startsWith(base+'/')&&path.endsWith('/delivery'))swap(path);};
 try{
  fs.mkdirSync=((path:any,...args:any[])=>{const result=(mkdir as any)(path,...args);afterDirectory(String(path));return result;}) as typeof fs.mkdirSync;
  fs.readFileSync=((path:any,...args:any[])=>{const result=(read as any)(path,...args);if(stage==='report'&&String(path).startsWith(base+'/')&&String(path).endsWith('/checker/scripts/harness/authorized_file.ts'))swap(String(path).split('/checker/')[0]);return result;}) as typeof fs.readFileSync;
  childProcess.spawnSync=((command:any,args:any,options:any)=>{const result=(spawn as any)(command,args,options);if(args?.some((arg:any)=>/authorized_tree.py|asset_digest.py/.test(String(arg)))){const request=JSON.parse(options.input);if(request.operation==='directory')afterDirectory(request.path);if(stage==='report'&&request.operation==='file-digests'&&request.paths.some((path:string)=>path.includes('/checker/')))swap(dirname(request.paths[0].split('/checker/')[0]+'/report.json'));}return result;}) as typeof childProcess.spawnSync;syncBuiltinESMExports();
  childProcess.spawn=((...args:any[])=>{const child=(launch as any)(...args);if(stage==='request-mutation')input.authorization.deadline=0;return child;}) as typeof childProcess.spawn;syncBuiltinESMExports();
  let failure:unknown,request:any;try{request=await new TechnicalReview(store).request(input);}catch(error){failure=error;}
  if(stage==='request-mutation'){assert.equal(failure,undefined);assert.equal(input.authorization.deadline,0);assert(request.input.authorization.deadline>Date.now());assert.equal(typeof request.id,'string');return;}
  assert(swapped,'must reach the targeted write boundary');assert.deepEqual(fs.readdirSync(outside),[],'must not create snapshots or reports outside the frozen root');assert.match(String(failure),/authorized_tree_failed|authorized_write_failed/);
  assert.equal((store.db.prepare('SELECT COUNT(*) AS n FROM reviews').get() as any).n,0);
  if(stage!=='report')assert.equal((store.db.prepare('SELECT COUNT(*) AS n FROM native_processes').get() as any).n,0);
 }finally{fs.mkdirSync=mkdir;fs.readFileSync=read;childProcess.spawnSync=spawn;childProcess.spawn=launch;syncBuiltinESMExports();store.close();fs.rmSync(root,{recursive:true,force:true});}
});
