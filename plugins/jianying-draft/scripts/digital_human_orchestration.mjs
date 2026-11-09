import fs from 'node:fs';
import crypto from 'node:crypto';

import {AdapterError} from './runtime_adapter.mjs';
import {canonical,fail,sha256} from './workflow_data.mjs';

const USAGES=new Set(['personal','commercial','editorial']);
const APPROVAL_TYPES=new Set(['portrait_rights','voice_rights','upload']);
const ACTIVE_STATES=new Set(['submitted','running']);
const TERMINAL_STATES=new Set(['completed','failed','cancelled']);

function strings(value,{allowEmpty=false}={}) {return Array.isArray(value) && (allowEmpty || value.length>0) &&
  value.every(item=>typeof item==='string' && item.trim()) && new Set(value).size===value.length;}
function hex(value) {return typeof value==='string' && /^[0-9a-f]{64}$/.test(value);}
function validateCatalogItem(item,kind) {
  if(!item || item.kind!==kind || typeof item.resource_id!=='string' || !item.resource_id.trim() ||
    typeof item.name!=='string' || !item.name.trim() || !strings(item.categories) ||
    !['basic','professional'].includes(item.edition) || !strings(item.allowed_usages) ||
    item.allowed_usages.some(value=>!USAGES.has(value)) || !Number.isSafeInteger(item.rank) || item.rank<0 ||
    !Number.isFinite(item.cost_microunits) || item.cost_microunits<0)
    fail('digital_human_catalog_invalid',`${kind} catalog item is invalid`);
  if(kind==='voice' && (!strings(item.languages) || !strings(item.styles)))
    fail('digital_human_catalog_invalid','voice languages and styles are required');
}

/** 在剪映库存数字人目录中分别筛选形象与声音，并保留拒绝原因。 */
export function searchDigitalHumanCatalog({catalog,query}={}) {
  if(!catalog || catalog.schema!=='jianying-digital-human-catalog/v1' || !Array.isArray(catalog.personas) ||
    !Array.isArray(catalog.voices) || !query || typeof query.category!=='string' || !query.category.trim() ||
    !USAGES.has(query.usage) || typeof query.language!=='string' || !query.language.trim() ||
    typeof query.voice_style!=='string' || !query.voice_style.trim() || !['basic','professional','any'].includes(query.edition) ||
    !Number.isFinite(query.maximum_cost_microunits) || query.maximum_cost_microunits<0)
    fail('digital_human_query_invalid','digital human catalog query is incomplete');
  const filter=(items,kind)=>{
    const accepted=[],rejected=[];
    for(const item of items) {
      validateCatalogItem(item,kind); const reasons=[];
      if(!item.categories.includes(query.category)) reasons.push('category_mismatch');
      if(query.edition!=='any' && item.edition!==query.edition) reasons.push(`edition_mismatch:${query.edition}`);
      if(!item.allowed_usages.includes(query.usage)) reasons.push(`usage_not_allowed:${query.usage}`);
      if(item.cost_microunits>query.maximum_cost_microunits) reasons.push('cost_exceeds_budget');
      if(kind==='voice' && !item.languages.includes(query.language)) reasons.push('language_mismatch');
      if(kind==='voice' && !item.styles.includes(query.voice_style)) reasons.push('voice_style_mismatch');
      (reasons.length?rejected:accepted).push({resource:structuredClone(item),reasons:reasons.length?reasons:['matched']});
    }
    accepted.sort((a,b)=>a.resource.rank-b.resource.rank||a.resource.resource_id.localeCompare(b.resource.resource_id));
    return {accepted,rejected};
  };
  const personas=filter(catalog.personas,'persona'),voices=filter(catalog.voices,'voice');
  if(!personas.accepted.length || !voices.accepted.length)
    fail('digital_human_candidate_unavailable','no stock persona and voice pair satisfies the query');
  return {schema:'jianying-digital-human-selection/v1',catalog_digest:sha256(canonical(catalog)),query:structuredClone(query),
    personas,voices,selected:{persona:personas.accepted[0].resource,voice:voices.accepted[0].resource}};
}

