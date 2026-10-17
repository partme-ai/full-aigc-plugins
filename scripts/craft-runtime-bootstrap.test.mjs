import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp, readFile, rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {gzipSync} from 'node:zlib';
import {extractRuntime, verifyRuntime} from './templates/craft-runtime-bootstrap.mjs';
import {createHash} from 'node:crypto';
function archive(name, value, type='0') {
 const h=Buffer.alloc(512);h.write(name);h.write('0000644\0',100);h.write(value.length.toString(8).padStart(11,'0')+'\0',124);h.fill(32,148,156);h.write(type,156);h.write('ustar\0',257);let sum=0;for(const b of h)sum+=b;h.write(sum.toString(8).padStart(6,'0')+'\0 ',148);
 return gzipSync(Buffer.concat([h,Buffer.from(value),Buffer.alloc((512-value.length%512)%512),Buffer.alloc(1024)]));
}
test('verified extraction works in Chinese and space paths and detects subsequent corruption',async()=>{
 const p=await mkdtemp(join(tmpdir(),'Craft 中文 '));try{await extractRuntime(archive('adapter.mjs','ok'),p);assert.equal(await readFile(join(p,'adapter.mjs'),'utf8'),'ok');const files={'adapter.mjs':createHash('sha256').update('ok').digest('hex')};assert.equal(await verifyRuntime(p,files),true);assert.equal(await verifyRuntime(p,{'adapter.mjs':'0'.repeat(64)}),false);}finally{await rm(p,{recursive:true,force:true});}
});
for(const path of ['../outside','/outside','C:/outside','a/../../outside','a\\outside'])test('reject tar path '+path,async()=>{const p=await mkdtemp(join(tmpdir(),'craft-'));try{await assert.rejects(extractRuntime(archive(path,'bad'),p));}finally{await rm(p,{recursive:true,force:true});}});
test('reject archive symlinks',async()=>{const p=await mkdtemp(join(tmpdir(),'craft-'));try{await assert.rejects(extractRuntime(archive('link','bad','2'),p));}finally{await rm(p,{recursive:true,force:true});}});
import {spawn} from 'node:child_process';
import {copyFile,writeFile,mkdir} from 'node:fs/promises';
test('MCP handshake and discovery finish without downloading the editor',async()=>{
 const p=await mkdtemp(join(tmpdir(),'craft-lazy-'));let child;
 try{
  await copyFile(new URL('./templates/craft-runtime-bootstrap.mjs',import.meta.url),join(p,'bootstrap.mjs'));
  await writeFile(join(p,'runtime.lock.json'),JSON.stringify({name:'testcraft',version:'0.1.0-dev.1',url:'file:///must-not-download',sha256:'0'.repeat(64),files:{}}));
  await writeFile(join(p,'catalog.lock.json'),JSON.stringify({tools:[{name:'open_editor',inputSchema:{type:'object'}}],resources:[],resourceTemplates:[]}));
  child=spawn(process.execPath,[join(p,'bootstrap.mjs')],{stdio:['pipe','pipe','pipe']});let output='',errors='';child.stdout.on('data',b=>output+=b);child.stderr.on('data',b=>errors+=b);
  child.stdin.write(JSON.stringify({jsonrpc:'2.0',id:1,method:'initialize',params:{protocolVersion:'2025-03-26',capabilities:{},clientInfo:{name:'test',version:'1'}}})+'\n');
  child.stdin.write(JSON.stringify({jsonrpc:'2.0',id:2,method:'tools/list',params:{}})+'\n');
  for(let i=0;i<30&&output.trim().split('\n').length<2;i++)await new Promise(r=>setTimeout(r,100));const rows=output.trim().split('\n').filter(Boolean).map(s=>JSON.parse(s));assert.ok(rows.some(r=>r.id===1&&r.result?.serverInfo),'initialize response missing: '+errors);assert.ok(rows.some(r=>r.id===2&&r.result?.tools[0].name==='open_editor'));assert.doesNotMatch(errors,/Downloading/);
 }finally{child?.kill();await rm(p,{recursive:true,force:true});}
});
test('first concurrent tool calls share one engine and preserve response IDs',async()=>{
 const p=await mkdtemp(join(tmpdir(),'craft-proxy-'));let child;
 try{
  await mkdir(join(p,'dist'));await copyFile(new URL('./templates/craft-runtime-bootstrap.mjs',import.meta.url),join(p,'bootstrap.mjs'));
  const source=`import {createInterface} from 'node:readline';console.error('engine-start');createInterface({input:process.stdin}).on('line',line=>{const r=JSON.parse(line);if(r.id===undefined)return;const result=r.method==='initialize'?{protocolVersion:'2025-03-26',capabilities:{tools:{}},serverInfo:{name:'fixture',version:'1'}}:{content:[{type:'text',text:'forwarded'}]};console.log(JSON.stringify({jsonrpc:'2.0',id:r.id,result}));});`;
  await writeFile(join(p,'dist/adapter.mjs'),source);await writeFile(join(p,'runtime.lock.json'),JSON.stringify({name:'fixture',version:'0.1.0-dev.1',files:{'adapter.mjs':createHash('sha256').update(source).digest('hex')}}));await writeFile(join(p,'catalog.lock.json'),JSON.stringify({tools:[{name:'echo',inputSchema:{type:'object'}}]}));
  child=spawn(process.execPath,[join(p,'bootstrap.mjs')],{stdio:['pipe','pipe','pipe']});let output='',errors='';child.stdout.on('data',b=>output+=b);child.stderr.on('data',b=>errors+=b);
  for(const request of [{id:1,method:'initialize',params:{protocolVersion:'2025-03-26',capabilities:{},clientInfo:{name:'fixture',version:'1'}}},{id:30,method:'tools/call',params:{name:'echo',arguments:{}}},{id:31,method:'tools/call',params:{name:'echo',arguments:{}}}])child.stdin.write(JSON.stringify({jsonrpc:'2.0',...request})+'\n');
  for(let i=0;i<50&&output.trim().split('\n').length<3;i++)await new Promise(r=>setTimeout(r,100));const rows=output.trim().split('\n').map(s=>JSON.parse(s));for(const id of [30,31])assert.ok(rows.some(r=>r.id===id&&r.result?.content[0].text==='forwarded'),errors);assert.equal(errors.split('engine-start').length-1,1);
 }finally{child?.kill();await rm(p,{recursive:true,force:true});}
});
