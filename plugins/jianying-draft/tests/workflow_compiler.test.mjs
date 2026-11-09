import test from 'node:test';
import assert from 'node:assert/strict';

const plan={schema:'jianying-workflow-plan/v1',workflow_id:'workflow-vlog',revision:1,
  catalog_ref:{schema:'jianying-planning-catalog/v2',digest:'c'.repeat(64)},
  outputs:[{output_id:'main',purpose:'personal',format:'video',delivery:'editable_draft',
    target:{logical_path:'outputs/main'}}],
  tool_requirements:{capabilities:['timeline.edit']}};
const cli={version:'1.6.19',sha256:'a'.repeat(64),jobSchema:'jianying-job/v2',
  capabilities:[{id:'schema.job_v2',status:'supported'},{id:'job.run',status:'supported'},
    {id:'timeline.edit',status:'supported'}]};
const ledger=(path='/media/a.mp4')=>[{asset_id:'asset-1',path,state:'verified',sha256:'b'.repeat(64),
  bytes:100,duration_us:6000000,streams:[{type:'video',width:1920,height:1080}]}];
const decisions=[{output_id:'main',clips:[{asset_id:'asset-1',in_us:1000000,out_us:4000000}]}];

test('unverified assets and missing selections cannot compile',async()=>{
  const {compileWorkflow}=await import('../scripts/workflow_compiler.mjs');
  assert.throws(()=>compileWorkflow({plan,assetLedger:[{...ledger()[0],state:'declared'}],decisions,cliIdentity:cli}),
    e=>e.code==='asset_not_verified');
  const result=compileWorkflow({plan,assetLedger:ledger(),decisions:[],cliIdentity:cli});
  assert.equal(result.can_compile,false); assert.deepEqual(result.job_bindings,[]); assert.equal(result.receipt,null);
  assert.ok(result.blockers.some(item=>item.code==='selection_required'));
});

test('vlog selection compiles half-open microsecond ranges into Job v2',async()=>{
  const {compileWorkflow}=await import('../scripts/workflow_compiler.mjs');
  const result=compileWorkflow({plan,assetLedger:ledger(),decisions,cliIdentity:cli});
  assert.equal(result.can_compile,true); assert.equal(result.can_execute,false);
  assert.equal(result.job_bindings.length,1);
  const binding=result.job_bindings[0],segment=binding.job.project.project.timeline.tracks[0].segments[0];
  assert.equal(binding.job.schema,'jianying-job/v2');
  assert.deepEqual(segment.range,{start_us:0,duration_us:3000000});
  assert.deepEqual(segment.source_range,{start_us:1000000,duration_us:3000000});
  assert.equal(binding.output_path,'outputs/main');
  assert.equal(result.receipt.cli.sha256,'a'.repeat(64));
});

test('invalid ranges and unsupported mappings fail closed',async()=>{
  const {compileWorkflow}=await import('../scripts/workflow_compiler.mjs');
  for(const clip of [
    {asset_id:'asset-1',in_us:4000000,out_us:4000000},
    {asset_id:'asset-1',in_us:-1,out_us:1},
    {asset_id:'asset-1',in_us:0,out_us:7000000},
    {asset_id:'asset-1',in_us:0,out_us:1000000,speed:2},
  ]) assert.throws(()=>compileWorkflow({plan,assetLedger:ledger(),decisions:[{output_id:'main',clips:[clip]}],cliIdentity:cli}),
    e=>['media_range_invalid','unsupported_edit_mapping'].includes(e.code));
});

test('explicit placement and source captions map onto the selected output timeline',async()=>{
  const {compileWorkflow}=await import('../scripts/workflow_compiler.mjs');
  const coursePlan=structuredClone(plan);
  coursePlan.outputs=[{...coursePlan.outputs[0],canvas:{width:1080,height:1920,frame_rate:{numerator:30,denominator:1}}}];
  const result=compileWorkflow({plan:coursePlan,assetLedger:ledger(),cliIdentity:cli,decisions:[{
    output_id:'main',clips:[{asset_id:'asset-1',in_us:1000000,out_us:4000000,target_start_us:0}],
    captions:[
      {caption_id:'zh-1',asset_id:'asset-1',in_us:1500000,out_us:2500000,text:'第一句',language:'zh-CN',review_status:'confirmed'},
      {caption_id:'en-1',asset_id:'asset-1',in_us:3500000,out_us:4500000,text:'Lesson one',language:'en',review_status:'pending'},
    ],
  }]});
  const project=result.job_bindings[0].job.project.project;
  assert.deepEqual({width:project.width,height:project.height}, {width:1080,height:1920});
  assert.deepEqual(project.timeline.tracks[1],{id:'captions-1-zh-CN',kind:'text',segments:[{
    type:'text',id:'caption-zh-1',range:{start_us:500000,duration_us:1000000},text:'第一句',
  }]});
  assert.deepEqual(result.job_bindings[0].caption_reviews,[
    {caption_id:'zh-1',language:'zh-CN',review_status:'confirmed'},
  ]);
});

