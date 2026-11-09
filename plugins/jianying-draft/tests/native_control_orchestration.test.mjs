import assert from 'node:assert/strict';
import test from 'node:test';

const editor={product:'剪映专业版',bundle_id:'com.lemon.lvpro',version:'11.5.13243',build:'11.6.0-beta2',platform:'macos'};
const direct=(semantic_id,capability,parameters)=>({semantic_id,label:semantic_id,route:'draft_protocol',
  fallback_route:'accessibility_adapter',status:'supported',capability,command:'released CLI command',parameters,
  state_scope:'draft',evidence:'released CLI differential'});
const runtime=(semantic_id,operation,input,readback,parameters=[])=>({semantic_id,label:semantic_id,route:'runtime_native',
  fallback_route:'accessibility_adapter',status:'partial',capability:'runtime.controls',command:null,parameters,
  state_contract:{operation,input,readback,readback_required:true},state_scope:'owned_session',evidence:'state readback'});

const controls=[
  direct('timeline.item.add','timeline.edit',['draft','resource','track','target_timerange']),
  direct('timeline.segment.split','timeline.edit',['draft','segment_id','at']),
  direct('timeline.segment.trim_left','timeline.edit',['draft','segment_id','source_start','duration']),
  direct('timeline.segment.trim_right','timeline.edit',['draft','segment_id','source_start','duration']),
  direct('timeline.segment.edge_trim','timeline.edit',['draft','segment_id','edge','time']),
  direct('timeline.segment.duplicate','timeline.edit',['draft','segment_id','track','new_track','dry_run']),
  direct('timeline.track.add','timeline.edit',['draft','kind','name']),
  direct('timeline.segment.move','timeline.edit',['draft','segment_id','offset']),
  direct('timeline.segment.delete','timeline.remove',['draft','segment_id']),
  direct('timeline.keyframe.add','timeline.keyframe',['draft','segment_id','property','time','value','easing']),
  direct('timeline.filter.add','timeline.filter',['draft','slug','start','duration','intensity','resource_identity']),
  direct('timeline.effect.add','timeline.effect',['draft','slug','start','duration','intensity','params','bind_segment_id','resource_identity']),
  direct('timeline.transition.set','timeline.transition',['draft','segment_id','slug','duration','resource_identity']),
  direct('track.cover.edit','project.cover',['draft','cover_image','time']),
  runtime('timeline.session.undo','invoke','empty_object','undo_depth'),
  runtime('timeline.session.snap','set','boolean','enabled',['enabled']),
  runtime('timeline.view.zoom','set','finite_number','zoom_value',['value']),
  runtime('timeline.audio.record','invoke','record_action_object','recording_state_and_new_audio_identity',['action','track','start_at','input_device']),
  {semantic_id:'timeline.segment.context_menu',label:'片段右键菜单',route:'accessibility_adapter',
    fallback_route:'visual_fallback',status:'unresolved',capability:'runtime.controls',command:null,
    parameters:['segment_id','action'],state_scope:'session',evidence:'children pending'},
];
const catalog={schema:'jianying-timeline-control-catalog/v1',editor_scope:'version-bound-runtime-profile',
  observed_editor:editor,route_priority:['draft_protocol','runtime_native','accessibility_adapter','visual_fallback'],
  controls,truth_rule:'supported semantics only'};
const surfaces=controls.map((control,index)=>({surface_id:`toolbar.${index+1}`,region:'toolbar',visual_order:index+1,
  label:control.label,semantic_id:control.semantic_id,status:control.status==='unresolved'?'unresolved':'mapped',
  route:control.route,fallback_route:control.fallback_route,parameters:control.parameters,evidence:control.evidence}));
surfaces.at(-1).expansion={kind:'context_menu',status:'pending_accessibility',child_surface_ids:[],
  evidence:'child actions and accessibility names are not observed'};
surfaces.push({surface_id:'canvas.split',region:'canvas',visual_order:1,label:'分割手势',
  semantic_id:'timeline.segment.split',status:'mapped',route:'draft_protocol',fallback_route:'accessibility_adapter',
  parameters:['segment_id','at'],evidence:'gesture'});
