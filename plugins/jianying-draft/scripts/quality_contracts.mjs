import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {canonical,fail,parseStrictJson,sha256,validateSchema} from './workflow_data.mjs';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const SCHEMA_FILES=new Map([
  ['jianying-creative-target/v1','creative-target.v1.schema.json'],
  ['jianying-quality-profile/v1','quality-profile.v1.schema.json'],
  ['jianying-evaluation-input/v1','evaluation-input.v1.schema.json'],
  ['jianying-evaluation-verdict/v1','evaluation-verdict.v1.schema.json'],
  ['jianying-revision-request/v1','revision-request.v1.schema.json'],
  ['jianying-iteration-policy/v1','iteration-policy.v1.schema.json'],
  ['jianying-evidence-bundle/v1','evidence-bundle.v1.schema.json'],
  ['jianying-visual-reference-set/v1','visual-reference-set.v1.schema.json'],
  ['jianying-comparative-evaluation-context/v1','comparative-evaluation-context.v1.schema.json'],
  ['jianying-macro-revision-request/v1','macro-revision-request.v1.schema.json'],
  ['jianying-retarget-proposal/v1','retarget-proposal.v1.schema.json'],
]);
const SCHEMAS=new Map([...SCHEMA_FILES].map(([id,file])=>[id,JSON.parse(fs.readFileSync(path.join(ROOT,'schemas',file),'utf8'))]));
const ACTIONS=new Set(['trim','reorder','replace_clip','adjust_volume','caption_edit','crop','scale','color_adjust','music_edit']);
const FORBIDDEN_KEYS=new Set(['command','script','handler','executable','approved','approval']);

const invalid=message=>fail('quality_contract_invalid',message);
const positiveInteger=(value,name,allowZero=false)=>{
  if(!Number.isSafeInteger(value) || (allowZero?value<0:value<=0)) invalid(`${name} must be a ${allowZero?'non-negative':'positive'} safe integer`);
};
const finiteRange=(value,name,minimum,maximum)=>{
  if(!Number.isFinite(value) || value<minimum || value>maximum) invalid(`${name} must be between ${minimum} and ${maximum}`);
};
const unique=(values,name)=>{
  if(new Set(values).size!==values.length) invalid(`${name} contains duplicates`);
};

function rejectExecutionClaims(value,location='$') {
  if(Array.isArray(value)) return value.forEach((item,index)=>rejectExecutionClaims(item,`${location}[${index}]`));
  if(!value || typeof value!=='object') return;
  for(const [key,item] of Object.entries(value)) {
    if(FORBIDDEN_KEYS.has(key)) invalid(`${location}.${key} is not allowed in a quality contract`);
    rejectExecutionClaims(item,`${location}.${key}`);
  }
}

function validateCreativeTarget(value) {
  positiveInteger(value.revision,'revision');
  positiveInteger(value.target_duration_us,'target_duration_us');
  unique(value.references.map(item=>item.reference_id),'reference IDs');
  unique(value.constraints.map(item=>item.constraint_id),'constraint IDs');
  unique(value.quality_profiles.map(item=>item.output_id),'quality profile outputs');
  rejectExecutionClaims(value);
}

function validateQualityProfile(value) {
  unique(value.dimensions.map(item=>item.dimension_id),'dimension IDs');
  for(const item of value.dimensions) {
    finiteRange(item.weight,`${item.dimension_id}.weight`,0,10);
    finiteRange(item.threshold,`${item.dimension_id}.threshold`,0,10);
  }
  for(const action of value.allowed_actions) if(!ACTIONS.has(action)) invalid(`unregistered quality action ${action}`);
  rejectExecutionClaims(value);
}

