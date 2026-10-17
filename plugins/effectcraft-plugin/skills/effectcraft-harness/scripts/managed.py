#!/usr/bin/env python3
"""EffectCraft 单技能的受管理入口：诊断、执行、核对、评估与局部修订。"""
import argparse
import importlib.util
import json
import math
from fractions import Fraction
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import uuid

sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent


def load(name):
    spec=importlib.util.spec_from_file_location('managed_'+name,HERE/(name+'.py'))
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value)
    return value


def read(path):
    return load('commands').reply_json(Path(path).read_text(encoding='utf-8'))


def doctor(runtime_home,probe_native=False,compare_catalog=None):
    key=load('platform_support').platform_key(); lock=read(HERE/'runtime.lock.json')
    expected=lock['artifacts'].get(key);home=Path(runtime_home).expanduser().absolute()
    catalog=load('command_catalog').validate(load('commands').catalog())
    python_lock=read(HERE/'python.lock.json');actual_python=sys.version.split()[0]
    argv=[sys.executable,'-I','-B',str(HERE/'managed.py'),'--runtime-home',str(home),'doctor']
    result={'platform':key,'python':actual_python,
            'pythonRuntime':{'lockedVersion':python_lock['version'],'actualVersion':actual_python,'matchesLock':actual_python==python_lock['version']},
            'runtime':{'version':lock['resolvedVersion'],'supported':bool(expected),'installed':False,'actualVersionOutput':None},
            'managedCommands':['doctor','plan','run','inspect','reconcile','resume','cancel','review','revise'],
            'catalog':{'commandCount':len(catalog['commands']),'toolCount':len(catalog['nativeTools']),
                       'runtimeSha256':catalog['runtimeSha256'],'runModes':['headless','desktop'],'executionAcceptance':'NOT_RUN'},
            'nativeCapabilities':{'status':'NOT_RUN','scope':'static diagnostics only; use --probe-native for verified readonly discovery','executionAcceptance':'NOT_RUN'},
            'acceptance':{'nativePlatform':'NOT_RUN','hostDispatch':'NOT_RUN'},
            'recovery':'run a validated plan to install pinned dependencies','recoveryActions':[]}
    # 旧目录有问题时先失败，不借诊断启动原生进程。
    if compare_catalog is not None:result['commandDiff']=load('command_catalog').compare(read(compare_catalog),catalog)
    directory=home/'effectcraft'/lock['resolvedVersion']
    if expected:
        result['runtime']['minimumSystem']=expected.get('minimumSystem',{})
        try:load('platform_support').check_minimum(expected.get('minimumSystem',{}))
        except ValueError as error:result['runtime']['platformError']=str(error)
    if expected and (directory.exists() or directory.is_symlink()):
        try:
            result['runtime'].update(load('bootstrap').inspect_install(directory,lock['artifact'],expected,lock['resolvedVersion'],key),installed=True)
        except (ValueError,OSError) as error:result['runtime']['error']=str(error)
    if probe_native and result['runtime']['installed'] and 'platformError' not in result['runtime']:
        result['nativeCapabilities']=load('native_diagnostics').observe(result['runtime']['executable'],catalog,
                                   expected.get('versionOutput',lock['artifact']+' '+lock['resolvedVersion']))
        result['runtime']['actualVersionOutput']=result['nativeCapabilities'].get('actualVersionOutput')
    if result['runtime'].get('error'):
        result['recoveryActions'].append({'id':'inspect_preserved_runtime','argv':argv,'automatic':False,
                                         'note':'Preserve the installation and task records; diagnostics never delete, reinstall or replay.'})
    elif expected and not result['runtime']['installed'] and 'platformError' not in result['runtime']:
        result['recoveryActions'].append({'id':'install_pinned_cli','argv':[sys.executable,'-I','-B',str(HERE/'bootstrap.py'),'--runtime-home',str(home)],
                                         'automatic':False,'note':'Explicit installation action; not executed by doctor.'})
    elif result['runtime']['installed'] and 'platformError' not in result['runtime']:
        result['recoveryActions'].append({'id':'probe_native','argv':argv+['--probe-native'],'automatic':False})
    else:result['recoveryActions'].append({'id':'inspect_platform_requirements','argv':argv,'automatic':False,
                                         'note':'No compatible native execution is authorized by this diagnostic.'})
    return result


