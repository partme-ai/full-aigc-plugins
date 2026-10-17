"""复核 SAM 只读评估中的目录、模型与权限事实；不会执行推理。"""
import importlib.util
from pathlib import Path


def policy():
    path=Path(__file__).with_name('sam_contract.py');spec=importlib.util.spec_from_file_location('plugin_sam_contract',path)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result


def inspect_sam(path):
    """报告是观察输入而非原生证明；重新读取模型文件，拒绝漂移和权限提升。"""
    api=policy();data=api.gateway().strict_json(Path(path).read_text())
    if not isinstance(data,dict):raise ValueError('sam_report_invalid')
    readonly={'readOnly':True,'taskExecutionAllowed':False,'downloadAllowed':False,'executionAllowed':False,'deliveryAllowed':False,'automaticReplay':False,'completeAcceptance':False}
    if type(data.get('schemaVersion')) is not int or data.get('schemaVersion')!=1 or data.get('reportKind')!='sam-readonly-assessment':return dict(readonly,compatible=False)
    if data.get('modelManifest')!=api.manifest() or data.get('modelManifestSha256')!=api.digest(api.manifest()):raise ValueError('sam_manifest_identity_mismatch')
    if not isinstance(data.get('snapshot'),dict) or data.get('snapshotSha256')!=api.digest(data['snapshot']):raise ValueError('sam_snapshot_identity_mismatch')
    files=data.get('modelFiles')
    if not isinstance(files,list) or len(files)!=3 or any(not isinstance(row,dict) for row in files):raise ValueError('sam_model_facts_invalid')
    paths=[row.get('path') for row in files];directory=None
    if any(path is not None for path in paths):
        if any(not isinstance(path,str) or not Path(path).is_absolute() for path in paths):raise ValueError('sam_model_paths_invalid')
        directory=Path(paths[0]).parent
        if any(Path(path).parent!=directory or Path(path).name!=expected['name'] for path,expected in zip(paths,api.FILES)):raise ValueError('sam_model_paths_invalid')
    expected=api.assess(data['snapshot'],data.get('reportedStatus'),directory)
    if not api.gateway().json_equal(expected,data):raise ValueError('sam_assessment_changed_or_inconsistent')
    return dict(readonly,compatible=True,compileFeature=expected['compileFeature'],statusCommandPresent=expected['statusCommandPresent'],modelIdentityVerified=expected['modelIdentityVerified'],runtimeIdentity=expected['runtimeIdentity'],blockers=expected['blockers'],nativeAttestation='NOT_PROVEN',scope=expected['scope'])