function validateApproval(approval,{type,assetIds,provider,purpose,now}) {
  if(!approval || approval.schema!=='jianying-digital-human-approval/v1' || approval.type!==type ||
    approval.status!=='approved' || approval.provider!==provider || approval.purpose!==purpose ||
    !strings(approval.asset_ids) || assetIds.some(id=>!approval.asset_ids.includes(id)) ||
    typeof approval.approval_id!=='string' || !approval.approval_id.trim() ||
    !Number.isFinite(Date.parse(approval.expires_at)) || Date.parse(approval.expires_at)<=now)
    fail('digital_human_approval_required',`${type} approval is missing or does not match the upload scope`);
}

/** 构建库存或自定义数字人请求；自定义肖像/声音在请求形成前完成独立授权校验。 */
export function buildDigitalHumanRequest({workflowId,selection,script,background,usage,entitlement,budget,provider,
  customAssets={likeness:[],voice:[]},approvals=[],now=Date.now()}={}) {
  if(typeof workflowId!=='string' || !workflowId.trim() || !selection || !script || typeof script.text!=='string' ||
    !script.text.trim() || typeof script.language!=='string' || !script.language.trim() || script.reviewed!==true ||
    !background || !['transparent','color','image','video'].includes(background.kind) || !usage ||
    !USAGES.has(usage.purpose) || typeof usage.channel!=='string' || !usage.channel.trim() || !entitlement ||
    !['basic','professional'].includes(entitlement.edition) || entitlement.status!=='active' || !budget ||
    typeof budget.currency!=='string' || !budget.currency.trim() || !Number.isFinite(budget.maximum_microunits) ||
    budget.maximum_microunits<0 || typeof provider!=='string' || !provider.trim() || !Array.isArray(approvals) ||
    !strings(customAssets.likeness,{allowEmpty:true}) || !strings(customAssets.voice,{allowEmpty:true}))
    fail('digital_human_request_invalid','digital human request is incomplete');
  const persona=selection.persona,voice=selection.voice;
  if(!persona || !['stock','custom'].includes(persona.source) || !voice || !['stock','custom'].includes(voice.source))
    fail('digital_human_request_invalid','persona and voice source must be explicit');
  if(persona.source==='stock' && (typeof persona.resource_id!=='string' || !persona.resource_id.trim()))
    fail('digital_human_request_invalid','stock persona resource ID is required');
  if(voice.source==='stock' && (typeof voice.resource_id!=='string' || !voice.resource_id.trim()))
    fail('digital_human_request_invalid','stock voice resource ID is required');
  const purpose=`${usage.purpose}:${usage.channel}`;
  if(persona.source==='custom') {
    if(!customAssets.likeness.length) fail('digital_human_approval_required','custom likeness assets are required');
    validateApproval(approvals.find(item=>item.type==='portrait_rights'),{type:'portrait_rights',assetIds:customAssets.likeness,
      provider,purpose,now});
    validateApproval(approvals.find(item=>item.type==='upload' && item.asset_ids.some(id=>customAssets.likeness.includes(id))),
      {type:'upload',assetIds:customAssets.likeness,provider,purpose,now});
  }
  if(voice.source==='custom') {
    if(!customAssets.voice.length) fail('digital_human_approval_required','custom voice assets are required');
    validateApproval(approvals.find(item=>item.type==='voice_rights'),{type:'voice_rights',assetIds:customAssets.voice,
      provider,purpose,now});
    validateApproval(approvals.find(item=>item.type==='upload' && item.asset_ids.some(id=>customAssets.voice.includes(id))),
      {type:'upload',assetIds:customAssets.voice,provider,purpose,now});
  }
  const body={schema:'jianying-digital-human-request/v1',workflow_id:workflowId,provider,
    selection:structuredClone(selection),script:{text:script.text,language:script.language,reviewed:true,
      content_digest:sha256(script.text)},background:structuredClone(background),usage:structuredClone(usage),
    entitlement:structuredClone(entitlement),budget:structuredClone(budget),custom_assets:structuredClone(customAssets),
    approval_ids:approvals.map(item=>item.approval_id).sort()};
  const requestId=`digital-human-${sha256(canonical(body)).slice(0,24)}`;
  return {...body,request_id:requestId,request_digest:sha256(canonical({...body,request_id:requestId}))};
}

