import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
import { AdapterError } from "./runtime_adapter.mjs";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const NAME = "jianying-draft-video-planning";
const fail = (code, message) => { throw new AdapterError(code, message); };
const read = file => JSON.parse(fs.readFileSync(file, "utf8"));

function skillDigest(root) {
  const files = [];
  function walk(dir) {
    for (const entry of fs.readdirSync(dir, {withFileTypes:true})) {
      const file = path.join(dir,entry.name);
      if (entry.isSymbolicLink()) fail("invalid_catalog","skill symlinks forbidden");
      if (entry.isDirectory()) walk(file);
      else if (entry.isFile()) files.push(file);
      else fail("invalid_catalog","non-regular skill entry");
    }
  }
  if (fs.lstatSync(root).isSymbolicLink()) fail("invalid_catalog","skill root symlink forbidden");
  walk(root);
  // 与技能仓 canonical manifest 同一口径：归一换行 + 按相对路径字符串排序
  const entries=files.map(file=>({
    rel: path.relative(root,file).split(path.sep).join("/"),
    data: fs.readFileSync(file).toString("binary").replace(/\r\n/g,"\n"),
  })).sort((a,b)=>a.rel<b.rel?-1:a.rel>b.rel?1:0);
  const hash=crypto.createHash("sha256");
  for(const entry of entries) {
    hash.update(entry.rel); hash.update("\0");
    hash.update(crypto.createHash("sha256").update(Buffer.from(entry.data,"binary")).digest("hex")); hash.update("\n");
  }
  return hash.digest("hex");
}

/** 从已锁定技能加载内容；候选路径必须显式传入且在结果标记。 */
export function loadPlanningData({pluginRoot=ROOT, developmentSkillRoot}={}) {
  let skillRoot, provenance;
  if(developmentSkillRoot) {
    skillRoot=path.resolve(developmentSkillRoot);
    provenance={kind:"development_candidate",digest:skillDigest(skillRoot)};
  } else {
    const lock=read(path.join(pluginRoot,"skills.lock.json"));
    const source=lock.sources?.find(s=>s.package==="jianying-skills" && s.skills?.includes(NAME));
    if(!source) fail("planning_skill_not_locked","planning_skill_not_locked: import a canonical immutable skills release first");
    if(source.repo!=="https://github.com/full-aigc-skills/jianying-skills.git")
      fail("invalid_skill_lock","planning source must be canonical");
    skillRoot=path.resolve(pluginRoot,source.dest,NAME);
    const expectedRoot=path.resolve(pluginRoot,"skills",NAME);
    if(skillRoot!==expectedRoot || !/^v\d+\.\d+\.\d+$/.test(source.ref) || !/^[a-f0-9]{40}$/.test(source.sha??""))
      fail("invalid_skill_lock","invalid planning skill lock identity");
    const digest=skillDigest(skillRoot);
    if(digest!==source.sha256?.[NAME]) fail("skill_digest_mismatch","planning skill content differs from lock");
    provenance={kind:"locked_release",ref:source.ref,commit:source.sha,digest};
  }
  const catalog=read(path.join(skillRoot,"references/video-taxonomy.json"));
  const recipes=read(path.join(skillRoot,"references/edit-recipes.json"));
  const channels=read(path.join(skillRoot,"references/channel-profiles.json"));
  const sources=read(path.join(skillRoot,"references/source-index.json"));
  const snapshot=read(path.join(skillRoot,"references/cli-capability-snapshot.json"));
  const known=new Set(snapshot.capabilities.map(c=>c.id));
  if(catalog.schema!=="jianying-video-taxonomy/v1" || recipes.schema!=="jianying-edit-recipes/v1")
    fail("invalid_catalog","unknown planning data schema");
  if(catalog.scenes.length!==108 || new Set(catalog.scenes.map(s=>s.id)).size!==108 ||
     new Set(catalog.families).size!==18 || recipes.recipes.length!==12 ||
     new Set(recipes.recipes.map(r=>r.id)).size!==12 || sources.sources.length!==108 ||
     new Set(sources.sources.map(s=>s.id)).size!==108)
    fail("invalid_catalog","catalog IDs/counts are inconsistent");
  for(const family of catalog.families)
    if(catalog.scenes.filter(s=>s.family===family).length!==6) fail("invalid_catalog","family membership invalid");
  for(const scene of catalog.scenes) {
    if(!/^[A-Z]{2}\d{2}$/.test(scene.id) ||
       scene.example!=="examples/scenarios/"+scene.id.toLowerCase()+".md" ||
       !fs.existsSync(path.join(skillRoot,scene.example)))
      fail("invalid_catalog","invalid example path or ID");
    if(!recipes.recipes.some(r=>r.id===scene.recipe) || !sources.sources.some(s=>s.id===scene.source_id))
      fail("invalid_catalog","unknown recipe or source");
    if(!Array.isArray(scene.required_capabilities) || scene.required_capabilities.some(c=>!known.has(c)))
      fail("invalid_catalog","unknown capability reference");
  }
  for(const recipe of recipes.recipes) {
    const ids=[...recipe.required_capabilities,...Object.values(recipe.optional_capabilities).flat()];
    if(ids.some(c=>!known.has(c))) fail("invalid_catalog","unknown recipe capability");
  }
  return {catalog,recipes,channels,sources,skillRoot,provenance};
}