function validateEvaluationInput(value) {
  positiveInteger(value.revision,'revision');
  unique(value.artifacts.map(item=>item.artifact_id),'artifact IDs');
  unique(value.evidence.map(item=>item.evidence_id),'evidence IDs');
  const artifacts=new Set(value.artifacts.map(item=>item.artifact_id));
  const artifactById=new Map(value.artifacts.map(item=>[item.artifact_id,item]));
  for(const item of value.artifacts) positiveInteger(item.bytes,`${item.artifact_id}.bytes`,true);
  for(const item of value.evidence) if(!artifacts.has(item.artifact_id)) invalid(`unknown evidence artifact ${item.artifact_id}`);
  unique(value.content_review.languages.map(item=>item.language),'content review languages');
  for(const [kind,artifactType] of [['captions','captions'],['transcript','transcript']]) {
    const review=value.content_review[kind];
    if(review.status==='absent' && Object.hasOwn(review,'artifact_id')) invalid(`${kind} absent status cannot reference an artifact`);
    if(review.status!=='absent' && (!review.artifact_id || artifactById.get(review.artifact_id)?.type!==artifactType))
      invalid(`${kind} review must reference its declared artifact`);
  }
  const languageStatus=new Map(value.content_review.languages.map(item=>[item.language,item.status]));
  for(const item of value.evidence) {
    const artifact=artifactById.get(item.artifact_id);
    if(['captions','transcript'].includes(artifact.type)) {
      const review=value.content_review[artifact.type];
      if(review.status!=='confirmed' && item.role!=='context_only')
        invalid(`${item.evidence_id} cannot promote unconfirmed ${artifact.type} to ${item.role}`);
    }
    if(item.type==='language_review' && (!item.language || languageStatus.get(item.language)!=='confirmed'))
      invalid(`${item.evidence_id} references an unconfirmed language review`);
  }
  if(value.evaluator_scope.maximum_cost<0 || !Number.isFinite(value.evaluator_scope.maximum_cost)) invalid('maximum_cost must be non-negative');
  rejectExecutionClaims(value);
}

function validateEvaluationVerdict(value) {
  positiveInteger(value.revision,'revision');
  unique(value.evidence_refs,'evidence refs');
  unique(value.scores.map(item=>item.dimension_id),'score dimensions');
  unique(value.hard_gates.map(item=>item.rule_id),'hard gate IDs');
  const refs=new Set(value.evidence_refs);
  for(const score of value.scores) finiteRange(score.value,`${score.dimension_id}.value`,0,10);
  for(const item of [...value.hard_gates,...value.findings]) {
    for(const reference of item.evidence_refs) if(!refs.has(reference)) invalid(`unknown evidence reference ${reference}`);
  }
  for(const finding of value.findings) {
    if(!finding.time_range && !finding.artifact_ref) invalid('finding requires a time range or artifact reference');
    if(finding.time_range) {
      positiveInteger(finding.time_range.start_us,'finding start_us',true);
      positiveInteger(finding.time_range.end_us,'finding end_us');
      if(finding.time_range.end_us<=finding.time_range.start_us) invalid('finding time range must be non-empty');
    }
  }
  if(value.decision==='pass' && (value.hard_gates.some(item=>!item.passed) || value.findings.some(item=>['major','critical'].includes(item.severity))))
    invalid('pass cannot override a failed hard gate or unresolved major finding');
  rejectExecutionClaims(value);
}

function validateRevisionRequest(value) {
  positiveInteger(value.from_revision,'from_revision');
  positiveInteger(value.to_revision,'to_revision');
  if(value.to_revision!==value.from_revision+1) invalid('to_revision must immediately follow from_revision');
  unique(value.actions.map(item=>item.action_id),'action IDs');
  for(const action of value.actions) if(!ACTIONS.has(action.type)) invalid(`unregistered revision action ${action.type}`);
  rejectExecutionClaims(value);
}

function validateIterationPolicy(value) {
  positiveInteger(value.maximum_revisions,'maximum_revisions');
  positiveInteger(value.maximum_model_calls,'maximum_model_calls',true);
  if(!Number.isFinite(value.maximum_budget.amount) || value.maximum_budget.amount<0) invalid('maximum budget must be non-negative');
  if(!Number.isFinite(Date.parse(value.deadline))) invalid('deadline must be an ISO timestamp');
  finiteRange(value.minimum_material_improvement,'minimum_material_improvement',0,10);
  positiveInteger(value.repeated_finding_limit,'repeated_finding_limit');
  finiteRange(value.regression_tolerance,'regression_tolerance',0,10);
}

