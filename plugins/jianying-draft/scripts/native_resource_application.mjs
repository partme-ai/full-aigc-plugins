import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

import {AdapterError} from './runtime_adapter.mjs';
import {canonical} from './workflow_data.mjs';

const SECRET_KEY=/(?:^|_)(?:access_?token|refresh_?token|token|secret|password|credential|cookie|authorization|api_?key)(?:$|_)/i;
const ACTIONS=new Set(['preview','apply','remove','inspect','recover']);

const digest=value=>crypto.createHash('sha256').update(canonical(value)).digest('hex');
const fail=(code,message,details={},recovery=[])=>{throw new AdapterError(code,message,details,recovery);};

function atomicJson(file,value) {
  fs.mkdirSync(path.dirname(file),{recursive:true});
  const temporary=`${file}.${process.pid}.${crypto.randomUUID()}.tmp`;
  fs.writeFileSync(temporary,`${JSON.stringify(value,null,2)}\n`,{encoding:'utf8',mode:0o600});
  fs.renameSync(temporary,file);
}

function rejectSecrets(value,location='$') {
  if(!value || typeof value!=='object') return;
  if(Array.isArray(value)) return value.forEach((item,index)=>rejectSecrets(item,`${location}[${index}]`));
  for(const [key,item] of Object.entries(value)) {
    if(SECRET_KEY.test(key)) fail('native_resource_secret_persistence_forbidden',`secret field cannot be persisted: ${location}.${key}`);
    rejectSecrets(item,`${location}.${key}`);
  }
}

function validateIdentity(identity) {
  if(!identity || typeof identity!=='object' || Array.isArray(identity) || typeof identity.kind!=='string' ||
    !identity.kind.trim() || typeof identity.editor_bundle!=='string' || !identity.editor_bundle.trim() ||
    typeof identity.editor_version!=='string' || !identity.editor_version.trim() ||
    typeof identity.adapter_version!=='string' || !identity.adapter_version.trim())
    fail('native_resource_application_adapter_invalid','version-bound adapter identity is required');
  rejectSecrets(identity,'$.adapter_identity');
}

function validateAdapter(adapter) {
  validateIdentity(adapter?.identity);
  for(const method of ['preview','snapshot','apply','inspect','remove','restore'])
    if(typeof adapter[method]!=='function') fail('native_resource_application_adapter_invalid',`${method} adapter operation is required`);
}

function validateRequest(request,schema,keys) {
  if(!request || request.schema!==schema || Object.keys(request).some(key=>!keys.includes(key)) ||
    typeof request.request_id!=='string' || !request.request_id.trim() ||
    typeof request.resource_id!=='string' || !request.resource_id.trim() ||
    typeof request.draft_path!=='string' || !path.isAbsolute(request.draft_path))
    fail('native_resource_application_request_invalid',`invalid ${schema} request`);
  rejectSecrets(request,'$.request');
}

function validateApproval(request,approval,now) {
  if(!approval || approval.schema!=='jianying-native-resource-approval/v1' || approval.status!=='approved' ||
    typeof approval.approval_id!=='string' || !approval.approval_id.trim() ||
    approval.request_digest!==nativeResourceRequestDigest(request) ||
    !Number.isFinite(Date.parse(approval.expires_at)) || Date.parse(approval.expires_at)<=now())
    fail('native_resource_application_approval_required','exact unexpired native-resource approval is required');
  rejectSecrets(approval,'$.approval');
}

function evidence(action,resourceId,identity,observation,now,outcome='succeeded') {
  if(!ACTIONS.has(action)) fail('native_action_evidence_invalid',`unsupported native action ${action}`);
  rejectSecrets(observation,'$.observation');
  return {schema:'jianying-native-action-evidence/v1',action,semantic_id:`resource.${action}`,
    resource_id:resourceId,adapter_identity:structuredClone(identity),observation:structuredClone(observation),
    observed_at:new Date(now()).toISOString(),outcome};
}

async function restore(adapter,snapshot,reason) {
  const recovered=await adapter.restore(structuredClone(snapshot),{reason});
  if(!recovered || recovered.status!=='restored')
    fail('native_resource_restore_failed','adapter did not verify snapshot restoration');
  rejectSecrets(recovered,'$.recovery');
  return recovered;
}

