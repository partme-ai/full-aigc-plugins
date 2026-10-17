"""固定任务族评价标准与不可覆盖的版本回执；评分和停滞按版本结算。"""
import importlib.util
from pathlib import Path
import re
import subprocess
import time


def load(name):
    spec=importlib.util.spec_from_file_location('craft_review_ledger_'+name,Path(__file__).with_name(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def quality_adapter(store,state):
    """同一账本按任务模式读取现有交付，不生成平行公共协议。"""
    if state['identity']['mode']=='workflow':return load('quality_review')
    return load('command_judge').Quality(store,state['taskId'])


def temporal_required(quality,state,report):
    if state['identity']['mode']!='workflow':return quality.temporal(state['output'],report)
    managed=load('managed');root=Path(state['output'])
    native=managed.read(root/'native.json')
    return bool(managed.read(root/'manifest.json').get('video') or native['composition'].get('duration',0)>0)


def immutable(path, value):
    """重复写入只接受规范化内容一致；不覆盖既有回执。"""
    tasks=load('task_store')
    if any(parent.is_symlink() for parent in path.parents):raise ValueError('review_receipt_symlink')
    if path.exists() or path.is_symlink():
        if path.is_symlink() or load('managed').read(path)!=value:
            raise ValueError('review_receipt_conflict')
    else:tasks.atomic_json(path,value)


def validate(store, root, criteria_hash):
    """在继续比较前复核每份已结算回执及其实际交付。"""
    ledger=root.get('qualityReviews')
    if ledger is None:
        if root.get('reviewedRequests') or root.get('bestTask'):
            raise ValueError('legacy_review_read_only')
        return {'schema':'effectcraft-review-ledger/v1','criteriaHash':criteria_hash,'entries':{},'order':[]}
    if (not isinstance(ledger,dict) or ledger.get('schema')!='effectcraft-review-ledger/v1'
            or not isinstance(ledger.get('entries'),dict) or len(ledger['entries'])>3):
        raise ValueError('review_ledger_invalid')
    if ledger.get('criteriaHash')!=criteria_hash:raise ValueError('criteria_changed')
    order=ledger.get('order')
    if (not isinstance(order,list) or any(not isinstance(task,str) for task in order)
            or len(order)!=len(set(order)) or set(order)!=set(ledger['entries'])):
        raise ValueError('review_ledger_invalid')
    best_task=None;best_score=-1;stagnant=0
    for task in order:
        entry=ledger['entries'][task]
        state=store.read(task)
        if store.lineage(state)[-1]['taskId']!=root['taskId']:raise ValueError('review_family_mismatch')
        request_id=entry['requestId']
        if not isinstance(request_id,str) or not re.fullmatch('[a-f0-9]{32}',request_id):
            raise ValueError('review_ledger_invalid')
        directory=store.path(task).parent/'reviews'/request_id
        if directory.is_symlink() or directory.parent.is_symlink():raise ValueError('review_receipt_symlink')
        for filename in ('request.json','response.json','quality.json'):
            load('task_store').file_sha(directory/filename)
        request=load('managed').read(directory/'request.json')
        response=load('managed').read(directory/'response.json')
        report=load('managed').read(directory/'quality.json')
        tasks=load('task_store')
        if request.get('schema')!='effectcraft-judge-request/v2':raise ValueError('legacy_review_read_only')
        if (tasks.digest(request)!=entry['requestHash'] or tasks.digest(response)!=entry['responseHash']
                or tasks.file_sha(directory/'quality.json')!=entry['reportSha256']
                or request['taskId']!=task or request['criteriaHash']!=criteria_hash
                or report['binding']!=entry['binding'] or request['binding']!=entry['binding']
                or report['technical']['status']!='PASS' or report['engineering']['status']!='PASS'
                or report['creative']['status'] not in ('PASS','FAIL')
                or report['creative']['receipt']!=response or response['score']!=entry['score']):
            raise ValueError('review_receipt_changed')
        quality=quality_adapter(store,state)
        if quality.binding(state['output'])!=entry['binding']:
            raise ValueError('artifact_changed')
        if quality.accept_judge(state['output'],report,request,response)['creative']!=report['creative']:
            raise ValueError('review_receipt_changed')
        if entry['score']>best_score:best_task=task;best_score=entry['score'];stagnant=0
        else:stagnant+=1
    if best_task is not None:
        expected={'taskId':best_task,**ledger['entries'][best_task]}
        if (root.get('bestVerified')!=expected or root.get('bestScore')!=best_score
                or root.get('bestTask')!=best_task or root['budget']['stagnant']!=stagnant):
            raise ValueError('review_selection_changed')
    return ledger


def review(store, task, criteria, judge=None, runtime_home=None):
    """保留本次只读技术检查，供公开入口输出拒绝诊断。"""
    report={}
    try:
        return _review(store,task,criteria,judge,report,runtime_home)
    except (ValueError,OSError,KeyError,TypeError,subprocess.SubprocessError) as error:
        error.review_report=report
        raise


def _review(store, task, criteria, judge, report, runtime_home):
    """只在当前任务族约束内写入评估；根账本是已结算版本的事实源。"""
    managed=load('managed');tasks=load('task_store')
    state=store.read(task)
    if state['schema']!='effectcraft-managed-task/v2':raise ValueError('legacy_task_read_only')
    if state['state']!='review_ready':raise ValueError('review_state_conflict')
    quality=quality_adapter(store,state)
    report.update(quality.inspect_delivery(state['output'],runtime_home) if state['identity']['mode']!='workflow' else quality.inspect_delivery(state['output']))
    with store.lock():store.allowed(store.read(task))
    if report.get('binding') and state['identity']['mode']=='workflow':
        kwargs={}
        if any(r['source']=='file' for r in report.get('nativeResources',{}).get('luts',[])):
            kwargs['before_render']=load('resource_validation').budget_hook(store,task)
        report['engineering']=load('engineering_review').verify(state['output'],runtime_home,
            state['identity']['runtimeSha256'],timeout=max(.1,min(120,state['deadline']-time.time())),**kwargs)
        if 'resourceValidation' in report['engineering']:report['resourceValidation']=report['engineering']['resourceValidation']
    response=managed.read(judge) if judge else None
    criteria_hash=tasks.digest(criteria)
    with store.lock():
        current=store.read(task);store.allowed(current)
        if current['state']!='review_ready' or current['identityHash']!=state['identityHash']:
            raise ValueError('review_state_conflict')
        root=store.lineage(current)[-1]
        ledger=validate(store,root,criteria_hash)
        entry=ledger['entries'].get(task)
        directory=store.path(task).parent
        request_path=directory/'judge-request.json'
        if entry:
            if response is not None and tasks.digest(response)!=entry['responseHash']:
                raise ValueError('judge_response_conflict')
            frozen=directory/'reviews'/entry['requestId']
            if report['technical']['status']!='PASS' or report['engineering']['status']!='PASS':
                report['historicalReview']={'path':str((frozen/'quality.json').relative_to(directory)),'sha256':entry['reportSha256']}
                action='technical_verification' if report['technical']['status']!='PASS' else 'engineering_verification'
                return {'report':report,'judgeRequest':None,'requiredAction':action}
            request=managed.read(frozen/'request.json')
            frozen_report=managed.read(frozen/'quality.json')
            frozen_report.update(engineering=report['engineering'],technical=report['technical'],userAcceptance=report['userAcceptance'])
            report=frozen_report
            reference={'path':str((frozen/'quality.json').relative_to(directory)), 'sha256':entry['reportSha256']}
            # 根记录先结算；崩溃后只修复子记录引用，不重算评分或停滞。
            if current.get('review')!=reference:
                current['review']=reference;store.save(current)
            return {'report':report,'judgeRequest':request,'requiredAction':None}
        if report['technical']['status']!='PASS':
            return {'report':report,'judgeRequest':None,'requiredAction':'technical_verification'}
        if quality.binding(state['output'])!=report.get('binding'):raise ValueError('artifact_changed')
        if request_path.exists():
            request=managed.read(request_path)
            if request['taskId']!=task or request['criteriaHash']!=criteria_hash:raise ValueError('criteria_changed')
            if request['binding']!=report['binding']:raise ValueError('artifact_changed')
        elif response is not None:raise ValueError('judge_request_missing')
        else:
            if report['engineering']['status']!='PASS':
                return {'report':report,'judgeRequest':None,'requiredAction':'engineering_verification'}
            proof_key='manifestSha256' if state['identity']['mode']=='workflow' else 'commandDeliverySha256'
            if report['binding'][proof_key]!=state.get('delivery',{}).get(proof_key):
                raise ValueError('artifact_changed')
            temporal=temporal_required(quality,state,report)
            request=quality.judge_request(task,state['output'],report,criteria,temporal)
            immutable(request_path,request)
        if not isinstance(request.get('requestId'),str) or not re.fullmatch('[a-f0-9]{32}',request['requestId']):
            raise ValueError('judge_request_changed')
        temporal=temporal_required(quality,state,report)
        expected=quality.judge_request(task,state['output'],report,criteria,temporal)
        expected['requestId']=request['requestId']
        if request!=expected:raise ValueError('judge_request_changed')
        if report['engineering']['status']!='PASS':
            return {'report':report,'judgeRequest':None,'requiredAction':'engineering_verification'}
        root['qualityReviews']=ledger
        if response is None:
            store.save(root)
            return {'report':report,'judgeRequest':request,'requiredAction':'host_visual_review'}
        if report['engineering']['status']!='PASS':raise ValueError('engineering_gate')
        report=quality.accept_judge(state['output'],report,request,response)
        if report['creative']['status']=='NOT_RUN':
            attempt={'schema':'effectcraft-judge-attempt/v1','requestHash':tasks.digest(request),
                     'responseHash':tasks.digest(response),'report':report}
            path=directory/'review-attempts'/(tasks.digest(response)+'.json')
            immutable(path,attempt)
            reference={'path':str(path.relative_to(directory)),'sha256':tasks.file_sha(path)}
            if current.get('reviewAttempt')!=reference:
                current['reviewAttempt']=reference;store.save(current)
            return {'report':report,'judgeRequest':request,'requiredAction':'host_visual_review'}
        frozen=directory/'reviews'/request['requestId']
        for name,value in [('request.json',request),('response.json',response),('quality.json',report)]:
            immutable(frozen/name,value)
        entry={'requestId':request['requestId'],'requestHash':tasks.digest(request),'responseHash':tasks.digest(response),
               'reportSha256':tasks.file_sha(frozen/'quality.json'),'binding':report['binding'],'score':response['score']}
        ledger['entries'][task]=entry;ledger['order'].append(task)
        if entry['score']>root.get('bestScore',-1):
            root['bestScore']=entry['score'];root['bestTask']=task;root['budget']['stagnant']=0
            root['bestVerified']={'taskId':task,**entry}
        else:root['budget']['stagnant']+=1
        reference={'path':str((frozen/'quality.json').relative_to(directory)), 'sha256':entry['reportSha256']}
        if task==root['taskId']:root['review']=reference
        store.save(root)
        if task!=root['taskId']:
            current['review']=reference;store.save(current)
        return {'report':report,'judgeRequest':request,'requiredAction':None}
