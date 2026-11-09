import test from 'node:test';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import {collectMediaQualityEvidence,collectProxyEvidence} from '../scripts/quality_proxy_evidence.mjs';
import {buildEvidenceBundle} from '../scripts/quality_evidence.mjs';

function fixture(t,{mutate=false,incomplete=false,noAudio=false}={}) {
  const root=fs.mkdtempSync(path.join(os.tmpdir(),'jy-proxy-evidence-'));
  t.after(()=>fs.rmSync(root,{recursive:true,force:true}));
  fs.mkdirSync(path.join(root,'runtime'),{recursive:true});
  const cli=path.join(root,'jianying');
  fs.writeFileSync(cli,`#!/usr/bin/env node
const fs=require('node:fs');
const args=process.argv.slice(2).filter(value=>value!=='--json');
if(args.includes('--version')) {console.log('jianying 1.6.19');process.exit(0);}
if(args[0]==='capabilities') {console.log(JSON.stringify({ok:true,data:{schema:'jianying-capabilities/v1',cli_version:'1.6.19',capabilities:[
  {id:'capabilities',status:'supported'},{id:'schema.job_v2',status:'supported'},{id:'job.run',status:'supported'},
  {id:'media.probe',status:'supported'},{id:'media.quality_evidence',status:'supported'}]}}));process.exit(0);}
if(args[0]==='media' && args[1]==='probe') {
  ${mutate?"fs.appendFileSync(args[2],'changed');":''}
  console.log(JSON.stringify({ok:true,data:${incomplete?"{duration_us:3000000,width:640,height:360,streams:['video']}" :
    "{duration_us:3000000,width:640,height:360,frame_rate:{numerator:30,denominator:1},streams:[{type:'video'},{type:'audio'}]}"}}));
  process.exit(0);
}
if(args[0]==='media' && args[1]==='evidence') {
  const digest=require('node:crypto').createHash('sha256').update(fs.readFileSync(args[2])).digest('hex');
  console.log(JSON.stringify({ok:true,data:{schema:'jianying-media-evidence/v1',algorithm:'jianying-media-evidence/1.0.0',
    source:{sha256:digest,bytes:fs.statSync(args[2]).size},video:{present:true,keyframes:[{time_us:0}]},
    audio:${noAudio?"{present:false,silences:[],integrated_lufs:null,true_peak_dbfs:null}":"{present:true,silences:[{start_us:1000000,end_us:1500000}],integrated_lufs:-16,true_peak_dbfs:-1.2}"}}}));process.exit(0);
}
console.log(JSON.stringify({ok:false,error:{type:'unsupported'}}));process.exit(1);
`,{mode:0o755});
  const sha256=crypto.createHash('sha256').update(fs.readFileSync(cli)).digest('hex');
  fs.writeFileSync(path.join(root,'runtime/jianying-cli.lock.json'),JSON.stringify({minimumVersion:'1.6.19',
    capabilitySchema:'jianying-capabilities/v1',jobSchema:'jianying-job/v2',requiredCapabilities:['capabilities'],artifacts:{}}));
  const proxy=path.join(root,'proxy.mp4'); fs.writeFileSync(proxy,Buffer.alloc(4096,7));
  return {proxyPath:proxy,pluginRoot:root,env:{JIANYING_CLI_PATH:cli,JIANYING_CLI_SHA256:sha256}};
}

