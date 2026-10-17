"""只读隔离重关联文件LUT，并以实际原生采样渲染核对已交付像素。"""
import copy
import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import time


def load(name):
 spec=importlib.util.spec_from_file_location('resource_validation_'+name,Path(__file__).with_name(name+'.py'));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def node(data,pointer):
 for part in pointer.strip('/').split('/'):
  key=part.replace('~1','/').replace('~0','~');data=data[int(key)] if isinstance(data,list) else data[key]
 return data


def verify(root,project,inventory,frames,executable,*,timeout=120,dependencies=None,session_factory=None,before_render=None):
 """只验证当前工程的包内静态文件LUT和显式采样帧；不改写原包。"""
 report={'schema':'effectcraft-file-lut-validation/v1','status':'NOT_RUN','scope':'listed static file LUTs and decoded sample frames only; font/creative/temporal fidelity NOT_RUN','verifiedFrames':0,'verifiedLuts':0,'samples':[]}
 deadline=time.monotonic()+timeout;root=Path(root);lineage=load('artifact_lineage');resources=load('native_resources');image=load('image_sequence');tasks=load('task_store')
 try:
  current=resources.inspect(root,project,declared=inventory)
  if current!=inventory:raise ValueError('file_lut_inventory_changed')
  selected=[r for r in inventory['luts'] if r['source']=='file']
  if not selected:return dict(report,reason='no_file_lut')
  if any(not r['packaged'] for r in selected):return dict(report,reason='file_lut_content_unavailable')
  if any(r['kind']=='lut' for r in inventory['dynamic']):return dict(report,reason='dynamic_lut_unverified')
  if not frames:return dict(report,reason='matching_frame_evidence_missing')
  if len(frames)>8 or timeout<=0:return dict(report,reason='file_lut_validation_budget')
  original=lineage.file(root,project);native=lineage.read(original);bound={project:lineage.sha(original)};expected=[];decoded=0
  for frame in frames:
   source=lineage.file(root,frame['path'])
   if lineage.sha(source)!=frame['sha256']:raise ValueError('file_lut_frame_changed')
   facts=image.rgba_facts(source);decoded+=facts['width']*facts['height']*4
   if decoded>64*1024*1024:return dict(report,reason='file_lut_validation_budget')
   bound[frame['path']]=frame['sha256'];expected.append(facts)
  with tempfile.TemporaryDirectory(prefix='effectcraft LUT readonly ') as temporary:
   isolated=Path(temporary);target=isolated/'project.ecproj';candidate=copy.deepcopy(native);copies={};total=0
   def payload(name,digest):
    nonlocal total
    source=lineage.file(root,name)
    if lineage.sha(source)!=digest:raise ValueError('file_lut_dependency_changed')
    bound[name]=digest
    if digest not in copies:
     total+=source.stat().st_size
     if total>512*1024*1024:raise TimeoutError('file_lut_validation_budget')
     destination=isolated/'assets'/digest;destination.parent.mkdir(exist_ok=True);shutil.copyfile(source,destination)
     if lineage.sha(destination)!=digest:raise ValueError('file_lut_dependency_changed')
     copies[digest]=destination
    return str(copies[digest])
   for resource in selected:
    if resource['bytes']>16*1024*1024:raise TimeoutError('file_lut_validation_budget')
    node(candidate,resource['pointer'])['v']=payload(resource['path'],resource['sha256'])
   dependencies=dependencies or {}
   for item,value in candidate['items'].items():
    if value['kind']['type']!='Footage':continue
    if item not in dependencies:return dict(report,reason='media_dependency_binding_missing')
    asset=dependencies[item];value['kind']['path']=payload(asset['path'],asset['sha256'])
   tasks.atomic_json(target,candidate);snapshot_hash=lineage.sha(target)
   remaining=deadline-time.monotonic()
   if remaining<=0:raise TimeoutError('file_lut_validation_budget')
   factory=session_factory or load('mcp_session').Session
   with factory([executable,'--empty','mcp'],timeout=remaining) as session:
    def call(name,args):
     remaining=deadline-time.monotonic()
     if remaining<=0:raise TimeoutError('file_lut_validation_budget')
     session.timeout=remaining
     return load('commands').parse_reply(session.request('tools/call',{'name':name,'arguments':args}))
    call('open_project',{'path':str(target)})
    for index,(frame,facts) in enumerate(zip(frames,expected)):
     rendered=isolated/('sample-'+str(index)+'.png')
     if before_render:before_render(facts['width']*facts['height']*4)
     call('render_frame',{'comp':frame['composition']['id'],'time':frame['seconds'],'max_side':frame.get('maxSide',0),'transparent':frame.get('requestedAlpha',False),'inline':False,'path':str(rendered)})
     if not rendered.is_file() or rendered.is_symlink():raise ValueError('file_lut_render_missing')
     actual=image.rgba_facts(rendered)
     if any(actual[k]!=facts[k] for k in ('width','height','rgbaSha256')):raise ValueError('file_lut_render_mismatch')
     report['samples'].append({'path':frame['path'],'composition':frame['composition']['id'],'seconds':frame['seconds'],'rgbaSha256':facts['rgbaSha256'],'width':facts['width'],'height':facts['height']})
   if lineage.sha(target)!=snapshot_hash or any(lineage.sha(p)!=digest for digest,p in copies.items()):raise ValueError('file_lut_snapshot_changed')
  if any(lineage.sha(lineage.file(root,name))!=digest for name,digest in bound.items()):raise ValueError('file_lut_original_changed')
  report.update(status='PASS',verifiedFrames=len(frames),verifiedLuts=len(selected),originalsPreserved=True,projectSha256=bound[project],remappedProperties=[r['pointer'] for r in selected],nonTargetPropertiesPreserved=True)
 except (TimeoutError,subprocess.TimeoutExpired) as error:report.update(reason=str(error))
 except (ValueError,OSError,KeyError,TypeError,RuntimeError,subprocess.SubprocessError) as error:
  budget=isinstance(error,ValueError) and str(error) in ('resource_budget_exceeded','deadline_exceeded','parent_cancelled_or_expired','cancel_requested')
  report.update(status='NOT_RUN' if budget else 'FAIL',reason=str(error) if isinstance(error,ValueError) else type(error).__name__)
 return report


