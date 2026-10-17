/** Controller的计划、源工程和额外输入检查不得在路径授权后读到目录外字节。 */
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {syncBuiltinESMExports} from 'node:module';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {Controller,skillDigest} from '../scripts/harness/controller.ts';
const hash=(bytes:string|Buffer)=>createHash('sha256').update(bytes).digest('hex');
const physical=(path:any)=>String(path).replace('/private/var/','/var/');
for(const mode of ['plan','source','guard'])test(`Controller refuses replaced ${mode} ancestor before external bytes`,async()=>{
 const root=fs.mkdtempSync(join(tmpdir(),'vectorcraft-controller-read-'));
 const folders=Object.fromEntries(['plan','source','guard','outside'].map(name=>{const path=join(root,name);fs.mkdirSync(path);return [name,path];}));
 const native=join(folders.source,'project.vectorcraft'),plan=join(folders.plan,'plan.json'),guard=join(folders.guard,'brief.txt');
 fs.writeFileSync(native,'authorized synthetic source');fs.writeFileSync(guard,'authorized synthetic brief');
 fs.writeFileSync(plan,JSON.stringify({operations:[],...(mode==='source'?{expectedProjectSha256:hash('authorized synthetic source')}:{})}));
 const path=mode==='plan'?plan:mode==='source'?native:guard;
 fs.writeFileSync(join(folders.outside,mode==='plan'?'plan.json':mode==='source'?'project.vectorcraft':'brief.txt'),mode==='plan'?fs.readFileSync(plan):'outside synthetic sentinel');
 // 执行载荷收敛在 vectorcraft-harness：托管执行控制与运行时锁只在 harness 技能内。
 const skill=resolve('skills/vectorcraft-harness'),expected=skillDigest(skill);let probes=0;
 const controller=new Controller(join(root,'state.sqlite'),async()=>{probes++;throw new Error('probe_should_not_run');});
 const read=fs.readFileSync,real=fs.realpathSync,stat=fs.lstatSync;let swapped=false,externalRead=false,planChecks=0;
 const swap=()=>{swapped=true;fs.renameSync(folders[mode],join(root,'original'));fs.symlinkSync(folders.outside,folders[mode],'dir');};
 try{
  fs.realpathSync=((value:any,...args:any[])=>{
   const result=(real as any)(value,...args);
   if(physical(value)===physical(path)&&!swapped){if(mode==='guard'||mode==='plan'&&++planChecks===2)swap();}
   return result;
  }) as typeof fs.realpathSync;
  fs.lstatSync=((value:any,...args:any[])=>{if(mode==='source'&&physical(value)===physical(path)&&!swapped)swap();return (stat as any)(value,...args);}) as typeof fs.lstatSync;
  fs.readFileSync=((value:any,...args:any[])=>{if(swapped&&physical(value)===physical(path))externalRead=true;return (read as any)(value,...args);}) as typeof fs.readFileSync;syncBuiltinESMExports();
  let error:unknown;try{await controller.run({key:mode,skill,expectedSkillSha256:expected,plan,output:join(root,'delivery'),runtimeHome:join(root,'runtime'),estimatedBytes:1048576,
   ...(mode==='source'?{source:folders.source}:{}),...(mode==='guard'?{inputFingerprints:{[guard]:hash('authorized synthetic brief')}}:{}),
   authorization:{objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:1,maxBytes:1048576,readRoots:[folders.plan,folders.source,folders.guard],writeRoots:[root]}});}catch(caught){error=caught;}
  assert(swapped,'must reach authorization-to-read boundary');assert.equal(externalRead,false,'Node parent read bytes outside frozen roots');
  assert.match(String(error),/asset_read_outside_root/);assert.equal(probes,0);assert.equal((controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,0);
  assert(!fs.existsSync(join(root,'delivery'))&&!fs.existsSync(join(root,'runtime')));
 }finally{fs.readFileSync=read;fs.realpathSync=real;fs.lstatSync=stat;syncBuiltinESMExports();controller.close();fs.rmSync(root,{recursive:true,force:true});}
});
