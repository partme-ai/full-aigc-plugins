import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

import {runJsonCommand} from './runtime_adapter.mjs';
import {canonical,fail,sha256,validateSchema} from './workflow_data.mjs';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const CATALOG_SCHEMA=JSON.parse(fs.readFileSync(path.join(ROOT,'schemas/timeline-control-catalog.v1.schema.json'),'utf8'));
const INVENTORY_SCHEMA=JSON.parse(fs.readFileSync(path.join(ROOT,'schemas/timeline-surface-inventory.v1.schema.json'),'utf8'));
const ROUTES=['draft_protocol','runtime_native','accessibility_adapter','visual_fallback'];
const COORDINATE_KEYS=new Set(['x','y','left','top','right','bottom','point','points','rect','bounds','coordinate',
  'coordinates','screen_coordinate','screen_coordinates']);

const required=(args,name)=>{
  const value=args?.[name];
  if(value===undefined || value===null || (typeof value==='string' && !value.trim()))
    fail('control_arguments_invalid',`missing ${name}`);
  return String(value);
};
const requiredObject=(args,name)=>{
  const value=args?.[name];
  if(!value || typeof value!=='object' || Array.isArray(value))
    fail('control_arguments_invalid',`${name} must be an object`);
  return value;
};
const flag=(argv,name,value)=>{if(value!==undefined && value!==null) argv.push(name,String(value));};
const booleanFlag=(argv,name,value)=>{if(value===true) argv.push(name);};

function addTimelineItemArgs(args) {
  const resource=requiredObject(args,'resource');
  const target=requiredObject(args,'target_timerange');
  const draft=required(args,'draft');
  const kind=required(resource,'kind');
  if(kind==='segment') {
    const track=typeof args.track==='string'?args.track:required(requiredObject(args,'track'),'id');
    const segment=requiredObject(resource,'segment');
    return ['timeline','add-segment',draft,track,canonical(segment)];
  }
  if(!['video','image','audio'].includes(kind))
    fail('control_arguments_invalid',`unsupported timeline item kind ${kind}`);
  const argv=['media',kind==='audio'?'add-audio':'add-video',draft,required(resource,'source'),required(target,'start')];
  if(target.duration!==undefined && target.duration!==null) argv.push(String(target.duration));
  const trackName=typeof args.track==='string'?args.track:args.track?.name;
  flag(argv,'--track-name',trackName);
  if(kind==='audio') flag(argv,'--volume',resource.volume);
  return argv;
}

const DIRECT_BUILDERS=new Map([
  ['timeline.item.add',addTimelineItemArgs],
  ['timeline.segment.split',args=>['timeline','split',required(args,'draft'),required(args,'segment_id'),required(args,'at')]],
  ['timeline.segment.trim_left',args=>['timeline','trim',required(args,'draft'),required(args,'segment_id'),
    required(args,'source_start'),required(args,'duration')]],
  ['timeline.segment.trim_right',args=>['timeline','trim',required(args,'draft'),required(args,'segment_id'),
    required(args,'source_start'),required(args,'duration')]],
  ['timeline.segment.edge_trim',args=>['timeline','trim',required(args,'draft'),required(args,'segment_id'),
    required(args,'source_start'),required(args,'duration')]],
  ['timeline.segment.duplicate',args=>{
    const argv=['timeline','duplicate',required(args,'draft'),required(args,'segment_id')];
    flag(argv,'--track',args.track); booleanFlag(argv,'--new-track',args.new_track);
    booleanFlag(argv,'--dry-run',args.dry_run); return argv;
  }],
  ['timeline.track.add',args=>['timeline','add-track',required(args,'draft'),required(args,'kind'),required(args,'name')]],
  ['timeline.segment.move',args=>['timeline','move',required(args,'draft'),required(args,'segment_id'),required(args,'offset')]],
  ['timeline.segment.delete',args=>{
    const argv=['timeline','remove',required(args,'draft'),required(args,'segment_id')];
    booleanFlag(argv,'--keep-track',args.keep_track); booleanFlag(argv,'--keep-materials',args.keep_materials);
    booleanFlag(argv,'--dry-run',args.dry_run); return argv;
  }],
  ['timeline.keyframe.add',args=>{
    const argv=['timeline','keyframe',required(args,'draft'),required(args,'segment_id'),required(args,'property'),
      required(args,'time'),required(args,'value')]; flag(argv,'--easing',args.easing); return argv;
  }],
  ['timeline.filter.add',args=>{
    const argv=['timeline','add-filter',required(args,'draft'),required(args,'slug')];
    if(args.full===true) argv.push('--full');
    else {argv.push(required(args,'start'),required(args,'duration'));}
    flag(argv,'--intensity',args.intensity); flag(argv,'--track-name',args.track_name);
    booleanFlag(argv,'--jianying',args.jianying); flag(argv,'--resource-id',args.resource_id); flag(argv,'--effect-id',args.effect_id);
    return argv;
  }],
  ['timeline.effect.add',args=>{
    const argv=['timeline','add-effect',required(args,'draft'),required(args,'slug')];
    if(args.full===true) argv.push('--full');
    else {argv.push(required(args,'start'),required(args,'duration'));}
    flag(argv,'--intensity',args.intensity); flag(argv,'--track-name',args.track_name);
    if(args.params!==undefined) argv.push('--params',canonical(args.params));
    flag(argv,'--bind',args.bind_segment_id); booleanFlag(argv,'--jianying',args.jianying);
    flag(argv,'--resource-id',args.resource_id); flag(argv,'--effect-id',args.effect_id); return argv;
  }],
  ['timeline.transition.set',args=>{
    const argv=['timeline','transition',required(args,'draft'),required(args,'segment_id'),required(args,'slug')];
    flag(argv,'--duration',args.duration); booleanFlag(argv,'--jianying',args.jianying); return argv;
  }],
  ['track.cover.edit',args=>{
    const argv=['project','add-cover',required(args,'draft'),required(args,'cover_image')];
    flag(argv,'--time',args.time); return argv;
  }],
]);

