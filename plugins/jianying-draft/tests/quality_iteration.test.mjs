import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

import {buildEvidenceBundle,verifyEvidenceBundle} from '../scripts/quality_evidence.mjs';
import {buildRevisionRequest,createWorkflowRevision,detectIterationStall,enforceIterationPolicy} from '../scripts/quality_iteration.mjs';
import {attachQualityLoop,validateWorkflowPlan} from '../scripts/workflow_plan.mjs';
import {qualityContractDigest} from '../scripts/quality_contracts.mjs';

const ROOT=path.resolve(import.meta.dirname,'..');
const FIXTURE=JSON.parse(fs.readFileSync(path.join(ROOT,'tests/fixtures/quality-loop/contracts.json'),'utf8'));

test('evidence aggregation binds artifact and only passes all required layers',()=>{
  const items=[
    {...FIXTURE.evidence_bundle.items[0]},
    {...FIXTURE.evidence_bundle.items[0],evidence_id:'technical-main',type:'technical',validator:'media-probe/v1',digest:'9'.repeat(64)},
    {...FIXTURE.evidence_bundle.items[0],evidence_id:'creative-main',type:'creative',validator:'manual/v1',digest:'a'.repeat(64)},
  ];
  const bundle=buildEvidenceBundle({workflowId:'VLOG-01',revision:1,outputId:'main',
    artifactDigest:'4'.repeat(64),items,requiredTypes:['structural','technical','creative']});
  assert.equal(bundle.conclusion,'passed');
  assert.deepEqual(verifyEvidenceBundle(bundle,{workflowId:'VLOG-01',revision:1,outputId:'main',
    artifactDigest:'4'.repeat(64),requiredTypes:['structural','technical','creative']}),{valid:true,conclusion:'passed'});
});

test('changed content, lower evidence, duplicate evidence and failures cannot be elevated',()=>{
  const structural=FIXTURE.evidence_bundle.items[0];
  const incomplete=buildEvidenceBundle({workflowId:'VLOG-01',revision:1,outputId:'main',artifactDigest:'4'.repeat(64),
    items:[structural],requiredTypes:['structural','technical','creative']});
  assert.equal(incomplete.conclusion,'incomplete');
  assert.throws(()=>verifyEvidenceBundle(incomplete,{workflowId:'VLOG-01',revision:1,outputId:'main',artifactDigest:'5'.repeat(64),
    requiredTypes:['structural']}),error=>error.code==='evidence_binding_mismatch');
  assert.throws(()=>buildEvidenceBundle({workflowId:'VLOG-01',revision:1,outputId:'main',artifactDigest:'4'.repeat(64),
    items:[structural,structuredClone(structural)],requiredTypes:['structural']}),error=>error.code==='quality_contract_invalid');
  const failed={...structural,passed:false,evidence_id:'failed'};
  assert.equal(buildEvidenceBundle({workflowId:'VLOG-01',revision:1,outputId:'main',artifactDigest:'4'.repeat(64),
    items:[failed],requiredTypes:['structural']}).conclusion,'failed');
});

test('review findings become bounded revision actions instead of commands',()=>{
  const request=buildRevisionRequest({verdict:FIXTURE.evaluation_verdict,
    allowedActions:['trim','reorder'],availableCapabilities:['timeline.edit']});
  assert.equal(request.schema,'jianying-revision-request/v1');
  assert.equal(request.from_revision,1); assert.equal(request.to_revision,2);
  assert.deepEqual(request.required_capabilities,['timeline.edit']);
  assert.deepEqual(request.required_approvals,['draft_write']);
  assert.equal(request.actions[0].type,'trim');
  assert.equal(JSON.stringify(request).includes('command'),false);
});

test('unsupported findings remain suggestions and cannot invent execution mappings',()=>{
  const verdict=structuredClone(FIXTURE.evaluation_verdict);
  verdict.findings[0].suggested_action='cinematic_transition';
  assert.throws(()=>buildRevisionRequest({verdict,allowedActions:['trim'],availableCapabilities:['timeline.edit']}),
    error=>error.code==='quality_revision_blocked');
  verdict.findings.push({...verdict.findings[0],code:'trim-opening',suggested_action:'trim'});
  const request=buildRevisionRequest({verdict,allowedActions:['trim'],availableCapabilities:['timeline.edit']});
  assert.equal(request.actions.length,1);
  assert.deepEqual(request.unsupported_suggestions,['opening_too_slow:cinematic_transition']);
});