function validateEvidenceBundle(value) {
  positiveInteger(value.revision,'revision');
  unique(value.items.map(item=>item.evidence_id),'evidence IDs');
  for(const item of value.items) if(!Number.isFinite(Date.parse(item.observed_at))) invalid(`${item.evidence_id} has an invalid observed_at`);
  if(value.conclusion==='passed') {
    const passed=new Set(value.items.filter(item=>item.passed).map(item=>item.type));
    for(const type of ['structural','technical','creative']) if(!passed.has(type)) invalid(`passed bundle lacks ${type} evidence`);
    if(value.items.some(item=>!item.passed)) invalid('passed bundle contains failed evidence');
  }
}

function validateVisualReferenceSet(value) {
  positiveInteger(value.revision,'revision');
  unique(value.references.map(item=>item.reference_id),'visual reference IDs');
  for(const item of value.references) {
    unique(item.allowed_deviations,`${item.reference_id}.allowed_deviations`);
    if(item.time_range) {
      positiveInteger(item.time_range.start_us,`${item.reference_id}.start_us`,true);
      positiveInteger(item.time_range.end_us,`${item.reference_id}.end_us`);
      if(item.time_range.end_us<=item.time_range.start_us) invalid(`${item.reference_id} time range must be non-empty`);
    }
  }
  rejectExecutionClaims(value);
}

function validateComparativeEvaluationContext(value) {
  positiveInteger(value.revision,'revision');
  positiveInteger(value.previous.revision,'previous.revision');
  if(value.previous.revision!==value.revision-1) invalid('comparative revisions must be consecutive');
  unique(value.comparison_dimensions,'comparison dimensions');
  const expected=['absolute_quality','prior_delta','target_gap'];
  if([...value.comparison_dimensions].sort().join(',')!==expected.join(','))
    invalid('comparative context must cover absolute quality, target gap and prior delta');
  const allowedTools=new Set(['artifact.inspect','evidence.read','quality.profile.read']);
  if(!value.critic.fresh_context || value.critic.write_access ||
    value.critic.allowed_tools.some(tool=>!allowedTools.has(tool)))
    invalid('critic must be fresh and read-only');
  rejectExecutionClaims(value);
}

function validateMacroRevisionRequest(value) {
  positiveInteger(value.from_revision,'from_revision');
  positiveInteger(value.to_revision,'to_revision');
  if(value.to_revision!==value.from_revision+1) invalid('macro to_revision must immediately follow from_revision');
  unique(value.strategies,'macro strategies');
  unique(value.reason_codes,'macro reason codes');
  if(!value.maximum_once || value.required_approvals.length!==1 || value.required_approvals[0]!=='human_macro_revision')
    invalid('macro revision must be one-time and human approved');
  rejectExecutionClaims(value);
}

function validateRetargetProposal(value) {
  positiveInteger(value.from_revision,'from_revision');
  positiveInteger(value.to_revision,'to_revision');
  if(value.to_revision!==value.from_revision+1) invalid('retarget to_revision must immediately follow from_revision');
  if(value.from_target_digest===value.proposed_target_digest) invalid('retarget must change the target digest');
  unique(value.evidence_refs,'retarget evidence refs');
  if(value.required_approval!=='human_retarget' || value.status!=='proposed')
    invalid('retarget must remain proposed until exact human approval');
  rejectExecutionClaims(value);
}

const SEMANTIC_VALIDATORS=new Map([
  ['jianying-creative-target/v1',validateCreativeTarget],
  ['jianying-quality-profile/v1',validateQualityProfile],
  ['jianying-evaluation-input/v1',validateEvaluationInput],
  ['jianying-evaluation-verdict/v1',validateEvaluationVerdict],
  ['jianying-revision-request/v1',validateRevisionRequest],
  ['jianying-iteration-policy/v1',validateIterationPolicy],
  ['jianying-evidence-bundle/v1',validateEvidenceBundle],
  ['jianying-visual-reference-set/v1',validateVisualReferenceSet],
  ['jianying-comparative-evaluation-context/v1',validateComparativeEvaluationContext],
  ['jianying-macro-revision-request/v1',validateMacroRevisionRequest],
  ['jianying-retarget-proposal/v1',validateRetargetProposal],
]);

