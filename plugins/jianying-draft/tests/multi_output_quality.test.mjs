import test from 'node:test';
import assert from 'node:assert/strict';

import {
  evaluateMultiOutputCompletion,
  verifyOutputRevisionIsolation,
  authorizePurposeOutputs,
} from '../scripts/multi_output_quality.mjs';

const verdict=(output_id,decision,revision=1)=>({output_id,decision,revision,input_digest:'a'.repeat(64)});

test('course parent waits for every required output and a failed teaser stays isolated',()=>{
  const status=evaluateMultiOutputCompletion({
    requiredOutputs:['master','teaser-1','teaser-2','teaser-3'],
    verdicts:[verdict('master','pass'),verdict('teaser-1','pass'),verdict('teaser-2','revise'),verdict('teaser-3','pass')],
  });
  assert.equal(status.terminal_state,'revision_required');
  assert.deepEqual(status.passed_outputs,['master','teaser-1','teaser-3']);
  assert.deepEqual(status.revision_outputs,['teaser-2']);
  assert.deepEqual(status.completed_outputs,[]);
});

test('course local revision changes only the requested teaser before parent completes',()=>{
  const before={master:'1'.repeat(64),'teaser-1':'2'.repeat(64),'teaser-2':'3'.repeat(64),'teaser-3':'4'.repeat(64)};
  const after={...before,'teaser-2':'5'.repeat(64)};
  assert.deepEqual(verifyOutputRevisionIsolation({before,after,expectedChanged:['teaser-2']}),{
    changed_outputs:['teaser-2'],unchanged_outputs:['master','teaser-1','teaser-3'],isolated:true,
  });
  const status=evaluateMultiOutputCompletion({
    requiredOutputs:Object.keys(after),
    verdicts:[verdict('master','pass'),verdict('teaser-1','pass'),verdict('teaser-2','pass',2),verdict('teaser-3','pass')],
  });
  assert.equal(status.terminal_state,'completed');
  assert.deepEqual(status.completed_outputs,Object.keys(after));
});

test('wedding private approval never authorizes the commercial output',()=>{
  const result=authorizePurposeOutputs({
    outputs:[
      {output_id:'ceremony',purpose:'private'},
      {output_id:'memory',purpose:'private'},
      {output_id:'advertisement',purpose:'commercial'},
    ],
    approvals:[{approval_id:'private-1',purpose:'private',output_ids:['ceremony','memory']}],
  });
  assert.deepEqual(result.authorized_outputs,['ceremony','memory']);
  assert.deepEqual(result.blocked_outputs,[{output_id:'advertisement',code:'commercial_approval_required'}]);
});

test('purpose approval must enumerate each output and cannot be reused across purposes',()=>{
  assert.throws(()=>authorizePurposeOutputs({
    outputs:[{output_id:'advertisement',purpose:'commercial'}],
    approvals:[{approval_id:'bad',purpose:'private',output_ids:['advertisement']}],
  }),error=>error.code==='purpose_approval_mismatch');
});
