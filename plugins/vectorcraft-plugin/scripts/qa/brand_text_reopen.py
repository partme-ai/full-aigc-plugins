#!/usr/bin/env python3
"""外部QA：独立重开实际文字返工交付，核验原生对象、字体和失败现场，不修改安装副本。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

config=json.loads(Path(sys.argv[1]).read_text())
root=Path(config['evidence']).resolve();skill=Path(config['skill']).resolve()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def hashes(d):return {p.relative_to(d).as_posix():sha(p) for p in sorted(d.rglob('*')) if p.is_file()}
def module(name):
 spec=importlib.util.spec_from_file_location('brand_reopen_'+name,skill/'scripts'/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
before=hashes(root);identity=hashes(skill);lock=json.loads((skill/'scripts/runtime.lock.json').read_text());binary=Path(config['runtime'])/'vectorcraft'/lock['resolvedVersion']/'vectorcraft-cli';assert sha(binary)==lock['artifacts']['darwin-arm64']['binarySha256']
Session=module('mcp_session').Session;snapshot=module('brand_variants').snapshot;cases=[]
for name in ('v1','v2'):
 directory=root/name;manifest=json.loads((directory/'manifest.json').read_text());expected=json.loads((directory/'native.json').read_text())
 for path,digest in manifest['files'].items():assert sha(directory/path)==digest
 with Session([str(binary),'mcp','--headless']) as session:
  session.command('document.open',{'path':str(directory/'project.vectorcraft')});native=session.command('document.json',{});fonts=session.command('text.fonts',{})
 assert session.process.returncode is not None
 assert snapshot(native)==snapshot(expected);assert native['artboards']==expected['artboards'];assert all(not x['missing'] for x in fonts)
 rendered=json.dumps(native,ensure_ascii=False);assert ('新品上市' if name=='v1' else '品牌焕新') in rendered and 'SAFE' in rendered and 'Songti SC' in rendered
 cases.append({'name':name,'result':'PASS','nativeObjectsMatchSavedDelivery':True,'fontDependenciesAvailable':True,'nativeTextPreserved':True,'reopenSessionExited':True,'files':hashes(directory),'manifest':manifest})
failures=[]
# 旧测试复制失败记录时未复制同级暂存目录；此处重新执行真实拒绝并原地保留全现场。
probe=Path(config['output']).parent/'failure-probes-v2';probe.mkdir(exist_ok=False);workflow=module('workflow')
source=root/'v1';source_manifest=json.loads((source/'manifest.json').read_text())
unknown={'expectedProjectSha256':source_manifest['files']['project.vectorcraft'],'operations':[{'command':'text.setText','params':{'id':999999999,'text':'其他标题'}}]}
missing=json.loads((skill/'examples/chinese-text.json').read_text());missing['operations'][0]['params']['font']='Craft Missing CJK Family 72625'
for name,plan,source_dir,error_type,reason in [('unknown-target-failure',unknown,source,RuntimeError,None),('missing-font-failure',missing,None,ValueError,'missing_fonts')]:
 d=probe/name
 try:workflow.execute(plan,d,source=source_dir,runtime_home=Path(config['runtime']))
 except error_type as error:
  if reason:assert reason in str(error)
 else:raise AssertionError('invalid text delivery admitted')
 f=json.loads((d/'failure.json').read_text());assert f['replayAllowed'] is False and not (d/'manifest.json').exists()
 if reason:assert reason in json.dumps(f)
 stage=(d/f['stage']).resolve();assert stage.is_relative_to(probe) and stage.is_dir()
 for path,record in f.get('files',{}).items():assert sha(stage/path)==record['sha256']
 failures.append({'name':name,'result':'PASS','noSuccessManifest':True,'replayAllowed':False,'failureRecord':f,'retainedStageFilesVerified':True,'files':hashes(d),'stageFiles':hashes(stage)})
assert before==hashes(root) and identity==hashes(skill)
proof={'schema':'vectorcraft-brand-text-reopen/v1','result':'PASS','driverSha256':sha(__file__),'runtimeSha256':sha(binary),'cases':cases,'failures':failures,'originalAndRevisedDeliveriesUnchanged':True,'installedSkillUnchanged':True,'scope':'independent native reopen of actual Chinese create/revision deliveries; all saved object properties, artboards, text and native font dependencies; no GUI or OS-font claim'}
Path(config['output']).write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'result':'PASS','nativeReopens':2,'retainedFailures':2}))
