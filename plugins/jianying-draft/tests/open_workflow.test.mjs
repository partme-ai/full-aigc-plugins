import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {loadPlanningData, planVideo} from '../scripts/video_planner.mjs';

const ROOT = path.resolve(import.meta.dirname, '..');
const FIX = path.join(ROOT, 'tests/fixtures');
const json = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const hash = b => crypto.createHash('sha256').update(b).digest('hex');
const legacy = path.join(ROOT, 'skills/jianying-draft-video-planning');
const brief = (change={}) => ({schema:'jianying-creative-brief/v1',request_id:'test',
  intent:'生活 Vlog',constraints:{},dimensions:{},output_intents:[],facts:[],metadata:{},...change});

async function api() {
  const file = path.join(ROOT, 'scripts/open_workflow.mjs');
  assert.ok(fs.existsSync(file), 'open workflow runtime is not implemented');
  return import(file);
}

function fixture(t, count=1) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'jy-open-test-'));
  t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  fs.mkdirSync(path.join(root,'references'),{recursive:true});
  fs.mkdirSync(path.join(root,'examples/scenarios'),{recursive:true});
  fs.writeFileSync(path.join(root,'examples/scenarios/vg01.md'),'fixture');
  fs.copyFileSync(path.join(FIX,'open_catalog_v2.schema.json'),path.join(root,'references/planning-catalog-v2.schema.json'));
  const catalog=json(path.join(FIX,'open_catalog_v2.json'));
  const seed=structuredClone(catalog.scenes[0]);
  for(let i=1;i<count;i++) catalog.scenes.push({...structuredClone(seed),id:`scene.life.case_${i}`,legacy_ids:[],aliases:[],name:`案例 ${i}`});
  const file=path.join(root,'references/planning-catalog-v2.json');
  const save=()=>fs.writeFileSync(file,JSON.stringify(catalog));
  save(); return {root,file,catalog,save};
}

test('v1 frozen resources and all 108 routes retain their public meaning',()=>{
  const baseline=json(path.join(FIX,'legacy_planning_v1.json'));
  for(const [file,digest] of Object.entries(baseline.files)) assert.equal(hash(fs.readFileSync(path.join(legacy,file))),digest,file);
  const data=loadPlanningData();
  assert.equal(data.catalog.scenes.length,108);
  for(const s of data.catalog.scenes) {
    const r=planVideo({schema:'jianying-video-intent/v1',scene_id:s.id},data);
    assert.equal(r.scene_id,s.id); assert.equal(r.recipe_id,s.recipe);
    assert.equal(r.example,s.example); assert.equal(r.executable,false);
  }
  assert.throws(()=>planVideo({schema:'unknown'},data),e=>e.code==='invalid_intent');
});

test('dual resource package keeps old consumer at 108 and v2 sees entry 109',async t=>{
  const {loadOpenCatalog,routeWorkflow}=await api(); const f=fixture(t,109);
  fs.cpSync(legacy,f.root,{recursive:true}); f.save();
  assert.equal(loadPlanningData({developmentSkillRoot:f.root}).catalog.scenes.length,108);
  const newer=loadOpenCatalog({developmentSkillRoot:f.root});
  assert.equal(routeWorkflow(brief({scene_ids:['scene.life.case_108']}),newer).selected_scenes[0].id,'scene.life.case_108');
  const input=path.join(f.root,'legacy-intent.json'),state=path.join(f.root,'state');
  fs.writeFileSync(input,JSON.stringify({schema:'jianying-video-intent/v1',scene_id:'VG01'}));
  const r=spawnSync(process.execPath,[path.join(ROOT,'scripts/harness.mjs'),'plan-video',input,'--development-skill-root',f.root,'--state-root',state],
    {encoding:'utf8',env:{PATH:'/nonexistent',JIANYING_CLI_PATH:'/nonexistent'},timeout:10000});
  assert.equal(r.status,0,r.stdout+r.stderr);
  assert.equal(JSON.parse(r.stdout).data.scene_id,'VG01'); assert.equal(fs.existsSync(state),false);
});