def preflight(plan, output, mode, inputs=None, source=None, revision_scope=None, store=None):
    inputs=inputs or {}
    if revision_scope is not None:
        if mode=='workflow':raise ValueError('revision_scope_mode')
        load('command_revision').validate_scope(plan,revision_scope)
    if mode=='workflow':
        load('workflow').validate(plan)
    else:
        load('commands').validate(plan,inputs,'bridge' if mode=='desktop' else 'headless')
    output=Path(output).absolute()
    if output.exists() or output.is_symlink():
        raise ValueError('output_exists')
    hashes={k:load('task_store').file_sha(v) for k,v in inputs.items()}
    for name,item in plan.get('assets',{}).items():
        actual=load('task_store').file_sha(item['path'])
        if actual!=item['sha256']:raise ValueError('asset_digest_mismatch')
        hashes[name]=actual
    source_package=None;source_producer=None
    if source:
        source_package=load('artifact_lineage').source_binding(source)
        if store is not None:source_producer=load('artifact_lineage').producer_binding(store,source)
        manifest=load('artifact_lineage').validate_source(source); project=Path(source)/'project.ecproj'
        if load('task_store').file_sha(project)!=manifest['files']['project.ecproj'] or plan.get('expectedProjectSha256')!=manifest['files']['project.ecproj']:
            raise ValueError('revision_conflict')
    return {'result':'VALID','planHash':load('task_store').digest(plan),'inputHashes':hashes,
            'mode':mode,'output':str(output),'source':str(source) if source else None,
            **({'sourcePackage':source_package} if source_package else {}),
            **({'sourceProducer':source_producer} if source_producer else {})}


class Hooks:
    """在真实 MCP 副作用前登记操作；合法返回后才能结算。"""
    def __init__(self, store, task):
        self.store=store;self.task=task

    def artifact_identity(self):
        return load('artifact_lineage').register_producer(self.store,self.task)

    def before(self, name, arguments):
        return self.store.begin_step(self.task,name,arguments)

    def after(self, identifier, result):
        self.store.finish_step(self.task,identifier,result)

    def checkpoint_export(self, identifier, context):
        load('render_recovery').capture(self.store,self.task,identifier,context)

    def allowed(self):
        with self.store.lock():self.store.allowed(self.store.read(self.task))

    def reserve_render(self, composition, plan):
        count=len(plan.get('frames',[0]))
        if plan.get('exports'):count+=math.ceil(Fraction(str(composition['frameRate']))*Fraction(str(composition['duration'])))
        binding={'composition':composition,'frames':plan.get('frames',[0]),'exports':plan.get('exports',[])}
        self.store.reserve_resources(self.task,{'frames':count,'decodedBytes':count*composition['width']*composition['height']*4},load('task_store').digest(binding))

    def observe_render(self, context):
        load('resource_meter').sample(self.store,self.task)

    def watch_render(self, stage, output):
        load('resource_meter').watch(self.store,self.task,stage,output,'workflow')

    def watch_segment(self, stage, output, part, composition):
        identity=stage.stat()
        attempt=load('task_store').digest({'path':str(stage.resolve()),'identity':[identity.st_dev,identity.st_ino]})
        count=part['frameCount']
        load('resource_budget').reserve_segment(self.store,self.task,output.name,attempt,count,
            count*composition['width']*composition['height']*4)
        load('resource_meter').watch(self.store,self.task,stage,output,'segment')

    def finish_segment(self, stage):
        load('resource_meter').sample(self.store,self.task)
        load('resource_meter').retire(self.store,self.task,stage)

    def command_observation(self,session,record,phase):
        return load("command_delivery").Observer(self.store,self.task)(session,record,phase)

    def prepare_command_output(self,output):
        request=read(self.store.path(self.task).parent/'request.json')
        if request.get('commandRevision'):
            load('command_revision').prepare_output(self.store,self.task,output)
        else:
            state=self.store.read(self.task)
            frames=sum(load('command_delivery').kind(op)=='frame' for op in state['plan']['operations'])
            self.store.reserve_resources(self.task,{'frames':frames,'decodedBytes':0},state['identity']['planHash'])
        load('resource_meter').watch(self.store,self.task,output,output,'commands')

    def session(self, argv):
        owner=self
        state=self.store.read(self.task)
        timeout=max(.1,min(120,state['deadline']-time.time()))
        underlying=load('mcp_session').Session(argv,timeout=timeout)
        class Wrapped:
            def __enter__(self):return self
            def __exit__(self,*args):underlying.close()
            def request(self,method,params):
                if method!='tools/call':return underlying.request(method,params)
                identifier=owner.before(params.get('name',method),params)
                result=underlying.request(method,params)
                # 使用真实返回解析器；畸形/错误回复保持 attempted，不误记成功。
                parsed=load('commands').parse_reply(result,receipt_only=True)
                owner.after(identifier,parsed)
                return result
        return Wrapped()


