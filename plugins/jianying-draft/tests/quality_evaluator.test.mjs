import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

import {createManualEvaluator,createTechnicalEvaluator,runEvaluator} from '../scripts/quality_evaluator.mjs';
import {qualityContractDigest} from '../scripts/quality_contracts.mjs';
import {canonical,sha256} from '../scripts/workflow_data.mjs';

const ROOT=path.resolve(import.meta.dirname,'..');
const FIXTURE=JSON.parse(fs.readFileSync(path.join(ROOT,'tests/fixtures/quality-loop/contracts.json'),'utf8'));

test('manual evaluator constructs an identity-bound verdict from review facts',()=>{
  const adapter=createManualEvaluator({reviewerId:'reviewer-1',version:'1'});
  const verdict=runEvaluator({adapter,input:FIXTURE.evaluation_input,profile:FIXTURE.quality_profile,context:{review:{
    decision:'revise',evidence_refs:['probe-main'],scores:[{dimension_id:'narrative',value:6,passed:false}],
    hard_gates:[{rule_id:'privacy',passed:true,evidence_refs:['probe-main']}],findings:FIXTURE.evaluation_verdict.findings,
    limitations:[],
  }}});
  assert.equal(verdict.evaluator.type,'human');
  assert.equal(verdict.evaluator.model,'reviewer-1');
  assert.equal(verdict.input_digest,qualityContractDigest(FIXTURE.evaluation_input));
  assert.equal(verdict.workflow_id,FIXTURE.evaluation_input.workflow_id);
});

test('deterministic evaluator passes valid artifact facts and blocks empty artifacts',()=>{
  const adapter=createTechnicalEvaluator({version:'1'});
  const passed=runEvaluator({adapter,input:FIXTURE.evaluation_input,profile:FIXTURE.quality_profile});
  assert.equal(passed.decision,'pass');
  assert.equal(passed.hard_gates[0].passed,true);
  const input=structuredClone(FIXTURE.evaluation_input); input.artifacts[0].bytes=0;
  const blocked=runEvaluator({adapter,input,profile:FIXTURE.quality_profile});
  assert.equal(blocked.decision,'blocked');
  assert.equal(blocked.findings[0].code,'artifact_empty');
});

test('locked Vlog audio requirement cannot pass without technical audio evidence',()=>{
  const catalog=JSON.parse(fs.readFileSync(path.join(ROOT,
    'skills/jianying-draft-video-planning/references/quality-profiles-v1.json'),'utf8'));
  const profile=catalog.profiles.find(item=>item.profile_id==='vlog.personal-story');
  assert.ok(profile.dimensions.some(item=>item.evidence_types.includes('audio_metrics')));
  const adapter=createTechnicalEvaluator({version:'1'});
  const missing=runEvaluator({adapter,input:FIXTURE.evaluation_input,profile});
  assert.equal(missing.decision,'blocked');
  assert.ok(missing.findings.some(item=>item.code==='audio_evidence_missing'));
  assert.ok(missing.hard_gates.some(item=>item.rule_id==='required_audio_evidence' && !item.passed));

  const contextual=structuredClone(FIXTURE.evaluation_input);
  contextual.evidence.push({evidence_id:'audio-context',type:'audio_metrics',artifact_id:'proxy-main',
    digest:'a'.repeat(64),role:'context_only'});
  assert.equal(runEvaluator({adapter,input:contextual,profile}).decision,'blocked');

  const technical=structuredClone(contextual);
  technical.evidence.at(-1).role='technical';
  assert.equal(runEvaluator({adapter,input:technical,profile}).decision,'blocked');
  const mediaDigest='b'.repeat(64);
  technical.evidence.push({evidence_id:`media-quality-${mediaDigest.slice(0,20)}`,type:'media_quality',
    artifact_id:'proxy-main',digest:mediaDigest,role:'technical'});
  const audioDigest=sha256(canonical({media_quality_digest:mediaDigest,
    artifact_digest:technical.artifacts[0].digest,type:'audio_metrics'}));
  technical.evidence.find(item=>item.type==='audio_metrics').digest=audioDigest;
  technical.evidence.find(item=>item.type==='audio_metrics').evidence_id=`audio-metrics-${audioDigest.slice(0,20)}`;
  const verdict=runEvaluator({adapter,input:technical,profile});
  assert.equal(verdict.decision,'pass');
  assert.ok(verdict.limitations.some(item=>item.includes('does not judge')));
  assert.equal(verdict.scores.some(item=>item.dimension_id==='audio_visual_coherence'),false);
});

