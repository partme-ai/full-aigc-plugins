import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {spawnSync} from 'node:child_process';

import {qualityContractDigest,validateQualityContract} from '../scripts/quality_contracts.mjs';
import {
  applyRetargetProposal,
  buildComparativeEvaluationContext,
  buildMacroRevisionRequest,
  buildRetargetProposal,
  buildVisualReferenceSet,
} from '../scripts/quality_iteration.mjs';
import {createManualEvaluator,runEvaluator} from '../scripts/quality_evaluator.mjs';

const ROOT=path.resolve(import.meta.dirname,'..');
const BASE=JSON.parse(fs.readFileSync(path.join(ROOT,'tests/fixtures/quality-loop/contracts.json'),'utf8'));
const COMPARATIVE=JSON.parse(fs.readFileSync(path.join(ROOT,'tests/fixtures/quality-loop/comparative-contracts.json'),'utf8'));

const targetFor=(revision=1)=>({...structuredClone(BASE.creative_target),revision});
const inputFor=(revision,proxyDigit,targetDigest=qualityContractDigest(targetFor(revision)))=>({
  ...structuredClone(BASE.evaluation_input),revision,target_digest:targetDigest,
  artifacts:[{...BASE.evaluation_input.artifacts[0],digest:String(proxyDigit).repeat(64)}],
});
const verdictFor=(revision,input)=>({...structuredClone(BASE.evaluation_verdict),revision,
  input_digest:qualityContractDigest(input)});

test('all comparative quality fixtures validate and keep canonical digests stable',()=>{
  for(const contract of Object.values(COMPARATIVE)) {
    assert.deepEqual(validateQualityContract(contract),{valid:true,schema:contract.schema});
    assert.equal(qualityContractDigest(contract),qualityContractDigest(Object.fromEntries(Object.entries(contract).reverse())));
  }
});

test('visual reference set is strict, digest-bound and contains no execution authority',()=>{
  const target=targetFor(1);
  const references=buildVisualReferenceSet({target,outputId:'main',references:[{
    reference_id:'opening-frame',type:'keyframe',artifact_digest:'a'.repeat(64),source_type:'user_supplied',
    usage:'opening composition',license_status:'cleared',allowed_deviations:['weather','background pedestrians'],
  }]});
  assert.deepEqual(validateQualityContract(references),{valid:true,schema:'jianying-visual-reference-set/v1'});
  assert.equal(references.target_digest,qualityContractDigest(target));
  const reordered=Object.fromEntries(Object.entries(references).reverse());
  assert.equal(qualityContractDigest(references),qualityContractDigest(reordered));
  for(const mutate of [
    value=>{value.command=['jianying','job','run'];},
    value=>{value.references[0].license_status='assumed';},
    value=>{value.references[0].artifact_digest='bad';},
  ]) {
    const value=structuredClone(references); mutate(value);
    assert.throws(()=>validateQualityContract(value),error=>error.code==='quality_contract_invalid');
  }
});

test('comparative context binds target current previous and a fresh read-only critic',()=>{
  const previousTarget=targetFor(1),currentTarget=targetFor(2);
  const references=buildVisualReferenceSet({target:currentTarget,outputId:'main',references:[{
    reference_id:'storyboard',type:'storyboard',artifact_digest:'b'.repeat(64),source_type:'reference_capture',
    usage:'narrative order',license_status:'restricted',allowed_deviations:['shot identity'],
  }]});
  const previousInput=inputFor(1,4,qualityContractDigest(previousTarget));
  const currentInput=inputFor(2,5,qualityContractDigest(currentTarget));
  const previousVerdict=verdictFor(1,previousInput);
  const context=buildComparativeEvaluationContext({target:currentTarget,references,currentInput,previousInput,
    previousVerdict,criticSessionId:'critic-session-2',usedCriticSessionIds:['critic-session-1']});
  assert.deepEqual(validateQualityContract(context),{valid:true,schema:'jianying-comparative-evaluation-context/v1'});
  assert.deepEqual(context.comparison_dimensions,['absolute_quality','target_gap','prior_delta']);
  assert.deepEqual(context.critic.allowed_tools,['artifact.inspect','evidence.read','quality.profile.read']);
  assert.equal(context.critic.fresh_context,true);
  assert.equal(context.critic.write_access,false);

  assert.throws(()=>buildComparativeEvaluationContext({target:currentTarget,references,currentInput,previousInput,
    previousVerdict,criticSessionId:'critic-session-1',usedCriticSessionIds:['critic-session-1']}),
  error=>error.code==='quality_critic_session_reused');
  const writable=structuredClone(context); writable.critic.write_access=true;
  assert.throws(()=>validateQualityContract(writable),error=>error.code==='quality_contract_invalid');
  const shell=structuredClone(context); shell.critic.allowed_tools.push('shell');
  assert.throws(()=>validateQualityContract(shell),error=>error.code==='quality_contract_invalid');
});