export function validateQualityContract(value) {
  if(!value || typeof value!=='object' || Array.isArray(value)) invalid('quality contract must be an object');
  const schema=SCHEMAS.get(value.schema);
  if(!schema) invalid(`unsupported quality contract schema ${String(value.schema)}`);
  try {validateSchema(value,schema);} catch(error) {invalid(error.message);}
  SEMANTIC_VALIDATORS.get(value.schema)(value);
  return {valid:true,schema:value.schema};
}

export function parseQualityContract(text,{maximumBytes=1024*1024}={}) {
  if(typeof text!=='string') invalid('quality contract must be UTF-8 JSON text');
  if(!Number.isSafeInteger(maximumBytes) || maximumBytes<=0) invalid('maximumBytes must be a positive safe integer');
  if(Buffer.byteLength(text,'utf8')>maximumBytes) fail('quality_contract_resource_limit',`quality contract exceeds ${maximumBytes} bytes`);
  const value=parseStrictJson(text);
  validateQualityContract(value);
  return value;
}

export function qualityContractDigest(value) {
  validateQualityContract(value);
  return sha256(canonical(value));
}

const factStatus=fact=>fact.source==='observed'&&fact.confirmed?'observed':
  ['user','human'].includes(fact.source)&&fact.confirmed?'user_confirmed':'inferred_pending_review';

function confirmedFact(brief,name,outputId) {
  const candidates=[`${name}:${outputId}`,name];
  return brief.facts.find(fact=>candidates.includes(fact.name) && fact.confirmed &&
    ['user','human','observed'].includes(fact.source) && typeof fact.source_ref==='string' && fact.source_ref.trim());
}

/** 从已经审查的简报和路由生成每个输出独立的创作目标；不授予任何执行权限。 */
export function buildCreativeTargets({brief,route,workflowId,profiles,references=[]}) {
  const notReady=message=>fail('quality_target_not_ready',message);
  if(!brief || brief.schema!=='jianying-creative-brief/v1' || !route || route.schema!=='jianying-open-route/v1' ||
    route.request_id!==brief.request_id || !Array.isArray(route.selected_scenes) || !route.selected_scenes.length)
    notReady('a reviewed route belonging to the creative brief is required');
  if(typeof workflowId!=='string' || !workflowId.trim()) notReady('workflow identity is required');
  if(typeof brief.intent!=='string' || !brief.intent.trim() || !Array.isArray(brief.output_intents) || !brief.output_intents.length)
    notReady('creative intent and at least one output are required');
  if(!Array.isArray(brief.facts) || !profiles || typeof profiles!=='object') notReady('confirmed facts and profiles are required');
  const rawConstraints=brief.facts.filter(fact=>['must_keep','must_avoid'].includes(fact.name));
  const constraints=rawConstraints.map((fact,index)=>({
    constraint_id:`constraint-${sha256(canonical({name:fact.name,value:fact.value,source_ref:fact.source_ref,index})).slice(0,16)}`,
    kind:fact.name,
    value:fact.value,
    source_status:factStatus(fact),
    source_ref:fact.source_ref,
  }));
  return brief.output_intents.map(output=>{
    const audience=confirmedFact(brief,'audience',output.id);
    const channel=confirmedFact(brief,'channel',output.id);
    const duration=confirmedFact(brief,'target_duration_us',output.id);
    const profile=profiles[output.id];
    if(!audience || !channel || !duration || !profile) notReady(`output ${output.id} lacks confirmed target facts or a locked profile`);
    const targetDuration=Number(duration.value);
    if(!Number.isSafeInteger(targetDuration) || targetDuration<=0) notReady(`output ${output.id} target duration is invalid`);
    const value={schema:'jianying-creative-target/v1',
      target_id:`target-${sha256(canonical({workflowId,output_id:output.id,profile})).slice(0,20)}`,
      workflow_id:workflowId,revision:1,narrative_goal:brief.intent,audience:audience.value,channel:channel.value,
      target_duration_us:targetDuration,references:structuredClone(references),constraints:structuredClone(constraints),
      quality_profiles:[{output_id:output.id,profile_id:profile.profile_id,version:profile.version,digest:profile.digest}],
      metadata:{'partme.request_id':brief.request_id,'partme.route_scenes':route.selected_scenes.map(scene=>scene.id).join(',')}};
    validateQualityContract(value);
    return value;
  });
}
