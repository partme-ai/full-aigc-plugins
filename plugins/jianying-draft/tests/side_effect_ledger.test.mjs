import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {SideEffectLedger} from '../scripts/side_effect_ledger.mjs';

for(const type of ['draft_write','remote_evaluation','native_export']) test(`${type} persists before execution and reconciles unknown outcome`,()=>{
  const ledger=new SideEffectLedger({stateRoot:fs.mkdtempSync(path.join(os.tmpdir(),'jianying-side-effect-'))});
  const scope={workflow_id:'VLOG-01',revision:1,target_digest:'a'.repeat(64)};
  const {state}=ledger.begin({type,scope});assert.equal(state.state,'queued');
  const claimed=ledger.claim(state.id);assert.equal(claimed.epoch,1);
  ledger.ambiguous(state.id,{reason:'injected_crash_after_submit'});
  assert.throws(()=>ledger.begin({type,scope}),error=>error.code==='side_effect_reconciliation_required');
  const reconciled=ledger.reconcile(state.id,{outcome:'succeeded',artifact:{digest:'b'.repeat(64)}});
  assert.equal(reconciled.state,'succeeded');
  const reused=ledger.begin({type,scope});assert.equal(reused.reused,true);assert.equal(reused.state.artifact.digest,'b'.repeat(64));
});

test('single writer lock rejects a second epoch claimant',()=>{
  const ledger=new SideEffectLedger({stateRoot:fs.mkdtempSync(path.join(os.tmpdir(),'jianying-side-effect-'))});
  const {state}=ledger.begin({type:'draft_write',scope:{id:'one'}});ledger.claim(state.id);
  assert.throws(()=>ledger.claim(state.id),error=>error.code==='side_effect_writer_occupied');
});
