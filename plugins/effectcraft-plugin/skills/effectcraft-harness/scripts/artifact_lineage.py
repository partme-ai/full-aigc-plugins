"""消费 ArtCraft 持有的 craft-artifact/v1；绑定工作流包身份，不另建公共协议。"""
import importlib.util
from fractions import Fraction
from pathlib import Path, PurePosixPath
import re

# 协议事实源：artcraft-plugin v0.1.0-dev.109 / 09d4ac5b8ff82f8fe819189e4be487b45ab2472b。
# schemas/craft-artifact-v1.json SHA256 c3385db540db71fccfdb049f79f05a9adba55ec008958579eab6fac46dd6ea5d。
HERE=Path(__file__).resolve().parent
HEX=re.compile(r'^[a-f0-9]{64}$')


def load(name):
    spec=importlib.util.spec_from_file_location('artifact_lineage_'+name,HERE/(name+'.py'))
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value


def read(path):return load('commands').reply_json(Path(path).read_text(encoding='utf-8'))
def digest(value):return load('task_store').digest(value)
def sha(path):return load('task_store').file_sha(path)


def fail(reason):raise ValueError('artifact_lineage: '+reason)


def file(root,name):
    if (not isinstance(name,str) or not name or '\\' in name or ':' in name or name.startswith('/')
            or any(part in ('','.','..') for part in name.split('/'))):fail('unsafe_location')
    path=root/PurePosixPath(name)
    if any(p.is_symlink() for p in (path,*path.parents) if p==root or root in p.parents):fail('symlink')
    if not path.resolve().is_relative_to(root.resolve()) or not path.is_file():fail('missing_or_escaping_file')
    return path


def inventory(root):
    result={}
    for path in sorted(root.rglob('*')):
        if path.is_symlink():fail('symlink')
        if path.is_file() and path!=root/'manifest.json':result[path.relative_to(root).as_posix()]=sha(path)
    return result


def reference(value):
    if (not isinstance(value,dict) or set(value)!=set(('assetId','version','sha256'))
            or any(not isinstance(value[k],str) or not 1<=len(value[k])<=256 for k in ('assetId','version'))
            or not isinstance(value['sha256'],str) or not HEX.fullmatch(value['sha256'])):fail('source_reference_invalid')
    return value


def validate_source(root):
    """在安装／原生副作用前校验源包；旧包可读但不补造任务来源。"""
    root=Path(root);manifest=read(file(root,'manifest.json'))
    if 'artifact' in manifest or 'artifactBinding' in manifest:verify(root,manifest)
    else:
        files=manifest.get('files')
        if not isinstance(files,dict) or 'project.ecproj' not in files:fail('legacy_file_table_invalid')
        for name,expected in files.items():
            if sha(file(root,name))!=expected:fail('legacy_file_changed')
        for asset in manifest.get('assets',{}).values():
            if files.get(asset['path'])!=asset['sha256']:fail('legacy_dependency_mismatch')
    return manifest


def source_ref(root):
    manifest=validate_source(root)
    if 'artifact' in manifest:return reference({k:manifest['artifact'][k] for k in ('assetId','version','sha256')})
    content=manifest['files']['project.ecproj']
    return {'assetId':'legacy-project:'+content,'version':content,'sha256':content}


def source_binding(root):
    """绑定整包版本，任务登记后不能仅靠未变化的原生工程摘要放行。"""
    root=Path(root);parent=source_ref(root)
    return {'schema':'effectcraft-source-package/v1','manifestSha256':sha(file(root,'manifest.json')),'sourceRef':parent}


def standalone(context):
    identity=digest(context['executionIdentity'])
    return {'producerTaskId':'standalone:'+identity,'taskIdentityHash':identity,'mode':'standalone'}


def binding(context):
    return {'schema':'effectcraft-artifact-binding/v1','producer':context.get('artifactProducer') or standalone(context),
            'planSha256':digest(context['plan']),'runtimeSha256':context['runtimeSha256'],
            'sourceRef':context.get('sourceArtifact')}