function acquisitionBinding(acquisition,request) {
  if(!acquisition || acquisition.schema!=='jianying-native-resource-acquisition/v1' || acquisition.state!=='ready' ||
    acquisition.request_id!==request.acquisition_request_id || acquisition.selected?.resource_id!==request.resource_id ||
    acquisition.selected?.domain!==request.domain || acquisition.receipt?.asset_id!==request.resource_id ||
    acquisition.cli?.register?.status!=='registered' || acquisition.cli?.preflight?.status!=='ready')
    fail('native_resource_acquisition_not_ready','application request is not bound to a CLI-verified acquisition');
  return {acquisition_request_id:acquisition.request_id,acquisition_digest:digest(acquisition),
    receipt_digest:digest(acquisition.receipt),register_status:acquisition.cli.register.status,
    preflight_status:acquisition.cli.preflight.status};
}

/** 计算应用或移除请求的稳定批准摘要。 */
export function nativeResourceRequestDigest(request) {return digest(request);}

/** 预览并应用已由 CLI 登记/预检的资源；任何模糊结果都会恢复应用前快照。 */
export async function applyNativeResource({acquisition,request,approval,adapter,stateRoot,now=()=>Date.now()}={}) {
  validateRequest(request,'jianying-native-resource-application-request/v1',
    ['schema','request_id','acquisition_request_id','resource_id','domain','draft_path','target']);
  if(typeof request.acquisition_request_id!=='string' || !request.acquisition_request_id.trim() ||
    typeof request.domain!=='string' || !request.domain.trim() || !request.target || typeof request.target!=='object' ||
    Array.isArray(request.target) || typeof stateRoot!=='string' || !stateRoot.trim())
    fail('native_resource_application_request_invalid','application acquisition, domain, target, and state root are required');
  validateApproval(request,approval,now); validateAdapter(adapter);
  const cliHandoff=acquisitionBinding(acquisition,request),targetDigest=digest(request.target);
  const preview=await adapter.preview(structuredClone(request),{receipt:structuredClone(acquisition.receipt)});
  if(!preview || preview.status!=='ready' || typeof preview.artifact_digest!=='string' || !/^[a-f0-9]{64}$/.test(preview.artifact_digest))
    fail('native_resource_preview_invalid','adapter preview is missing or not bound to a stable artifact');
  rejectSecrets(preview,'$.preview');
  const snapshot=await adapter.snapshot({draft_path:request.draft_path,request_id:request.request_id});
  if(!snapshot || typeof snapshot.snapshot_id!=='string' || !snapshot.snapshot_id.trim())
    fail('native_resource_snapshot_invalid','pre-application snapshot is missing');
  rejectSecrets(snapshot,'$.snapshot');
  const applied=await adapter.apply(structuredClone(request),{receipt:structuredClone(acquisition.receipt),approval:structuredClone(approval)});
  if(!applied || applied.status!=='applied' || typeof applied.application_id!=='string' || !applied.application_id.trim()) {
    const recovery=await restore(adapter,snapshot,'ambiguous_or_failed_apply');
    throw new AdapterError('native_resource_apply_ambiguous','resource application outcome is not exactly applied',
      {recovered:true,recovery,snapshot_id:snapshot.snapshot_id});
  }
  rejectSecrets(applied,'$.application');
  const expected={resource_id:request.resource_id,target_digest:targetDigest};
  const inspection=await adapter.inspect(structuredClone(request),{expected,application:structuredClone(applied)});
  if(!inspection || inspection.status!=='present' || inspection.resource_id!==request.resource_id ||
    inspection.target_digest!==targetDigest) {
    const recovery=await restore(adapter,snapshot,'application_verification_failed');
    throw new AdapterError('native_resource_application_verification_failed','draft resource or timeline readback differs from the request',
      {recovered:true,recovery,snapshot_id:snapshot.snapshot_id});
  }
  rejectSecrets(inspection,'$.inspection');
  const actions=[evidence('preview',request.resource_id,adapter.identity,preview,now),
    evidence('apply',request.resource_id,adapter.identity,applied,now),
    evidence('inspect',request.resource_id,adapter.identity,inspection,now)];
  const base={schema:'jianying-native-resource-application/v1',request_id:request.request_id,state:'verified',
    resource_id:request.resource_id,domain:request.domain,draft_path:request.draft_path,target_digest:targetDigest,
    approval_id:approval.approval_id,snapshot_id:snapshot.snapshot_id,preview_digest:preview.artifact_digest,
    application_id:applied.application_id,adapter_identity:structuredClone(adapter.identity),cli_handoff:cliHandoff,actions};
  const result={...base,application_digest:digest(base),artifacts:{application_path:path.join(path.resolve(stateRoot),
    request.request_id,'native-resource-application.json')}};
  rejectSecrets(result); atomicJson(result.artifacts.application_path,result); return result;
}

