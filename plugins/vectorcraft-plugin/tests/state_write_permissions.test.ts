/** 状态持久化不能通过临时链接或父目录替换改写外部文件。 */
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import childProcess from 'node:child_process';
import {syncBuiltinESMExports} from 'node:module';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {Controller} from '../scripts/harness/controller.ts';
for(const mode of ['temporary-link','parent-swap'])test(`state publication preserves external files under ${mode}`,()=>{
 const root=fs.realpathSync(fs.mkdtempSync(join(tmpdir(),'vectorcraft-state-write-'))),outside=join(root,'outside');fs.mkdirSync(outside);
 const controller=new Controller(join(root,'state.sqlite')),mkdir=fs.mkdirSync,spawn=childProcess.spawnSync;fs.mkdirSync(controller.snapshotRoot);
 const sentinel=join(outside,'sentinel.txt');fs.writeFileSync(sentinel,'synthetic external sentinel');let swapped=false;
 try{
  if(mode==='temporary-link')fs.symlinkSync(sentinel,join(controller.snapshotRoot,'unit-state.json.next'));
  else{
   fs.mkdirSync=((value:any,...args:any[])=>{const result=(mkdir as any)(value,...args);if(String(value)===controller.snapshotRoot&&!swapped){swapped=true;fs.renameSync(controller.snapshotRoot,controller.snapshotRoot+'-original');fs.symlinkSync(outside,controller.snapshotRoot,'dir');}return result;}) as typeof fs.mkdirSync;
   childProcess.spawnSync=((command:any,args:any,options:any)=>{const result=(spawn as any)(command,args,options);if(args?.some((arg:any)=>String(arg).endsWith('authorized_tree.py'))){const request=JSON.parse(options.input);if(request.operation==='directory'&&request.path===controller.snapshotRoot&&!swapped){swapped=true;fs.renameSync(controller.snapshotRoot,controller.snapshotRoot+'-original');fs.symlinkSync(outside,controller.snapshotRoot,'dir');}}return result;}) as typeof childProcess.spawnSync;syncBuiltinESMExports();
  }
  let failure:unknown;try{controller.publishState('unit',1,'running');}catch(error){failure=error;}
  assert.equal(fs.readFileSync(sentinel,'utf8'),'synthetic external sentinel','state write must not truncate external target');
  assert.deepEqual(fs.readdirSync(outside),['sentinel.txt'],'state write must not create files through a replaced directory');
  if(mode==='parent-swap'){assert(swapped);assert.match(String(failure),/authorized_write_failed/);}
  else{assert.equal(failure,undefined);assert.deepEqual(JSON.parse(fs.readFileSync(join(controller.snapshotRoot,'unit-state.json'),'utf8')),{epoch:1,state:'running',task:'unit'});}
 }finally{fs.mkdirSync=mkdir;childProcess.spawnSync=spawn;syncBuiltinESMExports();controller.close();fs.rmSync(root,{recursive:true,force:true});}
});
