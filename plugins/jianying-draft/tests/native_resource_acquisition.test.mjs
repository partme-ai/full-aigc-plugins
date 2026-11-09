import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import {fileURLToPath} from 'node:url';

import {
  acquireOfficialResource,
  filterResourceCandidates,
  inventoryNativeResourceCatalogs,
  observeNativeEdition,
  preflightNativeResourceUse,
} from '../scripts/native_resource_acquisition.mjs';
import {validateSchema} from '../scripts/workflow_data.mjs';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');

const query={
  schema:'jianying-native-resource-query/v1',request_id:'vlog-travel-music',domain:'music',keywords:['旅行','轻快'],
  filters:{styles:['vlog'],moods:['happy'],tempos:['upbeat'],aspect_ratios:['16:9'],edition:'professional',
    usage:'personal',channel:'douyin',minimum_duration_ms:10_000,maximum_duration_ms:180_000,
    maximum_cost_microunits:0,at_epoch_seconds:1_795_000_000},
  selection:{strategy:'ranked',maximum_candidates:10},
};

test('native capability and resource contracts have strict machine schemas',()=>{
  const fixtures=[
    ['native-edition-observation.v1.schema.json',{schema:'jianying-native-edition-observation/v1',
      application:{display_name:'剪映专业版',bundle_id:'com.lemon.lvpro',version:'11.5.13243'},
      session:{login_state:'unknown'},account:{edition:'unknown',status:'unknown',capabilities:[],
        source:'gui_observed',observed_at:'2026-09-22T01:00:00.000Z'},observation_digest:'a'.repeat(64)}],
    ['native-capability-catalog.v1.schema.json',{schema:'jianying-native-capability-catalog/v1',editor_identity:{},
      edition_observation:{},domains:[{domain:'music',visibility:'visible',edition:'mixed',
        actions:['search','filter','preview','download','apply','remove','inspect','recover'],evidence_level:'visual',
        raw_identifier:'tab.audio.music'}],unknown_domains:[]}],
    ['native-resource-query.v1.schema.json',query],
    ['resource-candidate.v1.schema.json',candidate()],
    ['native-action-evidence.v1.schema.json',{schema:'jianying-native-action-evidence/v1',action:'download',
      semantic_id:'music.resource.download',resource_id:'jy-music-travel-001',adapter_identity:{},observation:{},
      observed_at:'2026-09-21T10:00:00.000Z',outcome:'succeeded'}],
  ];
  for(const [name,value] of fixtures) {
    const schema=JSON.parse(fs.readFileSync(path.join(ROOT,'schemas',name),'utf8'));
    assert.equal(schema.additionalProperties,false);
    assert.doesNotThrow(()=>validateSchema(value,schema));
    assert.throws(()=>validateSchema({...value,unknown:true},schema),error=>error.code==='catalog_schema_invalid');
  }
});

test('read-only edition observation never infers account rights from the professional application name',async()=>{
  const calls=[];
  const adapter={identity:{kind:'fake_gui',editor_bundle:'com.lemon.lvpro',editor_version:'11.5.13243',adapter_version:'1'},
    async observeEdition({read_only}){calls.push({read_only}); return {application_display_name:'剪映专业版',
      login_state:'unknown',account_edition:'unknown',entitlement_status:'unknown',capabilities:[],
      source:'gui_observed',observed_at:'2026-09-22T01:00:00.000Z'};}};
  const observation=await observeNativeEdition({adapter});
  assert.deepEqual(calls,[{read_only:true}]);
  assert.equal(observation.application.display_name,'剪映专业版');
  assert.equal(observation.session.login_state,'unknown');
  assert.equal(observation.account.edition,'unknown');
  assert.equal(observation.account.status,'unknown');
  const schema=JSON.parse(fs.readFileSync(path.join(ROOT,'schemas/native-edition-observation.v1.schema.json'),'utf8'));
  assert.doesNotThrow(()=>validateSchema(observation,schema));
});

