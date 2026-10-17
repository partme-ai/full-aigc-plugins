"""固定引擎重开临时工程包，保全用户原件并核对当前原生结构。"""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile


def load(name):
    spec=importlib.util.spec_from_file_location('craft_engineering_'+name,Path(__file__).with_name(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def runtime_lock():
    return load('quality_review').read(Path(__file__).with_name('runtime.lock.json'))


def verify(root, runtime_home, runtime_sha, timeout=120, before_render=None):
    """只读安装检查及原生副本重开；不下载、不保存、不重放编辑。"""
    report={'schema':'effectcraft-engineering-review/v1','status':'NOT_RUN','fresh':False}
    import time
    deadline=time.monotonic()+timeout
    quality=load('quality_review');root=Path(root)
    try:
        if runtime_home is None:raise ValueError('engineering_runtime_location_missing')
        lock=runtime_lock();key=load('platform_support').platform_key();expected=lock['artifacts'][key]
        if expected['binarySha256']!=runtime_sha:raise ValueError('engineering_task_runtime_mismatch')
        installed=load('bootstrap').inspect_install(Path(runtime_home)/'effectcraft'/lock['resolvedVersion'],lock['artifact'],expected,lock['resolvedVersion'],load('platform_support').platform_key())
    except (ValueError,OSError,KeyError,TypeError) as error:
        report['reason']=str(error);return report
    try:
        bound=quality.binding(root);manifest=quality.read(root/'manifest.json');native=quality.read(root/'native.json')
        if any(manifest['files'].get(name)!=quality.sha(root/name) for name in ('project.ecproj','native.json')):
            raise ValueError('engineering_metadata_unbound')
        with tempfile.TemporaryDirectory(prefix='effectcraft readonly review ') as temporary:
            snapshot=Path(temporary);shutil.copyfile(root/'project.ecproj',snapshot/'project.ecproj')
            for asset in manifest.get('assets',{}).values():
                target=quality.contained(snapshot,asset['path']);target.parent.mkdir(parents=True,exist_ok=True)
                if target.exists():raise ValueError('engineering_asset_path_collision')
                shutil.copyfile(quality.contained(root,asset['path']),target)
                if quality.sha(target)!=asset['sha256']:raise ValueError('engineering_snapshot_changed')
            if quality.sha(snapshot/'project.ecproj')!=bound['projectSha256']:
                raise ValueError('engineering_snapshot_changed')
            with load('mcp_session').Session([installed['executable'],'--empty','mcp'],timeout=timeout) as session:
                def call(name,args):
                    return load('commands').parse_reply(session.request('tools/call',{'name':name,'arguments':args}))
                call('open_project',{'path':str(snapshot/'project.ecproj')})
                footage=call('execute_command',{'command':'footage.check','params':{'wait':True}})
                if (not isinstance(footage,dict) or type(footage.get('missing')) is not int or footage['missing']!=0
                        or type(footage.get('checked')) is not int):raise ValueError('native_footage_missing')
                overview=call('get_project',{})
                expected_items={asset['item'] for asset in manifest.get('assets',{}).values()}
                actual_items={item['id'] for item in overview['items'] if item['type'] not in ('Composition','Folder','Solid')}
                if expected_items!=actual_items:raise ValueError('native_dependency_mismatch')
                comp=call('get_comp',{'comp':native['composition']['id']})
                layers={str(layer['id']):call('get_layer',{'comp':comp['id'],'layer':layer['id']}) for layer in comp['layers']}
                if {'composition':comp,'layers':layers}!=native:raise ValueError('native_snapshot_mismatch')
            if quality.sha(snapshot/'project.ecproj')!=bound['projectSha256']:
                raise ValueError('engineering_snapshot_changed')
            for asset in manifest.get('assets',{}).values():
                if quality.sha(quality.contained(snapshot,asset['path']))!=asset['sha256']:
                    raise ValueError('engineering_snapshot_changed')
        if quality.binding(root)!=bound:raise ValueError('artifact_changed_during_engineering_review')
        report.update(status='PASS',fresh=True,projectSha256=bound['projectSha256'],runtimeSha256=runtime_sha,
            nativeSnapshotHash=load('task_store').digest(native),verifiedAssets=len(manifest.get('assets',{})),
            method='isolated native open, footage check and exact composition/layer comparison')
        if 'nativeResources' in manifest:
            report['resourceValidation']=load('resource_validation').workflow(root,installed['executable'],timeout=deadline-time.monotonic(),before_render=before_render)
            if report['resourceValidation']['status']=='FAIL':report.update(status='FAIL',fresh=False,reason='file_lut_validation_failed')
            elif report['resourceValidation']['status']=='NOT_RUN' and report['resourceValidation'].get('projects'):report.update(status='NOT_RUN',fresh=False,reason='file_lut_validation_incomplete')
    except (TimeoutError,subprocess.TimeoutExpired) as error:
        report.update(status='NOT_RUN',reason=str(error))
    except (ValueError,OSError,KeyError,TypeError,RuntimeError,subprocess.SubprocessError) as error:
        report.update(status='FAIL',reason=str(error))
    return report
