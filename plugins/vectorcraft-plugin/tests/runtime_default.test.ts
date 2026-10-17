import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,writeFileSync,rmSync,existsSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {Controller,skillDigest} from '../scripts/harness/controller.ts';
import {runtimeFixture} from './runtime_fixture.ts';
function fixture(){
 const root=mkdtempSync(join(tmpdir(),'craft-runtime-default-')),skill=join(root,'skill');mkdirSync(join(skill,'scripts'),{recursive:true});
 const probe=runtimeFixture(skill,'c'.repeat(64));
 writeFileSync(join(skill,'scripts/runtime.lock.json'),JSON.stringify({artifacts:{'darwin-arm64':{binarySha256:'c'.repeat(64)}}}));
 writeFileSync(join(skill,'scripts/execution_control.py'),'# synthetic fixture\n');
 writeFileSync(join(skill,'scripts/workflow.py'),`import argparse,pathlib,json,hashlib\np=argparse.ArgumentParser();p.add_argument('plan');p.add_argument('--output');p.add_argument('--runtime-home');p.add_argument('--control');a=p.parse_args();o=pathlib.Path(a.output);o.mkdir();(o/'project.vectorcraft').write_bytes(b'fixture');(o/'manifest.json').write_text(json.dumps({'schema':'vectorcraft-delivery/v1','runtimeSha256':'${'c'.repeat(64)}','files':{'project.vectorcraft':hashlib.sha256(b'fixture').hexdigest()}}))\n`);
 const plan=join(root,'plan.json');writeFileSync(plan,'{"operations":[]}');
 const request={key:'new',skill,expectedSkillSha256:skillDigest(skill),plan,output:join(root,'output'),runtimeHome:join(root,'runtime'),estimatedBytes:10000,authorization:{objects:[],fields:[],deadline:Date.now()+60000,maxAttempts:2,maxBytes:20000,readRoots:[root],writeRoots:[root]}};
 return {root,probe,request,close:()=>rmSync(root,{recursive:true,force:true})};
}
test('default new task probes before claim and refuses missing capability without output or intent',async()=>{
 const f=fixture();let probes=0;
 const controller=new Controller(join(f.root,'state.sqlite'),async()=>{probes++;return {...await f.probe(),commands:[]};});
 try{await assert.rejects(()=>controller.run(f.request),/capability_missing/);assert.equal(probes,1);assert.equal(existsSync(f.request.output),false);assert.equal((controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,0);}finally{controller.close();f.close();}
});
test('default probe binds capabilities; completed same key is readonly and does not reprobe',async()=>{
 const f=fixture();let probes=0;const controller=new Controller(join(f.root,'state.sqlite'),async()=>{probes++;return await f.probe();});
 try{const first=await controller.run(f.request);assert.equal(probes,1);assert.equal(first.state,'review_ready');assert.ok(first.binding.inputHashes['runtime:capabilities']);assert.equal((await controller.run(f.request)).id,first.id);assert.equal(probes,1);}finally{controller.close();f.close();}
});

test('concurrent first use reuses the same selection while another task is running',async()=>{
 const f=fixture(),database=join(f.root,'state.sqlite');let probes=0;
 const probe=async()=>{probes++;return await f.probe();};
 const a=new Controller(database,probe),b=new Controller(database,probe);
 try{
  const [first,second]=await Promise.all([a.run(f.request),b.run({...f.request,key:'other',output:join(f.root,'other')})]);
  assert.equal(first.state,'review_ready');assert.equal(second.state,'review_ready');assert.equal(probes,2);
  assert.equal((a.ledger.db.prepare('SELECT COUNT(*) AS n FROM runtime_selection').get() as any).n,1);
 }finally{a.close();b.close();f.close();}
});

test('a selection switched during a pending default probe is never silently overwritten',async()=>{
 const f=fixture();let release:any;const pending=new Promise<void>(r=>release=r);
 const controller=new Controller(join(f.root,'state.sqlite'),async()=>{await pending;return await f.probe();});
 try{
  const result=controller.run(f.request);const {RuntimeGate}=await import('../src/runtime/runtime_gate.ts');
  const report=await f.probe();new RuntimeGate(controller.ledger).activate({...report,binarySha256:'d'.repeat(64)},{mode:'headless',commands:{},tools:{}},[3]);
  release();await assert.rejects(()=>result,/runtime_selection_mismatch/);
  assert.equal(existsSync(f.request.output),false);assert.equal((controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,0);
 }finally{release();controller.close();f.close();}
});
