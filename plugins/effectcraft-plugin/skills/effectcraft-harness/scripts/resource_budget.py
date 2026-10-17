"""根任务共享资源账本：预占帧/解码量与单调编码字节高水位。"""
import re

LIMITS={'frames':10000,'decodedBytes':64*1024**3,'encodedBytes':2*1024**3}


def empty():
    return {'schema':'effectcraft-resource-budget/v1','limits':dict(LIMITS),'entries':{}}


def validate(value):
    if (not isinstance(value,dict) or value.get('schema')!='effectcraft-resource-budget/v1'
            or value.get('limits')!=LIMITS or not isinstance(value.get('entries'),dict)):
        raise ValueError('resource_budget_invalid')
    for task,entry in value['entries'].items():
        if not isinstance(task,str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,95}',task):
            raise ValueError('resource_budget_invalid')
        if (not isinstance(entry,dict) or set(entry)-{'segmentAttempts','commandFrames','reviewFrames'}!= {'frames','decodedBytes','encodedBytes','bindingHash'}
                or not isinstance(entry['bindingHash'],str) or not re.fullmatch('[a-f0-9]{64}',entry['bindingHash'])
                or any(type(entry[k]) is not int or entry[k]<0 for k in LIMITS)):
            raise ValueError('resource_budget_invalid')
        commands=entry.get('commandFrames',{})
        if not isinstance(commands,dict):raise ValueError('resource_budget_invalid')
        for operation,row in commands.items():
            if (not isinstance(operation,str) or not re.fullmatch('[a-f0-9]{64}',operation)
                    or not isinstance(row,dict) or set(row)!={'frames','decodedBytes'}
                    or type(row['frames']) is not int or row['frames']!=1
                    or type(row['decodedBytes']) is not int or row['decodedBytes']<=0):raise ValueError('resource_budget_invalid')
        reviews=entry.get('reviewFrames',{})
        if not isinstance(reviews,dict):raise ValueError('resource_budget_invalid')
        for attempt,row in reviews.items():
            if (not isinstance(attempt,str) or not re.fullmatch('[a-f0-9]{64}',attempt) or not isinstance(row,dict) or set(row)!={'frames','decodedBytes'} or type(row['frames']) is not int or row['frames']!=1 or type(row['decodedBytes']) is not int or row['decodedBytes']<=0):raise ValueError('resource_budget_invalid')
        attempts=entry.get('segmentAttempts',{})
        if not isinstance(attempts,dict):raise ValueError('resource_budget_invalid')
        identities=set()
        for segment,rows in attempts.items():
            if not isinstance(segment,str) or not re.fullmatch(r'segment_[0-9]{5}',segment) or not isinstance(rows,list) or not rows:
                raise ValueError('resource_budget_invalid')
            for row in rows:
                if (not isinstance(row,dict) or set(row)!={'attemptId','frames','decodedBytes'}
                        or not isinstance(row['attemptId'],str) or not re.fullmatch('[a-f0-9]{64}',row['attemptId'])
                        or row['attemptId'] in identities
                        or any(type(row[k]) is not int or row[k]<=0 for k in ('frames','decodedBytes'))
                        or any(row[k]!=rows[0][k] for k in ('frames','decodedBytes'))):
                    raise ValueError('resource_budget_invalid')
                identities.add(row['attemptId'])
        if any(sum(rows[0][key] for rows in attempts.values())>entry[key] for key in ('frames','decodedBytes')):
            raise ValueError('resource_attempt_coverage_invalid')
    return value


def check(value):
    validate(value)
    used=usage(value)
    if any(used[key]>limit for key,limit in LIMITS.items()):
        raise ValueError('resource_budget_exceeded')


def usage(value):
    """首段尝试包含在计划预占内；额外原生尝试追加帧数和解码量。"""
    validate(value)
    used={key:sum(entry[key] for entry in value['entries'].values()) for key in LIMITS}
    for entry in value['entries'].values():
        for key in ('frames','decodedBytes'):
            used[key]+=max(0,sum(row[key] for row in entry.get('commandFrames',{}).values())-entry[key])
        for row in entry.get('reviewFrames',{}).values():
            for key in ('frames','decodedBytes'):used[key]+=row[key]
        for rows in entry.get('segmentAttempts',{}).values():
            for row in rows[1:]:
                for key in ('frames','decodedBytes'):used[key]+=row[key]
    return used


def reserve_command(store, task, operation, decoded_bytes):
    """PNG原生调用前记账；预占与实际尝试取覆盖上界，不重复收费。"""
    if (not isinstance(operation,str) or not re.fullmatch('[a-f0-9]{64}',operation)
            or type(decoded_bytes) is not int or decoded_bytes<=0):raise ValueError('resource_attempt_invalid')
    row={'frames':1,'decodedBytes':decoded_bytes}
    with store.lock():
        state=store.read(task);store.allowed(state);root=store.lineage(state)[-1]
        if state['identity']['mode'] not in ('commands','desktop'):raise ValueError('resource_attempt_mode')
        value=root['resources'];entry=value['entries'].get(task)
        if entry is None:raise ValueError('resource_reservation_missing')
        records=entry.setdefault('commandFrames',{})
        if operation in records:
            if records[operation]!=row:raise ValueError('resource_attempt_conflict')
            return value
        records[operation]=row;validate(value);store.save(root);check(value)
        return value


