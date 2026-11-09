import path from 'node:path';
import {fail,canonical,sha256} from './workflow_data.mjs';
import {qualityContractDigest} from './quality_contracts.mjs';

const SAFE_MAX=Number.MAX_SAFE_INTEGER;

function validateCli(identity,required) {
  if(!identity || !/^\d+\.\d+\.\d+$/.test(identity.version??'') || !/^[a-f0-9]{64}$/.test(identity.sha256??'') ||
    identity.jobSchema!=='jianying-job/v2' || !Array.isArray(identity.capabilities))
    fail('cli_identity_invalid','a checksum-bound released CLI identity is required');
  const supported=new Set(identity.capabilities.filter(item=>item.status==='supported').map(item=>item.id));
  for(const capability of ['schema.job_v2','job.run',...required])
    if(!supported.has(capability)) fail('missing_capability',`${capability} is not supported`);
}

function validateLedger(ledger) {
  const result=new Map();
  for(const asset of ledger) {
    if(asset.state!=='verified' || !/^[a-f0-9]{64}$/.test(asset.sha256??'') ||
      !Number.isSafeInteger(asset.bytes) || asset.bytes<0 || !Number.isSafeInteger(asset.duration_us) || asset.duration_us<=0 ||
      !Array.isArray(asset.streams)) fail('asset_not_verified',`${asset.asset_id??'asset'} lacks verified media facts`);
    if(result.has(asset.asset_id)) fail('asset_not_verified',`duplicate ${asset.asset_id}`);
    result.set(asset.asset_id,asset);
  }
  return result;
}

function validateResourceAcquisitions(acquisitions) {
  if(!Array.isArray(acquisitions)) fail('official_resource_not_ready','resource acquisitions must be an array');
  const result=new Map();
  for(const acquisition of acquisitions) {
    const receipt=acquisition?.receipt,selected=acquisition?.selected,file=receipt?.identity?.file;
    if(acquisition?.schema!=='jianying-native-resource-acquisition/v1' || acquisition.state!=='ready' ||
      typeof acquisition.request_id!=='string' || !acquisition.request_id.trim() || result.has(acquisition.request_id) ||
      selected?.resource_id!==receipt?.asset_id || typeof selected?.domain!=='string' ||
      receipt?.schema_version!=='jianying-official-resource-receipt/v1' || receipt?.identity?.kind!=='downloaded_file' ||
      typeof file?.path!=='string' || !file.path.trim() || !/^[a-f0-9]{64}$/.test(file.sha256??'') ||
      !Number.isSafeInteger(file.byte_length) || file.byte_length<0 || acquisition.cli?.register?.status!=='registered' ||
      acquisition.cli?.preflight?.status!=='ready')
      fail('official_resource_not_ready',`${acquisition?.request_id??'resource'} lacks a CLI-verified acquisition receipt`);
    result.set(acquisition.request_id,acquisition);
  }
  return result;
}

