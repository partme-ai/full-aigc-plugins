"""取消任务族的停止证明与终态屏障；只读核对后代，不重放编辑。"""
from contextlib import ExitStack
import importlib.util
import math
from pathlib import Path
import re
import time


def load(name):
    spec=importlib.util.spec_from_file_location('cancel_'+name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def valid_id(value):return isinstance(value,str) and re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,95}',value)
def valid_sha(value):return isinstance(value,str) and re.fullmatch('[a-f0-9]{64}',value)
def valid_time(value):return type(value) in (int,float) and math.isfinite(value) and value>0


def validate(state, check_state=True):
    """校验版本化取消证明；历史无证明记录不在读取时补造。"""
    local=state.get('cancellationLocal')
    if local is not None:
        if (not isinstance(local,dict) or set(local)!={'schema','taskId','identityHash','kind','at'}
                or local['schema']!='effectcraft-cancellation-local/v1' or local['kind']!='not-started'
                or local['taskId']!=state['taskId'] or local['identityHash']!=state['identityHash']
                or not valid_time(local['at']) or not valid_time(state.get('cancellationRequestedAt'))
                or not state['createdAt'] <= local['at'] <= state['updatedAt']):
            raise ValueError('cancellation_local_invalid')
    family=state.get('cancellationFamily')
    if family is None:return
    if (not isinstance(family,dict) or set(family)!={'schema','taskId','identityHash','members','pendingTasks','unknownTasks','reasons','status','checkedAt','originalState'}
            or family['schema']!='effectcraft-cancellation-family/v1' or family['taskId']!=state['taskId']
            or family['identityHash']!=state['identityHash'] or not valid_time(family['checkedAt'])
            or family['originalState'] not in load('task_store').STATES
            or not state['createdAt'] <= family['checkedAt'] <= state['updatedAt']
            or not isinstance(family['members'],list) or not family['members']):raise ValueError('cancellation_family_invalid')
    members={}
    for member in family['members']:
        if (not isinstance(member,dict) or set(member)!={'taskId','identityHash','parent'}
                or not valid_id(member['taskId']) or not valid_sha(member['identityHash'])
                or member['taskId'] in members or member['parent'] is not None and not valid_id(member['parent'])):
            raise ValueError('cancellation_family_invalid')
        members[member['taskId']]=member
    if state['taskId'] not in members or members[state['taskId']]['identityHash']!=state['identityHash'] or members[state['taskId']]['parent']!=state['parent']:
        raise ValueError('cancellation_family_invalid')
    for task,member in members.items():
        seen=set()
        while task!=state['taskId']:
            if task in seen or task not in members:raise ValueError('cancellation_family_invalid')
            seen.add(task);task=members[task]['parent']
    for name in ('pendingTasks','unknownTasks'):
        ids=family[name]
        if not isinstance(ids,list) or any(not valid_id(x) for x in ids) or ids!=sorted(set(ids)) or set(ids)-members.keys():
            raise ValueError('cancellation_family_invalid')
    expected='waiting' if family['pendingTasks'] else 'unknown' if family['unknownTasks'] else 'stopped'
    if (set(family['pendingTasks'])&set(family['unknownTasks']) or family['status']!=expected
            or not isinstance(family['reasons'],dict) or set(family['reasons'])!=set(family['pendingTasks'])
            or any(not isinstance(x,str) or not x for x in family['reasons'].values())):
        raise ValueError('cancellation_family_invalid')

    if check_state and state['state'] not in ({'waiting':{'cancel_requested'},'unknown':{'reconciling'},'stopped':{'cancelled','review_ready','completed'}}[expected]):
        raise ValueError('cancellation_family_state_conflict')


def members_locked(store, state, states=None):
    """重读完整后代及原冻结名单；缺失/换身份/改父链不得静默丢弃。"""
    store.lineage(state)
    states=states if states is not None else store.all();by_id={x['taskId']:x for x in states};by_id[state['taskId']]=state
    ids={state['taskId']}
    while True:
        more={x['taskId'] for x in states if x['parent'] in ids}
        if more.issubset(ids):break
        ids.update(more)
    previous=state.get('cancellationFamily',{}).get('members',[])
    for old in previous:
        current=by_id.get(old['taskId'])
        if current is None:raise ValueError('cancellation_family_member_missing')
        if old['taskId'] not in ids or any(current[k]!=old[k] for k in ('identityHash','parent')):
            raise ValueError('cancellation_family_identity_conflict')
    result=[by_id[x] for x in sorted(ids)]
    for item in result:store.lineage(item)
    return result


def local_not_started(store, state):
    """取消持账本锁时在全部执行租约内取证；重启核对绝不调用本函数补造。"""
    if (state['schema']!='effectcraft-managed-task/v2' or state['state']!='planned' or state['steps']
            or state.get('worker') or state.get('workerHistory') or state.get('renderResumes') or state.get('processExit')
            or any(store.path(state['taskId']).parent.glob('lifecycle*.json'))):return False
    try:
        with ExitStack() as leases:
            for suffix in ('supervisor.lock','lifecycle.lock','lock'):
                leases.enter_context(load('platform_support').exclusive_lock(store.root/'leases'/(state['taskId']+'.'+suffix),timeout=0))
            state['cancellationLocal']={'schema':'effectcraft-cancellation-local/v1','taskId':state['taskId'],
                'identityHash':state['identityHash'],'kind':'not-started','at':time.time()}
            return True
    except TimeoutError:return False