def record(root,manifest,bound):
    """只依据实际包文件与显式生产身份构造公共对象；不推断技术／创作通过。"""
    if not isinstance(bound,dict) or set(bound)!=set(('schema','producer','planSha256','runtimeSha256','sourceRef')) or bound['schema']!='effectcraft-artifact-binding/v1':fail('binding_schema')
    producer=bound['producer']
    if (not isinstance(producer,dict) or set(producer)!=set(('producerTaskId','taskIdentityHash','mode'))
            or not isinstance(producer['producerTaskId'],str) or not 1<=len(producer['producerTaskId'])<=256
            or producer['mode'] not in ('managed','standalone')
            or not isinstance(producer['taskIdentityHash'],str) or not HEX.fullmatch(producer['taskIdentityHash'])):fail('producer_invalid')
    if producer['mode']=='standalone' and producer['producerTaskId']!='standalone:'+producer['taskIdentityHash']:fail('standalone_identity_invalid')
    for key in ('planSha256','runtimeSha256'):
        if not isinstance(bound[key],str) or not HEX.fullmatch(bound[key]):fail('binding_digest')
    if bound['runtimeSha256']!=manifest['runtimeSha256'] or bound['planSha256']!=digest(read(file(root,'plan.json'))):fail('execution_binding_changed')
    files=manifest.get('files')
    if not isinstance(files,dict) or not files or files!=inventory(root):fail('package_file_table_changed')
    for name in files:file(root,name)
    native=read(file(root,'project.ecproj'))
    if not isinstance(native,dict) or native.get('schema')!=1 or not isinstance(native.get('items'),dict):fail('native_format_invalid')
    parent=reference(bound['sourceRef']) if bound['sourceRef'] is not None else None
    if (parent['sha256'] if parent else None)!=manifest.get('sourceProjectSha256'):fail('source_project_changed')
    asset_id=parent['assetId'] if parent else 'effectcraft:'+digest(producer)
    version_payload={'binding':bound,'files':files,'sourceProjectSha256':manifest.get('sourceProjectSha256')}
    resources=manifest.get('nativeResources')
    if 'nativeResources' in manifest:
        if resources!=load('native_resources').inspect(root,'project.ecproj',declared=resources):fail('native_resources_changed')
        version_payload['nativeResources']=resources
    version=digest(version_payload)
    native_sha=files['project.ecproj']
    def ref(name,logical=None):
        if name not in files:fail('unlisted_reference')
        return {'assetId':logical or 'effectcraft-rendition:'+digest({'assetId':asset_id,'location':name}),
                'version':files[name],'sha256':files[name],'location':name}
    assets=manifest.get('assets',{})
    if not isinstance(assets,dict):fail('dependencies_invalid')
    dependencies=[];asset_paths=set()
    for alias,asset in sorted(assets.items()):
        if not isinstance(asset,dict) or files.get(asset.get('path'))!=asset.get('sha256'):fail('dependency_changed')
        name=asset['path'];file(root,name);asset_paths.add(name)
        dependencies.append({'assetRef':{k:v for k,v in ref(name,'effectcraft-media:'+digest({'assetId':asset_id,'alias':alias})).items() if k!='location'},
            'kind':'media','packaged':True,'missingReason':None})
    if resources is not None:dependencies.extend(load('native_resources').public_dependencies(resources))
    names={frame['path'] for frame in manifest.get('frames',[])}
    if manifest.get('video'):names.add(manifest['video']['path'])
    if manifest.get('imageSequence'):
        descriptor=manifest['imageSequence']['path'];names.add(descriptor)
        directory=PurePosixPath(descriptor).parent
        names.update(name for name in files if PurePosixPath(name).is_relative_to(directory) and name.endswith('.png'))
    if names & asset_paths:fail('rendition_is_dependency')
    composition=read(file(root,'native.json'))['composition']
    width=composition['width'];height=composition['height'];rate=Fraction(str(composition['frameRate']));duration=Fraction(str(composition['duration']))
    if type(width) is not int or type(height) is not int or min(width,height)<=0 or rate<=0 or duration<=0:fail('composition_invalid')
    if max(width,height,rate.numerator,rate.denominator,duration.denominator)>9007199254740991:fail('unsafe_time_or_dimension_integer')
    loss=manifest['lossReport']
    if files.get(loss['path'])!=loss['sha256']:fail('loss_report_changed')
    return {'protocolVersion':'craft-artifact/v1','assetId':asset_id,'version':version,'sha256':native_sha,
            'bytes':file(root,'project.ecproj').stat().st_size,'mediaType':'application/vnd.effectcraft.project+json',
            'producerTaskId':producer['producerTaskId'],'sourceRefs':[parent] if parent else [],
            'nativeProjectRef':{'assetId':asset_id,'version':version,'sha256':native_sha,'location':'project.ecproj'},
            'renditions':[ref(name) for name in sorted(names)],'dependencies':dependencies,
            'technicalMetadata':{'width':width,'height':height,'frameRate':{'num':rate.numerator,'den':rate.denominator},
                'durationTicks':str(duration.numerator),'timeBase':{'num':1,'den':duration.denominator},'colorSpace':'unknown'},
            'lossReportRef':ref(loss['path']),'evidenceRefs':[ref('native.json'),ref('operations.json')],'location':'project.ecproj'}