for(const count of [1,109,1000]) test(`v2 indexes all ${count} entries without the old cardinality limit`,async t=>{
  const {loadOpenCatalog,routeWorkflow}=await api(); const f=fixture(t,count);
  const data=loadOpenCatalog({developmentSkillRoot:f.root});
  assert.equal(data.catalog.scenes.length,count);
  const r=routeWorkflow(brief(),data);
  assert.equal(r.executable,false); assert.equal(r.evidence_level,'plan');
  assert.equal(r.provenance.kind,'development_candidate');
  assert.equal(r.production_ready,false);
  const chosen=count===1?'VG01':`scene.life.case_${count-1}`;
  assert.equal(routeWorkflow(brief({scene_ids:[chosen]}),data).selected_scenes.length,1);
});

test('duplicate keys, aliases, paths, references, versions and limits fail closed',async t=>{
  const {loadOpenCatalog}=await api();
  for(const [mutate,code] of [
    [c=>c.scenes.push({...structuredClone(c.scenes[0]),id:'scene.life.second'}),'catalog_identity_conflict'],
    [c=>c.scenes[0].primary_recipe_id='absent','catalog_reference_invalid'],
    [c=>c.scenes[0].tags.purpose=['absent'],'catalog_reference_invalid'],
    [c=>c.scenes[0].example_path='../outside','catalog_path_invalid'],
    [c=>c.scenes[0].handler='shell','catalog_schema_invalid'],
    [c=>c.schema='v999','unsupported_catalog_schema'],
    [c=>c.compatibility.consumer_contracts=['future-router/v9'],'catalog_compatibility_mismatch'],
    [c=>c.scenes=[],'catalog_empty'],
  ]) {
    const f=fixture(t); mutate(f.catalog); f.save();
    assert.throws(()=>loadOpenCatalog({developmentSkillRoot:f.root}),e=>e.code===code,code);
  }
  const f=fixture(t);
  assert.throws(()=>loadOpenCatalog({developmentSkillRoot:f.root,limits:{maxIndexBytes:8}}),e=>e.code==='catalog_resource_limit');
  fs.writeFileSync(f.file,'{"schema":1,"schema":2}');
  assert.throws(()=>loadOpenCatalog({developmentSkillRoot:f.root}),e=>e.code==='catalog_duplicate_key');
  f.save(); const file=path.join(f.root,'examples/scenarios/vg01.md'); fs.unlinkSync(file); fs.symlinkSync(f.file,file);
  assert.throws(()=>loadOpenCatalog({developmentSkillRoot:f.root}),e=>e.code==='catalog_path_invalid');
});

test('old release fails v2 explicitly rather than falling back or changing its lock',async t=>{
  const {loadOpenCatalog}=await api(); const root=fs.mkdtempSync(path.join(os.tmpdir(),'jy-old-plugin-'));
  t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  const current=JSON.parse(fs.readFileSync(path.join(ROOT,'skills.lock.json'),'utf8'));
  const source=structuredClone(current.sources.find(item=>item.package==='jianying-skills'));
  source.ref='v2.1.0'; source.sha='1'.repeat(40); source.sha256['jianying-draft-video-planning']='2'.repeat(64);
  fs.writeFileSync(path.join(root,'skills.lock.json'),JSON.stringify({version:1,sources:[source]}));
  const target=path.join(root,'skills/jianying-draft-video-planning');
  fs.mkdirSync(path.dirname(target),{recursive:true});
  fs.cpSync(path.join(ROOT,'skills/jianying-draft-video-planning'),target,{recursive:true});
  fs.rmSync(path.join(target,'references/planning-catalog-v2.json'));
  fs.rmSync(path.join(target,'references/planning-catalog-v2.schema.json'));
  const lock=fs.readFileSync(path.join(root,'skills.lock.json'));
  assert.throws(()=>loadOpenCatalog({pluginRoot:root}),e=>e.code==='catalog_v2_unavailable');
  assert.deepEqual(fs.readFileSync(path.join(root,'skills.lock.json')),lock);
});