/** 形成无上传副作用的预览计划。 */
export function buildDigitalHumanPreviewPlan({request}={}) {
  if(!request || request.schema!=='jianying-digital-human-request/v1' || !hex(request.request_digest))
    fail('digital_human_request_invalid','a bound digital human request is required');
  return {schema:'jianying-digital-human-preview-plan/v1',request_id:request.request_id,
    request_digest:request.request_digest,steps:['resolve_inventory','configure_voice','bind_script','configure_background','render_preview'],
    upload_required:request.custom_assets.likeness.length>0 || request.custom_assets.voice.length>0,
    submit_allowed:false,budget:structuredClone(request.budget)};
}

function validateLedger(ledger) {
  if(!ledger || typeof ledger.load!=='function' || typeof ledger.save!=='function')
    fail('digital_human_ledger_invalid','digital human task ledger is required');
}
function validateProvider(provider) {
  if(!provider || typeof provider.name!=='string' || !provider.name.trim() || typeof provider.version!=='string' ||
    !provider.version.trim() || typeof provider.estimate!=='function' || typeof provider.submit!=='function' ||
    typeof provider.status!=='function') fail('digital_human_provider_invalid','versioned provider adapter is required');
}

/** 按稳定 request_id 提交一次；已有、活动或不明确记录永不静默重提。 */
export async function submitOrResumeDigitalHumanTask({request,provider,ledger}={}) {
  if(!request || request.schema!=='jianying-digital-human-request/v1' || request.provider!==provider?.name ||
    !hex(request.request_digest)) fail('digital_human_request_invalid','request and provider are not bound');
  validateProvider(provider); validateLedger(ledger);
  const existing=await ledger.load(request.request_id);
  if(existing) {
    if(existing.request_digest!==request.request_digest) fail('digital_human_idempotency_conflict','stable request ID has another digest');
    if(existing.status==='ambiguous') fail('digital_human_submit_ambiguous','prior submission outcome is ambiguous');
    if(ACTIVE_STATES.has(existing.status) || TERMINAL_STATES.has(existing.status))
      return {action:'resume',task:structuredClone(existing)};
    fail('digital_human_task_invalid',`unknown persisted status ${existing.status}`);
  }
  const estimate=await provider.estimate(structuredClone(request));
  if(!estimate || !Number.isFinite(estimate.cost_microunits) || estimate.cost_microunits<0 ||
    estimate.cost_microunits>request.budget.maximum_microunits)
    fail('digital_human_budget_exceeded','provider estimate exceeds the approved budget');
  const submitted=await provider.submit(structuredClone(request),{idempotency_key:request.request_id,
    maximum_cost_microunits:request.budget.maximum_microunits});
  if(!submitted || typeof submitted.vendor_request_id!=='string' || !submitted.vendor_request_id.trim() ||
    typeof submitted.remote_task_id!=='string' || !submitted.remote_task_id.trim() ||
    !ACTIVE_STATES.has(submitted.status)) {
    const ambiguous={schema:'jianying-digital-human-task/v1',request_id:request.request_id,
      request_digest:request.request_digest,provider:provider.name,provider_version:provider.version,status:'ambiguous',
      vendor_request_id:submitted?.vendor_request_id??null,remote_task_id:submitted?.remote_task_id??null,
      estimated_cost_microunits:estimate.cost_microunits,actual_cost_microunits:null,artifact:null};
    await ledger.save(request.request_id,ambiguous);
    throw new AdapterError('digital_human_submit_ambiguous','provider did not return stable submission identities',
      {request_id:request.request_id,resubmit_allowed:false});
  }
  const task={schema:'jianying-digital-human-task/v1',request_id:request.request_id,
    request_digest:request.request_digest,provider:provider.name,provider_version:provider.version,status:submitted.status,
    vendor_request_id:submitted.vendor_request_id,remote_task_id:submitted.remote_task_id,
    estimated_cost_microunits:estimate.cost_microunits,actual_cost_microunits:null,artifact:null};
  await ledger.save(request.request_id,task);
  return {action:'submitted',task:structuredClone(task)};
}

