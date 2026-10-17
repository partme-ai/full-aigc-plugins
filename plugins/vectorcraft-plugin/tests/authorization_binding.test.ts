import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,writeFileSync,readFileSync,rmSync,realpathSync,renameSync,symlinkSync,unlinkSync,existsSync} from 'node:fs';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
import {createHash} from 'node:crypto';
import {Controller,skillDigest} from '../scripts/harness/controller.ts';
import {runtimeFixture} from './runtime_fixture.ts';
// 仅证明协调器授权边界；原生工程单写、GUI冲突与进程交接由真实验收覆盖。
function fixture(){
 const root=mkdtempSync(join(tmpdir(),'vector-auth-binding-')),skill=join(root,'skill');mkdirSync(join(skill,'scripts'),{recursive:true});
 writeFileSync(join(skill,'scripts/runtime.lock.json'),JSON.stringify({artifacts:{'darwin-arm64':{binarySha256:'c'.repeat(64)}}}));
 writeFileSync(join(skill,'scripts/execution_control.py'),'# coordinator unit fixture\n');
 writeFileSync(join(skill,'scripts/workflow.py'),`import argparse,pathlib,json,hashlib\np=argparse.ArgumentParser();p.add_argument('plan');p.add_argument('--output');p.add_argument('--runtime-home');p.add_argument('--control');a=p.parse_args();o=pathlib.Path(a.output);o.mkdir();(o/'project.vectorcraft').write_bytes(b'fixture');(o/'manifest.json').write_text(json.dumps({'schema':'vectorcraft-delivery/v1','runtimeSha256':'${'c'.repeat(64)}','files':{'project.vectorcraft':hashlib.sha256(b'fixture').hexdigest()}}))\n`);
 const probe=runtimeFixture(skill,'c'.repeat(64)),plan=join(root,'plan.json');writeFileSync(plan,'{"operations":[]}');
 const request={key:'authorization',skill,expectedSkillSha256:skillDigest(skill),plan,output:join(root,'output'),runtimeHome:join(root,'runtime'),estimatedBytes:10000,authorization:{objects:[3],fields:['paint.color'],deadline:Date.now()+60000,maxAttempts:1,maxBytes:20000,readRoots:[root],writeRoots:[root]}};
 return {root,probe,request,close(){rmSync(root,{recursive:true,force:true});}};
}
test('final output permission alone does not authorize sibling staging; refusal precedes probe',async()=>{
 const f=fixture();let probes=0;const controller=new Controller(join(f.root,'state.sqlite'),async()=>{probes++;return f.probe();});
 try{
  const request={...f.request,authorization:{...f.request.authorization,writeRoots:[f.request.output,f.request.runtimeHome]}};
  await assert.rejects(()=>controller.run(request),/staging_parent_not_authorized/);assert.equal(probes,0);assert.equal(existsSync(request.output),false);assert.equal((controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,0);
 }finally{controller.close();f.close();}
});
test('authorized physical roots and request paths stay fixed when a root alias changes during probe',async()=>{
 const f=fixture(),original=join(f.root,'authorized'),outside=join(f.root,'outside'),alias=join(f.root,'alias');mkdirSync(original);mkdirSync(outside);symlinkSync(original,alias);writeFileSync(join(original,'plan.json'),'{"operations":[]}');
 const controller=new Controller(join(f.root,'state.sqlite'),async()=>{unlinkSync(alias);symlinkSync(outside,alias);return f.probe();});
 try{
  const request={...f.request,plan:join(alias,'plan.json'),output:join(alias,'output'),runtimeHome:join(alias,'runtime'),authorization:{...f.request.authorization,readRoots:[alias],writeRoots:[alias]}};
  const task=await controller.run(request);assert.equal(task.state,'review_ready');assert.deepEqual(task.binding.authorization.writeRoots,[realpathSync(original)]);assert.equal(task.output,join(realpathSync(original),'output'));assert.equal(existsSync(join(original,'output')),true);assert.equal(existsSync(join(outside,'output')),false);
 }finally{controller.close();f.close();}
});
test('caller mutation cannot replace the input fingerprint or broaden authorization after probe starts',async()=>{
 const f=fixture(),brief=join(f.root,'brief.txt');writeFileSync(brief,'original');const sha=(p:string)=>createHash('sha256').update(readFileSync(p)).digest('hex');
 const request={...f.request,inputFingerprints:{[brief]:sha(brief)}};
 const controller=new Controller(join(f.root,'state.sqlite'),async()=>{writeFileSync(brief,'changed');request.inputFingerprints[brief]=sha(brief);request.authorization.fields.push('structure');request.authorization.objects.push(999);return f.probe();});
 try{await assert.rejects(()=>controller.run(request),/stale_execution_inputs/);assert.equal(existsSync(request.output),false);assert.equal((controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,0);}finally{controller.close();f.close();}
});
for(const replacement of ['root','output-parent']){
 test('replacing captured physical '+replacement+' with a new alias cannot redirect execution',async()=>{
  const f=fixture(),authorized=join(f.root,'authorized'),outside=join(f.root,'outside'),parent=join(authorized,'parent');mkdirSync(authorized);mkdirSync(outside);mkdirSync(join(outside,'parent'));mkdirSync(parent);writeFileSync(join(authorized,'plan.json'),'{"operations":[]}');
  const controller=new Controller(join(f.root,'state.sqlite'),async()=>{const path=replacement==='root'?authorized:parent;renameSync(path,path+'-saved');symlinkSync(outside,path);return f.probe();});
  try{await assert.rejects(()=>controller.run({...f.request,plan:join(authorized,'plan.json'),output:join(parent,'output'),runtimeHome:join(authorized,'runtime'),authorization:{...f.request.authorization,readRoots:[authorized],writeRoots:[authorized]}}),/authorization_path_changed/);assert.equal(existsSync(join(outside,'output')),false);assert.equal((controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,0);}finally{controller.close();f.close();}
 });
}
