import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {fail,canonical,sha256,validateSchema} from './workflow_data.mjs';
import {validateQualityContract} from './quality_contracts.mjs';
import {resolveQualityLoopGate,validateQualityLoopGate} from './quality_feature_gate.mjs';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const PLAN_SCHEMA=JSON.parse(fs.readFileSync(path.join(ROOT,'schemas/workflow-plan.v1.schema.json'),'utf8'));

// 目录只声明语义需求；实际步骤合同固定在插件代码中。
const STEP_REGISTRY=new Map([
  ['editorial_selection',{version:'1',executor:'human',input:'AssetLedger',output:'Selection',sideEffect:'none'}],
  ['draft_edit',{version:'1',executor:'cli',input:'EditDecision',output:'JobBundle',sideEffect:'draft_write'}],
  ['caption_mapping',{version:'1',executor:'cli',input:'EditDecision',output:'JobBundle',sideEffect:'draft_write'}],
  ['asr',{version:'1',executor:'model',input:'Media',output:'Transcript',sideEffect:'external'}],
  ['tts',{version:'1',executor:'model',input:'Text',output:'Media',sideEffect:'external'}],
  ['proxy_render',{version:'1',executor:'cli',input:'Draft',output:'ProxyMedia',sideEffect:'local_write',requiredCapabilities:['render.proxy']}],
  ['technical_validation',{version:'1',executor:'plugin',input:'ProxyMedia',output:'TechnicalEvidence',sideEffect:'none'}],
  ['creative_evaluation',{version:'1',executor:'model',input:'EvaluationInput',output:'EvaluationVerdict',sideEffect:'external',
    requiredCapabilities:['model.video.evaluate'],requiredApprovals:['external_service']}],
  ['human_review',{version:'1',executor:'human',input:'EvaluationInput',output:'ReviewDecision',sideEffect:'none'}],
  ['revision_planning',{version:'1',executor:'plugin',input:'EvaluationVerdict',output:'RevisionRequest',sideEffect:'none'}],
  ['native_export',{version:'1',executor:'cli',input:'Draft',output:'NativeMedia',sideEffect:'native_export',
    requiredCapabilities:['render.native'],requiredApprovals:['human_confirmation']}],
  ['delivery_validation',{version:'1',executor:'plugin',input:'EvidenceBundle',output:'DeliveryDecision',sideEffect:'none'}],
  ['native_resource_search',{version:'1',executor:'plugin',input:'NativeResourceQuery',output:'ResourceCandidateSet',sideEffect:'none'}],
  ['native_resource_filter',{version:'1',executor:'plugin',input:'ResourceCandidateSet',output:'FilteredResourceCandidateSet',sideEffect:'none'}],
  ['native_resource_acquire',{version:'1',executor:'plugin',input:'FilteredResourceCandidateSet',output:'ResourceReceipt',
    sideEffect:'resource_download',requiredCapabilities:['media.official_resource']}],
  ['native_resource_apply',{version:'1',executor:'cli',input:'ResourceReceipt',output:'NativeActionEvidence',
    sideEffect:'draft_write',requiredCapabilities:['media.official_resource_apply'],requiredApprovals:['human_confirmation']}],
  ['native_resource_remove',{version:'1',executor:'cli',input:'NativeActionEvidence',output:'NativeActionEvidence',sideEffect:'draft_write'}],
  ['native_resource_inspect',{version:'1',executor:'cli',input:'NativeActionEvidence',output:'NativeActionEvidence',sideEffect:'none'}],
  ['native_resource_recover',{version:'1',executor:'cli',input:'NativeActionEvidence',output:'NativeActionEvidence',sideEffect:'draft_write'}],
  ['native_draft_control',{version:'1',executor:'cli',input:'NativeControlRequest',output:'NativeActionEvidence',sideEffect:'draft_write'}],
  ['native_runtime_control',{version:'1',executor:'plugin',input:'NativeControlRequest',output:'RuntimeControlEvidence',sideEffect:'native_control'}],
  ['native_accessibility_control',{version:'1',executor:'plugin',input:'NativeControlRequest',output:'RuntimeControlEvidence',sideEffect:'native_control'}],
  ['native_visual_control',{version:'1',executor:'plugin',input:'NativeControlRequest',output:'RuntimeControlEvidence',sideEffect:'native_control'}],
  ['smart_package_preview',{version:'1',executor:'plugin',input:'SmartPackageRequest',output:'SmartPackageProposal',sideEffect:'none'}],
  ['smart_package_review',{version:'1',executor:'human',input:'SmartPackageProposal',output:'SmartPackageApproval',sideEffect:'none'}],
  ['smart_package_apply',{version:'1',executor:'plugin',input:'SmartPackageApproval',output:'SmartPackageEvidence',
    sideEffect:'composite_write',requiredCapabilities:['runtime.smart_package'],requiredApprovals:['human_confirmation']}],
  ['smart_package_verify',{version:'1',executor:'plugin',input:'SmartPackageEvidence',output:'SmartPackageEvidence',sideEffect:'none'}],
  ['digital_human_inventory',{version:'1',executor:'plugin',input:'DigitalHumanRequest',output:'DigitalHumanSelection',sideEffect:'none'}],
  ['digital_human_preview',{version:'1',executor:'plugin',input:'DigitalHumanSelection',output:'DigitalHumanPreview',sideEffect:'none'}],
  ['digital_human_approve',{version:'1',executor:'human',input:'DigitalHumanPreview',output:'DigitalHumanApproval',sideEffect:'none'}],
  ['digital_human_submit',{version:'1',executor:'plugin',input:'DigitalHumanApproval',output:'DigitalHumanTask',
    sideEffect:'remote_generation',requiredCapabilities:['runtime.digital_human'],requiredApprovals:['human_confirmation','external_service']}],
  ['digital_human_resume',{version:'1',executor:'plugin',input:'DigitalHumanTask',output:'DigitalHumanTask',sideEffect:'none'}],
  ['digital_human_verify',{version:'1',executor:'plugin',input:'DigitalHumanTask',output:'DigitalHumanEvidence',sideEffect:'none'}],
]);

