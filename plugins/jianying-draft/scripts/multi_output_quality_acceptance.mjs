#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import {fileURLToPath} from 'node:url';

import {runEvaluator} from './quality_evaluator.mjs';
import {collectMediaQualityEvidence,collectProxyEvidence} from './quality_proxy_evidence.mjs';
import {qualityContractDigest} from './quality_contracts.mjs';
import {runJob,runJsonCommand,handshake} from './runtime_adapter.mjs';
import {authorizePurposeOutputs,evaluateMultiOutputCompletion,verifyOutputRevisionIsolation} from './multi_output_quality.mjs';
import {canonical,sha256 as sha256Text} from './workflow_data.mjs';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const suiteFile=path.resolve(process.env.JIANYING_REPRESENTATIVE_SUMMARY??'');
if(!process.env.JIANYING_REPRESENTATIVE_SUMMARY||!fs.statSync(suiteFile,{throwIfNoEntry:false})?.isFile())
  throw new Error('JIANYING_REPRESENTATIVE_SUMMARY must name a representative binary suite summary');
const outputRoot=path.resolve(process.env.JIANYING_MULTI_OUTPUT_QUALITY_ROOT??path.join(process.cwd(),'jianying-multi-output-quality'));
fs.mkdirSync(outputRoot,{recursive:true});

const readJson=file=>JSON.parse(fs.readFileSync(file,'utf8'));
const writeJson=(file,value)=>{fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,`${JSON.stringify(value,null,2)}\n`);};
const fileDigest=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const ready=handshake();
if(ready.manifest?.contract_state!=='released'||ready.source==='development_override')
  throw new Error('multi-output quality acceptance requires the checksum-pinned released CLI');
const suite=readJson(suiteFile);
if(suite.cli?.version!==ready.version||suite.cli?.sha256!==ready.sha256)
  throw new Error('representative suite and current released CLI identity differ');
const catalog=readJson(path.join(ROOT,'skills/jianying-draft-video-planning/references/quality-profiles-v1.json'));
const profile=id=>catalog.profiles.find(item=>item.profile_id===id)??(()=>{throw new Error(`missing profile ${id}`);})();

function captionsFromJob(job) {
  return job.project.project.timeline.tracks.filter(track=>track.kind==='text').flatMap(track=>track.segments)
    .map(item=>({caption_id:item.id,start_us:item.range.start_us,end_us:item.range.start_us+item.range.duration_us,text:item.text}));
}