test('changed target or reference digest cannot reuse a comparative context',()=>{
  const target=targetFor(2);
  const references=buildVisualReferenceSet({target,outputId:'main',references:[{
    reference_id:'target-frame',type:'keyframe',artifact_digest:'c'.repeat(64),source_type:'generated',
    usage:'color and composition',license_status:'cleared',allowed_deviations:[],
  }]});
  const previousTarget=targetFor(1);
  const args={target,references,currentInput:inputFor(2,5,qualityContractDigest(target)),
    previousInput:inputFor(1,4,qualityContractDigest(previousTarget)),
    previousVerdict:verdictFor(1,inputFor(1,4,qualityContractDigest(previousTarget))),
    criticSessionId:'critic-session-new',usedCriticSessionIds:[]};
  const context=buildComparativeEvaluationContext(args);
  const changed=structuredClone(references); changed.references[0].allowed_deviations.push('subject identity');
  assert.notEqual(qualityContractDigest(references),qualityContractDigest(changed));
  assert.throws(()=>buildComparativeEvaluationContext({...args,references:changed,
    currentInput:{...args.currentInput,target_digest:'d'.repeat(64)}}),
  error=>error.code==='quality_comparison_binding_mismatch');
  assert.notEqual(context.reference_set_digest,qualityContractDigest(changed));
});

test('a stalled output gets at most one approved macro revision request',()=>{
  const target=targetFor(2);
  const references=buildVisualReferenceSet({target,outputId:'main',references:[{
    reference_id:'target-frame',type:'keyframe',artifact_digest:'e'.repeat(64),source_type:'user_supplied',
    usage:'visual target',license_status:'cleared',allowed_deviations:[],
  }]});
  const context=buildComparativeEvaluationContext({target,references,
    currentInput:inputFor(2,5,qualityContractDigest(target)),
    previousInput:inputFor(1,4,qualityContractDigest(targetFor(1))),
    previousVerdict:verdictFor(1,inputFor(1,4,qualityContractDigest(targetFor(1)))),
    criticSessionId:'critic-session-macro',usedCriticSessionIds:[]});
  const stalled={stopped:true,reasons:['minimum_material_improvement','repeated_finding'],material_improvement:0.2};
  const request=buildMacroRevisionRequest({context,stall:stalled,
    strategies:['restructure_timeline','rebuild_pacing'],priorMacroRequestDigests:[]});
  assert.deepEqual(validateQualityContract(request),{valid:true,schema:'jianying-macro-revision-request/v1'});
  assert.equal(request.maximum_once,true);
  assert.deepEqual(request.required_approvals,['human_macro_revision']);
  assert.throws(()=>buildMacroRevisionRequest({context,stall:stalled,strategies:['rebuild_pacing'],
    priorMacroRequestDigests:[qualityContractDigest(request)]}),error=>error.code==='quality_macro_revision_exhausted');
  assert.throws(()=>buildMacroRevisionRequest({context,stall:{stopped:false,reasons:[]},strategies:['rebuild_pacing'],
    priorMacroRequestDigests:[]}),error=>error.code==='quality_macro_revision_not_required');
});

test('retarget stays inert without exact human approval and invalidates old bindings when approved',()=>{
  const oldTarget=targetFor(2),newTarget={...targetFor(3),narrative_goal:'聚焦营地搭建而不是完整旅程'};
  const newReferences=buildVisualReferenceSet({target:newTarget,outputId:'main',references:[{
    reference_id:'retarget-storyboard',type:'storyboard',artifact_digest:'f'.repeat(64),source_type:'user_supplied',
    usage:'approved retarget',license_status:'cleared',allowed_deviations:['weather'],
  }]});
  const proposal=buildRetargetProposal({currentTarget:oldTarget,proposedTarget:newTarget,
    proposedReferences:newReferences,reason:'原素材缺少返程与日落镜头',evidenceRefs:['missing-shot-audit']});
  assert.deepEqual(validateQualityContract(proposal),{valid:true,schema:'jianying-retarget-proposal/v1'});
  const digest=qualityContractDigest(proposal);
  const approval={schema:'jianying-retarget-approval/v1',approval_id:'retarget-approval-1',status:'approved',
    proposal_digest:digest,user_id:'reviewer-1',expires_at:'2099-01-01T00:00:00.000Z'};
  const records=[
    {type:'verdict',id:'verdict-2',target_digest:proposal.from_target_digest},
    {type:'approval',id:'approval-2',target_digest:proposal.from_target_digest},
    {type:'evidence',id:'evidence-other',target_digest:'0'.repeat(64)},
    {type:'context',id:'context-2',target_digest:proposal.from_target_digest},
  ];
  assert.throws(()=>applyRetargetProposal({proposal,approval:{...approval,proposal_digest:'0'.repeat(64)},
    boundRecords:records,now:'2026-09-22T00:00:00.000Z'}),error=>error.code==='quality_retarget_approval_required');
  assert.throws(()=>applyRetargetProposal({proposal,approval:{...approval,expires_at:'2020-01-01T00:00:00.000Z'},
    boundRecords:records,now:'2026-09-22T00:00:00.000Z'}),error=>error.code==='quality_retarget_approval_required');
  const result=applyRetargetProposal({proposal,approval,boundRecords:records,now:'2026-09-22T00:00:00.000Z'});
  assert.equal(result.status,'retarget_applied');
  assert.equal(result.target_digest,proposal.proposed_target_digest);
  assert.deepEqual(result.invalidated,[
    {type:'approval',id:'approval-2'},
    {type:'context',id:'context-2'},
    {type:'verdict',id:'verdict-2'},
  ]);
  assert.equal(oldTarget.revision,2);
});