const stepId=(type,index)=>`step-${String(index+1).padStart(2,'0')}-${type.replaceAll('_','-')}`;

export function buildWorkflowPlan(brief,route) {
  if(route.schema!=='jianying-open-route/v1' || route.request_id!==brief.request_id)
    fail('workflow_plan_invalid','route and brief do not belong to the same request');
  if(!route.selected_scenes.length) fail('workflow_plan_invalid','a reviewed scene selection is required');
  const requirements=route.recipes.flatMap(recipe=>recipe.step_requirements.filter(item=>item.required));
  if(brief.output_intents.some(output=>output.delivery!=='plan') && !requirements.some(item=>item.type==='draft_edit')) {
    requirements.push({type:'draft_edit',preconditions:['selection confirmed'],capability_ids:[
      'timeline.edit','timeline.volume','timeline.audio_fade'],human_requirements:[],external_requirements:[]});
  }
  const steps=requirements.map((requirement,index)=>{
    const registered=STEP_REGISTRY.get(requirement.type);
    if(!registered) fail('unsupported_step_type',requirement.type);
    const id=stepId(requirement.type,index);
    return {id,type:requirement.type,type_version:registered.version,executor:registered.executor,
      depends_on:index?[stepsId(requirements,index-1)]:[],
      inputs:[{port:'input',data_type:registered.input,artifact_ref:index?`artifact-${index}`:'asset-ledger'}],
      outputs:[{port:'output',data_type:registered.output,artifact_ref:`artifact-${index+1}`}],
      preconditions:[...requirement.preconditions],capabilities:[...requirement.capability_ids],
      approval_requirements:[...requirement.human_requirements.map(value=>({type:'human_confirmation',scope:value})),
        ...requirement.external_requirements.map(value=>({type:'external_service',scope:value}))],
      timeout_ms:300000,budget:{currency:'CNY',maximum:0},retry:{maximum_attempts:1,backoff_ms:0},
      reconcile:{strategy:registered.sideEffect==='none'?'recompute':'inspect_before_retry'},
      validator:{type:'artifact',version:'1',evidence_level:'structural'}};
  });
  const capabilities=[...new Set(steps.flatMap(step=>step.capabilities))].sort();
  const risks=[...new Set(requirements.map(item=>STEP_REGISTRY.get(item.type).sideEffect).filter(value=>value!=='none'))]
    .map(type=>({type,approval_required:true}));
  const outputs=brief.output_intents.map(output=>({output_id:output.id,purpose:output.purpose,format:output.format,
    delivery:output.delivery,target:{logical_path:`outputs/${output.id}`},proof_requirements:['structural']}));
  const plan={schema:'jianying-workflow-plan/v1',workflow_id:`workflow-${sha256(canonical({request_id:brief.request_id,
      catalog:route.catalog_ref.digest,outputs:brief.output_intents})).slice(0,20)}`,revision:1,
    catalog_ref:route.catalog_ref,tool_requirements:{capabilities},brief:structuredClone(brief),
    assets:(brief.media??[]).map((media,index)=>({asset_id:`asset-${index+1}`,path:media,state:'declared'})),
    route:{kind:route.route,scene_ids:route.selected_scenes.map(scene=>scene.id),recipe_ids:route.recipes.map(recipe=>recipe.id),
      readiness:route.readiness},outputs,steps,limits:{maximum_revisions:3,maximum_budget:{currency:'CNY',amount:0}},
    risk_requirements:risks,proof_requirements:[{level:'structural',required:true}],metadata:{'partme.provenance':route.provenance}};
  validateWorkflowPlan(plan);
  return plan;
}

