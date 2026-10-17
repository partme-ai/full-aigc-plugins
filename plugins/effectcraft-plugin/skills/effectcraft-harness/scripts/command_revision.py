"""命令/桌面局部修订：显式范围、原生字段保全和任务族预算。"""
import copy
import importlib.util
from pathlib import Path


def load(name):
    spec=importlib.util.spec_from_file_location('craft_command_revision_'+name,Path(__file__).with_name(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def validate_scope(plan,scope):
    """根任务执行前绑定保存工程及创建别名，不扩展公开命令计划。"""
    if not isinstance(scope,list) or not scope or len(scope)>100:raise ValueError('revision_scope_invalid')
    aliases={op.get('as') for op in plan['operations'] if op.get('as')}
    comps={op.get('as') for op in plan['operations'] if op.get('command')=='comp.new' and op.get('as')}
    projects=set()
    for op in plan['operations']:
        if (op.get('tool')=='save_project' or op.get('command') in ('file.saveAs','file.saveCopy')):
            path=op['params'].get('path')
            if isinstance(path,dict) and set(path)=={'$output'}:projects.add(path['$output'])
    seen=set()
    for row in scope:
        if (not isinstance(row,dict) or set(row)!={'project','comp','layer','properties'}
                or row['comp'] not in comps or row['layer'] not in aliases or row['project'] not in projects):
            raise ValueError('revision_scope_invalid')
        load('commands').output_path(row['project']);props=row['properties']
        if (not isinstance(props,list) or not props or any(not isinstance(x,str) or not x or '*' in x or len(x)>256 for x in props)
                or len(props)!=len(set(props))):raise ValueError('revision_scope_invalid')
        for prop in props:
            key=(row['project'],row['comp'],row['layer'],prop)
            if key in seen:raise ValueError('revision_scope_duplicate')
            seen.add(key)
    return copy.deepcopy(scope)


def validate_plan(plan,project,allowed):
    """限定静态值/text参数，解析原生属性UID，保留关键帧及其他字段。"""
    if (not isinstance(plan,dict) or set(plan)!={'schema','binding','project','operations'}
            or plan['schema']!='effectcraft-command-revision/v1' or plan['project']!=project['path']
            or not isinstance(plan['operations'],list) or not 1<=len(plan['operations'])<=100):
        raise ValueError('revision_plan_invalid')
    targets=[];seen=set()
    permits={(row['comp'],row['layer'],prop) for row in allowed if row['project']==project['path'] for prop in row['properties']}
    def nodes(value):
        if isinstance(value,dict):
            yield value
            for child in value.values():yield from nodes(child)
        elif isinstance(value,list):
            for child in value:yield from nodes(child)
    for op in plan['operations']:
        if not isinstance(op,dict) or set(op)!={'comp','command','params'}:raise ValueError('revision_operation_invalid')
        if op['command'] not in ('layer.setText','prop.set'):raise ValueError('revision_command_not_allowed')
        params=op['params'];fields={'layer','text'} if op['command']=='layer.setText' else {'layer','path','value'}
        if not isinstance(params,dict) or set(params)!=fields:raise ValueError('revision_parameters_not_allowed')
        prop='text/sourceText' if op['command']=='layer.setText' else params['path']
        if type(op['comp']) is not int or type(params['layer']) is not int or not isinstance(prop,str):raise ValueError('revision_scope_exceeded')
        key=(op['comp'],params['layer'],prop)
        if key not in permits:raise ValueError('revision_scope_exceeded')
        if key in seen:raise ValueError('revision_duplicate_target')
        seen.add(key)
        try:layer=project['snapshot']['compositions'][str(op['comp'])]['layers'][str(params['layer'])]
        except KeyError:raise ValueError('revision_scope_unavailable') from None
        matches=[node for node in nodes(layer['properties']) if node.get('path')==prop and 'value' in node]
        if len(matches)!=1 or type(matches[0].get('uid')) is not int:raise ValueError('revision_property_unavailable')
        if matches[0].get('keys'):raise ValueError('animated_property_requires_time_scope')
        targets.append({'comp':op['comp'],'layer':params['layer'],'path':prop,'uid':matches[0]['uid']})
    load('task_store').canonical(plan)
    return targets


def assert_preserved(before,after,uids,before_assets,after_assets,text_uids=None):
    """比较完整原生工程；仅排除授权属性value和已核对素材位置。"""
    text_uids=text_uids or set()
    def normalized(value,assets):
        value=copy.deepcopy(value)
        for key,item in value['items'].items():
            if item['kind']['type']=='Footage':
                if key not in assets:raise ValueError('non_target_changed: missing asset identity')
                item['kind']['path']={'verifiedSha256':assets[key]['sha256']}
        found=set()
        def walk(node):
            if isinstance(node,dict):
                if node.get('uid') in uids and 'value' in node:
                    uid=node['uid']
                    if uid in found:raise ValueError('non_target_changed: duplicate property uid')
                    found.add(uid)
                    if uid in text_uids:
                        value=node['value']
                        if not isinstance(value,dict) or value.get('t')!='Text' or 'v' not in value:raise ValueError('non_target_changed: text format')
                        if isinstance(value['v'],dict):
                            if 'text' not in value['v']:raise ValueError('non_target_changed: text missing')
                            value['v']['text']='<authorized-text>'
                        elif isinstance(value['v'],str):value['v']='<authorized-text>'
                        else:raise ValueError('non_target_changed: text format')
                    else:node['value']='<authorized-value>'
                for child in node.values():walk(child)
            elif isinstance(node,list):
                for child in node:walk(child)
        walk(value)
        if found!=uids:raise ValueError('non_target_changed: property missing')
        return value
    if normalized(before,before_assets)!=normalized(after,after_assets):raise ValueError('non_target_changed')


def resolved_scope(store,root):
    """仅从原任务不可变成功回执解析创建别名，不相信后续自报的ID。"""
    delivery=load('command_delivery');delivery.document(store,root['taskId'])
    receipt=delivery.read(Path(root['output'])/'success.json');aliases={}
    for index,op in enumerate(root['plan']['operations']):
        if op.get('as'):
            step=receipt['steps'][index]
            if step['index']!=index or step['state']!='succeeded':raise ValueError('revision_scope_unavailable')
            aliases[op['as']]=step['result']
    scope=validate_scope(root['plan'],root['identity']['authorization'].get('revisionScope',[]))
    try:return [dict(row,comp=aliases[row['comp']]['comp'],layer=aliases[row['layer']]['layer']) for row in scope]
    except (KeyError,TypeError):raise ValueError('revision_scope_unavailable') from None


def prepare(store,state,plan,output,child,allowed,check_output=True,generator_version=2):
    """生成真实重开/保存/渲染计划；原件只读，素材以原摘要复制。"""
    tasks=load('task_store');delivery=load('command_delivery');commands=load('commands')
    if generator_version not in (1,2):raise ValueError('revision_generator_unsupported')
    data=delivery.document(store,state['taskId']);projects=data['projects']
    selected=next((p for p in projects if p['path']==plan['project']),None)
    if selected is None:raise ValueError('revision_project_unavailable')
    targets=validate_plan(plan,selected,allowed);inputs={};assets={};seeds={};contents={};operations=[];assignments={}
    output=Path(output).absolute()
    for p in projects:
        commands.output_path(p['path'])
        for asset in p['dependencies'].values():
            key=(asset['path'],asset['sha256'])
            if key in assets:continue
            name='revisionAsset'+format(len(assets),'04d');source=load('quality_review').contained(Path(state['output']),asset['path'])
            if tasks.file_sha(source)!=asset['sha256']:raise ValueError('command_dependency_changed')
            inputs[name]=str(source);assets[key]=str(output/'inputs'/(name+source.suffix))
    for frame in data['frames']:
        commands.output_path(frame['path'])
        candidates=[p for p in projects if all(p[k]==frame[k] for k in ('snapshot','nativeVersion','dependencies'))]
        if not candidates:raise ValueError('revision_frame_source_unavailable')
        owner=selected if selected in candidates else candidates[0];assignments[frame['path']]=owner['path']
    for index,p in enumerate(projects):
        seed=store.path(child).parent/'revision-inputs'/(str(index)+'.ecproj');native=delivery.read(Path(state['output'])/p['path'])
        for item,asset in p['dependencies'].items():native['items'][item]['kind']['path']=assets[(asset['path'],asset['sha256'])]
        content=tasks.canonical(native);contents[str(seed)]=content
        import hashlib
        seeds[str(seed)]=hashlib.sha256(content).hexdigest()
        operations.append({'tool':'open_project','params':{'path':str(seed)}})
        if p['path']==selected['path']:
            for op in plan['operations']:
                operations.append({'command':'comp.open','params':{'comp':op['comp']}})
                if generator_version==2:operations.append({'command':'layer.select','params':{'layers':[op['params']['layer']]}})
                operations.append({'command':op['command'],'params':copy.deepcopy(op['params'])})
        operations.append({'tool':'save_project','params':{'path':{'$output':p['path']}}})
        for frame in data['frames']:
            if assignments[frame['path']]!=p['path']:continue
            operations.append({'tool':'render_frame','params':{'comp':frame['composition']['id'],'time':frame['seconds'],
                'max_side':frame['maxSide'],'transparent':frame['requestedAlpha'],'inline':bool(frame.get('inlineCopies')),
                'path':{'$output':frame['path']}}})
    generated={'schema':'craft-command-plan/v1','operations':operations}
    commands.validate(generated,inputs,'bridge' if state['identity']['mode']=='desktop' else 'headless')
    if check_output:load('managed').preflight(generated,output,state['identity']['mode'],inputs)
    context={'sourceTask':state['taskId'],'sourceBinding':plan['binding'],'revision':copy.deepcopy(plan),
             'targets':targets,'seeds':seeds,'frames':assignments}
    if generator_version==2:context['generatorVersion']=2
    return generated,inputs,context,contents


def validate_prepared(store,task,runtime_home=None,for_reconcile=False):
    """恢复只核对原请求及私有种子，不再生成新基线或发送编辑。"""
    tasks=load('task_store');managed=load('managed');state=store.read(task)
    request=managed.read(store.path(task).parent/'request.json')
    if tasks.digest(request)!=state['identity']['authorization']['requestHash']:raise ValueError('request_changed')
    context=request.get('commandRevision')
    if not context:raise ValueError('revision_context_missing')
    source=store.read(context['sourceTask']);root=store.lineage(source)[-1]
    if state['parent']!=root['taskId'] or state['identity']['mode']!=source['identity']['mode'] or state['identity']['runtimeSha256']!=source['identity']['runtimeSha256']:
        raise ValueError('revision_identity_changed')
    if root.get('activeRevision')!=task:raise ValueError('revision_owner_changed')
    if for_reconcile:store.check_resources(state)
    else:store.allowed(state)
    quality=load('command_judge').Quality(store,source['taskId'])
    if quality.binding(source['output'])!=context['sourceBinding']:raise ValueError('artifact_changed')
    generated,inputs,expected,contents=prepare(store,source,context['revision'],state['output'],task,resolved_scope(store,root),check_output=False,generator_version=context.get('generatorVersion',1))
    if generated!=state['plan'] or inputs!=request['inputs'] or context!=expected:raise ValueError('revision_context_changed')
    for path,sha in context['seeds'].items():
        p=Path(path)
        if p.is_symlink() or not p.resolve().is_relative_to((store.path(task).parent/'revision-inputs').resolve()):raise ValueError('revision_seed_changed')
        try:actual=tasks.file_sha(p)
        except (ValueError,OSError):raise ValueError('revision_seed_changed') from None
        if actual!=sha:raise ValueError('revision_seed_changed')
    if runtime_home is not None:
        report=load('command_delivery').inspect(store,source['taskId'],runtime_home)
        if report['technical']['status']!='PASS' or report['engineering']['status']!='PASS':raise ValueError('engineering_gate')
    return context


def revise(store,task,plan,output,runtime_home):
    """先验证当前失败评价和原生门禁，再登记唯一子任务及共享预算。"""
    import uuid
    tasks=load('task_store');managed=load('managed');state=store.read(task);root=store.lineage(state)[-1]
    if state['identity']['mode'] not in ('commands','desktop') or state['state']!='review_ready' or not state.get('review'):raise ValueError('review_required')
    review=store.path(task).parent/state['review']['path']
    if tasks.file_sha(review)!=state['review']['sha256']:raise ValueError('review_changed')
    report=managed.read(review);request=managed.read(store.path(task).parent/'judge-request.json')
    ledger=load('review_ledger').validate(store,root,tasks.digest(request['criteria']))
    if task not in ledger['entries'] or ledger['entries'][task]['reportSha256']!=state['review']['sha256']:raise ValueError('settled_review_required')
    if report['technical']['status']!='PASS' or report['engineering']['status']!='PASS' or report['creative']['status']!='FAIL':raise ValueError('failed_creative_review_required')
    # 不为旧任务补造已用资源；缺少根任务真实帧计量时仅允许检查。
    root_delivery=load('command_delivery').document(store,root['taskId'])
    entry=root.get('resources',{}).get('entries',{}).get(root['taskId'],{})
    frames=entry.get('commandFrames',{})
    if (entry.get('bindingHash')!=root['identity']['planHash'] or not root_delivery['frames']
            or any(frames.get(frame['operationHash'])!={'frames':1,'decodedBytes':frame['composition']['width']*frame['composition']['height']*4}
                for frame in root_delivery['frames'])):raise ValueError('legacy_command_resource_read_only')
    binding=load('command_judge').Quality(store,task).binding(state['output'])
    if binding!=report['binding']:raise ValueError('artifact_changed')
    if plan.get('binding')!=binding:raise ValueError('revision_conflict')
    allowed=resolved_scope(store,root);child=uuid.uuid4().hex
    generated,inputs,context,contents=prepare(store,state,plan,output,child,allowed)
    def budget():
        current=store.read(root['taskId']);store.allowed(current)
        if current['budget']['revisions']>=2 or current['budget']['stagnant']>=2:raise ValueError('revision_budget_exhausted')
        if current.get('activeRevision'):raise ValueError('revision_in_progress')
        return current
    with store.lock():budget()
    fresh=load('command_delivery').inspect(store,task,runtime_home)
    if fresh['engineering']['status']!='PASS':raise ValueError('engineering_gate')
    if fresh['technical']['status']!='PASS' or fresh.get('binding')!=binding:raise ValueError('artifact_changed')
    with store.lock():
        current=budget();current['budget']['revisions']+=1;current['activeRevision']=child;store.save(current)
    # 预算先于任何子任务写入持久化，失败不退轮数、不换ID重试。
    request={'inputs':inputs,'source':None,'commandRevision':context}
    source=Path(state['output'])/plan['project']
    execution,manifest=load('runtime_binding').prepare(Path(__file__).resolve().parent.parent,runtime_home)
    store.create(child,plan=generated,output=str(output),runtime_sha=state['identity']['runtimeSha256'],
        inputs={k:tasks.file_sha(v) for k,v in inputs.items()},source=str(source),mode=state['identity']['mode'],
        authorization={'writeRoot':str(Path(output).absolute()),'inputs':inputs,'requestHash':tasks.digest(request)},parent=root['taskId'],runtime_binding=execution)
    tasks.atomic_json(store.path(child).parent/'request.json',request)
    for path,content in contents.items():
        p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('xb') as f:f.write(content)
    load('runtime_binding').freeze(store,child,Path(__file__).resolve().parent.parent,manifest)
    validate_prepared(store,child)
    result=managed.supervise(store,child,runtime_home)
    if result['state']=='review_ready':
        return settle_completed(store,child)
    return result


def prepare_output(store,task,output):
    """在原生会话创建前登记全量重渲染资源，不复用旧渲染观察。"""
    context=validate_prepared(store,task);state=store.read(task)
    if Path(output).absolute()!=Path(state['output']):raise ValueError('revision_output_changed')
    source=store.read(context['sourceTask']);data=load('command_delivery').document(store,source['taskId'])
    frames=data['frames'];decoded=sum(frame['composition']['width']*frame['composition']['height']*4 for frame in frames)
    store.reserve_resources(task,{'frames':len(frames),'decodedBytes':decoded},load('task_store').digest(context))
    for row in data['projects']+frames:
        name=load('commands').output_path(row['path'])
        (Path(output)/name).parent.mkdir(parents=True,exist_ok=True)


def assert_media_preserved(before,after):
    """比较实际RGBA解码像素；不支持的PNG要求完整字节一致。"""
    try:
        a=load('image_sequence').rgba_facts(before);b=load('image_sequence').rgba_facts(after)
        if any(a.get(k)!=b.get(k) for k in ('width','height','rgbaSha256')):raise ValueError('non_target_media_changed')
    except (ValueError,OSError) as error:
        if str(error)=='non_target_media_changed':raise
        load('png_inspection').inspect_png(before);load('png_inspection').inspect_png(after)
        if load('task_store').file_sha(before)!=load('task_store').file_sha(after):raise ValueError('non_target_media_changed')


def validate_result(store,task,proof=None,runtime_home=None,for_reconcile=False):
    """交付前核对源仍未变、全原生字段及未受影响媒体；失败保留现场。"""
    tasks=load('task_store');delivery=load('command_delivery');managed=load('managed')
    context=validate_prepared(store,task,for_reconcile=for_reconcile);state=store.read(task);source=store.read(context['sourceTask'])
    before=delivery.document(store,source['taskId']);after=delivery.document(store,task,proof)
    old={p['path']:p for p in before['projects']};new={p['path']:p for p in after['projects']}
    if set(old)!=set(new):raise ValueError('non_target_changed: project inventory')
    targets=context['targets'];selected=context['revision']['project']
    for name,p in old.items():
        a=managed.read(Path(source['output'])/name);b=managed.read(Path(state['output'])/name)
        text_addresses={(op['comp'],op['params']['layer']) for op in context['revision']['operations'] if op['command']=='layer.setText'}
        text_uids={row['uid'] for row in targets if (row['comp'],row['layer']) in text_addresses and row['path']=='text/sourceText'} if name==selected else set()
        assert_preserved(a,b,{row['uid'] for row in targets} if name==selected else set(),p['dependencies'],new[name]['dependencies'],text_uids)
    old_frames={f['path']:f for f in before['frames']};new_frames={f['path']:f for f in after['frames']}
    if set(old_frames)!=set(new_frames):raise ValueError('non_target_media_changed: frame inventory')
    for name,frame in old_frames.items():
        actual=new_frames[name]
        for field in ('composition','seconds','maxSide','requestedAlpha'):
            if actual[field]!=frame[field]:raise ValueError('non_target_media_changed: render contract')
        if context['frames'][name]!=selected or frame['composition']['id'] not in {row['comp'] for row in targets}:
            assert_media_preserved(Path(source['output'])/name,Path(state['output'])/name)
        else:
            load('png_inspection').inspect_png(Path(state['output'])/name)
    if runtime_home is not None:
        lock=managed.read(Path(__file__).with_name('runtime.lock.json'));expected=lock['artifacts'][load('platform_support').platform_key()]
        installed=load('bootstrap').inspect_install(Path(runtime_home)/'effectcraft'/lock['resolvedVersion'],lock['artifact'],expected,lock['resolvedVersion'],load('platform_support').platform_key())
        report=delivery.verify_projects(Path(state['output']),after['projects'],installed['executable'])
        if report['status']!='PASS':raise ValueError('engineering_gate: '+str(report))
    # 后续核对只能读取已生成的证据，不能因缺失而重新保存原工程。
    delivery.document(store,source['taskId']);delivery.document(store,task,proof)
    result={'schema':'effectcraft-command-preservation/v1','taskId':task,'sourceTask':source['taskId'],
            'sourceBinding':context['sourceBinding'],'deliverySha256':tasks.file_sha(delivery.directory(store,task)/'delivery.json'),
            'targets':targets,'projects':sorted(old),'frames':sorted(old_frames),'status':'PASS'}
    load('review_ledger').immutable(store.path(task).parent/'preservation.json',result)
    return result


def settle_completed(store,task):
    """监督器退出后仅核对既有保全回执；缺回执或进程证明保持占用。"""
    managed=load('managed');tasks=load('task_store');platform=load('platform_support')
    with platform.exclusive_lock(store.root/'leases'/(task+'.lifecycle.lock'),timeout=0), platform.exclusive_lock(store.root/'leases'/(task+'.lock'),timeout=0):
        state=store.read(task);request=managed.read(store.path(task).parent/'request.json')
        if not request.get('commandRevision'):return state
        root=store.lineage(state)[-1]
        if root.get('activeRevision') is None:return state
        if state['state']!='review_ready' or root.get('activeRevision')!=task:raise ValueError('revision_in_progress')
        lifecycle=store.lifecycle_path(state)
        if not lifecycle.is_file():raise ValueError('process_termination_unconfirmed')
        stopped=managed.read(lifecycle)
        if stopped.get('schema')!='effectcraft-process-lifecycle/v1' or stopped.get('status')!='stopped':raise ValueError('process_termination_unconfirmed')
        path=store.path(task).parent/'preservation.json'
        if not path.is_file():raise ValueError('preservation_receipt_missing')
        sha=tasks.file_sha(path);validate_result(store,task,for_reconcile=True)
        if tasks.file_sha(path)!=sha:raise ValueError('preservation_receipt_changed')
        with store.lock():
            latest=store.read(task);root=store.read(root['taskId']);store.check_resources(latest)
            if latest['delivery']!=state['delivery'] or latest['state']!='review_ready' or root.get('activeRevision')!=task:raise ValueError('revision_owner_changed')
            root['activeRevision']=None;store.save(root)
        return store.read(task)


def prove_not_executed(store,task):
    """仅证明注册表阻断前没有编辑调用；不重放、不退款、不重写原计划。"""
    import hashlib,json
    tasks=load('task_store');managed=load('managed');commands=load('commands');delivery=load('command_delivery');platform=load('platform_support')
    with platform.exclusive_lock(store.root/'leases'/(task+'.lifecycle.lock'),timeout=0), platform.exclusive_lock(store.root/'leases'/(task+'.lock'),timeout=0):
        state=store.read(task);request=managed.read(store.path(task).parent/'request.json')
        if not request.get('commandRevision'):return state
        settling=state['state']=='failed' and state.get('reconciliation',{}).get('result')=='revision_not_executed'
        if state['state']!='reconciling' and not settling:return state
        if settling:
            root=store.lineage(state)[-1]
            if root.get('activeRevision') is None:return state
            proof_path=store.path(task).parent/'not-executed.json'
            reference=state['reconciliation'].get('proof',{})
            try:
                if reference.get('path')!=proof_path.name or tasks.file_sha(proof_path)!=reference.get('sha256'):
                    raise ValueError('revision_not_executed_proof_changed')
            except (OSError,ValueError):raise ValueError('revision_not_executed_proof_changed') from None
        lifecycle=store.lifecycle_path(state)
        if not lifecycle.is_file() or managed.read(lifecycle).get('status')!='stopped':raise ValueError('process_termination_unconfirmed')
        if managed.read(lifecycle).get('schema')!='effectcraft-process-lifecycle/v1':raise ValueError('process_termination_unconfirmed')
        context=validate_prepared(store,task,for_reconcile=True);output=Path(state['output'])
        try:
            receipt=managed.read(output/'failure.json');journal=managed.read(output/'journal.json')
        except (OSError,ValueError):raise ValueError('revision_outcome_unknown: missing or invalid failure receipts') from None
        expected_sha=hashlib.sha256(json.dumps(state['plan'],ensure_ascii=False,sort_keys=True,allow_nan=False).encode()).hexdigest()
        if (receipt!=journal or receipt.get('schema')!='craft-command-receipt/v1' or receipt.get('pluginId')!='effectcraft'
                or receipt.get('result')!='FAIL' or receipt.get('planSha256')!=expected_sha
                or receipt.get('runtimeSha256')!=state['identity']['runtimeSha256']
                or receipt.get('mode')!=('bridge' if state['identity']['mode']=='desktop' else 'headless')
                or receipt.get('error')!=state.get('error') or (output/'success.json').exists()):raise ValueError('revision_outcome_unknown')
        rows=receipt.get('steps',[])
        if not rows or rows[-1].get('state')!='blocked':raise ValueError('revision_outcome_unknown')
        catalog=commands.ROUTES['effectcraft'][0];calls=[(catalog,{},None)]
        for index,row in enumerate(rows):
            if index>=len(state['plan']['operations']):raise ValueError('revision_outcome_unknown')
            op=state['plan']['operations'][index]
            if (row.get('index')!=index or row.get('command')!=op.get('command') or row.get('tool')!=op.get('tool')
                    or row.get('params')!=op['params']):raise ValueError('revision_outcome_unknown')
            if op.get('command'):calls.append((catalog,{'filter':op['command']},None))
            if index==len(rows)-1:
                if not op.get('command') or op['command'] not in ('layer.setText','prop.set','layer.select','comp.open'):raise ValueError('revision_outcome_unknown')
                if receipt['error']!='precondition_failed: '+op['command']+': '+str(row.get('reason')):raise ValueError('revision_outcome_unknown')
                break
            if row.get('state')!='succeeded':raise ValueError('revision_outcome_unknown')
            if op.get('tool')=='open_project':tool,args=op['tool'],op['params']
            elif op.get('command') in ('comp.open','layer.select'):tool,args=commands.native_call(op['command'],op['params'])
            else:raise ValueError('revision_outcome_unknown')
            calls.append((tool,args,tasks.digest(row['result'])))
        if len(calls)!=len(state['steps']):raise ValueError('revision_outcome_unknown')
        for (tool,args,result_sha),step in zip(calls,state['steps']):
            if (step['state']!='succeeded' or step['operation']!=tool
                    or step['argumentsHash']!=tasks.digest({'name':tool,'arguments':args})
                    or (result_sha is not None and step['resultHash']!=result_sha)):raise ValueError('revision_outcome_unknown')
        expected_inputs={'inputs/'+name+Path(path).suffix:state['identity']['inputHashes'][name] for name,path in request['inputs'].items()}
        if delivery.inventory(output)!=expected_inputs:raise ValueError('revision_outcome_unknown')
        source=store.read(context['sourceTask']);delivery.document(store,source['taskId'])
        proof={'schema':'effectcraft-command-not-executed/v1','taskId':task,'sourceBinding':context['sourceBinding'],
            'planHash':state['identity']['planHash'],'stepsHash':tasks.digest(state['steps']),
            'failureSha256':tasks.file_sha(output/'failure.json'),'journalSha256':tasks.file_sha(output/'journal.json'),
            'lifecycleSha256':tasks.file_sha(lifecycle),'seeds':context['seeds'],'result':'revision_not_executed'}
        path=store.path(task).parent/'not-executed.json';load('review_ledger').immutable(path,proof)
        with store.lock():
            latest=store.read(task);root=store.lineage(latest)[-1];store.check_resources(latest)
            if latest['steps']!=state['steps'] or latest['state']!=state['state'] or latest.get('reconciliation')!=state.get('reconciliation') or root.get('activeRevision')!=task:raise ValueError('revision_owner_changed')
            latest['state']='failed';latest['reconciliation']={'result':'revision_not_executed','automaticReplay':False,
                'proof':{'path':path.name,'sha256':tasks.file_sha(path)},'requiredAction':'inspect original task; another authorized revision uses remaining shared budget'}
            store.save(latest);root['activeRevision']=None;store.save(root)
        return store.read(task)
