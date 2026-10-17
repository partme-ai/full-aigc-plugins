"""对已授权对象属性执行最多两轮修订，并验证非目标内容保全。"""
import copy
import importlib.util
from pathlib import Path
import uuid
import time


def load(name):
    spec=importlib.util.spec_from_file_location('craft_revision_'+name,Path(__file__).with_name(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def validate_revision(plan, manifest, scope):
    allowed=set()
    bindings=manifest['bindings']
    for row in scope:
        if row['layer'] not in bindings or not isinstance(row.get('properties'),list):
            raise ValueError('revision_scope_invalid')
        layer=str(bindings[row['layer']]['layer'])
        allowed.update((layer,path) for path in row['properties'])
    touched=set()
    if not plan.get('operations'):
        raise ValueError('revision_empty')
    if any(key in plan for key in ('document','assets','revisionScope')):
        raise ValueError('revision_scope_exceeded')
    for operation in plan['operations']:
        command=operation['command']
        if command not in ('layer.setText','prop.set'):
            raise ValueError('revision_command_not_allowed')
        params=load('workflow').resolve(operation['params'],bindings)
        fields={'layer','text'} if command=='layer.setText' else {'layer','path','value'}
        if set(params)!=fields:
            raise ValueError('revision_parameters_not_allowed')
        address=(str(params['layer']),'text/sourceText' if command=='layer.setText' else params['path'])
        if address not in allowed:raise ValueError('revision_scope_exceeded')
        touched.add(address)
    return touched


def assert_preserved(before, after, targets):
    """只排除明确授权的属性值；关键帧、层级及其他字段仍参与完整比较。"""
    def normalized(value):
        value=copy.deepcopy(value)
        def walk(node,layer):
            if isinstance(node,dict):
                if (layer,node.get('path')) in targets and 'value' in node:
                    node['value']='<authorized-value>'
                for child in node.values():walk(child,layer)
            elif isinstance(node,list):
                for child in node:walk(child,layer)
        for layer,node in value.get('layers',{}).items():walk(node,str(layer))
        return value
    if normalized(before)!=normalized(after):
        raise ValueError('non_target_changed')


def revise(store, task, plan, output, runtime_home):
    if store.read(task)['identity']['mode']!='workflow':
        return load('command_revision').revise(store,task,plan,output,runtime_home)
    managed=load('managed'); quality=load('quality_review')
    state=store.read(task)
    root=store.lineage(state)[-1]
    if state['state']!='review_ready' or not state.get('review'):
        raise ValueError('review_required')
    review_path=store.path(task).parent/state['review']['path']
    if load('task_store').file_sha(review_path)!=state['review']['sha256']:
        raise ValueError('review_changed')
    report=managed.read(review_path)
    ledger=load('review_ledger').validate(store,root,load('task_store').digest(managed.read(store.path(task).parent/'judge-request.json')['criteria']))
    if task not in ledger['entries'] or ledger['entries'][task]['reportSha256']!=state['review']['sha256']:
        raise ValueError('settled_review_required')
    if report['technical']['status']!='PASS' or report['creative']['status']!='FAIL':
        raise ValueError('failed_creative_review_required')
    source=Path(state['output'])
    if quality.binding(source)!=report['binding']:raise ValueError('artifact_changed')
    scope=root['plan'].get('revisionScope',[])
    if not scope:raise ValueError('revision_scope_missing')
    manifest=managed.read(source/'manifest.json')
    targets=validate_revision(plan,manifest,scope)
    if plan.get('expectedProjectSha256')!=manifest['files']['project.ecproj']:
        raise ValueError('revision_conflict')
    managed.preflight(plan,output,'workflow',source=source)
    with store.lock():
        root=store.read(root['taskId']);store.allowed(root)
        if root['budget']['revisions']>=2 or root['budget']['stagnant']>=2:
            raise ValueError('revision_budget_exhausted')
        if root.get('activeRevision'):
            raise ValueError('revision_in_progress')
    # 预算先检查，原生只读核验在全局状态锁之外进行；结算前再次核对取消与并发。
    engineering=load('engineering_review').verify(source,runtime_home,state['identity']['runtimeSha256'],
        timeout=max(.1,min(120,root['deadline']-time.time())))
    if engineering['status']!='PASS':raise ValueError('engineering_gate: '+engineering.get('reason',engineering['status']))
    if quality.binding(source)!=report['binding']:raise ValueError('artifact_changed')
    with store.lock():
        root=store.read(root['taskId']);store.allowed(root)
        if root['budget']['revisions']>=2 or root['budget']['stagnant']>=2:
            raise ValueError('revision_budget_exhausted')
        if root.get('activeRevision'):raise ValueError('revision_in_progress')
        child=uuid.uuid4().hex
        root['budget']['revisions']+=1;root['activeRevision']=child;store.save(root)
    # 预算在尝试前持久化；异常不回退次数，也不自动重复尝试。
    result=managed.run(store,plan,output,runtime_home,source=source,task=child,parent=root['taskId'])
    if result['state']=='review_ready':
        try:
            assert_preserved(managed.read(source/'native.json'),managed.read(Path(output)/'native.json'),targets)
        except ValueError as error:
            store.fail(child,str(error),unknown=True)
            raise
        with store.lock():
            latest=store.read(root['taskId']);latest['activeRevision']=None;store.save(latest)
    return result
