import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

import {AdapterError,runJsonCommand} from './runtime_adapter.mjs';
import {canonical} from './workflow_data.mjs';

const DOMAINS=new Set(['media','music','text','sticker','effect','transition','caption','smart_package','filter','adjustment','template','digital_human']);
const DOWNLOAD_STATES=new Set(['not_downloaded','downloading','downloaded','failed','ambiguous']);
const USAGES=new Set(['personal','commercial','editorial']);
const SECRET_KEY=/(?:^|_)(?:access_?token|refresh_?token|token|secret|password|credential|cookie|authorization|api_?key)(?:$|_)/i;
const RESOURCE_KIND={text:'text_template',effect:'video_effect',caption:'caption_style'};
const ORDINARY_DOMAINS=['media','music','text','sticker','effect','transition','caption','filter','adjustment','template'];

function error(code,message,details={},recovery=[]) {throw new AdapterError(code,message,details,recovery);}
function rejectSecrets(value,location='$') {
  if(!value || typeof value!=='object') return;
  if(Array.isArray(value)) return value.forEach((item,index)=>rejectSecrets(item,`${location}[${index}]`));
  for(const [key,item] of Object.entries(value)) {
    if(SECRET_KEY.test(key)) error('native_resource_secret_persistence_forbidden',
      `secret field cannot be persisted: ${location}.${key}`);
    rejectSecrets(item,`${location}.${key}`);
  }
}
function strings(value,{allowEmpty=false}={}) {
  return Array.isArray(value) && (allowEmpty || value.length>0) && value.every(item=>typeof item==='string' && item.trim()) &&
    new Set(value).size===value.length;
}
function validateQuery(query) {
  if(!query || query.schema!=='jianying-native-resource-query/v1' || typeof query.request_id!=='string' || !query.request_id.trim() ||
    !DOMAINS.has(query.domain) || !strings(query.keywords,{allowEmpty:true}) || !query.filters || typeof query.filters!=='object' ||
    !query.selection || query.selection.strategy!=='ranked' || !Number.isSafeInteger(query.selection.maximum_candidates) ||
    query.selection.maximum_candidates<1 || query.selection.maximum_candidates>100)
    error('resource_query_invalid','native resource query is incomplete or unsupported');
  const filters=query.filters;
  for(const field of ['styles','moods','tempos','aspect_ratios'])
    if(!strings(filters[field]??[],{allowEmpty:true})) error('resource_query_invalid',`${field} filter is invalid`);
  if(!['basic','professional','any'].includes(filters.edition) || !USAGES.has(filters.usage) ||
    typeof filters.channel!=='string' || !filters.channel.trim() || !Number.isSafeInteger(filters.maximum_cost_microunits) ||
    filters.maximum_cost_microunits<0) error('resource_query_invalid','resource entitlement or cost filters are invalid');
  if(filters.at_epoch_seconds!==undefined && (!Number.isSafeInteger(filters.at_epoch_seconds) || filters.at_epoch_seconds<1))
    error('resource_query_invalid','resource query validation time is invalid');
  for(const field of ['minimum_duration_ms','maximum_duration_ms'])
    if(filters[field]!==undefined && (!Number.isSafeInteger(filters[field]) || filters[field]<1))
      error('resource_query_invalid',`${field} is invalid`);
  if(filters.minimum_duration_ms!==undefined && filters.maximum_duration_ms!==undefined &&
    filters.minimum_duration_ms>filters.maximum_duration_ms) error('resource_query_invalid','duration range is inverted');
}
function validateCandidate(candidate) {
  rejectSecrets(candidate,'$.candidate');
  if(!candidate || candidate.schema!=='jianying-resource-candidate/v1' || typeof candidate.candidate_id!=='string' || !candidate.candidate_id.trim() ||
    !DOMAINS.has(candidate.domain) || typeof candidate.title!=='string' || !candidate.title.trim() || candidate.provider!=='jianying_official' ||
    typeof candidate.resource_id!=='string' || !candidate.resource_id.trim() || !['basic','professional','unknown'].includes(candidate.edition) ||
    !DOWNLOAD_STATES.has(candidate.download_state) || !strings(candidate.styles,{allowEmpty:true}) || !strings(candidate.moods,{allowEmpty:true}) ||
    !strings(candidate.tempos,{allowEmpty:true}) || !strings(candidate.aspect_ratios,{allowEmpty:true}) || !strings(candidate.channels,{allowEmpty:true}) ||
    !strings(candidate.allowed_usages) || candidate.allowed_usages.some(value=>!USAGES.has(value)) ||
    !Number.isSafeInteger(candidate.cost_microunits) || candidate.cost_microunits<0 ||
    typeof candidate.terms_reference!=='string' || !candidate.terms_reference.trim() || !strings(candidate.restrictions,{allowEmpty:true}) ||
    typeof candidate.preview_only!=='boolean' || !Number.isSafeInteger(candidate.rank) || candidate.rank<0 ||
    (candidate.limited_free_until_epoch_seconds!==undefined && (!Number.isSafeInteger(candidate.limited_free_until_epoch_seconds) ||
      candidate.limited_free_until_epoch_seconds<1)) ||
    (candidate.duration_ms!==undefined && (!Number.isSafeInteger(candidate.duration_ms) || candidate.duration_ms<1)))
    error('resource_candidate_invalid','resource candidate lacks stable identity, entitlement, terms, or ranking evidence',
      {candidate_id:candidate?.candidate_id??null});
  const hasDraftPath=typeof candidate.draft_path==='string';
  const hasDraftResourceId=typeof candidate.draft_resource_id==='string';
  if(hasDraftPath!==hasDraftResourceId || (hasDraftPath && (!path.isAbsolute(candidate.draft_path) ||
    !candidate.draft_resource_id.trim())) || (hasDraftPath && typeof candidate.local_path==='string'))
    error('resource_candidate_invalid','candidate materialization must be one file or one draft resource',
      {candidate_id:candidate.candidate_id});
}
function intersects(required,actual) {return !required.length || required.some(value=>actual.includes(value));}

