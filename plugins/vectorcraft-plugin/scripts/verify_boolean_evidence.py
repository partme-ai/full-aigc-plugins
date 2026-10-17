#!/usr/bin/env python3
"""核对VC-DM-002当前规范逐场景证据；只关闭声明平台的布尔与组合合同，不推断V1、GUI或模型验收。"""
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
    block=text.split('### Requirement: VC-DM-002 ',1)[1].split('### Requirement:',1)[0]
    parts=block.split('#### Scenario: ')
    return {part.splitlines()[0].split()[0]:hashlib.sha256(part.strip().encode()).hexdigest() for part in parts[1:]}
def local(name):
    name = payload_name(name)
    path=ROOT/name
    if not isinstance(name,str) or name.startswith('/') or any(p in ('','.','..') for p in name.split('/')) or path.is_symlink() or not path.resolve().is_relative_to(ROOT):raise ValueError('invalid_evidence_path')
    return path

def main():
    path=ROOT/'docs/evidence/vectorcraft-boolean-fixed51-20261009.json';report=json.loads(path.read_text())
    if report['result']!='PASS' or report['tasksClosed']!=['4.6']:raise ValueError('incomplete_recovery_acceptance')
    index=json.loads((ROOT/'docs/evidence-index.json').read_text())
    known=next(entry['dependencies'] for entry in index['entries'] if entry['path']==str(path.relative_to(ROOT)))
    for name,digest in report['fingerprints'].items():
        if sha(local(name))==digest:continue
        # 只接受既有索引指向的真实原字节；不能用当前源码重新生成旧摘要。
        archived=[candidate for candidate,saved in known.items() if saved==digest and candidate.endswith('/'+name)]
        if len(archived)!=1 or sha(local(archived[0]))!=digest:raise ValueError('stale_recovery_evidence: '+name)
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
    print(json.dumps({'result':'PASS','scope':'VC-DM-002 current scenarios on fixed51/source38 macOS arm64 only','scenarios':len(current),'checks':checks,'taskClosed':'4.6'}))
if __name__=='__main__':main()
