"""登记自有孤儿段的原子归档意图；核对移动结果，不重放原生编辑。"""
import importlib.util
from pathlib import Path
import re
import tempfile


def load(name):
    spec=importlib.util.spec_from_file_location('orphan_'+name,Path(__file__).with_name(name+'.py'))
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value


def identity(path):
    load('segmented_sequence').regular_path(path)
    if not path.is_dir():raise ValueError('orphan_segment_missing')
    stat=path.stat();return [stat.st_dev,stat.st_ino]


def snapshot(path, expected):
    if identity(path)!=expected:raise ValueError('orphan_segment_identity_changed')
    files={}
    for child in path.iterdir():
        if (child.is_symlink() or not child.is_file()
                or not re.fullmatch(r'(?:frame(?:_[0-9]{5})?\.png|sequence\.json)',child.name)):
            raise ValueError('orphan_segment_unowned_file')
        files[child.name]={'sha256':load('task_store').file_sha(child),'bytes':child.stat().st_size}
    if identity(path)!=expected:raise ValueError('orphan_segment_identity_changed')
    return files


def validate(state):
    value=state.get('orphanArchives',{'schema':'effectcraft-orphan-archives/v1','entries':[]})
    if not isinstance(value,dict) or set(value)!={'schema','entries'} or value['schema']!='effectcraft-orphan-archives/v1' or not isinstance(value['entries'],list):
        raise ValueError('orphan_archive_invalid')
    output=Path(state['output']);seen=set()
    locations=state.get('resourceLocations',{}).get('locations',[])
    for row in value['entries']:
        if not isinstance(row,dict) or set(row)!={'source','identity','container','containerIdentity','destination','files','phase'}:
            raise ValueError('orphan_archive_invalid')
        if any(not isinstance(row[k],str) for k in ('source','container','destination')):raise ValueError('orphan_archive_invalid')
        source=Path(row['source']);container=Path(row['container']);destination=Path(row['destination'])
        if (source.parent!=output or not source.name.startswith('.effect-segment-')
                or container.parent!=output.parent or not container.name.startswith('.effectcraft-recovery-')
                or destination!=container/'segment' or row['phase'] not in ('prepared','archived')
                or row['source'] in seen):raise ValueError('orphan_archive_invalid')
        for key in ('identity','containerIdentity'):
            if not isinstance(row[key],list) or len(row[key])!=2 or any(type(n) is not int or n<0 for n in row[key]):
                raise ValueError('orphan_archive_invalid')
        if not isinstance(row['files'],dict):raise ValueError('orphan_archive_invalid')
        for name,facts in row['files'].items():
            if (not isinstance(name,str) or not re.fullmatch(r'(?:frame(?:_[0-9]{5})?\.png|sequence\.json)',name)
                    or not isinstance(facts,dict) or set(facts)!={'sha256','bytes'}
                    or type(facts['bytes']) is not int or facts['bytes']<0
                    or not isinstance(facts['sha256'],str) or not re.fullmatch('[a-f0-9]{64}',facts['sha256'])):
                raise ValueError('orphan_archive_invalid')
        location=next((r for r in locations if r['path']==row['source'] and r['identity']==row['identity']),None)
        if location is None:raise ValueError('orphan_archive_invalid')
        if row['phase']=='archived' and (location['kind']!='archived_segment' or location['alternate']!=row['destination']):
            raise ValueError('orphan_archive_invalid')
        seen.add(row['source'])
    for location in locations:
        if location['kind']=='archived_segment' and not any(r['source']==location['path'] and r['phase']=='archived' for r in value['entries']):
            raise ValueError('orphan_archive_invalid')
    return value


def verify_container(row):
    container=Path(row['container'])
    if identity(container)!=row['containerIdentity'] or any(p.name!='segment' for p in container.iterdir()):
        raise ValueError('orphan_archive_container_changed')


def settle_locked(store, task):
    """调用者持账本锁；只承认原移动事实，源仍在时不启动移动。"""
    state=store.read(task);value=validate(state);changed=False
    for row in value['entries']:
        verify_container(row);source=Path(row['source']);destination=Path(row['destination'])
        if source.exists() or source.is_symlink():
            if row['phase']!='prepared' or destination.exists() or destination.is_symlink():raise ValueError('orphan_segment_ambiguous')
            if snapshot(source,row['identity'])!=row['files']:raise ValueError('orphan_segment_changed')
            continue
        if snapshot(destination,row['identity'])!=row['files']:raise ValueError('orphan_segment_changed')
        if row['phase']=='prepared':
            location=next(r for r in state['resourceLocations']['locations'] if r['path']==row['source'])
            location.update(kind='archived_segment',alternate=row['destination'],retired=True)
            row['phase']='archived';changed=True
    if changed:store.save(state)
    return state


def owned_files(state):
    """只读校验未发布的登记目录；返回可由导出检查点接受的文件集合。"""
    validate(state);files=set()
    for row in state.get('resourceLocations',{}).get('locations',[]):
        source=Path(row['path'])
        if row['kind']=='segment' and (source.exists() or source.is_symlink()):
            facts=snapshot(source,row['identity'])
            files.update(source/name for name in facts)
    return files


def move(source, destination):
    """私有同文件系统目标内移动；跨卷/权限失败保留原目录。"""
    if destination.exists() or destination.is_symlink():raise ValueError('orphan_segment_ambiguous')
    if source.stat().st_dev!=destination.parent.stat().st_dev:raise ValueError('orphan_archive_cross_device')
    source.rename(destination)


def archive_locked(store, task):
    """仅显式恢复调用，调用者持任务/生命周期及账本锁。"""
    state=settle_locked(store,task);store.allowed(state)
    for location in list(state.get('resourceLocations',{}).get('locations',[])):
        if location['kind']!='segment':continue
        source=Path(location['path'])
        if not source.exists() and not source.is_symlink():continue
        files=snapshot(source,location['identity'])
        state=store.read(task);store.allowed(state)
        value=state.setdefault('orphanArchives',{'schema':'effectcraft-orphan-archives/v1','entries':[]})
        row=next((r for r in value['entries'] if r['source']==str(source)),None)
        if row is None:
            container=Path(tempfile.mkdtemp(prefix='.effectcraft-recovery-',dir=Path(state['output']).parent))
            row={'source':str(source),'identity':location['identity'],'container':str(container),
                'containerIdentity':identity(container),'destination':str(container/'segment'),'files':files,'phase':'prepared'}
            value['entries'].append(row);validate(state);store.save(state)
        verify_container(row)
        if snapshot(source,row['identity'])!=row['files']:raise ValueError('orphan_segment_changed')
        store.allowed(store.read(task))
        move(source,Path(row['destination']))
        state=settle_locked(store,task)
    return state


def archive_pending(store, task):
    """内部归档入口；生产调用者另持原任务生命周期锁。"""
    with store.lock():return archive_locked(store,task)