function stepsId(requirements,index) {return stepId(requirements[index].type,index);}

export function validateWorkflowPlan(plan) {
  try {validateSchema(plan,PLAN_SCHEMA);} catch(error) {fail('workflow_plan_invalid',error.message);}
  if(!Number.isSafeInteger(plan.revision) || plan.revision<1) fail('workflow_plan_invalid','revision must be a positive safe integer');
  if(Object.hasOwn(plan,'creative_targets') || Object.hasOwn(plan,'iteration_policy')) {
    if(!Array.isArray(plan.creative_targets) || !plan.iteration_policy)
      fail('workflow_plan_invalid','quality loop requires creative targets and an iteration policy together');
    try {validateQualityLoopGate(plan.metadata?.['partme.quality_loop_gate']);}
    catch(error) {
      if(error?.code?.startsWith('quality_feature_')) throw error;
      fail('quality_feature_gate_invalid','quality loop gate record is required');
    }
    try {
      validateQualityContract(plan.iteration_policy);
      for(const target of plan.creative_targets) validateQualityContract(target);
    } catch(error) {fail('workflow_plan_invalid',error.message);}
    const outputs=new Set(plan.outputs.map(output=>output.output_id));
    const targetOutputs=[];
    for(const target of plan.creative_targets) {
      if(target.workflow_id!==plan.workflow_id || target.revision!==plan.revision)
        fail('workflow_plan_invalid','creative target does not belong to this workflow revision');
      if(target.quality_profiles.length!==1) fail('workflow_plan_invalid','each creative target must bind one output profile');
      targetOutputs.push(target.quality_profiles[0].output_id);
    }
    if(new Set(targetOutputs).size!==targetOutputs.length || targetOutputs.length!==outputs.size || targetOutputs.some(id=>!outputs.has(id)))
      fail('workflow_plan_invalid','creative targets must cover every output exactly once');
  }
  if(new Set(plan.outputs.map(output=>output.output_id)).size!==plan.outputs.length)
    fail('workflow_graph_invalid','duplicate output ID');
  const ids=new Set(); const producers=new Set();
  for(const step of plan.steps) {
    if(!step || typeof step!=='object' || Object.hasOwn(step,'handler') || Object.hasOwn(step,'script') || Object.hasOwn(step,'command'))
      fail('unsupported_step_type','steps cannot provide handlers, scripts or commands');
    const registered=STEP_REGISTRY.get(step.type);
    if(!registered || step.type_version!==registered.version || step.executor!==registered.executor)
      fail('unsupported_step_type',`unregistered step ${step.type}`);
    if(!Number.isSafeInteger(step.timeout_ms) || step.timeout_ms<=0 ||
      !Array.isArray(step.preconditions) || step.preconditions.some(value=>typeof value!=='string' || !value.trim()) ||
      !Array.isArray(step.capabilities) || step.capabilities.some(value=>typeof value!=='string' || !value.trim()) ||
      new Set(step.capabilities).size!==step.capabilities.length ||
      !Array.isArray(step.approval_requirements) || step.approval_requirements.some(item=>!item || typeof item!=='object' ||
        !['human_confirmation','external_service'].includes(item.type) || typeof item.scope!=='string' || !item.scope.trim()) ||
      !step.budget || typeof step.budget.currency!=='string' || !step.budget.currency.trim() ||
      !Number.isFinite(step.budget.maximum) || step.budget.maximum<0 ||
      !step.retry || !Number.isSafeInteger(step.retry.maximum_attempts) || step.retry.maximum_attempts<1 ||
      !Number.isSafeInteger(step.retry.backoff_ms) || step.retry.backoff_ms<0 ||
      !step.reconcile || typeof step.reconcile.strategy!=='string' ||
      !step.validator || typeof step.validator.type!=='string' || !step.validator.type.trim() ||
      typeof step.validator.version!=='string' || !step.validator.version.trim() ||
      typeof step.validator.evidence_level!=='string' || !step.validator.evidence_level.trim())
      fail('workflow_plan_invalid',`step ${step.id} has an incomplete execution contract`);
    for(const capability of registered.requiredCapabilities??[])
      if(!step.capabilities.includes(capability)) fail('workflow_plan_invalid',`step ${step.id} lacks capability ${capability}`);
    const approvalTypes=new Set(step.approval_requirements.map(item=>item.type));
    for(const approval of registered.requiredApprovals??[])
      if(!approvalTypes.has(approval)) fail('workflow_plan_invalid',`step ${step.id} lacks ${approval} approval requirement`);
    if(registered.sideEffect!=='none' && step.reconcile.strategy!=='inspect_before_retry')
      fail('workflow_plan_invalid',`step ${step.id} must inspect side effects before retry`);
    for(const input of step.inputs??[]) {
      if(typeof input.port!=='string' || typeof input.artifact_ref!=='string' || input.data_type!==registered.input)
        fail('workflow_plan_invalid',`step ${step.id} has an invalid input port`);
    }
    if(ids.has(step.id)) fail('workflow_graph_invalid',`duplicate step ${step.id}`); ids.add(step.id);
    for(const output of step.outputs??[]) {
      if(producers.has(output.artifact_ref)) fail('workflow_graph_invalid',`duplicate producer ${output.artifact_ref}`);
      if(typeof output.port!=='string' || typeof output.artifact_ref!=='string' || output.data_type!==registered.output)
        fail('workflow_plan_invalid',`step ${step.id} has an invalid output port`);
      producers.add(output.artifact_ref);
    }
  }
  const visiting=new Set(),visited=new Set(),byId=new Map(plan.steps.map(step=>[step.id,step]));
  for(const step of plan.steps) {
    if(step.type.startsWith('native_resource_')) {
      if(!step.resource_query || step.resource_query.schema!=='jianying-native-resource-query/v1' ||
        typeof step.resource_query.request_id!=='string' || !step.resource_query.request_id.trim())
        fail('workflow_plan_invalid',`step ${step.id} lacks its native resource query`);
    }
    if(step.type==='native_resource_filter' && !step.depends_on.some(id=>byId.get(id)?.type==='native_resource_search'))
      fail('workflow_graph_invalid',`step ${step.id} must depend on native resource search`);
    if(step.type==='native_resource_acquire' && !step.depends_on.some(id=>byId.get(id)?.type==='native_resource_filter'))
      fail('workflow_graph_invalid',`step ${step.id} must depend on native resource filtering`);
    if(step.type==='native_resource_apply' && !step.depends_on.some(id=>byId.get(id)?.type==='native_resource_acquire'))
      fail('workflow_graph_invalid',`step ${step.id} must depend on native resource acquisition`);
    if(step.type==='native_resource_inspect' && !step.depends_on.some(id=>byId.get(id)?.type==='native_resource_apply'))
      fail('workflow_graph_invalid',`step ${step.id} must depend on native resource application`);
    if(['native_resource_apply','native_resource_inspect'].includes(step.type)) {
      const request=step.native_resource_application_request;
      if(!request || request.schema!=='jianying-native-resource-application-request/v1' ||
        typeof request.request_id!=='string' || !request.request_id.trim() ||
        typeof request.acquisition_request_id!=='string' || !request.acquisition_request_id.trim() ||
        typeof request.resource_id!=='string' || !request.resource_id.trim() ||
        typeof request.domain!=='string' || !request.domain.trim() ||
        typeof request.draft_path!=='string' || !path.isAbsolute(request.draft_path) ||
        !request.target || typeof request.target!=='object' || Array.isArray(request.target))
        fail('workflow_plan_invalid',`step ${step.id} lacks a bound native resource application request`);
    }
    if(step.type.startsWith('native_') && step.type.endsWith('_control')) {
      const control=step.native_control;
      if(!control || typeof control!=='object' || typeof control.request_id!=='string' || !control.request_id.trim() ||
        typeof control.semantic_id!=='string' || !control.semantic_id.trim() || !control.cli || !Array.isArray(control.cli.args) ||
        control.cli.args.some(value=>typeof value!=='string') || control.cli.args.some(value=>/^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$/.test(value)))
        fail('workflow_plan_invalid',`step ${step.id} has an invalid native control binding`);
      const coordinateKeys=new Set(['x','y','left','top','right','bottom','point','points','rect','bounds','coordinate',
        'coordinates','screen_coordinate','screen_coordinates']);
      const containsCoordinate=value=>value && typeof value==='object' && (Array.isArray(value)
        ? value.some(containsCoordinate)
        : Object.entries(value).some(([key,item])=>coordinateKeys.has(key.toLowerCase()) || containsCoordinate(item)));
      if(containsCoordinate(control)) fail('workflow_plan_invalid',`step ${step.id} is coordinate-bound`);
      const expectedType={draft_protocol:'native_draft_control',runtime_native:'native_runtime_control',
        accessibility_adapter:'native_accessibility_control',visual_fallback:'native_visual_control'}[control.route];
      if(expectedType!==step.type) fail('workflow_plan_invalid',`step ${step.id} route and type differ`);
      if(control.requires_state_readback && (!control.readback?.required || typeof control.readback.field!=='string'))
        fail('workflow_plan_invalid',`step ${step.id} lacks runtime state readback`);
    }
    if(step.type.startsWith('smart_package_')) {
      const request=step.smart_package_request;
      if(!request || request.schema!=='jianying-smart-package-request/v1' || typeof request.request_id!=='string' ||
        !request.request_id.trim() || typeof request.request_digest!=='string' || !/^[0-9a-f]{64}$/.test(request.request_digest))
        fail('workflow_plan_invalid',`step ${step.id} lacks a bound smart package request`);
      const prior={smart_package_review:'smart_package_preview',smart_package_apply:'smart_package_review',
        smart_package_verify:'smart_package_apply'}[step.type];
      if(prior && !step.depends_on.some(id=>byId.get(id)?.type===prior))
        fail('workflow_graph_invalid',`step ${step.id} must depend on ${prior}`);
    }
    if(step.type.startsWith('digital_human_')) {
      const request=step.digital_human_request;
      if(!request || request.schema!=='jianying-digital-human-request/v1' || typeof request.request_id!=='string' ||
        !request.request_id.trim() || typeof request.request_digest!=='string' || !/^[0-9a-f]{64}$/.test(request.request_digest))
        fail('workflow_plan_invalid',`step ${step.id} lacks a bound digital human request`);
      const prior={digital_human_preview:'digital_human_inventory',digital_human_approve:'digital_human_preview',
        digital_human_submit:'digital_human_approve',digital_human_resume:'digital_human_submit',
        digital_human_verify:'digital_human_resume'}[step.type];
      if(prior && !step.depends_on.some(id=>byId.get(id)?.type===prior))
        fail('workflow_graph_invalid',`step ${step.id} must depend on ${prior}`);
    }
  }
  function visit(id) {
    if(visiting.has(id)) fail('workflow_graph_invalid','cycle detected');
    if(visited.has(id)) return;
    const step=byId.get(id); if(!step) fail('workflow_graph_invalid',`unknown dependency ${id}`);
    visiting.add(id); for(const dependency of step.depends_on??[]) visit(dependency);
    visiting.delete(id); visited.add(id);
  }
  for(const id of byId.keys()) visit(id);
  return {valid:true,plan_digest:sha256(canonical(plan))};
}