def reserve_segment(store, task, segment, attempt, frames, decoded_bytes):
    """原生调用前登记独立尝试；失败与预算越界事实均跨重启保留。"""
    if (not isinstance(segment,str) or not re.fullmatch(r'segment_[0-9]{5}',segment)
            or not isinstance(attempt,str) or not re.fullmatch('[a-f0-9]{64}',attempt)
            or any(type(v) is not int or v<=0 for v in (frames,decoded_bytes))):
        raise ValueError('resource_attempt_invalid')
    row={'attemptId':attempt,'frames':frames,'decodedBytes':decoded_bytes}
    with store.lock():
        state=store.read(task);store.allowed(state);root=store.lineage(state)[-1]
        value=root['resources'];entry=value['entries'].get(task)
        if entry is None:raise ValueError('resource_reservation_missing')
        attempts=entry.setdefault('segmentAttempts',{})
        for key,rows in attempts.items():
            for prior in rows:
                if prior['attemptId']==attempt:
                    if key!=segment or prior!=row:raise ValueError('resource_attempt_conflict')
                    return value
        rows=attempts.setdefault(segment,[])
        if rows and any(rows[0][key]!=row[key] for key in ('frames','decodedBytes')):
            raise ValueError('resource_attempt_conflict')
        rows.append(row)
        validate(value)
        store.save(root)
        check(value)
        return value


def check_reference(state, value):
    entry=value['entries'].get(state['taskId']);reference=state.get('resourceReservation')
    expected={key:entry[key] for key in ('frames','decodedBytes','bindingHash')} if entry else None
    if reference!=expected:raise ValueError('resource_reservation_invalid')


def check_family(store, root):
    """持锁核对整个任务族，删除子记录不能给新兄弟任务释放已用预算。"""
    family={}
    for state in store.all():
        if store.lineage(state)[-1]['taskId']==root['taskId']:
            family[state['taskId']]=state
            check_reference(state,root['resources'])
            if state.get('resourceObservation',{}).get('status')=='UNKNOWN':raise ValueError('resource_observation_unknown')
    if set(root['resources']['entries'])-family.keys():
        raise ValueError('resource_reservation_invalid')


def reserve(store, task, amounts, binding):
    if (set(amounts)!= {'frames','decodedBytes'} or any(type(v) is not int or v<0 for v in amounts.values())
            or not isinstance(binding,str) or not re.fullmatch('[a-f0-9]{64}',binding)):
        raise ValueError('resource_reservation_invalid')
    with store.lock():
        state=store.read(task);store.allowed(state);root=store.lineage(state)[-1]
        value=root.get('resources')
        if value is None:raise ValueError('legacy_resource_budget_missing')
        validate(value)
        entry=dict(amounts,encodedBytes=0,bindingHash=binding)
        prior=value['entries'].get(task)
        if prior:
            if any(prior[k]!=entry[k] for k in ('frames','decodedBytes','bindingHash')):
                raise ValueError('resource_binding_conflict')
            return value
        value['entries'][task]=entry
        check(value) # 不足时不写部分预占；已有失败尝试仍保留。
        reference={key:entry[key] for key in ('frames','decodedBytes','bindingHash')}
        if root['taskId']==task:root['resourceReservation']=reference
        else:state['resourceReservation']=reference
        store.save(root)
        if root['taskId']!=task:store.save(state)
        return value


def observe(store, task, encoded_bytes):
    if type(encoded_bytes) is not int or encoded_bytes<0:raise ValueError('resource_observation_invalid')
    with store.lock():
        return observe_locked(store,store.read(task),encoded_bytes)


def observe_locked(store, state, encoded_bytes):
    if type(encoded_bytes) is not int or encoded_bytes<0:raise ValueError('resource_observation_invalid')
    root=store.lineage(state)[-1];value=root.get('resources')
    if value is None:raise ValueError('legacy_resource_budget_missing')
    validate(value);check_reference(state,value)
    if state['taskId'] not in value['entries']:raise ValueError('resource_reservation_missing')
    entry=value['entries'][state['taskId']];entry['encodedBytes']=max(entry['encodedBytes'],encoded_bytes)
    store.save(root) # 越界事实先落盘；重启或删除产物不能重新取得预算。
    check(value)
    return value


def reserve_review(store,task,attempt,decoded_bytes):
    """原生审阅的实际渲染追加到根任务族预算，越界事实不撤销。"""
    if not isinstance(attempt,str) or not re.fullmatch('[a-f0-9]{64}',attempt) or type(decoded_bytes) is not int or decoded_bytes<=0:raise ValueError('resource_attempt_invalid')
    row={'frames':1,'decodedBytes':decoded_bytes}
    with store.lock():
        state=store.read(task);store.allowed(state);root=store.lineage(state)[-1];value=root['resources'];entry=value['entries'].get(task)
        if entry is None:raise ValueError('resource_reservation_missing')
        records=entry.setdefault('reviewFrames',{})
        if attempt in records:
            if records[attempt]!=row:raise ValueError('resource_attempt_conflict')
            check(value);return value
        records[attempt]=row;validate(value);store.save(root);check(value);return value