test('independent reviewer cannot pass a locked audio profile using a context claim',()=>{
  const catalog=JSON.parse(fs.readFileSync(path.join(ROOT,
    'skills/jianying-draft-video-planning/references/quality-profiles-v1.json'),'utf8'));
  const profile=catalog.profiles.find(item=>item.profile_id==='vlog.personal-story');
  const adapter=createManualEvaluator({reviewerId:'reviewer-1',version:'1'});
  const review={decision:'pass',evidence_refs:['probe-main'],scores:[],hard_gates:[],findings:[],limitations:[]};
  assert.throws(()=>runEvaluator({adapter,input:FIXTURE.evaluation_input,profile,context:{review}}),
    error=>error.code==='evaluation_evidence_insufficient');
});

test('adapter output is rebound and cannot impersonate executor or return free text',()=>{
  const rebound=runEvaluator({adapter:{identity:{type:'model',provider:'fixture',model:'bound',version:'1'},
    evaluate:()=>({...FIXTURE.evaluation_verdict,workflow_id:'other',revision:99,input_digest:'f'.repeat(64)})},
    input:FIXTURE.evaluation_input,profile:FIXTURE.quality_profile});
  assert.equal(rebound.workflow_id,FIXTURE.evaluation_input.workflow_id);
  assert.equal(rebound.revision,FIXTURE.evaluation_input.revision);
  assert.equal(rebound.input_digest,qualityContractDigest(FIXTURE.evaluation_input));
  const bad=[
    {identity:{type:'executor',provider:'fixture',model:'bad',version:'1'},evaluate:()=>({})},
    {identity:{type:'model',provider:'fixture',model:'bad',version:'1'},evaluate:()=>"looks good"},
  ];
  for(const adapter of bad) assert.throws(()=>runEvaluator({adapter,input:FIXTURE.evaluation_input,profile:FIXTURE.quality_profile}),
    error=>['evaluation_binding_mismatch','quality_contract_invalid','evaluator_invalid'].includes(error.code));
});

test('manual evaluator cannot smuggle commands or approvals through review fields',()=>{
  const adapter=createManualEvaluator({reviewerId:'reviewer-1',version:'1'});
  assert.throws(()=>runEvaluator({adapter,input:FIXTURE.evaluation_input,profile:FIXTURE.quality_profile,context:{review:{
    ...FIXTURE.evaluation_verdict,command:'jianying job run',approved:true,
  }}}),error=>error.code==='quality_contract_invalid');
});

test('evaluator cannot cite unknown evidence or pass using context-only transcript evidence',()=>{
  const input=structuredClone(FIXTURE.evaluation_input);
  const manual=createManualEvaluator({reviewerId:'reviewer-1',version:'1'});
  const review={decision:'pass',evidence_refs:['unknown'],scores:[{dimension_id:'narrative',value:10,passed:true}],
    hard_gates:[{rule_id:'privacy',passed:true,evidence_refs:['unknown']}],findings:[],limitations:[]};
  assert.throws(()=>runEvaluator({adapter:manual,input,profile:FIXTURE.quality_profile,context:{review}}),
    error=>error.code==='evaluation_binding_mismatch');
  input.artifacts.push({artifact_id:'transcript-main',type:'transcript',digest:'a'.repeat(64),bytes:120});
  input.evidence.push({evidence_id:'transcript-context',type:'transcript_text',artifact_id:'transcript-main',
    digest:'b'.repeat(64),role:'context_only'});
  input.content_review.transcript={status:'unconfirmed',artifact_id:'transcript-main'};
  review.evidence_refs=['transcript-context']; review.hard_gates[0].evidence_refs=['transcript-context'];
  assert.throws(()=>runEvaluator({adapter:manual,input,profile:FIXTURE.quality_profile,context:{review}}),
    error=>error.code==='evaluation_binding_mismatch');
});