test('Harness routes official-resource queries by observed account rights and never silently downgrades',t=>{
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'jianying-native-resource-route-'));
  t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  const observationBody={schema:'jianying-native-edition-observation/v1',
    application:{display_name:'剪映专业版',bundle_id:'com.lemon.lvpro',version:'11.5.13243'},
    session:{login_state:'logged_in'},account:{edition:'basic',status:'active',
      capabilities:['official_assets.basic'],source:'gui_observed',observed_at:'2026-09-22T01:00:00.000Z'}};
  const normalize=value=>Array.isArray(value)?value.map(normalize):value&&typeof value==='object'?
    Object.fromEntries(Object.keys(value).sort().map(key=>[key,normalize(value[key])])):value;
  const observation={...observationBody,observation_digest:crypto.createHash('sha256')
    .update(JSON.stringify(normalize(observationBody))).digest('hex')};
  const queryPath=path.join(root,'query.json'),observationPath=path.join(root,'observation.json');
  fs.writeFileSync(observationPath,JSON.stringify(observation));
  fs.writeFileSync(queryPath,JSON.stringify({...query,filters:{...query.filters,edition:'any'}}));
  const routed=spawnSync(process.execPath,[path.join(ROOT,'scripts/harness.mjs'),'native-resource-route',queryPath,observationPath],
    {encoding:'utf8'});
  assert.equal(routed.status,0,routed.stdout||routed.stderr);
  const envelope=JSON.parse(routed.stdout);
  assert.equal(envelope.ok,true);
  assert.equal(envelope.data.query.filters.edition,'basic');
  assert.equal(envelope.data.decision.account_edition,'basic');

  fs.writeFileSync(queryPath,JSON.stringify(query));
  const blocked=spawnSync(process.execPath,[path.join(ROOT,'scripts/harness.mjs'),'native-resource-route',queryPath,observationPath],
    {encoding:'utf8'});
  assert.equal(blocked.status,1);
  const failure=JSON.parse(blocked.stdout);
  assert.equal(failure.ok,false);
  assert.equal(failure.error.type,'native_resource_edition_unavailable');
  assert.equal(failure.error.details.requested_edition,'professional');
  assert.equal(failure.error.details.observed_edition,'basic');
});

function candidate(overrides={}) {
  return {schema:'jianying-resource-candidate/v1',candidate_id:'music-travel-001',domain:'music',title:'旅行轻快日记',
    provider:'jianying_official',resource_id:'jy-music-travel-001',edition:'professional',download_state:'not_downloaded',
    styles:['vlog'],moods:['happy'],tempos:['upbeat'],aspect_ratios:['16:9'],channels:['douyin'],
    allowed_usages:['personal'],cost_microunits:0,terms_reference:'jianying://terms/music/jy-music-travel-001',
    restrictions:[],preview_only:false,rank:1,duration_ms:90_000,...overrides};
}

const ordinaryDomains=['media','music','text','sticker','effect','transition','caption','filter','adjustment','template'];

test('read-only catalog inventory covers all ordinary domains and preserves unavailable facts',async()=>{
  const capabilityCatalog={schema:'jianying-native-capability-catalog/v1',
    editor_identity:{bundle_id:'com.lemon.lvpro',version:'11.5.13243',build:'11.6.0-beta2',platform:'macos'},
    edition_observation:{edition:'professional',status:'active',source:'gui_observed'},
    domains:ordinaryDomains.map(domain=>({domain,visibility:domain==='adjustment'?'hidden':'visible',edition:'mixed',
      actions:['search','filter','preview','download','apply','remove','inspect','recover'],evidence_level:'visual',
      raw_identifier:`tab.${domain}`})),unknown_domains:[{raw_identifier:'tab.future'}]};
  const calls=[];
  const adapter={identity:{kind:'fake_gui',editor_bundle:'com.lemon.lvpro',editor_version:'11.5.13243',adapter_version:'1'},
    async observeEdition({read_only}){calls.push({domain:'edition',read_only}); return {
      application_display_name:'剪映专业版',login_state:'unknown',account_edition:'unknown',
      entitlement_status:'unknown',capabilities:[],source:'gui_observed',observed_at:'2026-09-22T01:00:00.000Z'};},
    async listCatalog({domain,read_only}){calls.push({domain,read_only}); return {candidates:[candidate({
      candidate_id:`${domain}-1`,resource_id:`jy-${domain}-1`,domain,title:`${domain} resource`,
      channels:['douyin'],aspect_ratios:['9:16']})],evidence:{observed_at:'2026-09-22T01:00:00.000Z',source:'fake_gui'}};}};
  const result=await inventoryNativeResourceCatalogs({capabilityCatalog,adapter});
  assert.equal(result.domains.length,10);
  assert.equal(result.domains.find(item=>item.domain==='adjustment').status,'unavailable');
  assert.equal(result.domains.find(item=>item.domain==='adjustment').candidates.length,0);
  assert.equal(calls.length,10);
  assert.ok(calls.every(call=>call.read_only===true));
  assert.equal(result.edition_observation.account.edition,'unknown');
  assert.equal(result.edition_observation.account.status,'unknown');
  assert.equal(result.catalog_digest.length,64);
  const schema=JSON.parse(fs.readFileSync(path.join(ROOT,'schemas/native-resource-catalog.v1.schema.json'),'utf8'));
  assert.doesNotThrow(()=>validateSchema(result,schema));
  const injected=structuredClone(result);
  injected.edition_observation.account.access_token='must-not-be-accepted';
  assert.throws(()=>validateSchema(injected,schema),error=>error.code==='catalog_schema_invalid');
});

