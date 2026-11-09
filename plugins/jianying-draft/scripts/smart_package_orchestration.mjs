import {canonical,fail,sha256} from './workflow_data.mjs';
import {AdapterError} from './runtime_adapter.mjs';

const STYLE_ROUTES=new Map([
  ['smart_recommended',{route_tags:['smart-package','balanced','general'],label:'智能推荐'}],
  ['technology',{route_tags:['smart-package','technology','high-tempo'],label:'科技风'}],
  ['life_vlog',{route_tags:['smart-package','life-vlog','authentic'],label:'生活 Vlog'}],
  ['marketing_sales',{route_tags:['smart-package','marketing','conversion'],label:'营销带货'}],
  ['knowledge',{route_tags:['smart-package','knowledge','clarity'],label:'知识分享'}],
  ['variety_entertainment',{route_tags:['smart-package','variety','entertainment'],label:'综艺娱乐'}],
]);
const OPERATION_ROUTES=new Map([
  ['smart_package',{route_tags:['smart-package','composite-edit'],label:'智能包装'}],
  ['smart_b_roll',{route_tags:['smart-package','b-roll'],label:'智能 B-Roll'}],
  ['smart_rough_cut',{route_tags:['smart-package','rough-cut','asset-driven'],label:'智能粗剪'}],
  ['script_rough_cut',{route_tags:['smart-package','rough-cut','script-driven'],label:'文案粗剪'}],
]);
const LIFECYCLE={stages:['plan','preview','approve','apply','verify'],failure_recovery:{snapshot_before_apply:true,
  ambiguous_apply:'restore',verification_failure:'restore'}};
const CHANGE_TYPES=new Set(['b_roll','caption','fancy_text','sound_effect','effect','transition']);
const ACTIONS=new Set(['add','update','remove']);

function strings(value,{allowEmpty=false}={}) {return Array.isArray(value) && (allowEmpty || value.length>0) &&
  value.every(item=>typeof item==='string' && item.trim()) && new Set(value).size===value.length;}
function digest(value) {return sha256(canonical(value));}

/** 将剪映智能包装版型映射到开放路由标签，不把界面文案当成执行命令。 */
export function mapSmartPackageStyle(styleId) {
  const mapped=STYLE_ROUTES.get(styleId);
  if(!mapped) fail('smart_package_style_unknown',String(styleId));
  return {style_id:styleId,label:mapped.label,route_tags:[...mapped.route_tags]};
}

/** 将剪映专属组合动作映射为开放路由标签，不暴露坐标或私有界面实现。 */
export function mapSmartPackageOperation(operationId) {
  const mapped=OPERATION_ROUTES.get(operationId);
  if(!mapped) fail('smart_package_operation_unknown',String(operationId));
  return {operation_id:operationId,label:mapped.label,route_tags:[...mapped.route_tags]};
}

/** 创建带受保护内容、预算、预览和批准边界的智能包装请求。 */
export function buildSmartPackageRequest({requestId,workflowId,styleId,inputAssets,allowedTracks,protectedContent,
  budget,preview,maximumDurationMs,operationId='smart_package'}={}) {
  const style=mapSmartPackageStyle(styleId);
  const operation=mapSmartPackageOperation(operationId);
  if(typeof requestId!=='string' || !requestId.trim() || typeof workflowId!=='string' || !workflowId.trim() ||
    !strings(inputAssets) || !strings(allowedTracks) || !protectedContent ||
    !strings(protectedContent.dialogue_ids,{allowEmpty:true}) || !strings(protectedContent.brand_claim_ids,{allowEmpty:true}) ||
    !strings(protectedContent.segment_ids,{allowEmpty:true}) || !budget || typeof budget.currency!=='string' ||
    !Number.isFinite(budget.maximum) || budget.maximum<0 || !preview || preview.required!==true ||
    preview.human_approval_required!==true || !Number.isSafeInteger(maximumDurationMs) || maximumDurationMs<1)
    fail('smart_package_request_invalid','smart package request boundaries are incomplete');
  const body={schema:'jianying-smart-package-request/v1',request_id:requestId,workflow_id:workflowId,operation,style,
    input_assets:[...inputAssets],allowed_tracks:[...allowedTracks],protected_content:structuredClone(protectedContent),
    budget:structuredClone(budget),preview:structuredClone(preview),maximum_duration_ms:maximumDurationMs,
    lifecycle:structuredClone(LIFECYCLE)};
  return {...body,request_digest:digest(body)};
}