/** 按创作目标和权益约束筛选候选，并保留每个接受/拒绝理由。 */
export function filterResourceCandidates(query,candidates) {
  validateQuery(query);
  if(!Array.isArray(candidates) || candidates.length>query.selection.maximum_candidates)
    error('resource_candidate_invalid','candidate collection is invalid or exceeds the query bound');
  const seen=new Set(),accepted=[],rejected=[];
  for(const candidate of candidates) {
    validateCandidate(candidate);
    if(seen.has(candidate.candidate_id) || seen.has(`resource:${candidate.resource_id}`))
      error('resource_candidate_invalid','candidate and resource identities must be unique',{candidate_id:candidate.candidate_id});
    seen.add(candidate.candidate_id); seen.add(`resource:${candidate.resource_id}`);
    const reasons=[];
    if(candidate.domain!==query.domain) reasons.push('domain_mismatch');
    const searchable=`${candidate.title} ${candidate.resource_id} ${candidate.styles.join(' ')}`.toLowerCase();
    if(query.keywords.length && !query.keywords.some(keyword=>searchable.includes(keyword.toLowerCase()))) reasons.push('keyword_mismatch');
    for(const [field,label] of [['styles','style'],['moods','mood'],['tempos','tempo'],['aspect_ratios','aspect_ratio']])
      if(!intersects(query.filters[field]??[],candidate[field])) reasons.push(`${label}_mismatch`);
    if(query.filters.edition!=='any' && candidate.edition!==query.filters.edition) reasons.push(`edition_mismatch:${query.filters.edition}`);
    if(candidate.edition==='unknown') reasons.push('edition_unknown');
    if(!candidate.allowed_usages.includes(query.filters.usage)) reasons.push(`usage_not_allowed:${query.filters.usage}`);
    if(!candidate.channels.includes(query.filters.channel)) reasons.push(`channel_not_allowed:${query.filters.channel}`);
    if(query.filters.minimum_duration_ms!==undefined &&
      (!Number.isSafeInteger(candidate.duration_ms) || candidate.duration_ms<query.filters.minimum_duration_ms))
      reasons.push('duration_below_minimum');
    if(query.filters.maximum_duration_ms!==undefined &&
      (!Number.isSafeInteger(candidate.duration_ms) || candidate.duration_ms>query.filters.maximum_duration_ms))
      reasons.push('duration_above_maximum');
    if(candidate.cost_microunits>query.filters.maximum_cost_microunits) reasons.push('cost_exceeds_budget');
    if(candidate.limited_free_until_epoch_seconds!==undefined &&
      candidate.limited_free_until_epoch_seconds<(query.filters.at_epoch_seconds??Math.floor(Date.now()/1000)))
      reasons.push('limited_free_expired');
    if(candidate.preview_only) reasons.push('preview_only');
    (reasons.length?rejected:accepted).push({candidate:structuredClone(candidate),
      reasons:reasons.length?reasons:['domain_match','goal_match','usage_allowed','within_budget']});
  }
  accepted.sort((left,right)=>left.candidate.rank-right.candidate.rank||left.candidate.candidate_id.localeCompare(right.candidate.candidate_id));
  return {accepted,rejected};
}