test('domain preflight enforces transition adjacency, effect range, music usage and template aspect ratio',()=>{
  const baseRequirement={schema:'jianying-native-resource-use/v1',request_id:'use-1',usage:'personal',channel:'douyin',
    at_epoch_seconds:1_795_000_000,target:{start_ms:0,duration_ms:2_000},context:{}};
  const timeline={duration_ms:10_000,protected_segment_ids:['protected']};
  const music=preflightNativeResourceUse({candidate:candidate({download_state:'downloaded'}),
    requirement:{...baseRequirement,domain:'music',resource_id:'jy-music-travel-001'},timeline});
  assert.ok(music.checks.includes('music_range_and_usage_verified'));
  const transitionCandidate=candidate({candidate_id:'transition-1',resource_id:'transition-1',domain:'transition'});
  const transition=preflightNativeResourceUse({candidate:transitionCandidate,requirement:{...baseRequirement,domain:'transition',
    resource_id:'transition-1',context:{adjacent_segment_ids:['a','b'],cut_at_ms:3_000}},timeline});
  assert.ok(transition.checks.includes('adjacent_segments_verified'));
  const effectCandidate=candidate({candidate_id:'effect-1',resource_id:'effect-1',domain:'effect'});
  const effect=preflightNativeResourceUse({candidate:effectCandidate,requirement:{...baseRequirement,domain:'effect',
    resource_id:'effect-1',target:{start_ms:500,duration_ms:1_000,segment_ids:['a']}},timeline});
  assert.ok(effect.checks.includes('effect_range_verified'));
  const templateCandidate=candidate({candidate_id:'template-1',resource_id:'template-1',domain:'template',aspect_ratios:['9:16']});
  const template=preflightNativeResourceUse({candidate:templateCandidate,requirement:{...baseRequirement,domain:'template',
    resource_id:'template-1',target:{aspect_ratio:'9:16'}},timeline});
  assert.ok(template.checks.includes('template_aspect_ratio_verified'));
  const schema=JSON.parse(fs.readFileSync(path.join(ROOT,'schemas/native-resource-use-preflight.v1.schema.json'),'utf8'));
  for(const result of [music,transition,effect,template]) assert.doesNotThrow(()=>validateSchema(result,schema));
});