test('locked v2 fixture requires exact bytes and never falls back to development',async t=>{
  const {loadOpenCatalog}=await api();
  const {boundedSkillDigest}=await import('../scripts/workflow_data.mjs');
  const f=fixture(t); f.catalog.scenes[0].status='published_knowledge'; f.save();
  const install=path.join(f.root,'installed');
  const target=path.join(install,'skills/jianying-draft-video-planning');
  fs.mkdirSync(target,{recursive:true});
  fs.cpSync(path.join(f.root,'references'),path.join(target,'references'),{recursive:true});
  fs.cpSync(path.join(f.root,'examples'),path.join(target,'examples'),{recursive:true});
  const lock=json(path.join(ROOT,'skills.lock.json'));
  lock.sources[0].sha256['jianying-draft-video-planning']=boundedSkillDigest(target);
  fs.writeFileSync(path.join(install,'skills.lock.json'),JSON.stringify(lock));
  // 仅验证锁消费协议；这个人工组成的安装夹不是真实 Release 证据。
  assert.equal(loadOpenCatalog({pluginRoot:install}).provenance.kind,'locked_release');
  fs.appendFileSync(path.join(target,'examples/scenarios/vg01.md'),'tampered');
  assert.throws(()=>loadOpenCatalog({pluginRoot:install}),e=>e.code==='skill_digest_mismatch');
});

test('malformed objects and duplicate dimension values return structured failures',async t=>{
  const {loadOpenCatalog}=await api(); const f=fixture(t);
  fs.writeFileSync(f.file,'null');
  assert.throws(()=>loadOpenCatalog({developmentSkillRoot:f.root}),e=>e.code==='unsupported_catalog_schema');
  f.catalog.dimensions[0].values.push({id:'personal',name:'different label'}); f.save();
  assert.throws(()=>loadOpenCatalog({developmentSkillRoot:f.root}),e=>e.code==='catalog_identity_conflict');
});

test('catalog provenance hashes the bytes parsed even if index changes during loading',async t=>{
  const {loadOpenCatalog}=await api();
  const {boundedSkillDigest}=await import('../scripts/workflow_data.mjs');
  const f=fixture(t),expected=boundedSkillDigest(f.root);
  const original=fs.readSync; let changed=false;
  t.mock.method(fs,'readSync',function(...args) {
    const n=original.apply(this,args);
    if(!changed && n && args[1].subarray(0,n).toString().includes('"catalog_id":"test-catalog"')) {
      changed=true; f.catalog.revision='fixture-2'; f.save();
    }
    return n;
  });
  const result=loadOpenCatalog({developmentSkillRoot:f.root});
  assert.equal(changed,true); assert.equal(result.catalog.revision,'fixture-1');
  assert.equal(result.provenance.digest,expected);
});

test('a valid hard tag cannot hide an unknown preference value',async t=>{
  const {loadOpenCatalog,routeWorkflow}=await api(); const f=fixture(t);
  const r=routeWorkflow(brief({dimensions:{purpose:['not-registered']},constraints:{tags:{purpose:['personal']}},scene_ids:['VG01'],media:['declared.mp4']}),
    loadOpenCatalog({developmentSkillRoot:f.root}));
  assert.equal(r.readiness,'needs_review');
  assert.ok(r.blockers.some(b=>b.code==='unknown_dimension_value'));
});

test('explicit incompatible recipe selection asks review and does not compile',async t=>{
  const {loadOpenCatalog,routeWorkflow}=await api(); const f=fixture(t,2);
  f.catalog.recipes.push({...structuredClone(f.catalog.recipes[0]),id:'R02',conflicts:['R01']});
  f.catalog.scenes[1].primary_recipe_id='R02'; f.save();
  const r=routeWorkflow(brief({scene_ids:['VG01','scene.life.case_1'],media:['unread.mp4']}),loadOpenCatalog({developmentSkillRoot:f.root}));
  assert.equal(r.readiness,'needs_review'); assert.ok(r.blockers.some(b=>b.code==='recipe_conflict'));
});

test('known, composed, proposed and capability blocked stay separate',async t=>{
  const {loadOpenCatalog,routeWorkflow}=await api(); const f=fixture(t,2);
  f.catalog.scenes[1].primary_recipe_id='R02';
  f.catalog.recipes.push({...structuredClone(f.catalog.recipes[0]),id:'R02'}); f.save();
  const data=loadOpenCatalog({developmentSkillRoot:f.root});
  assert.equal(routeWorkflow(brief({scene_ids:['VG01']}),data).route,'known');
  assert.equal(routeWorkflow(brief({scene_ids:['VG01','scene.life.case_1']}),data).route,'composed');
  const unknown=routeWorkflow(brief({intent:'宠物成长故事'}),data);
  assert.equal(unknown.route,'proposed'); assert.deepEqual(unknown.selected_scenes,[]);
  assert.equal(unknown.readiness,'needs_review');
  const panoramic=routeWorkflow(brief({output_intents:[{id:'pano',purpose:'个人',format:'360',delivery:'native_export'}]}),data);
  assert.equal(panoramic.readiness,'capability_blocked'); assert.ok(panoramic.blockers.some(b=>b.code==='unsupported_delivery_format'));
});