def worker(store, task, runtime_home):
    state=store.read(task)
    load('runtime_binding').resolve(store,task)
    with load('platform_support').exclusive_lock(store.root/'leases'/(task+'.lock'),timeout=0):
        recovering=state['state']=='resuming'
        store.start(task); hooks=Hooks(store,task)
        try:
            request=read(store.path(task).parent/'request.json')
            if load('task_store').digest(request)!=state['identity']['authorization'].get('requestHash'):
                raise ValueError('request_changed')
            plan=state['plan'];output=Path(state['output'])
            if recovering:
                context=load('render_recovery').validate(store,store.read(task))
                load('workflow').validate(plan)
                hashes={name:load('task_store').file_sha(path) for name,path in request['inputs'].items()}
                hashes.update({name:load('task_store').file_sha(asset['path']) for name,asset in plan.get('assets',{}).items()})
                current={'inputHashes':hashes}
            else:
                current=preflight(plan,output,state['identity']['mode'],request['inputs'],request.get('source'),request.get('revisionScope'),store=store)
            if request.get('revisionScope')!=state['identity']['authorization'].get('revisionScope'):
                raise ValueError('revision_scope_changed')
            if current['inputHashes']!=state['identity']['inputHashes']:
                raise ValueError('input_changed')
            key=load('platform_support').platform_key()
            if read(HERE/'runtime.lock.json')['artifacts'][key]['binarySha256']!=state['identity']['runtimeSha256']:
                raise ValueError('runtime_changed; original task must keep its locked runtime')
            output.parent.mkdir(parents=True,exist_ok=True)
            if request.get('commandRevision'):
                load('command_revision').validate_prepared(store,task,runtime_home)
            if state['identity']['mode']=='workflow':
                if recovering:
                    with load('output_guard').resume_claim(output,context['executionIdentity'],context['outputIdentity']):
                        load('render_recovery').archive_failure(store,task,context)
                        result=load('workflow').finish_export(context,hooks,state['renderRecovery']['operationId'])
                else:
                    result=load('workflow').execute(plan,output,runtime_home,request.get('source'),task_hooks=hooks)
                proof={'manifestSha256':load('task_store').file_sha(output/'manifest.json'),
                       'projectSha256':load('task_store').file_sha(output/'project.ecproj'),'engineeringReopen':'PASS'}
            elif state['identity']['mode']=='commands':
                result=load('commands').execute(plan,output,runtime_home,session_factory=hooks.session,inputs=request['inputs'],observer=hooks.command_observation,prepare_output=hooks.prepare_command_output)
                if result['result']!='PASS':raise RuntimeError(result.get('error','native_command_failed'))
                load('command_completion').capture(store,task)
                proof=load('command_delivery').finalize(store,task)
            else:
                result=load('desktop_session').run(plan,output,runtime_home,request['inputs'],task_hooks=hooks)
                if result['result']!='PASS':raise RuntimeError(result.get('error','desktop_command_failed'))
                load('command_completion').capture(store,task)
                proof=load('command_delivery').finalize(store,task)
            if request.get('commandRevision'):
                load('command_revision').validate_result(store,task,proof,runtime_home)
            store.delivered(task,proof)
        except BaseException as error:
            store.fail(task,str(error),unknown=bool(store.read(task)['steps']))
            raise