test('domain preflight rejects expired, usage-conflicting and context-free resources',()=>{
  const requirement={schema:'jianying-native-resource-use/v1',request_id:'reject-1',domain:'music',
    resource_id:'jy-music-travel-001',usage:'commercial',channel:'douyin',at_epoch_seconds:1_795_000_000,
    target:{start_ms:0,duration_ms:2_000},context:{}};
  assert.throws(()=>preflightNativeResourceUse({candidate:candidate(),requirement,timeline:{duration_ms:10_000}}),
    error=>error.code==='native_resource_usage_conflict');
  const expiredCandidate=candidate({limited_free_until_epoch_seconds:1_794_999_999});
  assert.throws(()=>preflightNativeResourceUse({candidate:expiredCandidate,requirement:{...requirement,usage:'personal'},
    timeline:{duration_ms:10_000}}),error=>error.code==='native_resource_limited_free_expired');
  const transitionCandidate=candidate({candidate_id:'transition-2',resource_id:'transition-2',domain:'transition'});
  assert.throws(()=>preflightNativeResourceUse({candidate:transitionCandidate,requirement:{...requirement,usage:'personal',
    domain:'transition',resource_id:'transition-2'},timeline:{duration_ms:10_000}}),
    error=>error.code==='transition_adjacency_required');
  const protectedEffect=candidate({candidate_id:'effect-2',resource_id:'effect-2',domain:'effect'});
  assert.throws(()=>preflightNativeResourceUse({candidate:protectedEffect,requirement:{...requirement,usage:'personal',
    domain:'effect',resource_id:'effect-2',target:{start_ms:0,duration_ms:1_000,segment_ids:['protected']}},
    timeline:{duration_ms:10_000,protected_segment_ids:['protected']}}),error=>error.code==='native_resource_protected_target');
});

test('candidate filtering preserves accepted and rejected reasons',()=>{
  const result=filterResourceCandidates(query,[
    candidate(),
    candidate({candidate_id:'commercial-only',resource_id:'commercial-only',allowed_usages:['commercial'],rank:2}),
    candidate({candidate_id:'wrong-mood',resource_id:'wrong-mood',moods:['sad'],rank:3}),
  ]);
  assert.deepEqual(result.accepted.map(item=>item.candidate.candidate_id),['music-travel-001']);
  assert.deepEqual(result.rejected.map(item=>item.candidate.candidate_id),['commercial-only','wrong-mood']);
  assert.ok(result.rejected[0].reasons.includes('usage_not_allowed:personal'));
  assert.ok(result.rejected[1].reasons.includes('mood_mismatch'));
});

test('unknown edition remains unavailable even when the query accepts either edition',()=>{
  const anyEdition=structuredClone(query); anyEdition.filters.edition='any';
  const result=filterResourceCandidates(anyEdition,[candidate({edition:'unknown'})]);
  assert.equal(result.accepted.length,0);
  assert.ok(result.rejected[0].reasons.includes('edition_unknown'));
});

test('expired limited-free and unknown resource domains fail closed',()=>{
  const expired=filterResourceCandidates(query,[candidate({limited_free_until_epoch_seconds:1_794_999_999})]);
  assert.equal(expired.accepted.length,0);
  assert.ok(expired.rejected[0].reasons.includes('limited_free_expired'));
  assert.throws(()=>filterResourceCandidates(query,[candidate({domain:'future_magic'})]),
    error=>error.code==='resource_candidate_invalid');
});

test('duration, channel and budget participate in combined filtering',()=>{
  const result=filterResourceCandidates(query,[
    candidate({candidate_id:'too-short',resource_id:'too-short',duration_ms:5_000}),
    candidate({candidate_id:'wrong-channel',resource_id:'wrong-channel',channels:['xiaohongshu']}),
    candidate({candidate_id:'paid',resource_id:'paid',cost_microunits:1}),
  ]);
  assert.deepEqual(result.rejected.map(item=>item.reasons),[
    ['duration_below_minimum'],['channel_not_allowed:douyin'],['cost_exceeds_budget'],
  ]);
});