test('hard constraints exclude, ambiguity asks, unknown dimensions are not invented',async t=>{
  const {loadOpenCatalog,routeWorkflow}=await api(); const f=fixture(t,8); const data=loadOpenCatalog({developmentSkillRoot:f.root});
  const r=routeWorkflow(brief({intent:'',constraints:{tags:{purpose:['commercial']}}}),data);
  assert.equal(r.candidates.length,0); assert.equal(r.readiness,'needs_review');
  const ambiguous=routeWorkflow(brief({intent:''}),data);
  assert.equal(ambiguous.readiness,'needs_selection'); assert.equal(ambiguous.candidates.length,3);
  const unknown=routeWorkflow(brief({dimensions:{unknown_axis:['unknown']}}),data);
  assert.equal(unknown.readiness,'needs_review'); assert.ok(unknown.blockers.some(b=>b.code==='unknown_dimension'));
  assert.throws(()=>routeWorkflow(brief({approval:true}),data),e=>e.code==='invalid_brief');
});

test('stable cursor covers catalog and rejects a changed query or catalog',async t=>{
  const {loadOpenCatalog,routeWorkflow}=await api(); const f=fixture(t,109); const data=loadOpenCatalog({developmentSkillRoot:f.root});
  const input=brief({intent:''}); const ids=[]; let cursor;
  do {const r=routeWorkflow(input,data,{cursor}); ids.push(...r.candidates.map(x=>x.id)); cursor=r.next_cursor;} while(cursor);
  assert.equal(new Set(ids).size,109); assert.equal(ids.length,109);
  const first=routeWorkflow(input,data);
  assert.deepEqual(routeWorkflow(input,data),first);
  assert.throws(()=>routeWorkflow(brief({intent:'changed'}),data,{cursor:first.next_cursor}),e=>e.code==='invalid_cursor');
  f.catalog.revision='changed'; f.save();
  assert.throws(()=>routeWorkflow(input,loadOpenCatalog({developmentSkillRoot:f.root}),{cursor:first.next_cursor}),e=>e.code==='invalid_cursor');
});

test('workflow-plan black box does not need CLI, media, model, or create task state',async t=>{
  const f=fixture(t); const file=path.join(f.root,'brief.json'); const state=path.join(f.root,'tasks');
  fs.writeFileSync(file,JSON.stringify(brief({scene_ids:['VG01'],media:['/not/readable/not-a-real-video.mp4']})));
  const r=spawnSync(process.execPath,[path.join(ROOT,'scripts/harness.mjs'),'workflow-plan',file,'--development-skill-root',f.root,'--state-root',state],
    {encoding:'utf8',env:{PATH:'/nonexistent',JIANYING_CLI_PATH:'/nonexistent',JIANYING_CLI_SHA256:'0'.repeat(64)},timeout:10000});
  assert.equal(r.status,0,r.stdout+r.stderr);
  const result=JSON.parse(r.stdout); assert.equal(result.ok,true); assert.equal(result.data.executable,false);
  assert.equal(result.data.readiness,'planned'); assert.equal(result.data.capability_check,'not_performed');
  assert.equal(result.data.workflow_plan.schema,'jianying-workflow-plan/v1');
  assert.equal(result.data.workflow_plan.assets[0].state,'declared');
  assert.equal(fs.existsSync(state),false);
});

test('observed facts require collection time and conflicting purposes require review',async t=>{
  const {loadOpenCatalog,routeWorkflow}=await api(); const f=fixture(t);
  const data=loadOpenCatalog({developmentSkillRoot:f.root});
  assert.throws(()=>routeWorkflow(brief({facts:[{name:'duration',value:'6s',source:'observed',source_ref:'probe-1',confirmed:true}]}),data),
    e=>e.code==='invalid_brief');
  const result=routeWorkflow(brief({scene_ids:['VG01'],media:['declared.mp4'],dimensions:{purpose:['personal']},
    output_intents:[{id:'ad',purpose:'commercial',format:'video',delivery:'editable_draft'}]}),data);
  assert.equal(result.readiness,'needs_review');
  assert.ok(result.blockers.some(item=>item.code==='purpose_conflict'));
});

