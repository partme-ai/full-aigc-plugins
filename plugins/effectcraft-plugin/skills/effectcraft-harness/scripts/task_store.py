"""持久化任务身份；先登记尝试，再发出副作用，未知结果不自动重放。"""
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import tempfile
import time
import uuid


def load(name):
    spec = importlib.util.spec_from_file_location('craft_task_' + name, Path(__file__).with_name(name + '.py'))
    value = importlib.util.module_from_spec(spec); spec.loader.exec_module(value)
    return value


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise ValueError('invalid_file: ' + str(path))
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def atomic_json(path, value):
    path = Path(path)
    if path.is_symlink():
        raise ValueError('state_symlink')
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.state-', delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(canonical(value) + b'\n'); stream.flush(); os.fsync(stream.fileno())
    try:
        temporary.replace(path)
        if os.name != 'nt':
            fd = os.open(path.parent, os.O_RDONLY)
            try: os.fsync(fd)
            finally: os.close(fd)
    finally:
        temporary.unlink(missing_ok=True)


def exit_evidence(returncode, ownership=None):
    """区分已核对业务退出与强制组停止；不把持有者退出写成已知业务结果。"""
    if type(returncode) is not int:raise ValueError('worker_exit_not_confirmed')
    source='legacy-business-result';verified=True
    if ownership is not None:
        if (not isinstance(ownership,dict) or ownership.get('schema')!='effectcraft-posix-group-lease/v1'
                or type(ownership.get('workerResultVerified')) is not bool):raise ValueError('process_exit_evidence_invalid')
        verified=ownership['workerResultVerified'];source=ownership.get('exitCodeSource')
        if verified:
            if (source!='business-result' or type(ownership.get('workerReturncode')) is not int
                    or ownership['workerReturncode']!=returncode):raise ValueError('process_exit_evidence_invalid')
        elif (source!='group-holder-forced-stop' or ownership.get('workerReturncode') is not None
                or ownership.get('forcedDrain') is not True or returncode>=0
                or type(ownership.get('gateReturncode')) is not int
                or ownership['gateReturncode']!=returncode):raise ValueError('process_exit_evidence_invalid')
    return {'schema':'effectcraft-managed-process-exit/v1','returncode':returncode,'source':source,
            'workerResultVerified':verified,'observedAt':time.time()}


def validate_exit_record(state):
    """已版本化退出记录与业务退出字段须一致；历史无该字段的记录保持兼容。"""
    if 'processExit' not in state:return
    value=state['processExit']
    if (not isinstance(value,dict) or set(value)!={'schema','returncode','source','workerResultVerified','observedAt'}
            or value['schema']!='effectcraft-managed-process-exit/v1' or type(value['returncode']) is not int
            or type(value['workerResultVerified']) is not bool or type(value['observedAt']) not in (int,float)
            or not math.isfinite(value['observedAt']) or value['observedAt']<=0):raise ValueError('process_exit_record_invalid')
    if value['workerResultVerified']:
        if (value['source'] not in ('legacy-business-result','business-result')
                or type(state.get('workerExitCode')) is not int or state['workerExitCode']!=value['returncode']
                or state.get('workerExitObservedAt')!=value['observedAt']):raise ValueError('process_exit_record_invalid')
    elif (value['source']!='group-holder-forced-stop' or value['returncode']>=0
            or state.get('workerExitCode') is not None or state.get('workerExitObservedAt') is not None):
        raise ValueError('process_exit_record_invalid')


ACTIVE = {'planned', 'resuming', 'running', 'reconciling', 'cancel_requested'}
STATES = ACTIVE | {'review_ready', 'completed', 'failed', 'cancelled'}


