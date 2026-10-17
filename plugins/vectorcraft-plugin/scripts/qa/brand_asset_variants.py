#!/usr/bin/env python3
"""VC-DM-006 素材变体：真实原生命令、无关画板保全与显式QA故障注入。"""
import hashlib,importlib.util,json,os,shutil,sys
from pathlib import Path
from PIL import Image
import fitz
config=json.loads(Path(sys.argv[1]).read_text());root=Path(config['output']).resolve();root.mkdir(exist_ok=False)
origin=Path(config['skill']).resolve();runtime=Path(config['runtime']).resolve();skill=root/'isolated skill'
shutil.copytree(origin,skill,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def tree(path):return {p.relative_to(path).as_posix():sha(p) for p in sorted(path.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
identity=tree(origin);copied=tree(skill)
for name,size,color in [('old.png',(12,8),'#ef5b36'),('new.png',(24,16),'#2366e8')]:Image.new('RGB',size,color).save(root/name)
for name,color in [('old.svg','#ef5b36'),('new.svg','#2366e8')]:
 (root/name).write_text('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="16"><rect width="24" height="16" fill="'+color+'"/></svg>')
def asset(name):return {'path':str(root/name),'sha256':sha(root/name)}
exports=[{'format':f,'artboard':i} for i in range(3) for f in ['svg','pdf','png']]
plan={'document':{'name':'Registered brand variants','width':96,'height':80},'assets':{'logo':asset('old.png'),'mark':asset('old.svg')},'operations':[
 {'command':'artboard.new','params':{'name':'Variant','x':120,'y':0,'width':96,'height':80}},
 {'command':'artboard.new','params':{'name':'Control','x':240,'y':0,'width':96,'height':80}},
 *[{'command':'asset.place','params':{'asset':a,'rect':[x,16 if a=='logo' else 48,36,24]},'as':a+str(i)} for i,x in enumerate([12,132]) for a in ['logo','mark']],
 {'command':'shape.rectangle','params':{'x':252,'y':16,'width':36,'height':24},'as':'control'},
 {'command':'paint.setFill','params':{'color':'#ef5b36'}}, {'command':'paint.setStroke','params':{'none':True}}], 'exports':exports}
w=load('brand_asset_qa',skill/'scripts/workflow.py');source=root/'source';first=w.execute(plan,source,runtime_home=runtime);original=tree(source)
control=first['bindings']['control']['id']
# 仅在独立QA副本注入一次真实的无关对象填充修改；不修改安装副本。
proxy='''
import os
class _AssetFaultSession(Session):
 def request(self, method, params=None):
  value=super().request(method,params)
  args=(params or {}).get('arguments',{})
  marker=os.environ.get('CRAFT_BRAND_ASSET_FAULT_LOG')
  trigger=args.get('command')=='links.relink' and str(args.get('params',{}).get('path','')).endswith('/newLogo.png')
  if marker and trigger and not Path(marker).exists():
   result=super().request('tools/call',{'name':'run_command','arguments':{'command':'paint.setFill','params':{'ids':[int(os.environ['CRAFT_BRAND_ASSET_FAULT_OBJECT'])],'color':'#2366e8'}}})
   Path(marker).write_text(json.dumps(result))
  return value
Session=_AssetFaultSession
'''
# mcp_session imports Path/json already; keep this instrumentation bound separately.
with (skill/'scripts/mcp_session.py').open('a') as stream:stream.write(proxy)
instrumented=tree(skill)
fault_plan={'expectedProjectSha256':first['files']['project.vectorcraft'],'assets':{'newLogo':asset('new.png')},'operations':[{'command':'asset.replace','params':{'asset':'logo','replacement':'newLogo'}}],'exports':exports}
os.environ['CRAFT_BRAND_ASSET_FAULT_OBJECT']=str(control);os.environ['CRAFT_BRAND_ASSET_FAULT_LOG']=str(root/'injection.json')
refused=False
try:w.execute(fault_plan,root/'fault',source=source,runtime_home=runtime)
except ValueError as error:
 refused='brand_dependency_violation' in str(error)
 if not refused:raise
finally:
 os.environ.pop('CRAFT_BRAND_ASSET_FAULT_OBJECT',None);os.environ.pop('CRAFT_BRAND_ASSET_FAULT_LOG',None)
assert (root/'injection.json').exists()
injection=json.loads((root/'injection.json').read_text());assert not injection.get('isError',False)
if config.get('baseline'):
 assert not refused and (root/'fault/manifest.json').exists()
 proof={'schema':'vectorcraft-brand-asset-baseline/v1','result':'FAIL','expectedGapConfirmed':True,'reason':'published workflow accepted a real nonconsumer mutation after asset replacement','originFiles':identity,'driverSha256':sha(__file__),'runtimeSha256':first['runtimeSha256'],'unrelatedObjectId':control,'injection':injection}
 (root/'proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'result':'FAIL','expectedGapConfirmed':True}));sys.exit(0)
assert refused and not (root/'fault/manifest.json').exists()
failure=json.loads((root/'fault/failure.json').read_text());stage=(root/'fault'/failure['stage']).resolve();assert not failure['replayAllowed']
check=json.loads((stage/'brand-dependencies.json').read_text())['checks'][0]
assert check['status']=='failed' and control in check['affectedObjectIds'] and check['unexpectedDependencies']
assert check['checkpointRetained'] and sha(stage/check['checkpoint'])==check['checkpointSha256']
sessions=load('brand_asset_sessions',skill/'scripts/mcp_session.py');binary=runtime/'vectorcraft/0.2.0-craft.2/vectorcraft-cli'
brand=w.brand_module()
def reopen(directory,project='project.vectorcraft'):
 with sessions.Session([str(binary),'mcp','--headless']) as s:
  s.command('document.open',{'path':str(directory/project)})
  native=s.command('document.json',{});links=s.command('links.check',{})
  assert links['missing']==0 and links['modified']==0
  return native
checkpoint=reopen(stage,check['checkpoint']);old=json.loads((source/'native.json').read_text())
assert brand.snapshot(checkpoint)[control]==brand.snapshot(old)[control] and checkpoint['artboards']==old['artboards']
for name,value in failure['files'].items():assert sha(stage/name)==value['sha256']
healthy_plan={'expectedProjectSha256':first['files']['project.vectorcraft'],'assets':{'newLogo':asset('new.png'),'newMark':asset('new.svg')},'operations':[
 {'command':'asset.replace','params':{'asset':'logo','replacement':'newLogo'}}, {'command':'asset.replace','params':{'asset':'mark','replacement':'newMark'}}]}
healthy=root/'healthy';manifest=w.execute(healthy_plan,healthy,source=source,runtime_home=runtime)
assert len(manifest['outputs'])==9
checks=json.loads((healthy/'brand-dependencies.json').read_text())['checks'];assert len(checks)==2 and all(x['status']=='passed' and x['checkpointRetained'] is False for x in checks)
assert checks[0]['consumerIds']==first['assets']['logo']['ids'] and checks[0]['replacementIds']==checks[0]['consumerIds']
assert checks[1]['consumerIds']==first['assets']['mark']['ids'] and checks[1]['replacementIds']!=checks[1]['consumerIds']
assert sha(healthy/'brand-dependencies.json')==manifest['brandDependencyReport']['sha256']
new=reopen(healthy);assert brand.snapshot(new)[control]==brand.snapshot(old)[control]
decoded=[]
for i in range(3):
 for fmt in ['svg','pdf','png']:
  name='artboard-'+str(i+1)+'.'+fmt
  assert (sha(source/name)==sha(healthy/name)) is (i==2)
  if fmt=='png':
   with Image.open(healthy/name) as im:im.verify()
   with Image.open(healthy/name) as im:
    assert im.size==(96,80)
    if i<2:
     rgb=im.convert('RGB');assert rgb.getpixel((20,24))==(35,102,232) and rgb.getpixel((20,56))==(35,102,232)
  else:
   with fitz.open(healthy/name) as doc:assert len(doc)==1 and doc[0].rect.width==96 and doc[0].rect.height==80
  decoded.append({'path':name,'result':'PASS','sha256':sha(healthy/name),'unrelatedUnchanged':i==2})
empty_plan={**healthy_plan,'exports':[]};empty=w.execute(empty_plan,root/'empty',source=source,runtime_home=runtime);assert empty['outputs']==[];reopen(root/'empty')
# 摘要篡改和链接清单必须在安装／原生编辑前拒绝。
preflight=[]
for fault in ['tampered-plan','linked-plan','unknown-asset']:
 copy=root/fault;shutil.copytree(source,copy);value=json.loads(json.dumps(healthy_plan));output=root/(fault+'-output');cache=root/(fault+'-runtime')
 if fault=='tampered-plan':(copy/'plan.json').write_text('{}')
 elif fault=='linked-plan':(copy/'plan.json').unlink();(copy/'plan.json').symlink_to(source/'plan.json')
 else:value['operations'][0]['params']['asset']='missing'
 try:w.execute(value,output,source=copy,runtime_home=cache)
 except ValueError as error:reason=str(error)
 else:raise AssertionError('invalid plan accepted')
 assert not output.exists() and not cache.exists()
 preflight.append({'fault':fault,'reason':reason,'result':'PASS','beforeRuntimeAndOutput':True})
assert tree(source)==original and tree(origin)==identity and tree(skill)==instrumented
proof={'schema':'vectorcraft-brand-asset-native/v1','result':'PASS','level':config.get('level','native-candidate'),'platform':'Darwin-arm64','runtimeSha256':sha(binary),'driverSha256':sha(__file__),
 'originFiles':identity,'copiedFiles':copied,'instrumentedFiles':instrumented,'qaInstrumentation':proxy,'sourceFiles':original,'updatedFiles':tree(healthy),'manifest':manifest,'checks':checks,'decoded':decoded,
 'fault':{'result':'PASS','explicitQaNativeMutation':True,'injection':injection,'check':check,'failure':failure,'checkpointIndependentlyReopened':True,'retainedFilesVerified':True},'preflight':preflight,
 'explicitEmptyExportsPreserved':True,'sourceAndInstalledSkillPreserved':True,'scope':'registered raster and SVG assets with two consumers each; three artboards with unrelated SVG/PDF/PNG byte preservation; independent native reopen; QA-only nonconsumer mutation refusal; no GUI/model/universal-format claim'}
# failure diagnostics contain private staging paths; only retain portable identities and reasons.
proof['fault']['failure']={k:failure[k] for k in ['replayAllowed','files']}
(root/'proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'result':'PASS','decoded':9,'unrelatedBytePreservation':3,'faults':4}))
