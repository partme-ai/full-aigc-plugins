"""持久任务、只读核对、目标绑定审阅和有界修订。"""
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import copy
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
STATES = {'PLANNED','RUNNING','VERIFYING','AWAITING_REVIEW','COMPLETED','FAILED_OR_PARTIAL','UNKNOWN','BLOCKED'}


def module(name):
    path = ROOT / 'skills/lightcraft-use/scripts' / (name + '.py')
    spec = importlib.util.spec_from_file_location('upstream_' + name, path)
    result = importlib.util.module_from_spec(spec); spec.loader.exec_module(result)
    return result


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def atomic(path, value):
    path = Path(path); temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, prefix='.state-', delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary and temporary.exists(): temporary.unlink()


def inspect(task):
    task = Path(task)
    if task.is_symlink(): raise ValueError('task_symlink')
    path = task / 'state.json'
    if path.is_symlink() or not path.is_file(): raise ValueError('task_state_missing')
    try: state = module('command_gateway').strict_json(path.read_text())
    except (ValueError, OSError) as error: raise ValueError('task_state_corrupt') from error
    if not isinstance(state, dict): raise ValueError('task_state_invalid')
    if state.get('schemaVersion') != 1: return {'readOnly': True, 'compatible': False, 'legacy': state}
    module('command_gateway').validate_schema(json.loads((ROOT/'schemas/task-state.schema.json').read_text()),state)
    required = {'taskId','status','goal','goalSha256','plan','planSha256','originals','history','revision','maxRevisions','outputRoot'}
    if not required <= state.keys() or state['status'] not in STATES:
        raise ValueError('task_state_invalid')
    if digest(state['goal']) != state['goalSha256'] or digest(state['plan']) != state['planSha256']:
        raise ValueError('task_identity_mismatch')
    if 'batchScope' in state:
        if digest(state['batchScope'])!=state.get('batchScopeSha256'):raise ValueError('batch_scope_identity_mismatch')
        validate_batch(state['plan'],state['batchScope'],state.get('revisionScope'))
    return state


