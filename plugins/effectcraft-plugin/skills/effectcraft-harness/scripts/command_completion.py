"""已完成命令的交付登记恢复；只核对原结果，不重新执行创作。"""
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import time


def load(name):
    spec=importlib.util.spec_from_file_location('completion_'+name,Path(__file__).with_name(name+'.py'))
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value


def read(path):
    load('segmented_sequence').regular_path(path)
    if not path.is_file() or path.stat().st_size>16*1024*1024:raise ValueError('completion_document_invalid')
    value=load('commands').reply_json(path.read_text(encoding='utf-8'))
    if not isinstance(value,dict):raise ValueError('completion_document_invalid')
    return value


def process_identity(value):
    """进程号仅作原生命周期绑定，不据此判断存活或发送信号。"""
    if (value.get('schema')!='effectcraft-process-lifecycle/v1'
            or any(type(value.get(k)) is not int or value[k]<=0 for k in ('guardianPid','workerGroup'))
            or type(value.get('startedAt')) not in (int,float) or not math.isfinite(value['startedAt'])):
        raise ValueError('completion_process_unconfirmed')
    ownership=value.get('ownership')
    # 字段缺失沿用非POSIX合同；显式坏值不能回退为无归属材料。
    if 'ownership' in value and (not isinstance(ownership,dict)
            or ownership.get('schema')!='effectcraft-posix-group-lease/v1'
            or not isinstance(ownership.get('nonce'),str) or not re.fullmatch('[a-f0-9]{32}',ownership['nonce'])):
        raise ValueError('completion_process_unconfirmed: invalid ownership')
    return {k:value[k] for k in ('guardianPid','workerGroup','startedAt')}|{'ownershipNonce':ownership['nonce'] if ownership is not None else None}


def material(store,state):
    """绑定全部成功操作、原成功日志、请求与项目素材，不补造旧任务材料。"""
    tasks=load('task_store');commands=load('commands');delivery=load('command_delivery')
    output=Path(state['output']);load('segmented_sequence').regular_path(output)
    if not output.is_dir():raise ValueError('completion_unresolved')
    if (state['schema']!='effectcraft-managed-task/v2' or state['identity']['mode'] not in ('commands','desktop')
            or not state['steps'] or any(step['state']!='succeeded' for step in state['steps'])):raise ValueError('completion_unresolved')
    request_path=store.path(state['taskId']).parent/'request.json';request=read(request_path)
    if tasks.digest(request)!=state['identity']['authorization'].get('requestHash'):raise ValueError('completion_unresolved')
    receipt=read(output/'success.json');journal=read(output/'journal.json')
    expected=hashlib.sha256(json.dumps(state['plan'],ensure_ascii=False,sort_keys=True,allow_nan=False).encode()).hexdigest()
    if (receipt!=journal or receipt.get('schema')!='craft-command-receipt/v1' or receipt.get('result')!='PASS'
            or receipt.get('pluginId')!='effectcraft' or receipt.get('runtimeSha256')!=state['identity']['runtimeSha256']
            or receipt.get('mode')!=('bridge' if state['identity']['mode']=='desktop' else 'headless')
            or receipt.get('planSha256')!=expected or len(receipt.get('steps',[]))!=len(state['plan']['operations'])):
        raise ValueError('completion_unresolved')
    bindings={'output':str(output)}
    for name,path in request['inputs'].items():
        expected_sha=state['identity']['inputHashes'][name];item=receipt['inputs'][name]
        target=load('quality_review').contained(output,item['path'])
        if item['sha256']!=expected_sha or tasks.file_sha(Path(path))!=expected_sha or tasks.file_sha(target)!=expected_sha:
            raise ValueError('completion_unresolved')
        bindings[name]={'path':str(target),'sha256':expected_sha}
    cursor=0
    for index,(op,row) in enumerate(zip(state['plan']['operations'],receipt['steps'])):
        args=commands.resolve(op['params'],bindings)
        if (row.get('index')!=index or row.get('state')!='succeeded' or row.get('command')!=op.get('command')
                or row.get('tool')!=op.get('tool') or row.get('params')!=args or 'result' not in row):raise ValueError('completion_unresolved')
        tool,arguments=commands.native_call(op['command'],args) if 'command' in op else (op['tool'],args)
        result=copy.deepcopy(row['result'])
        if isinstance(result,dict) and isinstance(result.get('content'),list):
            for item in result['content']:
                if isinstance(item,dict) and item.get('type')=='image':item.pop('path',None)
        digest=tasks.digest({'name':tool,'arguments':arguments});found=False
        for position in range(cursor,len(state['steps'])):
            step=state['steps'][position]
            if step['operation']==tool and step['argumentsHash']==digest and step['resultHash']==tasks.digest(result):
                cursor=position+1;found=True;break
        if not found:raise ValueError('completion_unresolved')
        if 'as' in op:bindings[op['as']]=row['result']
    base=store.path(state['taskId']).parent
    observations={}
    for path in sorted((delivery.directory(store,state['taskId'])/'observations').rglob('*')):
        load('segmented_sequence').regular_path(path)
        if path.is_file():observations[path.relative_to(base).as_posix()]=tasks.file_sha(path)
    desktop_sha=None
    if state['identity']['mode']=='desktop':
        stopped=read(output/'desktop-session.json')
        if (stopped.get('schema')!='craft-owned-desktop-session/v1' or stopped.get('domain')!='effectcraft'
                or stopped.get('ownedProcessesStopped') is not True or stopped.get('listenerOwnedByPID') is not True
                or type(stopped.get('sessionsStarted')) is not int or stopped['sessionsStarted']<1):raise ValueError('completion_process_unconfirmed')
        desktop_sha=tasks.file_sha(output/'desktop-session.json')
    return {'stepsHash':tasks.digest(state['steps']),'receipts':{step['id']:tasks.file_sha(base/'receipts'/(step['id']+'.json')) for step in state['steps']},
            'successSha256':tasks.file_sha(output/'success.json'),'journalSha256':tasks.file_sha(output/'journal.json'),
            'requestSha256':tasks.file_sha(request_path),'files':delivery.inventory(output),'observations':observations,
            'outputIdentity':[output.stat().st_dev,output.stat().st_ino],'desktopStopSha256':desktop_sha,
            'worker':state['worker'],'deadline':state['deadline'],'budget':state['budget']}