/** 将一个可审计的剪映官方资源取得子图绑定到计划副本。 */
export function attachNativeResourceAcquisition(plan,resourceQuery) {
  validateWorkflowPlan(plan);
  if(!resourceQuery || resourceQuery.schema!=='jianying-native-resource-query/v1' ||
    typeof resourceQuery.request_id!=='string' || !resourceQuery.request_id.trim())
    fail('workflow_plan_invalid','native resource query is required');
  const result=structuredClone(plan);
  if(result.steps.some(step=>step.resource_query?.request_id===resourceQuery.request_id))
    fail('workflow_graph_invalid',`duplicate native resource request ${resourceQuery.request_id}`);
  const offset=result.steps.length;
  const definitions=[
    ['native_resource_search','NativeResourceQuery','ResourceCandidateSet','none'],
    ['native_resource_filter','ResourceCandidateSet','FilteredResourceCandidateSet','none'],
    ['native_resource_acquire','FilteredResourceCandidateSet','ResourceReceipt','inspect_before_retry'],
  ];
  for(const [index,[type,input,output,reconcile]] of definitions.entries()) {
    const id=stepId(type,offset+index);
    result.steps.push({id,type,type_version:'1',executor:'plugin',depends_on:index?[result.steps.at(-1).id]:[],
      inputs:[{port:'input',data_type:input,artifact_ref:index?`native-resource-${resourceQuery.request_id}-${index}`:
        `native-resource-query-${resourceQuery.request_id}`}],
      outputs:[{port:'output',data_type:output,artifact_ref:`native-resource-${resourceQuery.request_id}-${index+1}`}],
      preconditions:index===0?['creative brief confirmed']:['previous resource step verified'],
      capabilities:type==='native_resource_acquire'?['media.official_resource']:[],approval_requirements:[],
      timeout_ms:type==='native_resource_acquire'?600000:300000,budget:{currency:'CNY',maximum:resourceQuery.filters?.maximum_cost_microunits??0},
      retry:{maximum_attempts:1,backoff_ms:0},reconcile:{strategy:reconcile},
      validator:{type:'artifact',version:'1',evidence_level:type==='native_resource_acquire'?'content':'structural'},
      resource_query:structuredClone(resourceQuery)});
  }
  result.tool_requirements.capabilities=[...new Set([...(result.tool_requirements.capabilities??[]),
    'media.official_resource',...(resourceQuery.domain==='music'?['media.audio']:[])])].sort();
  if(!result.risk_requirements.some(item=>item.type==='resource_download'))
    result.risk_requirements.push({type:'resource_download',approval_required:true});
  validateWorkflowPlan(result);
  return result;
}

