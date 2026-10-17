"""更新准入只读检查；安装器只管理包缓存，任务数据独立保留。"""
import argparse
import importlib.util
import json
from pathlib import Path
import re
CONTRACTS={'execution':'printcraft.execution/1','verification':'printcraft.verification/1'}
OPTIONAL_CONTRACTS={'ocr':'printcraft.ocr/1','ocrBackend':'printcraft.ocr-backend/1'}

def validate_contracts(manifest):
    contracts=manifest.get('extensions',{}).get('org.full-aigc.printcraft',{}).get('contracts')
    if (not isinstance(contracts,dict) or any(contracts.get(key)!=value for key,value in CONTRACTS.items())
            or set(contracts)-set(CONTRACTS)-set(OPTIONAL_CONTRACTS)
            or any(contracts[key]!=OPTIONAL_CONTRACTS[key] for key in set(contracts)&set(OPTIONAL_CONTRACTS))):raise ValueError('legacy_or_incompatible_contract_readonly')
def version_key(value):
    match=re.fullmatch(r'(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?(?:\+[0-9A-Za-z.-]+)?',value)
    if not match:raise ValueError('invalid_version')
    major,minor,patch,pre=match.groups()
    return (int(major),int(minor),int(patch),1 if pre is None else 0,tuple((0,int(x)) if x.isdigit() else (1,x) for x in (pre or '').split('.')))

def check(current,candidate,task_data):
    current=Path(current).resolve();candidate=Path(candidate).resolve();task_data=Path(task_data).resolve()
    if task_data==candidate or candidate in task_data.parents or task_data==current or current in task_data.parents:raise ValueError('task_data_must_be_outside_package_cache')
    old=json.loads((current/'plugin.json').read_text());new=json.loads((candidate/'plugin.json').read_text())
    if old['name']!=new['name']:raise ValueError('cross_domain_update')
    spec=importlib.util.spec_from_file_location('candidate_validation',candidate/'scripts/validate_package.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.validate()
    if version_key(new['version'])<version_key(old['version']):raise ValueError('rollback_requires_compatible_explicit_migration')
    for manifest in (old,new):
        validate_contracts(manifest)
    return {'status':'UPDATE_ELIGIBLE','dataMigration':'NONE','taskDataPreserved':True,'oldVersion':old['version'],'newVersion':new['version'],'installation':'NOT_PERFORMED'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--current-root',type=Path,required=True);p.add_argument('--candidate-root',type=Path,required=True);p.add_argument('--task-data',type=Path,required=True);a=p.parse_args();print(json.dumps(check(a.current_root,a.candidate_root,a.task_data)))