function digest(value) {return crypto.createHash('sha256').update(canonical(value)).digest('hex');}

/** 只读观察安装显示、登录状态和账号权益；应用名称绝不推断账号版型。 */
export async function observeNativeEdition({adapter}={}) {
  const identity=adapter?.identity;
  if(!identity || typeof adapter.observeEdition!=='function' || typeof identity.editor_bundle!=='string' ||
    !identity.editor_bundle.trim() || typeof identity.editor_version!=='string' || !identity.editor_version.trim())
    error('native_edition_adapter_invalid','read-only native edition observer is required');
  rejectSecrets(identity,'$.adapter_identity');
  const observed=await adapter.observeEdition({read_only:true});
  rejectSecrets(observed,'$.observation');
  if(!observed || typeof observed.application_display_name!=='string' || !observed.application_display_name.trim() ||
    !['logged_in','logged_out','unknown'].includes(observed.login_state) ||
    !['basic','professional','unknown'].includes(observed.account_edition) ||
    !['active','expired','inactive','unknown'].includes(observed.entitlement_status) ||
    !strings(observed.capabilities??[],{allowEmpty:true}) || observed.source!=='gui_observed' ||
    typeof observed.observed_at!=='string' || !Number.isFinite(Date.parse(observed.observed_at)) ||
    (observed.expires_at!==undefined && (typeof observed.expires_at!=='string' || !Number.isFinite(Date.parse(observed.expires_at)))))
    error('native_edition_observation_invalid','edition observation is incomplete or ambiguous');
  const account={edition:observed.account_edition,status:observed.entitlement_status,
    capabilities:structuredClone(observed.capabilities??[]),source:observed.source,observed_at:observed.observed_at};
  if(observed.expires_at!==undefined) account.expires_at=observed.expires_at;
  const body={schema:'jianying-native-edition-observation/v1',application:{display_name:observed.application_display_name,
    bundle_id:identity.editor_bundle,version:identity.editor_version},session:{login_state:observed.login_state},account};
  return {...body,observation_digest:digest(body)};
}

