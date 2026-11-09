#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import process from 'node:process';
import {spawnSync} from 'node:child_process';

import {compileWorkflow} from './workflow_compiler.mjs';
import {handshake,runJob,runJsonCommand} from './runtime_adapter.mjs';

const root=path.resolve(process.env.JIANYING_ACCEPTANCE_ROOT??fs.mkdtempSync(path.join(os.tmpdir(),'jianying-representative-')));
fs.mkdirSync(root,{recursive:true});

function command(program,args) {
  const result=spawnSync(program,args,{encoding:'utf8',env:process.env});
  if(result.status!==0) throw new Error(`${program} failed: ${result.stderr}`);
  return result.stdout;
}

function json(file,value) {
  fs.mkdirSync(path.dirname(file),{recursive:true});
  fs.writeFileSync(file,`${JSON.stringify(value,null,2)}\n`);
}

function sha256(file) {return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');}

function media(name,duration,color,frequency) {
  const file=path.join(root,'media',`${name}.mp4`); fs.mkdirSync(path.dirname(file),{recursive:true});
  command('ffmpeg',['-hide_banner','-loglevel','error','-y','-f','lavfi','-i',`color=c=${color}:s=640x360:d=${duration}:r=30`,
    '-f','lavfi','-i',`sine=frequency=${frequency}:duration=${duration}`,'-shortest','-c:v','libx264','-preset','ultrafast',
    '-pix_fmt','yuv420p','-c:a','aac',file]);
  const probe=JSON.parse(command('ffprobe',['-v','error','-show_entries','format=duration,size:stream=codec_type,width,height',
    '-of','json',file]));
  return {file,probe,ledger:{asset_id:name,path:file,state:'verified',sha256:sha256(file),bytes:fs.statSync(file).size,
    duration_us:Math.round(Number(probe.format.duration)*1_000_000),streams:probe.streams.map(stream=>({type:stream.codec_type,...stream}))}};
}

function plan(workflowId,outputs) {
  return {schema:'jianying-workflow-plan/v1',workflow_id:workflowId,revision:1,
    catalog_ref:{schema:'jianying-planning-catalog/v2',digest:'c'.repeat(64)},brief:{},assets:[],route:{},steps:[],
    limits:{},risk_requirements:[],proof_requirements:[],metadata:{},outputs,
    tool_requirements:{capabilities:['timeline.edit']}};
}

function output(outputId,purpose='personal',extra={}) {
  return {output_id:outputId,purpose,format:'video',delivery:'editable_draft',target:{logical_path:`outputs/${outputId}`},...extra};
}

function cliIdentity(ready) {
  return {version:ready.version,sha256:ready.sha256,jobSchema:ready.jobSchema,capabilities:ready.manifest.capabilities};
}

function execute(name,workflow,ledger,decisions,ready,{skipBlocked=true}={}) {
  const chainRoot=path.join(root,name); fs.mkdirSync(chainRoot,{recursive:true});
  const compilation=compileWorkflow({plan:workflow,assetLedger:ledger,decisions,cliIdentity:cliIdentity(ready),
    outputRoot:path.join(chainRoot,'drafts')});
  json(path.join(chainRoot,'workflow-plan.json'),workflow); json(path.join(chainRoot,'asset-ledger.json'),ledger);
  json(path.join(chainRoot,'edit-decisions.json'),decisions); json(path.join(chainRoot,'compilation.json'),compilation);
  const outputs=[];
  for(const binding of compilation.job_bindings) {
    const jobPath=path.join(chainRoot,'jobs',`${binding.output_id}.job.json`); json(jobPath,binding.job);
    if(skipBlocked&&binding.blockers.length) {outputs.push({output_id:binding.output_id,status:'blocked',blockers:binding.blockers});continue;}
    const invocation=runJob({jobPath,outputPath:binding.output_path,env:process.env});
    if(invocation.exitCode!==0||invocation.envelope?.ok!==true) throw new Error(JSON.stringify(invocation));
    const proxy=path.join(chainRoot,'proxies',`${binding.output_id}.mp4`); fs.mkdirSync(path.dirname(proxy),{recursive:true});
    const rendered=runJsonCommand({args:['render','proxy',binding.output_path,'--out',proxy],requiredCapabilities:['render.proxy'],env:process.env});
    if(rendered.exitCode!==0||rendered.envelope?.ok!==true) throw new Error(JSON.stringify(rendered));
    const probe=JSON.parse(command('ffprobe',['-v','error','-show_entries','format=duration,size:stream=codec_type,width,height',
      '-of','json',proxy]));
    outputs.push({output_id:binding.output_id,status:'verified',job_digest:binding.job_digest,draft:binding.output_path,
      proxy,proxy_sha256:sha256(proxy),probe,invocation:invocation.envelope,render:rendered.envelope});
  }
  const evidence={schema:'jianying-representative-binary-acceptance/v1',chain:name,cli:{version:ready.version,
    sha256:ready.sha256,source:ready.source},outputs}; json(path.join(chainRoot,'evidence.json'),evidence); return evidence;
}

const ready=handshake({env:process.env});
const vlogMedia=['red','green','blue','yellow'].map((color,index)=>media(`vlog-${index+1}`,6,color,440+index*110));
const vlogPlan=plan('VLOG-01',[output('main')]);
const vlogDecisions=[{output_id:'main',clips:vlogMedia.map(item=>({asset_id:item.ledger.asset_id,in_us:1_000_000,out_us:4_000_000}))}];
const vlog=execute('VLOG-01',vlogPlan,vlogMedia.map(item=>item.ledger),vlogDecisions,ready);

const courseMedia=media('course',120,'navy',330);
const coursePlan=plan('COURSE-01',[output('master','education'),
  output('teaser-1','education',{derived_from:'master',canvas:{width:1080,height:1920,frame_rate:{numerator:30,denominator:1}}}),
  output('teaser-2','education',{derived_from:'master',canvas:{width:1080,height:1920,frame_rate:{numerator:30,denominator:1}}}),
  output('teaser-3','education',{derived_from:'master',canvas:{width:1080,height:1920,frame_rate:{numerator:30,denominator:1}}})]);
const captions=[
  {caption_id:'zh-1',asset_id:'course',in_us:11_000_000,out_us:13_000_000,text:'第一章',language:'zh-CN',review_status:'confirmed'},
  {caption_id:'en-1',asset_id:'course',in_us:11_000_000,out_us:13_000_000,text:'Chapter one',language:'en',review_status:'confirmed'},
  {caption_id:'zh-2',asset_id:'course',in_us:51_000_000,out_us:53_000_000,text:'第二章',language:'zh-CN',review_status:'confirmed'},
  {caption_id:'en-pending',asset_id:'course',in_us:91_000_000,out_us:93_000_000,text:'Pending review',language:'en',review_status:'pending'},
];
const ranges=[[0,120],[10,20],[50,60],[90,100]];
const courseDecisions=coursePlan.outputs.map((item,index)=>({output_id:item.output_id,
  clips:[{asset_id:'course',in_us:ranges[index][0]*1_000_000,out_us:ranges[index][1]*1_000_000}],captions}));
const course=execute('COURSE-01',coursePlan,[courseMedia.ledger],courseDecisions,ready);

const weddingMedia=media('wedding',60,'purple',550);
const weddingPlan=plan('WEDDING-01',[output('ceremony','private'),output('memory','private',{derived_from:'ceremony'}),
  output('advertisement','commercial',{derived_from:'ceremony',blockers:[{code:'commercial_approval_required'}]})]);
const weddingDecisions=[
  {output_id:'ceremony',clips:[{asset_id:'wedding',in_us:0,out_us:60_000_000}]},
  {output_id:'memory',clips:[{asset_id:'wedding',in_us:10_000_000,out_us:25_000_000}]},
  {output_id:'advertisement',clips:[{asset_id:'wedding',in_us:20_000_000,out_us:30_000_000}]},
];
const wedding=execute('WEDDING-01',weddingPlan,[weddingMedia.ledger],weddingDecisions,ready);

const summary={schema:'jianying-representative-binary-suite/v1',created_at:new Date().toISOString(),root,
  no_cargo_path:spawnSync('cargo',['--version'],{encoding:'utf8',env:process.env}).error?.code==='ENOENT',
  cli:{version:ready.version,sha256:ready.sha256,source:ready.source},chains:{vlog,course,wedding}};
json(path.join(root,'summary.json'),summary);
process.stdout.write(`${JSON.stringify(summary,null,2)}\n`);