/** 只选型与预检；不理解媒体内容、不生成虚构时间码、不执行原生动作。 */
export function planVideo(intent,data,manifest) {
  if(!intent || intent.schema!=="jianying-video-intent/v1") fail("invalid_intent","unknown intent schema");
  const allowed=new Set(["schema","scene_id","query","delivery","channel","media","requested_features"]);
  if(Object.keys(intent).some(k=>!allowed.has(k))) fail("invalid_intent","unknown intent property");
  if(intent.scene_id!==undefined && (typeof intent.scene_id!=="string" || !/^[A-Z]{2}\d{2}$/.test(intent.scene_id)))
    fail("invalid_intent","scene_id must match the scene ID format");
  if(intent.scene_id && intent.query) fail("invalid_intent","choose scene_id or query, not both");
  const delivery=intent.delivery??"plan";
  if(!Object.hasOwn(data.recipes.delivery_capabilities,delivery)) fail("invalid_intent","unknown delivery");
  const channel=intent.channel??"custom";
  if(!data.channels.profiles.some(c=>c.id===channel)) fail("invalid_intent","unknown channel");
  const features=intent.requested_features??[];
  if(!Array.isArray(features) || features.some(f=>!["asr","tts","transitions","auto_caption_verification"].includes(f)))
    fail("invalid_intent","unknown requested feature");
  const media=intent.media??[];
  if(!Array.isArray(media) || media.some(m=>typeof m!=="string" || !m.trim()))
    fail("invalid_intent","media must be non-empty path strings when provided");
  let candidates;
  if(intent.scene_id) {
    candidates=data.catalog.scenes.filter(s=>s.id===intent.scene_id);
    if(!candidates.length) fail("unknown_scene","unknown scene ID");
  } else {
    if(intent.query!==undefined && typeof intent.query!=="string") fail("invalid_intent","query must be text");
    const q=(intent.query??"").trim().toLowerCase();
    candidates=q?data.catalog.scenes.filter(s=>(s.name+" "+s.family+" "+s.brief+" "+s.id).toLowerCase().includes(q)):data.catalog.scenes;
  }
  const base={schema:"jianying-video-plan/v1",evidence_level:"plan",executable:false,delivery,channel,provenance:data.provenance};
  if(candidates.length!==1) return {...base,status:candidates.length?"needs_selection":"waiting_input",
    candidates:candidates.map(s=>({id:s.id,name:s.name,brief:s.brief})),missing_inputs:candidates.length?["scene_id"]:["supported scene or clearer query"]};
  const scene=candidates[0],recipe=data.recipes.recipes.find(r=>r.id===scene.recipe);
  const required=delivery==="plan"?[]:[...new Set([
    ...scene.required_capabilities,...data.recipes.delivery_capabilities[delivery],
    ...features.flatMap(f=>recipe.optional_capabilities[f])
  ])];
  const support=new Set((manifest?.capabilities??[]).filter(c=>c.status==="supported").map(c=>c.id));
  const missing=required.filter(c=>!support.has(c));
  const missingInputs=delivery!=="plan" && !media.length?["media"]: [];
  const status=missingInputs.length?"waiting_input":missing.length?"blocked_capability":"planned";
  return {...base,status,scene_id:scene.id,scene_name:scene.name,recipe_id:recipe.id,example:scene.example,
    beats:scene.beats,editorial_choice:scene.edit,required_assets:scene.assets,acceptance:scene.acceptance,
    guardrails:[scene.guardrail],skills:scene.skills,human_steps:recipe.human_steps,
    source:data.sources.sources.find(s=>s.id===scene.source_id),
    required_capabilities:required,missing_capabilities:missing,missing_inputs:missingInputs,
    capability_check:manifest?"provided_manifest":"not_performed",
    next_steps:["probe actual media and confirm semantic selections","construct concrete job/v2 separately","approve writes and external execution separately"],
    warnings:["planned is not execution readiness; media paths/content/timing are not verified",
      "native export requires separate real-host approval and artifact evidence"]};
}