function assertNoCoordinates(value,location='$') {
  if(!value || typeof value!=='object') return;
  if(Array.isArray(value)) {value.forEach((item,index)=>assertNoCoordinates(item,`${location}[${index}]`)); return;}
  for(const [key,item] of Object.entries(value)) {
    if(COORDINATE_KEYS.has(key.toLowerCase())) fail('coordinate_control_forbidden',`${location}.${key} is coordinate-bound`);
    assertNoCoordinates(item,`${location}.${key}`);
  }
}

function sameEditor(left,right) {
  return ['bundle_id','version','build','platform'].every(field=>left?.[field]===right?.[field]);
}

function validateCatalog(catalog) {
  try {validateSchema(catalog,CATALOG_SCHEMA);} catch(error) {fail('control_catalog_invalid',error.message);}
  assertNoCoordinates(catalog);
  if(catalog.route_priority.length!==ROUTES.length || catalog.route_priority.some((route,index)=>route!==ROUTES[index]))
    fail('control_catalog_invalid','route priority must prefer draft, runtime, accessibility, then visual fallback');
  const ids=new Set();
  for(const control of catalog.controls) {
    if(ids.has(control.semantic_id)) fail('control_catalog_invalid',`duplicate semantic ID ${control.semantic_id}`);
    ids.add(control.semantic_id);
    if(control.command!==null && typeof control.command!=='string') fail('control_catalog_invalid',`${control.semantic_id} command is invalid`);
    if(control.route==='draft_protocol' && control.status==='supported' && !DIRECT_BUILDERS.has(control.semantic_id)) {
      // 目录可以先于编译器扩展，但未知直接命令不能被静默执行。
      continue;
    }
    if(control.state_contract && (!['set','invoke'].includes(control.state_contract.operation) ||
      control.state_contract.readback_required!==true)) fail('control_catalog_invalid',`${control.semantic_id} state contract is invalid`);
  }
  return ids;
}

