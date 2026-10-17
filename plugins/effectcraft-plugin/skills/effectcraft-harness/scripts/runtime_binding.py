"""任务私有执行快照与解释器绑定；升级不改旧任务，损坏材料不自动重建。"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path,PurePosixPath
import re
import shutil
import subprocess
import sys
import uuid


def load(name):
    spec=importlib.util.spec_from_file_location('execution_'+name,Path(__file__).with_name(name+'.py'))
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result


def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()


def file_sha(path):
    path=Path(path)
    if path.is_symlink() or not path.is_file():raise ValueError('bound_file_invalid')
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def read(path):return load('commands').reply_json(Path(path).read_text(encoding='utf-8'))


def relative(name):
    if not isinstance(name,str):raise ValueError('execution_manifest_invalid')
    p=PurePosixPath(name)
    if not isinstance(name,str) or not p.parts or p.is_absolute() or '..' in p.parts or '\\' in name or ':' in name:
        raise ValueError('execution_manifest_invalid')
    return p


def source_files(skill):
    """只收集执行资源，不复制用户素材、环境变量、宿主元数据或任意凭据文件。"""
    skill=Path(skill)
    if skill.is_symlink():raise ValueError('execution_source_symlink')
    paths=list((skill/'scripts').glob('*.py'))
    paths += [skill/'scripts'/n for n in ('runtime.lock.json','python.lock.json','desktop.lock.json','desktop-platforms.lock.json','parameter-contract.json','python-platforms.tsv','launch.sh','launch.ps1','task_entry.sh','task_entry.ps1','entry_identity.awk','web_adapter.mjs')]
    paths += [skill/'references'/n for n in ('command-coverage.json','native-command-snapshot.json','bridge-tools.json','commands.json')]
    for folder in ('runtime-integrity','python-integrity'):
        directory=skill/'scripts'/folder
        if directory.is_symlink():raise ValueError('execution_source_symlink')
        paths+=list(directory.rglob('*'))
    result={};total=0
    for path in sorted(paths):
        if any(parent.is_symlink() for parent in path.parents if parent==skill or skill in parent.parents):
            raise ValueError('execution_source_symlink')
        if path.is_symlink():raise ValueError('execution_source_symlink')
        if path.is_dir():continue
        if not path.is_file():raise ValueError('execution_source_missing: '+path.name)
        total+=path.stat().st_size
        if total>64*1024*1024:raise ValueError('execution_source_too_large')
        result[path.relative_to(skill).as_posix()]=file_sha(path)
    return result


def python_identity(skill,platform):
    executable=Path(sys.executable).resolve()
    value={'mode':'external','executable':str(executable),'sha256':file_sha(executable),'version':sys.version.split()[0],'root':None,'platform':platform}
    lock=read(Path(skill)/'scripts/python.lock.json');entry=lock['artifacts'].get(platform)
    if entry and value['version']==lock['version']:
        for root in executable.parents:
            if (root/entry['executable']).resolve()==executable and (root/'installation.json').is_file():
                value.update(mode='locked',root=str(root));verify_python(value,skill);break
    return value


def verify_python(value,skill):
    """锁定Python检查整个发行载荷；外部兼容解释器只绑定自身文件，不声称已隔离。"""
    if file_sha(value['executable'])!=value['sha256']:raise ValueError('bound_python_changed')
    if value['mode']=='external':return
    lock=read(Path(skill)/'scripts/python.lock.json');entry=lock['artifacts'][value['platform']];root=Path(value['root'])
    if root.is_symlink() or (root/entry['executable']).resolve()!=Path(value['executable']):raise ValueError('bound_python_changed')
    receipt=read(root/'installation.json')
    if any(receipt.get(k)!=v for k,v in {'version':value['version'],'platform':value['platform'],'archiveSha256':entry['archiveSha256']}.items()):
        raise ValueError('bound_python_changed')
    manifest=Path(skill)/'scripts'/entry['integrityFile']
    if file_sha(manifest)!=entry['integritySha256']:raise ValueError('bound_python_manifest_changed')
    expected={}
    for line in manifest.read_text(encoding='utf-8').splitlines():
        kind,sha,name=line.split('\t');relative(name)
        if name in expected or kind not in ('f','l') or not re.fullmatch('[a-f0-9]{64}',sha):raise ValueError('bound_python_manifest_invalid')
        expected[name]=(kind,sha)
    actual={p.relative_to(root).as_posix():p for p in root.rglob('*') if (p.is_file() or p.is_symlink()) and p!=root/'installation.json'}
    if set(actual)!=set(expected):raise ValueError('bound_python_inventory_changed')
    for name,(kind,sha) in expected.items():
        path=actual[name]
        if kind=='l':
            if not path.is_symlink() or hashlib.sha256(os.readlink(path).encode()).hexdigest()!=sha:raise ValueError('bound_python_changed')
        elif file_sha(path)!=sha:raise ValueError('bound_python_changed')


def validate_binding(value):
    if (not isinstance(value,dict) or set(value)!=({'schema','skillSha256','python','runtimeHome','nativeVersion','platform','entrySha256'} if value.get('schema')=='effectcraft-execution-binding/v2' else {'schema','skillSha256','python','runtimeHome','nativeVersion','platform'})
            or value['schema'] not in ('effectcraft-execution-binding/v1','effectcraft-execution-binding/v2') or not isinstance(value['skillSha256'],str) or not re.fullmatch('[a-f0-9]{64}',value['skillSha256'])
            or not isinstance(value['runtimeHome'],str) or not Path(value['runtimeHome']).is_absolute()
            or not isinstance(value['nativeVersion'],str) or not re.fullmatch(r'\d+\.\d+\.\d+',value['nativeVersion'])
            or not isinstance(value['platform'],str) or not re.fullmatch('[a-z0-9_-]+',value['platform'])):
        raise ValueError('execution_binding_invalid')
    if value['schema']=='effectcraft-execution-binding/v2' and (not isinstance(value['entrySha256'],str) or not re.fullmatch('[a-f0-9]{64}',value['entrySha256'])):raise ValueError('execution_binding_invalid')
    py=value['python']
    if (not isinstance(py,dict) or set(py)!={'mode','executable','sha256','version','root','platform'} or py['mode'] not in ('locked','external')
            or not isinstance(py['executable'],str) or not Path(py['executable']).is_absolute()
            or not isinstance(py['sha256'],str) or not re.fullmatch('[a-f0-9]{64}',py['sha256'])
            or not isinstance(py['version'],str) or not re.fullmatch(r'\d+\.\d+\.\d+',py['version'])
            or py['platform']!=value['platform'] or (py['mode']=='locked' and (not isinstance(py['root'],str) or not Path(py['root']).is_absolute()))
            or py['mode']=='external' and py['root'] is not None):raise ValueError('execution_binding_invalid')


def entry_bytes(binding,skill):
    """固定字段描述仅用于安装前选择；不保存命令、凭据或可执行Shell表达式。"""
    py=binding['python'];lock=read(Path(skill)/'scripts/python.lock.json');entry=lock['artifacts'].get(py['platform'],{})
    minimum=entry.get('minimumSystem',{})
    system_min=minimum.get('macOS',minimum.get('glibc',minimum.get('windows','0.0')))
    rows=[('schema','effectcraft-task-entry/v1'),('mode',py['mode']),('executable',py['executable']),('executableSha256',py['sha256']),
          ('root',py['root'] or '-'),('platform',py['platform']),('version',py['version']),
          ('manifest',entry.get('integrityFile','-') if py['mode']=='locked' else '-'),
          ('manifestSha256',entry.get('integritySha256','-') if py['mode']=='locked' else '-'),
          ('archiveSha256',entry.get('archiveSha256','-') if py['mode']=='locked' else '-'),('minimumSystem',system_min)]
    if any(not isinstance(value,str) or any(c in value for c in ('\t','\r','\n','\0')) for key,value in rows):
        raise ValueError('bound_entry_path_unrepresentable')
    return ''.join(key+'\t'+value+'\n' for key,value in rows).encode('utf-8')


def verify_entry(store,task,skill):
    """重读权威状态，启动描述与原绑定相符才允许派发原控制器。"""
    state=store.read(task);binding=state['identity'].get('runtimeBinding')
    if not binding or binding['schema']!='effectcraft-execution-binding/v2':raise ValueError('bound_entry_missing; legacy task requires original diagnostics')
    directory=store.path(task).parent/'execution'
    if file_sha(directory/'entry.tsv')!=binding['entrySha256'] or (directory/'entry.tsv').read_bytes()!=entry_bytes(binding,skill):
        raise ValueError('bound_entry_changed')
    identity=directory/'identity.json'
    if file_sha(identity)!=hashlib.sha256(load('task_store').canonical(state['identity'])+b'\n').hexdigest():raise ValueError('bound_entry_identity_changed')
    return binding


def prepare(skill,runtime_home):
    skill=Path(skill)
    if skill.is_symlink():raise ValueError('execution_source_symlink')
    skill=skill.resolve();platform=load('platform_support').platform_key();manifest=source_files(skill)
    lock=read(skill/'scripts/runtime.lock.json')
    value={'schema':'effectcraft-execution-binding/v1','skillSha256':digest(manifest),
           'python':python_identity(skill,platform),'runtimeHome':str(Path(runtime_home).expanduser().absolute()),
           'nativeVersion':lock['resolvedVersion'],'platform':platform}
    value['schema']='effectcraft-execution-binding/v2';value['entrySha256']=hashlib.sha256(entry_bytes(value,skill)).hexdigest()
    validate_binding(value);return value,manifest


def freeze(store,task,source,manifest):
    state=store.read(task);binding=state['identity'].get('runtimeBinding')
    if binding is None:raise ValueError('legacy_execution_binding_missing')
    validate_binding(binding)
    if digest(manifest)!=binding['skillSha256']:raise ValueError('execution_manifest_changed')
    for name in manifest:relative(name)
    if source_files(source)!=manifest:raise ValueError('execution_source_changed')
    directory=store.path(task).parent;destination=directory/'execution'
    if destination.exists() or destination.is_symlink():raise ValueError('execution_snapshot_exists')
    stage=directory/('.execution-'+uuid.uuid4().hex);stage.mkdir(mode=0o700)
    # 失败暂存区保留供核对；不覆盖任何已存在的执行快照或任务。
    for name in manifest:
        target=stage/'skill'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Path(source)/name,target)
    if source_files(source)!=manifest or inventory(stage/'skill')!=manifest:raise ValueError('execution_source_changed')
    load('task_store').atomic_json(stage/'manifest.json',manifest)
    if binding['schema']=='effectcraft-execution-binding/v2':
        payload=entry_bytes(binding,stage/'skill')
        if hashlib.sha256(payload).hexdigest()!=binding['entrySha256']:raise ValueError('bound_entry_changed')
        (stage/'entry.tsv').write_bytes(payload);load('task_store').atomic_json(stage/'identity.json',state['identity'])
    stage.rename(destination)


def inventory(skill):
    result={}
    for path in Path(skill).rglob('*'):
        if path.is_symlink():raise ValueError('execution_snapshot_symlink')
        if path.is_file():result[path.relative_to(skill).as_posix()]=file_sha(path)
    return result


def resolve(store,task):
    state=store.read(task);binding=state['identity'].get('runtimeBinding')
    if binding is None:raise ValueError('legacy_execution_binding_missing; inspect original task')
    validate_binding(binding);directory=store.path(task).parent/'execution';skill=directory/'skill'
    try:
        if directory.is_symlink() or skill.is_symlink():raise ValueError('execution_snapshot_symlink')
        if (directory/'manifest.json').is_symlink():raise ValueError('execution_snapshot_symlink')
        manifest=read(directory/'manifest.json')
        if not isinstance(manifest,dict) or digest(manifest)!=binding['skillSha256']:raise ValueError('execution_snapshot_manifest_changed')
        for name in manifest:relative(name)
        if inventory(skill)!=manifest:raise ValueError('execution_snapshot_changed')
    except (OSError,ValueError,TypeError):raise ValueError('execution_snapshot_invalid; preserve original task') from None
    if binding['schema']=='effectcraft-execution-binding/v2':verify_entry(store,task,skill)
    verify_python(binding['python'],skill)
    lock=read(skill/'scripts/runtime.lock.json')
    if lock['resolvedVersion']!=binding['nativeVersion'] or lock['artifacts'][binding['platform']]['binarySha256']!=state['identity']['runtimeSha256']:
        raise ValueError('execution_native_binding_changed')
    return {'python':binding['python']['executable'],'script':str(skill/'scripts/managed.py'),
            'guard':str(skill/'scripts/process_guard.py'),'runtimeHome':binding['runtimeHome']}


def references(store):
    """只读列出保留引用；单个状态根不能授权删除其他状态根或原始CLI正在使用的版本。"""
    native=set();python=set();legacy=[]
    for state in store.all():
        binding=state['identity'].get('runtimeBinding')
        if binding is None:legacy.append(state['taskId']);continue
        validate_binding(binding);native.add(str(Path(binding['runtimeHome'])/'effectcraft'/binding['nativeVersion']))
        python.add(binding['python']['executable'])
    return {'nativeVersions':sorted(native),'pythonExecutables':sorted(python),'legacyTasks':legacy,
            'destructiveCleanupAllowed':False,'scope':'readonly references of this state root only; retain snapshots and all referenced versions'}


def handoff(store,args,current_script):
    """使用exec替换控制器，避免新前端死亡后留下脱离监督的旧控制器。"""
    state=store.read(args.task)
    if 'runtimeBinding' not in state['identity']:
        if args.action!='inspect':raise ValueError('legacy_execution_binding_missing; inspect original task')
        return
    bound=resolve(store,args.task)
    args.runtime_home=Path(bound['runtimeHome'])
    if Path(current_script).resolve()==Path(bound['script']).resolve() and Path(sys.executable).resolve()==Path(bound['python']).resolve():return
    suffix=[args.action,'--task',args.task]
    for key in ('plan','output','source','criteria','judge'):
        item=getattr(args,key,None)
        if item is not None:suffix+=['--'+key,str(item)]
    if args.action=='revise':
        suffix+=['--mode',args.mode]
        for item in args.input:suffix+=['--input',item]
    argv=[bound['python'],'-I','-B',bound['script'],'--state-root',str(store.root),'--runtime-home',bound['runtimeHome'],*suffix]
    if os.name=='nt':return windows_handoff(store,args.task,bound,argv)
    os.execv(bound['python'],argv)


def windows_handoff(store,task,bound,argv):
    """Windows无原位exec；沿用带门控Job的守护器和stdin所有权通道监督旧控制器。"""
    receipt=store.path(task).parent/('controller-'+uuid.uuid4().hex+'.json')
    command=[bound['python'],'-I','-B',bound['guard'],'--receipt',str(receipt),
             '--lease',str(store.root/'leases'/(task+'.controller.lock')),'--',*argv]
    child=subprocess.Popen(command,stdin=subprocess.PIPE)
    try:
        code=child.wait()
    except BaseException:
        child.stdin.close();child.wait(timeout=30);raise
    finally:
        if not child.stdin.closed:child.stdin.close()
    record=read(receipt);exit_code=record.get('returncode')
    if (record.get('schema')!='effectcraft-process-lifecycle/v1' or record.get('status')!='stopped'
            or type(exit_code) is not int or (exit_code if exit_code>=0 else 1)!=code):
        raise ValueError('bound_controller_termination_unconfirmed')
    raise SystemExit(code if code>=0 else 1)
