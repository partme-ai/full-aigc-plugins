#!/usr/bin/env python3
"""校验独立技能源候选；不修改 skills.lock、不伪造发布引用、不覆盖插件快照。"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]

def verify(source):
    source=Path(source).resolve()
    root=subprocess.check_output(['git','-C',str(source),'rev-parse','--show-toplevel'],text=True).strip()
    if Path(root).resolve()!=source:raise ValueError('source_must_be_repository_root')
    suite=json.loads((source/'skill-suite.json').read_text())
    harness=suite['pluginId']+'-harness'
    names=[row['name'] for row in suite['skills']]
    if suite['pluginId']!='effectcraft' or len(names)!=16 or harness not in names:raise ValueError('candidate_skill_identity')
    for name in ('build_command_coverage.py','build_scenario_catalog.py','sync_skill_suite.py'):
        subprocess.run([sys.executable,'-I','-B',str(source/'scripts'/name),'--check'],cwd=source,check=True,stdout=subprocess.PIPE)
    identities={}
    for row in suite['skills']:
        skill=source/'skills'/row['name']
        # 执行实现只收敛在 harness；领域技能是薄文档，不再自带 scripts/。
        required=['SKILL.md','agents/openai.yaml']+(['scripts/launch.sh','scripts/launch.ps1','scripts/managed.py','scripts/python.lock.json','scripts/runtime.lock.json'] if row['name']==harness else [])
        if any(not (skill/name).is_file() for name in required):raise ValueError('candidate_entry_missing: '+row['name'])
        if row['name']!=harness and (skill/'scripts').exists():raise ValueError('candidate_domain_skill_carries_scripts: '+row['name'])
        if any(p.is_symlink() for p in skill.rglob('*')):raise ValueError('candidate_symlink')
        files={p.relative_to(skill).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(skill.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
        identities[row['name']]=hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    published=json.loads((ROOT/'skills.lock.json').read_text())
    return {'schema':'effectcraft-source-candidate/v1','sourceHead':subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip(),
            'workingTreeCandidate':bool(subprocess.check_output(['git','-C',str(source),'status','--porcelain'],text=True)),
            'skills':identities,'runtimeVersion':suite['runtimeVersion'],'publishedSource':published['sources'][0],
            'status':'candidate-structure-verified','releaseReady':False,
            'remaining':['target-platform native acceptance','fixed released source snapshot','host acceptance bound to final candidate','separate publication authorization']}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--report',type=Path);args=p.parse_args()
    report=json.dumps(verify(args.source),ensure_ascii=False,indent=2)+'\n'
    if args.report:args.report.write_text(report)
    else:print(report,end='')
