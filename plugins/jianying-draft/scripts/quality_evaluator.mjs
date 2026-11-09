import {canonical,fail,sha256} from './workflow_data.mjs';
import {qualityContractDigest,validateQualityContract} from './quality_contracts.mjs';

const EVALUATOR_TYPES=new Set(['human','model','deterministic']);
const REVIEW_FIELDS=new Set(['decision','evidence_refs','scores','hard_gates','findings','limitations']);
const RESULT_FIELDS=new Set([...REVIEW_FIELDS,'schema','workflow_id','revision','output_id','input_digest','evaluator','metadata']);

function validateIdentity(identity) {
  if(!identity || !EVALUATOR_TYPES.has(identity.type) ||
    ['provider','model','version'].some(key=>typeof identity[key]!=='string' || !identity[key].trim()))
    fail('evaluator_invalid','evaluator identity must be an independent human, model or deterministic validator');
}

function requiredAudioEvidence(profile,input) {
  if(!profile.dimensions.some(dimension=>dimension.evidence_types.includes('audio_metrics'))) return {required:false,refs:[]};
  const artifacts=new Map(input.artifacts.map(item=>[item.artifact_id,item]));
  const media=input.evidence.filter(item=>item.type==='media_quality' && item.role==='technical' &&
    item.evidence_id===`media-quality-${item.digest.slice(0,20)}`);
  const refs=input.evidence.filter(item=>{
    const artifact=artifacts.get(item.artifact_id);
    if(item.type!=='audio_metrics' || item.role!=='technical' ||
      !['proxy_media','native_media'].includes(artifact?.type) || artifact.bytes<=0) return false;
    return media.some(source=>{
      if(source.artifact_id!==item.artifact_id) return false;
      const digest=sha256(canonical({media_quality_digest:source.digest,
        artifact_digest:artifact.digest,type:'audio_metrics'}));
      return item.digest===digest && item.evidence_id===`audio-metrics-${digest.slice(0,20)}`;
    });
  }).map(item=>item.evidence_id);
  return {required:true,refs};
}

function verdictEnvelope(identity,input,result) {
  if(!result || typeof result!=='object' || Array.isArray(result)) fail('evaluator_invalid','evaluator must return a structured result');
  return {schema:'jianying-evaluation-verdict/v1',workflow_id:input.workflow_id,revision:input.revision,output_id:input.output_id,
    input_digest:qualityContractDigest(input),evaluator:structuredClone(identity),decision:result.decision,
    evidence_refs:structuredClone(result.evidence_refs??[]),scores:structuredClone(result.scores??[]),
    hard_gates:structuredClone(result.hard_gates??[]),findings:structuredClone(result.findings??[]),
    limitations:structuredClone(result.limitations??[]),metadata:{}};
}