function validateInventory(inventory,catalog,controlIds) {
  try {validateSchema(inventory,INVENTORY_SCHEMA);} catch(error) {fail('surface_inventory_invalid',error.message);}
  assertNoCoordinates(inventory);
  if(!sameEditor(inventory.observed_editor,catalog.observed_editor))
    fail('surface_inventory_invalid','surface inventory editor identity differs from the control catalog');
  if(!Number.isSafeInteger(inventory.coverage.expected_surfaces) || inventory.coverage.expected_surfaces<1 ||
    inventory.coverage.expected_surfaces!==inventory.surfaces.length)
    fail('surface_inventory_invalid','surface count differs from the declared coverage');
  if(!Number.isSafeInteger(inventory.evidence.width) || !Number.isSafeInteger(inventory.evidence.height) ||
    inventory.evidence.width<1 || inventory.evidence.height<1)
    fail('surface_inventory_invalid','screenshot evidence dimensions are invalid');
  const regionCounts={}; const surfaceIds=new Set(); const semanticSurfaces=new Map();
  for(const surface of inventory.surfaces) {
    if(surfaceIds.has(surface.surface_id)) fail('surface_inventory_invalid',`duplicate surface ID ${surface.surface_id}`);
    surfaceIds.add(surface.surface_id);
    if(!controlIds.has(surface.semantic_id)) fail('surface_inventory_invalid',`unknown semantic ID ${surface.semantic_id}`);
    if(!Number.isSafeInteger(surface.visual_order) || surface.visual_order<1)
      fail('surface_inventory_invalid',`${surface.surface_id} has an invalid visual order`);
    regionCounts[surface.region]=(regionCounts[surface.region]??0)+1;
    const items=semanticSurfaces.get(surface.semantic_id)??[]; items.push(surface.surface_id); semanticSurfaces.set(surface.semantic_id,items);
  }
  for(const surface of inventory.surfaces) {
    if(surface.parent_surface_id!==undefined && (!surfaceIds.has(surface.parent_surface_id) ||
      surface.parent_surface_id===surface.surface_id))
      fail('surface_inventory_invalid',`${surface.surface_id} has an invalid parent surface`);
    if(surface.expansion) {
      const children=surface.expansion.child_surface_ids;
      if(surface.expansion.status==='enumerated' && children.length===0)
        fail('surface_inventory_invalid',`${surface.surface_id} is enumerated without children`);
      for(const childId of children) {
        const child=inventory.surfaces.find(candidate=>candidate.surface_id===childId);
        if(!child || child.parent_surface_id!==surface.surface_id)
          fail('surface_inventory_invalid',`${childId} is not a child of ${surface.surface_id}`);
        if(surface.expansion.status==='enumerated' &&
          (typeof child.accessibility_name!=='string' || !child.accessibility_name.trim()))
          fail('surface_inventory_invalid',`${childId} lacks an accessibility name`);
      }
    }
  }
  const declaredRegions=inventory.coverage.regions;
  if(Object.keys(declaredRegions).length!==Object.keys(regionCounts).length || Object.entries(declaredRegions).some(([region,count])=>
    !Number.isSafeInteger(count) || count<1 || regionCounts[region]!==count))
    fail('surface_inventory_invalid','observed region counts differ from declared coverage');
  if(Object.values(declaredRegions).reduce((sum,count)=>sum+count,0)!==inventory.coverage.expected_surfaces)
    fail('surface_inventory_invalid','declared region totals differ from expected surfaces');
  const expandable=inventory.surfaces.filter(surface=>surface.expansion);
  const enumerated=expandable.filter(surface=>surface.expansion.status==='enumerated');
  if(inventory.coverage.expandable_parents!==undefined &&
    (!Number.isSafeInteger(inventory.coverage.expandable_parents) ||
      inventory.coverage.expandable_parents!==expandable.length))
    fail('surface_inventory_invalid','declared expandable parent count differs from inventory');
  if(inventory.coverage.enumerated_parents!==undefined &&
    (!Number.isSafeInteger(inventory.coverage.enumerated_parents) ||
      inventory.coverage.enumerated_parents!==enumerated.length))
    fail('surface_inventory_invalid','declared enumerated parent count differs from inventory');
  return {regionCounts,semanticSurfaces};
}

/** 校验发布 CLI 的控制目录与逐入口 Surface Inventory，并保留重复语义实例。 */
export function validateNativeControlContracts({catalog,inventory}) {
  const controlIds=validateCatalog(catalog);
  const {regionCounts,semanticSurfaces}=validateInventory(inventory,catalog,controlIds);
  const duplicateSemantics=[...semanticSurfaces.entries()].filter(([,surfaceIds])=>surfaceIds.length>1)
    .map(([semantic_id,surface_ids])=>({semantic_id,surface_ids:[...surface_ids].sort()}))
    .sort((left,right)=>left.semantic_id.localeCompare(right.semantic_id));
  return {schema:'jianying-native-control-validation/v1',editor:structuredClone(inventory.observed_editor),
    surface_count:inventory.surfaces.length,region_counts:Object.fromEntries(Object.entries(regionCounts).sort()),
    screenshot_sha256:inventory.evidence.sha256,duplicate_semantics:duplicateSemantics,
    unresolved_surface_ids:inventory.surfaces.filter(surface=>surface.status==='unresolved').map(surface=>surface.surface_id).sort(),
    catalog_digest:sha256(canonical(catalog)),inventory_digest:sha256(canonical(inventory))};
}