/** 将已取得的官方资源收据继续编译为需批准的应用与独立回读子图。 */
export function attachNativeResourceApplicationWorkflow(plan,request) {
  validateWorkflowPlan(plan);
  if(!request || request.schema!=='jianying-native-resource-application-request/v1' ||
    typeof request.request_id!=='string' || !request.request_id.trim() ||
    typeof request.acquisition_request_id!=='string' || !request.acquisition_request_id.trim() ||
    typeof request.resource_id!=='string' || !request.resource_id.trim() ||
    typeof request.domain!=='string' || !request.domain.trim() ||
    typeof request.draft_path!=='string' || !path.isAbsolute(request.draft_path) ||
    !request.target || typeof request.target!=='object' || Array.isArray(request.target))
    fail('workflow_plan_invalid','a bound native resource application request is required');
  const result=structuredClone(plan);
  if(result.steps.some(step=>step.native_resource_application_request?.request_id===request.request_id))
    fail('workflow_graph_invalid',`duplicate native resource application request ${request.request_id}`);
  const acquisition=result.steps.find(step=>step.type==='native_resource_acquire' &&
    step.resource_query?.request_id===request.acquisition_request_id);
  if(!acquisition || acquisition.resource_query.domain!==request.domain)
    fail('workflow_graph_invalid',`missing matching native resource acquisition ${request.acquisition_request_id}`);
  const definitions=[
    ['native_resource_apply','ResourceReceipt','NativeActionEvidence','inspect_before_retry'],
    ['native_resource_inspect','NativeActionEvidence','NativeActionEvidence','none'],
  ];
  let dependency=acquisition;
  for(const [type,input,output,reconcile] of definitions) {
    const id=stepId(type,result.steps.length);
    const registered=STEP_REGISTRY.get(type);
    result.steps.push({id,type,type_version:'1',executor:registered.executor,depends_on:[dependency.id],
      inputs:[{port:'input',data_type:input,artifact_ref:dependency.outputs[0].artifact_ref}],
      outputs:[{port:'output',data_type:output,artifact_ref:`native-resource-application-${request.request_id}-${type}`}],
      preconditions:[type==='native_resource_apply'?'resource receipt and exact approval verified':
        'application side effect returned and requires independent readback'],
      capabilities:type==='native_resource_apply'?['media.official_resource_apply']:[],
      approval_requirements:type==='native_resource_apply'?
        [{type:'human_confirmation',scope:`native resource ${request.request_id}`}]:[],
      timeout_ms:300000,budget:{currency:'CNY',maximum:0},retry:{maximum_attempts:1,backoff_ms:0},
      reconcile:{strategy:reconcile},validator:{type:'artifact',version:'1',
        evidence_level:type==='native_resource_inspect'?'content':'structural'},
      resource_query:structuredClone(acquisition.resource_query),
      native_resource_application_request:structuredClone(request)});
    dependency=result.steps.at(-1);
  }
  result.tool_requirements.capabilities=[...new Set([...(result.tool_requirements.capabilities??[]),
    'media.official_resource_apply'])].sort();
  if(!result.risk_requirements.some(item=>item.type==='draft_write'))
    result.risk_requirements.push({type:'draft_write',approval_required:true});
  result.metadata={...result.metadata,'partme.native_resource_application':{request_id:request.request_id,
    acquisition_request_id:request.acquisition_request_id,resource_id:request.resource_id,domain:request.domain}};
  validateWorkflowPlan(result);
  return result;
}