const inventory={schema:'jianying-timeline-surface-inventory/v1',
  observed_editor:Object.fromEntries(Object.entries(editor).filter(([key])=>key!=='product')),
  evidence:{kind:'user_screenshot',sha256:'a'.repeat(64),width:1920,height:534},
  coverage:{expected_surfaces:surfaces.length,regions:{toolbar:controls.length,canvas:1}},surfaces,
  expansion_rule:'enumerate children',truth_rule:'mapped does not mean executable'};
const canary={schema:'jianying-control-canary/v1',status:'passed',editor:inventory.observed_editor,
  adapter:{kind:'accessibility_adapter',version:'1'},observed_at:'2026-09-22T00:00:00.000Z'};

test('surface inventory preserves duplicate semantics, screenshot identity, counts and unresolved entries',async()=>{
  const {validateNativeControlContracts}=await import('../scripts/native_control_orchestration.mjs');
  const result=validateNativeControlContracts({catalog,inventory});
  assert.equal(result.surface_count,surfaces.length);
  assert.deepEqual(result.region_counts,{canvas:1,toolbar:controls.length});
  assert.deepEqual(result.duplicate_semantics,[{semantic_id:'timeline.segment.split',surface_ids:['canvas.split','toolbar.2']}]);
  assert.deepEqual(result.unresolved_surface_ids,[`toolbar.${controls.length}`]);
  assert.equal(result.screenshot_sha256,'a'.repeat(64));
});

test('draft controls compile to fixed released Rust CLI argv without screen coordinates',async()=>{
  const {compileNativeControlPlan}=await import('../scripts/native_control_orchestration.mjs');
  const requests=[
    {request_id:'item',semantic_id:'timeline.item.add',arguments:{draft:'/draft',resource:{kind:'video',source:'/clip.mp4'},track:{name:'主轨'},target_timerange:{start:'0s',duration:'2s'}}},
    {request_id:'split',semantic_id:'timeline.segment.split',arguments:{draft:'/draft',segment_id:'s1',at:'1s'}},
    {request_id:'trim',semantic_id:'timeline.segment.trim_left',arguments:{draft:'/draft',segment_id:'s1',source_start:'0s',duration:'2s'}},
    {request_id:'trim-right',semantic_id:'timeline.segment.trim_right',arguments:{draft:'/draft',segment_id:'s1',source_start:'0s',duration:'1500ms'}},
    {request_id:'edge-trim',semantic_id:'timeline.segment.edge_trim',arguments:{draft:'/draft',segment_id:'s1',source_start:'250ms',duration:'1250ms'}},
    {request_id:'duplicate',semantic_id:'timeline.segment.duplicate',arguments:{draft:'/draft',segment_id:'s1',new_track:true,dry_run:true}},
    {request_id:'track',semantic_id:'timeline.track.add',arguments:{draft:'/draft',kind:'video',name:'B-Roll'}},
    {request_id:'move',semantic_id:'timeline.segment.move',arguments:{draft:'/draft',segment_id:'s1',offset:'500ms'}},
    {request_id:'delete',semantic_id:'timeline.segment.delete',arguments:{draft:'/draft',segment_id:'s2'}},
    {request_id:'keyframe',semantic_id:'timeline.keyframe.add',arguments:{draft:'/draft',segment_id:'s1',property:'alpha',time:'1s',value:'0.5',easing:'linear'}},
    {request_id:'filter',semantic_id:'timeline.filter.add',arguments:{draft:'/draft',slug:'cinematic',start:'0s',duration:'2s',intensity:0.8}},
    {request_id:'effect',semantic_id:'timeline.effect.add',arguments:{draft:'/draft',slug:'blur',start:'0s',duration:'2s',intensity:0.4,params:{radius:4}}},
    {request_id:'transition',semantic_id:'timeline.transition.set',arguments:{draft:'/draft',segment_id:'s1',slug:'fade',duration:'300ms'}},
    {request_id:'cover',semantic_id:'track.cover.edit',arguments:{draft:'/draft',cover_image:'/cover.png',time:1200}},
  ];
  const plan=compileNativeControlPlan({requests,catalog,inventory,adapters:{draft_protocol:true}});
  assert.equal(plan.steps.length,14);
  assert.deepEqual(plan.steps.map(step=>step.cli.args.slice(0,2)),[
    ['media','add-video'],['timeline','split'],['timeline','trim'],['timeline','trim'],['timeline','trim'],
    ['timeline','duplicate'],['timeline','add-track'],['timeline','move'],['timeline','remove'],
    ['timeline','keyframe'],['timeline','add-filter'],['timeline','add-effect'],['timeline','transition'],
    ['project','add-cover'],
  ]);
  assert.deepEqual(plan.steps[1].surface_ids,['canvas.split','toolbar.2']);
  assert.ok(plan.steps.every(step=>step.route==='draft_protocol' && step.requires_state_readback===false));
});