/** 根据现场账号权益收紧官方资源查询；任何未知、过期或越权请求都暂停。 */
export function routeNativeResourceQuery(query,editionObservation) {
  validateQuery(query);
  rejectSecrets(editionObservation,'$.edition_observation');
  if(!editionObservation || editionObservation.schema!=='jianying-native-edition-observation/v1' ||
    typeof editionObservation.observation_digest!=='string' || !/^[0-9a-f]{64}$/.test(editionObservation.observation_digest))
    error('native_edition_observation_invalid','a digest-bound edition observation is required');
  const {observation_digest,...body}=editionObservation;
  if(digest(body)!==observation_digest)
    error('native_edition_observation_invalid','edition observation digest mismatch');
  const application=editionObservation.application,session=editionObservation.session,account=editionObservation.account;
  if(!application || typeof application.display_name!=='string' || !application.display_name.trim() ||
    typeof application.bundle_id!=='string' || !application.bundle_id.trim() ||
    typeof application.version!=='string' || !application.version.trim() ||
    !session || !['logged_in','logged_out','unknown'].includes(session.login_state) || !account ||
    !['basic','professional','unknown'].includes(account.edition) ||
    !['active','expired','inactive','unknown'].includes(account.status) ||
    !strings(account.capabilities??[],{allowEmpty:true}) || account.source!=='gui_observed' ||
    typeof account.observed_at!=='string' || !Number.isFinite(Date.parse(account.observed_at)))
    error('native_edition_observation_invalid','edition observation is incomplete');
  const validationTime=(query.filters.at_epoch_seconds??Math.floor(Date.now()/1000))*1000;
  const expired=account.expires_at!==undefined && (!Number.isFinite(Date.parse(account.expires_at)) ||
    Date.parse(account.expires_at)<=validationTime);
  if(session.login_state!=='logged_in' || account.edition==='unknown' || account.status!=='active' || expired)
    error('native_resource_edition_unavailable','official-resource account rights are not currently usable',
      {login_state:session.login_state,observed_edition:account.edition,entitlement_status:expired?'expired':account.status},
      ['sign in to Jianying if required','refresh the read-only edition observation','select a local licensed resource']);
  const requested=query.filters.edition;
  if(account.edition==='basic' && requested==='professional')
    error('native_resource_edition_unavailable','professional resource requested by a basic account',
      {requested_edition:requested,observed_edition:account.edition},
      ['choose a basic or currently valid limited-free resource','refresh a valid professional entitlement observation']);
  const routed=structuredClone(query);
  if(account.edition==='basic' && requested==='any') routed.filters.edition='basic';
  const capability=`official_assets.${routed.filters.edition==='any'?account.edition:routed.filters.edition}`;
  if(!account.capabilities.includes(capability))
    error('native_resource_edition_unavailable','observed account lacks the required official-resource capability',
      {required_capability:capability,observed_capabilities:structuredClone(account.capabilities)},
      ['refresh the read-only edition observation','select a local licensed resource']);
  return {schema:'jianying-native-resource-route/v1',query:routed,decision:{account_edition:account.edition,
    requested_edition:requested,routed_edition:routed.filters.edition,capability,observation_digest}};
}

function validateCatalogAdapter(adapter,catalog) {
  const identity=adapter?.identity;
  if(!identity || typeof adapter.listCatalog!=='function' || typeof adapter.observeEdition!=='function' || typeof identity.kind!=='string' ||
    typeof identity.editor_bundle!=='string' || typeof identity.editor_version!=='string' ||
    typeof identity.adapter_version!=='string') error('native_catalog_adapter_invalid','read-only native catalog adapter is required');
  rejectSecrets(identity,'$.adapter_identity');
  rejectSecrets(catalog,'$.capability_catalog');
  const editor=catalog?.editor_identity;
  if(!editor || editor.bundle_id!==identity.editor_bundle || editor.version!==identity.editor_version)
    error('native_catalog_identity_mismatch','catalog adapter does not match the observed editor identity');
}