/** 将经 CLI 目录编译的语义控件步骤绑定到 WorkflowPlan；不接受自由命令或屏幕坐标。 */
export function attachNativeControlPlan(plan,nativeControlPlan) {
  validateWorkflowPlan(plan);
  if(nativeControlPlan?.schema!=='jianying-native-control-plan/v1' || nativeControlPlan.can_execute!==true ||
    !Array.isArray(nativeControlPlan.steps) || nativeControlPlan.steps.length===0)
    fail('workflow_plan_invalid','a compiled native control plan is required');
  const result=structuredClone(plan);
  if(result.steps.some(step=>step.type.startsWith('native_') && step.type.endsWith('_control')))
    fail('workflow_graph_invalid','workflow already contains native control steps');
  let dependency=result.steps.at(-1)?.id??null;
  for(const [index,control] of nativeControlPlan.steps.entries()) {
    const type={draft_protocol:'native_draft_control',runtime_native:'native_runtime_control',
      accessibility_adapter:'native_accessibility_control',visual_fallback:'native_visual_control'}[control.route];
    if(!type) fail('workflow_plan_invalid',`unsupported native control route ${control.route}`);
    const id=stepId(type,result.steps.length);
    result.steps.push({id,type,type_version:'1',executor:type==='native_draft_control'?'cli':'plugin',
      depends_on:dependency?[dependency]:[],inputs:[{port:'input',data_type:'NativeControlRequest',
        artifact_ref:`native-control-request-${control.request_id}`}],outputs:[{port:'output',
        data_type:type==='native_draft_control'?'NativeActionEvidence':'RuntimeControlEvidence',
        artifact_ref:`native-control-evidence-${control.request_id}`}],
      preconditions:['control catalog and surface inventory verified',...(control.requires_state_readback
        ?['exact editor canary passed','before and after state readback available']:[])],
      capabilities:[control.capability],approval_requirements:[{type:'human_confirmation',scope:`native control ${control.request_id}`}],
      timeout_ms:300000,budget:{currency:'CNY',maximum:0},retry:{maximum_attempts:1,backoff_ms:0},
      reconcile:{strategy:'inspect_before_retry'},validator:{type:'artifact',version:'1',
        evidence_level:control.requires_state_readback?'content':'structural'},native_control:structuredClone(control),
      sequence:index+1});
    dependency=id;
  }
  result.tool_requirements.capabilities=[...new Set([...(result.tool_requirements.capabilities??[]),
    'runtime.control_catalog',...nativeControlPlan.steps.map(step=>step.capability)])].sort();
  for(const type of [...new Set(nativeControlPlan.steps.map(step=>step.route==='draft_protocol'?'draft_write':'native_control'))])
    if(!result.risk_requirements.some(item=>item.type===type)) result.risk_requirements.push({type,approval_required:true});
  result.metadata={...result.metadata,'partme.native_control':{schema:nativeControlPlan.schema,
    catalog_digest:nativeControlPlan.catalog_digest,inventory_digest:nativeControlPlan.inventory_digest,
    editor:structuredClone(nativeControlPlan.editor),coverage_complete:nativeControlPlan.coverage?.can_claim_complete===true}};
  validateWorkflowPlan(result);
  return result;
}