function isExpandable(surface) {
  return Boolean(surface.expansion) || surface.surface_id.endsWith('.menu') || surface.semantic_id.endsWith('.context_menu') ||
    surface.semantic_id==='timeline.sequence.menu' || surface.semantic_id==='timeline.view.settings';
}

function expanded(inventory,surface) {
  if(surface.expansion) return surface.expansion.status==='enumerated';
  if(inventory.surfaces.some(candidate=>candidate.parent_surface_id===surface.surface_id)) return true;
  return surface.semantic_id==='timeline.view.settings' && inventory.surfaces.some(candidate=>candidate.region==='view_settings_popover');
}

/** 生成菜单、弹层、右键和未知入口的可机读覆盖缺口；存在缺口时禁止声称完整覆盖。 */
export function buildControlCoverageReport({catalog,inventory}) {
  const validation=validateNativeControlContracts({catalog,inventory});
  const gaps=[];
  for(const surface of inventory.surfaces) {
    if(surface.status==='unresolved') gaps.push({type:'unresolved_surface',surface_id:surface.surface_id,
      semantic_id:surface.semantic_id,region:surface.region,reason:surface.evidence});
    if(isExpandable(surface) && !expanded(inventory,surface)) gaps.push({type:'unexpanded_parent',surface_id:surface.surface_id,
      semantic_id:surface.semantic_id,region:surface.region,
      reason:surface.expansion?.evidence??'child actions are not enumerated for this editor version'});
  }
  for(const control of catalog.controls) {
    if(control.route==='draft_protocol' && control.status==='supported' && !DIRECT_BUILDERS.has(control.semantic_id)) {
      gaps.push({type:'compiler_mapping_missing',surface_id:null,semantic_id:control.semantic_id,region:null,
        reason:'released CLI exposes this direct control but the workflow compiler has no fixed argv mapping'});
    }
  }
  gaps.sort((left,right)=>String(left.surface_id??'').localeCompare(String(right.surface_id??''))||
    left.type.localeCompare(right.type));
  return {schema:'jianying-control-coverage-report/v1',editor:validation.editor,
    catalog_digest:validation.catalog_digest,inventory_digest:validation.inventory_digest,
    surface_count:validation.surface_count,region_counts:validation.region_counts,
    unresolved_surface_ids:validation.unresolved_surface_ids,gaps,can_claim_complete:gaps.length===0};
}

function assertCanary(canary,editor) {
  if(canary?.schema!=='jianying-control-canary/v1' || canary.status!=='passed' || !sameEditor(canary.editor,editor) ||
    !canary.adapter || typeof canary.adapter.kind!=='string' || typeof canary.adapter.version!=='string' ||
    !Number.isFinite(Date.parse(canary.observed_at??'')))
    fail('control_canary_required','an exact-version passed control canary is required');
}

function runtimeArgs(control,args,editor) {
  const operation=control.state_contract?.operation;
  if(operation==='set') {
    if(!Object.hasOwn(args,'value')) fail('control_arguments_invalid','runtime set requires value');
    return ['runtime','controls','set',control.semantic_id,'--value',canonical(args.value),'--bundle-id',editor.bundle_id,
      '--version',editor.version,'--build',editor.build];
  }
  if(operation==='invoke') return ['runtime','controls','invoke',control.semantic_id,'--arguments',canonical(args),
    '--bundle-id',editor.bundle_id,'--version',editor.version,'--build',editor.build];
  fail('runtime_readback_missing',`${control.semantic_id} has no executable state contract`);
}