test('runtime distribution has no Dream Loop FAL Python or research dependency',()=>{
  const runtimeFiles=fs.readdirSync(path.join(ROOT,'scripts')).filter(name=>name.endsWith('.mjs'));
  const forbidden=/(?:research\/dream-loop|fal-batch|from\s+['"]dream-loop|python(?:3)?\s+.*dream-loop)/i;
  for(const name of runtimeFiles) {
    const source=fs.readFileSync(path.join(ROOT,'scripts',name),'utf8');
    assert.equal(forbidden.test(source),false,`${name} introduces a forbidden Dream Loop runtime dependency`);
  }
});

test('comparative context is enforced by evaluator and exposed through the Harness command surface',t=>{
  const previousTarget=targetFor(1),currentTarget=targetFor(2);
  const references=buildVisualReferenceSet({target:currentTarget,outputId:'main',references:[{
    reference_id:'judge-frame',type:'keyframe',artifact_digest:'9'.repeat(64),source_type:'user_supplied',
    usage:'comparison',license_status:'cleared',allowed_deviations:[],
  }]});
  const previousInput=inputFor(1,4,qualityContractDigest(previousTarget));
  const currentInput=inputFor(2,5,qualityContractDigest(currentTarget));
  const context=buildComparativeEvaluationContext({target:currentTarget,references,currentInput,previousInput,
    previousVerdict:verdictFor(1,previousInput),criticSessionId:'critic-evaluator',usedCriticSessionIds:[]});
  const adapter=createManualEvaluator({reviewerId:'reviewer',version:'1'});
  const verdict=runEvaluator({adapter,input:currentInput,profile:BASE.quality_profile,comparativeContext:context,
    context:{review:{decision:'blocked',evidence_refs:['probe-main'],scores:[{dimension_id:'narrative',value:6,passed:false}],
      hard_gates:[{rule_id:'privacy',passed:true,evidence_refs:['probe-main']}],findings:[],limitations:['human review']}}});
  assert.equal(verdict.revision,2);
  const mismatched=structuredClone(context); mismatched.current.evaluation_input_digest='0'.repeat(64);
  assert.throws(()=>runEvaluator({adapter,input:currentInput,profile:BASE.quality_profile,comparativeContext:mismatched,
    context:{review:{decision:'blocked',evidence_refs:[],scores:[],hard_gates:[],findings:[],limitations:[]}}}),
  error=>error.code==='evaluation_binding_mismatch');

  const temporary=fs.mkdtempSync(path.join(os.tmpdir(),'jianying-comparative-command-'));
  t.after(()=>fs.rmSync(temporary,{recursive:true,force:true}));
  const requestPath=path.join(temporary,'reference-request.json');
  fs.writeFileSync(requestPath,JSON.stringify({target:currentTarget,outputId:'main',references:[{
    reference_id:'command-frame',type:'keyframe',artifact_digest:'8'.repeat(64),source_type:'user_supplied',
    usage:'command surface',license_status:'cleared',allowed_deviations:[],
  }]}));
  const result=spawnSync(process.execPath,[path.join(ROOT,'scripts/harness.mjs'),'quality-reference-set',requestPath],
    {cwd:ROOT,encoding:'utf8'});
  assert.equal(result.status,0,result.stderr||result.stdout);
  const envelope=JSON.parse(result.stdout.trim());
  assert.equal(envelope.ok,true);
  assert.equal(envelope.data.schema,'jianying-visual-reference-set/v1');
});