def attach(root,manifest,context):
    """生成新包记录；生产身份随导出上下文持久化，恢复不创建新任务。"""
    try:
        manifest['nativeResources']=load('native_resources').inspect(Path(root),'project.ecproj')
        bound=binding(context);manifest['artifactBinding']=bound;manifest['artifact']=record(Path(root),manifest,bound)
    except (KeyError,TypeError,OSError,ValueError) as error:
        if isinstance(error,ValueError) and str(error).startswith('artifact_lineage:'):raise
        fail('invalid_package: '+type(error).__name__)
    return manifest


def verify(root,manifest):
    """重算完整内容与引用；缺失任何一半绑定都不能降级为旧包。"""
    try:
        if manifest.get('artifact')!=record(Path(root),manifest,manifest['artifactBinding']):fail('record_changed')
    except (KeyError,TypeError,OSError,ValueError) as error:
        if isinstance(error,ValueError) and str(error).startswith('artifact_lineage:'):raise
        fail('invalid_package: '+type(error).__name__)


def producer_root():
    """私有定位记录跨state-root稳定；公共产物不包含本机账本路径。"""
    return Path.home()/'.local/share/craft-tasks/effectcraft-artifact-producers'


def producer_owner(store,state):
    return {'stateRoot':str(store.root),'taskId':state['taskId'],'identityHash':state['identityHash']}


def producer_locator(identity,task):
    if not isinstance(identity,str) or not HEX.fullmatch(identity):raise ValueError('source_producer_identity_invalid')
    if not isinstance(task,str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,95}',task):raise ValueError('source_producer_task_invalid')
    return producer_root()/(digest({'taskId':task,'identityHash':identity})+'.json')


def read_producer_locator(identity,task):
    path=producer_locator(identity,task)
    try:
        if producer_root().is_symlink() or path.is_symlink() or not path.is_file() or path.stat().st_size>1024*1024:raise ValueError('shape')
        value=read(path);owner=value['owner']
        if (set(value)!={'schema','owner'} or value['schema']!='effectcraft-artifact-producer/v1'
                or set(owner)!={'stateRoot','taskId','identityHash'} or owner['identityHash']!=identity or owner['taskId']!=task
                or not isinstance(owner['stateRoot'],str) or not Path(owner['stateRoot']).is_absolute()
                or not isinstance(owner['taskId'],str)):raise ValueError('shape')
        return value
    except (OSError,ValueError,TypeError,KeyError):raise ValueError('source_producer_locator_invalid') from None


def register_producer(store,task):
    """先持久定位再发布包；原任务仍须单独证明交付及进程停止。"""
    if producer_root().is_symlink():raise ValueError('source_producer_locator_invalid')
    with load('platform_support').exclusive_lock(producer_root()/'producers.lock'):
        with store.lock():
            state=store.read(task);owner=producer_owner(store,state);path=producer_locator(state['identityHash'],task)
            expected={'schema':'effectcraft-artifact-producer/v1','owner':owner}
            if path.exists() or path.is_symlink():
                if read_producer_locator(state['identityHash'],task)!=expected:raise ValueError('source_producer_locator_conflict')
            else:
                if 'artifactProducerLocator' in state:raise ValueError('source_producer_locator_missing')
                load('task_store').atomic_json(path,expected)
            reference={'schema':'effectcraft-producer-locator/v1','sha256':sha(path)}
            if state.get('artifactProducerLocator',reference)!=reference:raise ValueError('source_producer_locator_conflict')
            if 'artifactProducerLocator' not in state:
                state['artifactProducerLocator']=reference;store.save(state)
            return {'producerTaskId':task,'taskIdentityHash':state['identityHash'],'mode':'managed'}