/** 把语义控制请求编译为固定 CLI argv 或版本绑定 Runtime Control；从不接受屏幕坐标。 */
export function compileNativeControlPlan({requests,catalog,inventory,adapters={},canary=null}) {
  const validation=validateNativeControlContracts({catalog,inventory});
  if(!Array.isArray(requests) || requests.length===0) fail('control_request_invalid','at least one control request is required');
  const controls=new Map(catalog.controls.map(control=>[control.semantic_id,control]));
  const surfacesBySemantic=new Map();
  for(const surface of inventory.surfaces) {
    const items=surfacesBySemantic.get(surface.semantic_id)??[]; items.push(surface.surface_id); surfacesBySemantic.set(surface.semantic_id,items);
  }
  const requestIds=new Set();
  const steps=requests.map((request,index)=>{
    assertNoCoordinates(request);
    if(!request || typeof request.request_id!=='string' || !request.request_id.trim() || requestIds.has(request.request_id) ||
      typeof request.semantic_id!=='string' || !request.semantic_id.trim() || !request.arguments ||
      typeof request.arguments!=='object' || Array.isArray(request.arguments))
      fail('control_request_invalid','control request identity or arguments are invalid');
    requestIds.add(request.request_id);
    const control=controls.get(request.semantic_id);
    if(!control) fail('control_unknown',request.semantic_id);
    if(control.status==='unresolved') fail('control_unresolved',request.semantic_id);
    const route=[control.route,control.fallback_route].find(candidate=>adapters[candidate]===true);
    if(!route) fail('control_adapter_unavailable',`${request.semantic_id} requires ${control.route} or ${control.fallback_route}`);
    let args,readback=null;
    if(route==='draft_protocol') {
      if(control.status!=='supported') fail('control_not_supported',request.semantic_id);
      const builder=DIRECT_BUILDERS.get(request.semantic_id);
      if(!builder) fail('control_direct_mapping_missing',request.semantic_id);
      args=builder(request.arguments);
    } else {
      assertCanary(canary,inventory.observed_editor);
      if(!control.state_contract?.readback_required) fail('runtime_readback_missing',request.semantic_id);
      args=runtimeArgs(control,request.arguments,inventory.observed_editor);
      readback={field:control.state_contract.readback,required:true,operation:control.state_contract.operation};
    }
    return {step_id:`native-control-${String(index+1).padStart(2,'0')}`,request_id:request.request_id,
      semantic_id:request.semantic_id,route,capability:control.capability,status:control.status,
      surface_ids:[...(surfacesBySemantic.get(request.semantic_id)??[])].sort(),arguments:structuredClone(request.arguments),
      cli:{args,required_capabilities:[control.capability]},requires_state_readback:Boolean(readback),readback};
  });
  return {schema:'jianying-native-control-plan/v1',editor:validation.editor,
    catalog_digest:validation.catalog_digest,inventory_digest:validation.inventory_digest,
    can_execute:true,steps,coverage:buildControlCoverageReport({catalog,inventory})};
}

/** 对 Runtime Control 强制执行前后状态读取；无变化、缺字段或不匹配均进入不明确状态。 */
export async function verifyRuntimeControlExecution({step,adapter}) {
  if(!step?.requires_state_readback || !step.readback?.required || !adapter ||
    typeof adapter.readState!=='function' || typeof adapter.execute!=='function')
    fail('runtime_readback_missing','runtime control adapter and readback contract are required');
  const field=step.readback.field;
  const before=await adapter.readState(step,field);
  const execution=await adapter.execute(step);
  if(!execution || execution.status!=='applied') fail('runtime_control_ambiguous','runtime adapter did not confirm an applied action');
  const after=await adapter.readState(step,field);
  if(!before || typeof before!=='object' || !after || typeof after!=='object' || !Object.hasOwn(after,field))
    fail('runtime_readback_missing',`${field} was not returned after execution`);
  if(step.readback.operation==='set') {
    if(after[field]!==step.arguments.value) fail('runtime_state_mismatch',`${field} does not match the requested value`);
  } else if(canonical(before)===canonical(after)) fail('runtime_state_unchanged',`${field} did not change after invocation`);
  return {schema:'jianying-runtime-control-evidence/v1',request_id:step.request_id,semantic_id:step.semantic_id,
    status:'verified',before:structuredClone(before),after:structuredClone(after),execution:structuredClone(execution),
    evidence_digest:sha256(canonical({step,before,after,execution}))};
}

/** 只通过锁定发布 CLI 取得控制目录和 Surface Inventory。 */
export async function probeNativeControlContracts({cliRunner=runJsonCommand}={}) {
  const invoke=async args=>{
    const result=await cliRunner({args,requiredCapabilities:['runtime.control_catalog']});
    if(result?.exitCode!==0 || result?.envelope?.ok!==true)
      fail('control_catalog_probe_failed',result?.envelope?.error?.message??'released CLI control probe failed');
    return result.envelope.data;
  };
  const catalog=await invoke(['runtime','controls','list']);
  const inventory=await invoke(['runtime','controls','surfaces']);
  return {catalog,inventory,validation:validateNativeControlContracts({catalog,inventory}),
    coverage:buildControlCoverageReport({catalog,inventory})};
}