/** 通过只读 Adapter 枚举普通原生资源域；隐藏、未知和缺失域保留为不可用事实。 */
export async function inventoryNativeResourceCatalogs({capabilityCatalog,adapter}={}) {
  if(!capabilityCatalog || capabilityCatalog.schema!=='jianying-native-capability-catalog/v1' ||
    !Array.isArray(capabilityCatalog.domains) || !Array.isArray(capabilityCatalog.unknown_domains))
    error('native_capability_catalog_invalid','native capability catalog is required');
  validateCatalogAdapter(adapter,capabilityCatalog);
  const editionObservation=await observeNativeEdition({adapter});
  const capabilityByDomain=new Map(capabilityCatalog.domains.map(item=>[item.domain,item]));
  const domains=[]; const seenResources=new Set();
  for(const domain of ORDINARY_DOMAINS) {
    const capability=capabilityByDomain.get(domain);
    if(!capability) {
      domains.push({domain,status:'unresolved',actions:[],candidates:[],evidence:{reason:'domain_not_enumerated'}});
      continue;
    }
    if(capability.visibility!=='visible') {
      domains.push({domain,status:capability.visibility==='hidden'?'unavailable':'unresolved',
        actions:structuredClone(capability.actions),candidates:[],evidence:{reason:`visibility:${capability.visibility}`}});
      continue;
    }
    if(!capability.actions.includes('search') || !capability.actions.includes('inspect'))
      error('native_catalog_action_missing',`${domain} lacks read-only search or inspect capability`);
    const listed=await adapter.listCatalog({domain,read_only:true});
    if(!listed || !Array.isArray(listed.candidates) || !listed.evidence || typeof listed.evidence.observed_at!=='string' ||
      !Number.isFinite(Date.parse(listed.evidence.observed_at)))
      error('native_catalog_evidence_invalid',`${domain} catalog lacks candidates or observation evidence`);
    rejectSecrets(listed.evidence,`$.catalog.${domain}.evidence`);
    const candidates=listed.candidates.map(candidate=>{
      validateCandidate(candidate);
      if(candidate.domain!==domain) error('resource_candidate_invalid',`${candidate.candidate_id} belongs to another domain`);
      if(seenResources.has(candidate.resource_id)) error('resource_candidate_invalid',`duplicate resource identity ${candidate.resource_id}`);
      seenResources.add(candidate.resource_id);
      const safe=structuredClone(candidate); delete safe.local_path;
      return safe;
    }).sort((left,right)=>left.rank-right.rank||left.resource_id.localeCompare(right.resource_id));
    domains.push({domain,status:'available',actions:structuredClone(capability.actions),candidates,
      evidence:structuredClone(listed.evidence)});
  }
  const body={schema:'jianying-native-resource-catalog/v1',editor_identity:structuredClone(capabilityCatalog.editor_identity),
    edition_observation:editionObservation,adapter_identity:structuredClone(adapter.identity),domains,
    unknown_domains:structuredClone(capabilityCatalog.unknown_domains)};
  return {...body,catalog_digest:digest(body)};
}

function validateUseRequirement(requirement) {
  if(!requirement || requirement.schema!=='jianying-native-resource-use/v1' || typeof requirement.request_id!=='string' ||
    !requirement.request_id.trim() || !DOMAINS.has(requirement.domain) || typeof requirement.resource_id!=='string' ||
    !requirement.resource_id.trim() || !USAGES.has(requirement.usage) || typeof requirement.channel!=='string' ||
    !requirement.channel.trim() || !requirement.target || typeof requirement.target!=='object' || Array.isArray(requirement.target) ||
    !requirement.context || typeof requirement.context!=='object' || Array.isArray(requirement.context) ||
    !Number.isSafeInteger(requirement.at_epoch_seconds) || requirement.at_epoch_seconds<1)
    error('native_resource_use_invalid','native resource use requirement is incomplete');
}
function validateRange(target,timeline) {
  if(!Number.isSafeInteger(target.start_ms) || target.start_ms<0 || !Number.isSafeInteger(target.duration_ms) ||
    target.duration_ms<1 || !Number.isSafeInteger(timeline?.duration_ms) || timeline.duration_ms<1 ||
    target.start_ms+target.duration_ms>timeline.duration_ms)
    error('native_resource_range_invalid','resource range must be positive and remain inside the timeline');
}