/** 将智能包装拆成预览、人工复核、应用和独立验证四步子图。 */
export function attachSmartPackageWorkflow(plan,request) {
  validateWorkflowPlan(plan);
  if(!request || request.schema!=='jianying-smart-package-request/v1' || typeof request.request_id!=='string' ||
    typeof request.request_digest!=='string' || !/^[0-9a-f]{64}$/.test(request.request_digest))
    fail('workflow_plan_invalid','a bound smart package request is required');
  const result=structuredClone(plan);
  if(result.steps.some(step=>step.smart_package_request?.request_id===request.request_id))
    fail('workflow_graph_invalid',`duplicate smart package request ${request.request_id}`);
  const definitions=[
    ['smart_package_preview','plugin','SmartPackageRequest','SmartPackageProposal','none'],
    ['smart_package_review','human','SmartPackageProposal','SmartPackageApproval','none'],
    ['smart_package_apply','plugin','SmartPackageApproval','SmartPackageEvidence','inspect_before_retry'],
    ['smart_package_verify','plugin','SmartPackageEvidence','SmartPackageEvidence','none'],
  ];
  let dependency=result.steps.at(-1)?.id??null;
  for(const [type,executor,input,output,reconcile] of definitions) {
    const id=stepId(type,result.steps.length);
    result.steps.push({id,type,type_version:'1',executor,depends_on:dependency?[dependency]:[],
      inputs:[{port:'input',data_type:input,artifact_ref:`${request.request_id}-${input}`}],
      outputs:[{port:'output',data_type:output,artifact_ref:`${request.request_id}-${output}-${id}`}],
      preconditions:type==='smart_package_preview'?['input assets and protected content frozen']:
        ['previous smart package step verified'],capabilities:type==='smart_package_apply'?['runtime.smart_package']:[],
      approval_requirements:type==='smart_package_apply'?[{type:'human_confirmation',scope:`smart package ${request.request_id}`}]:[],
      timeout_ms:type==='smart_package_apply'?900000:300000,budget:{currency:request.budget.currency,
        maximum:type==='smart_package_apply'?request.budget.maximum:0},retry:{maximum_attempts:1,backoff_ms:0},
      reconcile:{strategy:reconcile},validator:{type:'artifact',version:'1',
        evidence_level:type==='smart_package_verify'?'content':'structural'},smart_package_request:structuredClone(request)});
    dependency=id;
  }
  result.tool_requirements.capabilities=[...new Set([...(result.tool_requirements.capabilities??[]),'runtime.smart_package'])].sort();
  if(!result.risk_requirements.some(item=>item.type==='composite_write'))
    result.risk_requirements.push({type:'composite_write',approval_required:true});
  result.metadata={...result.metadata,'partme.smart_package':{request_id:request.request_id,
    request_digest:request.request_digest,operation_id:request.operation?.operation_id??'smart_package',
    lifecycle:structuredClone(request.lifecycle??{stages:['plan','preview','approve','apply','verify']}),
    style_id:request.style.style_id}};
  validateWorkflowPlan(result);
  return result;
}

