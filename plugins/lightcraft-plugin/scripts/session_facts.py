"""只读消费上游 MCP 探测回执；不连接桌面、不执行任务或接受产物。"""
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def upstream():
    path=ROOT/'skills/lightcraft-use/scripts/command_gateway.py'
    spec=importlib.util.spec_from_file_location('session_receipts',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def inspect_session(path):
    """验证观察事实与固定身份，外来源仅可读；任何结果都不能触发重放。"""
    gateway=upstream();read=gateway.read_receipt(path)
    if not read['compatible']:return dict(read,taskExecutionAllowed=False,deliveryAllowed=False)
    receipt=read['receipt']
    if receipt.get('receiptKind')!='mcp-readonly-probe' or receipt.get('readOnly') is not True:raise ValueError('not_readonly_mcp_probe')
    if receipt.get('backendSessionIdentity')!='NOT_PROVIDED_BY_NATIVE_PROTOCOL':raise ValueError('unsupported_backend_identity_claim')
    requests=receipt.get('requests')
    if not isinstance(requests,list) or len(requests)!=4:raise ValueError('probe_requests_invalid')
    # 固定观察事务的结构门禁；不重新解释原生命令或重新计算其错误分类。
    methods=['initialize','notifications/initialized','tools/list','resources/read'];ids=[1,None,2,3]
    for index,request in enumerate(requests):
        if not isinstance(request,dict) or request.get('jsonrpc')!='2.0' or request.get('method')!=methods[index] or set(request)-{'jsonrpc','method','id','params'}:raise ValueError('probe_requests_invalid')
        if ids[index] is None:
            if 'id' in request:raise ValueError('probe_requests_invalid')
        elif type(request.get('id')) is not int or request['id']!=ids[index]:raise ValueError('probe_requests_invalid')
        if not isinstance(request.get('params'),dict):raise ValueError('probe_requests_invalid')
        if index in (1,2) and request['params']!={}:raise ValueError('probe_requests_invalid')
        if index==3 and request['params']!={'uri':'lightcraft://library'}:raise ValueError('probe_requests_invalid')
    data=''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in requests).encode()
    if hashlib.sha256(data).hexdigest()!=receipt.get('requestsSha256'):raise ValueError('probe_requests_identity_mismatch')
    steps=[{'command':'mcp:'+r['method'],'params':r['params']} for r in requests if 'id' in r]
    plan={'domain':'lightcraft','steps':steps}
    if hashlib.sha256(json.dumps(plan,sort_keys=True,ensure_ascii=False).encode()).hexdigest()!=receipt['planSha256']:raise ValueError('probe_plan_identity_mismatch')
    rows=receipt['steps']
    if len(rows)>3 or any(row.get('index')!=i or row.get('command')!=steps[i]['command'] for i,row in enumerate(rows)):raise ValueError('probe_steps_identity_mismatch')
    snapshot=ROOT/'skills/lightcraft-use/scripts'
    lock=gateway.strict_json((snapshot/'runtime.lock.json').read_text())
    if receipt['runtimeLockSha256']!=gateway.file_sha(snapshot/'runtime.lock.json'):raise ValueError('probe_runtime_lock_mismatch')
    process=receipt.get('process',{});native=receipt.get('runtimeIdentity');requested=receipt.get('requestedMode',{})
    if not isinstance(process,dict) or not isinstance(requested,dict):raise ValueError('probe_process_invalid')
    if native is not None:
        if not isinstance(native,dict) or native.get('version')!=lock['resolvedVersion'] or native.get('binarySha256') not in {a['binarySha256'] for a in lock['artifacts'].values()}:raise ValueError('probe_runtime_identity_mismatch')
        if native.get('mode') not in ('Headless','Connect') or native.get('mode')!=requested.get('mode') or native.get('transport')!='stdio-mcp' or native.get('readOnly') is not True:raise ValueError('probe_mode_identity_mismatch')
        if native.get('connectAddress')!=requested.get('connectAddress'):raise ValueError('probe_endpoint_mismatch')
        if process.get('stdinSha256')!=receipt['requestsSha256']:raise ValueError('probe_stdin_identity_mismatch')
    if receipt['status']=='NATIVE_EXIT_ZERO_REVIEW_REQUIRED':
        if (native is None or process.get('status')!='EXITED' or process.get('exitCode')!=0 or process.get('logComplete') is not True
                or len(rows)!=3 or any(row['status']!='SUCCEEDED' for row in rows) or receipt.get('backendQuery')!='PASS'):
            raise ValueError('probe_success_inconsistent')
    elif receipt.get('backendQuery')=='PASS':raise ValueError('probe_query_status_inconsistent')
    resources=gateway.capture_resources(snapshot)
    return {'readOnly':True,'compatible':True,'runId':receipt['runId'],'status':receipt['status'],
            'runtimeIdentity':native,'backendQuery':receipt.get('backendQuery','NOT_CONFIRMED'),
            'backendSessionIdentity':receipt.get('backendSessionIdentity','NOT_PROVIDED_BY_NATIVE_PROTOCOL'),
            'sourceSnapshotMatches':resources==receipt['skillResourceSha256'],
            'taskExecutionAllowed':False,'deliveryAllowed':False,'automaticReplay':False,
            'scope':'observation only; a probe cannot resume a task, prove desktop session identity, or accept exported images'}