/** 仅凭已保存远程 task ID 恢复状态，不调用 submit。 */
export async function refreshDigitalHumanTask({request,provider,ledger}={}) {
  validateProvider(provider); validateLedger(ledger);
  const task=await ledger.load(request?.request_id);
  if(!task || task.request_digest!==request?.request_digest || task.provider!==provider.name ||
    typeof task.remote_task_id!=='string' || !task.remote_task_id.trim())
    fail('digital_human_task_missing','persisted remote task identity is required');
  if(task.status==='ambiguous') fail('digital_human_submit_ambiguous','ambiguous task must be reconciled manually');
  if(TERMINAL_STATES.has(task.status)) return structuredClone(task);
  const status=await provider.status(task.remote_task_id,{vendor_request_id:task.vendor_request_id});
  if(!status || !['submitted','running','completed','failed','cancelled','ambiguous'].includes(status.status))
    fail('digital_human_status_invalid','provider status response is invalid');
  const updated={...task,status:status.status,actual_cost_microunits:status.actual_cost_microunits??task.actual_cost_microunits,
    artifact:status.artifact??task.artifact};
  if(updated.actual_cost_microunits!==null && (!Number.isFinite(updated.actual_cost_microunits) ||
    updated.actual_cost_microunits<0 || updated.actual_cost_microunits>request.budget.maximum_microunits))
    fail('digital_human_budget_exceeded','actual cost exceeds the approved budget');
  await ledger.save(request.request_id,updated);
  if(updated.status==='ambiguous') fail('digital_human_status_ambiguous','remote task status is ambiguous');
  return structuredClone(updated);
}

/** 验证完成任务的本地产物身份、摘要和费用，不接受仅有供应商成功提示。 */
export function verifyDigitalHumanArtifact({request,task}={}) {
  if(!request || !task || task.request_id!==request.request_id || task.request_digest!==request.request_digest ||
    task.status!=='completed' || !task.artifact || typeof task.artifact.path!=='string' || !hex(task.artifact.sha256) ||
    !Number.isSafeInteger(task.artifact.byte_length) || task.artifact.byte_length<1)
    fail('digital_human_artifact_invalid','completed task lacks a bound artifact identity');
  let stat;
  try {stat=fs.lstatSync(task.artifact.path);} catch {fail('digital_human_artifact_missing','digital human artifact is missing');}
  if(stat.isSymbolicLink() || !stat.isFile() || stat.size!==task.artifact.byte_length)
    fail('digital_human_artifact_invalid','digital human artifact file identity is invalid');
  const actual=crypto.createHash('sha256').update(fs.readFileSync(task.artifact.path)).digest('hex');
  if(actual!==task.artifact.sha256) fail('digital_human_artifact_digest_mismatch','digital human artifact content changed');
  return {schema:'jianying-digital-human-evidence/v1',request_id:request.request_id,status:'verified',
    provider:task.provider,vendor_request_id:task.vendor_request_id,remote_task_id:task.remote_task_id,
    actual_cost_microunits:task.actual_cost_microunits,artifact:structuredClone(task.artifact),
    evidence_digest:sha256(canonical({request_digest:request.request_digest,task}))};
}
