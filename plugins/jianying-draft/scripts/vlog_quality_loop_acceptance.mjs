#!/usr/bin/env node
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import {fileURLToPath} from 'node:url';

import {runJob,runJsonCommand,handshake} from './runtime_adapter.mjs';
import {collectMediaQualityEvidence,collectProxyEvidence} from './quality_proxy_evidence.mjs';
import {runEvaluator} from './quality_evaluator.mjs';
import {buildRevisionRequest} from './quality_iteration.mjs';
import {qualityContractDigest} from './quality_contracts.mjs';
import {canonical,sha256 as sha256Text} from './workflow_data.mjs';

const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const FIXTURES=path.join(ROOT,'tests/fixtures/quality-loop');
const source=path.resolve(process.env.JIANYING_VLOG_SOURCE??'');
const outputRoot=path.resolve(process.env.JIANYING_QUALITY_ACCEPTANCE_ROOT??path.join(process.cwd(),'jianying-vlog-quality-acceptance'));
if(!process.env.JIANYING_VLOG_SOURCE||!fs.statSync(source,{throwIfNoEntry:false})?.isFile())
  throw new Error('JIANYING_VLOG_SOURCE must name an existing regular video file');
fs.mkdirSync(outputRoot,{recursive:true});

function writeJson(file,value) {fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,`${JSON.stringify(value,null,2)}\n`);}
function readJson(file) {return JSON.parse(fs.readFileSync(file,'utf8'));}
function sha256(file) {return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');}

const ready=handshake();
if(ready.manifest?.contract_state!=='released'||ready.source==='development_override')
  throw new Error('quality acceptance requires the checksum-pinned released CLI, not a development override');
const contracts=readJson(path.join(FIXTURES,'contracts.json'));
const profile=contracts.quality_profile;

function executeRevision(revision) {
  const revisionRoot=path.join(outputRoot,`revision-${revision}`);
  const job=readJson(path.join(FIXTURES,`vlog-revision-${revision}.job.json`));
  job.project.project.materials[0].path=source;
  const jobPath=path.join(revisionRoot,'job.json'),draft=path.join(revisionRoot,'draft'),proxy=path.join(revisionRoot,'proxy.mp4');
  writeJson(jobPath,job);
  const execution=runJob({jobPath,outputPath:draft});
  if(execution.exitCode!==0||execution.envelope?.ok!==true) throw new Error(`revision ${revision} job failed`);
  const render=runJsonCommand({args:['render','proxy',draft,'--out',proxy],requiredCapabilities:['render.proxy']});
  if(render.exitCode!==0||render.envelope?.ok!==true) throw new Error(`revision ${revision} proxy failed`);
  const options={proxyPath:proxy,workflowId:'VLOG-01',revision,outputId:'main',observedAt:new Date().toISOString()};
  const proxyEvidence=collectProxyEvidence(options),mediaEvidence=collectMediaQualityEvidence(options);
  const input={schema:'jianying-evaluation-input/v1',workflow_id:'VLOG-01',revision,output_id:'main',
    target_digest:qualityContractDigest({...contracts.creative_target,revision}),profile_digest:qualityContractDigest(profile),
    artifacts:[proxyEvidence.artifact],evidence:[proxyEvidence.evidence,mediaEvidence.evidence],
    content_review:{captions:{status:'absent'},transcript:{status:'absent'},languages:[]},
    evaluator_scope:{provider:'local',model:'opening-duration-policy',maximum_cost:0,upload_allowed:false},metadata:{}};
  const durationUs=mediaEvidence.analysis.duration_us;
  const evidenceRefs=input.evidence.map(item=>item.evidence_id);
  const adapter={identity:{type:'deterministic',provider:'local',model:'opening-duration-policy',version:'1'},
    evaluate:()=>({decision:durationUs>4_000_000?'revise':'pass',evidence_refs:evidenceRefs,
      scores:[{dimension_id:'narrative',value:durationUs>4_000_000?6:9,passed:durationUs<=4_000_000}],
      hard_gates:[{rule_id:'artifact_non_empty',passed:true,evidence_refs:evidenceRefs}],
      findings:durationUs>4_000_000?[{code:'opening_duration_exceeded',severity:'major',output_id:'main',
        time_range:{start_us:4_000_000,end_us:durationUs},observation:'开场超过已批准的四秒建立窗口',rule_id:'narrative',
        evidence_refs:evidenceRefs,suggested_action:'trim'}]:[],
      limitations:['仅验证开场时长规则，不替代叙事、审美或音画人工评审']})};
  const verdict=runEvaluator({adapter,input,profile});
  const evidence={schema:'jianying-vlog-quality-revision-evidence/v1',revision,source:{path:source,sha256:sha256(source)},
    cli:{version:ready.version,sha256:ready.sha256,source:ready.source},job_digest:sha256Text(canonical(job)),
    execution:execution.envelope,render:render.envelope,proxy:{path:proxy,sha256:sha256(proxy)},
    proxy_evidence:proxyEvidence,media_evidence:mediaEvidence,evaluation_input:input,verdict};
  writeJson(path.join(revisionRoot,'evidence.json'),evidence);return evidence;
}

const first=executeRevision(1);
if(first.verdict.decision!=='revise') throw new Error('revision 1 must deterministically request a trim');
const revisionRequest=buildRevisionRequest({verdict:first.verdict,allowedActions:profile.allowed_actions,
  availableCapabilities:['timeline.edit']});
writeJson(path.join(outputRoot,'revision-request.json'),revisionRequest);
const second=executeRevision(2);
if(second.verdict.decision!=='pass'||first.evaluation_input.target_digest===second.evaluation_input.target_digest||
  first.job_digest===second.job_digest) throw new Error('revision 2 did not produce an independently bound passing result');
const summary={schema:'jianying-vlog-quality-loop-acceptance/v1',created_at:new Date().toISOString(),root:outputRoot,
  source:{path:source,sha256:sha256(source)},cli:{version:ready.version,sha256:ready.sha256,source:ready.source},
  no_development_override:true,revision_request_digest:qualityContractDigest(revisionRequest),
  approval_rebind_required:first.evaluation_input.target_digest!==second.evaluation_input.target_digest,
  revisions:[{revision:1,decision:first.verdict.decision,proxy:first.proxy.sha256},
    {revision:2,decision:second.verdict.decision,proxy:second.proxy.sha256}],
  limitations:['deterministic loop does not replace real JianYing cold reopen, playback, native export or human creative review']};
writeJson(path.join(outputRoot,'summary.json'),summary);
process.stdout.write(`${JSON.stringify(summary,null,2)}\n`);