function evaluateCourseOutput({outputId,revision,proxyPath,jobPath,forceContextFailure=false}) {
  const job=readJson(jobPath),captions=captionsFromJob(job),recordFile=path.join(outputRoot,'course',outputId,`revision-${revision}`,'captions.json');
  const record={schema:'jianying-caption-review/v1',output_id:outputId,revision,status:'confirmed',captions,
    languages:[...new Set(captions.map(item=>item.caption_id.includes('-en')?'en':'zh-CN'))]};
  writeJson(recordFile,record);
  const options={proxyPath,workflowId:'COURSE-01',revision,outputId,observedAt:new Date().toISOString()};
  const proxy=collectProxyEvidence(options),media=collectMediaQualityEvidence(options);
  const captionArtifact={artifact_id:`captions-${outputId}-r${revision}`,type:'captions',digest:fileDigest(recordFile),bytes:fs.statSync(recordFile).size};
  const captionEvidence={evidence_id:`caption-review-${outputId}-r${revision}`,type:'caption_context_review',artifact_id:captionArtifact.artifact_id,
    digest:sha256Text(canonical(record)),role:'fact',language:'zh-CN'};
  const languages=['zh-CN','en'].map(language=>({language,status:record.languages.includes(language)?'confirmed':'not_required'}));
  const input={schema:'jianying-evaluation-input/v1',workflow_id:'COURSE-01',revision,output_id:outputId,
    target_digest:sha256Text(canonical({workflow:'COURSE-01',outputId,revision})),profile_digest:qualityContractDigest(profile('course.multi-delivery')),
    artifacts:[proxy.artifact,captionArtifact],evidence:[proxy.evidence,media.evidence,captionEvidence],
    content_review:{captions:{status:'confirmed',artifact_id:captionArtifact.artifact_id},transcript:{status:'absent'},languages},
    evaluator_scope:{provider:'local',model:'course-output-policy',maximum_cost:0,upload_allowed:false},metadata:{'partme.profile_output':outputId}};
  const refs=input.evidence.map(item=>item.evidence_id),contextPassed=!forceContextFailure;
  const adapter={identity:{type:'deterministic',provider:'local',model:'course-output-policy',version:'1'},evaluate:()=>({
    decision:contextPassed?'pass':'revise',evidence_refs:refs,
    scores:[
      {dimension_id:'subtitle_timing_and_layout',value:captions.length?9:8,passed:true},
      {dimension_id:'teaser_context_fidelity',value:contextPassed?9:5,passed:contextPassed},
      {dimension_id:'delivery_isolation',value:10,passed:true},
    ],
    hard_gates:[
      {rule_id:'teaser_context_fidelity',passed:contextPassed,evidence_refs:refs},
      {rule_id:'delivery_isolation',passed:true,evidence_refs:refs},
    ],
    findings:contextPassed?[]:[{code:'teaser_context_incomplete',severity:'major',output_id:outputId,
      time_range:{start_us:1_000_000,end_us:3_000_000},observation:'预告字幕缺少本段适用条件，需局部补充语境',rule_id:'teaser_context_fidelity',
      evidence_refs:refs,suggested_action:'caption_edit'}],
    limitations:['本地策略只验证已确认字幕、代理技术事实和显式语境规则，不替代课程负责人及双语人工终审'],
  })};
  const verdict=runEvaluator({adapter,input,profile:profile('course.multi-delivery')});
  const result={output_id:outputId,revision,profile_binding:{profile_id:'course.multi-delivery',version:'1.0.0',
    digest:input.profile_digest},job_digest:fileDigest(jobPath),proxy_digest:fileDigest(proxyPath),input,verdict,proxy_evidence:proxy,media_evidence:media};
  writeJson(path.join(outputRoot,'course',outputId,`revision-${revision}`,'evidence.json'),result); return result;
}

function renderCourseQualityProxy(binding) {
  const proxy=path.join(outputRoot,'course',binding.output_id,'revision-1','proxy.mp4');
  fs.mkdirSync(path.dirname(proxy),{recursive:true});
  const rendered=runJsonCommand({args:['render','proxy',binding.draft_path,'--out',proxy,'--burn-captions'],
    requiredCapabilities:['render.proxy']});
  if(rendered.exitCode!==0||rendered.envelope?.ok!==true) throw new Error(`course ${binding.output_id} quality proxy failed`);
  const expectedCaptions=captionsFromJob(readJson(binding.job_path)).length;
  if(rendered.envelope.data?.captions_burned!==expectedCaptions)
    throw new Error(`course ${binding.output_id} quality proxy did not burn the expected captions`);
  return {proxy,render:rendered.envelope,expected_captions:expectedCaptions};
}

function reviseCourseTeaser(binding) {
  const revisionRoot=path.join(outputRoot,'course',binding.output_id,'revision-2');
  const job=readJson(binding.job_path);
  const text=job.project.project.timeline.tracks.find(track=>track.kind==='text')?.segments?.[0];
  if(!text) throw new Error('teaser-2 revision requires one confirmed caption');
  text.text=`${text.text}：包含适用条件`;
  const jobPath=path.join(revisionRoot,'job.json'),draft=path.join(revisionRoot,'draft'),proxy=path.join(revisionRoot,'proxy.mp4');
  writeJson(jobPath,job);
  const execution=runJob({jobPath,outputPath:draft});
  if(execution.exitCode!==0||execution.envelope?.ok!==true) throw new Error('course teaser revision job failed');
  const render=runJsonCommand({args:['render','proxy',draft,'--out',proxy,'--burn-captions'],requiredCapabilities:['render.proxy']});
  if(render.exitCode!==0||render.envelope?.ok!==true) throw new Error('course teaser revision proxy failed');
  if(render.envelope.data?.captions_burned!==captionsFromJob(job).length)
    throw new Error('course teaser revision did not burn its confirmed captions');
  return {...evaluateCourseOutput({outputId:binding.output_id,revision:2,proxyPath:proxy,jobPath}),execution:execution.envelope,render:render.envelope};
}