function compileOutput(plan,output,decision,assets,resourceAcquisitions) {
  let cursor=0;
  const materials=[],segments=[];
  const placements=[];
  for(const [index,clip] of decision.clips.entries()) {
    const asset=assets.get(clip.asset_id);
    if(!asset) fail('asset_not_verified',`unknown verified asset ${clip.asset_id}`);
    if(Object.hasOwn(clip,'speed') && clip.speed!==1) fail('unsupported_edit_mapping','only constant 1x speed is supported');
    if(Object.hasOwn(clip,'effects') || Object.hasOwn(clip,'transition') || Object.hasOwn(clip,'multicam'))
      fail('unsupported_edit_mapping','effects, transitions, and multicamera mappings are not supported');
    if(!Number.isSafeInteger(clip.in_us) || !Number.isSafeInteger(clip.out_us) || clip.in_us<0 ||
      clip.out_us<=clip.in_us || clip.out_us>asset.duration_us || clip.out_us>SAFE_MAX)
      fail('media_range_invalid',`${clip.asset_id} range is not a valid half-open source interval`);
    const duration=clip.out_us-clip.in_us;
    const targetStart=Object.hasOwn(clip,'target_start_us')?clip.target_start_us:cursor;
    if(!Number.isSafeInteger(targetStart) || targetStart<0 || targetStart>SAFE_MAX-duration || targetStart<cursor)
      fail('media_range_invalid',`${clip.asset_id} target placement is invalid or overlaps an earlier clip`);
    const materialId=`material-${index+1}`;
    materials.push({type:'video',id:materialId,path:path.resolve(asset.path)});
    segments.push({type:'video',id:`segment-${index+1}`,range:{start_us:targetStart,duration_us:duration},
      material_id:materialId,source_range:{start_us:clip.in_us,duration_us:duration},speed:1,volume:1});
    placements.push({asset_id:clip.asset_id,source_start_us:clip.in_us,source_end_us:clip.out_us,target_start_us:targetStart});
    cursor=targetStart+duration;
  }
  if(!segments.length) fail('selection_required',`${output.output_id} has no clips`);
  const captionSegmentsByLanguage=new Map(),captionReviews=[];
  for(const caption of decision.captions??[]) {
    if(caption.review_status!=='confirmed') continue;
    if(typeof caption.text!=='string' || !caption.text.trim() || !Number.isSafeInteger(caption.in_us) ||
      !Number.isSafeInteger(caption.out_us) || caption.in_us<0 || caption.out_us<=caption.in_us)
      fail('media_range_invalid',`${caption.caption_id??'caption'} has an invalid interval or text`);
    for(const placement of placements.filter(item=>item.asset_id===caption.asset_id)) {
      const intersectionStart=Math.max(caption.in_us,placement.source_start_us);
      const intersectionEnd=Math.min(caption.out_us,placement.source_end_us);
      if(intersectionEnd<=intersectionStart) continue;
      const targetStart=placement.target_start_us+(intersectionStart-placement.source_start_us);
      const language=caption.language??'und';
      const captionSegments=captionSegmentsByLanguage.get(language)??[];
      captionSegments.push({type:'text',id:`caption-${caption.caption_id}`,range:{start_us:targetStart,
        duration_us:intersectionEnd-intersectionStart},text:caption.text});
      captionSegmentsByLanguage.set(language,captionSegments);
      captionReviews.push({caption_id:caption.caption_id,language:caption.language,review_status:caption.review_status});
    }
  }
  const canvas=output.canvas??{width:1920,height:1080,frame_rate:{numerator:30,denominator:1}};
  if(!Number.isSafeInteger(canvas.width) || !Number.isSafeInteger(canvas.height) || canvas.width<16 || canvas.height<16 ||
    !Number.isSafeInteger(canvas.frame_rate?.numerator) || !Number.isSafeInteger(canvas.frame_rate?.denominator) ||
    canvas.frame_rate.numerator<=0 || canvas.frame_rate.denominator<=0)
    fail('unsupported_edit_mapping','output canvas is invalid');
  const tracks=[{id:'video-1',kind:'video',segments}];
  for(const [index,[language,captionSegments]] of [...captionSegmentsByLanguage.entries()].sort(([left],[right])=>left.localeCompare(right)).entries()) {
    captionSegments.sort((left,right)=>left.range.start_us-right.range.start_us||left.id.localeCompare(right.id));
    tracks.push({id:`captions-${index+1}-${language}`,kind:'text',segments:captionSegments});
  }
  for(const [index,placement] of (decision.official_resources??[]).entries()) {
    const acquisition=resourceAcquisitions.get(placement.request_id);
    if(!acquisition) fail('official_resource_not_ready',`${placement.request_id??'resource'} has no verified acquisition`);
    if(acquisition.selected.domain!=='music')
      fail('unsupported_edit_mapping',`${acquisition.selected.domain} official resource Job mapping is not implemented`);
    if(!Number.isSafeInteger(placement.start_us) || placement.start_us<0 || !Number.isSafeInteger(placement.duration_us) ||
      placement.duration_us<=0 || placement.start_us>SAFE_MAX-placement.duration_us || !Number.isFinite(placement.volume) ||
      placement.volume<0 || placement.volume>1) fail('media_range_invalid',`${placement.request_id} placement is invalid`);
    const materialId=`official-material-${index+1}`;
    materials.push({type:'audio',id:materialId,path:path.resolve(acquisition.receipt.identity.file.path)});
    tracks.push({id:`official-audio-${index+1}`,kind:'audio',segments:[{type:'audio',id:`official-segment-${index+1}`,
      range:{start_us:placement.start_us,duration_us:placement.duration_us},material_id:materialId,
      source_range:{start_us:0,duration_us:placement.duration_us},speed:1,volume:placement.volume}]});
  }
  return {job:{schema:'jianying-job/v2',operation:'create',project:{type:'new',project:{name:`${plan.workflow_id}-${output.output_id}`,
    width:canvas.width,height:canvas.height,frame_rate:canvas.frame_rate,timeline:{tracks},materials}}},captionReviews};
}

