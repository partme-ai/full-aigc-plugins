import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import {resolveQualityLoopGate} from '../scripts/quality_feature_gate.mjs';
import {SideEffectLedger} from '../scripts/side_effect_ledger.mjs';
import {attachQualityLoop,validateWorkflowPlan} from '../scripts/workflow_plan.mjs';

const ROOT=path.resolve(import.meta.dirname,'..');
const FIXTURE=JSON.parse(fs.readFileSync(path.join(ROOT,'tests/fixtures/quality-loop/contracts.json'),'utf8'));

function basePlan() {
  return {schema:'jianying-workflow-plan/v1',workflow_id:'VLOG-01',revision:1,
    catalog_ref:{schema:'jianying-planning-catalog/v2',digest:'c'.repeat(64)},tool_requirements:{capabilities:[]},
    brief:{},assets:[],route:{},outputs:[{output_id:'main',purpose:'personal',format:'video',delivery:'editable_draft',
      target:{logical_path:'outputs/main'}}],steps:[],limits:{maximum_revisions:3,maximum_budget:{currency:'CNY',amount:0}},
    risk_requirements:[],proof_requirements:[],metadata:{}};
}

test('quality loop is default-off and explicit opt-in binds the packaged config digest',()=>{
  assert.throws(()=>attachQualityLoop(basePlan(),{creativeTargets:[FIXTURE.creative_target],
    iterationPolicy:FIXTURE.iteration_policy}),error=>error.code==='quality_loop_disabled');
  const plan=attachQualityLoop(basePlan(),{creativeTargets:[FIXTURE.creative_target],
    iterationPolicy:FIXTURE.iteration_policy,qualityLoopOptIn:true});
  assert.equal(plan.metadata['partme.quality_loop_gate'].activation,'explicit_opt_in');
  assert.match(plan.metadata['partme.quality_loop_gate'].config_digest,/^[a-f0-9]{64}$/);
  const stale=structuredClone(plan);
  stale.metadata['partme.quality_loop_gate'].config_digest='0'.repeat(64);
  assert.throws(()=>validateWorkflowPlan(stale),error=>error.code==='quality_feature_gate_stale');
  const missing=structuredClone(plan);
  delete missing.metadata['partme.quality_loop_gate'];
  assert.throws(()=>validateWorkflowPlan(missing),error=>error.code==='quality_feature_gate_invalid');
});

test('feature flag parser rejects unknown fields and preview default enablement',()=>{
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'jianying-quality-gate-'));
  const file=path.join(root,'feature-flags.json');
  fs.writeFileSync(file,JSON.stringify({schema:'jianying-plugin-feature-flags/v1',features:{
    iterative_video_quality_loop:{default_enabled:false,stage:'preview',
      rollback:'preserve_ledgers_and_pending_occupancy',unknown:true}}}));
  assert.throws(()=>resolveQualityLoopGate({optIn:true,configPath:file}),error=>error.code==='quality_feature_config_invalid');
  fs.writeFileSync(file,JSON.stringify({schema:'jianying-plugin-feature-flags/v1',features:{
    iterative_video_quality_loop:{default_enabled:true,stage:'preview',
      rollback:'preserve_ledgers_and_pending_occupancy'}}}));
  assert.throws(()=>resolveQualityLoopGate({configPath:file}),error=>error.code==='quality_feature_config_invalid');
});

test('closing the gate preserves an ambiguous side-effect ledger and its occupancy',()=>{
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'jianying-quality-rollback-'));
  const ledger=new SideEffectLedger({stateRoot:path.join(root,'ledger')});
  const scope={workflow_id:'VLOG-01',revision:2,target_digest:'a'.repeat(64)};
  const {state}=ledger.begin({type:'native_export',scope});
  ledger.claim(state.id);
  ledger.ambiguous(state.id,{reason:'injected_crash_after_submit'});
  const ledgerFile=path.join(root,'ledger',state.id,'ledger.json');
  const before=fs.readFileSync(ledgerFile);

  assert.throws(()=>attachQualityLoop(basePlan(),{creativeTargets:[FIXTURE.creative_target],
    iterationPolicy:FIXTURE.iteration_policy}),error=>error.code==='quality_loop_disabled');
  assert.deepEqual(fs.readFileSync(ledgerFile),before);
  assert.throws(()=>ledger.begin({type:'native_export',scope}),error=>error.code==='side_effect_reconciliation_required');
});
