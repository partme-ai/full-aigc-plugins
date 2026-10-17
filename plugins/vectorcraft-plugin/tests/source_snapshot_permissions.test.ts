/** 源快照复制必须拒绝检查后目录替换；仅使用合成协调器夹具。 */
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
const hash=(value:string)=>createHash('sha256').update(value).digest('hex');
test('source snapshot refuses an ancestor swapped after link checking before copying bytes',async()=>{
 const root=fs.realpathSync(fs.mkdtempSync(join(tmpdir(),'vectorcraft-source-copy-'))),source=join(root,'source'),skill=join(root,'skill'),outside=join(root,'outside');
 for(const dir of [join(source,'assets'),join(skill,'scripts'),outside])fs.mkdirSync(dir,{recursive:true});
 fs.writeFileSync(join(source,'project.vectorcraft'),'synthetic project');fs.writeFileSync(join(source,'assets','input.txt'),'authorized source');
 fs.writeFileSync(join(outside,'input.txt'),'outside synthetic sentinel');
 fs.writeFileSync(join(source,'manifest.json'),JSON.stringify({schema:'vectorcraft-delivery/v1',files:{'project.vectorcraft':hash('synthetic project'),'assets/input.txt':hash('authorized source')}}));
 fs.writeFileSync(join(skill,'scripts','execution_control.py'),'# fixture');fs.writeFileSync(join(skill,'scripts','workflow.py'),'raise RuntimeError("must not launch")');
 fs.writeFileSync(join(skill,'scripts','runtime.lock.json'),JSON.stringify({artifacts:{'darwin-arm64':{binarySha256:'c'.repeat(64)}}}));
 const probe=runtimeFixture(skill,'c'.repeat(64)),plan=join(root,'plan.json');fs.writeFileSync(plan,JSON.stringify({operations:[],expectedProjectSha256:hash('synthetic project')}));
 const controller=new Controller(join(root,'state.sqlite'),probe),mkdir=fs.mkdirSync,read=fs.readFileSync,spawn=childProcess.spawnSync;let swapped=false,externalRead=false;
 try{
  fs.mkdirSync=((value:any,...args:any[])=>{const result=(mkdir as any)(value,...args);if(String(value).includes('plan-snapshots/')&&String(value).endsWith('-source/assets')&&!swapped){swapped=true;fs.renameSync(join(source,'assets'),join(source,'original-assets'));fs.symlinkSync(outside,join(source,'assets'),'dir');}return result;}) as typeof fs.mkdirSync;
  childProcess.spawnSync=((command:any,args:any,options:any)=>{const result=(spawn as any)(command,args,options);if(args?.some((arg:any)=>String(arg).endsWith('authorized_tree.py'))){const request=JSON.parse(options.input);if(request.operation==='directory'&&request.path.endsWith('-source/assets')&&!swapped){swapped=true;fs.renameSync(join(source,'assets'),join(source,'original-assets'));fs.symlinkSync(outside,join(source,'assets'),'dir');}}return result;}) as typeof childProcess.spawnSync;
  fs.readFileSync=((value:any,...args:any[])=>{if(swapped&&String(value)===join(source,'assets/input.txt'))externalRead=true;return (read as any)(value,...args);}) as typeof fs.readFileSync;syncBuiltinESMExports();
  let failure:unknown;try{await controller.run({key:'copy-race',skill,expectedSkillSha256:skillDigest(skill),plan,source,output:join(root,'delivery'),runtimeHome:join(root,'runtime'),estimatedBytes:1048576,
   authorization:{objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:1,maxBytes:1048576,readRoots:[source,plan],writeRoots:[root]}});}catch(error){failure=error;}
  assert(swapped);assert.equal(externalRead,false,'must not read external source bytes');assert.match(String(failure),/asset_read_outside_root/);assert(!fs.existsSync(join(root,'delivery')));
  assert.equal((controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM native_processes').get() as any).n,0);
 }finally{fs.mkdirSync=mkdir;fs.readFileSync=read;childProcess.spawnSync=spawn;syncBuiltinESMExports();controller.close();fs.rmSync(root,{recursive:true,force:true});}
});