test('runtime controls require an exact-version canary and verify before/after state readback',async()=>{
  const {compileNativeControlPlan,verifyRuntimeControlExecution}=await import('../scripts/native_control_orchestration.mjs');
  const plan=compileNativeControlPlan({catalog,inventory,canary,adapters:{runtime_native:true},requests:[
    {request_id:'snap',semantic_id:'timeline.session.snap',arguments:{value:true}},
    {request_id:'undo',semantic_id:'timeline.session.undo',arguments:{}},
  ]});
  assert.deepEqual(plan.steps[0].cli.args.slice(0,4),['runtime','controls','set','timeline.session.snap']);
  assert.equal(plan.steps[0].readback.field,'enabled');
  let current={enabled:false,undo_depth:2};
  const adapter={
    async readState(_step,field){return {[field]:current[field]};},
    async execute(step){if(step.semantic_id==='timeline.session.snap') current.enabled=true; else current.undo_depth=1;
      return {request_id:`exec-${step.request_id}`,status:'applied'};},
  };
  const snap=await verifyRuntimeControlExecution({step:plan.steps[0],adapter});
  const undo=await verifyRuntimeControlExecution({step:plan.steps[1],adapter});
  assert.deepEqual(snap.after,{enabled:true});
  assert.deepEqual(undo.after,{undo_depth:1});
  assert.equal(snap.status,'verified');
});

test('coordinate-only, unresolved, missing-canary and missing-adapter plans fail closed',async()=>{
  const {compileNativeControlPlan}=await import('../scripts/native_control_orchestration.mjs');
  assert.throws(()=>compileNativeControlPlan({catalog,inventory,adapters:{draft_protocol:true},requests:[
    {request_id:'bad',semantic_id:'timeline.segment.split',arguments:{x:120,y:80}},
  ]}),error=>error.code==='coordinate_control_forbidden');
  assert.throws(()=>compileNativeControlPlan({catalog,inventory,adapters:{accessibility_adapter:true},canary,requests:[
    {request_id:'menu',semantic_id:'timeline.segment.context_menu',arguments:{segment_id:'s1',action:'copy'}},
  ]}),error=>error.code==='control_unresolved');
  assert.throws(()=>compileNativeControlPlan({catalog,inventory,adapters:{runtime_native:true},requests:[
    {request_id:'snap',semantic_id:'timeline.session.snap',arguments:{value:true}},
  ]}),error=>error.code==='control_canary_required');
  assert.throws(()=>compileNativeControlPlan({catalog,inventory,canary,adapters:{runtime_native:false},requests:[
    {request_id:'snap',semantic_id:'timeline.session.snap',arguments:{value:true}},
  ]}),error=>error.code==='control_adapter_unavailable');
});

