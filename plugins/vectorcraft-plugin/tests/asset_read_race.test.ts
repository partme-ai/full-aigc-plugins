/** 父进程素材预检不得在检查路径后无约束读取被替换的目录。 */
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {syncBuiltinESMExports} from 'node:module';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {Controller,skillDigest} from '../scripts/harness/controller.ts';

test('Controller refuses a replaced asset ancestor before reading outside bytes',async()=>{
 const root=fs.mkdtempSync(join(tmpdir(),'vectorcraft-parent-asset-'));
 const allowed=join(root,'allowed'),outside=join(root,'outside');fs.mkdirSync(allowed);fs.mkdirSync(outside);
 const asset=join(allowed,'logo.svg'),data=Buffer.from('<svg xmlns="http://www.w3.org/2000/svg" width="8" height="8"/>');
 fs.writeFileSync(asset,data);fs.writeFileSync(join(outside,'logo.svg'),'<svg>outside synthetic sentinel</svg>');
 const plan=join(root,'plan.json');fs.writeFileSync(plan,JSON.stringify({document:{width:16,height:16},assets:{logo:{path:asset,sha256:createHash('sha256').update(data).digest('hex')}},operations:[{command:'asset.place',params:{asset:'logo',rect:[0,0,8,8]}}]}));
 const controller=new Controller(join(root,'state.sqlite'));
 const originalStat=fs.lstatSync,originalRead=fs.readFileSync;let swapped=false,outsideRead=false;
 try {
  fs.lstatSync=((path:any,...args:any[])=>{
   if(String(path)===asset&&!swapped){swapped=true;fs.renameSync(allowed,join(root,'original'));fs.symlinkSync(outside,allowed,'dir');}
   return (originalStat as any)(path,...args);
  }) as typeof fs.lstatSync;
  fs.readFileSync=((path:any,...args:any[])=>{
   if(String(path)===asset&&swapped)outsideRead=true;
   return (originalRead as any)(path,...args);
  }) as typeof fs.readFileSync;
  syncBuiltinESMExports();
  let error:any;try{await controller.run({key:'ancestor-race',skill:resolve('skills/vectorcraft-harness'),expectedSkillSha256:skillDigest(resolve('skills/vectorcraft-harness')),
   plan,output:join(root,'delivery'),runtimeHome:join(root,'runtime'),python:process.env.VECTORCRAFT_TEST_PYTHON??(fs.existsSync('/opt/anaconda3/bin/python3')?'/opt/anaconda3/bin/python3':'python3'),estimatedBytes:1048576,
   authorization:{objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:1,maxBytes:1048576,readRoots:[plan,allowed],writeRoots:[root]}});}catch(caught){error=caught;}
  assert(swapped,'test must reach the path-to-read boundary');
  assert.equal(outsideRead,false,'Node parent attempted to read outside bytes');
  assert.match(String(error),/asset_read_outside_root/);
  assert(!fs.existsSync(join(root,'delivery'))&&!fs.existsSync(join(root,'runtime')));
 }finally{fs.lstatSync=originalStat;fs.readFileSync=originalRead;syncBuiltinESMExports();controller.close();fs.rmSync(root,{recursive:true,force:true});}
});
