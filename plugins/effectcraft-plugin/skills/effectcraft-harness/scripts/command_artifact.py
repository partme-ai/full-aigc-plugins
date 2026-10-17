"""命令／桌面消费craft-artifact/v1；公共对象与私有可移植映射分开。"""
import copy
from fractions import Fraction
import importlib.util
from pathlib import Path
import re


def load(name):
    spec=importlib.util.spec_from_file_location('command_artifact_'+name,Path(__file__).with_name(name+'.py'))
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value


def digest(value):return load('task_store').digest(value)
def sha(path):return load('task_store').file_sha(path)
def fail(reason):raise ValueError('command_artifact: '+reason)


def metadata(project):
    """多合成工程保留完整私有上下文，不虚构任意单一尺寸／时间基准。"""
    values=list(project['snapshot']['compositions'].values());result={'colorSpace':'unknown'}
    if len(values)!=1:return result
    comp=values[0]['composition'];width=comp['width'];height=comp['height']
    rate=Fraction(str(comp['frameRate']));duration=Fraction(str(comp['duration']))
    if (type(width) is not int or type(height) is not int or min(width,height)<=0 or min(rate,duration)<=0
            or max(width,height,rate.numerator,rate.denominator,duration.denominator)>9007199254740991):fail('unsafe_time_or_dimension')
    result.update(width=width,height=height,frameRate={'num':rate.numerator,'den':rate.denominator},
                  durationTicks=str(duration.numerator),timeBase={'num':1,'den':duration.denominator})
    return result


def contexts(data):
    """只携带相对位置与原生观察；不把用户本机账本路径写入公共对象。"""
    fields=('path','sha256','snapshot','nativeVersion','dependencies')
    return {'projects':[{k:copy.deepcopy(p[k]) for k in fields} for p in data['projects']],
            'frames':[{k:copy.deepcopy(f[k]) for k in fields+('composition','seconds','requestedAlpha','maxSide','inlineCopies') if k in f} for f in data['frames']]}


def source_refs(store,state):
    if not state.get('parent'):return {}
    request=load('commands').reply_json((store.path(state['taskId']).parent/'request.json').read_text(encoding='utf-8'))
    if digest(request)!=state['identity']['authorization'].get('requestHash'):fail('request_changed')
    context=request.get('commandRevision')
    if not context:fail('revision_context_missing')
    source=store.read(context['sourceTask']);delivery=load('command_delivery');data=delivery.document(store,source['taskId'])
    expected={'commandDeliverySha256':source['delivery']['commandDeliverySha256'],'receiptSha256':data['receiptSha256'],'filesHash':digest(data['files'])}
    if state['parent']!=store.lineage(source)[-1]['taskId'] or context.get('sourceBinding')!=expected:fail('source_binding_changed')
    artifacts={a['location']:a for a in data.get('artifactMap',{}).get('artifacts',[])};result={}
    for project in data['projects']:
        artifact=artifacts.get(project['path'])
        result[project['path']]={k:artifact[k] for k in ('assetId','version','sha256')} if artifact else {
            'assetId':'legacy-command-project:'+project['sha256'],'version':project['sha256'],'sha256':project['sha256']}
    return result


