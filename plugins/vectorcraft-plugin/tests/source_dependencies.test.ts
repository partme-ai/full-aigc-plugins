import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,writeFileSync,readFileSync,rmSync,symlinkSync,existsSync} from 'node:fs';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {createHash} from 'node:crypto';
import {Controller,skillDigest} from '../scripts/harness/controller.ts';
import {runtimeFixture} from './runtime_fixture.ts';
const sha=(value:string|Buffer)=>createHash('sha256').update(value).digest('hex');
// 合成协调器工作流，仅证明源输入版本绑定；原生验收独立执行。
function fixture(){
 const root=mkdtempSync(join(tmpdir(),'vector-source-inputs-')),skill=join(root,'skill'),source=join(root,'source');
 mkdirSync(join(skill,'scripts'),{recursive:true});mkdirSync(source);
 writeFileSync(join(skill,'scripts/runtime.lock.json'),JSON.stringify({artifacts:{'darwin-arm64':{binarySha256:'c'.repeat(64)}}}));
 writeFileSync(join(skill,'scripts/execution_control.py'),'# coordinator fixture\n');
 writeFileSync(join(skill,'scripts/workflow.py'),`import argparse,pathlib,json,hashlib\np=argparse.ArgumentParser();p.add_argument('plan');p.add_argument('--source');p.add_argument('--output');p.add_argument('--runtime-home');p.add_argument('--control');a=p.parse_args();o=pathlib.Path(a.output);o.mkdir();(o/'project.vectorcraft').write_bytes(b'fixture');(o/'manifest.json').write_text(json.dumps({'schema':'vectorcraft-delivery/v1','runtimeSha256':'${'c'.repeat(64)}','files':{'project.vectorcraft':hashlib.sha256(b'fixture').hexdigest()}}))\n`);
 const probe=runtimeFixture(skill,'c'.repeat(64));
 const files={'project.vectorcraft':sha('native'),'plan.json':sha('{"operations":[]}'),'asset.bin':sha('asset')};
 writeFileSync(join(source,'project.vectorcraft'),'native');writeFileSync(join(source,'plan.json'),'{"operations":[]}');writeFileSync(join(source,'asset.bin'),'asset');
 const manifest={schema:'vectorcraft-delivery/v1',bindings:{object:{id:3}},files};writeFileSync(join(source,'manifest.json'),JSON.stringify(manifest));
 const plan=join(root,'plan.json');writeFileSync(plan,JSON.stringify({expectedProjectSha256:files['project.vectorcraft'],operations:[]}));
 const request={key:'source',skill,expectedSkillSha256:skillDigest(skill),plan,source,output:join(root,'output'),runtimeHome:join(root,'runtime'),estimatedBytes:10000,authorization:{objects:[3],fields:['paint.color'],deadline:Date.now()+60000,maxAttempts:1,maxBytes:20000,readRoots:[root],writeRoots:[root]}};
 return {root,source,manifest,probe,request,close(){rmSync(root,{recursive:true,force:true});}};
}
for(const [name,file,content] of [['manifest','manifest.json','{"bindings":{}}'],['inherited plan','plan.json','{"exports":[]}'],['declared asset','asset.bin','changed'],['previously absent PDF date','pdf-export-date.json','{}']]){
 test('source '+name+' cannot change while runtime is probing',async()=>{
  const f=fixture(),controller=new Controller(join(f.root,'state.sqlite'),async()=>{writeFileSync(join(f.source,file),content);return f.probe();});
  try{await assert.rejects(()=>controller.run(f.request),/stale_source_dependencies/);assert.equal((controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,0);assert.equal(existsSync(f.request.output),false);}finally{controller.close();f.close();}
 });
}
test('source manifest and declared dependency digests enter immutable task identity',async()=>{
 const f=fixture(),controller=new Controller(join(f.root,'state.sqlite'),f.probe);
 try{const task=await controller.run(f.request);assert.equal(task.binding.inputHashes['source:manifest.json'],sha(readFileSync(join(f.source,'manifest.json'))));assert.equal(task.binding.inputHashes['source:file:plan.json'],f.manifest.files['plan.json']);assert.equal(task.binding.inputHashes['source:file:asset.bin'],f.manifest.files['asset.bin']);assert.equal(task.state,'review_ready');}finally{controller.close();f.close();}
});
test('source manifest cannot introduce path traversal or linked inputs before probing',async()=>{
 for(const name of ['../escape','linked.bin']){
  const f=fixture();let probes=0;const controller=new Controller(join(f.root,'state.sqlite'),async()=>{probes++;return f.probe();});
  try{if(name==='linked.bin')symlinkSync(join(f.source,'asset.bin'),join(f.source,name));(f.manifest.files as any)[name]=sha('asset');writeFileSync(join(f.source,'manifest.json'),JSON.stringify(f.manifest));await assert.rejects(()=>controller.run(f.request),/invalid_source_dependency/);assert.equal(probes,0);}finally{controller.close();f.close();}
 }
});
test('ordinary dependency filenames cannot bypass guards through object prototype setters',async()=>{
 const f=fixture();writeFileSync(join(f.source,'__proto__'),'asset');Object.defineProperty(f.manifest.files,'__proto__',{value:sha('asset'),enumerable:true});writeFileSync(join(f.source,'manifest.json'),JSON.stringify(f.manifest));
 const controller=new Controller(join(f.root,'state.sqlite'),async()=>{writeFileSync(join(f.source,'__proto__'),'changed');return f.probe();});
 try{await assert.rejects(()=>controller.run(f.request),/stale_source_dependencies/);assert.equal(existsSync(f.request.output),false);}finally{controller.close();f.close();}
});
test('a declared dependency cannot escape its source bundle through a parent directory link',async()=>{
 const f=fixture(),outside=join(f.root,'outside');mkdirSync(outside);writeFileSync(join(outside,'asset.bin'),'asset');symlinkSync(outside,join(f.source,'parent-link'));
 (f.manifest.files as any)['parent-link/asset.bin']=sha('asset');writeFileSync(join(f.source,'manifest.json'),JSON.stringify(f.manifest));let probes=0;
 const controller=new Controller(join(f.root,'state.sqlite'),async()=>{probes++;return f.probe();});
 try{await assert.rejects(()=>controller.run(f.request),/invalid_source_dependency/);assert.equal(probes,0);}finally{controller.close();f.close();}
});
test('execution uses a hash-verified readonly source snapshot while resource identity stays on the user source',async()=>{
 const f=fixture(),controller=new Controller(join(f.root,'state.sqlite'),f.probe);
 try{
  const task=await controller.run(f.request),intent=JSON.parse((controller.ledger.db.prepare('SELECT intent FROM steps WHERE task=?').get(task.id) as any).intent);
  assert.ok(intent.sourceSnapshot);assert.notEqual(intent.sourceSnapshot,f.source);assert.equal(skillDigest(intent.sourceSnapshot),intent.sourceSnapshotSha256);
  assert.equal(sha(readFileSync(join(intent.sourceSnapshot,'manifest.json'))),task.binding.inputHashes['source:manifest.json']);
  assert.equal(readFileSync(join(intent.sourceSnapshot,'asset.bin'),'utf8'),'asset');
  assert.match(task.resource,/source\/project\.vectorcraft$/);
 }finally{controller.close();f.close();}
});