def supervise(store, task, runtime_home, recover=False):
    """监督通道断开由独立守护器清理整个自有进程树，核实后才结算。"""
    platform=load('platform_support')
    with platform.exclusive_lock(store.root/'leases'/(task+'.supervisor.lock'),timeout=0):
        with platform.exclusive_lock(store.root/'leases'/(task+'.lifecycle.lock'),timeout=0):
            state=store.read(task)
            store.allowed(state)
            bound=load('runtime_binding').resolve(store,task)
            if recover:
                with store.lock():
                    state=store.read(task);store.allowed(state)
                    if (state['state']!='reconciling' or state.get('reconciliation',{}).get('result')!='render_resume_ready'
                            or state.get('termination',{}).get('status')=='confirmed'):
                        raise ValueError('reconciliation_required')
                    previous=store.lifecycle_path(state)
                    if read(previous).get('status')!='stopped':raise ValueError('process_termination_unconfirmed')
                    load('render_recovery').validate(store,state)
                    state=load('orphan_segments').archive_locked(store,task)
                    load('render_recovery').validate(store,state)
                    history=state.setdefault('renderResumes',[])
                    if len(history)>=9999:raise ValueError('render_resume_budget_exceeded')
                    history.append({'at':time.time(),'lifecycleReceipt':previous.name,'sha256':load('task_store').file_sha(previous)})
                    state['state']='resuming';state['lifecycleReceipt']='lifecycle-resume-'+format(len(history),'04d')+'.json'
                    store.save(state)
            elif state['state']!='planned' or state['steps']:
                raise ValueError('reconciliation_required')
        receipt=store.lifecycle_path(state)
        args=[bound['python'],'-I','-B',bound['guard'],'--receipt',str(receipt),
              '--lease',str(store.root/'leases'/(task+'.lifecycle.lock')),'--',
              bound['python'],'-I','-B',bound['script'],'--state-root',str(store.root),
              '--runtime-home',bound['runtimeHome'],'_worker','--task',task]
        options={'start_new_session':True} if os.name!='nt' else {'creationflags':subprocess.CREATE_NEW_PROCESS_GROUP}
        with (store.path(task).parent/'worker.log').open('ab') as log:
            child=subprocess.Popen(args,stdin=subprocess.PIPE,stdout=log,stderr=log,**options)
            cancellation=False;stop_reason=None;next_sample=0
            try:
                while child.poll() is None:
                    try:
                        with store.lock():
                            if time.monotonic()>=next_sample:
                                load('resource_meter').sample_locked(store,task,live=True);next_sample=time.monotonic()+1
                            store.allowed(store.read(task))
                    except ValueError as error:
                        # 原生调用阻塞时也检查完整祖先链；停止意图先落盘，再关闭守护通道。
                        cancellation=True;stop_reason=str(error);store.cancel(task)
                        child.stdin.close();child.wait(timeout=25);break
                    time.sleep(.1)
            except BaseException:
                store.cancel(task);child.stdin.close()
                try:child.wait(timeout=25)
                finally:store.fail(task,'supervisor interrupted; inspect lifecycle receipt',unknown=True)
                raise
            finally:
                if not child.stdin.closed:child.stdin.close()
        lifecycle=read(receipt)
        if lifecycle.get('schema')!='effectcraft-process-lifecycle/v1' or lifecycle.get('status')!='stopped':
            return store.fail(task,'owned process tree termination is unconfirmed',unknown=True)
        try:load('task_store').exit_evidence(lifecycle.get('returncode'),lifecycle.get('ownership'))
        except ValueError as error:return store.fail(task,'owned process result unconfirmed: '+str(error),unknown=True)
        try:load('resource_meter').sample(store,task)
        except (ValueError,OSError) as error:return store.fail(task,'resource observation unconfirmed: '+str(error),unknown=True)
        if cancellation:store.stopped(task,'owned process tree verified stopped: '+stop_reason)
        return store.worker_exited(task,lifecycle['returncode'],lifecycle.get('ownership'))