/** 在 Job 编译前执行逐域前置校验，拒绝相邻片段、用途、范围或画幅不明确的资源应用。 */
export function preflightNativeResourceUse({candidate,requirement,timeline}={}) {
  validateCandidate(candidate); validateUseRequirement(requirement);
  if(candidate.domain!==requirement.domain || candidate.resource_id!==requirement.resource_id)
    error('native_resource_identity_mismatch','resource requirement is not bound to the selected candidate');
  if(candidate.edition==='unknown') error('native_resource_edition_unknown','resource edition is unknown');
  if(candidate.limited_free_until_epoch_seconds!==undefined &&
    candidate.limited_free_until_epoch_seconds<requirement.at_epoch_seconds)
    error('native_resource_limited_free_expired','limited-free entitlement has expired');
  if(!candidate.allowed_usages.includes(requirement.usage))
    error('native_resource_usage_conflict',`${requirement.usage} use is not allowed`);
  if(!candidate.channels.includes(requirement.channel))
    error('native_resource_channel_conflict',`${requirement.channel} channel is not allowed`);
  const checks=['identity_bound','edition_known','usage_allowed','channel_allowed'];
  if(requirement.domain==='transition') {
    const adjacent=requirement.context.adjacent_segment_ids;
    if(!Array.isArray(adjacent) || adjacent.length!==2 || !strings(adjacent) || adjacent[0]===adjacent[1] ||
      !Number.isSafeInteger(requirement.context.cut_at_ms) || requirement.context.cut_at_ms<1 ||
      requirement.context.cut_at_ms>=timeline?.duration_ms)
      error('transition_adjacency_required','transition requires two distinct adjacent segments and an in-range cut point');
    checks.push('adjacent_segments_verified');
  } else if(['effect','filter','adjustment'].includes(requirement.domain)) {
    validateRange(requirement.target,timeline);
    const protectedIds=new Set(timeline?.protected_segment_ids??[]);
    const targetIds=requirement.target.segment_ids??[];
    if(!strings(targetIds,{allowEmpty:true}) || targetIds.some(id=>protectedIds.has(id)))
      error('native_resource_protected_target','effect range includes protected or invalid segments');
    checks.push('effect_range_verified','protected_content_excluded');
  } else if(requirement.domain==='template') {
    if(typeof requirement.target.aspect_ratio!=='string' || !candidate.aspect_ratios.includes(requirement.target.aspect_ratio))
      error('template_aspect_ratio_mismatch','template does not support the requested aspect ratio');
    checks.push('template_aspect_ratio_verified');
  } else if(['media','music','text','sticker','caption'].includes(requirement.domain)) {
    validateRange(requirement.target,timeline);
    checks.push(requirement.domain==='music'?'music_range_and_usage_verified':'placement_range_verified');
  }
  return {schema:'jianying-native-resource-use-preflight/v1',request_id:requirement.request_id,status:'ready',
    domain:requirement.domain,resource_id:requirement.resource_id,usage:requirement.usage,channel:requirement.channel,
    checks,requirement_digest:digest(requirement),candidate_digest:digest(candidate)};
}

function validateAdapter(adapter) {
  const identity=adapter?.identity;
  if(!identity || !['fake_gui','accessibility_adapter','visual_fallback'].includes(identity.kind) ||
    typeof identity.editor_bundle!=='string' || !identity.editor_bundle.trim() || typeof identity.editor_version!=='string' ||
    !identity.editor_version.trim() || typeof identity.adapter_version!=='string' || !identity.adapter_version.trim() ||
    typeof adapter.search!=='function' || typeof adapter.triggerDownload!=='function' || typeof adapter.inspectResource!=='function' ||
    typeof adapter.collectEvidence!=='function') error('native_adapter_invalid','version-bound native resource adapter is required');
}
function atomicJson(file,value) {
  fs.mkdirSync(path.dirname(file),{recursive:true});
  const temp=`${file}.${process.pid}.${crypto.randomUUID()}.tmp`;
  fs.writeFileSync(temp,`${JSON.stringify(value,null,2)}\n`,{mode:0o600}); fs.renameSync(temp,file);
}
function localIdentity(candidate) {
  if(typeof candidate.draft_path==='string' && typeof candidate.draft_resource_id==='string') {
    const draft=path.resolve(candidate.draft_path),contentPath=path.join(draft,'draft_content.json');
    let draftStat,contentStat,bytes,document;
    try {
      draftStat=fs.lstatSync(draft); contentStat=fs.lstatSync(contentPath);
      if(draftStat.isSymbolicLink() || !draftStat.isDirectory() || contentStat.isSymbolicLink() || !contentStat.isFile())
        error('resource_materialization_invalid','draft resource must use a regular isolated draft');
      bytes=fs.readFileSync(contentPath); document=JSON.parse(bytes);
    } catch(cause) {
      if(cause instanceof AdapterError) throw cause;
      error('resource_materialization_missing','draft resource cannot be inspected',
        {resource_id:candidate.resource_id,draft});
    }
    const matches=[];
    const visit=value=>{
      if(!value || typeof value!=='object') return;
      if(Array.isArray(value)) return value.forEach(visit);
      if(value.id===candidate.draft_resource_id) matches.push(value);
      Object.values(value).forEach(visit);
    };
    visit(document);
    if(matches.length!==1) error('resource_materialization_invalid',
      `draft resource ${candidate.draft_resource_id} matched ${matches.length} nodes`,
      {resource_id:candidate.resource_id,draft});
    return {kind:'draft_resource',resource_id:candidate.draft_resource_id,
      resource_sha256:crypto.createHash('sha256').update(canonical(matches[0])).digest('hex'),
      observed_draft_sha256:crypto.createHash('sha256').update(bytes).digest('hex')};
  }
  if(typeof candidate.local_path!=='string' || !candidate.local_path.trim())
    error('resource_materialization_missing','downloaded resource has no local materialization path',{resource_id:candidate.resource_id});
  let stat;
  try {stat=fs.lstatSync(candidate.local_path);} catch {
    error('resource_materialization_missing','downloaded resource path cannot be inspected',{resource_id:candidate.resource_id});
  }
  if(stat.isSymbolicLink() || !stat.isFile()) error('resource_materialization_invalid','downloaded resource must be a regular file',
    {resource_id:candidate.resource_id,path:candidate.local_path});
  const sha256=crypto.createHash('sha256').update(fs.readFileSync(candidate.local_path)).digest('hex');
  return {kind:'downloaded_file',file:{path:path.resolve(candidate.local_path),sha256,byte_length:stat.size}};
}
function ensureCliSuccess(result,operation) {
  if(result?.exitCode!==0 || result?.envelope?.ok!==true)
    error('official_resource_cli_failed',`released CLI ${operation} failed`,{operation,response:result?.envelope??null,exit_code:result?.exitCode??null},
      ['inspect the structured CLI error','do not apply the resource until registration and preflight pass']);
}

