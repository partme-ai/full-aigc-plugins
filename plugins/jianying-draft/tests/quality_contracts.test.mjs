import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const ROOT=path.resolve(import.meta.dirname,'..');
const FIXTURE=JSON.parse(fs.readFileSync(path.join(ROOT,'tests/fixtures/quality-loop/contracts.json'),'utf8'));

async function api() {
  return import('../scripts/quality_contracts.mjs');
}

test('all quality-loop fixtures validate and produce stable canonical digests',async()=>{
  const {validateQualityContract,qualityContractDigest}=await api();
  for(const value of Object.values(FIXTURE)) {
    assert.deepEqual(validateQualityContract(value),{valid:true,schema:value.schema});
    const reversed=Object.fromEntries(Object.entries(value).reverse());
    assert.equal(qualityContractDigest(value),qualityContractDigest(reversed));
    assert.match(qualityContractDigest(value),/^[a-f0-9]{64}$/);
  }
});

test('strict parsing rejects unknown fields, duplicate keys, deep input and oversized payloads',async()=>{
  const {parseQualityContract}=await api();
  assert.throws(()=>parseQualityContract('{"schema":"jianying-creative-target/v1","schema":"x"}'),
    error=>error.code==='catalog_duplicate_key');
  const unknown=structuredClone(FIXTURE.creative_target); unknown.command='rm';
  assert.throws(()=>parseQualityContract(JSON.stringify(unknown)),error=>error.code==='quality_contract_invalid');
  const deep='{"a":'.repeat(65)+'0'+'}'.repeat(65);
  assert.throws(()=>parseQualityContract(deep),error=>error.code==='catalog_resource_limit');
  assert.throws(()=>parseQualityContract(JSON.stringify(FIXTURE.creative_target),{maximumBytes:8}),
    error=>error.code==='quality_contract_resource_limit');
});

test('creative target separates sources and invalidates unsafe execution claims',async()=>{
  const {validateQualityContract}=await api();
  for(const mutate of [
    value=>{value.revision=0;},
    value=>{value.target_duration_us=-1;},
    value=>{value.constraints[0].source_status='model_confirmed';},
    value=>{value.quality_profiles[0].digest='bad';},
    value=>{value.metadata.approved=true;},
  ]) {
    const value=structuredClone(FIXTURE.creative_target); mutate(value);
    assert.throws(()=>validateQualityContract(value),error=>error.code==='quality_contract_invalid');
  }
});

test('profile rejects duplicate dimensions, executable fields and invalid scoring boundaries',async()=>{
  const {validateQualityContract}=await api();
  for(const mutate of [
    value=>{value.dimensions.push(structuredClone(value.dimensions[0]));},
    value=>{value.dimensions[0].threshold=11;},
    value=>{value.allowed_actions.push('shell');},
    value=>{value.handler='custom';},
  ]) {
    const value=structuredClone(FIXTURE.quality_profile); mutate(value);
    assert.throws(()=>validateQualityContract(value),error=>error.code==='quality_contract_invalid');
  }
});

test('evaluation input and verdict bind evidence and hard gates before pass',async()=>{
  const {validateQualityContract}=await api();
  const input=structuredClone(FIXTURE.evaluation_input); input.artifacts[0].digest='bad';
  assert.throws(()=>validateQualityContract(input),error=>error.code==='quality_contract_invalid');
  const missingEvidence=structuredClone(FIXTURE.evaluation_verdict);
  missingEvidence.findings[0].evidence_refs=['absent'];
  assert.throws(()=>validateQualityContract(missingEvidence),error=>error.code==='quality_contract_invalid');
  const falsePass=structuredClone(FIXTURE.evaluation_verdict);
  falsePass.decision='pass'; falsePass.hard_gates[0].passed=false;
  assert.throws(()=>validateQualityContract(falsePass),error=>error.code==='quality_contract_invalid');
  const invented=structuredClone(FIXTURE.evaluation_verdict); invented.command=['jianying','job','run'];
  assert.throws(()=>validateQualityContract(invented),error=>error.code==='quality_contract_invalid');
});

test('caption transcript and language-review status cannot promote unconfirmed text to fact evidence',async()=>{
  const {validateQualityContract}=await api();
  const input=structuredClone(FIXTURE.evaluation_input);
  input.artifacts.push({artifact_id:'transcript-main',type:'transcript',digest:'a'.repeat(64),bytes:120});
  input.evidence.push({evidence_id:'transcript-context',type:'transcript_text',artifact_id:'transcript-main',
    digest:'b'.repeat(64),role:'context_only'});
  input.content_review.transcript={status:'unconfirmed',artifact_id:'transcript-main'};
  assert.deepEqual(validateQualityContract(input),{valid:true,schema:'jianying-evaluation-input/v1'});
  input.evidence[1].role='fact';
  assert.throws(()=>validateQualityContract(input),error=>error.code==='quality_contract_invalid');
  input.evidence[1].role='context_only';
  input.content_review.transcript.status='confirmed';
  input.evidence[1].role='fact';
  assert.deepEqual(validateQualityContract(input),{valid:true,schema:'jianying-evaluation-input/v1'});
  input.content_review.languages=[{language:'en',status:'unconfirmed'}];
  input.evidence.push({evidence_id:'language-en',type:'language_review',artifact_id:'transcript-main',
    digest:'c'.repeat(64),role:'fact',language:'en'});
  assert.throws(()=>validateQualityContract(input),error=>error.code==='quality_contract_invalid');
});

