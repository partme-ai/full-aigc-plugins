import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {AdapterError} from './runtime_adapter.mjs';
import {fail,sha256,canonical,parseStrictJson,validateSchema,safeFile,readBounded,boundedSkillDigest} from './workflow_data.mjs';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const NAME='jianying-draft-video-planning';
const INDEX='references/planning-catalog-v2.json';
const SCHEMA='references/planning-catalog-v2.schema.json';
// 正典合同来自 Skills；摘要固定，目录不能通过附带宽松 Schema 绕过消费者校验。
const SCHEMA_SHA256='3bf119648a947c7808de30f45a9ce3ebd9437d384ee2556e80f130d2b286e96a';
const BRIEF_SCHEMA=JSON.parse(fs.readFileSync(path.join(ROOT,'schemas/creative-brief.v1.schema.json'),'utf8'));

/** 显式 v2 读取；保持旧入口与固定种子合同不变。 */
export function loadOpenCatalog({pluginRoot=ROOT,developmentSkillRoot,limits={}}={}) {
  const bounds={maxIndexBytes:16*1024*1024,maxScenes:10000,maxExampleBytes:262144,...limits};
  for(const [key,n] of Object.entries(bounds)) {
    if(!['maxIndexBytes','maxScenes','maxExampleBytes'].includes(key) || !Number.isSafeInteger(n) || n<1 || n>64*1024*1024)
      fail('catalog_resource_limit','invalid administrator resource limit');
  }
  let root,source;
  if(developmentSkillRoot) root=path.resolve(developmentSkillRoot);
  else {
    const lock=parseStrictJson(readBounded(path.join(pluginRoot,'skills.lock.json'),1024*1024).toString('utf8'));
    source=lock.sources?.find(s=>s.package==='jianying-skills' && s.skills?.includes(NAME));
    if(!source || source.repo!=='https://github.com/full-aigc-skills/jianying-skills.git' || source.dest!=='skills/' ||
      !/^v\d+\.\d+\.\d+$/.test(source.ref??'') || !/^[a-f0-9]{40}$/.test(source.sha??'') ||
      !/^[a-f0-9]{64}$/.test(source.sha256?.[NAME]??'')) fail('invalid_skill_lock','canonical immutable skill lock required');
    if(fs.lstatSync(path.join(pluginRoot,'skills')).isSymbolicLink()) fail('catalog_path_invalid','symlink skills directory');
    root=path.join(pluginRoot,'skills',NAME);
  }
  // 先限制目录本身大小，再遍历完整性；缺新版资源有专用恢复信息。
  if(!fs.existsSync(path.join(root,INDEX))) fail('catalog_v2_unavailable','Install a compatible immutable Skills release, or explicitly select a development catalog');
  const indexBytes=readBounded(safeFile(root,INDEX,bounds.maxIndexBytes),bounds.maxIndexBytes);
  const schemaBytes=readBounded(safeFile(root,SCHEMA,262144),262144);
  if(sha256(schemaBytes)!==SCHEMA_SHA256) fail('unsupported_catalog_schema','catalog Schema differs from the pinned consumer contract');
  const catalog=parseStrictJson(indexBytes.toString('utf8'));
  if(catalog?.schema!=='jianying-planning-catalog/v2') fail('unsupported_catalog_schema','expected jianying-planning-catalog/v2');
  if(Array.isArray(catalog.scenes) && catalog.scenes.length===0) fail('catalog_empty','no scenes');
  if(Array.isArray(catalog.scenes) && catalog.scenes.length>bounds.maxScenes) fail('catalog_resource_limit','scene count exceeds configured bound');
  const schema=parseStrictJson(schemaBytes.toString('utf8'));
  for(const name of ['scenes','recipes','sources','domains','overlays','dimensions']) {
    const rows=catalog[name];
    if(Array.isArray(rows) && new Set(rows.map(x=>x?.id)).size!==rows.length) fail('catalog_identity_conflict',`duplicate ${name} ID`);
  }
  validateSchema(catalog,schema);
  if(!catalog.compatibility.consumer_contracts.includes('jianying-open-routing/v1'))
    fail('catalog_compatibility_mismatch','catalog does not declare support for this router');
  const refs=(values,known,label)=>{
    if(values.some(v=>!known.has(v))) fail('catalog_reference_invalid',`unknown ${label}: ${values.filter(v=>!known.has(v)).join(',')}`);
  };
  const sets=Object.fromEntries(['recipes','sources','domains','overlays'].map(k=>[k,new Set(catalog[k].map(x=>x.id))]));
  const dims=new Map(catalog.dimensions.map(d=>[d.id,new Set(d.values.map(v=>v.id))]));
  for(const dimension of catalog.dimensions)
    if(dims.get(dimension.id).size!==dimension.values.length) fail('catalog_identity_conflict',`${dimension.id}.values`);
  const identities=new Set();
  for(const scene of catalog.scenes) {
    for(const id of [scene.id,...scene.legacy_ids,...scene.aliases]) {
      const key=id.toLowerCase();
      if(identities.has(key)) fail('catalog_identity_conflict',id);
      identities.add(key);
    }
    refs([scene.primary_recipe_id],sets.recipes,'recipe');
    for(const [key,group] of [['domain_ids','domains'],['overlay_ids','overlays'],['source_ids','sources']]) refs(scene[key],sets[group],key);
    for(const [key,values] of Object.entries(scene.tags)) refs(values,dims.get(key)??new Set(),`tags.${key}`);
    safeFile(root,scene.example_path,bounds.maxExampleBytes);
    if(!developmentSkillRoot && scene.status==='test_fixture') fail('catalog_test_fixture','test content cannot be a production catalog');
  }
  for(const recipe of catalog.recipes) {
    refs(recipe.optional_overlays,sets.overlays,'recipe overlays'); refs(recipe.conflicts,sets.recipes,'recipe conflicts');
  }
  refs(catalog.compatibility.legacy_seed_ids,new Set(catalog.scenes.flatMap(s=>s.legacy_ids)),'legacy_seed_ids');
  for(const source of catalog.sources) {
    if(source.popularity.status==='measured' && !source.popularity.metrics.length) fail('catalog_schema_invalid','popularity claim lacks metrics');
  }
  if(Object.keys(catalog.metadata).some(k=>!k.includes('.'))) fail('catalog_schema_invalid','metadata must be namespaced');
  const digest=boundedSkillDigest(root,new Map([[INDEX,indexBytes],[SCHEMA,schemaBytes]]));
  if(source && digest!==source.sha256[NAME]) fail('skill_digest_mismatch','planning skill differs from lock');
  const provenance=source?{kind:'locked_release',ref:source.ref,commit:source.sha,digest}:
    {kind:'development_candidate',digest};
  return {catalog,provenance,skillRoot:root,catalogDigest:sha256(indexBytes)};
}

