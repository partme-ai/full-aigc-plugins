import test from 'node:test';
import assert from 'node:assert/strict';
import {exportWithHostPath} from '../host-export.mjs';
import {mkdtemp, readFile, rm} from 'node:fs/promises';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {writeOutput} from '../runtime/automation.mjs';

const payload=()=>({content:[{type:'text',text:JSON.stringify({dataBase64:Buffer.from('%!PS-Adobe').toString('base64'),format:'ai',warnings:[]})}]});
test('host saves bytes while browser receives no filesystem path',async()=>{
 let forwarded,saved;
 const result=await exportWithHostPath({name:'export',arguments:{path:'交付.ai',options:{aiVersion:'7'}}},async p=>{forwarded=p;return payload();},async(path,bytes)=>{saved={path,bytes};return path;});
 assert.deepEqual(forwarded.arguments,{format:'ai',options:{aiVersion:'7'}});
 assert.equal(saved.path,'交付.ai');assert.equal(saved.bytes.toString(),'%!PS-Adobe');
 const receipt=JSON.parse(result.content[0].text);assert.equal(receipt.path,'交付.ai');assert.equal(receipt.dataBase64,undefined);
});
test('backend errors never create an output',async()=>{
 const failure={isError:true,content:[{type:'text',text:'export failed'}]};let saved=false;
 assert.equal(await exportWithHostPath({name:'export',arguments:{path:'out.ai'}},async()=>failure,async()=>{saved=true;}),failure);
 assert.equal(saved,false);
});
test('save failures are not reported as successful exports',async()=>{
 await assert.rejects(()=>exportWithHostPath({name:'export',arguments:{path:'out.ai'}},async()=>payload(),async()=>{throw Error('outside workspace');}),/outside workspace/);
});
test('pathless exports preserve native byte responses',async()=>{
 const result=payload();assert.equal(await exportWithHostPath({name:'export',arguments:{format:'ai'}},async()=>result,async()=>{throw Error('unexpected write');}),result);
});
test('actual workspace writer handles Unicode, refuses traversal and preserves existing files',async()=>{
 const workspace=await mkdtemp(join(tmpdir(),'vector-export-'));
 const request={name:'export',arguments:{path:'中文 交付.ai'}};
 const save=(path,bytes)=>writeOutput(workspace,path,bytes,true);
 try {
  await exportWithHostPath(request,async()=>payload(),save);
  assert.equal(await readFile(join(workspace,'中文 交付.ai'),'utf8'),'%!PS-Adobe');
  await assert.rejects(()=>exportWithHostPath(request,async()=>payload(),save),/EEXIST/);
  await assert.rejects(()=>exportWithHostPath({name:'export',arguments:{path:'../escape.ai'}},async()=>payload(),save),/workspace/);
  assert.equal(await readFile(join(workspace,'中文 交付.ai'),'utf8'),'%!PS-Adobe');
 } finally {await rm(workspace,{recursive:true,force:true});}
});