test('released-adapter probe becomes digest-bound proxy and technical evidence',t=>{
  const input=fixture(t);
  const result=collectProxyEvidence({...input,workflowId:'VLOG-01',revision:1,outputId:'main',
    observedAt:'2026-09-21T00:00:00.000Z'});
  assert.equal(result.artifact.type,'proxy_media');
  assert.equal(result.artifact.bytes,4096);
  assert.match(result.artifact.digest,/^[a-f0-9]{64}$/);
  assert.equal(result.probe.duration_us,3000000);
  assert.deepEqual(result.probe.frame_rate,{numerator:30,denominator:1});
  assert.deepEqual(result.bundle_items.map(item=>item.type),['proxy','technical']);
  assert.ok(result.bundle_items.every(item=>item.artifact_ref===result.artifact.artifact_id && item.passed));
  const bundle=buildEvidenceBundle({workflowId:'VLOG-01',revision:1,outputId:'main',artifactDigest:result.artifact.digest,
    items:result.bundle_items,requiredTypes:['structural','technical','creative']});
  assert.equal(bundle.conclusion,'incomplete');
  assert.equal(JSON.stringify(result).includes(input.proxyPath),false);
});

test('missing empty symlink incomplete and concurrently replaced proxies fail closed',t=>{
  const input=fixture(t);
  assert.throws(()=>collectProxyEvidence({...input,proxyPath:path.join(path.dirname(input.proxyPath),'missing.mp4'),
    workflowId:'VLOG-01',revision:1,outputId:'main'}),error=>error.code==='proxy_artifact_missing');
  fs.writeFileSync(input.proxyPath,'');
  assert.throws(()=>collectProxyEvidence({...input,workflowId:'VLOG-01',revision:1,outputId:'main'}),
    error=>error.code==='proxy_artifact_invalid');

  const linked=fixture(t); const target=linked.proxyPath; linked.proxyPath=path.join(path.dirname(target),'linked.mp4'); fs.symlinkSync(target,linked.proxyPath);
  assert.throws(()=>collectProxyEvidence({...linked,workflowId:'VLOG-01',revision:1,outputId:'main'}),
    error=>error.code==='proxy_artifact_invalid');

  const incomplete=fixture(t,{incomplete:true});
  assert.throws(()=>collectProxyEvidence({...incomplete,workflowId:'VLOG-01',revision:1,outputId:'main'}),
    error=>error.code==='proxy_probe_invalid');

  const changed=fixture(t,{mutate:true});
  assert.throws(()=>collectProxyEvidence({...changed,workflowId:'VLOG-01',revision:1,outputId:'main'}),
    error=>error.code==='proxy_artifact_changed');
});

test('caller cannot request or inject a higher evidence level',t=>{
  const input=fixture(t);
  assert.throws(()=>collectProxyEvidence({...input,workflowId:'VLOG-01',revision:1,outputId:'main',
    requestedEvidenceLevel:'native_export'}),error=>error.code==='proxy_evidence_options_invalid');
  assert.throws(()=>collectProxyEvidence({...input,workflowId:'VLOG-01',revision:1,outputId:'main',passed:true}),
    error=>error.code==='proxy_evidence_options_invalid');
});

test('released CLI media evidence binds keyframes silence peak and loudness to proxy digest',t=>{
  const input=fixture(t);
  const result=collectMediaQualityEvidence({...input,workflowId:'VLOG-01',revision:1,outputId:'main',
    observedAt:'2026-09-21T00:00:00.000Z'});
  assert.equal(result.analysis.video.keyframes[0].time_us,0);
  assert.equal(result.analysis.audio.silences[0].start_us,1_000_000);
  assert.equal(result.analysis.audio.integrated_lufs,-16);
  assert.equal(result.analysis.audio.true_peak_dbfs,-1.2);
  assert.equal(result.evidence.role,'technical');
  assert.equal(result.audio_evidence.type,'audio_metrics');
  assert.equal(result.audio_evidence.artifact_id,result.evidence.artifact_id);
  assert.match(result.bundle_item.validator,/jianying-media-evidence/);
  assert.match(result.bundle_item.limitations[0],/do not prove narrative/);
});

test('released CLI reporting no audio cannot mint audio metrics evidence',t=>{
  const input=fixture(t,{noAudio:true});
  const result=collectMediaQualityEvidence({...input,workflowId:'VLOG-01',revision:1,outputId:'main'});
  assert.equal(result.analysis.audio.present,false);
  assert.equal(result.audio_evidence,undefined);
});