def verify_producer(bound):
    """逐操作核对来源，不按PID、完整包或定位记录推断编辑完成。"""
    try:
        if (not isinstance(bound,dict) or set(bound)!={'schema','owner','manifestSha256','projectSha256','locatorSha256'}
                or bound['schema']!='effectcraft-source-producer/v1'):raise ValueError('binding')
        owner=bound['owner']
        if (not isinstance(owner,dict) or set(owner)!={'stateRoot','taskId','identityHash'}
                or not isinstance(owner['stateRoot'],str) or not Path(owner['stateRoot']).is_absolute()
                or not isinstance(owner['identityHash'],str) or not HEX.fullmatch(owner['identityHash'])
                or any(not isinstance(bound[k],str) or not HEX.fullmatch(bound[k]) for k in ('manifestSha256','projectSha256'))):raise ValueError('binding')
        tasks=load('task_store');original=tasks.Store(owner['stateRoot']);state=original.read(owner['taskId'])
        if state['schema']!='effectcraft-managed-task/v2' or state['identityHash']!=owner['identityHash']:raise ValueError('identity')
        if bound['locatorSha256'] is not None:
            if (read_producer_locator(owner['identityHash'],owner['taskId'])!={'schema':'effectcraft-artifact-producer/v1','owner':owner}
                    or sha(producer_locator(owner['identityHash'],owner['taskId']))!=bound['locatorSha256']
                    or state.get('artifactProducerLocator')!={'schema':'effectcraft-producer-locator/v1','sha256':bound['locatorSha256']}):raise ValueError('locator')
        elif 'artifactProducerLocator' in state:raise ValueError('locator_missing')
        delivery=state.get('delivery')
        if (state['state'] not in ('review_ready','completed') or state.get('cancellationRequestedAt')
                or any(step['state']!='succeeded' for step in state['steps'])
                or not isinstance(delivery,dict) or delivery.get('manifestSha256')!=bound['manifestSha256']
                or delivery.get('projectSha256')!=bound['projectSha256'] or delivery.get('engineeringReopen')!='PASS'):
            raise ValueError('delivery_unconfirmed')
        stopped=read(original.lifecycle_path(state))
        if stopped.get('schema')!='effectcraft-process-lifecycle/v1' or stopped.get('status')!='stopped':raise ValueError('stop_unconfirmed')
        tasks.exit_evidence(stopped.get('returncode'),stopped.get('ownership'))
    except (OSError,ValueError,TypeError,KeyError):raise ValueError('source_producer_unconfirmed; reconcile original task') from None


def producer_binding(store,root):
    """保留受管理身份的源包必须绑定可核对的原任务；旧包只读规则独立。"""
    manifest=validate_source(root);producer=manifest.get('artifactBinding',{}).get('producer')
    if not producer or producer['mode']=='standalone':return None
    identity=producer['taskIdentityHash'];task=producer['producerTaskId'];path=producer_locator(identity,task);locator=None
    if path.exists() or path.is_symlink():
        owner=read_producer_locator(identity,task)['owner'];locator=sha(path)
    else:
        # 旧发行仅可在调用者已有原账本时核对；不扫描用户目录或写入补造定位记录。
        owner={'stateRoot':str(store.root),'taskId':producer['producerTaskId'],'identityHash':identity}
    if owner['taskId']!=producer['producerTaskId']:raise ValueError('source_producer_identity_mismatch')
    bound={'schema':'effectcraft-source-producer/v1','owner':owner,'manifestSha256':sha(file(Path(root),'manifest.json')),
           'projectSha256':manifest['files']['project.ecproj'],'locatorSha256':locator}
    verify_producer(bound);return bound