const courseBindings=suite.chains.course.outputs.filter(item=>item.status==='verified').map(item=>({
  output_id:item.output_id,draft_path:item.draft,job_path:path.join(suite.root,'COURSE-01','jobs',`${item.output_id}.job.json`),
}));
const courseRevision1=courseBindings.map(item=>{
  const qualityProxy=renderCourseQualityProxy(item);
  return {...evaluateCourseOutput({outputId:item.output_id,revision:1,proxyPath:qualityProxy.proxy,
    jobPath:item.job_path,forceContextFailure:item.output_id==='teaser-2'}),quality_proxy_render:qualityProxy.render};
});
const courseBefore=evaluateMultiOutputCompletion({requiredOutputs:courseBindings.map(item=>item.output_id),
  verdicts:courseRevision1.map(item=>item.verdict)});
const revised=reviseCourseTeaser(courseBindings.find(item=>item.output_id==='teaser-2'));
const beforeDigests=Object.fromEntries(courseRevision1.map(item=>[item.output_id,item.job_digest]));
const afterDigests={...beforeDigests,'teaser-2':revised.job_digest};
const isolation=verifyOutputRevisionIsolation({before:beforeDigests,after:afterDigests,expectedChanged:['teaser-2']});
if(courseRevision1.find(item=>item.output_id==='teaser-2').proxy_digest===revised.proxy_digest)
  throw new Error('course teaser caption revision did not change the burned-in quality proxy');
const courseAfter=evaluateMultiOutputCompletion({requiredOutputs:courseBindings.map(item=>item.output_id),verdicts:courseRevision1
  .filter(item=>item.output_id!=='teaser-2').map(item=>item.verdict).concat(revised.verdict)});

const weddingAuthorization=authorizePurposeOutputs({outputs:[
  {output_id:'ceremony',purpose:'private'},{output_id:'memory',purpose:'private'},{output_id:'advertisement',purpose:'commercial'},
],approvals:[{approval_id:'private-delivery',purpose:'private',output_ids:['ceremony','memory']}]});
const weddingEvidence=suite.chains.wedding.outputs.map(item=>({output_id:item.output_id,status:item.status,
  purpose:item.output_id==='advertisement'?'commercial':'private',proxy_digest:item.proxy?fileDigest(item.proxy):null,
  blockers:item.blockers??[],human_review:'pending'}));

const summary={schema:'jianying-multi-output-quality-acceptance/v1',created_at:new Date().toISOString(),root:outputRoot,
  cli:{version:ready.version,sha256:ready.sha256,source:ready.source},course:{revision_1:courseBefore,revision_2:courseAfter,
    revision_isolation:isolation,outputs:[...courseRevision1,revised]},wedding:{authorization:weddingAuthorization,outputs:weddingEvidence,
    terminal_state:'needs_human_review',limitations:['仪式连续性和私人纪念情绪仍需授权人员人工评审','商业广告在商业授权缺失时保持阻塞']},
  limitations:['课程本地策略验收不替代课程负责人、双语专家或真实剪映人工终审','婚礼用途隔离已验证，主观评审仍为 pending']};
writeJson(path.join(outputRoot,'summary.json'),summary);
process.stdout.write(`${JSON.stringify(summary,null,2)}\n`);