/** 执行“检索→筛选→下载→落地→CLI 注册与预检”的可恢复资源取得链。 */
export async function acquireOfficialResource({query,adapter,cliRunner=runJsonCommand,entitlementPath,stateRoot,
  poll={maximum_attempts:10,interval_ms:250},atEpochSeconds}={}) {
  validateQuery(query); validateAdapter(adapter);
  if(typeof entitlementPath!=='string' || !entitlementPath.trim() || typeof stateRoot!=='string' || !stateRoot.trim() ||
    !Number.isSafeInteger(poll.maximum_attempts) || poll.maximum_attempts<1 || poll.maximum_attempts>100 ||
    !Number.isSafeInteger(poll.interval_ms) || poll.interval_ms<0 || poll.interval_ms>60000)
    error('resource_acquisition_invalid','entitlement, state root, and bounded polling policy are required');
  const candidates=await adapter.search(structuredClone(query));
  const filtered=filterResourceCandidates(query,candidates);
  if(!filtered.accepted.length) error('resource_candidate_unavailable','no official resource satisfies the query and usage gates',
    {request_id:query.request_id,rejected:filtered.rejected});
  let selected=structuredClone(filtered.accepted[0].candidate);
  const downloadTrace=[{attempt:0,state:selected.download_state}];
  if(selected.download_state==='failed') error('resource_download_failed','selected resource is already in failed state',{resource_id:selected.resource_id});
  if(selected.download_state==='ambiguous') error('resource_download_ambiguous','selected resource download state is ambiguous',{resource_id:selected.resource_id});
  if(selected.download_state!=='downloaded') await adapter.triggerDownload(structuredClone(selected));
  for(let attempt=1; selected.download_state!=='downloaded' && attempt<=poll.maximum_attempts; attempt+=1) {
    selected=await adapter.inspectResource(structuredClone(selected)); validateCandidate(selected);
    downloadTrace.push({attempt,state:selected.download_state,failure_code:selected.failure_code??null});
    if(selected.download_state==='failed') error('resource_download_failed','official resource download failed',
      {resource_id:selected.resource_id,failure_code:selected.failure_code??'unknown'});
    if(selected.download_state==='ambiguous') error('resource_download_ambiguous','official resource download outcome is ambiguous',
      {resource_id:selected.resource_id});
    if(selected.download_state!=='downloaded' && attempt<poll.maximum_attempts && poll.interval_ms)
      await new Promise(resolve=>setTimeout(resolve,poll.interval_ms));
  }
  if(selected.download_state!=='downloaded') error('resource_download_timeout','official resource did not materialize within the bounded wait',
    {resource_id:selected.resource_id,attempts:poll.maximum_attempts});
  const observation=await adapter.collectEvidence(structuredClone(selected));
  rejectSecrets(observation,'$.observation');
  if(!observation || observation.resource_id!==selected.resource_id || typeof observation.observed_at!=='string' ||
    !Number.isFinite(Date.parse(observation.observed_at))) error('native_action_evidence_invalid','adapter evidence is not bound to the selected resource');
  const acquiredAt=atEpochSeconds??Math.floor(Date.parse(observation.observed_at)/1000);
  if(!Number.isSafeInteger(acquiredAt) || acquiredAt<1) error('native_action_evidence_invalid','resource acquisition time is invalid');
  const receipt={schema_version:'jianying-official-resource-receipt/v1',asset_id:selected.resource_id,title:selected.title,
    resource_kind:RESOURCE_KIND[selected.domain]??selected.domain,tier:selected.edition==='professional'?'professional':'basic',
    identity:localIdentity(selected),acquired_at_epoch_seconds:acquiredAt,terms_reference:selected.terms_reference,
    allowed_usages:structuredClone(selected.allowed_usages),restrictions:structuredClone(selected.restrictions),preview_only:selected.preview_only};
  const evidence={schema:'jianying-native-action-evidence/v1',action:'download',semantic_id:`${selected.domain}.resource.download`,
    resource_id:selected.resource_id,adapter_identity:structuredClone(adapter.identity),observation:structuredClone(observation),
    observed_at:observation.observed_at,outcome:'succeeded'};
  const requestRoot=path.join(path.resolve(stateRoot),query.request_id);
  const receiptPath=path.join(requestRoot,'official-resource-receipt.json');
  const preflightPath=path.join(requestRoot,'official-resource-preflight.json');
  const acquisitionPath=path.join(requestRoot,'native-resource-acquisition.json');
  const storeRoot=path.join(path.resolve(stateRoot),'receipts');
  atomicJson(receiptPath,receipt);
  const common=['--entitlement',path.resolve(entitlementPath),'--usage',query.filters.usage,'--store-root',storeRoot];
  if(atEpochSeconds!==undefined) common.push('--at',String(atEpochSeconds));
  const materialArgs=receipt.identity.kind==='draft_resource'?['--draft',path.resolve(selected.draft_path)]:
    [receipt.identity.file.path];
  const register=cliRunner({args:['media','official','register',receiptPath,...materialArgs,...common],
    requiredCapabilities:['media.official_resource']});
  ensureCliSuccess(register,'register');
  const requirement={asset_id:selected.resource_id,usage:query.filters.usage};
  if(receipt.identity.kind==='draft_resource') requirement.draft=path.resolve(selected.draft_path);
  else requirement.resource=receipt.identity.file.path;
  const preflight={schema_version:'jianying-official-resource-preflight/v1',requirements:[requirement]};
  atomicJson(preflightPath,preflight);
  const preflightArgs=['media','official','preflight',preflightPath,'--entitlement',path.resolve(entitlementPath),'--store-root',storeRoot];
  if(atEpochSeconds!==undefined) preflightArgs.push('--at',String(atEpochSeconds));
  const checked=cliRunner({args:preflightArgs,requiredCapabilities:['media.official_resource']});
  ensureCliSuccess(checked,'preflight');
  const result={schema:'jianying-native-resource-acquisition/v1',request_id:query.request_id,state:'ready',
    adapter:structuredClone(adapter.identity),candidates:filtered,selected,download_trace:downloadTrace,receipt,
    native_action_evidence:evidence,cli:{register:register.envelope.data,preflight:checked.envelope.data},
    artifacts:{receipt_path:receiptPath,preflight_path:preflightPath,acquisition_path:acquisitionPath,store_root:storeRoot}};
  rejectSecrets(result,'$.acquisition');
  atomicJson(acquisitionPath,result);
  return result;
}
