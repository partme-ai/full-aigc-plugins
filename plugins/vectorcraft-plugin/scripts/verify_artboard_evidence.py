#!/usr/bin/env python3
"""核对当前 VC-DM-004 四场景、原生回执和安装身份，不提升为完整 V1。"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def payload_name(name):
    """执行载荷收敛在 vectorcraft-harness：历史证据绑定的 skills/<domain>/scripts/ 路径按字节等价映射到 harness。"""
    if isinstance(name, str):
        prefix = 'skills/vectorcraft-'
        if name.startswith(prefix) and '/scripts/' in name and not (ROOT/name).is_file():
            candidate = 'skills/vectorcraft-harness/scripts/' + name.split('/scripts/', 1)[1]
            if (ROOT/candidate).is_file():
                return candidate
    return name

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def contracts():
    text = (ROOT/'openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md').read_text()
    block = text.split('### Requirement: VC-DM-004 ',1)[1].split('### Requirement:',1)[0]
    return {part.splitlines()[0].split()[0]:hashlib.sha256(part.strip().encode()).hexdigest() for part in block.split('#### Scenario: ')[1:]}
def local(name):
    name = payload_name(name)
    path = ROOT/name
    if not isinstance(name,str) or name.startswith('/') or any(p in ('','.','..') for p in name.split('/')) or path.is_symlink() or not path.resolve().is_relative_to(ROOT):
        raise ValueError('invalid_evidence_path')
    return path
def main():
    report_path='docs/evidence/vectorcraft-artboards-fixed54-20261009.json'
    report = json.loads(local(report_path).read_text())
    if report['result'] != 'PASS' or report['tasksClosed'] != ['4.12']:
        raise ValueError('incomplete_artboard_acceptance')
    index=json.loads(local('docs/evidence-index.json').read_text())
    known=next(e['dependencies'] for e in index['entries'] if e['path']==report_path)
    def bound(name):
        digest=report['fingerprints'][name]
        if sha(local(name))==digest:return local(name)
        archived=[p for p,saved in known.items() if saved==digest and p.endswith('/'+name)]
        if len(archived)!=1 or sha(local(archived[0]))!=digest:raise ValueError('stale_artboard_evidence: '+name)
        return local(archived[0])
    for name in report['fingerprints']:bound(name)
    matrix = json.loads(local(report['scenarioMatrix']).read_text())
    current = contracts()
    if matrix['scenarioContracts'] != current or {r['scenario'] for r in matrix['entries']} != set(current):
        raise ValueError('scenario_coverage_mismatch')
    checks = 0
    for row in matrix['entries']:
        if not row['checks'] or not any(c['level']=='native-fixed-install' for c in row['checks']):
            raise ValueError('missing_native_scenario_evidence')
        for check in row['checks']:
            path = local(check['report'])
            if check['report'] not in report['fingerprints']:
                raise ValueError('unbound_raw_evidence')
            if 'contains' in check:
                assert check['contains'] in path.read_text(), 'missing regression evidence'
            else:
                value = json.loads(path.read_text())
                try:
                    for key in check['pointer'].split('/')[1:]:
                        value = value[int(key)] if isinstance(value,list) else value[key]
                except (KeyError, IndexError, TypeError) as exc:
                    raise ValueError('missing_scenario_receipt: '+row['scenario']) from exc
                if value != check['expected']:
                    raise ValueError('failed_scenario_check: '+row['scenario'])
            checks += 1
    host = json.loads(local(report['host']).read_text())
    integrity = json.loads(local(report['installedIntegrity']).read_text())
    lock = json.loads(bound('skills.lock.json').read_text())['sources'][0]
    if (host['pluginCommit'] != report['pluginCommit'] or host['skillSourceCommit'] != report['sourceCommit']
            or integrity['digests'] != lock['sha256'] or integrity['skillsUnchanged'] != 13):
        raise ValueError('installed_identity_mismatch')
    native = json.loads(local(report['native']).read_text())
    required = {'locked-visible','remote-change','stroke-reaching-board','shadow-reaching-board',
                'indivisible-cross-board-group','complete-clipping-group','empty-board','legacy-default',
                'isolation-off','unknown-descendant-conservative-parent','pdf-fixed-date','pdf-fixed-date-later',
                'pdf-default-now','pdf-default-later','pdf-null-default'}
    required |= {'invalid-isolation-'+str(i) for i in range(10)} | {'invalid-pdf-date-'+str(i) for i in range(6)}
    if {r['name'] for r in native['cases']} != required or len(native['cases']) != 31:
        raise ValueError('missing_native_case')
    if native['runtimeSha256'] != report['runtimeSha256'] or native['driverSha256'] != sha(bound('scripts/qa/artboard_isolation.py')):
        raise ValueError('native_execution_identity_mismatch')
    for row in native['cases']:
        if row['result'] != 'PASS' or row['sourceSelectionHistoryPreserved'] is not True:
            raise ValueError('failed_native_case')
        for key, hash_key in [('receipt','sha256'),('state','stateSha256')]:
            name = 'docs/evidence/vc-dm-004/'+row[key]
            if name not in report['fingerprints'] or sha(local(name)) != row[hash_key]:
                raise ValueError('unbound_native_receipt')
    if not all(row['sha256']==lock['sha256'][row['name']] for row in host['skills']) or len(host['skills']) != 13:
        raise ValueError('host_skill_mismatch')
    print(json.dumps({'result':'PASS','scope':'four current VC-DM-004 scenarios on fixed54/source40 macOS arm64 only','scenarios':4,'nativeCases':31,'checks':checks,'taskClosed':'4.12'}))
if __name__ == '__main__':
    main()
