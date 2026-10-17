/** 账本验收只读取任务冻结的输出根；相同摘要不能授权额外读取路径。 */
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {syncBuiltinESMExports} from 'node:module';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import {Ledger} from '../scripts/harness/ledger.ts';
for(const mode of ['outside-artifact','replaced-output'])test(`ledger verification refuses ${mode} before reading external bytes`,()=>{
 const root=fs.realpathSync(fs.mkdtempSync(join(tmpdir(),'vectorcraft-ledger-read-'))),output=join(root,'output'),outside=join(root,'outside');fs.mkdirSync(output);fs.mkdirSync(outside);
 for(const folder of [output,outside])fs.writeFileSync(join(folder,'artifact.txt'),'synthetic artifact');
 const ledger=new Ledger(join(root,'state.sqlite')),read=fs.readFileSync;let externalRead=false;
 try{
  const task=ledger.claim(mode,join(output,'project.vectorcraft'),output,{planHash:'a'.repeat(64),inputHashes:{},projectRevision:null,runtimeIdentity:'b'.repeat(64),authorization:{objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:1,maxBytes:1048576}});
  ledger.intent(task.id,task.epoch,0,{synthetic:true},0);ledger.receipt(task.id,task.epoch,0,{synthetic:true});
  if(mode==='replaced-output'){fs.renameSync(output,output+'-original');fs.symlinkSync(outside,output,'dir');}
  const artifact=join(mode==='outside-artifact'?outside:output,'artifact.txt');
  fs.readFileSync=((path:any,...args:any[])=>{if(String(path)===artifact)externalRead=true;return (read as any)(path,...args);}) as typeof fs.readFileSync;syncBuiltinESMExports();
  let failure:unknown;try{ledger.verified(task.id,task.epoch,{path:artifact,sha256:createHash('sha256').update('synthetic artifact').digest('hex')});}catch(error){failure=error;}
  assert.equal(externalRead,false,'ledger parent must not read bytes outside the task output');assert.match(String(failure),/asset_read_outside_root/);assert.equal(ledger.get(task.id).state,'running');
 }finally{fs.readFileSync=read;syncBuiltinESMExports();ledger.close();fs.rmSync(root,{recursive:true,force:true});}
});