function validateApplication(application) {
  if(!application || application.schema!=='jianying-native-resource-application/v1' || application.state!=='verified' ||
    typeof application.application_digest!=='string' || !/^[a-f0-9]{64}$/.test(application.application_digest))
    fail('native_resource_application_invalid','verified application evidence is required');
  const {application_digest,artifacts,...base}=application;
  if(digest(base)!==application_digest) fail('native_resource_application_invalid','application evidence digest mismatch');
}

/** 局部移除一个已验证资源；模糊移除或回读失败时恢复移除前快照。 */
export async function removeNativeResource({application,request,approval,adapter,stateRoot,now=()=>Date.now()}={}) {
  validateApplication(application);
  validateRequest(request,'jianying-native-resource-removal-request/v1',
    ['schema','request_id','resource_id','draft_path','target_digest','application_digest']);
  if(request.resource_id!==application.resource_id || request.draft_path!==application.draft_path ||
    request.target_digest!==application.target_digest || request.application_digest!==application.application_digest ||
    typeof stateRoot!=='string' || !stateRoot.trim())
    fail('native_resource_removal_request_invalid','removal request differs from the verified application');
  validateApproval(request,approval,now); validateAdapter(adapter);
  const snapshot=await adapter.snapshot({draft_path:request.draft_path,request_id:request.request_id});
  if(!snapshot || typeof snapshot.snapshot_id!=='string' || !snapshot.snapshot_id.trim())
    fail('native_resource_snapshot_invalid','pre-removal snapshot is missing');
  rejectSecrets(snapshot,'$.snapshot');
  const removed=await adapter.remove(structuredClone(request),{application:structuredClone(application),approval:structuredClone(approval)});
  if(!removed || removed.status!=='removed' || typeof removed.removal_id!=='string' || !removed.removal_id.trim()) {
    const recovery=await restore(adapter,snapshot,'ambiguous_or_failed_remove');
    throw new AdapterError('native_resource_remove_ambiguous','resource removal outcome is not exactly removed',
      {recovered:true,recovery,snapshot_id:snapshot.snapshot_id});
  }
  rejectSecrets(removed,'$.removal');
  const inspection=await adapter.inspect(structuredClone(request),{expected:{resource_id:request.resource_id,
    target_digest:request.target_digest},removal:structuredClone(removed)});
  if(!inspection || inspection.status!=='absent') {
    const recovery=await restore(adapter,snapshot,'removal_verification_failed');
    throw new AdapterError('native_resource_removal_verification_failed','resource remains after local removal',
      {recovered:true,recovery,snapshot_id:snapshot.snapshot_id});
  }
  rejectSecrets(inspection,'$.inspection');
  const actions=[evidence('remove',request.resource_id,adapter.identity,removed,now),
    evidence('inspect',request.resource_id,adapter.identity,inspection,now)];
  const base={schema:'jianying-native-resource-removal/v1',request_id:request.request_id,state:'verified_removed',
    resource_id:request.resource_id,draft_path:request.draft_path,target_digest:request.target_digest,
    application_digest:request.application_digest,approval_id:approval.approval_id,snapshot_id:snapshot.snapshot_id,
    removal_id:removed.removal_id,adapter_identity:structuredClone(adapter.identity),actions};
  const result={...base,removal_digest:digest(base),artifacts:{removal_path:path.join(path.resolve(stateRoot),request.request_id,
    'native-resource-removal.json')}};
  rejectSecrets(result); atomicJson(result.artifacts.removal_path,result); return result;
}
