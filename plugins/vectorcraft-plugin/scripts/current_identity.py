#!/usr/bin/env python3
"""从固定插件与技能锁生成当前身份，不访问兄弟仓或联网升级。"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def identity(root=ROOT):
    read = lambda path: json.loads((root/path).read_text())
    plugin, lock = read('plugin.json'), read('skills.lock.json')
    if len(lock['sources']) != 1:
        raise ValueError('one_skill_authority_required')
    source = lock['sources'][0]
    skills = {}
    # 执行载荷收敛在 vectorcraft-harness：运行时与桌面锁只在 harness，且必须与领域技能引用保持一致。
    runtime = read('skills/vectorcraft-harness/scripts/runtime.lock.json')
    desktop = read('skills/vectorcraft-harness/scripts/desktop.lock.json')
    for name in source['skills']:
        skills[name] = source['sha256'][name]
    baseline = read('runtime/vectorcraft-cli.lock.json')
    if baseline.get('role') != 'historical-baseline' or baseline.get('executionAuthority') != 'skills/*/scripts/runtime.lock.json':
        raise ValueError('ambiguous_root_runtime_authority')
    catalog = read('skills/vectorcraft-use/references/command-coverage.json')
    artifact = runtime['artifacts']['darwin-arm64']
    if catalog['runtimeSha256'] != artifact['binarySha256']:
        raise ValueError('catalog_runtime_identity_drift')
    return {'schema':'vectorcraft-current-identity/v1', 'pluginVersion':plugin['version'],
        'skillSource':{k:source[k] for k in ('repo','ref','sha')}, 'skills':skills,
        'runtime':{'version':runtime['resolvedVersion'], 'platform':'darwin-arm64',
                   'binarySha256':artifact['binarySha256'], 'archiveSha256':artifact['archiveSha256']},
        'desktop':{'version':desktop['version'], 'binarySha256':desktop['binarySha256']},
        'rootRuntimeRole':baseline['role'], 'commandCount':len(catalog['commands']),
        'commandAcceptance':{status:sum(row['executionAcceptance']==status for row in catalog['commands'])
                             for status in sorted({row['executionAcceptance'] for row in catalog['commands']})},
        'stage':read('project-status.json')['stage'],
        'scope':'fixed plugin snapshot; source candidate changes require a separately pinned release; no live enabled or creative acceptance claim'}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    path=ROOT/'docs/current-identity.json'
    data=json.dumps(identity(),ensure_ascii=False,indent=2)+'\n'
    if args.check:
        if not path.is_file() or path.read_text()!=data:
            raise SystemExit('current_identity_drift')
    else:
        path.write_text(data)
    print(json.dumps({'result':'PASS','scope':'fixed version identity only'}))
