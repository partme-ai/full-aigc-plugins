import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { loadPlanningData, planVideo } from "../scripts/video_planner.mjs";

const root = process.env.JIANYING_TEST_PLANNING_SKILL ??
  path.resolve(import.meta.dirname, "../skills/jianying-draft-video-planning");
const data = loadPlanningData({ developmentSkillRoot: root });
const caps = JSON.parse(fs.readFileSync(path.join(root,"references/cli-capability-snapshot.json")));
for (const scene of data.catalog.scenes) {
  test(scene.id + " routes its own example and enforces media/native gates", () => {
    const input = {schema:"jianying-video-intent/v1", scene_id:scene.id, delivery:"plan", channel:"custom", media:[], requested_features:[]};
    const result = planVideo(input, data);
    assert.equal(result.status,"planned");
    assert.equal(result.recipe_id,scene.recipe);
    assert.equal(result.example,scene.example);
    assert.deepEqual(result.beats,scene.beats);
    assert.equal(result.evidence_level,"plan");
    assert.equal(result.executable,false);
    assert.equal(planVideo({...input,delivery:"structural"}, data, caps).status,"waiting_input");
    const native = planVideo({...input,delivery:"native_export",media:["placeholder.mp4"]},data,caps);
    assert.equal(native.status,"blocked_capability");
    assert.ok(native.missing_capabilities.includes("render.native"));
  });
}
test("ambiguous wedding request requires selection",()=>{
  const r=planVideo({schema:"jianying-video-intent/v1",query:"婚礼",delivery:"plan"},data);
  assert.equal(r.status,"needs_selection");
  assert.ok(r.candidates.some(s=>s.id==="WD04"));
});
test("unknown scene, feature, schema and delivery reject",()=>{
  for(const change of [{scene_id:"UNKNOWN"},{requested_features:["magic"]},{schema:"v99"},{delivery:"finished"}]) {
    assert.throws(()=>planVideo({schema:"jianying-video-intent/v1",scene_id:"VG01",delivery:"plan",...change},data));
  }
});
test("selected TTS blocked only when executing, not globally",()=>{
  const request={schema:"jianying-video-intent/v1",scene_id:"VG01",delivery:"structural",media:["clip.mp4"],requested_features:["tts"]};
  const altered={...caps,capabilities:caps.capabilities.filter(c=>c.id!=="media.tts_local")};
  assert.equal(planVideo(request,data,altered).status,"blocked_capability");
  assert.equal(planVideo({...request,requested_features:[]},data,altered).status,"planned");
});
test("duplicate, unknown recipe and traversal fail during load",()=>{
  for(const mutation of [
    c=>c.scenes[1].id=c.scenes[0].id,
    c=>c.scenes[0].recipe="UNKNOWN",
    c=>c.scenes[0].example="../escape.md"
  ]) {
    const tmp=fs.mkdtempSync(path.join(os.tmpdir(),"jy-planning-negative-"));
    try {
      fs.cpSync(root,tmp,{recursive:true});
      const file=path.join(tmp,"references/video-taxonomy.json");
      const catalog=JSON.parse(fs.readFileSync(file)); mutation(catalog);
      fs.writeFileSync(file,JSON.stringify(catalog));
      assert.throws(()=>loadPlanningData({developmentSkillRoot:tmp}));
    } finally {fs.rmSync(tmp,{recursive:true,force:true});}
  }
});
test("default load cannot silently use a source checkout",()=>{
  const tmp=fs.mkdtempSync(path.join(os.tmpdir(),"jy-planning-lock-"));
  try {
    fs.writeFileSync(path.join(tmp,"skills.lock.json"),JSON.stringify({sources:[]}));
    assert.throws(()=>loadPlanningData({pluginRoot:tmp}),/planning_skill_not_locked/);
  } finally {fs.rmSync(tmp,{recursive:true,force:true});}
});

test("locked installed skill is used and modified content is rejected",()=>{
  const pluginRoot=path.resolve(import.meta.dirname,"..");
  const installed=loadPlanningData({pluginRoot});
  assert.equal(installed.provenance.kind,"locked_release");
  assert.equal(installed.catalog.scenes.length,108);
  const tmp=fs.mkdtempSync(path.join(os.tmpdir(),"jy-planning-integrity-"));
  try {
    fs.copyFileSync(path.join(pluginRoot,"skills.lock.json"),path.join(tmp,"skills.lock.json"));
    const skill=path.join(tmp,"skills/jianying-draft-video-planning");
    fs.cpSync(installed.skillRoot,skill,{recursive:true});
    fs.appendFileSync(path.join(skill,"examples/scenarios/tr01.md"),"\nmodified");
    assert.throws(()=>loadPlanningData({pluginRoot:tmp}),e=>e.code==="skill_digest_mismatch");
  } finally {fs.rmSync(tmp,{recursive:true,force:true});}
});
