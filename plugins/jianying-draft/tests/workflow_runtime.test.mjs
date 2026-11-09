import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const compilation={schema:'jianying-workflow-compilation/v1',can_compile:true,can_execute:false,
  plan_digest:'1'.repeat(64),blockers:[{code:'approval_required'}],
  job_bindings:[{output_id:'main',purpose:'personal',output_path:'/tmp/output-main',job_digest:'2'.repeat(64),
    job:{schema:'jianying-job/v2',operation:'create'}}],
  receipt:{schema:'jianying-compilation-receipt/v1',execution_digest:'3'.repeat(64),semantic_digest:'4'.repeat(64),
    cli:{version:'1.6.19',sha256:'5'.repeat(64),job_schema:'jianying-job/v2'}}};

async function runtime(t,options={}) {
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'jy-runtime-')); t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  const {WorkflowRuntime}=await import('../scripts/workflow_runtime.mjs');
  return {root,run:new WorkflowRuntime({stateRoot:root,...options})};
}

test('approval binds revision inputs jobs CLI purpose target budget and expiry',async t=>{
  const {run}=await runtime(t); const state=run.start({compilation,revision:1,budget:{currency:'CNY',maximum:0}});
  const binding=run.approvalBinding(state.run_id);
  assert.deepEqual(Object.keys(binding).sort(),['budget','cli_sha256','execution_digest','expires_scope','job_digests',
    'plan_digest','purposes','revision','run_id','targets'].sort());
  assert.throws(()=>run.approve(state.run_id,{...binding,execution_digest:'bad',user_id:'u',expires_at:'2999-01-01T00:00:00Z'}),
    e=>e.code==='approval_scope_mismatch');
  const approved=run.approve(state.run_id,{...binding,user_id:'u',expires_at:'2999-01-01T00:00:00Z'});
  assert.equal(approved.stage,'ready');
});

test('expired approval is rejected before any side effect',async t=>{
  let effects=0;
  const {run}=await runtime(t,{executor:()=>{effects++;return {ok:true,artifacts:[]};}});
  const state=run.start({compilation,revision:1,budget:{currency:'CNY',maximum:0}});
  const binding=run.approvalBinding(state.run_id);
  assert.throws(()=>run.approve(state.run_id,{...binding,user_id:'u',expires_at:'2000-01-01T00:00:00Z'}),
    error=>error.code==='approval_expired');
  assert.equal(effects,0);
  assert.equal(run.show(state.run_id).stage,'awaiting_approval');
});

test('approval is rechecked against the execution clock after it was granted',async t=>{
  let effects=0,now=Date.parse('2030-01-01T00:00:00Z');
  const {run}=await runtime(t,{now:()=>now,executor:()=>{effects++;return {ok:true,artifacts:[]};}});
  const state=run.start({compilation,revision:1,budget:{currency:'CNY',maximum:0}});
  const binding=run.approvalBinding(state.run_id);
  run.approve(state.run_id,{...binding,user_id:'u',expires_at:'2030-01-01T00:01:00Z'});
  now=Date.parse('2030-01-01T00:02:00Z');
  assert.throws(()=>run.execute(state.run_id),error=>error.code==='approval_required');
  assert.equal(effects,0);
  assert.equal(run.show(state.run_id).stage,'ready');
});

test('approval revocation and bounded revision invalidate prior approval and evidence',async t=>{
  const {run}=await runtime(t); const state=run.start({compilation,revision:1,budget:{currency:'CNY',maximum:0}});
  const binding=run.approvalBinding(state.run_id);
  run.approve(state.run_id,{...binding,user_id:'u',expires_at:'2999-01-01T00:00:00Z'});
  assert.equal(run.revokeApproval(state.run_id,{user_id:'u'}).stage,'awaiting_approval');
  assert.throws(()=>run.execute(state.run_id),e=>e.code==='approval_required');
  const revised=run.revise(state.run_id,{plan_digest:'6'.repeat(64),execution_digest:'7'.repeat(64)});
  assert.equal(revised.revision,2); assert.equal(revised.approval,null); assert.deepEqual(revised.evidence,[]);
  assert.throws(()=>run.revise(state.run_id,{plan_digest:'8'.repeat(64),execution_digest:'9'.repeat(64),revision:5}),
    e=>e.code==='workflow_revision_limit');
});

test('two runtime instances execute one side effect only',async t=>{
  let effects=0;
  const {root,run}=await runtime(t,{executor:()=>{effects++; return {ok:true,artifacts:[{output_id:'main',path:'/tmp/output-main'}]};},
    verifier:()=>({ok:true,evidence:[{level:'structural'}]})});
  const {WorkflowRuntime}=await import('../scripts/workflow_runtime.mjs'); const other=new WorkflowRuntime({stateRoot:root,
    executor:()=>{effects++; return {ok:true};},verifier:()=>({ok:true,evidence:[]})});
  const state=run.start({compilation,revision:1,budget:{currency:'CNY',maximum:0}}),binding=run.approvalBinding(state.run_id);
  run.approve(state.run_id,{...binding,user_id:'u',expires_at:'2999-01-01T00:00:00Z'});
  assert.equal(run.execute(state.run_id).terminal_state,'completed');
  assert.equal(other.execute(state.run_id).terminal_state,'completed');
  assert.equal(effects,1);
});

