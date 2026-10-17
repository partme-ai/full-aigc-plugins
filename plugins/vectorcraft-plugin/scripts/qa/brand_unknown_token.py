#!/usr/bin/env python3
"""真实固定安装入口的未知色板拒绝及检查点保全；不重放失败命令。"""
import hashlib,importlib.util,json,sys,shutil
from pathlib import Path
c=json.loads(Path(sys.argv[1]).read_text());root=Path(c['output']).resolve();root.mkdir(exist_ok=False)
skill=Path(c['skill']);source=Path(c['source']);runtime=Path(c['runtime'])
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def tree(path):return {p.relative_to(path).as_posix():sha(p) for p in sorted(path.rglob('*')) if p.is_file()}
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
original=tree(source);identity=tree(skill);manifest=json.loads((source/'manifest.json').read_text())
w=load('unknown_token_workflow',skill/'scripts/workflow.py');output=root/'unknown'
try:w.execute({'expectedProjectSha256':manifest['files']['project.vectorcraft'],'operations':[{'command':'swatch.edit','params':{'name':'MissingBrandToken-VC-DM-006','color':'#175cce'}}]},output,source=source,runtime_home=runtime)
except (RuntimeError,ValueError) as error:reason=str(error)
else:raise AssertionError('unknown token accepted')
assert 'outcome_unknown' not in reason and not (output/'manifest.json').exists()
failure=json.loads((output/'failure.json').read_text());assert failure['replayAllowed'] is False
stage=(output/failure['stage']).resolve()
for name,row in failure['files'].items():assert sha(stage/name)==row['sha256']
checkpoints=list(stage.glob('brand-checkpoint-*.vectorcraft'));assert len(checkpoints)==1
sessions=load('unknown_token_sessions',skill/'scripts/mcp_session.py');binary=runtime/'vectorcraft/0.2.0-craft.2/vectorcraft-cli'
with sessions.Session([str(binary),'mcp','--headless']) as s:
 s.command('document.open',{'path':str(checkpoints[0])});model=s.command('document.json',{})
before=json.loads((source/'native.json').read_text());assert model['layers']==before['layers'] and model['artboards']==before['artboards']
assert tree(source)==original and tree(skill)==identity
linked_refusals=[]
for mode in ['direct','native-gateway']:
    copied=root/('linked-source-'+mode);shutil.copytree(source,copied)
    (copied/'plan.json').unlink();(copied/'plan.json').symlink_to(source/'plan.json')
    edit={'command':'swatch.edit','params':{'name':'Brand Primary','color':'#175cce'}}
    plan={'expectedProjectSha256':manifest['files']['project.vectorcraft'],'operations':[edit if mode=='direct' else {'command':'native.command','params':edit}]}
    output_path=root/('linked-output-'+mode);empty_runtime=root/('empty-runtime-'+mode)
    try:w.execute(plan,output_path,source=copied,runtime_home=empty_runtime)
    except ValueError as error:assert 'brand_source_plan_digest_mismatch' in str(error)
    else:raise AssertionError('linked export plan accepted')
    assert not output_path.exists() and not empty_runtime.exists()
    linked_refusals.append({'mode':mode,'result':'PASS','beforeRuntimeAndOutput':True})
proof={'schema':'vectorcraft-brand-unknown-token-native/v1','result':'PASS','level':'fixed-install','platform':'Darwin-arm64','driverSha256':sha(__file__),'runtimeSha256':sha(binary),'skillFiles':identity,'inputFiles':original,'reason':reason,'failureFiles':failure['files'],'unknownSwatchRefused':True,'noSuccessManifest':True,'replayAllowed':False,'checkpointIndependentlyReopened':True,'checkpointSha256':sha(checkpoints[0]),'sourceAndSkillPreserved':True,'linkedPlanRefusals':linked_refusals}
(root/'proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'result':'PASS','unknownTokenRefused':True}))