@contextmanager
def task_lock(task):
    """flock 生命周期排他；不以 PID 文件判断是否活动。"""
    task = Path(task)
    inspect(task)
    fd = os.open(task / '.controller.lock', os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w') as stream:
        try: fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise ValueError('task_controller_busy') from None
        try: yield
        finally: fcntl.flock(stream, fcntl.LOCK_UN)


def writable(task):
    state = inspect(task)
    if state.get('readOnly'): raise ValueError('legacy_task_read_only')
    return state


def save(task, state, event):
    state['updatedAt'] = now()
    state['history'].append({'event': event, 'at': state['updatedAt'], 'status': state['status'], 'revision': state['revision']})
    atomic(Path(task) / 'state.json', state)



def validate_batch(plan, scope, revision=None):
    """任务授权策略：约束明确 ID 与字段，不复制原生控件或结果解释。"""
    if not isinstance(scope,dict) or set(scope)!={'targetIds','observedIds','allowedFields'}:raise ValueError('batch_scope_invalid')
    def ids(values):
        if not isinstance(values,list) or not values or len(values)>200 or any(type(i) is not int or i<=0 for i in values) or len(set(values))!=len(values):raise ValueError('batch_ids_invalid')
        return set(values)
    def fields(values):
        if not isinstance(values,list) or not values or any(not isinstance(v,str) or not v for v in values) or len(set(values))!=len(values):raise ValueError('batch_fields_invalid')
        return set(values)
    targets=ids(scope['targetIds']);observed=ids(scope['observedIds']);allowed=fields(scope['allowedFields'])
    if not targets<=observed:raise ValueError('batch_targets_not_observed')
    if revision is not None:
        if not isinstance(revision,dict) or set(revision)!={'targetIds','allowedFields'}:raise ValueError('batch_revision_scope_required')
        revised=ids(revision['targetIds']);selected=fields(revision['allowedFields'])
        if not revised<=targets or not selected<=allowed:raise ValueError('batch_revision_outside_scope')
        targets=revised;allowed=selected
    module('command_gateway').validate_shape('lightcraft',plan)
    selected_id=None
    for step in plan['steps']:
        command=step['command'];params=step['params']
        if command=='develop.set':
            if set(params)!={'ids','values'} or not ids(params['ids'])<=targets:raise ValueError('batch_write_outside_scope')
            values=params['values']
            if not isinstance(values,dict) or not values or not set(values)<=allowed or any(type(v) not in (int,float) or not math.isfinite(v) for v in values.values()):raise ValueError('batch_fields_outside_scope')
        elif command=='library.select':
            if set(params)-{'ids','active'} or not ids(params.get('ids'))<=observed or type(params.get('active')) is not int or params['active'] not in params['ids']:raise ValueError('batch_selection_invalid')
            selected_id=params['active']
        elif command in ('photo.inspect','develop.get'):
            if set(params)!={'id'} or type(params['id']) is not int or params['id'] not in observed:raise ValueError('batch_read_identity_invalid')
        elif command=='app.export':
            if selected_id not in targets:raise ValueError('batch_export_requires_target_selection')
        elif command not in ('library.info','library.state','catalog.query','develop.controls','engine.commands'):
            raise ValueError('batch_command_not_allowed: '+command)
    return scope



def verify_batch_execution(state, receipt):
    """按照片身份核对真实回执的完整前后设置；缺失观测不能接受。"""
    if 'batchScope' not in state:return None
    steps=state['plan']['steps'];rows=receipt.get('steps',[])
    writes=[i for i,step in enumerate(steps) if step['command']=='develop.set']
    if not writes:return {'status':'NOT_RUN','reason':'no develop writes'}
    if len(rows)!=len(steps) or any(row.get('index')!=i or row.get('command')!=steps[i]['command'] or row.get('status')!='SUCCEEDED' for i,row in enumerate(rows)):raise ValueError('batch_steps_incomplete')
    before={};after={}
    for i,(step,row) in enumerate(zip(steps,rows)):
        if step['command']!='photo.inspect':continue
        result=row.get('native',{}).get('result',{});identifier=step['params']['id']
        if result.get('id')!=identifier or not isinstance(result.get('develop'),dict):raise ValueError('batch_photo_identity_invalid')
        source=result.get('source',{})
        if source.get('type')!='file' or source.get('path') not in state['originals']:raise ValueError('batch_original_identity_invalid')
        if i<min(writes):before[identifier]=result
        if i>max(writes):after[identifier]=result
    observed=set(state['batchScope']['observedIds'])
    if set(before)!=observed or set(after)!=observed:raise ValueError('batch_observation_incomplete')
    expected={i:copy.deepcopy(photo['develop']) for i,photo in before.items()}
    for i in writes:
        params=steps[i]['params']
        for identifier in params['ids']:
            for field,value in params['values'].items():
                cursor=expected[identifier];parts=field.split('.')
                for part in parts[:-1]:
                    if not isinstance(cursor,dict) or part not in cursor:raise ValueError('batch_field_not_observed')
                    cursor=cursor[part]
                if not isinstance(cursor,dict) or parts[-1] not in cursor:raise ValueError('batch_field_not_observed')
                cursor[parts[-1]]=value
    if any(before[i]['source']!=after[i]['source'] or not module('command_gateway').json_equal(expected[i],after[i]['develop']) for i in observed):raise ValueError('batch_settings_outside_scope')
    return {'status':'PASS','observedIds':state['batchScope']['observedIds'],'beforeSha256':digest(before),'afterSha256':digest(after),'automaticReplay':False}


def create(task, goal, plan, inputs, library=None, output_root=None, max_revisions=3, batch_scope=None):
    gateway = module('command_gateway')
    gateway.validate_shape('lightcraft', plan)
    if batch_scope is not None:validate_batch(plan,batch_scope)
    if type(max_revisions) is not int or not 0 <= max_revisions <= 20: raise ValueError('revision_limit_invalid')
    # 先按原输入拒绝文件链接，再统一父目录别名，避免 /tmp 与 /private/tmp 误判漂移。
    originals = {str(Path(path).resolve()): sha for path, sha in gateway.capture_inputs(inputs).items()}
    gateway.preflight_writes(plan, originals, output_root)
    state = {'schemaVersion': 1, 'taskId': str(uuid.uuid4()), 'status': 'PLANNED',
             'goal': goal, 'goalSha256': digest(goal), 'plan': plan, 'planSha256': digest(plan),
             'originals': originals, 'inputRoots': [str(Path(p).resolve()) for p in inputs],
             'library': str(Path(library).resolve()) if library else None,
             'outputRoot': str(Path(output_root).resolve()) if output_root else None,
             'revision': 0, 'maxRevisions': max_revisions, 'history': [], 'automaticReplay': False,
             'createdAt': now(), 'acceptance': {'execution':'NOT_RUN','persistence':'NOT_RUN','artifacts':'NOT_RUN','reopen':'NOT_RUN','visual':'NOT_RUN'}}
    if batch_scope is not None:state.update(batchScope=batch_scope,batchScopeSha256=digest(batch_scope))
    task = Path(task)
    gateway.validate_schema(json.loads((ROOT/'schemas/task-state.schema.json').read_text()),state)
    task.mkdir(parents=True, exist_ok=False)
    save(task, state, 'created')
    return state


def check_inputs(state):
    current = module('command_gateway').capture_inputs(state['inputRoots'])
    if current != state['originals']: raise ValueError('task_input_changed')


def run(task, runtime_home=None):
    """仅 PLANNED 可运行；持有任务锁，开始状态先落盘。"""
    with task_lock(task):
        state = writable(task)
        if state['status'] != 'PLANNED': raise ValueError('task_not_planned_no_replay')
        check_inputs(state)
        module('command_gateway').preflight_writes(state['plan'], state['originals'], state['outputRoot'])
        runs = Path(task) / 'runs'; runs.mkdir(exist_ok=True)
        run_dir = runs / str(uuid.uuid4())
        plan_path = Path(task) / 'current-plan.json'; atomic(plan_path, state['plan'])
        state.update(status='RUNNING', receiptPath=str((run_dir / 'receipt.json').absolute()))
        save(task, state, 'native_requested')
        argv = [sys.executable, '-I', '-B', str(ROOT / 'skills/lightcraft-use/scripts/commands.py'), 'run', str(plan_path), '--output', str(run_dir)]
        argv += ['--stop-file', str(Path(task)/'stop-request.json')]
        if runtime_home: argv += ['--runtime-home', str(runtime_home)]
        if state['library']: argv += ['--library', state['library']]
        if state['outputRoot']: argv += ['--output-root', state['outputRoot']]
        for path in state['inputRoots']: argv += ['--input', path]
        # 子命令独占原生监督；控制器不添加竞争的超时，不根据退出码重放。
        try:
            # 子包装器输出落盘，控制器 stdout 只返回一个状态 JSON，避免混入第二份回执。
            with (runs/(run_dir.name+'.stdout.log')).open('wb') as stdout, (runs/(run_dir.name+'.stderr.log')).open('wb') as stderr:
                subprocess.run(argv, check=False, stdout=stdout, stderr=stderr)
        except (OSError, KeyboardInterrupt) as error:
            state.update(status='UNKNOWN', controllerError=str(error)); save(task,state,'controller_interrupted'); return state
        if not Path(state['receiptPath']).is_file():
            state.update(status='UNKNOWN', controllerError='execution_receipt_missing')
        else:
            try:
                read = module('command_gateway').read_receipt(state['receiptPath'])
            except (OSError,ValueError) as error:
                state.update(status='UNKNOWN', controllerError='execution_receipt_invalid: '+str(error))
                save(task,state,'execution_recorded')
                return state
            receipt = read['receipt']
            if not read['compatible'] or receipt.get('planSha256') != state['planSha256']:
                state.update(status='UNKNOWN', controllerError='execution_contract_mismatch')
            else:
                state['runId'] = receipt.get('runId')
                state['acceptance']['execution'] = receipt['status']
                state['status'] = 'VERIFYING' if receipt['status'] == 'NATIVE_EXIT_ZERO_REVIEW_REQUIRED' else 'FAILED_OR_PARTIAL' if receipt['status']=='FAILED_OR_PARTIAL' else 'UNKNOWN'
                if state['status']=='VERIFYING' and 'batchScope' in state:
                    try:state['batchObservation']=verify_batch_execution(state,receipt)
                    except (ValueError,KeyError,TypeError) as error:state.update(status='UNKNOWN',controllerError=str(error))
        save(task, state, 'execution_recorded')
        return state


def reconcile(task):
    """只读证据核对，不推进状态、不启动 CLI、不仅凭 PID 认定结束。"""
    state = inspect(task)
    if state.get('readOnly'): return state
    report = {'readOnly': True, 'status': state['status'], 'automaticReplay': False, 'processIdentity': 'UNCONFIRMED',
              'libraryReopen': 'NOT_RUN', 'receipt': None, 'artifacts': [], 'differences': []}
    try: check_inputs(state)
    except (OSError, ValueError) as error: report['differences'].append(str(error))
    path = state.get('receiptPath')
    if path and Path(path).is_file():
        try:
            read = module('command_gateway').read_receipt(path); report['receipt'] = read
            if not read['compatible'] or read['receipt'].get('planSha256') != state['planSha256']:
                report['differences'].append('execution_contract_mismatch')
            process=read['receipt'].get('process')
            start_file=Path(path).parent/'logs/process-start.json'
            if not process and start_file.is_file():
                process=module('command_gateway').strict_json(start_file.read_text())
            if isinstance(process,dict):
                report['processFacts']=process
                pid=process.get('pid')
                if type(pid) is int and pid>0 and process.get('processIdentity'):
                    probe=subprocess.run(['ps','-ww','-p',str(pid),'-o','lstart=','-o','command='],capture_output=True,text=True,timeout=2)
                    report['processIdentity']=('MATCHING_ACTIVE_PROCESS' if probe.returncode==0 and probe.stdout.strip()==process['processIdentity'] else 'ABSENT_OR_DIFFERENT_NO_DESCENDANT_PROOF')
        except (OSError, ValueError, subprocess.SubprocessError) as error: report['differences'].append(str(error))
    elif state['status'] != 'PLANNED': report['differences'].append('execution_receipt_missing')
    for item in state.get('artifacts', []):
        path = Path(item['path'])
        report['artifacts'].append({'path':str(path),'currentSha256':module('artifacts').sha(path) if path.is_file() else None,'expectedSha256':item['sha256']})
    # 独立重开可能写照片库，因此此只读 API 不假装执行了重开。
    report['reopenEvidence'] = state.get('reopenEvidence')
    if state['library']:
        try:report['libraryCurrentSha256']=module('command_gateway').capture_inputs([state['library']])
        except (OSError,ValueError) as error:report['differences'].append('library_identity: '+str(error))
    return report


def stop(task):
    """调度停止事实可记录；不对未证明身份的 PID 发送信号。"""
    writable(task)
    request={'at':now(),'localSchedulingStopped':True,'nativeTermination':'UNCONFIRMED'}
    # 运行控制器持锁时仍可发布停止请求；只有监督器能终止它实际启动的进程组。
    atomic(Path(task)/'stop-request.json',request)
    try:
        with task_lock(task):
            state=writable(task);state['stopRequest']=request
            if state['status'] in ('PLANNED','RUNNING'):state['status']='UNKNOWN'
            save(task,state,'stop_requested')
            return state
    except ValueError as error:
        if str(error)!='task_controller_busy':raise
        return {'stopRequest':request,'status':'REQUESTED','automaticReplay':False}


def remaining(task):
    state = writable(task); check_inputs(state)
    if not state.get('receiptPath') or not Path(state['receiptPath']).is_file(): raise ValueError('remaining_receipt_missing')
    read = module('command_gateway').read_receipt(state['receiptPath'])
    if not read['compatible']: raise ValueError('remaining_requires_current_receipt')
    receipt = read['receipt']
    if (receipt.get('runId')!=state.get('runId')
            or receipt.get('inputSha256')!=state['originals']
            or receipt.get('skillResourceSha256')!=module('command_gateway').capture_resources(ROOT/'skills/lightcraft-use/scripts')):
        raise ValueError('remaining_identity_mismatch')
    if receipt.get('planSha256') != state['planSha256'] or receipt.get('status') != 'FAILED_OR_PARTIAL' or not receipt.get('protocolComplete'):
        raise ValueError('remaining_requires_confirmed_execution')
    rows = receipt.get('steps', [])
    if len(rows)!=len(state['plan']['steps']) or any(row['index']!=index or row['command']!=state['plan']['steps'][index]['command'] for index,row in enumerate(rows)):
        raise ValueError('remaining_identity_step_mismatch')
    indexes = [r['index'] for r in rows if r['status'] == 'NOT_EXECUTED']
    if not indexes: raise ValueError('no_confirmed_remaining_steps')
    # 独立会话必须显式恢复选择；不要直接提交这个建议片段。
    return {'schemaVersion':1, 'sourceRunId':receipt['runId'], 'sourcePlanSha256':state['planSha256'],
            'proposal': {'domain':'lightcraft','steps':[state['plan']['steps'][i] for i in indexes]},
            'requiresSessionPreconditions':True,'requiresAuthorizationReview':True,'automaticReplay':False}


def review_request(task, candidates, settings, rubric_version, reopen_evidence=None):
    with task_lock(task):
        state = writable(task); check_inputs(state)
        if state['status'] != 'VERIFYING': raise ValueError('review_requires_verified_execution')
        if not isinstance(settings,dict) or not isinstance(rubric_version,str) or not rubric_version: raise ValueError('review_settings_and_rubric_required')
        execution = module('command_gateway').read_receipt(state.get('receiptPath',''))
        receipt = execution['receipt']
        if (not execution['compatible'] or receipt.get('runId')!=state.get('runId')
                or receipt.get('planSha256')!=state['planSha256']
                or receipt.get('status')!='NATIVE_EXIT_ZERO_REVIEW_REQUIRED'
                or receipt.get('skillResourceSha256')!=module('command_gateway').capture_resources(ROOT/'skills/lightcraft-use/scripts')):
            raise ValueError('review_execution_identity_mismatch')
        observed=[r.get('native',{}).get('result') for r in receipt.get('steps',[]) if r.get('command')=='develop.get' and r.get('status')=='SUCCEEDED']
        if 'batchScope' not in state and settings not in observed: raise ValueError('review_settings_not_observed')
        photos=[r.get('native',{}).get('result') for r in receipt.get('steps',[]) if r.get('command')=='photo.inspect' and r.get('status')=='SUCCEEDED']
        if not photos or any(not isinstance(p,dict) or 'id' not in p or 'source' not in p for p in photos):raise ValueError('review_photo_identity_not_observed')
        if 'batchScope' in state:
            if state.get('batchObservation',{}).get('status')!='PASS':raise ValueError('batch_review_observation_required')
            latest={p['id']:p for p in photos};targets=state['batchScope']['targetIds']
            expected={str(i):latest[i]['develop'] for i in targets}
            if not module('command_gateway').json_equal(settings,expected):raise ValueError('batch_review_settings_mismatch')
            photos=[latest[i] for i in targets]
        photo_identity=[{'id':p['id'],'source':p['source']} for p in photos]
        if not state['outputRoot'] or not candidates: raise ValueError('review_candidates_required')
        facts = []
        for candidate in candidates:
            fact = module('artifacts').verify(candidate['path'], state['outputRoot'], candidate.get('expected'))
            if fact['technicalStatus'] != 'PASS': raise ValueError('artifact_target_mismatch: '+json.dumps(fact['differences']))
            facts.append(fact)
        binding = {'goalSha256':state['goalSha256'],'originals':state['originals'],'candidates':facts,
                   'settings':settings,'settingsSha256':digest(settings),'photos':photo_identity,'rubricVersion':rubric_version,'revision':state['revision']}
        request = {'schemaVersion':1,'requestId':str(uuid.uuid4()),'taskId':state['taskId'],'binding':binding,'bindingSha256':digest(binding)}
        state.update(status='AWAITING_REVIEW', reviewRequest=request, artifacts=facts, reopenEvidence=reopen_evidence)
        state['acceptance'].update(execution=receipt['status'],artifacts='PASS',visual='NOT_RUN')
        atomic(Path(task)/('review-request-'+str(state['revision'])+'.json'),request)
        save(task,state,'review_requested')
        return request


def review(task, receipt):
    with task_lock(task):
        module('command_gateway').validate_schema(json.loads((ROOT/'schemas/review-receipt.schema.json').read_text()),receipt)
        state = writable(task); check_inputs(state)
        request = state.get('reviewRequest')
        if state['status'] != 'AWAITING_REVIEW' or not request: raise ValueError('review_not_requested')
        for fact in state['artifacts']:
            if module('artifacts').sha(fact['path']) != fact['sha256']: raise ValueError('candidate_changed_review_expired')
        if (receipt.get('schemaVersion')!=1 or receipt.get('requestId')!=request['requestId']
                or receipt.get('bindingSha256')!=request['bindingSha256']
                or receipt.get('source') not in ('human','host-model') or not receipt.get('reviewer')
                or receipt.get('verdict') not in ('PASS','FAIL') or not receipt.get('observations')):
            raise ValueError('review_receipt_invalid')
        if state.get('reviewReceipt'): raise ValueError('duplicate_review_receipt')
        state['reviewReceipt']=receipt
        state['acceptance']['visual']=receipt['verdict']
        save(task,state,'review_recorded')
        return state


def revise(task, plan, issue, scope):
    with task_lock(task):
        state = writable(task); check_inputs(state)
        if state['status'] != 'AWAITING_REVIEW' or state.get('reviewReceipt',{}).get('verdict') != 'FAIL': raise ValueError('revision_requires_failed_review')
        if not issue or not scope: raise ValueError('revision_scope_required')
        if state['revision']>=state['maxRevisions']: raise ValueError('revision_limit_reached')
        module('command_gateway').validate_shape('lightcraft',plan)
        if 'batchScope' in state:validate_batch(plan,state['batchScope'],scope)
        module('command_gateway').preflight_writes(plan,state['originals'],state['outputRoot'])
        state.setdefault('revisions',[]).append({'revision':state['revision'],'request':state['reviewRequest'],'receipt':state['reviewReceipt'],'issue':issue,'scope':scope})
        state.update(status='PLANNED',plan=plan,planSha256=digest(plan),revision=state['revision']+1)
        if 'batchScope' in state:state['revisionScope']=scope
        for key in ['reviewRequest','reviewReceipt','artifacts','receiptPath','runId','reopenEvidence','batchObservation']:
            state.pop(key,None)
        state['acceptance']={k:'NOT_RUN' for k in state['acceptance']}
        save(task,state,'revision_planned')
        return state


def deliver(task):
    with task_lock(task):
        state = writable(task); check_inputs(state)
        if state['status']!='AWAITING_REVIEW' or state['acceptance']['visual']!='PASS' or not state.get('reviewReceipt'): raise ValueError('delivery_visual_review_required')
        for fact in state['artifacts']:
            if module('artifacts').sha(fact['path']) != fact['sha256']: raise ValueError('candidate_changed_review_expired')
        reopen = state.get('reopenEvidence') or {}
        # 重开证据必须引用独立 run，且同一库与当前设置；用户 JSON 声明不能替代回执。
        evidence_path = reopen.get('receiptPath')
        if not evidence_path: raise ValueError('delivery_reopen_receipt_required')
        read = module('command_gateway').read_receipt(evidence_path)
        evidence = read['receipt']
        if (not read['compatible'] or evidence.get('runId') == state.get('runId')
                or evidence.get('libraryPath') != state['library']
                or evidence.get('status') != 'NATIVE_EXIT_ZERO_REVIEW_REQUIRED'
                or evidence.get('skillResourceSha256')!=module('command_gateway').capture_resources(ROOT/'skills/lightcraft-use/scripts')):
            raise ValueError('delivery_reopen_identity_mismatch')
        observed = [r.get('native',{}).get('result') for r in evidence.get('steps',[]) if r.get('command')=='develop.get' and r.get('status')=='SUCCEEDED']
        if 'batchScope' not in state and state['reviewRequest']['binding']['settings'] not in observed: raise ValueError('delivery_reopen_settings_mismatch')
        photos=[r.get('native',{}).get('result') for r in evidence.get('steps',[]) if r.get('command')=='photo.inspect' and r.get('status')=='SUCCEEDED']
        if 'batchScope' in state:
            latest={p['id']:p for p in photos};targets=state['batchScope']['targetIds']
            if not set(targets)<=set(latest) or not module('command_gateway').json_equal({str(i):latest[i].get('develop') for i in targets},state['reviewRequest']['binding']['settings']):raise ValueError('batch_delivery_settings_mismatch')
            photos=[latest[i] for i in targets]
        identities=[{'id':p['id'],'source':p['source']} for p in photos if isinstance(p,dict) and 'id' in p and 'source' in p]
        if sorted(identities,key=digest)!=sorted(state['reviewRequest']['binding']['photos'],key=digest):raise ValueError('delivery_reopen_photo_identity_mismatch')
        if not state['library'] or evidence.get('libraryAfterSha256')!=module('command_gateway').capture_inputs([state['library']]):raise ValueError('delivery_library_changed_after_reopen')
        info=[r.get('native',{}).get('result') for r in evidence.get('steps',[]) if r.get('command')=='library.info' and r.get('status')=='SUCCEEDED']
        if not info or any(not isinstance(r,dict) or r.get('persistent') is not True or r.get('unsavedOps')!=0 for r in info):raise ValueError('delivery_library_persistence_unconfirmed')
        state['acceptance'].update(reopen='PASS',persistence='PASS')
        state['status']='COMPLETED'
        save(task,state,'delivered')
        atomic(Path(task)/'delivery.json',{'schemaVersion':1,'taskId':state['taskId'],'runId':state['runId'],'acceptance':state['acceptance'],'artifacts':state['artifacts'],'reviewReceipt':state['reviewReceipt'],'reopenEvidence':reopen,'unverified':['other RAW variants','other platforms','remote CI']})
        return state
