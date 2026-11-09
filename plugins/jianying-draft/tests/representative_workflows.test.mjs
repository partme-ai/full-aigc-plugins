import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import {compileWorkflow} from '../scripts/workflow_compiler.mjs';
import {WorkflowRuntime,verifyDraftArtifact} from '../scripts/workflow_runtime.mjs';

const cli={version:'1.6.14',sha256:'a'.repeat(64),jobSchema:'jianying-job/v2',capabilities:[
  {id:'schema.job_v2',status:'supported'},{id:'job.run',status:'supported'},{id:'timeline.edit',status:'supported'},
]};

function plan(workflowId,outputs) {
  return {schema:'jianying-workflow-plan/v1',workflow_id:workflowId,revision:1,
    catalog_ref:{schema:'jianying-planning-catalog/v2',digest:'c'.repeat(64)},brief:{},assets:[],route:{},steps:[],
    limits:{},risk_requirements:[],proof_requirements:[],metadata:{},outputs,
    tool_requirements:{capabilities:['timeline.edit']}};
}

function output(outputId,purpose='personal',extra={}) {
  return {output_id:outputId,purpose,format:'video',delivery:'editable_draft',
    target:{logical_path:`outputs/${outputId}`},...extra};
}

function asset(assetId,durationUs,sha='b') {
  return {asset_id:assetId,path:`/synthetic/${assetId}.mp4`,state:'verified',sha256:sha.repeat(64),bytes:100,
    duration_us:durationUs,streams:[{type:'video',width:1920,height:1080},{type:'audio'}]};
}

function duration(job) {
  return Math.max(...job.project.project.timeline.tracks.flatMap(track=>track.segments)
    .map(segment=>segment.range.start_us+segment.range.duration_us));
}

function executeSimulation(t,compilation,failurePolicy='stop_all') {
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'jy-representative-'));
  t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  const runtime=new WorkflowRuntime({stateRoot:path.join(root,'state'),executor:bindings=>({artifacts:bindings.map(binding=>{
    const draft=path.join(root,binding.output_id); fs.mkdirSync(draft,{recursive:true});
    const expected=duration(binding.job);
    fs.writeFileSync(path.join(draft,'draft_content.json'),JSON.stringify({duration:expected,tracks:[{segments:[{}]}]}));
    fs.writeFileSync(path.join(draft,'draft_meta_info.json'),'{}');
    return {output_id:binding.output_id,path:draft,duration_us:expected};
  })}),verifier:artifacts=>{
    const checks=artifacts.map(item=>({output_id:item.output_id,...verifyDraftArtifact(item.path,{duration_us:item.duration_us})}));
    return {ok:checks.every(item=>item.ok),evidence:checks};
  }});
  const state=runtime.start({compilation,revision:1,budget:{currency:'CNY',maximum:0},failure_policy:failurePolicy});
  if(state.stage==='blocked') return {runtime,state};
  runtime.approve(state.run_id,{...runtime.approvalBinding(state.run_id),user_id:'acceptance',expires_at:'2999-01-01T00:00:00Z'});
  return {runtime,state:runtime.execute(state.run_id)};
}

test('VLOG-01 compiles four half-open selections into a verified 12-second output and detects replacement',t=>{
  const assets=[1,2,3,4].map(index=>asset(`vlog-${index}`,6_000_000,String(index)));
  const workflow=plan('VLOG-01',[output('main')]);
  const decisions=[{output_id:'main',clips:assets.map(item=>({asset_id:item.asset_id,in_us:1_000_000,out_us:4_000_000}))}];
  const compilation=compileWorkflow({plan:workflow,assetLedger:assets,decisions,cliIdentity:cli});
  assert.equal(duration(compilation.job_bindings[0].job),12_000_000);
  assert.equal(executeSimulation(t,compilation).state.terminal_state,'completed');
  const replaced=structuredClone(assets); replaced[0].sha256='f'.repeat(64);
  const replacement=compileWorkflow({plan:workflow,assetLedger:replaced,decisions,cliIdentity:cli});
  assert.notEqual(compilation.receipt.semantic_digest,replacement.receipt.semantic_digest);
});