test('unknown outcome stays occupied until reconciliation verifies the existing artifact',async t=>{
  const {run}=await runtime(t,{executor:()=>{const error=new Error('lost response');error.outcome='unknown';throw error;},
    verifier:()=>({ok:true,evidence:[{level:'structural',sha256:'6'.repeat(64)}]})});
  const state=run.start({compilation,revision:1,budget:{currency:'CNY',maximum:0}}),binding=run.approvalBinding(state.run_id);
  run.approve(state.run_id,{...binding,user_id:'u',expires_at:'2999-01-01T00:00:00Z'});
  assert.throws(()=>run.execute(state.run_id),e=>e.code==='execution_outcome_unknown');
  assert.equal(run.show(state.run_id).stage,'reconciling');
  assert.equal(run.reconcile(state.run_id,{outcome:'artifact_exists'}).terminal_state,'completed');
});

test('crash after a successful side effect but before result persistence requires reconciliation',async t=>{
  let effects=0,artifactExists=false;
  const {run}=await runtime(t,{
    executor:()=>{effects++;artifactExists=true;return {ok:true,artifacts:[{output_id:'main',path:'/tmp/output-main'}]};},
    checkpoint:name=>{if(name==='execution.returned_before_persist') throw new Error('simulated process crash');},
    verifier:()=>({ok:artifactExists,evidence:artifactExists?[{level:'structural',sha256:'7'.repeat(64)}]:[]})
  });
  const state=run.start({compilation,revision:1,budget:{currency:'CNY',maximum:0}}),binding=run.approvalBinding(state.run_id);
  run.approve(state.run_id,{...binding,user_id:'u',expires_at:'2999-01-01T00:00:00Z'});
  assert.throws(()=>run.execute(state.run_id),error=>error.code==='execution_outcome_unknown');
  assert.equal(effects,1);
  assert.equal(run.show(state.run_id).stage,'reconciling');
  assert.throws(()=>run.resume(state.run_id),error=>error.code==='manual_reconciliation_required');
  assert.equal(effects,1);
  assert.equal(run.reconcile(state.run_id,{outcome:'artifact_exists'}).terminal_state,'completed');
  assert.equal(effects,1);
});

test('cancel request does not release occupancy before stop confirmation',async t=>{
  const {run}=await runtime(t); const state=run.start({compilation,revision:1,budget:{currency:'CNY',maximum:0}});
  const requested=run.cancel(state.run_id); assert.equal(requested.stage,'cancel_requested');
  assert.throws(()=>run.resume(state.run_id),e=>e.code==='cancel_not_confirmed');
  assert.equal(run.confirmCancelled(state.run_id).terminal_state,'cancelled');
  assert.throws(()=>run.resume(state.run_id),e=>e.code==='task_cancelled');
});

test('independent artifact verification rejects missing and duration-mismatched drafts',async t=>{
  const {verifyDraftArtifact}=await import('../scripts/workflow_runtime.mjs');
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'jy-draft-')); t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  assert.equal(verifyDraftArtifact(root,{duration_us:3000000}).ok,false);
  fs.writeFileSync(path.join(root,'draft_content.json'),JSON.stringify({duration:14008333,tracks:[{segments:[{}]}]}));
  fs.writeFileSync(path.join(root,'draft_meta_info.json'),'{}');
  const result=verifyDraftArtifact(root,{duration_us:3000000});
  assert.equal(result.ok,false); assert.ok(result.issues.some(issue=>issue.code==='duration_mismatch'));
});

test('stop_all blocks every branch when one required output is blocked',async t=>{
  const blocked=structuredClone(compilation);
  blocked.job_bindings.push({...blocked.job_bindings[0],output_id:'advertisement',purpose:'commercial',
    output_path:'/tmp/output-ad',job_digest:'6'.repeat(64),blockers:[{code:'commercial_approval_required'}]});
  const {run}=await runtime(t); const state=run.start({compilation:blocked,revision:1,budget:{currency:'CNY',maximum:0}});
  assert.equal(state.stage,'blocked'); assert.equal(state.terminal_state,null);
  assert.deepEqual(state.runnable_outputs,[]); assert.deepEqual(state.blocked_outputs,['advertisement']);
});

test('continue_independent executes permitted branches but parent remains partially completed',async t=>{
  const mixed=structuredClone(compilation);
  mixed.job_bindings.push({...mixed.job_bindings[0],output_id:'advertisement',purpose:'commercial',
    output_path:'/tmp/output-ad',job_digest:'6'.repeat(64),blockers:[{code:'commercial_approval_required'}]});
  let received=[];
  const {run}=await runtime(t,{executor:bindings=>{received=bindings;return {artifacts:[{output_id:'main',path:'/tmp/output-main'}]};},
    verifier:()=>({ok:true,evidence:[{level:'structural'}]})});
  const state=run.start({compilation:mixed,revision:1,budget:{currency:'CNY',maximum:0},failure_policy:'continue_independent'});
  const binding=run.approvalBinding(state.run_id);
  run.approve(state.run_id,{...binding,user_id:'u',expires_at:'2999-01-01T00:00:00Z'});
  const finished=run.execute(state.run_id);
  assert.deepEqual(received.map(item=>item.output_id),['main']);
  assert.equal(finished.stage,'partially_completed');
  assert.equal(finished.terminal_state,'partially_completed');
  assert.deepEqual(finished.blocked_outputs,['advertisement']);
});