def capture(store,task):
    """仅活跃worker在成功返回后登记完成证明；悬空旧证明不自动接管。"""
    with store.lock():
        state=store.read(task);store.allowed(state)
        if state['state']!='running':raise ValueError('completion_unresolved')
        path=store.path(task).parent/'command-completion.json'
        if 'commandCompletion' in state:return validate(store,state)
        if path.exists() or path.is_symlink():raise ValueError('completion_orphan_proof')
        value=material(store,state);bound=load('runtime_binding').resolve(store,task)
        lifecycle=read(store.lifecycle_path(state))
        if lifecycle.get('status')!='running':raise ValueError('completion_process_unconfirmed')
        value.update(schema='effectcraft-command-completion/v1',taskId=task,identityHash=state['identityHash'],
                     runtimeBindingHash=load('task_store').digest(state['identity']['runtimeBinding']),
                     processIdentity=process_identity(lifecycle),lifecycleReceipt=store.lifecycle_path(state).name)
        load('review_ledger').immutable(path,value)
        state['commandCompletion']={'schema':'effectcraft-command-completion-reference/v1','sha256':load('task_store').file_sha(path)}
        store.save(state);return value


def validate(store,state):
    """重读完整材料；任何变更拒绝恢复，不删除、不重新保存原作品。"""
    try:
        tasks=load('task_store');reference=state['commandCompletion'];path=store.path(state['taskId']).parent/'command-completion.json'
        if (set(reference)!={'schema','sha256'} or reference['schema']!='effectcraft-command-completion-reference/v1'
                or tasks.file_sha(path)!=reference['sha256']):raise ValueError('reference')
        value=read(path)
        expected=material(store,state)
        expected.update(schema='effectcraft-command-completion/v1',taskId=state['taskId'],identityHash=state['identityHash'],
                        runtimeBindingHash=tasks.digest(state['identity']['runtimeBinding']),
                        processIdentity=value['processIdentity'],lifecycleReceipt=store.lifecycle_path(state).name)
        if value!=expected:raise ValueError('binding')
        load('runtime_binding').resolve(store,state['taskId'])
        return value
    except (OSError,ValueError,KeyError,TypeError) as error:raise ValueError('completion_proof_invalid: '+str(error)) from error


def recover(store,task):
    """取得原执行租约，锁外只读核验，锁内再次复核后补齐交付登记。"""
    state=store.read(task)
    if 'commandCompletion' not in state or state['state'] not in ('running','reconciling'):return state
    platform=load('platform_support');tasks=load('task_store')
    with platform.exclusive_lock(store.root/'leases'/(task+'.supervisor.lock'),timeout=0), platform.exclusive_lock(store.root/'leases'/(task+'.lifecycle.lock'),timeout=0), platform.exclusive_lock(store.root/'leases'/(task+'.lock'),timeout=0):
        with store.lock():
            state=store.read(task);store.allowed(state);store.check_source_revision(state);context=validate(store,state)
            lifecycle_path=store.lifecycle_path(state);lifecycle=read(lifecycle_path)
            if lifecycle.get('status')!='stopped' or process_identity(lifecycle)!=context['processIdentity']:
                raise ValueError('completion_process_unconfirmed')
            tasks.exit_evidence(lifecycle.get('returncode'),lifecycle.get('ownership'));lifecycle_sha=tasks.file_sha(lifecycle_path)
            bound=load('runtime_binding').resolve(store,task)
        delivery=load('command_delivery');proof=delivery.finalize(store,task)
        report=delivery.inspect(store,task,bound['runtimeHome'],proof=proof)
        if report['engineering']['status']=='PASS' and report['technical']['status']=='PASS':
            request=read(store.path(task).parent/'request.json')
            if request.get('commandRevision'):
                load('command_revision').validate_result(store,task,proof,bound['runtimeHome'],for_reconcile=True)
        with store.lock():
            latest=store.read(task);store.allowed(latest);store.check_source_revision(latest)
            if latest['state'] not in ('running','reconciling') or validate(store,latest)!=context:
                raise ValueError('completion_proof_invalid: task changed')
            if tasks.file_sha(store.lifecycle_path(latest))!=lifecycle_sha:raise ValueError('completion_process_unconfirmed')
            delivery.document(store,task,proof)
            ready=report['engineering']['status']=='PASS' and report['technical']['status']=='PASS'
            latest.update(state='review_ready' if ready else 'reconciling')
            latest['reconciliation']={'result':'verified_completed_commands' if ready else 'completed_commands_not_verified',
                'automaticReplay':False,'completionSha256':latest['commandCompletion']['sha256'],
                'lifecycleSha256':lifecycle_sha,'completionReview':report}
            if ready:latest['delivery']=dict(proof,engineeringReopen='PASS')
            return store.save(latest)