function validateChange(change,request) {
  if(!change || typeof change.change_id!=='string' || !change.change_id.trim() || !CHANGE_TYPES.has(change.type) ||
    !ACTIONS.has(change.action) || typeof change.track!=='string' || !request.allowed_tracks.includes(change.track) ||
    !Number.isSafeInteger(change.start_ms) || change.start_ms<0 || !Number.isSafeInteger(change.duration_ms) ||
    change.duration_ms<1 || change.start_ms+change.duration_ms>request.maximum_duration_ms ||
    !Array.isArray(change.target_ids) || change.target_ids.some(item=>typeof item!=='string' || !item.trim()) ||
    typeof change.content_digest!=='string' || !/^[0-9a-f]{64}$/.test(change.content_digest))
    fail('smart_package_change_invalid',`invalid or out-of-policy change ${change?.change_id??'unknown'}`);
  const protectedDialogue=new Set(request.protected_content.dialogue_ids);
  const protectedBrands=new Set(request.protected_content.brand_claim_ids);
  const protectedSegments=new Set(request.protected_content.segment_ids);
  if(change.action==='remove' && change.target_ids.some(id=>protectedDialogue.has(id)))
    fail('smart_package_protected_dialogue','package deletes protected dialogue');
  if(['update','remove'].includes(change.action) && change.target_ids.some(id=>protectedBrands.has(id)))
    fail('smart_package_protected_brand','package changes a protected brand claim');
  if(change.target_ids.some(id=>protectedSegments.has(id)) && change.action!=='add')
    fail('smart_package_protected_segment','package changes a protected segment');
}

function validateProposal(request,proposal) {
  if(!proposal || proposal.schema!=='jianying-smart-package-proposal/v1' || proposal.request_digest!==request.request_digest ||
    typeof proposal.change_set_id!=='string' || !proposal.change_set_id.trim() || proposal.status!=='preview_ready' ||
    !proposal.preview || typeof proposal.preview.artifact_digest!=='string' || !/^[0-9a-f]{64}$/.test(proposal.preview.artifact_digest) ||
    !Array.isArray(proposal.changes) || proposal.changes.length===0 || !Array.isArray(proposal.unexplained_changes) ||
    !Number.isFinite(proposal.estimated_cost) || proposal.estimated_cost<0 || proposal.estimated_cost>request.budget.maximum)
    fail('smart_package_proposal_invalid','smart package proposal is unbound, unexplained, or over budget');
  if(proposal.unexplained_changes.length) fail('smart_package_unexplained_changes','proposal contains unexplained changes');
  const ids=new Set();
  for(const change of proposal.changes) {
    if(ids.has(change.change_id)) fail('smart_package_change_invalid',`duplicate change ${change.change_id}`);
    ids.add(change.change_id); validateChange(change,request);
  }
}

/** 将智能 B-Roll/包装提案拆成字幕、花字、音效、特效、转场和补充画面分组。 */
export function decomposeSmartPackageProposal({request,proposal}={}) {
  validateProposal(request,proposal);
  const groups=Object.fromEntries([...CHANGE_TYPES].map(type=>[type,[]]));
  for(const change of proposal.changes) groups[change.type].push(structuredClone(change));
  return {schema:'jianying-smart-package-change-set/v1',request_id:request.request_id,
    request_digest:request.request_digest,change_set_id:proposal.change_set_id,preview:structuredClone(proposal.preview),groups,
    change_count:proposal.changes.length,change_set_digest:digest(proposal.changes)};
}