test('COURSE-01 compiles a 120-second master plus three 10-second derivatives with relocated confirmed subtitles',t=>{
  const workflow=plan('COURSE-01',[
    output('master'),
    output('teaser-1','education',{derived_from:'master',canvas:{width:1080,height:1920,frame_rate:{numerator:30,denominator:1}}}),
    output('teaser-2','education',{derived_from:'master',canvas:{width:1080,height:1920,frame_rate:{numerator:30,denominator:1}}}),
    output('teaser-3','education',{derived_from:'master',canvas:{width:1080,height:1920,frame_rate:{numerator:30,denominator:1}}}),
  ]);
  const captions=[
    {caption_id:'zh-1',asset_id:'course',in_us:11_000_000,out_us:13_000_000,text:'第一章',language:'zh-CN',review_status:'confirmed'},
    {caption_id:'en-1',asset_id:'course',in_us:11_000_000,out_us:13_000_000,text:'Chapter one',language:'en',review_status:'confirmed'},
    {caption_id:'zh-2',asset_id:'course',in_us:51_000_000,out_us:53_000_000,text:'第二章',language:'zh-CN',review_status:'confirmed'},
    {caption_id:'en-pending',asset_id:'course',in_us:91_000_000,out_us:93_000_000,text:'Pending review',language:'en',review_status:'pending'},
  ];
  const ranges=[[0,120], [10,20], [50,60], [90,100]];
  const decisions=workflow.outputs.map((item,index)=>({output_id:item.output_id,
    clips:[{asset_id:'course',in_us:ranges[index][0]*1_000_000,out_us:ranges[index][1]*1_000_000}],captions}));
  const compilation=compileWorkflow({plan:workflow,assetLedger:[asset('course',120_000_000)],decisions,cliIdentity:cli});
  assert.deepEqual(compilation.job_bindings.map(item=>duration(item.job)),[120_000_000,10_000_000,10_000_000,10_000_000]);
  assert.deepEqual(compilation.job_bindings.slice(1).map(item=>item.derived_from),['master','master','master']);
  const firstTeaserCaptions=compilation.job_bindings[1].job.project.project.timeline.tracks.slice(1).flatMap(track=>track.segments);
  assert.deepEqual(firstTeaserCaptions.map(item=>item.range),[
    {start_us:1_000_000,duration_us:2_000_000},{start_us:1_000_000,duration_us:2_000_000},
  ]);
  assert.equal(compilation.job_bindings[3].caption_reviews.some(item=>item.review_status==='pending'),false);
  assert.equal(executeSimulation(t,compilation).state.terminal_state,'completed');
});

test('WEDDING-01 keeps three purposes isolated and blocks commercial or unsupported multicamera branches',t=>{
  const workflow=plan('WEDDING-01',[
    output('ceremony','private'),output('memory','private',{derived_from:'ceremony'}),
    output('advertisement','commercial',{derived_from:'ceremony',blockers:[{code:'commercial_approval_required'}]}),
  ]);
  const decisions=[
    {output_id:'ceremony',clips:[{asset_id:'wedding',in_us:0,out_us:60_000_000}]},
    {output_id:'memory',clips:[{asset_id:'wedding',in_us:10_000_000,out_us:25_000_000}]},
    {output_id:'advertisement',clips:[{asset_id:'wedding',in_us:20_000_000,out_us:30_000_000}]},
  ];
  const compilation=compileWorkflow({plan:workflow,assetLedger:[asset('wedding',60_000_000)],decisions,cliIdentity:cli});
  assert.deepEqual(compilation.job_bindings.map(item=>duration(item.job)),[60_000_000,15_000_000,10_000_000]);
  assert.equal(executeSimulation(t,compilation).state.stage,'blocked');
  const partial=executeSimulation(t,compilation,'continue_independent').state;
  assert.equal(partial.terminal_state,'partially_completed');
  assert.deepEqual(partial.blocked_outputs,['advertisement']);
  const multicamera=structuredClone(decisions); multicamera[0].clips[0].multicam={sync:'audio'};
  assert.throws(()=>compileWorkflow({plan:workflow,assetLedger:[asset('wedding',60_000_000)],decisions:multicamera,cliIdentity:cli}),
    error=>error.code==='unsupported_edit_mapping');
});