def run(store, plan, output, runtime_home, mode='workflow', inputs=None, source=None, task=None, parent=None, revision_scope=None):
    inputs=inputs or {};check=preflight(plan,output,mode,inputs,source,revision_scope,store=store)
    if source and not parent:
        for prior in store.all():
            if Path(prior['output']).resolve()==Path(source).resolve():
                raise ValueError('managed_source_requires_revise: '+prior['taskId'])
    key=load('platform_support').platform_key();lock=read(HERE/'runtime.lock.json')
    if key not in lock['artifacts']:raise ValueError('unsupported_platform: '+key)
    task=task or uuid.uuid4().hex
    request={'inputs':inputs,'source':str(source) if source else None}
    authorization={'writeRoot':str(Path(output).absolute()),'inputs':inputs}
    if check.get('sourcePackage'):authorization['sourcePackage']=check['sourcePackage']
    if check.get('sourceProducer'):authorization['sourceProducer']=check['sourceProducer']
    if revision_scope is not None:
        request['revisionScope']=revision_scope;authorization['revisionScope']=revision_scope
    authorization['requestHash']=load('task_store').digest(request)
    execution,manifest=load('runtime_binding').prepare(HERE.parent,runtime_home)
    store.create(task,plan=plan,output=str(output),runtime_sha=lock['artifacts'][key]['binarySha256'],
                 inputs=check['inputHashes'],source=str(Path(source)/'project.ecproj') if source else None,
                 mode=mode,authorization=authorization,parent=parent,runtime_binding=execution)
    load('task_store').atomic_json(store.path(task).parent/'request.json',request)
    load('runtime_binding').freeze(store,task,HERE.parent,manifest)
    return supervise(store,task,runtime_home)


def reconcile(store, task):
    current=store.read(task)
    state=load('command_completion').recover(store,task) if 'commandCompletion' in current and current['state'] in ('running','reconciling') else _reconcile(store,task)
    if state['identity']['mode']!='workflow' and state.get('parent') and state['state']=='review_ready':
        return load('command_revision').settle_completed(store,task)
    if state['identity']['mode']!='workflow' and state.get('parent') and (state['state']=='reconciling' or state['state']=='failed' and state.get('reconciliation',{}).get('result')=='revision_not_executed'):
        return load('command_revision').prove_not_executed(store,task)
    return state


