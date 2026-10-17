"""受管理命令/桌面的内部交付观察；公开回执与用户输出保持原样。"""
import hashlib
import json
import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import time


def load(name):
    spec=importlib.util.spec_from_file_location('command_delivery_'+name,Path(__file__).with_name(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def read(path):return load('quality_review').read(path)
def sha(path):return load('task_store').file_sha(path)


def directory(store,task):
    path=store.path(task).parent/'command-delivery'
    if path.is_symlink():raise ValueError('command_delivery_symlink')
    return path


def relative(output,path):
    value=Path(path)
    if not value.is_absolute():value=output/value
    if value.is_symlink() or not value.resolve().is_relative_to(output.resolve()):
        raise ValueError('command_artifact_outside_output')
    name=value.resolve().relative_to(output.resolve()).as_posix()
    if name in ('success.json','journal.json','failure.json','desktop-session.json','desktop.log') or name.startswith('.desktop-data/'):
        raise ValueError('command_artifact_reserved')
    return name


def kind(record):
    if record.get('tool')=='save_project' or record.get('command') in ('file.save','file.saveAs','file.saveCopy'):
        return 'project'
    if record.get('tool')=='render_frame' or record.get('command')=='render.saveCurrentPreview':return 'frame'
    return None


def call(session,name,args,deadline=None):
    if deadline is not None:
        remaining=deadline-time.monotonic()
        if remaining<=0:raise TimeoutError('command_engineering_timeout')
        session.timeout=min(getattr(session,'timeout',remaining),remaining)
    return load('commands').parse_reply(session.request('tools/call',{'name':name,'arguments':args}))


def snapshot(session,deadline=None):
    """以固定time=0读取所有合成/图层，避免界面时间影响结构比较。"""
    overview=call(session,'get_project',{},deadline)
    comps={}
    for item in overview['items']:
        if item['type']!='Composition':continue
        comp=call(session,'get_comp',{'comp':item['id']},deadline)
        layers={str(layer['id']):call(session,'get_layer',{'comp':comp['id'],'layer':layer['id'],'time':0},deadline) for layer in comp['layers']}
        comps[str(comp['id'])]={'composition':comp,'layers':layers}
    return {'compositions':comps,'footageItems':sorted(item['id'] for item in overview['items'] if item['type'] not in ('Composition','Folder','Solid'))},overview


def dependencies(output,project):
    """固定原生JSON格式中的素材地址必须属于受管理输出包。"""
    data=read(output/project)
    if data.get('schema')!=1 or not isinstance(data.get('items'),dict):raise ValueError('command_project_format_unsupported')
    result={}
    for item in data['items'].values():
        source=item['kind']
        if source['type']!='Footage':continue
        name=relative(output,source['path']) if Path(source['path']).is_absolute() else relative(output,(output/project).parent/source['path'])
        result[str(item['id'])]={'path':name,'sha256':sha(output/name)}
    return result


def live_context(session,output):
    """固定只读脚本获取原生修订号与真实素材地址，不执行用户脚本。"""
    code='(function(){var r=[];for(var i=1;i<=app.project.numItems;i++){var x=app.project.item(i);if(x instanceof FootageItem && x.file){r.push({id:x.id,path:x.file.fsName});}}return {revision:app.project.__info().revision,footage:r};})()'
    reply=call(session,'run_script',{'code':code,'name':'readonly managed delivery identity'})
    value=reply.get('result') if isinstance(reply,dict) else None
    if (not isinstance(reply,dict) or reply.get('ok') is not True or not isinstance(value,dict) or type(value.get('revision')) is not int
            or value['revision']<0 or not isinstance(value.get('footage'),list)):
        raise ValueError('command_native_context_unavailable')
    assets={}
    for row in value['footage']:
        if not isinstance(row,dict) or type(row.get('id')) is not int or row['id']<=0 or not isinstance(row.get('path'),str):
            raise ValueError('command_native_context_unavailable')
        item=str(row['id'])
        if item in assets:raise ValueError('command_native_dependencies_mismatch')
        name=relative(output,row['path']);assets[item]={'path':name,'sha256':sha(output/name)}
    return {'revision':value['revision'],'dependencies':assets}


class Observer:
    """保存/渲染前持久化上下文，返回后绑定实际文件；缺失记录不补建。"""
    def __init__(self,store,task):self.store=store;self.task=task

    def __call__(self,session,record,phase):
        artifact=kind(record)
        if artifact is None:return
        state=self.store.read(self.task);output=Path(state['output']);base=directory(self.store,self.task)
        identity={k:record.get(k) for k in ('index','tool','command','params')}
        operation=load('task_store').digest(identity)
        before=base/'observations'/(str(record['index'])+'.before.json')
        after=base/'observations'/(str(record['index'])+'.json')
        if phase=='before':
            self.store.allowed(state)
            # 显式输出先校验边界；未指定保存路径时再查询当前原生路径。
            path=record['params'].get('path')
            if path:relative(output,path)
            context=live_context(session,output)
            native,overview=snapshot(session)
            if context!=live_context(session,output):raise ValueError('command_native_context_changed')
            if sorted(int(item) for item in context['dependencies'])!=native['footageItems']:
                raise ValueError('command_native_dependencies_mismatch')
            path=path or (overview.get('path') if artifact=='project' else None)
            if not path:return
            name=relative(output,path)
            data={'schema':'effectcraft-command-observation/v1','taskId':self.task,'identityHash':state['identityHash'],
                  'operationHash':operation,'index':record['index'],'kind':artifact,'path':name,'snapshot':native,'nativeVersion':context['revision'],'dependencies':context['dependencies']}
            if artifact=='frame':
                comp=call(session,'get_comp',{'comp':record['params'].get('comp',overview['activeComp'])})
                data.update(composition=comp,seconds=record['params'].get('time',overview.get('time',0)),
                    requestedAlpha=record['params'].get('transparent',False),maxSide=record['params'].get('max_side',0 if record.get('command')=='render.saveCurrentPreview' else 960))
                width=comp['width'];height=comp['height']
                if type(width) is not int or type(height) is not int or min(width,height)<=0:raise ValueError('command_composition_dimensions_invalid')
                load('resource_budget').reserve_command(self.store,self.task,operation,width*height*4)
                load('resource_meter').watch(self.store,self.task,output,output,'commands',media=[name])
            load('review_ledger').immutable(before,data)
        elif phase=='after':
            if not before.exists():
                if record['params'].get('path'):raise ValueError('command_observation_missing')
                return
            data=read(before)
            if data['operationHash']!=operation or data['identityHash']!=state['identityHash'] or record['state']!='succeeded':
                raise ValueError('command_observation_mismatch')
            after_context=live_context(session,output)
            if after_context!={'revision':data['nativeVersion'],'dependencies':data['dependencies']}:
                raise ValueError('command_render_dependency_changed' if artifact=='frame' else 'command_native_context_changed')
            name=data['path'];data.update(sha256=sha(output/name),beforeSha256=sha(before))
            if artifact=='frame':
                result=record.get('result',{})
                data['inlineCopies']=[{'path':relative(output,item['path']),'sha256':item['sha256']}
                    for item in result.get('content',[]) if isinstance(item,dict) and item.get('type')=='image'
                    and item.get('sha256')==data['sha256'] and item.get('path')] if isinstance(result,dict) else []
            if artifact=='project':
                if dependencies(output,name)!=data['dependencies']:raise ValueError('command_native_dependencies_mismatch')
                if sorted(int(item) for item in data['dependencies'])!=data['snapshot']['footageItems']:
                    raise ValueError('command_native_dependencies_mismatch')
            load('review_ledger').immutable(after,data)
            if artifact=='frame':load('resource_meter').sample(self.store,self.task)
        else:raise ValueError('command_observation_phase')


def inventory(output):
    files={}
    for path in sorted(output.rglob('*')):
        name=path.relative_to(output).as_posix()
        if name.split('/')[0] in ('.desktop-data','desktop.log','journal.json','success.json','failure.json','desktop-session.json'):continue
        if path.is_symlink():raise ValueError('command_artifact_symlink')
        if path.is_file():files[name]=sha(path)
    return files


def finalize(store,task):
    """成功回执落盘后固定内部清单；不更改公开输出，不复建旧任务基线。"""
    state=store.read(task);output=Path(state['output']);base=directory(store,task)
    receipt=read(output/'success.json')
    if (receipt.get('schema')!='craft-command-receipt/v1' or receipt.get('result')!='PASS'
            or receipt.get('runtimeSha256')!=state['identity']['runtimeSha256']
            or receipt.get('pluginId')!='effectcraft'
            or receipt.get('mode')!=('bridge' if state['identity']['mode']=='desktop' else 'headless')
            or receipt.get('planSha256')!=hashlib.sha256(json.dumps(state['plan'],ensure_ascii=False,sort_keys=True,allow_nan=False).encode()).hexdigest()):raise ValueError('command_receipt_mismatch')
    current={};observations={}
    for step in receipt['steps']:
        if step['state']!='succeeded':raise ValueError('command_step_unresolved')
        path=base/'observations'/(str(step['index'])+'.json')
        if path.exists():
            data=read(path)
            if (data['taskId']!=task or data['identityHash']!=state['identityHash']
                    or data['operationHash']!=load('task_store').digest({k:step.get(k) for k in ('index','tool','command','params')})
                    or data['beforeSha256']!=sha(path.with_name(str(step['index'])+'.before.json'))):
                raise ValueError('command_observation_mismatch')
            observations[path.name]=sha(path);current[data['path']]=data
        elif kind(step) and step['params'].get('path'):raise ValueError('command_observation_missing')
    for name,data in current.items():
        if sha(output/name)!=data['sha256']:raise ValueError('command_artifact_changed')
    data={'schema':'effectcraft-command-delivery/v1','taskId':task,'identityHash':state['identityHash'],
          'receiptSha256':sha(output/'success.json'),'files':inventory(output),'observations':observations,
          'projects':[v for v in current.values() if v['kind']=='project'],
          'frames':[v for v in current.values() if v['kind']=='frame']}
    data['artifactMap']=load('command_artifact').build(store,state,data)
    load('review_ledger').immutable(base/'delivery.json',data)
    return {'receiptSha256':data['receiptSha256'],'commandDeliverySha256':sha(base/'delivery.json'),'engineeringReopen':'NOT_RUN',
            'commandArtifacts':load('command_artifact').reference(data['artifactMap'])}


def document(store,task,proof=None):
    state=store.read(task);base=directory(store,task);path=base/'delivery.json';proof=proof if proof is not None else state.get('delivery') or {}
    if not proof.get('commandDeliverySha256'):raise ValueError('legacy_command_delivery_read_only')
    if sha(path)!=proof['commandDeliverySha256']:raise ValueError('command_delivery_changed')
    data=read(path);output=Path(state['output'])
    if (data['schema']!='effectcraft-command-delivery/v1' or data['taskId']!=task or data['identityHash']!=state['identityHash']
            or data['receiptSha256']!=proof['receiptSha256'] or sha(output/'success.json')!=proof['receiptSha256']):
        raise ValueError('command_receipt_changed')
    for name,expected in data['observations'].items():
        path=load('quality_review').contained(base/'observations',name)
        if sha(path)!=expected:raise ValueError('command_observation_changed')
        observed=read(path)
        if sha(path.with_name(str(observed['index'])+'.before.json'))!=observed['beforeSha256']:
            raise ValueError('command_observation_changed')
    if inventory(output)!=data['files']:raise ValueError('command_artifact_changed')
    for project in data['projects']:
        if dependencies(output,project['path'])!=project['dependencies']:raise ValueError('command_dependency_changed')
    if 'artifactMap' in data:
        adapter=load('command_artifact');adapter.verify_document(store,state,data)
        if proof.get('commandArtifacts')!=adapter.reference(data['artifactMap']):raise ValueError('command_artifact_reference_changed')
    return data


def verify_projects(output,projects,executable,timeout=120,session_factory=None):
    """隔离打开每个当前保存工程；仅重映射副本素材地址，原件不保存。"""
    report={'status':'NOT_RUN','fresh':False,'projects':[]}
    if not projects:return dict(report,reason='no_saved_native_project')
    session_factory=session_factory or load('mcp_session').Session
    deadline=time.monotonic()+timeout
    try:
        for project in projects:
            if sha(output/project['path'])!=project['sha256']:raise ValueError('command_artifact_changed')
            with tempfile.TemporaryDirectory(prefix='effectcraft command readonly ') as temporary:
                root=Path(temporary);target=root/project['path'];target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(output/project['path'],target)
                if sha(target)!=project['sha256']:raise ValueError('command_snapshot_changed')
                native=read(target)
                for item,asset in project['dependencies'].items():
                    source=load('quality_review').contained(output,asset['path']);copy_asset=root/'isolated-assets'/item/source.name
                    copy_asset.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,copy_asset)
                    if sha(copy_asset)!=asset['sha256']:raise ValueError('command_dependency_changed')
                    native['items'][item]['kind']['path']=str(copy_asset)
                if project['dependencies']:load('task_store').atomic_json(target,native)
                isolated_hash=sha(target)
                remaining=deadline-time.monotonic()
                if remaining<=0:raise TimeoutError('command_engineering_timeout')
                with session_factory([executable,'--empty','mcp'],timeout=remaining) as session:
                    call(session,'open_project',{'path':str(target)},deadline)
                    footage=call(session,'execute_command',{'command':'footage.check','params':{'wait':True}},deadline)
                    if (type(footage.get('missing')) is not int or footage['missing']!=0
                            or type(footage.get('checked')) is not int or footage['checked']<len(project['dependencies'])):
                        raise ValueError('native_footage_missing')
                    actual,_=snapshot(session,deadline)
                    if actual!=project['snapshot']:raise ValueError('command_native_snapshot_mismatch')
                if sha(target)!=isolated_hash:raise ValueError('command_snapshot_changed')
                if sha(output/project['path'])!=project['sha256']:raise ValueError('command_artifact_changed')
                for item,asset in project['dependencies'].items():
                    if sha(root/'isolated-assets'/item/Path(asset['path']).name)!=asset['sha256']:
                        raise ValueError('command_snapshot_changed')
                for asset in project['dependencies'].values():
                    if sha(output/asset['path'])!=asset['sha256']:raise ValueError('command_dependency_changed')
            report['projects'].append({'path':project['path'],'sha256':project['sha256'],'compositions':len(actual['compositions']),
                                       'verifiedAssets':len(project['dependencies'])})
        report.update(status='PASS',fresh=True)
    except (TimeoutError,subprocess.TimeoutExpired) as error:report.update(reason=str(error))
    except (ValueError,OSError,KeyError,TypeError,RuntimeError,subprocess.SubprocessError) as error:report.update(status='FAIL',reason=str(error))
    return report


def inspect(store,task,runtime_home,proof=None):
    """复用真实PNG解码器；缺覆盖、缺运行时与未知创作保持独立NOT_RUN。"""
    report={'schema':'effectcraft-quality/v1','engineering':{'status':'NOT_RUN'},'technical':{'status':'NOT_RUN','media':[]},
            'creative':{'status':'NOT_RUN'},'userAcceptance':{'status':'NOT_RUN','source':'explicit user decision required'},
            'readyForAcceptance':False,'accepted':False}
    state=store.read(task);output=Path(state['output'])
    try:
        proof=proof if proof is not None else state.get('delivery') or {}
        data=document(store,task,proof)
        if 'artifactMap' in data:report['commandArtifacts']=data['artifactMap']
        resources=data.get('artifactMap',{}).get('nativeResources')
        if resources is not None:
            report['nativeResources']=resources;report['dependencyClosure']=load('native_resources').closure(resources)
        report['binding']={'commandDeliverySha256':proof['commandDeliverySha256'],
                           'receiptSha256':data['receiptSha256'],'filesHash':load('task_store').digest(data['files'])}
        known={p['path'] for p in data['projects']}
        if resources is not None:
            known.update(r['path'] for i in resources for r in i['luts'] if r.get('packaged') and r.get('path'))
        for project in data['projects']:known.update(asset['path'] for asset in project['dependencies'].values())
        unmatched=[]
        for frame in data['frames']:
            path=load('quality_review').contained(output,frame['path']);comp=frame['composition']
            facts=load('image_sequence').rgba_facts(path) if frame['requestedAlpha'] else load('png_inspection').inspect_png(path)
            max_side=frame['maxSide'];ratio=min(1,max_side/max(comp['width'],comp['height'])) if max_side else 1
            dimensions=(max(1,round(comp['width']*ratio)),max(1,round(comp['height']*ratio)))
            if (facts['width'],facts['height'])!=dimensions:raise ValueError('preview_dimensions_mismatch')
            sources=[project['path'] for project in data['projects'] if project['snapshot']==frame['snapshot'] and project['nativeVersion']==frame['nativeVersion'] and project['dependencies']==frame['dependencies']]
            if not sources:unmatched.append(frame['path'])
            report['technical']['media'].append({'path':frame['path'],'facts':facts,'composition':comp,'sourceProjects':sources,
                'seconds':frame['seconds'],'sourceSnapshotHash':load('task_store').digest(frame['snapshot'])})
            known.add(frame['path'])
            for item in frame.get('inlineCopies',[]):
                if item['sha256']!=frame['sha256'] or data['files'].get(item['path'])!=item['sha256']:
                    raise ValueError('command_inline_copy_mismatch')
                known.add(item['path'])
        unreviewed=sorted(set(data['files'])-known)
        report['technical'].update(status='PASS' if data['frames'] and not unreviewed and not unmatched else 'NOT_RUN',unreviewed=unreviewed,unmatchedFrames=unmatched,
            verifiedAssets=sum(len(project['dependencies']) for project in data['projects']))
        if unmatched:report['technical']['reason']='frame_source_project_unavailable'
        elif unreviewed:report['technical']['reason']='command_outputs_not_reviewed'
        elif not data['frames']:report['technical']['reason']='no_supported_media_to_review'
    except (ValueError,OSError,KeyError,TypeError,subprocess.SubprocessError) as error:
        report['technical'].update(status='FAIL',reason=str(error));return report
    try:
        if runtime_home is None:raise ValueError('engineering_runtime_location_missing')
        lock=read(Path(__file__).with_name('runtime.lock.json'));expected=lock['artifacts'][load('platform_support').platform_key()]
        if expected['binarySha256']!=state['identity']['runtimeSha256']:raise ValueError('engineering_task_runtime_mismatch')
        installed=load('bootstrap').inspect_install(Path(runtime_home)/'effectcraft'/lock['resolvedVersion'],lock['artifact'],expected,lock['resolvedVersion'],load('platform_support').platform_key())
    except (ValueError,OSError,KeyError,TypeError) as error:
        report['engineering']['reason']=str(error);return report
    report['engineering']=verify_projects(output,data['projects'],installed['executable'],timeout=max(.1,min(120,state['deadline']-time.time())))
    if resources is not None and report['engineering']['status']=='PASS':
        adapter=load('resource_validation')
        try:
            report['resourceValidation']=adapter.commands(output,data,installed['executable'],timeout=max(.1,min(120,state['deadline']-time.time())),before_render=adapter.budget_hook(store,task))
        except (ValueError,OSError,KeyError,TypeError,RuntimeError,subprocess.SubprocessError) as error:
            report['resourceValidation']={'schema':'effectcraft-file-lut-review/v1','status':'FAIL','reason':str(error)}
        if report['resourceValidation']['status']=='FAIL':report['engineering'].update(status='FAIL',fresh=False,reason='file_lut_validation_failed')
        elif report['resourceValidation']['status']=='NOT_RUN' and report['resourceValidation'].get('projects'):report['engineering'].update(status='NOT_RUN',fresh=False,reason='file_lut_validation_incomplete')
    try:document(store,task,proof)
    except (ValueError,OSError,KeyError,TypeError) as error:
        report['technical'].update(status='FAIL',reason=str(error));report['engineering'].update(status='FAIL',fresh=False,reason=str(error))
    return report


def review(store,task,criteria,judge=None,runtime_home=None):
    return load('review_ledger').review(store,task,criteria,judge,runtime_home)
