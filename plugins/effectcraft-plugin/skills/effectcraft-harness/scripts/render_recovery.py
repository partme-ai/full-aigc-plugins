"""受管理分段导出内部检查点；只允许续跑渲染，不复用编辑调用。"""
import importlib.util
from pathlib import Path

HERE=Path(__file__).resolve().parent


def load(name):
    spec=importlib.util.spec_from_file_location('render_recovery_'+name,HERE/(name+'.py'))
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value


def resources():
    """绑定同一技能的执行代码与锁，升级后不冒用新执行器恢复旧任务。"""
    return {p.relative_to(HERE).as_posix():load('task_store').file_sha(p)
        for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}


def capture(store,task,operation,context):
    """在首次渲染前绑定任务、原生工程、素材和预览字节。"""
    with store.lock():
        state=store.read(task);store.allowed(state)
        if state['schema']!='effectcraft-managed-task/v2' or state['state']!='running':raise ValueError('state_conflict')
        step=state['steps'][-1]
        expected={'project':context['project'],'exports':context['plan'].get('exports',[])}
        if (step['id']!=operation or step['operation']!='render_and_deliver' or step['state']!='attempted'
                or step['argumentsHash']!=load('task_store').digest(expected)
                or any(s['state']!='succeeded' for s in state['steps'][:-1])):
            raise ValueError('render_recovery_operation_invalid')
        if context['plan'].get('exports',[{}])[0].get('format')!='png-segmented':raise ValueError('render_recovery_format_invalid')
        output=Path(context['output'])
        if output.is_symlink() or not output.is_dir() or output!=Path(state['output']):raise ValueError('render_recovery_output_invalid')
        if Path(context['stage'])!=output or Path(context['project'])!=output/'project.ecproj':raise ValueError('render_recovery_project_invalid')
        files={}
        for path in output.rglob('*'):
            if path.is_symlink():raise ValueError('render_recovery_symlink')
            if path.is_file():files[path.relative_to(output).as_posix()]=load('task_store').file_sha(path)
        value=dict(context,taskId=task,identityHash=state['identityHash'],operationId=operation,
            outputIdentity=[output.stat().st_dev,output.stat().st_ino],immutableFiles=files,resources=resources())
        path=store.path(task).parent/'render-context.json'
        load('task_store').atomic_json(path,value)
        state['renderRecovery']={'schema':'effectcraft-render-recovery/v1','contextSha256':load('task_store').file_sha(path),'operationId':operation}
        store.save(state)


def validate(store,state):
    """只读核对当前检查点；持有任务/生命周期锁的调用者才能据此继续。"""
    reference=state['renderRecovery'];path=store.path(state['taskId']).parent/'render-context.json';tasks=load('task_store')
    if reference.get('schema')!='effectcraft-render-recovery/v1' or tasks.file_sha(path)!=reference['contextSha256']:
        raise ValueError('render_recovery_context_changed')
    value=load('commands').reply_json(path.read_text(encoding='utf-8'))
    if (value.get('schema')!='effectcraft-export-context/v1' or value['taskId']!=state['taskId']
            or value['identityHash']!=state['identityHash'] or tasks.digest(value['plan'])!=state['identity']['planHash']
            or value['operationId']!=reference['operationId']):raise ValueError('render_recovery_binding_changed')
    step=state['steps'][-1]
    if (step['id']!=reference['operationId'] or step['operation']!='render_and_deliver'
            or any(s['state']!='succeeded' for s in state['steps'][:-1])):
        raise ValueError('render_recovery_operation_invalid')
    output=Path(value['output'])
    load('segmented_sequence').regular_path(output)
    if (output!=Path(state['output']) or not output.is_dir()
            or [output.stat().st_dev,output.stat().st_ino]!=value['outputIdentity']):raise ValueError('render_recovery_output_changed')
    if tasks.file_sha(value['cli'])!=value['runtimeSha256'] or value['runtimeSha256']!=state['identity']['runtimeSha256']:
        raise ValueError('render_recovery_runtime_changed')
    if value['resources']!=resources():raise ValueError('render_recovery_resources_changed')
    for relative,expected in value['immutableFiles'].items():
        path=output/relative
        if not path.resolve().is_relative_to(output.resolve()) or path.is_symlink() or not path.is_file() or tasks.file_sha(path)!=expected:
            raise ValueError('render_recovery_input_changed: '+relative)
    generated={'exchange-loss.json','manifest.json'}
    orphan_files=load('orphan_segments').owned_files(state)
    for path in output.rglob('*'):
        if path.is_symlink():raise ValueError('render_recovery_symlink')
        if not path.is_file():continue
        relative=path.relative_to(output).as_posix()
        if relative in value['immutableFiles'] or relative in generated or relative.startswith('rgba-segments/') or path in orphan_files:continue
        if relative=='failure.json':
            failure=load('commands').reply_json(path.read_text(encoding='utf-8'))
            if failure.get('schema')=='craft-failed-stage/v1' and (output/failure['stage']).resolve()==Path(value['working']).resolve():continue
        raise ValueError('render_recovery_unowned_file: '+relative)
    if value['sourceProject'] and tasks.file_sha(value['sourceProject'])!=value['sourceHash']:raise ValueError('revision_conflict')
    for name,asset in value['plan'].get('assets',{}).items():
        if tasks.file_sha(asset['path'])!=state['identity']['inputHashes'][name]:raise ValueError('input_changed')
    return value


def archive_failure(store,task,context):
    """保留旧失败诊断到任务目录，不把它装进成功交付清单。"""
    path=Path(context['output'])/'failure.json'
    if path.exists():
        failure=load('commands').reply_json(path.read_text(encoding='utf-8'))
        target=store.path(task).parent/('render-failure-'+str(len(store.read(task).get('renderResumes',[])))+'.json')
        load('task_store').atomic_json(target,failure);path.unlink()