def _reconcile(store, task):
    """只核对完整已落盘交付；无法证明的部分编辑继续保持 reconciling。"""
    if store.read(task)['schema']!='effectcraft-managed-task/v2':raise ValueError('legacy_task_read_only')
    with load('platform_support').exclusive_lock(store.root/'leases'/(task+'.supervisor.lock'),timeout=0), load('platform_support').exclusive_lock(store.root/'leases'/(task+'.lifecycle.lock'),timeout=0), load('platform_support').exclusive_lock(store.root/'leases'/(task+'.lock'),timeout=0):
        with store.lock():
            state=store.read(task)
            if state['state'] not in ('running','resuming','reconciling','cancel_requested'):
                return state
            lifecycle_path=store.lifecycle_path(state)
            cancelling=state['state']=='cancel_requested' or bool(state.get('cancellationRequestedAt'))
            never_started=cancelling and load('cancellation').check_local(store,state)
            if lifecycle_path.exists():
                lifecycle=read(lifecycle_path)
                if (lifecycle.get('schema')!='effectcraft-process-lifecycle/v1' or lifecycle.get('status')!='stopped'
                        or cancelling and type(lifecycle.get('returncode')) is not int):
                    raise ValueError('process_termination_unconfirmed')
            elif cancelling and not never_started:
                raise ValueError('process_termination_unconfirmed: cancellation lifecycle missing')
            elif state.get('worker'):
                raise ValueError('legacy_process_ownership_unknown')
            desktop_operations=load('desktop_revision').inspect_conflicts(store,state)
            if cancelling and not never_started:exit_result=load('task_store').exit_evidence(lifecycle['returncode'],lifecycle.get('ownership'))
            state=load('orphan_segments').settle_locked(store,task)
            state=load('resource_meter').sample_locked(store,task)
            state['state']='reconciling'
            state['reconciliation']={'result':'unknown','automaticReplay':False,
                'requiredAction':'inspect original project, native process and receipts; partial edits cannot be resent'}
            if desktop_operations:state['reconciliation']['desktopOperations']=desktop_operations
            if cancelling:
                # 控制器已重启；原回执及执行租约分别证明停止，未知编辑保持原身份。
                state['termination']={'status':'confirmed','reason':'not started at cancellation' if never_started else 'cancel reconciliation verified owned process stop','at':time.time()}
                if not never_started:
                    state['termination'].update(lifecycleReceipt=lifecycle_path.name,lifecycleSha256=load('task_store').file_sha(lifecycle_path))
                    state['processExit']=exit_result
                    state['workerExitCode']=exit_result['returncode'] if exit_result['workerResultVerified'] else None
                    state['workerExitObservedAt']=exit_result['observedAt'] if exit_result['workerResultVerified'] else None
                state=load('cancellation').update_locked(store,state,current_confirmed=True)
                if state['state']=='cancelled':state['reconciliation']['result']='cancelled_after_verified_stop'
                return store.save(state)
            if state.get('delivery') and not any(s['state']=='attempted' for s in state['steps']):
                if state['identity']['mode']=='workflow':
                    report=load('quality_review').inspect_delivery(state['output']);proof_key='manifestSha256'
                else:
                    report=load('command_delivery').inspect(store,task,None);proof_key='commandDeliverySha256'
                if report['technical']['status']=='PASS' and report.get('binding',{}).get(proof_key)==state['delivery'].get(proof_key):
                    state['state']='review_ready';state['reconciliation']['result']='verified_delivery'
            if state['state']=='reconciling' and state.get('renderRecovery'):
                load('render_recovery').validate(store,state)
                if (state['steps'][-1]['state']=='attempted' and not state.get('cancellationRequestedAt')
                        and state.get('termination',{}).get('status')!='confirmed'):
                    state['reconciliation']={'result':'render_resume_ready','automaticReplay':False,
                        'requiredAction':'resume only original segmented export; no editing calls'}
            return store.save(state)


def review(store, task, criteria, judge=None, runtime_home=None):
    if store.read(task)['identity']['mode']!='workflow':
        return load('command_delivery').review(store,task,criteria,judge,runtime_home)
    return load('review_ledger').review(store,task,criteria,judge,runtime_home)