def check_local(store,state):
    """检查既有未启动证明，不生成任何新的证明或进程结果。"""
    validate(state, check_state=False)
    if not state.get('cancellationLocal'):return False
    if (state.get('worker') or state['steps'] or state.get('workerHistory') or state.get('renderResumes')
            or state.get('processExit') or any(store.path(state['taskId']).parent.glob('lifecycle*.json'))):
        raise ValueError('cancellation_local_conflict')
    return True


def observed_stop(store, state, current_confirmed=False):
    """后代必须释放全部租约并核对原回执；终态字符串和PID均不是停止证明。"""
    if state['schema']!='effectcraft-managed-task/v2':return False,'legacy_task_read_only'
    try:
        with ExitStack() as leases:
            if not current_confirmed:
                for suffix in ('supervisor.lock','lifecycle.lock','lock'):
                    leases.enter_context(load('platform_support').exclusive_lock(store.root/'leases'/(state['taskId']+'.'+suffix),timeout=0))
            if check_local(store,state):return True,None
            if current_confirmed:return True,None
            path=store.lifecycle_path(state)
            if not path.is_file():return False,'missing_stop_evidence'
            value=load('commands').reply_json(path.read_text(encoding='utf-8'))
            if value.get('schema')!='effectcraft-process-lifecycle/v1' or value.get('status')!='stopped':return False,'lifecycle_not_stopped'
            load('task_store').exit_evidence(value.get('returncode'),value.get('ownership'))
            termination=state.get('termination',{})
            if termination.get('lifecycleSha256') and load('task_store').file_sha(path)!=termination['lifecycleSha256']:
                return False,'stop_receipt_changed'
            prior=state.get('cancellationFamily',{}).get('originalState',state['state'])
            if prior not in ('review_ready','completed') and state['state'] in ('running','resuming','cancel_requested','planned') and termination.get('status')!='confirmed':
                return False,'stop_not_settled'
            return True,None
    except TimeoutError:return False,'execution_lease_busy'
    except (ValueError,OSError,KeyError,TypeError):return False,'stop_evidence_invalid'


def record(state,members,pending,unknown,reasons):
    return {'schema':'effectcraft-cancellation-family/v1','taskId':state['taskId'],'identityHash':state['identityHash'],
        'originalState':state.get('cancellationFamily',{}).get('originalState',state['state']),
        'members':[{'taskId':x['taskId'],'identityHash':x['identityHash'],'parent':x['parent']} for x in members],
        'pendingTasks':sorted(pending),'unknownTasks':sorted(unknown),'reasons':reasons,
        'status':'waiting' if pending else 'unknown' if unknown else 'stopped','checkedAt':time.time()}


def update_locked(store, state, current_confirmed=False):
    """仅更新当前任务的任务族观察；每个后代经自己的原控制器结算。"""
    family=members_locked(store,state);pending=[];unknown=[];reasons={}
    for item in family:
        stopped,reason=observed_stop(store,item,current_confirmed and item['taskId']==state['taskId'])
        if not stopped:pending.append(item['taskId']);reasons[item['taskId']]=reason
        elif any(x['state']=='attempted' for x in item['steps']):unknown.append(item['taskId'])
    state['cancellationFamily']=record(state,family,pending,unknown,reasons)
    if pending:state['state']='cancel_requested'
    elif unknown:state['state']='reconciling'
    else:
        original=state['cancellationFamily']['originalState']
        state['state']=original if original in ('review_ready','completed') else 'cancelled'
    return state


def request_locked(store, task):
    """先落盘根取消与固定名单，再传播后代；中断后祖先约束仍阻止新调度。"""
    root=store.read(task)
    if root['schema']!='effectcraft-managed-task/v2':raise ValueError('legacy_task_read_only')
    family=members_locked(store,root)
    root.setdefault('cancellationRequestedAt',time.time())
    local_not_started(store,root)
    root['cancellationFamily']=record(root,family,[x['taskId'] for x in family],[],{x['taskId']:'cancellation_requested' for x in family})
    root['state']='cancel_requested'
    store.save(root)
    # 传播失败也不丢根取消意图；不依赖本进程内存继续阻止新后代。
    for item in family:
        if item['taskId']==task or item['schema']!='effectcraft-managed-task/v2':continue
        item=store.read(item['taskId']);item.setdefault('cancellationRequestedAt',root['cancellationRequestedAt'])
        local_not_started(store,item)
        if item['state'] in ('planned','running','resuming','reconciling','cancel_requested') or item.get('activeRevision'):item['state']='cancel_requested'
        store.save(item)
    family=members_locked(store,store.read(task))
    # 子树先观察，避免未启动的祖先忽略正在运行的孙任务。
    family.sort(key=lambda x:len(store.lineage(x)),reverse=True)
    for item in family:
        if item['schema']!='effectcraft-managed-task/v2':continue
        state=update_locked(store,store.read(item['taskId']));store.save(state)
    return store.read(task)
