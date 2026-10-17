import {runtimeFixture} from './runtime_fixture.ts';
import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, writeFileSync, mkdirSync, rmSync, readFileSync,existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
import { Controller, skillDigest } from '../scripts/harness/controller.ts';

test('controller binds a supplied standalone snapshot, records intent and verifies actual files', async()=>{
  const root=mkdtempSync(join(tmpdir(),'vectorcraft-controller-'));
  // 这是流程协调单元 fixture，不充当 Vector 原生验收。
  const skill=join(root,'skill');mkdirSync(join(skill,'scripts'),{recursive:true});
  writeFileSync(join(skill,'scripts','workflow.py'),`import argparse,hashlib,json,pathlib\np=argparse.ArgumentParser();p.add_argument('plan');p.add_argument('--output');p.add_argument('--runtime-home');p.add_argument('--source');p.add_argument('--control');a=p.parse_args();o=pathlib.Path(a.output);o.mkdir();(o/'project.vectorcraft').write_bytes(b'fixture');h=hashlib.sha256(b'fixture').hexdigest();m={'schema':'vectorcraft-delivery/v1','runtimeSha256':'${'c'.repeat(64)}','files':{'project.vectorcraft':h},'outputs':[],'fontDependencies':[]};(o/'manifest.json').write_text(json.dumps(m));print(json.dumps(m))\n`);
  writeFileSync(join(skill,'scripts','execution_control.py'),'# synthetic coordinator fixture; no native acceptance\n');
  writeFileSync(join(skill,'scripts','runtime.lock.json'),JSON.stringify({artifacts:{'darwin-arm64':{binarySha256:'c'.repeat(64)}}}));
  runtimeFixture(skill,'c'.repeat(64));
  const plan=join(root,'plan.json');writeFileSync(plan,'{"operations":[]}');
  const authorization={objects:[2],fields:['paint.color'],deadline:Date.now()+60000,maxAttempts:1,maxBytes:100000,readRoots:[root],writeRoots:[root]};
  const controller=new Controller(join(root,'state.sqlite'),runtimeFixture(skill,'c'.repeat(64)));
  try {
    const request={key:'one',skill,expectedSkillSha256:skillDigest(skill),plan,output:join(root,'output'),
      runtimeHome:join(root,'runtime'),python:'python3',authorization,estimatedBytes:10000};
    const brief=join(root,'brief.txt');writeFileSync(brief,'goal');
    const guarded={...request,inputFingerprints:{[brief]:createHash('sha256').update('old goal').digest('hex')}};
    await assert.rejects(()=>controller.run(guarded),/stale_execution_inputs/);
    assert.equal((controller.ledger.db.prepare('SELECT COUNT(*) AS n FROM tasks').get() as any).n,0);
    const value=await controller.run(request);
    assert.equal(value.state,'review_ready');
    assert.equal(controller.ledger.get(value.id).attempts,1);
    assert.equal((await controller.run(request)).id,value.id);
    const submitted=controller.ledger.db.prepare('SELECT intent FROM steps WHERE task=?').get(value.id) as any;
    const intent=JSON.parse(submitted.intent);
    assert.deepEqual(intent.plan,{operations:[]});
    assert.notEqual(intent.skillSnapshot,skill);
    assert.equal(skillDigest(intent.skillSnapshot),request.expectedSkillSha256);
    assert.equal(readFileSync(intent.planSnapshot,'utf8'),'{"operations":[]}');
    const originalManifest=readFileSync(join(request.output,'manifest.json'),'utf8');
    const rewritten=JSON.parse(originalManifest);rewritten.audit='rewritten';
    writeFileSync(join(request.output,'manifest.json'),JSON.stringify(rewritten));
    await assert.rejects(()=>controller.run(request),/receipt_manifest_mismatch/);
    writeFileSync(join(request.output,'manifest.json'),originalManifest);
    assert.throws(()=>controller.verifyDelivery(request.output,'d'.repeat(64)),/runtime_identity_mismatch/);
    writeFileSync(join(request.output,'project.vectorcraft'),'tampered');
    assert.throws(()=>controller.verifyDelivery(request.output,'c'.repeat(64)),/artifact_digest_mismatch/);
    await assert.rejects(()=>controller.run(request),/artifact_digest_mismatch/);
    const changed={...request,key:'two',output:join(root,'other'),expectedSkillSha256:'0'.repeat(64)};
    await assert.rejects(()=>controller.run(changed),/skill_snapshot_mismatch/);
    await assert.rejects(()=>controller.run({...request,key:'three',output:join(tmpdir(),'escape')}),/outside_authorized_roots/);
    const workflow=join(skill,'scripts','workflow.py');writeFileSync(workflow,readFileSync(workflow,'utf8')+'# changed source identity\n');
    await assert.rejects(()=>controller.run({...request,expectedSkillSha256:skillDigest(skill)}),/idempotency_conflict/);
  } finally {controller.close();rmSync(root,{recursive:true,force:true});}
});

test('changing a bound brief during execution stops the owned group and retains the unresolved task',async()=>{
  const root=mkdtempSync(join(tmpdir(),'vectorcraft-live-guard-')),skill=join(root,'skill'),marker=join(root,'started'),brief=join(root,'brief.txt');
  mkdirSync(join(skill,'scripts'),{recursive:true});writeFileSync(brief,'goal');
  writeFileSync(join(skill,'scripts','workflow.py'),`import pathlib,time\npathlib.Path(${JSON.stringify(marker)}).write_text('started')\ntime.sleep(10)\n`);
  writeFileSync(join(skill,'scripts','execution_control.py'),'# synthetic unit fixture\n');
  writeFileSync(join(skill,'scripts','runtime.lock.json'),JSON.stringify({artifacts:{'darwin-arm64':{binarySha256:'c'.repeat(64)}}}));
  runtimeFixture(skill,'c'.repeat(64));
  const plan=join(root,'plan.json');writeFileSync(plan,'{"operations":[]}');const controller=new Controller(join(root,'state.sqlite'),runtimeFixture(skill,'c'.repeat(64)));
  try{
    let settled=false;
    const result=controller.run({key:'guarded',skill,expectedSkillSha256:skillDigest(skill),plan,output:join(root,'output'),runtimeHome:join(root,'runtime'),estimatedBytes:1000,
      inputFingerprints:{[brief]:createHash('sha256').update('goal').digest('hex')},authorization:{objects:[2],fields:['paint.color'],deadline:Date.now()+10000,maxAttempts:1,maxBytes:10000,readRoots:[root],writeRoots:[root]}})
      .then(value=>{settled=true;return {value,error:null};},error=>{settled=true;return {value:null,error};});
    const deadline=Date.now()+5000;while(!existsSync(marker)&&!settled&&Date.now()<deadline)await new Promise(r=>setTimeout(r,10));
    assert.ok(existsSync(marker),'fixture process must actually start');writeFileSync(brief,'changed goal');
    const outcome=await result;assert.match(String(outcome.error),/outcome_unknown/);assert.equal(existsSync(join(root,'output')),false);
    const row=controller.ledger.db.prepare('SELECT id,state,attempts FROM tasks WHERE key=?').get('guarded') as any;
    assert.ok(['cancel_requested','reconciling'].includes(row.state));assert.equal(row.attempts,1);assert.equal(controller.processes.observe(row.id,1).stopped,true);
  }finally{controller.close();rmSync(root,{recursive:true,force:true});}
});
