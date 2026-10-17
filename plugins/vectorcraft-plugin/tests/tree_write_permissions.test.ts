/** 目录创建和技能复制不能在快照父目录被替换后产生根外内容。 */
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import childProcess from 'node:child_process';
import {syncBuiltinESMExports} from 'node:module';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import {Controller,skillDigest} from '../scripts/harness/controller.ts';
import {runtimeFixture} from './runtime_fixture.ts';
const hash=(v:string)=>createHash('sha256').update(v).digest('hex');
for(const stage of ['skill-copy','source-directory'])test(`snapshot parent swap refuses external ${stage} effects`,async()=>{
 const root=fs.realpathSync(fs.mkdtempSync(join(tmpdir(),'vectorcraft-tree-write-'))),skill=join(root,'skill'),source=join(root,'source'),outside=join(root,'outside');
 for(const folder of [join(skill,'scripts'),source,outside])fs.mkdirSync(folder,{recursive:true});
 fs.writeFileSync(join(skill,'scripts','workflow.py'),'raise RuntimeError("must not launch")');fs.writeFileSync(join(skill,'scripts','execution_control.py'),'# synthetic fixture');
 fs.writeFileSync(join(skill,'scripts','runtime.lock.json'),JSON.stringify({artifacts:{'darwin-arm64':{binarySha256:'c'.repeat(64)}}}));
 fs.writeFileSync(join(source,'project.vectorcraft'),'synthetic native');fs.writeFileSync(join(source,'manifest.json'),JSON.stringify({schema:'vectorcraft-delivery/v1',files:{'project.vectorcraft':hash('synthetic native')}}));
 const probe=runtimeFixture(skill,'c'.repeat(64)),plan=join(root,'plan.json');fs.writeFileSync(plan,JSON.stringify({operations:[],expectedProjectSha256:hash('synthetic native')}));
 const controller=new Controller(join(root,'state.sqlite'),probe),mkdir=fs.mkdirSync,copy=fs.cpSync,spawn=childProcess.spawnSync;let swapped=false;
 const swap=()=>{if(swapped)return;swapped=true;fs.renameSync(controller.snapshotRoot,controller.snapshotRoot+'-original');fs.symlinkSync(outside,controller.snapshotRoot,'dir');};
 try{
  fs.mkdirSync=((path:any,...args:any[])=>{if(stage==='source-directory'&&String(path).endsWith('-source'))swap();const result=(mkdir as any)(path,...args);if(stage==='skill-copy'&&String(path)===controller.snapshotRoot)swap();return result;}) as typeof fs.mkdirSync;
  fs.cpSync=((...args:any[])=>{const result=(copy as any)(...args);return result;}) as typeof fs.cpSync;
  childProcess.spawnSync=((command:any,args:any,options:any)=>{const request=args?.some((arg:any)=>String(arg).endsWith('authorized_tree.py'))?JSON.parse(options.input):null;if(stage==='source-directory'&&request?.operation==='directory'&&request.path.endsWith('-source'))swap();const result=(spawn as any)(command,args,options);if(stage==='skill-copy'&&request?.operation==='directory'&&request.path===controller.snapshotRoot)swap();return result;}) as typeof childProcess.spawnSync;syncBuiltinESMExports();
  let failure:unknown;try{await controller.run({key:stage,skill,expectedSkillSha256:skillDigest(skill),plan,source,output:join(root,'delivery'),runtimeHome:join(root,'runtime'),estimatedBytes:1048576,authorization:{objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:1,maxBytes:1048576,readRoots:[source,plan],writeRoots:[root]}});}catch(error){failure=error;}
  assert(swapped,'must reach the checked directory boundary');assert.deepEqual(fs.readdirSync(outside),[],'must not create directories or copy files outside frozen snapshots');assert.match(String(failure),/authorized_tree_failed/);
  assert.equal((controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM native_processes').get() as any).n,0);
 }finally{fs.mkdirSync=mkdir;fs.cpSync=copy;childProcess.spawnSync=spawn;syncBuiltinESMExports();controller.close();fs.rmSync(root,{recursive:true,force:true});}
});