test('coverage report blocks completeness for unresolved and unexpanded parents',async()=>{
  const {buildControlCoverageReport}=await import('../scripts/native_control_orchestration.mjs');
  const report=buildControlCoverageReport({catalog,inventory});
  assert.equal(report.can_claim_complete,false);
  assert.ok(report.gaps.some(gap=>gap.type==='unresolved_surface'));
  assert.ok(report.gaps.some(gap=>gap.type==='unexpanded_parent'));
  const unmapped={...catalog,controls:[...catalog.controls,direct('timeline.future.action','timeline.edit',['draft'])]};
  const unmappedInventory={...inventory,coverage:{expected_surfaces:inventory.surfaces.length+1,
    regions:{...inventory.coverage.regions,toolbar:inventory.coverage.regions.toolbar+1}},surfaces:[...inventory.surfaces,
    {surface_id:'toolbar.future',region:'toolbar',visual_order:99,label:'future',semantic_id:'timeline.future.action',
      status:'mapped',route:'draft_protocol',fallback_route:'accessibility_adapter',parameters:['draft'],evidence:'future'}]};
  const unmappedReport=buildControlCoverageReport({catalog:unmapped,inventory:unmappedInventory});
  assert.ok(unmappedReport.gaps.some(gap=>gap.type==='compiler_mapping_missing' && gap.semantic_id==='timeline.future.action'));
  const falseComplete=structuredClone(inventory);
  falseComplete.surfaces.at(-2).expansion.status='enumerated';
  assert.throws(()=>buildControlCoverageReport({catalog,inventory:falseComplete}),
    error=>error.code==='surface_inventory_invalid' && /enumerated without children/.test(error.message));
});

test('released CLI probing accepts only successful structured catalog envelopes',async()=>{
  const {probeNativeControlContracts}=await import('../scripts/native_control_orchestration.mjs');
  const calls=[];
  const result=await probeNativeControlContracts({cliRunner:request=>{
    calls.push(request);
    return {exitCode:0,envelope:{ok:true,data:calls.length===1?catalog:inventory}};
  }});
  assert.deepEqual(calls.map(call=>call.args),[['runtime','controls','list'],['runtime','controls','surfaces']]);
  assert.ok(calls.every(call=>call.requiredCapabilities.includes('runtime.control_catalog')));
  assert.equal(result.validation.surface_count,surfaces.length);
  await assert.rejects(()=>probeNativeControlContracts({cliRunner:()=>({exitCode:1,envelope:{ok:false,error:{type:'boom'}}})}),
    error=>error.code==='control_catalog_probe_failed');
});

test('compiled semantic controls attach to WorkflowPlan with fixed executors and readback contracts',async()=>{
  const {compileNativeControlPlan}=await import('../scripts/native_control_orchestration.mjs');
  const {attachNativeControlPlan,validateWorkflowPlan}=await import('../scripts/workflow_plan.mjs');
  const controlPlan=compileNativeControlPlan({catalog,inventory,canary,
    adapters:{draft_protocol:true,runtime_native:true},requests:[
      {request_id:'split',semantic_id:'timeline.segment.split',arguments:{draft:'/draft',segment_id:'s1',at:'1s'}},
      {request_id:'snap',semantic_id:'timeline.session.snap',arguments:{value:true}},
    ]});
  const plan={schema:'jianying-workflow-plan/v1',workflow_id:'workflow-controls',revision:1,
    catalog_ref:{schema:'jianying-planning-catalog/v2',digest:'c'.repeat(64)},tool_requirements:{capabilities:['timeline.edit']},
    brief:{request_id:'controls'},assets:[],route:{kind:'known'},outputs:[],steps:[],limits:{maximum_revisions:3},
    risk_requirements:[],proof_requirements:[],metadata:{}};
  const attached=attachNativeControlPlan(plan,controlPlan);
  assert.deepEqual(attached.steps.map(step=>step.type),['native_draft_control','native_runtime_control']);
  assert.deepEqual(attached.steps.map(step=>step.executor),['cli','plugin']);
  assert.equal(attached.steps[1].native_control.readback.field,'enabled');
  assert.ok(attached.tool_requirements.capabilities.includes('runtime.control_catalog'));
  assert.equal(attached.metadata['partme.native_control'].coverage_complete,false);
  assert.equal(validateWorkflowPlan(attached).valid,true);
  const injected=structuredClone(attached); injected.steps[0].native_control.arguments.x=12;
  assert.throws(()=>validateWorkflowPlan(injected),error=>error.code==='workflow_plan_invalid');
});
