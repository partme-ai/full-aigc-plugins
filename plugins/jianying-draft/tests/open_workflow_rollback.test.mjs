import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';

import {boundedSkillDigest} from '../scripts/workflow_data.mjs';
import {WorkflowRuntime} from '../scripts/workflow_runtime.mjs';
import {SideEffectLedger} from '../scripts/side_effect_ledger.mjs';

const ROOT=path.resolve(import.meta.dirname,'..');
const run=(pluginRoot,args,env={})=>{
  const processResult=spawnSync(process.execPath,[fs.realpathSync(path.join(pluginRoot,'scripts/harness.mjs')),...args],{
    encoding:'utf8',timeout:15000,env:{PATH:'/nonexistent',JIANYING_CLI_PATH:'/nonexistent',...env}});
  assert.equal(processResult.error,undefined);
  assert.ok(processResult.stdout,JSON.stringify({status:processResult.status,signal:processResult.signal,
    stderr:processResult.stderr}));
  return {status:processResult.status,result:JSON.parse(processResult.stdout)};
};

test('old Skills lock rollback keeps v1 planning and occupied workflow and side-effect ledgers',t=>{
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'jianying-open-rollback-'));
  t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  const pluginRoot=path.join(root,'plugin');
  for(const directory of ['scripts','runtime','schemas'])
    fs.cpSync(path.join(ROOT,directory),path.join(pluginRoot,directory),{recursive:true});
  const skillRoot=path.join(pluginRoot,'skills/jianying-draft-video-planning');
  fs.mkdirSync(path.dirname(skillRoot),{recursive:true});
  fs.cpSync(path.join(ROOT,'skills/jianying-draft-video-planning'),skillRoot,{recursive:true});

  const stateRoot=path.join(root,'persistent-state');
  const intentFile=path.join(root,'intent.json');
  const briefFile=path.join(root,'brief.json');
  fs.writeFileSync(intentFile,JSON.stringify({schema:'jianying-video-intent/v1',scene_id:'VG01'}));
  fs.writeFileSync(briefFile,JSON.stringify({schema:'jianying-creative-brief/v1',request_id:'rollback',
    intent:'生活 Vlog',constraints:{},dimensions:{},output_intents:[],facts:[],metadata:{}}));

  const lock=JSON.parse(fs.readFileSync(path.join(ROOT,'skills.lock.json'),'utf8'));
  const before=run(ROOT,['plan-video',intentFile,'--state-root',stateRoot]);
  assert.equal(before.status,0);
  fs.writeFileSync(path.join(pluginRoot,'skills.lock.json'),JSON.stringify(lock));
  assert.equal(run(pluginRoot,['workflow-plan',briefFile,'--state-root',stateRoot]).status,0);

  const compilation={schema:'jianying-workflow-compilation/v1',can_compile:true,can_execute:false,
    plan_digest:'1'.repeat(64),blockers:[{code:'approval_required'}],
    job_bindings:[{output_id:'main',purpose:'personal',output_path:path.join(root,'output'),
      job_digest:'2'.repeat(64),job:{schema:'jianying-job/v2',operation:'create'}}],
    receipt:{schema:'jianying-compilation-receipt/v1',execution_digest:'3'.repeat(64),
      semantic_digest:'4'.repeat(64),cli:{version:'1.6.30',sha256:'5'.repeat(64),job_schema:'jianying-job/v2'}}};
  const runtime=new WorkflowRuntime({stateRoot,executor:()=>{
    const error=new Error('lost native response');error.outcome='unknown';throw error;
  }});
  const started=runtime.start({compilation,revision:1,budget:{currency:'CNY',maximum:0}});
  runtime.approve(started.run_id,{...runtime.approvalBinding(started.run_id),user_id:'test-reviewer',
    expires_at:'2999-01-01T00:00:00Z'});
  assert.throws(()=>runtime.execute(started.run_id),error=>error.code==='execution_outcome_unknown');
  const runFile=path.join(stateRoot,started.run_id,'state.json');
  const occupiedRun=fs.readFileSync(runFile);
  const ledger=new SideEffectLedger({stateRoot:path.join(stateRoot,'side-effects')});
  const scope={workflow_id:'VLOG-01',revision:1,target_digest:'a'.repeat(64)};
  const effect=ledger.begin({type:'native_export',scope}).state;
  ledger.claim(effect.id);
  ledger.ambiguous(effect.id,{reason:'lost_native_response'});
  const effectFile=ledger.file(effect.id),occupiedEffect=fs.readFileSync(effectFile);

  // An operator can stop new workflow work before restoring the previous Skills lock.
  const disabled={JIANYING_OPEN_WORKFLOW_DISABLED:'1'};
  for(const args of [['workflow-plan',briefFile],['workflow-check','missing.json'],
    ['workflow-compile','missing.json'],['workflow-start','missing.json'],
    ['workflow-approve',started.run_id],['workflow-execute',started.run_id],
    ['workflow-resume',started.run_id],['workflow-confirm-cancelled',started.run_id]]) {
    const stopped=run(pluginRoot,[...args,'--state-root',stateRoot],disabled);
    assert.equal(stopped.status,1);
    assert.equal(stopped.result.error.type,'open_workflow_disabled');
  }
  const legacyWhileDisabled=run(pluginRoot,['plan-video',intentFile,'--state-root',stateRoot],disabled);
  assert.equal(legacyWhileDisabled.status,0);
  assert.deepEqual(fs.readFileSync(runFile),occupiedRun);
  assert.deepEqual(fs.readFileSync(effectFile),occupiedEffect);

  // CI uses a v1-only package fixture; an optional immutable release export exercises the same black box locally.
  const releasedSkillRoot=process.env.JIANYING_ROLLBACK_OLD_SKILL_ROOT;
  if(releasedSkillRoot) {
    fs.rmSync(skillRoot,{recursive:true});
    fs.cpSync(releasedSkillRoot,skillRoot,{recursive:true});
  } else {
    fs.rmSync(path.join(skillRoot,'references/planning-catalog-v2.json'));
    fs.rmSync(path.join(skillRoot,'references/planning-catalog-v2.schema.json'));
  }
  const source=lock.sources.find(item=>item.package==='jianying-skills');
  source.ref='v2.1.0';
  source.sha='686e5e0b68e7b8cc31b853bc43b759d2c6e29ddc';
  source.sha256['jianying-draft-video-planning']=boundedSkillDigest(skillRoot);
  if(releasedSkillRoot) assert.equal(source.sha256['jianying-draft-video-planning'],
    '3b3285b45604d29e76d19f6db8df0dc722404a5d272bb67229908a13f633a6af');
  fs.writeFileSync(path.join(pluginRoot,'skills.lock.json'),JSON.stringify(lock));
  const rolledBackLock=fs.readFileSync(path.join(pluginRoot,'skills.lock.json'));

  const unavailable=run(pluginRoot,['workflow-plan',briefFile,'--state-root',stateRoot]);
  assert.equal(unavailable.status,1);
  assert.equal(unavailable.result.error.type,'catalog_v2_unavailable');
  const legacy=run(pluginRoot,['plan-video',intentFile,'--state-root',stateRoot]);
  assert.equal(legacy.status,0);
  assert.equal(legacy.result.data.scene_id,'VG01');
  const normalize=({provenance,...plan})=>plan;
  assert.deepEqual(normalize(legacy.result.data),normalize(before.result.data));
  const blocked=run(pluginRoot,['workflow-resume',started.run_id,'--state-root',stateRoot]);
  assert.equal(blocked.status,1);
  assert.equal(blocked.result.error.type,'manual_reconciliation_required');
  assert.deepEqual(fs.readFileSync(path.join(pluginRoot,'skills.lock.json')),rolledBackLock);
  assert.deepEqual(fs.readFileSync(runFile),occupiedRun);
  assert.deepEqual(fs.readFileSync(effectFile),occupiedEffect);
  assert.equal(fs.existsSync(path.join(stateRoot,started.run_id,'execution.lock')),true);
  assert.throws(()=>ledger.begin({type:'native_export',scope}),error=>error.code==='side_effect_reconciliation_required');
});
