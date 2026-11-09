import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

import {AdapterError,runJsonCommand} from './runtime_adapter.mjs';
import {canonical,sha256} from './workflow_data.mjs';

const OPTION_KEYS=new Set(['proxyPath','workflowId','revision','outputId','observedAt','env','pluginRoot']);
const fail=(code,message)=>{throw new AdapterError(code,message);};

function hashRegularFile(file) {
  let descriptor;
  try {
    const stat=fs.lstatSync(file);
    if(!stat.isFile() || stat.isSymbolicLink()) fail('proxy_artifact_invalid','proxy must be a regular non-symbolic file');
    if(stat.size<=0) fail('proxy_artifact_invalid','proxy must not be empty');
    descriptor=fs.openSync(file,'r');
    const digest=crypto.createHash('sha256'),buffer=Buffer.allocUnsafe(1024*1024);
    let offset=0;
    while(offset<stat.size) {
      const length=fs.readSync(descriptor,buffer,0,Math.min(buffer.length,stat.size-offset),offset);
      if(length<=0) fail('proxy_artifact_changed','proxy changed while hashing');
      digest.update(buffer.subarray(0,length)); offset+=length;
    }
    const after=fs.fstatSync(descriptor);
    if(after.size!==stat.size || after.mtimeMs!==stat.mtimeMs)
      fail('proxy_artifact_changed','proxy changed while hashing');
    return {digest:digest.digest('hex'),bytes:stat.size};
  } catch(error) {
    if(error instanceof AdapterError) throw error;
    if(error.code==='ENOENT') fail('proxy_artifact_missing','proxy artifact does not exist');
    fail('proxy_artifact_invalid',`cannot inspect proxy artifact: ${error.code??error.message}`);
  } finally {
    if(descriptor!==undefined) fs.closeSync(descriptor);
  }
}

function normalizeProbe(value) {
  const frame=value?.frame_rate;
  const streams=Array.isArray(value?.streams)?value.streams.map(item=>typeof item==='string'?{type:item}:
    {type:item?.type??item?.codec_type}):[];
  if(!Number.isSafeInteger(value?.duration_us) || value.duration_us<=0 ||
    !Number.isSafeInteger(value?.width) || value.width<=0 || !Number.isSafeInteger(value?.height) || value.height<=0 ||
    !Number.isSafeInteger(frame?.numerator) || frame.numerator<=0 ||
    !Number.isSafeInteger(frame?.denominator) || frame.denominator<=0 ||
    !streams.length || streams.some(item=>!['video','audio'].includes(item.type)) || !streams.some(item=>item.type==='video'))
    fail('proxy_probe_invalid','CLI media probe lacks duration, canvas, frame rate or a decodable video stream');
  return {duration_us:value.duration_us,width:value.width,height:value.height,
    frame_rate:{numerator:frame.numerator,denominator:frame.denominator},streams};
}

/** 从校验过的 Rust CLI 探测结果生成代理与技术证据；调用者不能指定通过级别。 */
export function collectProxyEvidence(options) {
  if(!options || typeof options!=='object' || Array.isArray(options) ||
    Object.keys(options).some(key=>!OPTION_KEYS.has(key)))
    fail('proxy_evidence_options_invalid','proxy evidence options contain an unknown or privileged field');
  const {proxyPath,workflowId,revision,outputId,observedAt=new Date().toISOString(),env,pluginRoot}=options;
  if(typeof proxyPath!=='string' || !proxyPath.trim()) fail('proxy_artifact_missing','proxy artifact path is required');
  if(typeof workflowId!=='string' || !workflowId.trim() || typeof outputId!=='string' || !outputId.trim() ||
    !Number.isSafeInteger(revision) || revision<1 || !Number.isFinite(Date.parse(observedAt)))
    fail('proxy_evidence_options_invalid','workflow, revision, output and observation time are required');
  const absolute=path.resolve(proxyPath),before=hashRegularFile(absolute);
  const result=runJsonCommand({args:['media','probe',absolute],requiredCapabilities:['media.probe'],env,pluginRoot});
  if(result.exitCode!==0 || result.envelope?.ok!==true)
    fail('proxy_probe_failed','released CLI media probe did not return a successful JSON envelope');
  const probe=normalizeProbe(result.envelope.data),after=hashRegularFile(absolute);
  if(before.digest!==after.digest || before.bytes!==after.bytes)
    fail('proxy_artifact_changed','proxy content changed during evidence collection');
  const artifactId=`proxy-${sha256(canonical({workflowId,revision,outputId,digest:after.digest})).slice(0,20)}`;
  const environment=`jianying-cli/${result.ready.version}/${result.ready.sha256.slice(0,16)}`;
  const base={workflow_id:workflowId,revision,output_id:outputId,artifact_digest:after.digest,probe,
    cli:{version:result.ready.version,sha256:result.ready.sha256}};
  const proxyDigest=sha256(canonical({...base,type:'proxy'}));
  const technicalDigest=sha256(canonical({...base,type:'technical'}));
  const limitations=['CLI probe proves decodability and technical metadata, not narrative or subjective quality'];
  if(!probe.streams.some(item=>item.type==='audio')) limitations.push('proxy contains no audio stream');
  return {
    artifact:{artifact_id:artifactId,type:'proxy_media',digest:after.digest,bytes:after.bytes},
    evidence:{evidence_id:`probe-${technicalDigest.slice(0,20)}`,type:'media_probe',artifact_id:artifactId,
      digest:technicalDigest,role:'technical'},
    probe,
    bundle_items:[
      {evidence_id:`proxy-${proxyDigest.slice(0,20)}`,type:'proxy',digest:proxyDigest,validator:'jianying-cli.media.probe/v1',
        environment,observed_at:observedAt,passed:true,artifact_ref:artifactId,limitations},
      {evidence_id:`technical-${technicalDigest.slice(0,20)}`,type:'technical',digest:technicalDigest,
        validator:'jianying-cli.media.probe/v1',environment,observed_at:observedAt,passed:true,artifact_ref:artifactId,limitations},
    ],
  };
}

