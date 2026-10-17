/** 交付检查不得扩张冻结读取根，也不得用哈希检查之后被替换的原生JSON验收。 */
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {syncBuiltinESMExports} from 'node:module';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import {Controller} from '../scripts/harness/controller.ts';
const hash=(v:string|Buffer)=>createHash('sha256').update(v).digest('hex');
const physical=(v:any)=>String(v).replace('/private/var/','/var/');
for(const mode of ['root','nested'])test(`delivery refuses replaced ${mode} ancestor before external bytes`,()=>{
 const root=fs.mkdtempSync(join(tmpdir(),'vectorcraft-delivery-read-')),output=join(root,'delivery'),outside=join(root,'outside');fs.mkdirSync(output);fs.mkdirSync(outside);fs.mkdirSync(join(output,'assets'));
 const project=join(output,'project.vectorcraft'),asset=join(output,'assets/logo.svg');fs.writeFileSync(project,'synthetic native');fs.writeFileSync(asset,'synthetic logo');fs.writeFileSync(join(outside,mode==='root'?'project.vectorcraft':'logo.svg'),'outside synthetic sentinel');
 fs.writeFileSync(join(output,'manifest.json'),JSON.stringify({schema:'vectorcraft-delivery/v1',runtimeSha256:'a'.repeat(64),files:{'project.vectorcraft':hash('synthetic native'),'assets/logo.svg':hash('synthetic logo')}}));
 if(mode==='root'){fs.mkdirSync(join(outside,'assets'));fs.writeFileSync(join(outside,'assets/logo.svg'),'outside synthetic logo');}
 const controller=new Controller(join(root,'state.sqlite')),target=mode==='root'?project:asset,folder=mode==='root'?output:join(output,'assets');const stat=fs.lstatSync,read=fs.readFileSync;let swapped=false,externalRead=false;
 try{
  fs.lstatSync=((path:any,...args:any[])=>{if(physical(path)===physical(target)&&!swapped){swapped=true;fs.renameSync(folder,join(root,'original'));fs.symlinkSync(outside,folder,'dir');}return (stat as any)(path,...args);}) as typeof fs.lstatSync;
  fs.readFileSync=((path:any,...args:any[])=>{if(swapped&&physical(path)===physical(target))externalRead=true;return (read as any)(path,...args);}) as typeof fs.readFileSync;syncBuiltinESMExports();
  let error:unknown;try{controller.verifyDelivery(output,'a'.repeat(64));}catch(caught){error=caught;}
  assert(swapped);assert.equal(externalRead,false,'delivery parent read outside bytes');assert.match(String(error),/asset_read_outside_root|artifact_digest_mismatch/);
 }finally{fs.lstatSync=stat;fs.readFileSync=read;syncBuiltinESMExports();controller.close();fs.rmSync(root,{recursive:true,force:true});}
});
test('geometry cannot use native JSON changed after its manifest digest was checked',()=>{
 const root=fs.mkdtempSync(join(tmpdir(),'vectorcraft-delivery-binding-')),output=join(root,'delivery');fs.mkdirSync(output);
 const native={units:'Points',artboards:[{id:2,rect:{x0:0,y0:0,x1:100,y1:100}}],layers:[{id:4,kind:{type:'path',path:{subpaths:[{closed:false,anchors:[{p:[10,10]},{p:[20,20]}]}]}},appearance:{items:[]}}]};
 const correct=JSON.stringify(native);native.layers[0].kind.path.subpaths[0].anchors[0].p=[11,10];const incorrect=JSON.stringify(native);
 fs.writeFileSync(join(output,'project.vectorcraft'),'unit native');fs.writeFileSync(join(output,'native.json'),incorrect);const extra=join(output,'extra.txt');fs.writeFileSync(extra,'unit extra');
 fs.writeFileSync(join(output,'manifest.json'),JSON.stringify({schema:'vectorcraft-delivery/v1',runtimeSha256:'a'.repeat(64),files:{'project.vectorcraft':hash('unit native'),'native.json':hash(incorrect),'extra.txt':hash('unit extra')}}));
 const contract:any={schema:'vectorcraft-geometry-contract/v1',units:'Points',coordinateSpace:'artboard-local',tolerance:0.000001,artboards:[{id:2,rect:[0,0,100,100]}],paths:[{objectId:4,artboardId:2,subpaths:[{closed:false,anchors:[{p:[10,10]},{p:[20,20]}]}],strokes:[]}]};
 const controller=new Controller(join(root,'state.sqlite')),stat=fs.lstatSync;let changed=false;
 try{
  fs.lstatSync=((path:any,...args:any[])=>{if(physical(path)===physical(extra)&&!changed){changed=true;fs.writeFileSync(join(output,'native.json'),correct);}return (stat as any)(path,...args);}) as typeof fs.lstatSync;syncBuiltinESMExports();
  assert.throws(()=>controller.verifyDelivery(output,'a'.repeat(64),contract),/artifact_digest_mismatch/);assert(changed);
 }finally{fs.lstatSync=stat;syncBuiltinESMExports();controller.close();fs.rmSync(root,{recursive:true,force:true});}
});
