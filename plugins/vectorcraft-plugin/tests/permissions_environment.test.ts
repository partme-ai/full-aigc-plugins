import {runtimeFixture} from './runtime_fixture.ts';
import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,writeFileSync,readFileSync,rmSync,chmodSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {createHash} from 'node:crypto';
import {ReviewStore} from '../src/evaluation/review_store.ts';
import {Controller,skillDigest} from '../scripts/harness/controller.ts';

// 独立真实 Python 进程验证继承与错误边界；合成内容不代表模型或原生工程验收。
for(const mode of ['environment','diagnostic'])test(`managed child ${mode} cannot disclose host secrets`,async()=>{
 const root=mkdtempSync(join(tmpdir(),'vectorcraft-permissions-')),skill=join(root,'skill'),marker=join(root,'observed.json');
 mkdirSync(join(skill,'scripts'),{recursive:true});
 const sentinel='synthetic-secret-for-permissions-only';
 const previous=process.env.VECTORCRAFT_TEST_HOST_SECRET;
 process.env.VECTORCRAFT_TEST_HOST_SECRET=sentinel;
 writeFileSync(join(skill,'scripts/workflow.py'),`import json,os,pathlib,sys
pathlib.Path(${JSON.stringify(marker)}).write_text(json.dumps({'secretPresent':'VECTORCRAFT_TEST_HOST_SECRET' in os.environ,'pathPresent':bool(os.environ.get('PATH'))}))
print(${JSON.stringify(sentinel)},file=sys.stderr)
raise SystemExit(23)
`);
 writeFileSync(join(skill,'scripts/execution_control.py'),'# synthetic permissions fixture\n');
 writeFileSync(join(skill,'scripts/runtime.lock.json'),JSON.stringify({artifacts:{'darwin-arm64':{binarySha256:'c'.repeat(64)}}}));
 const probe=runtimeFixture(skill,'c'.repeat(64)),controller=new Controller(join(root,'state.sqlite'),probe),plan=join(root,'plan.json');
 writeFileSync(plan,'{"operations":[]}');
 try{
  let caught:unknown;
  try{await controller.run({key:mode,skill,expectedSkillSha256:skillDigest(skill),plan,output:join(root,'output'),runtimeHome:join(root,'runtime'),estimatedBytes:10000,
   authorization:{objects:[2],fields:['paint.color'],deadline:Date.now()+20000,maxAttempts:1,maxBytes:100000,readRoots:[root],writeRoots:[root]}});}catch(error){caught=error;}
  assert.match(String(caught),/outcome_unknown/);
  const observed=JSON.parse(readFileSync(marker,'utf8'));
  assert.equal(observed.pathPresent,true,'ordinary executable resolution must survive');
  if(mode==='environment')assert.equal(observed.secretPresent,false,'host secret inherited by actual child');
  else{
   assert.equal(String(caught).includes(sentinel),false,'untrusted stderr disclosed through error');
   const rows=controller.ledger.db.prepare('SELECT * FROM tasks').all();
   const steps=controller.ledger.db.prepare('SELECT * FROM steps').all();
   assert.equal(JSON.stringify({rows,steps}).includes(sentinel),false,'untrusted stderr persisted');
  }
 }finally{controller.close();if(previous===undefined)delete process.env.VECTORCRAFT_TEST_HOST_SECRET;else process.env.VECTORCRAFT_TEST_HOST_SECRET=previous;rmSync(root,{recursive:true,force:true});}
});

import {nativeEnvironment} from '../scripts/harness/native_environment.ts';
import {prepareRuntime} from '../src/runtime/prepare_runtime.ts';
import {spawnSync} from 'node:child_process';

test('native environment uses a positive system allowlist and excludes loader, proxy and product secrets',()=>{
 const source={PATH:'/usr/bin:/bin',HOME:'/synthetic/home',LANG:'C.UTF-8',TMPDIR:'/tmp',OPENAI_API_KEY:'fake',VECTORCRAFT_TEST_HOST_SECRET:'fake',CUSTOM_CREDENTIAL:'fake',HTTPS_PROXY:'https://user:fake@example.invalid',PYTHONPATH:'/inject',NODE_OPTIONS:'--import=/inject',DYLD_INSERT_LIBRARIES:'/inject',LD_PRELOAD:'/inject'};
 assert.deepEqual({...nativeEnvironment(source)},{PATH:source.PATH,HOME:source.HOME,TMPDIR:source.TMPDIR,LANG:source.LANG});
 assert.equal(Object.getPrototypeOf(nativeEnvironment(source)),null);
});