/** 从发布 Rust CLI 收集内容摘要绑定的关键帧、静音、峰值和响度事实。 */
export function collectMediaQualityEvidence(options) {
  if(!options || typeof options!=='object' || Array.isArray(options) ||
    Object.keys(options).some(key=>!OPTION_KEYS.has(key)))
    fail('proxy_evidence_options_invalid','media quality evidence options contain an unknown or privileged field');
  const {proxyPath,workflowId,revision,outputId,observedAt=new Date().toISOString(),env,pluginRoot}=options;
  if(typeof proxyPath!=='string'||!proxyPath.trim()||typeof workflowId!=='string'||!workflowId.trim()||
    typeof outputId!=='string'||!outputId.trim()||!Number.isSafeInteger(revision)||revision<1)
    fail('proxy_evidence_options_invalid','workflow, revision, output and proxy are required');
  const absolute=path.resolve(proxyPath),before=hashRegularFile(absolute);
  const result=runJsonCommand({args:['media','evidence',absolute],requiredCapabilities:['media.quality_evidence'],env,pluginRoot});
  if(result.exitCode!==0 || result.envelope?.ok!==true) fail('media_quality_evidence_failed','released CLI media evidence failed');
  const analysis=result.envelope.data,after=hashRegularFile(absolute);
  if(before.digest!==after.digest || before.bytes!==after.bytes || analysis?.schema!=='jianying-media-evidence/v1' ||
    analysis?.source?.sha256!==after.digest || !Array.isArray(analysis?.video?.keyframes) || !Array.isArray(analysis?.audio?.silences))
    fail('media_quality_evidence_invalid','CLI evidence is incomplete or does not bind the current proxy');
  const artifactId=`proxy-${sha256(canonical({workflowId,revision,outputId,digest:after.digest})).slice(0,20)}`;
  const bound={workflow_id:workflowId,revision,output_id:outputId,artifact_digest:after.digest,analysis};
  const digest=sha256(canonical(bound)),environment=`jianying-cli/${result.ready.version}/${result.ready.sha256.slice(0,16)}`;
  const measuredAudio=analysis.audio.present===true && Number.isFinite(analysis.audio.integrated_lufs) &&
    Number.isFinite(analysis.audio.true_peak_dbfs);
  const audioDigest=measuredAudio?sha256(canonical({media_quality_digest:digest,
    artifact_digest:after.digest,type:'audio_metrics'})):undefined;
  return {analysis,evidence:{evidence_id:`media-quality-${digest.slice(0,20)}`,type:'media_quality',artifact_id:artifactId,digest,role:'technical'},
    ...(measuredAudio?{audio_evidence:{evidence_id:`audio-metrics-${audioDigest.slice(0,20)}`,type:'audio_metrics',
      artifact_id:artifactId,digest:audioDigest,role:'technical'}}:{}),
    bundle_item:{evidence_id:`media-quality-${digest.slice(0,20)}`,type:'technical',digest,
      validator:analysis.algorithm,environment,observed_at:observedAt,passed:true,artifact_ref:artifactId,
      limitations:['keyframes, silence and loudness are technical facts; they do not prove narrative or subjective quality']}};
}