/** 有界读取创作简报；不探测简报中的媒体路径。 */
export function readCreativeBrief(file) {
  return parseStrictJson(readBounded(path.resolve(file),1024*1024).toString('utf8'));
}

/** 只做开放路由，不自称 WorkflowPlan 编译完成或已获准执行。 */
export function routeWorkflow(brief,data,{cursor}={}) {
  try {validateSchema(brief,BRIEF_SCHEMA);} catch(error) {
    if(error instanceof AdapterError) fail('invalid_brief',error.message);
    throw error;
  }
  if(new Set(brief.output_intents.map(o=>o.id)).size!==brief.output_intents.length) fail('invalid_brief','duplicate output IDs');
  if(brief.facts.some(f=>f.source==='observed' && (!f.source_ref.trim() || !f.observed_at?.trim())))
    fail('invalid_brief','observed facts require evidence reference and collection time');
  const catalog=data.catalog,blockers=[],questions=[];
  const dims=new Map(catalog.dimensions.map(d=>[d.id,new Set(d.values.map(v=>v.id))]));
  for(const [key,values] of [...Object.entries(brief.dimensions),...Object.entries(brief.constraints.tags??{})]) {
    if(!dims.has(key)) blockers.push({code:'unknown_dimension',field:key});
    else if(values.some(v=>!dims.get(key).has(v))) blockers.push({code:'unknown_dimension_value',field:key});
  }
  const domains=new Map(catalog.domains.map(d=>[d.id,d.name]));
  for(const id of [...brief.constraints.domain_ids??[],...brief.constraints.exclude_domain_ids??[]])
    if(!domains.has(id)) blockers.push({code:'unknown_domain',field:id});
  for(const output of brief.output_intents) {
    if(!['video','flat'].includes(output.format)) blockers.push({code:'unsupported_delivery_format',output_id:output.id,format:output.format});
  }
  const purposeDimension=catalog.dimensions.find(d=>d.id==='purpose');
  const selectedPurposes=new Set(brief.dimensions.purpose??[]);
  if(selectedPurposes.size && purposeDimension) {
    const purposeAliases=new Map(purposeDimension.values.flatMap(value=>[[value.id,value.id],[value.name,value.id]]));
    for(const output of brief.output_intents) {
      const purpose=purposeAliases.get(output.purpose);
      if(purpose && !selectedPurposes.has(purpose)) blockers.push({code:'purpose_conflict',output_id:output.id,purpose});
    }
  }
  const q=brief.intent.trim().toLowerCase();
  const matches=scene=>{
    const fields=[scene.id,...scene.legacy_ids,scene.name,...scene.aliases,...scene.applies_when,...scene.domain_ids.map(id=>domains.get(id))];
    return fields.some(v=>v.toLowerCase().includes(q));
  };
  const conflicts=scene=>{
    const result=[];
    if(brief.constraints.domain_ids?.some(id=>!scene.domain_ids.includes(id))) result.push('required_domain');
    if(brief.constraints.exclude_domain_ids?.some(id=>scene.domain_ids.includes(id))) result.push('excluded_domain');
    for(const [key,values] of Object.entries(brief.constraints.tags??{}))
      if(values.some(v=>!scene.tags[key]?.includes(v))) result.push(`required_tag:${key}`);
    return result;
  };
  const selected=(brief.scene_ids??[]).map(id=>{
    const scene=catalog.scenes.find(s=>[s.id,...s.legacy_ids,...s.aliases].includes(id));
    if(!scene) fail('unknown_scene',`unknown selected scene: ${id}`);
    return scene;
  });
  if(new Set(selected.map(s=>s.id)).size!==selected.length) fail('invalid_brief','same scene selected through multiple aliases');
  const excluded=catalog.scenes.filter(s=>conflicts(s).length);
  for(const s of selected) if(conflicts(s).length) blockers.push({code:'selected_scene_conflict',scene_id:s.id,reasons:conflicts(s)});
  const candidates=catalog.scenes.filter(s=>!conflicts(s).length && (!q || matches(s)));
  const score=scene=>Object.entries(brief.dimensions).reduce((n,[key,values])=>n+values.filter(v=>scene.tags[key]?.includes(v)).length,0);
  candidates.sort((a,b)=>score(b)-score(a)||(a.id<b.id?-1:a.id>b.id?1:0));
  if(!selected.length && q && candidates.length===1) selected.push(candidates[0]);
  const queryDigest=sha256(canonical(brief)); let offset=0;
  if(cursor!==undefined) {
    try {
      if(typeof cursor!=='string' || cursor.length>2048 || !/^[a-zA-Z0-9_-]+$/.test(cursor)) throw Error();
      const value=JSON.parse(Buffer.from(cursor,'base64url').toString('utf8'));
      if(value.catalog!==data.catalogDigest || value.query!==queryDigest || !Number.isSafeInteger(value.offset) ||
        value.offset<0 || value.offset>=candidates.length || value.offset%3!==0) throw Error();
      offset=value.offset;
    } catch {fail('invalid_cursor','cursor does not belong to this catalog/query');}
  }
  const next=offset+3<candidates.length?Buffer.from(JSON.stringify({catalog:data.catalogDigest,query:queryDigest,offset:offset+3})).toString('base64url'):null;
  let route=selected.length?(selected.length>1?'composed':'known'):q && !candidates.length?'proposed':null;
  let readiness=selected.length?'planned':route==='proposed'?'needs_review':'needs_selection';
  if(!selected.length) questions.push('请选择具体用途、案例或确认新的策略提案');
  if(selected.length && !(brief.media??[]).length) {
    readiness='needs_input'; questions.push('请提供素材清单；路径声明尚未经过媒体探测');
  }
  if(blockers.length) readiness=blockers.some(b=>b.code==='unsupported_delivery_format')?'capability_blocked':'needs_review';
  if(!candidates.length && excluded.length) readiness='needs_review';
  const recipes=[...new Set(selected.map(s=>s.primary_recipe_id))];
  for(const id of recipes) {
    const recipe=catalog.recipes.find(r=>r.id===id);
    if(recipe.conflicts.some(r=>recipes.includes(r))) {blockers.push({code:'recipe_conflict',recipe_id:id});readiness='needs_review';}
  }
  return {schema:'jianying-open-route/v1',request_id:brief.request_id,route,readiness,
    evidence_level:'plan',executable:false,production_ready:false,capability_check:'not_performed',
    provenance:data.provenance,catalog_ref:{schema:catalog.schema,catalog_id:catalog.catalog_id,revision:catalog.revision,digest:data.catalogDigest},
    selected_scenes:selected.map(s=>({id:s.id,name:s.name,example_path:s.example_path,recipe_id:s.primary_recipe_id,
      asset_requirements:s.asset_requirements,acceptance:s.acceptance,guardrails:s.guardrails,source_ids:s.source_ids})),
    recipes:catalog.recipes.filter(r=>recipes.includes(r.id)),
    candidates:candidates.slice(offset,offset+3).map(s=>({id:s.id,name:s.name,recipe_id:s.primary_recipe_id,
      reasons:[q?'query_match':'needs_purpose',...Object.keys(brief.dimensions).filter(k=>brief.dimensions[k].some(v=>s.tags[k]?.includes(v)))],
      asset_requirements:s.asset_requirements,source_ids:s.source_ids})),
    excluded:excluded.slice(0,3).map(s=>({id:s.id,reasons:conflicts(s)})),excluded_count:excluded.length,
    candidate_count:candidates.length,next_cursor:next,blockers,questions,
    proposal:route==='proposed'?{intent:brief.intent,requires_review:true,scene_id:null,
      strategy_candidates:catalog.recipes.slice(0,3).map(r=>({id:r.id,goal:r.goal}))}:null,
    next_steps:['verify actual media','confirm editorial selections','compile WorkflowPlan and Jobs separately','approve execution separately'],
    warnings:['Routing is not a compiled WorkflowPlan, executable Job, media analysis or export evidence.']};
}