test('unsafe placement, overlapping placement, and unsupported effects fail closed',async()=>{
  const {compileWorkflow}=await import('../scripts/workflow_compiler.mjs');
  for(const clips of [
    [{asset_id:'asset-1',in_us:0,out_us:1000000,target_start_us:Number.MAX_SAFE_INTEGER}],
    [{asset_id:'asset-1',in_us:0,out_us:2000000,target_start_us:0},{asset_id:'asset-1',in_us:2000000,out_us:3000000,target_start_us:1000000}],
    [{asset_id:'asset-1',in_us:0,out_us:1000000,effects:['cinematic']}],
  ]) assert.throws(()=>compileWorkflow({plan,assetLedger:ledger(),decisions:[{output_id:'main',clips}],cliIdentity:cli}),
    e=>['media_range_invalid','unsupported_edit_mapping'].includes(e.code));
});

test('multi-output jobs are isolated and preserve master-derived relationships',async()=>{
  const {compileWorkflow}=await import('../scripts/workflow_compiler.mjs');
  const multi=structuredClone(plan);
  multi.outputs=[
    {...multi.outputs[0],output_id:'master',target:{logical_path:'outputs/master'}},
    {...multi.outputs[0],output_id:'teaser',target:{logical_path:'outputs/teaser'},derived_from:'master'},
  ];
  const result=compileWorkflow({plan:multi,assetLedger:ledger(),cliIdentity:cli,decisions:[
    {output_id:'master',clips:[{asset_id:'asset-1',in_us:0,out_us:6000000}]},
    {output_id:'teaser',clips:[{asset_id:'asset-1',in_us:1000000,out_us:4000000}]},
  ],outputRoot:'/tmp/course-output'});
  assert.equal(result.job_bindings.length,2);
  assert.equal(result.job_bindings[1].derived_from,'master');
  assert.notEqual(result.job_bindings[0].output_path,result.job_bindings[1].output_path);
  assert.notEqual(result.job_bindings[0].job_digest,result.job_bindings[1].job_digest);
  assert.ok(result.job_bindings.every(binding=>!ledger()[0].path.startsWith(binding.output_path)));
});

test('duplicate targets, source overwrite, and unknown derivations are rejected',async()=>{
  const {compileWorkflow}=await import('../scripts/workflow_compiler.mjs');
  const multi=structuredClone(plan);
  multi.outputs=[
    {...multi.outputs[0],output_id:'one',target:{logical_path:'outputs/shared'}},
    {...multi.outputs[0],output_id:'two',target:{logical_path:'outputs/shared'},derived_from:'missing'},
  ];
  const choices=multi.outputs.map(output=>({output_id:output.output_id,clips:decisions[0].clips}));
  assert.throws(()=>compileWorkflow({plan:multi,assetLedger:ledger(),decisions:choices,cliIdentity:cli}),e=>e.code==='output_isolation_invalid');
  const overwrite=structuredClone(plan); overwrite.outputs[0].target.logical_path='/media/a.mp4';
  assert.throws(()=>compileWorkflow({plan:overwrite,assetLedger:ledger(),decisions,cliIdentity:cli}),e=>e.code==='output_isolation_invalid');
});

test('semantic digest is stable across physical paths while execution binding changes',async()=>{
  const {compileWorkflow}=await import('../scripts/workflow_compiler.mjs');
  const first=compileWorkflow({plan,assetLedger:ledger('/tmp/one/a.mp4'),decisions,cliIdentity:cli});
  const second=compileWorkflow({plan,assetLedger:ledger('/tmp/two/a.mp4'),decisions,cliIdentity:cli});
  assert.equal(first.receipt.semantic_digest,second.receipt.semantic_digest);
  assert.notEqual(first.receipt.execution_digest,second.receipt.execution_digest);
  assert.notEqual(first.job_bindings[0].job_digest,second.job_bindings[0].job_digest);
});