/** 将数字人库存、预览、批准、单次提交、恢复和产物验证绑定到计划。 */
export function attachDigitalHumanWorkflow(plan,request) {
  validateWorkflowPlan(plan);
  if(!request || request.schema!=='jianying-digital-human-request/v1' || typeof request.request_id!=='string' ||
    typeof request.request_digest!=='string' || !/^[0-9a-f]{64}$/.test(request.request_digest))
    fail('workflow_plan_invalid','a bound digital human request is required');
  const result=structuredClone(plan);
  if(result.steps.some(step=>step.digital_human_request?.request_id===request.request_id))
    fail('workflow_graph_invalid',`duplicate digital human request ${request.request_id}`);
  const definitions=[
    ['digital_human_inventory','plugin','DigitalHumanRequest','DigitalHumanSelection','none'],
    ['digital_human_preview','plugin','DigitalHumanSelection','DigitalHumanPreview','none'],
    ['digital_human_approve','human','DigitalHumanPreview','DigitalHumanApproval','none'],
    ['digital_human_submit','plugin','DigitalHumanApproval','DigitalHumanTask','inspect_before_retry'],
    ['digital_human_resume','plugin','DigitalHumanTask','DigitalHumanTask','none'],
    ['digital_human_verify','plugin','DigitalHumanTask','DigitalHumanEvidence','none'],
  ];
  let dependency=result.steps.at(-1)?.id??null;
  for(const [type,executor,input,output,reconcile] of definitions) {
    const id=stepId(type,result.steps.length);
    result.steps.push({id,type,type_version:'1',executor,depends_on:dependency?[dependency]:[],
      inputs:[{port:'input',data_type:input,artifact_ref:`${request.request_id}-${input}-${id}`}],
      outputs:[{port:'output',data_type:output,artifact_ref:`${request.request_id}-${output}-${id}`}],
      preconditions:type==='digital_human_inventory'?['entitlement and rights policy frozen']:
        ['previous digital human step verified'],capabilities:type==='digital_human_submit'?['runtime.digital_human']:[],
      approval_requirements:type==='digital_human_submit'?[{type:'human_confirmation',scope:`digital human ${request.request_id}`},
        {type:'external_service',scope:`provider ${request.provider}`}]:[],timeout_ms:type==='digital_human_submit'?1800000:300000,
      budget:{currency:request.budget.currency,maximum:type==='digital_human_submit'?request.budget.maximum_microunits:0},
      retry:{maximum_attempts:1,backoff_ms:0},reconcile:{strategy:reconcile},validator:{type:'artifact',version:'1',
        evidence_level:type==='digital_human_verify'?'content':'structural'},digital_human_request:structuredClone(request)});
    dependency=id;
  }
  result.tool_requirements.capabilities=[...new Set([...(result.tool_requirements.capabilities??[]),'runtime.digital_human'])].sort();
  if(!result.risk_requirements.some(item=>item.type==='remote_generation'))
    result.risk_requirements.push({type:'remote_generation',approval_required:true});
  result.metadata={...result.metadata,'partme.digital_human':{request_id:request.request_id,
    request_digest:request.request_digest,provider:request.provider,upload_required:
      request.custom_assets.likeness.length>0||request.custom_assets.voice.length>0}};
  validateWorkflowPlan(result);
  return result;
}

/** 将目标和有界迭代策略绑定到计划副本；不修改原计划，也不授予执行权限。 */
export function attachQualityLoop(plan,{creativeTargets,iterationPolicy,qualityLoopOptIn=false}) {
  const gate=resolveQualityLoopGate({optIn:qualityLoopOptIn});
  const result=structuredClone(plan);
  result.creative_targets=structuredClone(creativeTargets);
  result.iteration_policy=structuredClone(iterationPolicy);
  result.metadata={...result.metadata,'partme.quality_loop_gate':gate};
  validateWorkflowPlan(result);
  return result;
}