def aggregate(cases):
 statuses=[case['status'] for case in cases]
 return {'schema':'effectcraft-file-lut-review/v1','status':'FAIL' if 'FAIL' in statuses else ('PASS' if statuses and all(s=='PASS' for s in statuses) else 'NOT_RUN'),'projects':cases,'scope':'listed static file LUTs and sampled frames only; no font, complete temporal or creative qualification'}


def commands(root,data,executable,*,timeout=120,before_render=None):
 """消费已验证命令映射；只选择同工程版本、结构和依赖的帧。"""
 mapping=data.get('artifactMap',{})
 if 'nativeResources' not in mapping:return aggregate([])
 load('command_artifact').validate(root,mapping);deadline=time.monotonic()+timeout;cases=[]
 for project in mapping['contexts']['projects']:
  inventory=next(i for i in mapping['nativeResources'] if i['project']==project['path'])
  if not any(r['source']=='file' for r in inventory['luts']):continue
  frames=[f for f in mapping['contexts']['frames'] if all(f[k]==project[k] for k in ('snapshot','nativeVersion','dependencies'))]
  result=verify(root,project['path'],inventory,frames,executable,timeout=deadline-time.monotonic(),dependencies=project['dependencies'],before_render=before_render)
  cases.append(dict(result,project=project['path']))
 return aggregate(cases)


def workflow(root,executable,*,timeout=120,before_render=None):
 """兼容旧清单；当前工作流资源和帧必须属于已绑定文件表。"""
 quality=load('quality_review');root=Path(root);bound=quality.binding(root);manifest=quality.read(root/'manifest.json')
 if 'nativeResources' not in manifest:return aggregate([])
 inventory=manifest['nativeResources']
 if not any(r['source']=='file' for r in inventory['luts']):return aggregate([])
 comp=quality.read(root/'native.json')['composition'];frames=[dict(f,sha256=manifest['files'][f['path']],composition=comp,maxSide=0) for f in manifest.get('frames',[])]
 dependencies={str(a['item']):a for a in manifest.get('assets',{}).values()}
 result=verify(root,'project.ecproj',inventory,frames,executable,timeout=timeout,dependencies=dependencies,before_render=before_render)
 if quality.binding(root)!=bound:result.update(status='FAIL',reason='file_lut_original_changed')
 return aggregate([dict(result,project='project.ecproj')])


def budget_hook(store,task):
 """每次只读渲染先持久登记新尝试；重复review也不能返还资源预算。"""
 import secrets
 def reserve(decoded_bytes):load('resource_budget').reserve_review(store,task,secrets.token_hex(32),decoded_bytes)
 return reserve