test('same path media replacement invalidates semantic and execution bindings',async()=>{
  const {compileWorkflow}=await import('../scripts/workflow_compiler.mjs');
  const first=compileWorkflow({plan,assetLedger:ledger('/tmp/same/a.mp4'),decisions,cliIdentity:cli});
  const replaced=ledger('/tmp/same/a.mp4'); replaced[0].sha256='d'.repeat(64);
  const second=compileWorkflow({plan,assetLedger:replaced,decisions,cliIdentity:cli});
  assert.notEqual(first.receipt.semantic_digest,second.receipt.semantic_digest);
  assert.notEqual(first.receipt.execution_digest,second.receipt.execution_digest);
});

test('partial or replaced CLI identity blocks compilation',async()=>{
  const {compileWorkflow}=await import('../scripts/workflow_compiler.mjs');
  const partial={...cli,capabilities:cli.capabilities.map(item=>item.id==='timeline.edit'?{...item,status:'partial'}:item)};
  assert.throws(()=>compileWorkflow({plan,assetLedger:ledger(),decisions,cliIdentity:partial}),e=>e.code==='missing_capability');
  assert.throws(()=>compileWorkflow({plan,assetLedger:ledger(),decisions,cliIdentity:{...cli,sha256:'bad'}}),e=>e.code==='cli_identity_invalid');
});

test('a CLI-verified downloaded official music resource compiles into the Vlog Job',async()=>{
  const {compileWorkflow}=await import('../scripts/workflow_compiler.mjs');
  const nativePlan=structuredClone(plan);
  nativePlan.tool_requirements.capabilities.push('media.official_resource','media.audio');
  const nativeCli=structuredClone(cli);
  nativeCli.capabilities.push({id:'media.official_resource',status:'supported'},{id:'media.audio',status:'supported'});
  const acquisition={schema:'jianying-native-resource-acquisition/v1',request_id:'vlog-travel-music',state:'ready',
    selected:{domain:'music',resource_id:'jy-music-travel-001',local_path:'/official/travel.m4a'},
    receipt:{schema_version:'jianying-official-resource-receipt/v1',asset_id:'jy-music-travel-001',
      identity:{kind:'downloaded_file',file:{path:'/official/travel.m4a',sha256:'e'.repeat(64),byte_length:2048}}},
    cli:{register:{status:'registered'},preflight:{status:'ready'}}};
  const result=compileWorkflow({plan:nativePlan,assetLedger:ledger(),cliIdentity:nativeCli,resourceAcquisitions:[acquisition],
    decisions:[{...decisions[0],official_resources:[{request_id:'vlog-travel-music',start_us:0,duration_us:3000000,volume:0.35}]}]});
  const project=result.job_bindings[0].job.project.project;
  assert.deepEqual(project.materials.at(-1),{type:'audio',id:'official-material-1',path:'/official/travel.m4a'});
  assert.deepEqual(project.timeline.tracks.at(-1),{id:'official-audio-1',kind:'audio',segments:[{type:'audio',
    id:'official-segment-1',range:{start_us:0,duration_us:3000000},material_id:'official-material-1',
    source_range:{start_us:0,duration_us:3000000},speed:1,volume:0.35}]});
  assert.equal(result.receipt.official_resources[0].asset_id,'jy-music-travel-001');
});

test('official resource compilation rejects missing acquisition or failed CLI preflight',async()=>{
  const {compileWorkflow}=await import('../scripts/workflow_compiler.mjs');
  const nativePlan=structuredClone(plan);
  nativePlan.tool_requirements.capabilities.push('media.official_resource','media.audio');
  const nativeCli=structuredClone(cli);
  nativeCli.capabilities.push({id:'media.official_resource',status:'supported'},{id:'media.audio',status:'supported'});
  const nativeDecision=[{...decisions[0],official_resources:[{request_id:'missing',start_us:0,duration_us:1000000,volume:1}]}];
  assert.throws(()=>compileWorkflow({plan:nativePlan,assetLedger:ledger(),cliIdentity:nativeCli,decisions:nativeDecision,
    resourceAcquisitions:[]}),error=>error.code==='official_resource_not_ready');
});