def parser():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime-home',type=Path,default=Path(os.environ.get('CRAFT_RUNTIME_HOME',str(Path.home()/'.local/share/craft-runtimes'))))
    parser.add_argument('--state-root',type=Path,default=Path(os.environ.get('CRAFT_STATE_HOME',str(Path.home()/'.local/share/craft-tasks/effectcraft'))))
    sub=parser.add_subparsers(dest='action',required=True)
    diagnostic=sub.add_parser('doctor');diagnostic.add_argument('--probe-native',action='store_true');diagnostic.add_argument('--compare-catalog',type=Path)
    for name in ('plan','run','revise'):
        p=sub.add_parser(name);p.add_argument('--plan',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
        p.add_argument('--mode',choices=['workflow','commands','desktop'],default='workflow');p.add_argument('--input',action='append',default=[])
        p.add_argument('--source',type=Path);p.add_argument('--task')
        if name in ('plan','run'):p.add_argument('--revision-scope',type=Path)
    for name in ('inspect','reconcile','resume','cancel','_worker','review'):
        p=sub.add_parser(name);p.add_argument('--task',required=True)
        if name=='review':p.add_argument('--criteria',type=Path,required=True);p.add_argument('--judge',type=Path)
    return parser


def main():
    # 固定重定向输出编码，Windows默认代码页也能返回中文帮助和回执。
    import sys
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,"reconfigure"):stream.reconfigure(encoding="utf-8")
    args=parser().parse_args()
    try:
        store=load('task_store').Store(args.state_root)
        if args.action in ('resume','revise','reconcile','review','cancel','_worker'):
            load('runtime_binding').handoff(store,args,Path(__file__))
        if args.action=='doctor':result=doctor(args.runtime_home,args.probe_native,args.compare_catalog)
        elif args.action=='inspect':result=store.read(args.task)
        elif args.action=='cancel':result=store.cancel(args.task)
        elif args.action=='reconcile':result=reconcile(store,args.task)
        elif args.action=='resume':
            state=store.read(args.task)
            if state['state']=='planned' and not state['steps']:
                result=supervise(store,args.task,args.runtime_home)
            else:
                result=reconcile(store,args.task)
                if result.get('state')=='reconciling' and result.get('reconciliation',{}).get('result')=='render_resume_ready':
                    result=supervise(store,args.task,args.runtime_home,recover=True)
        elif args.action=='review':result=review(store,args.task,read(args.criteria),args.judge,args.runtime_home)
        elif args.action=='_worker':worker(store,args.task,args.runtime_home);return
        else:
            inputs={}
            for item in args.input:
                name,sep,value=item.partition('=')
                if not sep or name in inputs:raise ValueError('invalid_input')
                inputs[name]=str(Path(value).absolute())
            plan=read(args.plan)
            scope=read(args.revision_scope) if getattr(args,'revision_scope',None) else None
            if args.action=='plan':result=preflight(plan,args.output,args.mode,inputs,args.source,scope,store=store)
            elif args.action=='revise':result=load('revision').revise(store,args.task,plan,args.output,args.runtime_home)
            else:result=run(store,plan,args.output,args.runtime_home,args.mode,inputs,args.source,args.task,revision_scope=scope)
        print(json.dumps(result,ensure_ascii=False,allow_nan=False))
        if result.get('state') in ('failed','reconciling','cancel_requested'):raise SystemExit(1)
    except (ValueError,OSError,KeyError,TypeError,subprocess.SubprocessError) as error:
        result={'result':'FAIL','error':str(error)}
        if args.action=='review':
            # 历史PASS属于原摘要；拒绝不能冒充当前创作验收。
            report=getattr(error,'review_report',{}).copy()
            report.setdefault('schema','effectcraft-quality/v1')
            report.setdefault('engineering',{'status':'NOT_RUN'})
            report.setdefault('technical',{'status':'NOT_RUN'})
            report.setdefault('userAcceptance',{'status':'NOT_RUN','source':'explicit user decision required'})
            report['creative']={'status':'NOT_RUN','reason':str(error)}
            report['readyForAcceptance']=False;report['accepted']=False
            result.update(schema='effectcraft-review-rejection/v1',taskId=args.task,report=report,
                          requiredAction='inspect_current_delivery_and_request')
        print(json.dumps(result,ensure_ascii=False,allow_nan=False));raise SystemExit(1)


if __name__=='__main__':main()