test('not-downloaded official resource is acquired then registered and preflighted by released CLI contract',async t=>{
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'jianying-native-resource-')); t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  const mediaPath=path.join(root,'travel-music.m4a');
  const calls=[]; let inspections=0;
  const adapter={
    identity:{kind:'fake_gui',editor_bundle:'com.lemon.lvpro',editor_version:'11.5.13243',adapter_version:'1'},
    async search(){return [candidate()];},
    async triggerDownload(value){calls.push({kind:'download',resource_id:value.resource_id}); return {request_id:'download-1'};},
    async inspectResource(value){
      inspections+=1;
      if(inspections===1) return {...value,download_state:'downloading'};
      fs.writeFileSync(mediaPath,'fixture-official-music');
      return {...value,download_state:'downloaded',local_path:mediaPath};
    },
    async collectEvidence(value){return {surface_id:'music.recommended',resource_id:value.resource_id,
      entitlement_marker:'professional',observed_at:'2026-09-21T10:00:00.000Z'};},
  };
  const cliRunner=({args,requiredCapabilities})=>{
    calls.push({kind:'cli',args,requiredCapabilities});
    const command=args[2];
    return {exitCode:0,envelope:{ok:true,data:command==='register'?{status:'registered'}:{status:'ready'}}};
  };
  const entitlementPath=path.join(root,'entitlement.json'); fs.writeFileSync(entitlementPath,'{}');
  const result=await acquireOfficialResource({query,adapter,cliRunner,entitlementPath,stateRoot:path.join(root,'state'),
    poll:{maximum_attempts:3,interval_ms:0}});
  assert.equal(result.schema,'jianying-native-resource-acquisition/v1');
  assert.equal(result.state,'ready');
  assert.equal(result.selected.resource_id,'jy-music-travel-001');
  assert.deepEqual(result.download_trace.map(item=>item.state),['not_downloaded','downloading','downloaded']);
  assert.equal(result.receipt.identity.kind,'downloaded_file');
  assert.equal(result.receipt.identity.file.sha256,crypto.createHash('sha256').update('fixture-official-music').digest('hex'));
  assert.equal(calls.filter(item=>item.kind==='download').length,1);
  const cliCalls=calls.filter(item=>item.kind==='cli');
  assert.equal(cliCalls.length,2);
  assert.deepEqual(cliCalls.map(item=>item.args.slice(0,3)),[
    ['media','official','register'],['media','official','preflight'],
  ]);
  assert.ok(cliCalls.every(item=>item.requiredCapabilities.includes('media.official_resource')));
  assert.equal(fs.existsSync(result.artifacts.receipt_path),true);
  assert.equal(fs.existsSync(result.artifacts.preflight_path),true);
  assert.equal(fs.existsSync(result.artifacts.acquisition_path),true);
  const persisted=JSON.parse(fs.readFileSync(result.artifacts.acquisition_path,'utf8'));
  assert.deepEqual(persisted.candidates,result.candidates);
  assert.equal(persisted.selected.resource_id,result.selected.resource_id);
});

test('embedded effect acquisition hands a draft-resource identity to the Rust CLI without a fake file',async t=>{
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'jianying-native-draft-resource-'));
  t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  const draft=path.join(root,'draft'); fs.mkdirSync(draft,{recursive:true});
  const node={id:'effect-node-1',name:'科技感',resource_id:'remote-effect'};
  const draftBytes=Buffer.from(JSON.stringify({materials:{video_effects:[node]},tracks:[]}));
  fs.writeFileSync(path.join(draft,'draft_content.json'),draftBytes);
  const effectQuery={...query,request_id:'effect-draft-resource',domain:'effect',keywords:['科技'],
    filters:{...query.filters,styles:[],moods:[],tempos:[],aspect_ratios:[]}};
  const effectCandidate=candidate({candidate_id:'effect-candidate',domain:'effect',title:'科技感',
    resource_id:'jy-effect-1',download_state:'downloaded',styles:[],moods:[],tempos:[],aspect_ratios:[],
    draft_path:draft,draft_resource_id:'effect-node-1'});
  const calls=[];
  const adapter={identity:{kind:'fake_gui',editor_bundle:'com.lemon.lvpro',editor_version:'11.5.13243',adapter_version:'1'},
    async search(){return [effectCandidate];},async triggerDownload(){throw new Error('already materialized in draft');},
    async inspectResource(value){return value;},async collectEvidence(value){return {resource_id:value.resource_id,
      observed_at:'2026-09-21T10:00:00.000Z'};}};
  const cliRunner=({args})=>{calls.push(args); return {exitCode:0,envelope:{ok:true,data:
    args[2]==='register'?{status:'registered'}:{status:'ready'}}};};
  const entitlementPath=path.join(root,'entitlement.json'); fs.writeFileSync(entitlementPath,'{}');
  const result=await acquireOfficialResource({query:effectQuery,adapter,cliRunner,entitlementPath,
    stateRoot:path.join(root,'state'),poll:{maximum_attempts:1,interval_ms:0}});
  assert.equal(result.receipt.identity.kind,'draft_resource');
  assert.equal(result.receipt.identity.resource_id,'effect-node-1');
  assert.equal(result.receipt.identity.resource_sha256,crypto.createHash('sha256').update(JSON.stringify(node)).digest('hex'));
  assert.equal(result.receipt.identity.observed_draft_sha256,crypto.createHash('sha256').update(draftBytes).digest('hex'));
  assert.deepEqual(calls[0].slice(0,5),['media','official','register',result.artifacts.receipt_path,'--draft']);
  assert.equal(calls[0][5],draft);
  const preflight=JSON.parse(fs.readFileSync(result.artifacts.preflight_path,'utf8'));
  assert.equal(preflight.requirements[0].draft,draft);
  assert.equal(Object.hasOwn(preflight.requirements[0],'resource'),false);
});

