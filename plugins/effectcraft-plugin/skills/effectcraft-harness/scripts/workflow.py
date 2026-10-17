#!/usr/bin/env python3
"""持续 MCP 会话中的原生合成、动画与渲染计划。"""
import argparse
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

def exchange_report(root,outputs,warnings):
    spec=importlib.util.spec_from_file_location('craft_exchange_loss',Path(__file__).with_name('exchange_loss.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.write_report(root,outputs,warnings)

ALLOWED = {'native.command', 'asset.import', 'asset.replace', 'layer.addItem', 'layer.newText', 'layer.newShape', 'layer.newSolid', 'layer.setText',
           'layer.select', 'layer.setParent', 'prop.set', 'prop.addKey',
           'keys.select', 'keys.easyEase', 'keys.interpolation', 'mask.new', 'mask.setVertex', 'mask.remove',
           'effect.apply', 'effect.remove', 'effect.toggle', 'comp.settings', 'comp.workArea'}

PARAMETER_COMMANDS = {'effect.apply', 'effect.remove', 'effect.toggle', 'mask.new', 'mask.setVertex', 'mask.remove'}


def parameter_contract():
    """读取本技能内由固定 CLI 反射得到的字段合同，并绑定已校验制品身份。"""
    folder = Path(__file__).parent
    contract = json.loads((folder / 'parameter-contract.json').read_text(encoding='utf-8'))
    lock = json.loads((folder / 'runtime.lock.json').read_text(encoding='utf-8'))
    spec=importlib.util.spec_from_file_location('workflow_platform',folder/'platform_support.py')
    support=importlib.util.module_from_spec(spec);spec.loader.exec_module(support)
    key=support.platform_key()
    if (contract.get('schema') != 'effectcraft-parameter-contract/v1'
            or contract.get('runtimeVersion') != lock['resolvedVersion']
            or contract.get('runtimeSha256ByPlatform', {}).get(key) != lock['artifacts'][key]['binarySha256']
            or set(contract.get('commands', {})) != PARAMETER_COMMANDS):
        raise ValueError('parameter_contract_identity_mismatch')
    return contract['commands']


def verify_parameter_contracts(call, schemas):
    """只读反射在工程打开或创建之前执行；能力漂移不得继续编辑。"""
    for command, schema in schemas.items():
        observed = call('describe_command', {'command': command})
        if observed.get('id') != command or observed.get('schema') != schema:
            raise ValueError('parameter_schema_mismatch: ' + command)

def command_error(name, args, content):
    """只归类固定引擎在效果/蒙版命令执行前返回的参数校验错误。"""
    command = args.get('command')
    mapped = {'effect.apply', 'effect.remove', 'effect.toggle', 'mask.new', 'mask.setVertex', 'mask.remove'}
    if name == 'execute_command' and command in mapped and len(content) == 1:
        item = content[0]
        text = item.get('text')
        if item.get('type') == 'text' and isinstance(text, str) and text.startswith(f'invalid parameters for `{command}`:'):
            return ValueError(f'unsupported_mapping: {command}: {text}')
    return RuntimeError('command_failed: ' + name + ': ' + json.dumps(content))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def resolve(value, bindings):
    if isinstance(value, dict):
        if set(value) == {'$ref'}:
            try:
                parts = value['$ref'].split('.')
                result = bindings[parts[0]]
                for field in parts[1:]:
                    result = result[int(field)] if isinstance(result, list) else result[field]
                return result
            except (KeyError, IndexError, TypeError, ValueError, AttributeError):
                raise ValueError('unresolved_reference: ' + str(value['$ref'])) from None
        return {key: resolve(item, bindings) for key, item in value.items()}
    if isinstance(value, list):
        return [resolve(item, bindings) for item in value]
    return value


def load_module(name):
    spec = importlib.util.spec_from_file_location('craft_' + name, Path(__file__).with_name(name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def native_module():
    spec = importlib.util.spec_from_file_location('craft_native_workflow', Path(__file__).with_name('native_workflow.py'))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def validate(plan):
    if not isinstance(plan, dict) or not isinstance(plan.get('operations'), list):
        raise ValueError('operations_required')
    aliases = set()
    schemas = {}
    contract = parameter_contract() if any(isinstance(item, dict) and item.get('command') in PARAMETER_COMMANDS for item in plan['operations']) else {}
    for item in plan['operations']:
        if not isinstance(item, dict):
            raise ValueError('invalid_operation')
        if item.get('command') == 'native.command':
            native_module().validate(item.get('params'))
        if item.get('command') not in ALLOWED:
            raise ValueError('unsupported_command')
        alias = item.get('as')
        if alias is not None:
            if alias in aliases:
                raise ValueError('duplicate_alias')
            if not isinstance(alias, str) or not re.fullmatch(r'[a-zA-Z][\w-]*', alias):
                raise ValueError('invalid_alias')
            aliases.add(alias)
        if not isinstance(item.get('params', {}), dict):
            raise ValueError('invalid_params')
        command = item['command']
        if command in contract:
            schema = contract[command]
            params = item.get('params', {})
            # 原生 check_params 允许 comp/merge 及 layer/layers 互为别名；字段值中的
            # $ref 保留到会话绑定阶段，不凭静态字段检查推断实际图层或属性存在。
            accepted = set(schema['properties']) | {'comp', 'merge'}
            if accepted & {'layer', 'layers'}:
                accepted |= {'layer', 'layers'}
            unknown = sorted(set(params) - accepted)
            if unknown:
                raise ValueError('unsupported_mapping: ' + command + ': unknown parameter(s) ' + ', '.join(unknown))
            missing = sorted(set(schema['required']) - set(params))
            if missing:
                raise ValueError('unsupported_mapping: ' + command + ': missing parameter(s) ' + ', '.join(missing))
            schemas[command] = schema
    if not isinstance(plan.get('exports', []), list) or len(plan.get('exports', [])) > 1:
        raise ValueError('invalid_export')
    for export in plan.get('exports', []):
        if not isinstance(export, dict) or set(export)-{'format','chunkFrames'} or export.get('format') not in ('mp4','png-sequence','png-segmented'):
            raise ValueError('invalid_export')
        if 'chunkFrames' in export and (export['format']!='png-segmented' or type(export['chunkFrames']) is not int or not 1<=export['chunkFrames']<=10000):
            raise ValueError('invalid_export')
    if type(plan.get('previewAlpha',True)) is not bool:
        raise ValueError('preview_alpha_must_be_boolean')
    for value in plan.get('frames', [0]):
        if type(value) not in (int, float) or not 0 <= value <= 3600:
            raise ValueError('invalid_frame_time')
    if 'document' in plan:
        doc = plan['document']
        if set(doc) - {'name', 'width', 'height', 'frameRate', 'duration', 'background'}:
            raise ValueError('unsupported_document_setting')
        for field in ('width', 'height'):
            if type(doc.get(field)) is not int or not 0 < doc[field] <= 16384:
                raise ValueError('invalid_document_size')
        for field, limit in [('frameRate', 240), ('duration', 3600)]:
            if type(doc.get(field)) not in (int, float) or not 0 < doc[field] <= limit:
                raise ValueError('invalid_document_timing')
    contract_module=load_module('composition_contract')
    if 'workArea' in plan and plan['workArea'] is None:raise ValueError('invalid_work_area')
    if 'document' in plan:contract_module.document(plan['document'],plan.get('workArea'))
    elif 'workArea' in plan:
        if not isinstance(plan['workArea'],list) or len(plan['workArea'])!=2 or not all(contract_module.number(v) for v in plan['workArea']) or not 0<=plan['workArea'][0]<plan['workArea'][1]:raise ValueError('invalid_work_area')
    return schemas


def execute(plan, output, runtime_home=None, source=None, task_hooks=None):
    return _execute(plan, output, runtime_home, source, {'output': False}, task_hooks)


def _execute(plan, output, runtime_home, source, owned, task_hooks=None):
    schemas = validate(plan)
    output = Path(output).absolute()
    output = output.parent.resolve()/output.name
    if output.exists() or output.is_symlink():
        raise ValueError('output_exists')
    source_project, source_hash = None, None
    bindings = {}
    inherited = {}
    source_artifact = None
    if source:
        source = Path(source).resolve()
        source_artifact = load_module('artifact_lineage').source_ref(source)
        source_project = source / 'project.ecproj'
        if source_project.is_symlink():
            raise ValueError('invalid_source')
        prior = json.loads((source / 'manifest.json').read_text(encoding='utf-8'))
        source_hash = sha(source_project)
        if source_hash != prior['files']['project.ecproj'] or source_hash != plan.get('expectedProjectSha256'):
            raise ValueError('revision_conflict')
        if 'document' in plan:
            raise ValueError('revision_cannot_recreate_document')
        bindings = prior['bindings']
        inherited = prior.get('assets', {})
    elif 'document' not in plan:
        raise ValueError('document_required')
    composition_contract=load_module('composition_contract')
    expected_composition=(composition_contract.observed(json.loads((source/'native.json').read_text(encoding='utf-8'))['composition']) if source_project else composition_contract.document(plan['document']))
    if 'workArea' in plan:expected_composition['workArea']=composition_contract.area(plan['workArea'],expected_composition)
    # 输入失败须在安装、输出占用及保留暂存前返回；复制后仍复核以发现并发变化。
    for alias, asset in inherited.items():
        path = (source / asset['path']).resolve()
        if not path.is_relative_to(source):
            raise ValueError('invalid_asset_path')
        if not path.is_file() or sha(path) != asset['sha256']:
            raise ValueError('asset_digest_mismatch: ' + alias)
    for alias, asset in plan.get('assets', {}).items():
        if alias in inherited:
            raise ValueError('asset_alias_exists')
        path = Path(asset['path'])
        if path.is_symlink() or not path.is_file() or sha(path) != asset['sha256']:
            raise ValueError('asset_digest_mismatch: ' + alias)
    installed = load_module('bootstrap').install(json.loads(Path(__file__).with_name('runtime.lock.json').read_text(encoding='utf-8')),
        runtime_home or os.environ.get('CRAFT_RUNTIME_HOME', str(Path.home() / '.local/share/craft-runtimes')))
    cli = installed['executable']
    output.parent.mkdir(parents=True, exist_ok=True)
    execution_identity = {'planHash': hashlib.sha256(json.dumps(plan, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest(),
                         'inputHashes': {name: asset['sha256'] for name, asset in {**inherited, **plan.get('assets', {})}.items()},
                         'projectRevision': source_hash, 'runtimeSha256': installed['binarySha256']}
    with load_module('output_guard').claim(output, execution_identity), load_module('preserved_stage').preserved_stage(output, '.effectcraft-', owned) as temporary:
        stage = Path(temporary)
        project = stage / 'project.ecproj'
        working = stage
        assets = {}
        def copy_asset(alias, path, digest):
            if not re.fullmatch(r'[a-zA-Z][\w-]*', alias) or not re.fullmatch(r'[a-f0-9]{64}', digest):
                raise ValueError('invalid_asset')
            path = Path(path)
            if path.is_symlink() or not path.is_file() or sha(path) != digest:
                raise ValueError('asset_digest_mismatch: ' + alias)
            destination = working / 'assets' / (alias + path.suffix.lower())
            destination.parent.mkdir(exist_ok=True)
            if destination.exists():
                raise ValueError('duplicate_asset')
            shutil.copyfile(path, destination)
            if sha(destination) != digest:
                raise ValueError('asset_changed_during_copy')
            return destination
        for alias, asset in inherited.items():
            path = (source / asset['path']).resolve()
            if not path.is_relative_to(source):
                raise ValueError('invalid_asset_path')
            assets[alias] = dict(asset, staging=str(copy_asset(alias, path, asset['sha256'])))
        for alias, asset in plan.get('assets', {}).items():
            if alias in assets:
                raise ValueError('asset_alias_exists')
            assets[alias] = {'sha256': asset['sha256'], 'staging': str(copy_asset(alias, asset['path'], asset['sha256']))}
        receipts = []
        owned['operations'] = receipts
        with (task_hooks.session if task_hooks else load_module('mcp_session').Session)([cli, '--empty', 'mcp']) as session:
            def call(name, args):
                owned['lastAttempt'] = {'tool': name, 'arguments': args, 'phase': 'submitted'}
                result = session.request('tools/call', {'name': name, 'arguments': args})
                owned['lastAttempt']['phase'] = 'reply_received'
                if result.get('isError'):
                    raise command_error(name, args, result['content'])
                text = [x['text'] for x in result.get('content', []) if x.get('type') == 'text']
                if len(text) != 1:
                    raise RuntimeError('unexpected_result')
                value = json.loads(text[0])
                receipts.append({'tool': name, 'arguments': args, 'result': value})
                return value
            verify_parameter_contracts(call, schemas)
            if source_project:
                call('open_project', {'path': str(source_project)})
                baseline=call('get_comp',{'comp':bindings['composition']['comp']})
                composition_contract.verify(composition_contract.observed(json.loads((source/'native.json').read_text(encoding='utf-8'))['composition']),baseline)
                for asset in assets.values():
                    if 'item' in asset:
                        call('execute_command', {'command': 'file.replaceFootage', 'params': {'item': asset['item'], 'path': asset['staging']}})
            else:
                bindings['composition'] = call('execute_command', {'command': 'comp.new', 'params': plan['document']})
            if not source_project:
                call('execute_command',{'command':'comp.workArea','params':{'comp':bindings['composition']['comp'],'start':0,'end':expected_composition['duration']}})
            for operation in plan['operations']:
                params = resolve(operation.get('params', {}), bindings)
                configuration_command=params['command'] if operation['command']=='native.command' else operation['command']
                configuration_params=params['params'] if operation['command']=='native.command' else params
                current_time=None
                if configuration_command=='comp.workArea' and configuration_params.get('set') in ('begin','end'):
                    current_time=composition_contract.current_time(call('get_state',{}))
                expected_composition=composition_contract.updated(expected_composition,configuration_command,configuration_params,bindings['composition']['comp'],current_time=current_time)
                if operation['command'] == 'native.command':
                    result = native_module().execute(session, params, owned, receipts, stage)
                elif operation['command'] == 'asset.import':
                    asset = assets[params['asset']]
                    if 'item' in asset:
                        raise ValueError('asset_already_imported')
                    imported = call('execute_command', {'command': 'file.import', 'params': {'paths': [asset['staging']]}})
                    if imported['errors'] or len(imported['items']) != 1:
                        raise ValueError('asset_import_failed')
                    asset['item'] = imported['items'][0]
                    result = {'item': asset['item']}
                elif operation['command'] == 'asset.replace':
                    alias, replacement = params['asset'], params['replacement']
                    if alias == replacement or 'item' not in assets[alias] or 'item' in assets[replacement]:
                        raise ValueError('invalid_asset_replacement')
                    updated = assets.pop(replacement)
                    updated['item'] = assets[alias]['item']
                    call('execute_command', {'command': 'file.replaceFootage', 'params': {'item': updated['item'], 'path': updated['staging']}})
                    assets[alias] = updated
                    result = {'item': updated['item']}
                else:
                    if operation['command'] == 'layer.addItem' and params.get('item') not in {asset.get('item') for asset in assets.values()}:
                        raise ValueError('registered_asset_required')
                    result = call('execute_command', {'command': operation['command'], 'params': params})
                if operation.get('as'):
                    if operation['as'] in bindings:
                        raise ValueError('alias_already_exists')
                    bindings[operation['as']] = result
            if 'workArea' in plan:
                expected_composition['workArea']=composition_contract.area(plan['workArea'],expected_composition)
                call('execute_command',{'command':'comp.workArea','params':{'comp':bindings['composition']['comp'],'start':expected_composition['workArea'][0],'end':expected_composition['workArea'][1]}})
            comp = call('get_comp', {'comp': bindings['composition']['comp']})
            composition_validation=composition_contract.verify(expected_composition,comp)
            if plan.get('exports'):
                overview = call('get_project', {})
                if sum(item.get('name') == comp['name'] for item in overview['items']) != 1:
                    raise ValueError('ambiguous_composition_name')
            for time in plan.get('frames', [0]):
                if time >= comp['duration']:
                    raise ValueError('frame_out_of_range')
            overview = call('get_project', {})
            for item in overview['items']:
                if item['type'] not in ('Composition', 'Folder', 'Solid') and item['id'] not in {asset.get('item') for asset in assets.values()}:
                    raise ValueError('unregistered_dependency')
            call('save_project', {'path': str(project)})
            if assets:
                if any('item' not in asset for asset in assets.values()):
                    raise ValueError('asset_not_imported')
                load_module('preserved_stage').claim_output(output, owned)
                collected = call('execute_command', {'command': 'file.collectFiles', 'params': {'folder': str(output)}})
                if collected['errors']:
                    raise ValueError('asset_collection_failed')
                project = Path(collected['project'])
                if project != output / 'project.ecproj':
                    raise ValueError('unexpected_collected_project')
                for asset in assets.values():
                    target = output / '(Footage)' / Path(asset['staging']).name
                    if not target.is_file() or sha(target) != asset['sha256']:
                        raise ValueError('collected_asset_mismatch')
                    asset['path'] = target.relative_to(output).as_posix()
                stage = output
            call('open_project', {'path': str(project)})
            comp = call('get_comp', {'comp': bindings['composition']['comp']})
            composition_validation=composition_contract.verify(expected_composition,comp)
            layers = {str(layer['id']): call('get_layer', {'comp': comp['id'], 'layer': layer['id']}) for layer in comp['layers']}
            if task_hooks:
                task_hooks.reserve_render(comp,plan);task_hooks.watch_render(stage,output)
            frames = []
            for index, time in enumerate(plan.get('frames', [0])):
                filename = f'frame-{index:04d}.png'
                call('render_frame', {'comp': comp['id'], 'time': time, 'max_side': 0, 'path': str(stage / filename), 'inline': False, 'transparent': plan.get('previewAlpha',True)})
                if not (stage / filename).is_file():
                    raise ValueError('frame_missing')
                frames.append({'path': filename, 'seconds': time, 'requestedAlpha': plan.get('previewAlpha',True)})
        output_format=plan.get('exports',[{}])[0].get('format') if plan.get('exports') else None
        if task_hooks and output_format=='png-segmented' and stage!=output:
            # 无素材时在编辑会话结束后原子发布自有工程目录；渲染故障不再搬动工程。
            if output.exists() or output.is_symlink():raise ValueError('output_exists')
            stage.rename(output);stage=output;project=output/'project.ecproj'
        context={'schema':'effectcraft-export-context/v1','plan':plan,'output':str(output),
            'stage':str(stage),'working':str(working),'project':str(project),
            'sourceProject':str(source_project) if source_project else None,'sourceHash':source_hash,
            'compositionValidation':composition_validation,'comp':comp,'layers':layers,'frames':frames,'bindings':bindings,'assets':assets,'receipts':receipts,
            'cli':str(cli),'runtimeSha256':installed['binarySha256'],'executionIdentity':execution_identity}
        context['sourceArtifact']=source_artifact
        context['artifactProducer']=task_hooks.artifact_identity() if task_hooks and hasattr(task_hooks,'artifact_identity') else load_module('artifact_lineage').standalone(context)
        return finish_export(context,task_hooks)


def finish_export(context, task_hooks=None, export_operation=None):
    if task_hooks:
        task_hooks.reserve_render(context['comp'],context['plan']);task_hooks.watch_render(context['stage'],context['output'])
    try:result=_finish_export(context,task_hooks,export_operation)
    except BaseException:
        if task_hooks:
            try:task_hooks.observe_render(context)
            except (ValueError,OSError):pass # 计量诊断已持久化，保留原生原异常。
        raise
    if task_hooks:task_hooks.observe_render(context)
    return result


def _finish_export(context, task_hooks=None, export_operation=None):
    """只执行既定导出与交付完成阶段；不重新进入 MCP 编辑会话。"""
    plan=context['plan'];output=Path(context['output']);stage=Path(context['stage'])
    project=Path(context['project']);working=Path(context['working']);cli=context['cli']
    source_project=Path(context['sourceProject']) if context['sourceProject'] else None
    source_hash=context['sourceHash'];comp=context['comp'];layers=context['layers']
    frames=context['frames'];bindings=context['bindings'];receipts=context['receipts']
    assets={key:dict(value) for key,value in context['assets'].items()}
    initial=export_operation is None
    # 交付记录使用包内路径；原生文件自身仍是引擎保存的格式。
    serialized = json.dumps(receipts, ensure_ascii=False, indent=2)
    for asset in assets.values():
        serialized = serialized.replace(asset['staging'], asset['path'])
        del asset['staging']
    serialized = serialized.replace(str(working), '.').replace(str(stage), '.').replace(str(source_project) if source_project else '\x00', 'source/project.ecproj')
    if initial: (stage / 'operations.json').write_text(serialized + '\n', encoding='utf-8', newline='\n')
    for name, value in [('native.json', {'composition': comp, 'layers': layers}), ('plan.json', plan)]:
        if initial: (stage / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    if initial and context.get('compositionValidation'):
        (stage/'composition-validation.json').write_text(json.dumps(context['compositionValidation'],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if task_hooks and initial:
        export_operation=task_hooks.before('render_and_deliver',{'project':str(project),'exports':plan.get('exports',[])})
        if (plan.get('exports') or [{}])[0].get('format')=='png-segmented':
            task_hooks.checkpoint_export(export_operation,context)
    output_format = plan.get('exports', [{}])[0].get('format') if plan.get('exports') else None
    sequence = load_module('image_sequence').export_sequence(cli, project, comp, stage) if output_format == 'png-sequence' else None
    if output_format == 'png-segmented':
        producer = load_module('segmented_sequence')
        chunk_frames = plan['exports'][0].get('chunkFrames')
        chunk_bytes = min(producer.CHUNK_BYTES, chunk_frames*comp['width']*comp['height']*4) if chunk_frames else producer.CHUNK_BYTES
        segmented = producer.render_segments(cli, project.resolve(), comp, (stage/'rgba-segments').resolve(), chunk_bytes,
            before_segment=task_hooks.allowed if task_hooks else None,before_native=task_hooks.watch_segment if task_hooks else None,
            after_native=task_hooks.finish_segment if task_hooks else None)
        descriptor = stage/'rgba-segments/segments.json'
        sequence = {'path':'rgba-segments/segments.json','sha256':sha(descriptor),
                    'metadata':{'width':comp['width'],'height':comp['height'],'bitDepth':8,'channels':'rgba','alphaRepresentation':'straight-png','colorSpace':'unknown','frameRate':segmented['frameRate'],'frameCount':segmented['frameCount'],'durationTicks':str(segmented['frameCount']),'timeBase':{'num':segmented['frameRate']['den'],'den':segmented['frameRate']['num']}}}
    if output_format == 'mp4':
        # 0.2.0 CLI 将 --comp 字符串解释为名称，数字 ID 只用于 MCP。
        rendered = subprocess.run([cli, '--project', str(project), 'render', '--comp', comp['name'], '--out', str(stage / 'intro.mp4'), '--format', 'h264', '--start', '0', '--end', str(comp['duration']), '--fps', str(comp['frameRate']), '--audio', 'off'], capture_output=True, text=True, timeout=180)
        if rendered.returncode or not (stage / 'intro.mp4').is_file():
            raise RuntimeError('render_failed: ' + rendered.stdout[-1000:] + rendered.stderr[-1000:])
    if source_project and sha(source_project) != source_hash:
        raise ValueError('revision_conflict')
    exchange_report(stage,[frame['path'] for frame in frames]+(['intro.mp4'] if output_format == 'mp4' else [])+([f.relative_to(stage).as_posix() for f in sorted((stage/Path(sequence['path']).parent).rglob('*.png'))] if sequence else []),{})
    manifest = {'schema': 'effectcraft-delivery/v1', 'sourceProjectSha256': source_hash,
                'runtimeSha256': context['runtimeSha256'], 'bindings': bindings, 'frames': frames, 'assets': assets,
                'video': {'path': 'intro.mp4', 'alpha': False} if output_format == 'mp4' else None,
                'imageSequence': sequence,
                'files': {f.relative_to(stage).as_posix(): sha(f) for f in stage.rglob('*') if f.is_file() and f!=stage/'manifest.json'}, 'lossReport': {'path':'exchange-loss.json','sha256':sha(stage/'exchange-loss.json')}, 'acceptance': 'requires-domain-and-visual-review'}
    load_module('artifact_lineage').attach(stage,manifest,context)
    (stage / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    if stage != output:
        if output.exists() or output.is_symlink():
            raise ValueError('output_exists')
        stage.rename(output)
    if task_hooks: task_hooks.after(export_operation, {'manifestSha256': sha(output/'manifest.json')})
    return manifest

def main():
    # 固定重定向输出编码，Windows默认代码页也能返回中文帮助和回执。
    import sys
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,"reconfigure"):stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--runtime-home', type=Path)
    parser.add_argument('--asset', action='append', default=[], help='name=/absolute/path; computes input digest')
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding='utf-8'))
        for assignment in args.asset:
            alias, path = assignment.split('=', 1)
            plan.setdefault('assets', {})[alias] = {'path': path, 'sha256': sha(path)}
        print(json.dumps(execute(plan, args.output, args.runtime_home, args.source), ensure_ascii=False))
    except (ValueError, RuntimeError, OSError, subprocess.SubprocessError) as error:
        print(json.dumps({'error': str(error)}, ensure_ascii=False))
        raise SystemExit(1)

if __name__ == '__main__':
    main()