/** 执行只读评估适配器并复核身份和输入绑定；不向适配器提供草稿写权限。 */
export function runEvaluator({adapter,input,profile,comparativeContext,context={}}) {
  validateQualityContract(input); validateQualityContract(profile);
  if(input.schema!=='jianying-evaluation-input/v1' || profile.schema!=='jianying-quality-profile/v1')
    fail('evaluator_invalid','evaluation input and quality profile are required');
  validateIdentity(adapter?.identity);
  if(typeof adapter.evaluate!=='function') fail('evaluator_invalid','evaluator adapter has no evaluate function');
  if(comparativeContext!==undefined) {
    validateQualityContract(comparativeContext);
    if(comparativeContext.schema!=='jianying-comparative-evaluation-context/v1' ||
      comparativeContext.workflow_id!==input.workflow_id || comparativeContext.output_id!==input.output_id ||
      comparativeContext.revision!==input.revision ||
      comparativeContext.current.evaluation_input_digest!==qualityContractDigest(input) ||
      comparativeContext.profile_digest!==input.profile_digest)
      fail('evaluation_binding_mismatch','comparative context is not bound to the evaluation input');
  }
  const evaluatorContext=structuredClone(context);
  if(comparativeContext!==undefined) evaluatorContext.comparative=structuredClone(comparativeContext);
  const raw=adapter.evaluate({input:structuredClone(input),profile:structuredClone(profile),context:evaluatorContext});
  for(const key of Object.keys(raw??{})) if(!RESULT_FIELDS.has(key))
    fail('quality_contract_invalid',`evaluator result contains forbidden field ${key}`);
  const verdict=verdictEnvelope(adapter.identity,input,raw);
  validateQualityContract(verdict);
  if(verdict.workflow_id!==input.workflow_id || verdict.revision!==input.revision || verdict.output_id!==input.output_id ||
    verdict.input_digest!==qualityContractDigest(input)) fail('evaluation_binding_mismatch','evaluation verdict is not bound to its input');
  const evidenceById=new Map(input.evidence.map(item=>[item.evidence_id,item]));
  if(verdict.evidence_refs.some(reference=>!evidenceById.has(reference)))
    fail('evaluation_binding_mismatch','evaluation verdict cites evidence outside its input');
  if(verdict.decision==='pass' && verdict.evidence_refs.some(reference=>evidenceById.get(reference).role==='context_only'))
    fail('evaluation_binding_mismatch','context-only evidence cannot support a pass decision');
  if(verdict.decision==='pass' && requiredAudioEvidence(profile,input).required &&
    requiredAudioEvidence(profile,input).refs.length===0)
    fail('evaluation_evidence_insufficient','profile requires technical audio metrics evidence before a pass decision');
  return verdict;
}

export function createManualEvaluator({reviewerId,version}) {
  const identity={type:'human',provider:'manual',model:reviewerId,version}; validateIdentity(identity);
  return {identity,evaluate:({context})=>{
    const review=context.review;
    if(!review || typeof review!=='object' || Array.isArray(review)) fail('evaluator_invalid','manual review facts are required');
    for(const key of Object.keys(review)) if(!REVIEW_FIELDS.has(key)) fail('quality_contract_invalid',`manual review contains forbidden field ${key}`);
    return structuredClone(review);
  }};
}

export function createTechnicalEvaluator({version}) {
  const identity={type:'deterministic',provider:'local',model:'technical-evidence',version}; validateIdentity(identity);
  return {identity,evaluate:({input,profile})=>{
    const evidenceRefs=input.evidence.map(item=>item.evidence_id);
    const empty=input.artifacts.filter(item=>item.bytes===0);
    const audio=requiredAudioEvidence(profile,input),audioMissing=audio.required && audio.refs.length===0;
    const passed=empty.length===0 && !audioMissing;
    return {decision:passed?'pass':'blocked',evidence_refs:evidenceRefs,
      scores:[{dimension_id:'technical_integrity',value:passed?10:0,passed}],
      hard_gates:[{rule_id:'artifact_non_empty',passed:empty.length===0,evidence_refs:evidenceRefs},
        ...(audio.required?[{rule_id:'required_audio_evidence',passed:!audioMissing,evidence_refs:audio.refs.length?audio.refs:evidenceRefs}]:[])],
      findings:[...empty.map(item=>({code:'artifact_empty',severity:'critical',output_id:input.output_id,artifact_ref:item.artifact_id,
        observation:`artifact ${item.artifact_id} is empty`,rule_id:'artifact_non_empty',evidence_refs:evidenceRefs,
        suggested_action:'replace_clip'})),...(audioMissing?[{code:'audio_evidence_missing',severity:'major',output_id:input.output_id,
        artifact_ref:input.artifacts.find(item=>['proxy_media','native_media'].includes(item.type))?.artifact_id??input.artifacts[0].artifact_id,
        observation:'profile requires technical audio metrics, but no verified audio evidence is bound to a media artifact',
        rule_id:'required_audio_evidence',evidence_refs:evidenceRefs,suggested_action:'music_edit'}]:[])],
      limitations:['deterministic evaluator does not judge narrative, audio-visual coherence or visual taste']};
  }};
}