test('revision, iteration and evidence contracts enforce bounded and layered state',async()=>{
  const {validateQualityContract}=await api();
  const revision=structuredClone(FIXTURE.revision_request); revision.to_revision=1;
  assert.throws(()=>validateQualityContract(revision),error=>error.code==='quality_contract_invalid');
  const policy=structuredClone(FIXTURE.iteration_policy); policy.maximum_revisions=0;
  assert.throws(()=>validateQualityContract(policy),error=>error.code==='quality_contract_invalid');
  const evidence=structuredClone(FIXTURE.evidence_bundle); evidence.items.push(structuredClone(evidence.items[0]));
  assert.throws(()=>validateQualityContract(evidence),error=>error.code==='quality_contract_invalid');
  const elevated=structuredClone(FIXTURE.evidence_bundle); elevated.conclusion='passed';
  assert.throws(()=>validateQualityContract(elevated),error=>error.code==='quality_contract_invalid');
});

test('confirmed brief and reviewed route build isolated creative targets per output',async()=>{
  const {buildCreativeTargets}=await api();
  const brief={schema:'jianying-creative-brief/v1',request_id:'request-1',intent:'婚礼记录',constraints:{},dimensions:{},
    output_intents:[
      {id:'memory',purpose:'private',format:'video',delivery:'editable_draft'},
      {id:'advertisement',purpose:'commercial',format:'video',delivery:'native_export'},
    ],facts:[
      {name:'audience',value:'家人与朋友',source:'user',source_ref:'brief',confirmed:true},
      {name:'channel',value:'personal',source:'user',source_ref:'brief',confirmed:true},
      {name:'target_duration_us',value:'60000000',source:'user',source_ref:'brief',confirmed:true},
      {name:'must_keep',value:'交换戒指',source:'human',source_ref:'review-1',confirmed:true},
      {name:'must_avoid',value:'未授权宾客特写',source:'observed',source_ref:'privacy-1',confirmed:true,observed_at:'2026-09-21T00:00:00Z'},
      {name:'must_keep',value:'推断的烟花',source:'inferred',source_ref:'model-1',confirmed:false},
    ],metadata:{}};
  const route={schema:'jianying-open-route/v1',request_id:'request-1',selected_scenes:[{id:'WEDDING-01'}]};
  const profiles={
    memory:{profile_id:'wedding.memory',version:'1.0.0',digest:'a'.repeat(64)},
    advertisement:{profile_id:'wedding.commercial',version:'1.0.0',digest:'b'.repeat(64)},
  };
  const targets=buildCreativeTargets({brief,route,workflowId:'workflow-wedding',profiles});
  assert.equal(targets.length,2);
  assert.deepEqual(targets.map(item=>item.quality_profiles[0].output_id),['memory','advertisement']);
  assert.notEqual(targets[0].quality_profiles[0].digest,targets[1].quality_profiles[0].digest);
  assert.deepEqual(targets[0].constraints.map(item=>item.source_status),
    ['user_confirmed','observed','inferred_pending_review']);
  targets[0].constraints[0].value='changed';
  assert.equal(targets[1].constraints[0].value,'交换戒指');
});

test('creative target building requires reviewed route, confirmed boundary facts and one profile per output',async()=>{
  const {buildCreativeTargets}=await api();
  const brief={schema:'jianying-creative-brief/v1',request_id:'r',intent:'Vlog',constraints:{},dimensions:{},
    output_intents:[{id:'main',purpose:'personal',format:'video',delivery:'editable_draft'}],facts:[],metadata:{}};
  const route={schema:'jianying-open-route/v1',request_id:'r',selected_scenes:[{id:'VG01'}]};
  assert.throws(()=>buildCreativeTargets({brief,route,workflowId:'workflow-vlog',profiles:{}}),
    error=>error.code==='quality_target_not_ready');
  brief.facts=[
    {name:'audience',value:'朋友',source:'user',source_ref:'brief',confirmed:true},
    {name:'channel',value:'personal',source:'user',source_ref:'brief',confirmed:true},
    {name:'target_duration_us',value:'60000000',source:'inferred',source_ref:'model',confirmed:false},
  ];
  assert.throws(()=>buildCreativeTargets({brief,route,workflowId:'workflow-vlog',profiles:{main:{profile_id:'vlog',version:'1.0.0',digest:'a'.repeat(64)}}}),
    error=>error.code==='quality_target_not_ready');
  route.request_id='different';
  assert.throws(()=>buildCreativeTargets({brief,route,workflowId:'workflow-vlog',profiles:{}}),
    error=>error.code==='quality_target_not_ready');
});
