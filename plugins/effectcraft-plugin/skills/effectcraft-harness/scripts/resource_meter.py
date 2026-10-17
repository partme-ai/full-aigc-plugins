"""登记自有媒体目录身份，核对崩溃后残留；不读取或清理外部目录。"""
import importlib.util
import math
from pathlib import Path
import re
import time


def load(name):
    spec=importlib.util.spec_from_file_location('resource_meter_'+name,Path(__file__).with_name(name+'.py'))
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value


def validate(value, output):
    if not isinstance(value,dict) or value.get('schema')!='effectcraft-resource-locations/v1' or not isinstance(value.get('locations'),list):
        raise ValueError('resource_locations_invalid')
    output=Path(output);seen=set()
    for row in value['locations']:
        if not isinstance(row,dict) or set(row)-{'media'}!={'path','alternate','identity','kind','retired'}:raise ValueError('resource_locations_invalid')
        path=Path(row['path']);alternate=Path(row['alternate'])
        if (not path.is_absolute() or not alternate.is_absolute() or '..' in path.parts or '..' in alternate.parts
                or not isinstance(row['identity'],list) or len(row['identity'])!=2
                or any(type(n) is not int or n<0 for n in row['identity']) or type(row['retired']) is not bool):
            raise ValueError('resource_locations_invalid')
        if row['kind']=='workflow':
            valid=(path==output or path.parent==output.parent and path.name.startswith('.effectcraft-')) and alternate==output
        elif row['kind']=='commands':
            valid=path==output and alternate==output
            media=row.get('media',[])
            if (not isinstance(media,list) or any(not isinstance(n,str) for n in media) or len(media)!=len(set(media))
                    or any(not isinstance(n,str) or not n or not Path(n).parts or Path(n).is_absolute() or '..' in Path(n).parts
                        or Path(n).parts[0] in ('inputs','.desktop-data') for n in media)):raise ValueError('resource_locations_invalid')
        elif row['kind']=='segment':
            valid=(path.parent==output and path.name.startswith('.effect-segment-') and alternate.parent==output/'rgba-segments'
                and re.fullmatch('segment_[0-9]{5}',alternate.name))
        elif row['kind']=='archived_segment':
            valid=(path.parent==output and path.name.startswith('.effect-segment-') and alternate.name=='segment'
                and alternate.parent.parent==output.parent and alternate.parent.name.startswith('.effectcraft-recovery-')
                and row['retired'])
        else:valid=False
        if 'media' in row and row['kind']!='commands':raise ValueError('resource_locations_invalid')
        if not valid or row['path'] in seen:raise ValueError('resource_locations_invalid')
        seen.add(row['path'])
    return value


def validate_observation(value):
    if (not isinstance(value,dict) or value.get('schema')!='effectcraft-resource-observation/v1'
            or value.get('status') not in ('PASS','UNKNOWN') or type(value.get('at')) not in (int,float)
            or not math.isfinite(value['at'])):raise ValueError('resource_observation_invalid')
    if value['status']=='PASS':
        if (set(value)!={'schema','status','at','observedBytes','mediaFiles'}
                or any(type(value[k]) is not int or value[k]<0 for k in ('observedBytes','mediaFiles'))):
            raise ValueError('resource_observation_invalid')
    elif set(value)!={'schema','status','at','error'} or not isinstance(value['error'],str):
        raise ValueError('resource_observation_invalid')