test('download failure is structured and never falls through to CLI or another unapproved resource',async()=>{
  let cliCalled=false;
  const adapter={
    identity:{kind:'fake_gui',editor_bundle:'com.lemon.lvpro',editor_version:'11.5.13243',adapter_version:'1'},
    async search(){return [candidate()];},
    async triggerDownload(){return {request_id:'download-failed'};},
    async inspectResource(value){return {...value,download_state:'failed',failure_code:'network_unavailable'};},
    async collectEvidence(){throw new Error('must not collect evidence after failure');},
  };
  await assert.rejects(()=>acquireOfficialResource({query,adapter,entitlementPath:'/tmp/entitlement.json',
    stateRoot:'/tmp/unused',cliRunner:()=>{cliCalled=true;}}),error=>{
    assert.equal(error.code,'resource_download_failed');
    assert.equal(error.details.resource_id,'jy-music-travel-001');
    return true;
  });
  assert.equal(cliCalled,false);
});

test('missing usage or terms evidence fails closed before download',async()=>{
  let downloadCalled=false;
  const adapter={identity:{kind:'fake_gui',editor_bundle:'com.lemon.lvpro',editor_version:'11.5.13243',adapter_version:'1'},
    async search(){return [candidate({terms_reference:''})];},async triggerDownload(){downloadCalled=true;},
    async inspectResource(value){return value;},async collectEvidence(){return {};}};
  await assert.rejects(()=>acquireOfficialResource({query,adapter,entitlementPath:'/tmp/entitlement.json',
    stateRoot:'/tmp/unused',cliRunner:()=>{}}),error=>error.code==='resource_candidate_invalid');
  assert.equal(downloadCalled,false);
});

test('Adapter secrets are rejected before resource acquisition evidence is persisted',async t=>{
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'jianying-native-resource-secret-'));
  t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  const mediaPath=path.join(root,'secret.m4a');
  const adapter={identity:{kind:'fake_gui',editor_bundle:'com.lemon.lvpro',editor_version:'11.5.13243',adapter_version:'1'},
    async search(){return [candidate({download_state:'downloaded',local_path:mediaPath})];},
    async triggerDownload(){throw new Error('already downloaded');},
    async inspectResource(value){return value;},
    async collectEvidence(value){fs.writeFileSync(mediaPath,'secret fixture'); return {resource_id:value.resource_id,
      observed_at:'2026-09-21T10:00:00.000Z',access_token:'must-not-persist'};}};
  fs.writeFileSync(mediaPath,'secret fixture');
  await assert.rejects(()=>acquireOfficialResource({query,adapter,entitlementPath:path.join(root,'entitlement.json'),
    stateRoot:path.join(root,'state'),cliRunner:()=>{throw new Error('CLI must not run after secret evidence');}}),error=>{
    assert.equal(error.code,'native_resource_secret_persistence_forbidden');
    return true;
  });
  assert.equal(fs.existsSync(path.join(root,'state',query.request_id,'native-resource-acquisition.json')),false);
});