test('revision actions fail closed when capabilities or verdict state are incompatible',()=>{
  assert.throws(()=>buildRevisionRequest({verdict:FIXTURE.evaluation_verdict,allowedActions:['trim'],availableCapabilities:[]}),
    error=>error.code==='quality_revision_blocked');
  const passed=structuredClone(FIXTURE.evaluation_verdict); passed.decision='pass'; passed.findings=[];
  assert.throws(()=>buildRevisionRequest({verdict:passed,allowedActions:['trim'],availableCapabilities:['timeline.edit']}),
    error=>error.code==='quality_revision_not_required');
});

test('revision request creates a new immutable plan revision and binds its evidence',()=>{
  const base={schema:'jianying-workflow-plan/v1',workflow_id:'VLOG-01',revision:1,
    catalog_ref:{schema:'jianying-planning-catalog/v2',digest:'c'.repeat(64)},tool_requirements:{capabilities:[]},
    brief:{},assets:[],route:{},outputs:[{output_id:'main',purpose:'personal',format:'video',delivery:'editable_draft',
      target:{logical_path:'outputs/main'}}],steps:[],limits:{maximum_revisions:3,maximum_budget:{currency:'CNY',amount:0}},
    risk_requirements:[],proof_requirements:[],metadata:{}};
  const plan=attachQualityLoop(base,{creativeTargets:[FIXTURE.creative_target],iterationPolicy:FIXTURE.iteration_policy,
    qualityLoopOptIn:true});
  const request=buildRevisionRequest({verdict:FIXTURE.evaluation_verdict,
    allowedActions:['trim'],availableCapabilities:['timeline.edit']});
  const revised=createWorkflowRevision({plan,verdict:FIXTURE.evaluation_verdict,revisionRequest:request});
  assert.equal(validateWorkflowPlan(revised).valid,true);
  assert.equal(revised.revision,2);
  assert.equal(revised.creative_targets[0].revision,2);
  assert.equal(revised.metadata['partme.verdict_digest'],qualityContractDigest(FIXTURE.evaluation_verdict));
  assert.equal(revised.metadata['partme.revision_request_digest'],qualityContractDigest(request));
  assert.equal(plan.revision,1);
  const tampered=structuredClone(request); tampered.verdict_digest='0'.repeat(64);
  assert.throws(()=>createWorkflowRevision({plan,verdict:FIXTURE.evaluation_verdict,revisionRequest:tampered}),
    error=>error.code==='quality_revision_binding_mismatch');
});

test('iteration policy blocks limits and side effects before another revision',()=>{
  const base={current_revision:1,model_calls:0,accumulated_budget:{currency:'CNY',amount:0},
    completed_human_reviews:['before_revision_execution']};
  assert.deepEqual(enforceIterationPolicy({policy:FIXTURE.iteration_policy,state:base,now:'2026-09-21T00:00:00Z'}),
    {allowed:true,next_revision:2});
  for(const [change,code] of [
    [state=>{state.current_revision=3;},'quality_revision_limit'],
    [state=>{state.model_calls=2;},'quality_model_call_limit'],
    [state=>{state.accumulated_budget.amount=1;},'quality_budget_limit'],
    [state=>{state.completed_human_reviews=[];},'quality_human_review_required'],
  ]) {
    const state=structuredClone(base); change(state);
    assert.throws(()=>enforceIterationPolicy({policy:FIXTURE.iteration_policy,state,now:'2026-09-21T00:00:00Z'}),
      error=>error.code===code);
  }
  assert.throws(()=>enforceIterationPolicy({policy:FIXTURE.iteration_policy,state:base,now:'2100-01-01T00:00:00Z'}),
    error=>error.code==='quality_deadline_exceeded');
});

test('stagnation detects weak improvement repeated findings and hard-gate regression',()=>{
  const previous=structuredClone(FIXTURE.evaluation_verdict);
  const current=structuredClone(FIXTURE.evaluation_verdict); current.revision=2;
  current.scores[0].value=6.5;
  let result=detectIterationStall({policy:FIXTURE.iteration_policy,previousVerdict:previous,currentVerdict:current,
    findingHistory:[['opening_too_slow']]});
  assert.equal(result.stopped,true);
  assert.ok(result.reasons.includes('minimum_material_improvement'));
  assert.ok(result.reasons.includes('repeated_finding'));
  current.scores[0].value=8; current.hard_gates[0].passed=false;
  result=detectIterationStall({policy:FIXTURE.iteration_policy,previousVerdict:previous,currentVerdict:current,findingHistory:[]});
  assert.equal(result.stopped,true);
  assert.ok(result.reasons.includes('hard_gate_regression'));
});