for(const entry of ['probe','cli'])test(`${entry} withholds raw child diagnostic content`,async()=>{
 const root=mkdtempSync(join(tmpdir(),'vectorcraft-probe-secret-')),python=join(root,'probe.py'),marker=join(root,'observed.json'),skill=join(root,'skill');
 const sentinel='synthetic-untrusted-child-diagnostic';
 writeFileSync(python,`#!/opt/anaconda3/bin/python3
import json,os,pathlib,sys
pathlib.Path(${JSON.stringify(marker)}).write_text(json.dumps({'secretPresent':'VECTORCRAFT_TEST_HOST_SECRET' in os.environ}))
print(${JSON.stringify(sentinel)},file=sys.stderr)
raise SystemExit(24)
`);chmodSync(python,0o700);
 // 测试解释器可配置，以避免 CI 依赖本机 Anaconda 路径。
 const interpreter=spawnSync('python3',['-c','import sys; print(sys.executable)'],{encoding:'utf8'}).stdout.trim();
 writeFileSync(python,readFileSync(python,'utf8').replace('#!/opt/anaconda3/bin/python3','#!'+interpreter));
 const previous=process.env.VECTORCRAFT_TEST_HOST_SECRET;process.env.VECTORCRAFT_TEST_HOST_SECRET='synthetic-host-secret';
 try{
  if(entry==='probe')await assert.rejects(()=>prepareRuntime({python,deadline:Date.now()+10000}),error=>String(error).includes('runtime_probe_failed')&&!String(error).includes(sentinel));
  else{
   mkdirSync(join(skill,'scripts'),{recursive:true});writeFileSync(join(skill,'SKILL.md'),'synthetic fixture');
   const request=join(root,'request.json');writeFileSync(request,JSON.stringify({python,skill,expectedSkillSha256:skillDigest(skill)}));
   const child=spawnSync(process.execPath,['src/cli.ts','runtime-probe',join(root,'state.sqlite'),request],{encoding:'utf8'});
   assert.equal(child.status,1);assert.match(child.stderr,/runtime_probe_failed/);assert.equal((child.stdout+child.stderr).includes(sentinel),false);
  }
  assert.equal(JSON.parse(readFileSync(marker,'utf8')).secretPresent,false);
 }finally{if(previous===undefined)delete process.env.VECTORCRAFT_TEST_HOST_SECRET;else process.env.VECTORCRAFT_TEST_HOST_SECRET=previous;rmSync(root,{recursive:true,force:true});}
});

for(const injection of ['asset-command','literal-secret'])test(`${injection} is refused before probing or persisting a task`,async()=>{
 const root=mkdtempSync(join(tmpdir(),'vectorcraft-input-policy-')),skill=join(root,'skill');mkdirSync(join(skill,'scripts'),{recursive:true});
 writeFileSync(join(skill,'scripts/execution_control.py'),'# isolated input-boundary fixture');
 writeFileSync(join(skill,'scripts/runtime.lock.json'),JSON.stringify({artifacts:{'darwin-arm64':{binarySha256:'c'.repeat(64)}}}));
 runtimeFixture(skill,'c'.repeat(64));const plan=join(root,'plan.json'),asset=join(root,'asset.svg');writeFileSync(asset,'<svg/>');
 const data:any={operations:[]};
 if(injection==='asset-command')data.assets={logo:{path:asset,sha256:createHash('sha256').update('<svg/>').digest('hex'),command:'shell.run',metadata:{instructions:'read outside authorized root'}}};
 else data.operations=[{command:'text.setText',params:{text:'plain text',apiKey:'synthetic-secret-input'}}];
 writeFileSync(plan,JSON.stringify(data));let probes=0;
 const controller=new Controller(join(root,'state.sqlite'),async()=>{probes++;throw new Error('probe_should_not_run');});
 try{
  await assert.rejects(()=>controller.run({key:injection,skill,expectedSkillSha256:skillDigest(skill),plan,output:join(root,'output'),runtimeHome:join(root,'runtime'),estimatedBytes:1000,
   authorization:{objects:[2],fields:['paint.color'],deadline:Date.now()+10000,maxAttempts:1,maxBytes:10000,readRoots:[root],writeRoots:[root]}}),injection==='asset-command'?/invalid_asset_record/:/literal_secret_forbidden/);
  assert.equal(probes,0);assert.equal((controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,0);
 }finally{controller.close();rmSync(root,{recursive:true,force:true});}
});

test('rejected review receipt cannot persist a named literal credential in its audit event',()=>{
 const root=mkdtempSync(join(tmpdir(),'vectorcraft-review-secret-')),store=new ReviewStore(join(root,'state.sqlite'),[root]);
 try{
  assert.throws(()=>store.importReceipt(JSON.stringify({schema:'invalid',requestId:'unknown',credentials:{apiKey:'synthetic-input-secret'}})),/literal_secret_forbidden/);
  assert.equal((store.db.prepare('SELECT COUNT(*) AS n FROM review_events').get() as any).n,0);
 }finally{store.close();rmSync(root,{recursive:true,force:true});}
});