test('workflow plan validates trusted typed DAG and derives selected requirements only',async t=>{
  const {loadOpenCatalog,routeWorkflow}=await api(); const f=fixture(t);
  const {buildWorkflowPlan,validateWorkflowPlan}=await import('../scripts/workflow_plan.mjs');
  const input=brief({scene_ids:['VG01'],media:['a.mp4'],
    output_intents:[{id:'main',purpose:'personal',format:'video',delivery:'editable_draft'}]});
  const route=routeWorkflow(input,loadOpenCatalog({developmentSkillRoot:f.root}));
  const plan=buildWorkflowPlan(input,route);
  assert.equal(plan.schema,'jianying-workflow-plan/v1');
  assert.equal(plan.revision,1);
  assert.deepEqual(plan.assets,[{asset_id:'asset-1',path:'a.mp4',state:'declared'}]);
  assert.deepEqual(plan.tool_requirements.capabilities,['timeline.audio_fade','timeline.edit','timeline.volume']);
  assert.ok(plan.risk_requirements.some(item=>item.type==='draft_write'));
  assert.equal(validateWorkflowPlan(plan).valid,true);
  const unsafe=structuredClone(plan); unsafe.steps[0].handler='/bin/sh';
  assert.throws(()=>validateWorkflowPlan(unsafe),e=>e.code==='unsupported_step_type');
  const cyclic=structuredClone(plan); cyclic.steps[0].depends_on=[cyclic.steps.at(-1).id];
  assert.throws(()=>validateWorkflowPlan(cyclic),e=>e.code==='workflow_graph_invalid');
});

test('workflow plan rejects duplicate producers and keeps outputs independently scoped',async t=>{
  const {loadOpenCatalog,routeWorkflow}=await api(); const f=fixture(t);
  const {buildWorkflowPlan,validateWorkflowPlan}=await import('../scripts/workflow_plan.mjs');
  const input=brief({scene_ids:['VG01'],media:['a.mp4'],output_intents:[
    {id:'private',purpose:'personal',format:'video',delivery:'editable_draft'},
    {id:'ad',purpose:'commercial',format:'video',delivery:'editable_draft'}]});
  const plan=buildWorkflowPlan(input,routeWorkflow(input,loadOpenCatalog({developmentSkillRoot:f.root})));
  assert.deepEqual(plan.outputs.map(o=>[o.output_id,o.purpose]),[['private','personal'],['ad','commercial']]);
  assert.notEqual(plan.outputs[0].target.logical_path,plan.outputs[1].target.logical_path);
  const duplicate=structuredClone(plan);
  duplicate.steps[1].outputs=structuredClone(duplicate.steps[0].outputs);
  assert.throws(()=>validateWorkflowPlan(duplicate),e=>e.code==='workflow_graph_invalid');
});

test('workflow plan rejects missing contracts and untyped or mismatched ports',async t=>{
  const {loadOpenCatalog,routeWorkflow}=await api(); const f=fixture(t);
  const {buildWorkflowPlan,validateWorkflowPlan}=await import('../scripts/workflow_plan.mjs');
  const input=brief({scene_ids:['VG01'],media:['a.mp4'],
    output_intents:[{id:'main',purpose:'personal',format:'video',delivery:'editable_draft'}]});
  const original=buildWorkflowPlan(input,routeWorkflow(input,loadOpenCatalog({developmentSkillRoot:f.root})));
  for(const mutate of [
    plan=>{delete plan.steps[0].retry;},
    plan=>{delete plan.steps[0].inputs[0].data_type;},
    plan=>{plan.steps[0].inputs[0].data_type='Untrusted';},
    plan=>{plan.steps[0].timeout_ms=0;},
  ]) {
    const candidate=structuredClone(original); mutate(candidate);
    assert.throws(()=>validateWorkflowPlan(candidate),e=>e.code==='workflow_plan_invalid');
  }
});