def compile_map(output,files,bound,context,*,resources=False,declared=None):
    """绑定整包与原观察；登记身份不声明工程、媒体、字体或创作已验收。"""
    output=Path(output);lineage=load('artifact_lineage')
    if (not isinstance(bound,dict) or set(bound)!={'schema','producer','planHash','runtimeSha256','filesHash','receiptSha256','observationsHash','sourceRefs'}
            or bound['schema']!='effectcraft-command-artifact-binding/v1'):fail('binding_schema')
    producer=bound['producer']
    if (not isinstance(producer,dict) or set(producer)!={'taskId','identityHash'}
            or not isinstance(producer['taskId'],str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,95}',producer['taskId'])):fail('producer_invalid')
    for value in [producer['identityHash'],*(bound[k] for k in ('planHash','runtimeSha256','filesHash','receiptSha256','observationsHash'))]:
        if not isinstance(value,str) or not lineage.HEX.fullmatch(value):fail('digest_invalid')
    if not isinstance(files,dict) or digest(files)!=bound['filesHash']:fail('file_binding_changed')
    if load('command_delivery').inventory(output)!=files:fail('package_files_changed')
    if sha(lineage.file(output,'success.json'))!=bound['receiptSha256']:fail('receipt_changed')
    for name,expected in files.items():
        if sha(lineage.file(output,name))!=expected:fail('file_changed')
    if not isinstance(context,dict) or set(context)!={'projects','frames'}:fail('contexts_invalid')
    parents=bound['sourceRefs']
    if not isinstance(parents,dict):fail('source_refs_invalid')
    for name,value in parents.items():lineage.reference(value)
    artifacts=[];known=set();unmatched=[]
    frame_sources={f['path']:[] for f in context['frames']}
    inventories=[load('native_resources').inspect(output,p['path'],declared=next((i for i in declared or [] if i.get('project')==p['path']),None)) for p in context['projects']] if resources else None
    version_payload={'binding':bound,'contexts':context,'files':files}
    if resources:version_payload['nativeResources']=inventories
    version=digest(version_payload)
    def ref(name,logical):
        if name not in files and name!='success.json':fail('unlisted_reference')
        content=bound['receiptSha256'] if name=='success.json' else files[name]
        return {'assetId':logical,'version':content,'sha256':content,'location':name}
    for project in context['projects']:
        name=project['path'];path=lineage.file(output,name);native=lineage.read(path)
        if (files.get(name)!=project['sha256'] or not isinstance(native,dict) or native.get('schema')!=1
                or not isinstance(native.get('items'),dict)):fail('native_format_or_digest')
        deps=project['dependencies'];footage={str(row['id']) for row in native['items'].values() if row['kind']['type']=='Footage'}
        if set(deps)!=footage or sorted(int(i) for i in deps)!=project['snapshot']['footageItems']:fail('native_dependency_context_changed')
        parent=parents.get(name);logical=parent['assetId'] if parent else 'effectcraft-command:'+digest({'producer':producer,'path':name})
        known.add(name);dependencies=[]
        for item,asset in sorted(deps.items()):
            if files.get(asset['path'])!=asset['sha256']:fail('dependency_changed')
            lineage.file(output,asset['path']);known.add(asset['path'])
            dependencies.append({'assetRef':{k:v for k,v in ref(asset['path'],'effectcraft-media:'+digest({'assetId':logical,'item':item})).items() if k!='location'},
                                 'kind':'media','packaged':True,'missingReason':None})
        if resources:
            inventory=next(i for i in inventories if i['project']==name)
            dependencies.extend(load('native_resources').public_dependencies(inventory))
            known.update(r['path'] for r in inventory['luts'] if r.get('packaged') and r.get('path'))
        renditions=[]
        for frame in context['frames']:
            if all(project[k]==frame[k] for k in ('snapshot','nativeVersion','dependencies')):
                frame_sources[frame['path']].append(name)
                for location in [frame['path']]+[x['path'] for x in frame.get('inlineCopies',[])]:
                    renditions.append(ref(location,'effectcraft-rendition:'+digest({'assetId':logical,'path':location})))
        artifacts.append({'protocolVersion':'craft-artifact/v1','assetId':logical,'version':version,'sha256':files[name],
            'bytes':path.stat().st_size,'mediaType':'application/vnd.effectcraft.project+json','producerTaskId':producer['taskId'],
            'sourceRefs':[parent] if parent else [],'nativeProjectRef':{'assetId':logical,'version':version,'sha256':files[name],'location':name},
            'renditions':sorted(renditions,key=lambda r:r['location']),'dependencies':dependencies,'technicalMetadata':metadata(project),
            'lossReportRef':None,'evidenceRefs':[ref('success.json','effectcraft-receipt:'+digest(producer))],'location':name})
    for frame in context['frames']:
        if files.get(frame['path'])!=frame['sha256']:fail('frame_changed')
        if not frame_sources[frame['path']]:unmatched.append(frame['path'])
        known.add(frame['path'])
        for item in frame.get('inlineCopies',[]):
            if files.get(item['path'])!=frame['sha256'] or item['sha256']!=frame['sha256']:fail('inline_copy_changed')
            known.add(item['path'])
    result={'schema':'effectcraft-command-artifact-map/v1','binding':copy.deepcopy(bound),'files':copy.deepcopy(files),
            'contexts':copy.deepcopy(context),'artifacts':artifacts,'unmatchedFrames':sorted(unmatched),
            'unreviewed':sorted(set(files)-known),'exchangeLoss':'NOT_RUN','qualification':'registration only; quality remains independently evaluated'}
    if resources:result['nativeResources']=inventories
    return result


def build(store,state,data):
    try:
        if data['taskId']!=state['taskId'] or data['identityHash']!=state['identityHash']:fail('task_changed')
        bound={'schema':'effectcraft-command-artifact-binding/v1','producer':{'taskId':state['taskId'],'identityHash':state['identityHash']},
               'planHash':state['identity']['planHash'],'runtimeSha256':state['identity']['runtimeSha256'],'filesHash':digest(data['files']),
               'receiptSha256':data['receiptSha256'],'observationsHash':digest(data['observations']),'sourceRefs':source_refs(store,state)}
        return compile_map(state['output'],data['files'],bound,contexts(data),resources=True)
    except (ValueError,OSError,KeyError,TypeError) as error:
        if isinstance(error,ValueError) and str(error).startswith('command_artifact:'):raise
        fail(str(error))


def validate(output,mapping):
    """输出和映射一起搬迁后核对相对引用；不查询PID、不发送原生编辑。"""
    try:
        expected=compile_map(output,mapping['files'],mapping['binding'],mapping['contexts'],resources='nativeResources' in mapping,declared=mapping.get('nativeResources'))
        if expected!=mapping:fail('map_or_version_changed')
        return expected['artifacts']
    except (ValueError,OSError,KeyError,TypeError) as error:
        if isinstance(error,ValueError) and str(error).startswith('command_artifact:'):raise
        fail(str(error))


def verify_document(store,state,data):
    """已有扩展重验当前任务与文件；历史无扩展记录不在读取时补造。"""
    mapping=data['artifactMap'];validate(state['output'],mapping)
    expected={'producer':{'taskId':state['taskId'],'identityHash':state['identityHash']},'planHash':state['identity']['planHash'],
              'runtimeSha256':state['identity']['runtimeSha256'],'filesHash':digest(data['files']),
              'receiptSha256':data['receiptSha256'],'observationsHash':digest(data['observations'])}
    if (any(mapping['binding'].get(k)!=v for k,v in expected.items()) or mapping['files']!=data['files'] or mapping['contexts']!=contexts(data)):
        fail('task_or_observation_changed')


def reference(mapping):
    return {'schema':'effectcraft-command-artifact-reference/v1','sha256':digest(mapping),'artifacts':mapping['artifacts']}