function validateApproval(request,changeSet,approval) {
  if(!approval || approval.schema!=='jianying-smart-package-approval/v1' || approval.status!=='approved' ||
    approval.request_digest!==request.request_digest || approval.change_set_digest!==changeSet.change_set_digest ||
    typeof approval.approval_id!=='string' || !approval.approval_id.trim() ||
    !Number.isFinite(Date.parse(approval.expires_at)) || Date.parse(approval.expires_at)<=Date.now())
    fail('smart_package_approval_required','exact unexpired preview approval is required');
}

async function restore(adapter,snapshot,reason) {
  if(typeof adapter.restore!=='function') fail('smart_package_restore_unavailable','smart package adapter cannot restore its snapshot');
  const result=await adapter.restore(snapshot,{reason});
  if(!result || result.status!=='restored') fail('smart_package_restore_failed','smart package snapshot restore was not verified');
  return result;
}

/** 执行预览批准后的智能包装，并对不明确结果或越界实际变更强制恢复。 */
export async function executeSmartPackageWithRecovery({request,proposal,approval,adapter}={}) {
  const stateTrace=[{stage:'plan',status:'planned'}];
  const changeSet=decomposeSmartPackageProposal({request,proposal});
  stateTrace.push({stage:'preview',status:'ready'});
  validateApproval(request,changeSet,approval);
  stateTrace.push({stage:'approve',status:'approved'});
  if(!adapter || typeof adapter.snapshot!=='function' || typeof adapter.preview!=='function' ||
    typeof adapter.apply!=='function' || typeof adapter.inspect!=='function')
    fail('smart_package_adapter_invalid','snapshot, preview, apply and inspect are required');
  const snapshot=await adapter.snapshot(request);
  if(!snapshot || typeof snapshot.snapshot_id!=='string' || !snapshot.snapshot_id.trim())
    fail('smart_package_snapshot_invalid','application snapshot is missing');
  const preview=await adapter.preview(request,proposal);
  if(!preview || preview.status!=='ready' || preview.artifact_digest!==proposal.preview.artifact_digest)
    fail('smart_package_preview_mismatch','adapter preview differs from the approved proposal');
  const applied=await adapter.apply(request,changeSet,approval);
  if(!applied || applied.status!=='applied') {
    stateTrace.push({stage:'apply',status:'ambiguous'});
    const recovery=await restore(adapter,snapshot,'ambiguous_or_failed_apply');
    stateTrace.push({stage:'recover',status:'restored'});
    throw new AdapterError('smart_package_apply_ambiguous','smart package apply did not produce an exact applied state',
      {recovered:true,recovery,snapshot_id:snapshot.snapshot_id,state_trace:stateTrace});
  }
  stateTrace.push({stage:'apply',status:'applied'});
  const inspection=await adapter.inspect(request,applied);
  try {
    const observed={...proposal,changes:inspection?.changes,unexplained_changes:inspection?.unexplained_changes??[]};
    const observedSet=decomposeSmartPackageProposal({request,proposal:observed});
    if(observedSet.change_set_digest!==changeSet.change_set_digest)
      fail('smart_package_change_drift','observed changes differ from the approved change set');
  } catch(error) {
    stateTrace.push({stage:'verify',status:'failed'});
    const recovery=await restore(adapter,snapshot,error.code??'verification_failed');
    stateTrace.push({stage:'recover',status:'restored'});
    error.details={...(error.details??{}),recovered:true,recovery,snapshot_id:snapshot.snapshot_id,state_trace:stateTrace};
    throw error;
  }
  stateTrace.push({stage:'verify',status:'verified'});
  return {schema:'jianying-smart-package-evidence/v1',request_id:request.request_id,status:'verified',
    approval_id:approval.approval_id,snapshot_id:snapshot.snapshot_id,preview_digest:preview.artifact_digest,
    change_set_digest:changeSet.change_set_digest,application:structuredClone(applied),inspection:structuredClone(inspection),
    state_trace:stateTrace,
    evidence_digest:digest({request,changeSet,approval,snapshot,preview,applied,inspection,stateTrace})};
}
