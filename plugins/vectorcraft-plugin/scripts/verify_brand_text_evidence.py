#!/usr/bin/env python3
"""核对VC-DM-003当前规范逐场景证据；只关闭声明平台的品牌色与文字合同，不推断V1、GUI或模型验收。"""
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]

def payload_name(name):
    """执行载荷收敛在 vectorcraft-harness：历史证据绑定的 skills/<domain>/scripts/ 路径按字节等价映射到 harness。"""
    if isinstance(name, str):
        prefix = 'skills/vectorcraft-'
        if name.startswith(prefix) and '/scripts/' in name and not (ROOT/name).is_file():
            candidate = 'skills/vectorcraft-harness/scripts/' + name.split('/scripts/', 1)[1]
            if (ROOT/candidate).is_file():
                return candidate
    return name

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def contracts():
    text=(ROOT/'openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md').read_text()
    block=text.split('### Requirement: VC-DM-003 ',1)[1].split('### Requirement:',1)[0]
    parts=block.split('#### Scenario: ')
    return {part.splitlines()[0].split()[0]:hashlib.sha256(part.strip().encode()).hexdigest() for part in parts[1:]}
def local(name):
    name = payload_name(name)
    path=ROOT/name
    if not isinstance(name,str) or name.startswith('/') or any(p in ('','.','..') for p in name.split('/')) or any(p.is_symlink() for p in [path,*path.parents] if p.is_relative_to(ROOT)) or not path.resolve().is_relative_to(ROOT):raise ValueError('invalid_evidence_path')
    return path

def main():
    path=ROOT/'docs/evidence/vectorcraft-brand-text-fixed53-20261009.json';report=json.loads(path.read_text())
    if report['result']!='PASS' or report['tasksClosed']!=['4.7','4.8','4.9']:raise ValueError('incomplete_brand_text_acceptance')
    index=json.loads((ROOT/'docs/evidence-index.json').read_text())
    known=next(entry['dependencies'] for entry in index['entries'] if entry['path']==str(path.relative_to(ROOT)))
    def bound(name):
        digest=report['fingerprints'][name]
        if sha(local(name))==digest:return local(name)
        archived=[candidate for candidate,saved in known.items() if saved==digest and candidate.endswith('/'+name)]
        if len(archived)!=1 or sha(local(archived[0]))!=digest:raise ValueError('stale_brand_text_evidence: '+name)
        return local(archived[0])
    for name in report['fingerprints']:bound(name)
    matrix=json.loads(local(report['scenarioMatrix']).read_text());current=contracts()
    if matrix['scenarioContracts']!=current or {row['scenario'] for row in matrix['entries']}!=set(current):raise ValueError('scenario_coverage_mismatch')
    checks=0
    for row in matrix['entries']:
        if not row['checks'] or not any(check['level']=='native-fixed-install' for check in row['checks']):raise ValueError('missing_native_scenario_evidence')
        for check in row['checks']:
            file=local(check['report'])
            if check['report'] not in report['fingerprints']:raise ValueError('unbound_raw_evidence')
            if 'contains' in check:
                if check['contains'] not in file.read_text():raise ValueError('missing_test_evidence: '+row['scenario'])
            else:
                value=json.loads(file.read_text())
                for part in check['pointer'].split('/')[1:]:value=value[int(part)] if isinstance(value,list) else value[part]
                if value!=check['expected']:raise ValueError('failed_scenario_check: '+row['scenario']+' '+check['pointer'])
            checks+=1
    host=json.loads(local(report['host']).read_text())
    if host['pluginCommit']!=report['pluginCommit'] or host['skillSourceCommit']!=report['sourceCommit'] or len(host['skills'])!=13:raise ValueError('fixed_host_identity_mismatch')
    if host['skillSourceCommit']!=report['sourceCommit'] or host['skillSourceRef']!=report['sourceRef'] or host['pluginVersion']!=report['pluginVersion'] or not host['skillsUnchangedAfterQA']:raise ValueError('fixed_host_source_mismatch')
    lock=json.loads(bound('skills.lock.json').read_text())['sources'][0]
    if lock['sha']!=report['sourceCommit'] or lock['ref']!=report['sourceRef'] or {row['name']:row['sha256'] for row in host['skills']}!=lock['sha256']:raise ValueError('fixed_skill_identity_mismatch')
    brand=json.loads(local('docs/evidence/vc-dm-003/brand.json').read_text())
    outline=json.loads(local('docs/evidence/vc-dm-003/outline.json').read_text())
    reopened=json.loads(local('docs/evidence/vc-dm-003/reopen.json').read_text())
    if not brand['fixedInstalled'] or len(brand['failures'])!=8 or len(outline['cases'])!=2 or len(outline['preflightRefusals'])!=18 or len(reopened['cases'])!=2 or len(reopened['failures'])!=2:raise ValueError('native_case_coverage_mismatch')
    for test,digest in report['sourceTestFingerprints'].items():
        if sha(local('docs/evidence/vc-dm-003/'+Path(test).name+'.txt'))!=digest:raise ValueError('source_test_driver_drift')
    for path,driver in [('scripts/qa/text_outline.py',outline),('scripts/qa/brand_text_reopen.py',reopened)]:
        if driver['driverSha256']!=sha(bound(path)):raise ValueError('external_qa_driver_drift')
    print(json.dumps({'result':'PASS','scope':'VC-DM-003 current scenarios on fixed53/source39 macOS arm64 only','scenarios':len(current),'checks':checks,'tasksClosed':['4.7','4.8','4.9']}))
if __name__=='__main__':main()