def watch(store, task, path, alternate, kind, media=None):
    path=Path(path).absolute();alternate=Path(alternate).absolute()
    path=path.parent.resolve()/path.name;alternate=alternate.parent.resolve()/alternate.name
    load('segmented_sequence').regular_path(path)
    if not path.is_dir():raise ValueError('resource_location_missing')
    identity=[path.stat().st_dev,path.stat().st_ino]
    with store.lock():
        state=store.read(task);store.allowed(state)
        value=state.setdefault('resourceLocations',{'schema':'effectcraft-resource-locations/v1','locations':[]})
        for row in value['locations']:
            if row['path']==str(path) or row['identity']==identity and row['kind']==kind:
                if row['identity']!=identity or row['kind']!=kind:raise ValueError('resource_location_identity_changed')
                if media is not None:
                    row['media']=sorted(set(row.get('media',[])+media));validate(value,state['output']);store.save(state)
                return
        value['locations'].append({'path':str(path),'alternate':str(alternate),'identity':identity,'kind':kind,'retired':False})
        if media is not None:value['locations'][-1]['media']=sorted(set(media))
        validate(value,state['output']);store.save(state)


def retire(store, task, path):
    path=Path(path).absolute();path=path.parent.resolve()/path.name
    with store.lock():
        state=store.read(task)
        row=next(r for r in state['resourceLocations']['locations'] if r['path']==str(path))
        row['retired']=True;store.save(state)


def files(state):
    """只核对已登记身份；发布前后路径重复命中的文件只计一次。"""
    value=validate(state['resourceLocations'],state['output']);result=set()
    for row in value['locations']:
        roots=[]
        for candidate in dict.fromkeys((row['path'],row['alternate'])):
            path=Path(candidate)
            if not path.exists() and not path.is_symlink():continue
            load('segmented_sequence').regular_path(path)
            if not path.is_dir() or [path.stat().st_dev,path.stat().st_ino]!=row['identity']:
                # 分段发布前，alternate可能仍是上一次失败的已核验段；不是本次身份就不读取它。
                if row['kind']=='segment' and candidate==row['alternate']:continue
                if roots and candidate==row['alternate']:continue
                raise ValueError('resource_location_identity_changed')
            roots.append(path)
        if not roots:
            if row['retired'] and row['kind']!='archived_segment':continue
            raise ValueError('resource_location_missing')
        for root in roots:
            if row['kind']=='commands':
                import os
                paths=[root/name for name in row.get('media',[])]
                for parent,dirs,names in os.walk(root,followlinks=False):
                    base=Path(parent)
                    if base==root:dirs[:]=[d for d in dirs if d not in ('inputs','.desktop-data')]
                    for name in dirs:
                        if (base/name).is_symlink():raise ValueError('resource_media_symlink')
                    paths.extend(base/name for name in names if Path(name).suffix.lower()=='.png')
            elif row['kind'] in ('segment','archived_segment'):paths=list(root.glob('frame_*.png'))+list(root.glob('frame.png'))
            else:
                paths=list(root.glob('frame-*.png'))+[root/'intro.mp4']
                for name in ('rgba-sequence','rgba-segments'):
                    folder=root/name
                    load('segmented_sequence').regular_path(folder)
                    if folder.exists():
                        for item in folder.rglob('*'):
                            if item.is_symlink():raise ValueError('resource_media_symlink')
                        paths.extend(folder.rglob('*.png'))
            for path in paths:
                if path.is_symlink():raise ValueError('resource_media_symlink')
                if path.is_file():result.add(path)
    return result


def sample_locked(store, task, live=False):
    """调用者持账本锁；越界/未知事实先落盘，不因异常丢失诊断。"""
    state=store.read(task)
    if not state.get('resourceLocations'):return state
    try:
        media=files(state);total=sum(path.stat().st_size for path in media)
        load('resource_budget').observe_locked(store,state,total)
        state=store.read(task)
        state['resourceObservation']={'schema':'effectcraft-resource-observation/v1','status':'PASS',
            'at':time.time(),'observedBytes':total,'mediaFiles':len(media)}
        return store.save(state)
    except (ValueError,OSError) as error:
        if live and isinstance(error,FileNotFoundError):return store.read(task)
        state=store.read(task)
        state['resourceObservation']={'schema':'effectcraft-resource-observation/v1','status':'UNKNOWN','at':time.time(),'error':str(error)}
        store.save(state);raise


def sample(store, task, live=False):
    with store.lock():return sample_locked(store,task,live)