test('WorkflowPlan binds resource search, filtering and acquisition before compilation',async()=>{
  const {attachNativeResourceAcquisition,validateWorkflowPlan}=await import('../scripts/workflow_plan.mjs');
  const plan={schema:'jianying-workflow-plan/v1',workflow_id:'workflow-vlog',revision:1,
    catalog_ref:{schema:'jianying-planning-catalog/v2',digest:'c'.repeat(64)},tool_requirements:{capabilities:['timeline.edit']},
    brief:{request_id:'vlog'},assets:[],route:{kind:'known'},outputs:[],steps:[],limits:{maximum_revisions:3},
    risk_requirements:[],proof_requirements:[],metadata:{}};
  const bound=attachNativeResourceAcquisition(plan,query);
  assert.deepEqual(bound.steps.map(step=>step.type),['native_resource_search','native_resource_filter','native_resource_acquire']);
  assert.ok(bound.tool_requirements.capabilities.includes('media.official_resource'));
  assert.ok(bound.tool_requirements.capabilities.includes('media.audio'));
  assert.equal(validateWorkflowPlan(bound).valid,true);
  const bypass=structuredClone(bound); bypass.steps[2].depends_on=[];
  assert.throws(()=>validateWorkflowPlan(bypass),error=>error.code==='workflow_graph_invalid');
});

test('published CLI black box validates a five-domain Vlog resource plan',{
  skip:!process.env.JIANYING_PUBLISHED_CLI,
},async()=>{
  const executable=fs.realpathSync(process.env.JIANYING_PUBLISHED_CLI);
  const lock=JSON.parse(fs.readFileSync(path.join(ROOT,'runtime/jianying-cli.lock.json'),'utf8'));
  const platform=`${process.platform}-${process.arch}`;
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(executable)).digest('hex'),
    lock.artifacts[platform].binarySha256);
  const probe=spawnSync(executable,['capabilities','--json'],{encoding:'utf8'});
  assert.equal(probe.status,0,probe.stderr);
  const envelope=JSON.parse(probe.stdout),manifest=envelope.data;
  assert.equal(envelope.ok,true);
  assert.equal(manifest.cli_version,lock.resolvedVersion);
  assert.equal(manifest.release_ref,lock.releaseRef);
  assert.equal(manifest.source_commit,lock.sourceCommit);
  assert.equal(manifest.contract_state,'released');
  const statuses=Object.fromEntries(manifest.capabilities.map(item=>[item.id,item.status]));
  assert.equal(statuses['media.official_resource'],'supported');
  assert.equal(statuses['media.audio'],'supported');
  assert.equal(statuses['media.official_resource_apply'],'partial');

  const {attachNativeResourceAcquisition,validateWorkflowPlan}=await import('../scripts/workflow_plan.mjs');
  let plan={schema:'jianying-workflow-plan/v1',workflow_id:'workflow-vlog-five-domain',revision:1,
    catalog_ref:{schema:'jianying-planning-catalog/v2',digest:'c'.repeat(64)},
    tool_requirements:{capabilities:['timeline.edit']},brief:{request_id:'vlog-five-domain'},
    assets:[{asset_id:'asset-1',path:'/declared/vlog.mp4',state:'declared'}],route:{kind:'known'},outputs:[],steps:[],
    limits:{maximum_revisions:3},risk_requirements:[],proof_requirements:[],metadata:{}};
  const domains=['media','music','sticker','transition','caption'];
  for(const domain of domains) plan=attachNativeResourceAcquisition(plan,{
    schema:'jianying-native-resource-query/v1',request_id:`vlog-${domain}`,domain,keywords:['生活 Vlog'],
    filters:{styles:['vlog'],moods:['happy'],tempos:['upbeat'],aspect_ratios:['9:16'],edition:'professional',
      usage:'personal',channel:'douyin',maximum_cost_microunits:0,at_epoch_seconds:1_795_000_000},
    selection:{strategy:'ranked',maximum_candidates:10},
  });
  assert.equal(validateWorkflowPlan(plan).valid,true);
  assert.deepEqual([...new Set(plan.steps.map(step=>step.resource_query.domain))],domains);
  assert.equal(plan.steps.length,15);
  assert.equal(plan.steps.filter(step=>step.type==='native_resource_acquire').length,5);
  assert.ok(plan.tool_requirements.capabilities.includes('media.official_resource'));
  assert.ok(plan.tool_requirements.capabilities.includes('media.audio'));
  assert.doesNotMatch(JSON.stringify(plan),/screen_coordinate|coordinates|"x"|"y"/);
});