class Store:
    """同一受管理根中串行更新身份账本；未完成会话永远保留。"""
    def __init__(self, root):
        path = Path(root).expanduser().absolute()
        if path.is_symlink():
            raise ValueError('state_root_symlink')
        self.root = path.resolve()

    def path(self, task):
        if not isinstance(task, str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,95}', task):
            raise ValueError('invalid_task_id')
        path = self.root / 'tasks' / task / 'state.json'
        if any(p.is_symlink() for p in (path, path.parent, path.parent.parent)):
            raise ValueError('state_symlink')
        return path

    def lock(self):
        return load('platform_support').exclusive_lock(self.root/'store.lock')

    def read(self, task):
        path = self.path(task)
        try:
            if path.stat().st_size > 16 * 1024 * 1024:
                raise ValueError('state_too_large')
            value = load('commands').reply_json(path.read_text(encoding='utf-8'))
            if not isinstance(value, dict) or value.get('schema') not in ('effectcraft-managed-task/v1','effectcraft-managed-task/v2') or value.get('taskId') != task or value.get('state') not in STATES:
                raise ValueError('shape')
            for field in ('createdAt', 'deadline'):
                if type(value[field]) not in (int, float) or not math.isfinite(value[field]):
                    raise ValueError('invalid time')
            if value['identity']['planHash'] != digest(value['plan']) or value['identityHash'] != digest(value['identity']):
                raise ValueError('identity_mismatch')
            if value['schema']=='effectcraft-managed-task/v2' and value['workKey']!=digest({k:v for k,v in value['identity'].items() if k not in ('authorization','runtimeSha256','runtimeBinding')}):
                raise ValueError('work_identity_mismatch')
            if 'runtimeBinding' in value['identity']:load('runtime_binding').validate_binding(value['identity']['runtimeBinding'])
            if not isinstance(value['steps'], list) or not isinstance(value['budget'], dict):
                raise ValueError('invalid records')
            validate_exit_record(value)
            load('cancellation').validate(value)
            if 'resources' in value:load('resource_budget').validate(value['resources'])
            if 'resourceLocations' in value:load('resource_meter').validate(value['resourceLocations'],value['output'])
            if 'resourceObservation' in value:load('resource_meter').validate_observation(value['resourceObservation'])
            load('orphan_segments').validate(value)
            if value['budget']['revisions'] < 0 or value['budget']['maxRevisions'] != 2:
                raise ValueError('invalid budget')
            if any(type(value['budget'][k]) is not int or value['budget'][k]<0 for k in ('revisions','stagnant')) or value['budget']['revisions']>2:
                raise ValueError('invalid budget')
            if value['deadline']>value['createdAt']+1800.01 or value.get('parent')==task:
                raise ValueError('invalid task bound')
            ids=set()
            for step in value['steps']:
                if step['state'] not in ('attempted','succeeded') or step['id'] in ids:
                    raise ValueError('invalid operation')
                ids.add(step['id'])
                if not re.fullmatch('[a-f0-9]{64}',step['argumentsHash']):
                    raise ValueError('invalid operation digest')
                if step['state']=='succeeded' and not re.fullmatch('[a-f0-9]{64}',step['resultHash']):
                    raise ValueError('invalid receipt digest')
                if value['schema']=='effectcraft-managed-task/v2' and not re.fullmatch('[a-f0-9]{32}',step['id']):
                    raise ValueError('invalid_operation_id')
            if value['schema']=='effectcraft-managed-task/v2':self._validate_receipts(task,value['steps'],path.parent/'receipts')
            return value
        except (OSError, KeyError, TypeError, ValueError) as error:
            raise ValueError('state_invalid: ' + str(error)) from error

    def _validate_receipts(self, task, steps, directory):
        """保全未结算回执，但拒绝无归属、版本或原调用不匹配的材料。"""
        if directory.is_symlink():raise ValueError('receipt_symlink')
        receipts={}
        if directory.exists():
            if not directory.is_dir():raise ValueError('receipt_directory_invalid')
            expected={step['id']+'.json' for step in steps}
            for path in directory.iterdir():
                if path.is_symlink() or not path.is_file():raise ValueError('receipt_entry_invalid')
                if path.name not in expected:raise ValueError('orphan_receipt')
                receipts[path.name]=path
        for step in steps:
            path=receipts.get(step['id']+'.json')
            if path is None:
                if step['state']=='succeeded':raise ValueError('receipt_missing')
                continue
            receipt=load('commands').reply_json(path.read_text(encoding='utf-8'))
            if (receipt['schema']!='effectcraft-step-result/v1' or receipt['operationId']!=step['id']
                    or receipt['taskId']!=task or receipt['argumentsHash']!=step['argumentsHash']
                    or 'result' not in receipt):raise ValueError('receipt_mismatch')
            if step['state']=='succeeded' and digest(receipt['result'])!=step['resultHash']:
                raise ValueError('receipt_mismatch')
            # attempted 的真实回执不自动结算；未知编辑仍由原任务显式核对。

    def save(self, state):
        state['updatedAt'] = time.time()
        atomic_json(self.path(state['taskId']), state)
        return state

    def all(self):
        directory = self.root/'tasks'
        if not directory.exists():
            return []
        # 目录存在却没有状态也是故障，禁止通过忽略它绕过占用。
        return [self.read(p.name) for p in sorted(directory.iterdir()) if p.is_dir()]

    def create(self, task, *, plan, output, runtime_sha, inputs, source, mode,
               authorization, seconds=1800, parent=None, runtime_binding=None):
        if type(seconds) not in (int, float) or not math.isfinite(seconds) or not 0 < seconds <= 1800:
            raise ValueError('invalid_deadline')
        if not re.fullmatch('[a-f0-9]{64}', runtime_sha):
            raise ValueError('runtime_identity_required')
        output = str(Path(output).absolute().parent.resolve()/Path(output).name)
        source = str(Path(source).resolve()) if source else None
        identity = {'planHash':digest(plan), 'inputHashes':inputs,
                    'project':source, 'projectRevision':file_sha(source) if source else None,
                    'runtimeSha256':runtime_sha, 'mode':mode, 'authorization':authorization}
        if runtime_binding is not None:
            load('runtime_binding').validate_binding(runtime_binding);identity['runtimeBinding']=runtime_binding
        work_key = digest({k:v for k,v in identity.items() if k not in ('authorization','runtimeSha256','runtimeBinding')})
        with self.lock():
            path = self.path(task)
            if path.parent.exists():
                raise ValueError('task_exists; inspect original task')
            states = self.all()
            for prior in states:
                if prior['state'] not in ACTIVE:
                    continue
                if prior['workKey'] == work_key:
                    raise ValueError('reconciliation_required: ' + prior['taskId'])
                if prior['output'] == output or (source and prior['identity']['project'] == source):
                    raise ValueError('resource_busy: ' + prior['taskId'])
            now = time.time(); deadline = now + seconds
            if parent:
                ancestor = self.read(parent)
                self.allowed(ancestor)
                deadline = min(deadline, ancestor['deadline'])
            state = {'schema':'effectcraft-managed-task/v2', 'taskId':task, 'state':'planned',
                     'plan':plan, 'identity':identity, 'identityHash':digest(identity), 'workKey':work_key,
                     'output':output, 'createdAt':now, 'deadline':deadline, 'parent':parent,
                     'budget':{'maxRevisions':2, 'revisions':0, 'stagnant':0},
                     'steps':[], 'worker':None, 'delivery':None, 'review':None}
            if not parent:state['resources']=load('resource_budget').empty()
            with load('project_claims').reserve(self,state):
                return self.save(state)

    def lineage(self, state):
        """只读核对完整父链；所有根预算查询共用循环检测。"""
        result=[state];seen={state['taskId']}
        while state['parent']:
            if state['parent'] in seen:raise ValueError('task_ancestry_cycle')
            seen.add(state['parent']);state=self.read(state['parent']);result.append(state)
        return result

    def reserve_resources(self, task, amounts, binding):
        return load('resource_budget').reserve(self,task,amounts,binding)

    def observe_resources(self, task, encoded_bytes):
        return load('resource_budget').observe(self,task,encoded_bytes)

    def allowed(self, state):
        if state['state'] in ('cancel_requested','cancelled') or state.get('cancellationRequestedAt'):
            raise ValueError('cancel_requested')
        if time.time() >= state['deadline']:
            raise ValueError('deadline_exceeded')
        # 每次调度重读完整祖先链，reconciling 不能抹去已持久化的取消意图。
        lineage=self.lineage(state)
        for parent in lineage[1:]:
            if (parent['state'] in ('cancel_requested','cancelled') or parent.get('cancellationRequestedAt')
                    or time.time() >= parent['deadline']):
                raise ValueError('parent_cancelled_or_expired')
        self.check_resources(state)

    def check_resources(self, state):
        """只读核对资源父链，不授权调度；过期／取消后仍可核对原结果。"""
        lineage=self.lineage(state)
        if 'resources' not in lineage[-1]:raise ValueError('legacy_resource_budget_missing')
        load('resource_budget').check(lineage[-1]['resources'])
        for item in lineage:load('resource_budget').check_reference(item,lineage[-1]['resources'])
        load('resource_budget').check_family(self,lineage[-1])

    def check_source_revision(self, state):
        """每次新操作与交付前核对源工程；外部变化、丢失或链接替换均拒绝。"""
        source = state['identity']['project']
        if source is None:
            return
        try:
            actual = file_sha(source)
        except (ValueError, OSError):
            raise ValueError('revision_conflict') from None
        if actual != state['identity']['projectRevision']:
            raise ValueError('revision_conflict')
        bound=state['identity']['authorization'].get('sourcePackage')
        if bound is not None:
            try:
                current=load('artifact_lineage').source_binding(Path(source).parent)
                if current!=bound:raise ValueError('source_package_changed')
            except (ValueError,OSError,KeyError,TypeError):
                raise ValueError('source_package_changed') from None
        producer=state['identity']['authorization'].get('sourceProducer')
        if producer is not None:load('artifact_lineage').verify_producer(producer)
        load('project_claims').verify(self,state)

    def start(self, task):
        with self.lock():
            state = self.read(task); self.allowed(state)
            if state['schema']!='effectcraft-managed-task/v2':raise ValueError('legacy_task_read_only')
            if state['state']=='resuming':
                reference=state.get('renderRecovery',{})
                if (not state['steps'] or state['steps'][-1]['id']!=reference.get('operationId')
                        or state['steps'][-1]['state']!='attempted'
                        or state.get('reconciliation',{}).get('result')!='render_resume_ready'
                        or any(s['state']!='succeeded' for s in state['steps'][:-1])):
                    raise ValueError('reconciliation_required')
            elif state['state'] != 'planned' or state['steps']:
                raise ValueError('reconciliation_required')
            self.check_source_revision(state)
            state['state'] = 'running'
            if state.get('worker'):state.setdefault('workerHistory',[]).append(state['worker'])
            state['worker'] = {'pid':os.getpid(), 'nonce':uuid.uuid4().hex}
            return self.save(state)

    def begin_step(self, task, operation, arguments):
        with self.lock():
            state = self.read(task); self.allowed(state)
            if state['state'] != 'running':
                raise ValueError('state_conflict')
            if any(s['state'] == 'attempted' for s in state['steps']):
                raise ValueError('unresolved_operation')
            self.check_source_revision(state)
            step = {'id':uuid.uuid4().hex, 'operation':operation, 'argumentsHash':digest(arguments),
                    'state':'attempted', 'attemptedAt':time.time()}
            state['steps'].append(step); self.save(state)
            return step['id']

    def finish_step(self, task, operation_id, result):
        with self.lock():
            state = self.read(task)
            if state['state'] not in ('running', 'cancel_requested'):
                raise ValueError('state_conflict')
            step = next(s for s in state['steps'] if s['id'] == operation_id)
            if step['state'] != 'attempted':
                raise ValueError('operation_already_settled')
            receipt_path=self.path(task).parent/'receipts'/(operation_id+'.json')
            receipt={'schema':'effectcraft-step-result/v1','taskId':task,'operationId':operation_id,
                     'argumentsHash':step['argumentsHash'],'result':result}
            if receipt_path.exists():
                existing=load('commands').reply_json(receipt_path.read_text(encoding='utf-8'))
                if canonical(existing)!=canonical(receipt):raise ValueError('operation_receipt_conflict')
            else:atomic_json(receipt_path,receipt)
            step.update(state='succeeded', resultHash=digest(result), completedAt=time.time())
            return self.save(state)

    def fail(self, task, error, unknown=False):
        with self.lock():
            state = self.read(task)
            unresolved = any(s['state'] == 'attempted' for s in state['steps'])
            state.update(state='reconciling' if unknown or unresolved else 'failed', error=str(error))
            return self.save(state)

    def cancel(self, task):
        if self.read(task)['schema']!='effectcraft-managed-task/v2':raise ValueError('legacy_task_read_only')
        with self.lock():
            return load('cancellation').request_locked(self,task)

    def stopped(self, task, reason):
        """监督器确认自有进程退出后调用；终止进程不证明未知编辑未发生。"""
        with self.lock():
            state=self.read(task)
            state.setdefault('cancellationRequestedAt',time.time())
            state['termination']={'status':'confirmed','reason':reason,'at':time.time()}
            return self.save(load('cancellation').update_locked(self,state,current_confirmed=True))

    def worker_exited(self, task, returncode, ownership=None):
        """登记已退出的自有worker；不把worker退出当作原生子进程停止证明。"""
        evidence=exit_evidence(returncode,ownership)
        with self.lock():
            state = self.read(task)
            if state['schema'] != 'effectcraft-managed-task/v2':
                raise ValueError('legacy_task_read_only')
            if state['state']=='cancelled' and load('cancellation').check_local(self,state):
                return state
            state['processExit']=evidence
            state['workerExitCode'] = returncode if evidence['workerResultVerified'] else None
            state['workerExitObservedAt'] = evidence['observedAt'] if evidence['workerResultVerified'] else None
            if state['state'] in ('planned','resuming'):
                # 持锁重读后处理，避免覆盖并发取消或已确认的交付终态。
                state['state'] = 'reconciling' if state['steps'] else 'failed'
                state['error'] = 'worker exited before durable start (code ' + str(returncode) + '); inspect worker.log'
            elif state['state'] == 'running':
                state['state'] = 'reconciling'
                state['error'] = 'worker exited without durable completion; inspect worker.log'
            return self.save(state)

    def delivered(self, task, manifest):
        with self.lock():
            state = self.read(task); self.allowed(state)
            if state['state'] != 'running' or any(s['state'] != 'succeeded' for s in state['steps']):
                raise ValueError('unresolved_operation')
            self.check_source_revision(state)
            state.update(state='review_ready', delivery=manifest)
            return self.save(state)

    def lifecycle_path(self, state):
        """每次续跑保留独立进程回执；禁止任务记录引用包外路径。"""
        name=state.get('lifecycleReceipt','lifecycle.json')
        if not isinstance(name,str) or not re.fullmatch(r'lifecycle(?:-resume-[0-9]{4})?\.json',name):
            raise ValueError('lifecycle_reference_invalid')
        path=self.path(state['taskId']).parent/name
        if path.is_symlink():raise ValueError('lifecycle_reference_invalid')
        return path