export function compileWorkflow({plan,assetLedger,decisions,cliIdentity,outputRoot,resourceAcquisitions=[]}) {
  if(plan?.schema!=='jianying-workflow-plan/v1') fail('workflow_plan_invalid','expected jianying-workflow-plan/v1');
  validateCli(cliIdentity,plan.tool_requirements?.capabilities??[]);
  const assets=validateLedger(assetLedger);
  const acquiredResources=validateResourceAcquisitions(resourceAcquisitions);
  const outputIds=new Set(plan.outputs.map(output=>output.output_id));
  const logicalTargets=new Set();
  const sourcePaths=new Set([...assets.values()].map(asset=>path.resolve(asset.path)));
  for(const output of plan.outputs) {
    if(output.derived_from && !outputIds.has(output.derived_from))
      fail('output_isolation_invalid',`${output.output_id} derives from unknown output ${output.derived_from}`);
    const target=output.target?.logical_path;
    if(typeof target!=='string' || !target.trim() || logicalTargets.has(target) || sourcePaths.has(path.resolve(target)))
      fail('output_isolation_invalid',`${output.output_id} does not have an isolated output target`);
    logicalTargets.add(target);
  }
  const byOutput=new Map(decisions.map(decision=>[decision.output_id,decision]));
  const missing=plan.outputs.filter(output=>!byOutput.has(output.output_id));
  const planDigest=sha256(canonical(plan));
  if(missing.length) return {schema:'jianying-workflow-compilation/v1',plan_digest:planDigest,can_compile:false,
    can_execute:false,blockers:missing.map(output=>({code:'selection_required',output_id:output.output_id})),job_bindings:[],receipt:null};
  const bindings=plan.outputs.map(output=>{
    const compiled=compileOutput(plan,output,byOutput.get(output.output_id),assets,acquiredResources),job=compiled.job;
    const outputPath=outputRoot?path.resolve(outputRoot,output.output_id):output.target.logical_path;
    return {output_id:output.output_id,purpose:output.purpose,logical_output_path:output.target.logical_path,
      output_path:outputPath,derived_from:output.derived_from??null,caption_reviews:compiled.captionReviews,
      blockers:structuredClone(output.blockers??[]),job,
      job_digest:sha256(canonical(job))};
  });
  const semantic={plan_digest:planDigest,assets:[...assets.values()].map(asset=>({asset_id:asset.asset_id,sha256:asset.sha256,
      duration_us:asset.duration_us,streams:asset.streams})),official_resources:[...acquiredResources.values()].map(item=>({
      request_id:item.request_id,asset_id:item.receipt.asset_id,domain:item.selected.domain,sha256:item.receipt.identity.file.sha256})),
    decisions,outputs:plan.outputs.map(output=>({output_id:output.output_id,
      purpose:output.purpose,target:output.target.logical_path}))};
  const execution={semantic,bindings:bindings.map(binding=>({output_id:binding.output_id,output_path:binding.output_path,
      job_digest:binding.job_digest})),paths:[...assets.values()].map(asset=>path.resolve(asset.path)),
    official_resource_paths:[...acquiredResources.values()].map(item=>path.resolve(item.receipt.identity.file.path))};
  const qualityContracts=plan.creative_targets?{workflow_id:plan.workflow_id,revision:plan.revision,
    target_digests:plan.creative_targets.map(qualityContractDigest),
    profile_digests:plan.creative_targets.map(target=>target.quality_profiles[0].digest),
    iteration_policy_digest:qualityContractDigest(plan.iteration_policy)}:undefined;
  const receipt={schema:'jianying-compilation-receipt/v1',compiler:{name:'jianying-edit-workflow-compiler',version:'1'},
    plan_digest:planDigest,catalog_ref:plan.catalog_ref,cli:{version:cliIdentity.version,sha256:cliIdentity.sha256,
      job_schema:cliIdentity.jobSchema},semantic_digest:sha256(canonical(semantic)),execution_digest:sha256(canonical(execution)),
    official_resources:semantic.official_resources,
    ...(qualityContracts?{quality_contracts:qualityContracts}:{}),job_digests:bindings.map(binding=>binding.job_digest),warnings:[]};
  return {schema:'jianying-workflow-compilation/v1',plan_digest:planDigest,can_compile:true,can_execute:false,
    blockers:[{code:'approval_required'}],job_bindings:bindings,receipt};
}
