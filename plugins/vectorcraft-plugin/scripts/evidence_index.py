#!/usr/bin/env python3
"""分层索引既有证据；只复用依赖未变化的结论，不提升 NOT_RUN 或 SKIP。"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LEVELS={'static','local-tests','native-candidate','fixed-install','host-load','gui','model','command-execution'}
STATUSES={'PASS','FAIL','SKIP','NOT_RUN'}


def safe_file(root, value):
    """只接受仓内普通相对文件；父目录链接也不允许。"""
    if not isinstance(value,str) or not value or '\\' in value or Path(value).is_absolute() or any(p in ('', '.', '..') for p in value.split('/')):
        raise ValueError('invalid_evidence_path')
    path=root/value
    if any(p.is_symlink() for p in [path,*path.parents] if p.is_relative_to(root)) or not path.is_file() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('invalid_evidence_path')
    return path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def archived_copy(root, name, digest):
    """执行身份归档按摘要定位收敛前字节；唯一命中返回归档相对路径，否则 None。"""
    base=root/'docs/evidence/pre-harness-convergence-identity'
    if not base.is_dir(): return None
    matches=[]
    for path in sorted(base.glob('*/'+name)):
        try:
            if sha(safe_file(root,path.relative_to(root).as_posix()))==digest: matches.append(path.relative_to(root).as_posix())
        except ValueError: continue
    return matches[0] if matches else None


def payload_target(root, name, digest):
    """收敛约定：skills/<domain>/scripts/<file> 按字节等价映射到 harness；摘要一致才接受。"""
    if isinstance(name,str) and name.startswith('skills/vectorcraft-') and '/scripts/' in name:
        candidate='skills/vectorcraft-harness/scripts/'+name.split('/scripts/',1)[1]
        try:
            if sha(safe_file(root,candidate))==digest:return candidate
        except ValueError:pass
    # harness 归位约定：src/harness/<file> 按字节等价映射到 scripts/harness；摘要一致才接受。
    if isinstance(name,str) and name.startswith('src/harness/'):
        candidate='scripts/harness/'+name.split('src/harness/',1)[1]
        try:
            if sha(safe_file(root,candidate))==digest:return candidate
        except ValueError:pass
    return None


ARCHIVE_PREFIXES=['docs/evidence/pre-portable-package-identity/','docs/evidence/pre-command-magic-wand-identity/','docs/evidence/pre-command-attributes-identity/','docs/evidence/pre-command-guide-identity/','docs/evidence/pre-command-effect-identity/','docs/evidence/pre-command-appearance-identity/','docs/evidence/pre-command-graphic-style-identity/','docs/evidence/pre-command-layer-identity/','docs/evidence/pre-command-shape-identity/','docs/evidence/pre-command-transparency-identity/','docs/evidence/pre-command-stroke-identity/','docs/evidence/pre-command-paint-identity/','docs/evidence/pre-revision64-identity/','docs/evidence/pre-fixed-ref-identity/','docs/evidence/pre-runtime-gate-identity/','docs/evidence/pre-runtime-default-identity/','docs/evidence/pre-runtime-artifacts-identity/','docs/evidence/pre-runtime-boundaries-identity/','docs/evidence/pre-open-reader-identity/','docs/evidence/pre-download-test-cache-identity/','docs/evidence/pre-authorization-identity/','docs/evidence/pre-recovery-binding-identity/','docs/evidence/pre-source-dependencies-identity/','docs/evidence/pre-task3-closure-identity/','docs/evidence/pre-path-identity/','docs/evidence/pre-source-recovery-identity/','docs/evidence/pre-receipt-recovery-identity/','docs/evidence/pre-launch-recovery-identity/','docs/evidence/pre-task3-6-closure-identity/','docs/evidence/pre-budget-cancel-identity/','docs/evidence/pre-budget-cancel-closure-identity/','docs/evidence/pre-brand-text-identity/','docs/evidence/pre-artboard-mapping-identity/','docs/evidence/pre-exchange-identity/','docs/evidence/pre-brand-variants-identity/','docs/evidence/pre-lineage-identity/','docs/evidence/pre-lineage-cache-fix-identity/','docs/evidence/pre-exchange-delivery-identity/','docs/evidence/pre-quality-checker-identity/','docs/evidence/pre-quality-roots-identity/','docs/evidence/pre-revision-budget-identity/','docs/evidence/pre-revision-goal-identity/','docs/evidence/pre-permissions-identity/','docs/evidence/pre-permissions-source44-identity/','docs/evidence/pre-filesystem-source45-identity/','docs/evidence/pre-assets-source46-identity/','docs/evidence/pre-node-asset-identity/','docs/evidence/pre-single-round-identity/','docs/evidence/pre-review-read-identity/','docs/evidence/pre-controller-read-identity/','docs/evidence/pre-delivery-read-identity/','docs/evidence/pre-source-copy-identity/','docs/evidence/pre-state-write-identity/','docs/evidence/pre-tree-write-identity/','docs/evidence/pre-technical-write-identity/','docs/evidence/pre-backup-write-identity/']


def resolve_dependency(root, name, digest):
    """依赖定位顺序：当前字节 → harness 等价映射 → 前缀归档 → 收敛归档；返回实际路径或 None。"""
    try:
        if sha(safe_file(root,name))==digest:return name
    except ValueError:pass
    mapped=payload_target(root,name,digest)
    if mapped:return mapped
    for prefix in ARCHIVE_PREFIXES:
        old=prefix+name
        try:
            if (root/old).is_file() and sha(safe_file(root,old))==digest:return old
        except ValueError:continue
    return archived_copy(root,name,digest)


def record(root, path, level, status, dependencies, scope, requirement=None, tasks=(), historical=False):
    """登记报告与输入摘要；证据层级必须由调用方明确声明。"""
    if level not in LEVELS: raise ValueError('invalid_evidence_level')
    if status not in STATUSES or not scope: raise ValueError('invalid_evidence_status_or_scope')
    report=safe_file(root,path)
    if report.suffix=='.json':
        data=json.loads(report.read_text())
        observed=data.get('result',data.get('status','')).upper()
        observed={'PASSED':'PASS','FAILED':'FAIL','SKIPPED':'SKIP'}.get(observed,observed)
        if observed and observed!=status: raise ValueError('evidence_status_mismatch')
    return {'path':path,'sha256':sha(report),'level':level,'status':status,'scope':scope,
            'requirement':requirement,'tasks':list(tasks),'historical':historical,
            'dependencies':{p:sha(safe_file(root,p)) for p in dependencies}}


def verify(root, entry):
    """依赖或报告内容失配即过期；不根据文件名判定通过。"""
    if entry.get('level') not in LEVELS or entry.get('status') not in STATUSES:
        raise ValueError('invalid_evidence_record')
    stale=[]
    for path, expected in {entry['path']:entry['sha256'],**entry['dependencies']}.items():
        try:
            if sha(safe_file(root,path))!=expected: stale.append(path)
        except ValueError:
            stale.append(path)
    return {'path':entry['path'],'state':'stale' if stale else 'historical' if entry.get('historical') else 'current',
            'status':entry['status'],'level':entry['level'],'staleDependencies':stale,'scope':entry['scope']}


def bound_report(root,path,level,scope,requirement=None,tasks=()):
    """读取执行时登记的摘要，不重新采样当前文件来洗白旧结论。"""
    data=json.loads(safe_file(root,path).read_text())
    dependencies=data.get('fingerprints',{})
    if not dependencies:raise ValueError('missing_execution_fingerprints')
    entry=record(root,path,level,'PASS',[],scope,requirement,tasks)
    entry['dependencies']=dependencies
    for name,digest in dependencies.items():
        if not isinstance(digest,str) or len(digest)!=64:raise ValueError('invalid_execution_fingerprint')
        try:safe_file(root,name)
        except ValueError:
            # 收敛移动的执行载荷：仅在 harness 等价映射或执行身份归档保存了摘要一致的原字节时接受。
            if not resolve_dependency(root,name,digest):raise ValueError('invalid_execution_fingerprint')
    return entry


def build(root=ROOT):
    """将当前固定安装与历史报告并列索引，不声称本轮重新执行。"""
    current='docs/evidence/craft-vector37-gateway-export-fixed-first-use-20261008.json'
    historical='docs/evidence/craft-full-command-fixed-first-use-20261007.json'
    observed=json.loads(safe_file(root,current).read_text())['hostLock']['plugins']['vectorcraft']
    plugin=json.loads(safe_file(root,'plugin.json').read_text())
    source=json.loads(safe_file(root,'skills.lock.json').read_text())['sources'][0]
    matching=(observed['version']==plugin['version'] and observed['skillSourceSha']==source['sha']
              and observed['skillSourceRef']==source['ref'] and observed['skills']==source['sha256']
              and observed['pluginManifestSha256']==sha(safe_file(root,'plugin.json')))
    entries=[
                record(root,current,'fixed-install','PASS',['skills.lock.json','plugin.json'] if matching else [],'published plugin37/source33; 13 standalone cold starts and two brand export routes; retained historical proof, not newly run', 'VC-DM-006',['4.30'],historical=not matching),
                record(root,historical,'host-load','PASS',[],'historical 58-skill matrix; does not describe later 64-skill inventories or this source candidate', historical=True),
                record(root,'docs/evidence/craft-fixed64-every-skill-cold-first-use-20261007.json','fixed-install','PASS',[],'64-skill cold matrix at its recorded versions (vectorcraft plugin30); not latest plugin37 or source34 acceptance', historical=True)]
    local='docs/evidence/vectorcraft-optimization-local-20261008.json'
    candidate_current=True
    if (root/local).is_file():
        candidate=json.loads(safe_file(root,local).read_text())
        old_version=candidate.get('fixedPluginVersion',candidate.get('pluginFixedVersion'))
        candidate_current=(old_version==plugin['version'])
        if candidate_current:
            entries.append(bound_report(root,local,'local-tests','current plugin Harness and review tests; source candidate code checked in its independent repository','VC-AR-003',['9.13','9.14','9.15']))
            entries.append(bound_report(root,'docs/evidence/vectorcraft-optimization-single-round-native-20261008.json','native-candidate','supplied receipt and native brand revision; not full sections3/6 acceptance','VC-QA-003'))
        else:
            for path,level in [(local,'local-tests'),('docs/evidence/vectorcraft-optimization-single-round-native-20261008.json','native-candidate')]:
                entries.append(record(root,path,level,'PASS',[],'pre-release candidate at its recorded version; execution fingerprints retained in report; not acceptance of this release',historical=True))
    control='docs/evidence/vectorcraft-execution-control-20261008.json'
    if (root/control).is_file():
        if candidate_current:
            entries.append(bound_report(root,control,'native-candidate','owned process supervision, readonly original-file recovery, cancellation epoch fence; full task acceptance remains open','VC-TX-003',['3.1','3.2','3.4','3.5','3.7','3.8']))
        else:
            entries.append(record(root,control,'native-candidate','PASS',[],'pre-release execution control at its original fingerprints; fixed release acceptance remains separate','VC-TX-003',['3.1','3.2','3.4','3.5','3.7','3.8'],historical=True))
    fixed='docs/evidence/vectorcraft-fixed38-optimization-20261008.json'
    if (root/fixed).is_file():
        proof=json.loads(safe_file(root,fixed).read_text())
        if proof['pluginVersion']==plugin['version'] and proof['sourceCommit']==source['sha']:
            entries.append(bound_report(root,fixed,'fixed-install','actual isolated host installation, 13 cold starts and protocol/brand technical tasks only',tasks=['9.3','9.6']))
        else:
            entries.append(record(root,fixed,'fixed-install','PASS',[],'fixed plugin38/source35; retained at original execution identity',tasks=['9.3','9.6'],historical=True))
    quality='docs/evidence/vectorcraft-technical-quality-candidate-20261008.json'
    if (root/quality).is_file():
        entries.append(bound_report(root,quality,'native-candidate','standalone technical decoder and negative tests at their recorded identity; coordinator evidence is separate and complete native engineering acceptance remains open',tasks=['6.1']))
    previous='docs/evidence/vectorcraft-optimization-local-before-execution-control-20261008.json'
    checked='docs/evidence/vectorcraft-checked-review-candidate-20261008.json'
    if (root/checked).is_file():
        entries.append(bound_report(root,checked,'native-candidate','persisted decoder checks of existing native export copies; fixture receipts only; native reopening and real creative acceptance remain open',tasks=['6.2']))
    cycle='docs/evidence/vectorcraft-revision-cycle-candidate-20261008.json'
    if (root/cycle).is_file():
        entries.append(bound_report(root,cycle,'native-candidate','bounded revision minimum: two actual native color revisions with injected scores; full6.6 and real creative acceptance remain open',tasks=['6.4','6.5']))
    geometry='docs/evidence/vectorcraft-geometry-candidate-20261008.json'
    if (root/geometry).is_file():
        entries.append(bound_report(root,geometry,'native-candidate','explicit units, offset artboard controls and retained closure failure; full4.3 remains open','VC-DM-001',['4.1','4.2']))
    boolean='docs/evidence/vectorcraft-boolean-transactions-source-candidate-20261008.json'
    if (root/boolean).is_file():
        entries.append(bound_report(root,boolean,'native-candidate','source37 candidate at recorded commit is consumed by plugin41; full4.6 remains open','VC-DM-002',['4.4','4.5']))
    managed='docs/evidence/vectorcraft-managed-boolean-pinned37-20261008.json'
    if (root/managed).is_file():
        entries.append(bound_report(root,managed,'native-candidate','actual supplied pinned source37 in Harness; structure scope checks; not host installation or full4.6','VC-DM-002'))
    for old in ['vectorcraft-geometry-before-source37-20261008.json','vectorcraft-revision-cycle-before-source37-20261008.json','vectorcraft-boolean-transactions-before-source37-20261008.json']:
        if (root/'docs/evidence'/old).is_file():
            entries.append(record(root,'docs/evidence/'+old,'native-candidate','PASS',[],'source36 or earlier independent candidate at original execution identity; not rebound',historical=True))
    fixed41='docs/evidence/vectorcraft-fixed41-structural-20261008.json'
    if (root/fixed41).is_file():
        data=json.loads(safe_file(root,fixed41).read_text())
        if data['pluginVersion']==plugin['version'] and data['sourceCommit']==source['sha']:
            entries.append(bound_report(root,fixed41,'fixed-install','13 actual installed cold skills,12 declared create/revise pairs and8 managed structural cases; full4.6 and model/GUI/creative gates remain open','VC-DM-002'))
        else:
            entries.append(record(root,fixed41,'fixed-install','PASS',[],'plugin41/source37 installed structural proof at original execution identity',historical=True))
    old_cycle='docs/evidence/vectorcraft-revision-cycle-before-geometry-20261008.json'
    if (root/old_cycle).is_file():
        entries.append(record(root,old_cycle,'native-candidate','PASS',[],'original pre-geometry execution fingerprints preserved; not rebound',historical=True))
    old_checked='docs/evidence/vectorcraft-checked-review-before-cycles-20261008.json'
    if (root/old_checked).is_file():
        entries.append(record(root,old_checked,'native-candidate','PASS',[],'original pre-cycle review coordinator proof; execution fingerprints preserved, not rebound',historical=True))
    if (root/previous).is_file():
        entries.append(record(root,previous,'local-tests','PASS',[],'original execution fingerprints retained inside historical report; never rebound to changed source',historical=True))
    runtime_gate='docs/evidence/vectorcraft-runtime-gate-candidate-20261008.json'
    if (root/runtime_gate).is_file():
        entries.append(bound_report(root,runtime_gate,'native-candidate','live 585-command and25-tool headless probe, drain guard and managed native creation; different-version upgrades, rollback and desktop acceptance remain open','VC-RT-002',['2.4']))
    runtime_default='docs/evidence/vectorcraft-runtime-default-candidate-20261008.json'
    if (root/runtime_default).is_file():
        entries.append(bound_report(root,runtime_default,'native-candidate','default cold fixed install and headless schemas, parallel creation, readonly resume, pre-edit refusal and8 managed structural cases; complete2.6 remains open','VC-RT-002',['2.5']))
    runtime_artifacts='docs/evidence/vectorcraft-runtime-default-artifacts-candidate-20261008.json'
    if (root/runtime_artifacts).is_file():
        entries.append(bound_report(root,runtime_artifacts,'native-candidate','fresh default headless cold/concurrent/refusal cases with all three delivery manifest and file digests; unchanged managed structural regression reused by exact fingerprints; full2.6 remains open','VC-RT-002',['2.5']))
    boundaries='docs/evidence/vectorcraft-runtime-boundaries-candidate-20261008.json'
    if (root/boundaries).is_file():
        entries.append(bound_report(root,boundaries,'native-candidate','Two real CLI versions,11 native cases, schema3 backup and old-reader refusal; complete2.6 remains open','VC-RT-002'))
    open_reader='docs/evidence/vectorcraft-open-reader-candidate-20261008.json'
    if (root/open_reader).is_file():
        entries.append(bound_report(root,open_reader,'native-candidate','Candidate database guard with open-reader red, WAL preservation and native/race/default cases; full2.6 awaits fixed43','VC-RT-002'))
    upgrade='docs/evidence/vectorcraft-runtime-upgrade-fixed43-20261008.json'
    if (root/upgrade).is_file():
        entries.append(record(root,upgrade,'fixed-install','PASS',[],'Public plugin43/source37 at original execution identity; report retains internal fingerprints but its tests/test_optimization_integrity.py pin was never committed and cannot be rebound; seven RT-002 scenarios were real bridge/version drain and open-reader budget rollback on macOS arm64; complete V1 remains open','VC-RT-002',['2.6'],historical=True))
    authorization='docs/evidence/vectorcraft-authorization-snapshot-local44-20261008.json'
    if (root/authorization).is_file():
        entries.append(bound_report(root,authorization,'local-tests','Three synthetic coordinator authorization regressions; 57 Node and43 Python tests; full3.3 and V1 remain open','VC-TX-001'))
    authorization_fixed='docs/evidence/vectorcraft-authorization-fixed44-20261008.json'
    if (root/authorization_fixed).is_file():
        entries.append(bound_report(root,authorization_fixed,'fixed-install','Public plugin44/source37 installed in isolated Codex host; 13 unchanged enabled skills,57 Node and43 Python regressions; full3.3 remains open','VC-TX-001'))
    recovery_candidate='docs/evidence/vectorcraft-recovery-binding-candidate45-20261008.json'
    if (root/recovery_candidate).is_file():
        entries.append(bound_report(root,recovery_candidate,'native-candidate','Recovery snapshot refusals and real coordinator crash/restart/native group stop/handoff; full3.3,3.6,3.9 and V1 remain open','VC-TX-002'))
    recovery_fixed='docs/evidence/vectorcraft-recovery-fixed45-20261008.json'
    if (root/recovery_fixed).is_file():
        entries.append(bound_report(root,recovery_fixed,'fixed-install','Public plugin45/source37 installed host and real cancellation/crash recovery subset; 13 unchanged skills,63 Node and43 Python regressions; full3.3,3.6,3.9 remain open','VC-TX-002'))
    writer_candidate='docs/evidence/vectorcraft-single-writer-candidate46-20261008.json'
    if (root/writer_candidate).is_file():
        entries.append(bound_report(root,writer_candidate,'native-candidate','Seven VC-TX-001 candidate scenarios with immutable native branches, signed GUI conflict and real crash/handoff; fixed46 acceptance remains separate','VC-TX-001'))
    writer_fixed='docs/evidence/vectorcraft-single-writer-fixed46-20261008.json'
    if (root/writer_fixed).is_file():
        entries.append(bound_report(root,writer_fixed,'fixed-install','Recorded installed plugin46 native single-writer cases; physical root replacement not covered, so full3.3 remains open; 75 Node and43 Python tests','VC-TX-001'))
    writer47_candidate='docs/evidence/vectorcraft-single-writer-candidate47-20261008.json'
    if (root/writer47_candidate).is_file():
        entries.append(bound_report(root,writer47_candidate,'native-candidate','VC-TX-001 candidate including physical namespace replacement,77 Node and43 Python tests; fixed47 remains separate','VC-TX-001'))
    writer47_fixed='docs/evidence/vectorcraft-single-writer-fixed47-20261008.json'
    if (root/writer47_fixed).is_file():
        entries.append(bound_report(root,writer47_fixed,'fixed-install','All seven VC-TX-001 scenarios including physical namespace replacement at public installed plugin47/source37 on macOS arm64; 77 Node and43 Python tests','VC-TX-001',['3.3']))
    recovery48='docs/evidence/vectorcraft-source-recovery-candidate48-20261008.json'
    if (root/recovery48).is_file():
        entries.append(bound_report(root,recovery48,'native-candidate','Source snapshot gate, actual post-save receipt loss and readonly original-output recovery;84 Node and43 Python tests; full3.6 remains open','VC-TX-002'))
    source_recovery_fixed='docs/evidence/vectorcraft-source-recovery-fixed48-20261008.json'
    if (root/source_recovery_fixed).is_file():
        entries.append(bound_report(root,source_recovery_fixed,'fixed-install','Public plugin48/source37 actual host installation, source snapshot refusal and post-save receipt loss;84 Node and43 Python tests; complete3.6 remains open','VC-TX-002'))
    linked_recovery='docs/evidence/vectorcraft-linked-recovery-fixed48-20261009.json'
    if (root/linked_recovery).is_file():
        entries.append(bound_report(root,linked_recovery,'fixed-install','External current QA against installed public plugin48/source37: original-stage nonempty linked dependency missing/modified refusal and post-inspection mutation refusal;15 recovery regressions; full3.6 remains open','VC-TX-002'))
    receipt_recovery='docs/evidence/vectorcraft-receipt-recovery-candidate49-20261009.json'
    if (root/receipt_recovery).is_file():
        entries.append(bound_report(root,receipt_recovery,'native-candidate','Receipt/manifest/artifact and post-inspection receipt binding; actual prepared directory identity for plain/linked before/after receipt crashes;97 Node and43 Python tests; full3.6 remains open','VC-TX-002'))
    receipt_fixed='docs/evidence/vectorcraft-receipt-recovery-fixed49-20261009.json'
    if (root/receipt_fixed).is_file():
        entries.append(bound_report(root,receipt_fixed,'fixed-install','Public installed plugin49/source38: four plain/linked crashes before/after receipt, receipt/artifact and post-inspection binding refusal;97 Node and43 Python tests; full3.6 remains open','VC-TX-002'))
    launch='docs/evidence/vectorcraft-launch-recovery-candidate50-20261009.json'
    if (root/launch).is_file():
        entries.append(bound_report(root,launch,'native-candidate','Six real GO-boundary crashes, source readonly inspection and post-inspection change refusal; four receipt regressions;109 Node and43 Python tests; fixed50 and full3.6 remain open','VC-TX-002'))
    task_recovery='docs/evidence/vectorcraft-task-recovery-fixed50-20261009.json'
    if (root/task_recovery).is_file():
        entries.append(bound_report(root,task_recovery,'fixed-install','All seven current VC-TX-002 scenarios in public installed50/source38 macOS arm64;13 actual cases,109 Node and43 Python tests,13 unchanged skills and30 stopped groups; only3.6 closes','VC-TX-002',['3.6']))
    budget_cancel='docs/evidence/vectorcraft-budget-cancel-candidate51-20261009.json'
    if (root/budget_cancel).is_file():
        entries.append(bound_report(root,budget_cancel,'native-candidate','Five real native cases: shared cancellation, original deadline restart, actual completed late receipt, shared attempt/reserved-byte denial;115 Node and43 Python tests; fixed51 and full3.9 remain open','VC-TX-003'))
    budget_fixed='docs/evidence/vectorcraft-budget-cancel-fixed51-20261009.json'
    if (root/budget_fixed).is_file():
        entries.append(bound_report(root,budget_fixed,'fixed-install','All five current VC-TX-003 scenarios on public installed51/source38 macOS arm64;five native cases,115 Node and43 Python tests,13 unchanged skills and13 stopped groups;only3.9 closes','VC-TX-003',['3.9']))
    geometry_fixed='docs/evidence/vectorcraft-geometry-fixed51-20261009.json'
    if (root/geometry_fixed).is_file():
        entries.append(bound_report(root,geometry_fixed,'fixed-install','All two current VC-DM-001 scenarios against installed public51/source38 macOS arm64;external QA driver,six native cases,18 exports,seven geometry tests,13 unchanged skills and6 stopped groups;only4.3 closes','VC-DM-001',['4.3']))
    boolean_fixed='docs/evidence/vectorcraft-boolean-fixed51-20261009.json'
    if (root/boolean_fixed).is_file():
        entries.append(bound_report(root,boolean_fixed,'fixed-install','All four current VC-DM-002 scenarios against installed public51/source38 macOS arm64;24 native workflow/Harness/SDK cases,17 source unit tests,13 unchanged skills and9 stopped registered groups;explicit failure injection;only4.6 closes','VC-DM-002',['4.6']))
    brand_text='docs/evidence/vectorcraft-brand-text-fixed53-20261009.json'
    if (root/brand_text).is_file():
        entries.append(bound_report(root,brand_text,'fixed-install','All four current VC-DM-003 scenarios on public installed53/source39 macOS arm64; explicit brand faults, same-RGB nonconsumers, Chinese revision/reopen and native SVG modes; only4.7/4.8/4.9 close','VC-DM-003',['4.7','4.8','4.9']))
    artboard_mapping='docs/evidence/vectorcraft-artboard-mapping-candidate54-20261009.json'
    if (root/artboard_mapping).is_file():
        entries.append(bound_report(root,artboard_mapping,'native-candidate','Source40 stable artboard-ID mapping and native receipt binding, three successful mappings/four refusals;9 mapping tests,49 Python and115 Node regressions;minimum4.10/4.11 only, complete4.12 remains open','VC-DM-004',['4.10','4.11']))
    artboard_mapping_fixed='docs/evidence/vectorcraft-artboard-mapping-fixed54-20261009.json'
    if (root/artboard_mapping_fixed).is_file():
        entries.append(bound_report(root,artboard_mapping_fixed,'fixed-install','Actual public54/source40 isolated host installation, three successful native mappings/four refusals/14 decoded outputs;13 skills unchanged;complete4.12 remains open','VC-DM-004'))
    artboards='docs/evidence/vectorcraft-artboards-fixed54-20261009.json'
    if (root/artboards).is_file():
        entries.append(bound_report(root,artboards,'fixed-install','All four current VC-DM-004 scenarios on installed54/source40 macOS arm64;31 native boundary cases, standalone export cold first use, stable-ID mapping and pinned renderer unknown-bounds semantics;only4.12 closes','VC-DM-004',['4.12']))
    native_exchange='docs/evidence/vectorcraft-native-exchange-fixed59-20261009.json'
    if (root/native_exchange).is_file():
        entries.append(bound_report(root,native_exchange,'fixed-install','All three current VC-AR-002 scenarios on actual Codex public59/source43 macOS arm64; native text/freeform reopen/edit,three decoded exports,20 refusals;13 skills unchanged;only5.6 closes','VC-AR-002',['5.6']))
    exchange_delivery='docs/evidence/vectorcraft-exchange-delivery-candidate59-20261009.json'
    if (root/exchange_delivery).is_file():
        entries.append(bound_report(root,exchange_delivery,'native-candidate','Public59 supplemental AR-002 guard; actual58 PDF substitute gap,85 Python regressions and20 native refusals;fixed5.6 remains open','VC-AR-002'))
    lineage_fixed='docs/evidence/vectorcraft-lineage-fixed58-20261009.json'
    if (root/lineage_fixed).is_file():
        entries.append(bound_report(root,lineage_fixed,'fixed-install','All three current VC-AR-001 scenarios on actual public58/source43 Codex0.153.4 macOS arm64; native create/move/reopen/revise and public7 cases;13 skill digests unchanged;only5.3 closes','VC-AR-001',['5.3']))
    lineage58='docs/evidence/vectorcraft-lineage-candidate58-20261009.json'
    if (root/lineage58).is_file():
        entries.append(bound_report(root,lineage58,'native-candidate','Source43/public58 read-only artifact lineage guard; real57 CI cache-write failure reproduced and fixed;74 Python regressions;fixed5.3 remains open','VC-AR-001',['5.1','5.2']))
    lineage='docs/evidence/vectorcraft-lineage-candidate57-20261009.json'
    if (root/lineage).is_file():
        entries.append(bound_report(root,lineage,'native-candidate','Source43 movable native artifact lineage and public57 integrity guard; source177 pass30 skip,plugin73 pass;fixed5.3 remains open','VC-AR-001',['5.1','5.2']))
    brand_fixed='docs/evidence/vectorcraft-brand-variants-fixed56-20261009.json'
    if (root/brand_fixed).is_file():
        entries.append(bound_report(root,brand_fixed,'fixed-install','All six current VC-DM-006 scenarios on actual isolated Codex public56/source42 macOS arm64 installation; registered token and raster/SVG asset consumers, preserved unrelated exports and retained failure checkpoints; only4.18 closes','VC-DM-006',['4.18']))
    brand_variants='docs/evidence/vectorcraft-brand-variants-candidate56-20261009.json'
    if (root/brand_variants).is_file():
        entries.append(bound_report(root,brand_variants,'native-candidate','Source42 registered asset guards and SVG instance bounds correction; real baseline55 gap, native candidate asset/token regressions; fixed56 qualification remains separate','VC-DM-006',['4.16','4.17']))
    exchange='docs/evidence/vectorcraft-exchange-candidate55-20261009.json'
    if (root/exchange).is_file():
        entries.append(bound_report(root,exchange,'native-candidate','Source41 raster scope and plugin55 technical disclosure guard; fixed54 gap, three native reopen/nine decode/four explicit disclosure refusals;minimum4.13/4.14 only,4.15 remains open','VC-DM-005',['4.13','4.14']))
    automatic='docs/evidence/vectorcraft-exchange-automatic55-20261009.json'
    if (root/automatic).is_file():
        entries.append(bound_report(root,automatic,'fixed-install','Installed55 automatic freeform SVG fallback, independent native edit preservation, three export decodes and seven refusals; supplementary scope,4.15 formal closure pending','VC-DM-005'))
    exchange_qualified='docs/evidence/vectorcraft-exchange-qualified55-20261009.json'
    if (root/exchange_qualified).is_file():
        entries.append(bound_report(root,exchange_qualified,'fixed-install','Both current VC-DM-005 scenarios; native source independently reopened and edited, automatic freeform SVG fallback, three decodes, seven refusals; macOS arm64 fixed55/source41 only','VC-DM-005',['4.15']))
    exchange_fixed='docs/evidence/vectorcraft-exchange-fixed55-20261009.json'
    if (root/exchange_fixed).is_file():
        entries.append(bound_report(root,exchange_fixed,'fixed-install','Actual public55/source41 installation/discovery and installed-copy three native reopen/nine decode/four disclosure refusals;13 skills unchanged;explicit expansion only,complete4.15 remains open','VC-DM-005'))
    quality='docs/evidence/vectorcraft-quality-checker-candidate60-20261009.json'
    if (root/quality).is_file():
        entries.append(bound_report(root,quality,'local-tests','Readonly checker bundle identity and stale dependency regression; no task6.3 closure or fixed native acceptance','VC-QA-001'))
    roots='docs/evidence/vectorcraft-quality-roots-candidate61-20261009.json'
    if (root/roots).is_file():
        entries.append(bound_report(root,roots,'native-candidate','Persisted checked read roots restored at public receipt CLI;19 candidate native boundary cases;fixed61 qualification remains open','VC-QA-001'))
    quality_fixed='docs/evidence/vectorcraft-quality-fixed61-20261009.json'
    if (root/quality_fixed).is_file():
        entries.append(bound_report(root,quality_fixed,'fixed-install','All three current VC-QA-001 scenarios; actual public61/source43 Codex macOS arm64;19 native boundaries and unchanged13 skill identities;creative judgment not executed','VC-QA-001',['6.3']))
    revision_budget='docs/evidence/vectorcraft-revision-budget-candidate62-20261009.json'
    if (root/revision_budget).is_file():
        entries.append(bound_report(root,revision_budget,'native-candidate','Public61 native budget gap, candidate62 higher-score readonly snapshot reuse and durable stop;three red/twelve green units;complete6.6 remains open','VC-QA-002'))
    revision_budget_fixed='docs/evidence/vectorcraft-revision-budget-fixed62-20261009.json'
    if (root/revision_budget_fixed).is_file():
        entries.append(bound_report(root,revision_budget_fixed,'fixed-install','Public62/source43 actual installed native budget subset:readonly higher-score best retained within four attempts;13 skills unchanged;complete6.6 remains open','VC-QA-002'))
    revision_limits='docs/evidence/vectorcraft-revision-limits-fixed62-20261009.json'
    if (root/revision_limits).is_file():
        entries.append(bound_report(root,revision_limits,'fixed-install','Public62/source43 three native revisions: small improvement, lower score and round limit; owned signed desktop mutation rejects stale source before effects; complete6.6 remains open','VC-QA-002'))
    revision_goal='docs/evidence/vectorcraft-revision-goal-candidate63-20261009.json'
    if (root/revision_goal).is_file():
        entries.append(bound_report(root,revision_goal,'native-candidate','Public62 goal-change feedback gap and three red units;candidate63 latest checked feedback and original best retention;15 real native guards;fixed63/full6.6 pending','VC-QA-002'))
    revision_fixed='docs/evidence/vectorcraft-revision-fixed63-20261009.json'
    if (root/revision_fixed).is_file():
        entries.append(bound_report(root,revision_fixed,'fixed-install','All four current VC-QA-002 scenarios;actual public63/source43 Codex macOS arm64;6 native revisions,15 native guards and owned signed desktop stale source;QA scores,creative judgment separate','VC-QA-002',['6.6']))
    release_gate='docs/evidence/vectorcraft-release-gate-20261009.json'
    if (root/release_gate).is_file():
        entries.append(bound_report(root,release_gate,'fixed-install','External release-owner six-layer gate revalidates unchanged public63/source43 actual installed native proof;docs/spec-only isolated package refuses capability promotion;no new native/model run or marketplace eligibility','VC-RL-001',['7.1','7.2','7.3']))
    permissions='docs/evidence/vectorcraft-permissions-candidate-20261009.json'
    if (root/permissions).is_file():
        entries.append(bound_report(root,permissions,'native-candidate','Partial VC-RL-002 candidate: named-credential and environment regressions plus actual native revision;host secret references and public fixed qualification remain open;no task closure','VC-RL-002',[]))
    permissions44='docs/evidence/vectorcraft-permissions-integration-candidate64-20261009.json'
    if (root/permissions44).is_file():
        entries.append(bound_report(root,permissions44,'native-candidate','Unpublished64/source44 integration;source44 public CI and13 real independent cold installs;actual plugin native revision;full permissions and host secret-reference acceptance remain open','VC-RL-002',[]))
    permissions45='docs/evidence/vectorcraft-permissions-filesystem-integration-candidate64-20261009.json'
    if (root/permissions45).is_file():
        entries.append(bound_report(root,permissions45,'native-candidate','Unpublished64/source45 kernel file scopes,pre-RPC guards,source signed GUI and direct kernel refusals,13 cold installs and current plugin native revision;host secrets,asset preflight audit and fixed64 permission qualification remain open','VC-RL-002',[]))
    permissions46='docs/evidence/vectorcraft-permissions-assets-integration-candidate64-20261009.json'
    if (root/permissions46).is_file():
        entries.append(bound_report(root,permissions46,'native-candidate','Unpublished64/source46 trusted Python asset roots and secure copy; actual native asset create/inherit,28 permission targets and13 cold installs; full host secrets and fixed qualification remain open','VC-RL-002',[]))
    parent_assets='docs/evidence/vectorcraft-permissions-parent-assets-candidate64-20261009.json'
    if (root/parent_assets).is_file():
        entries.append(bound_report(root,parent_assets,'native-candidate','Node parent asset ancestor-swap read reproduced and refused with fixed-reader descriptor digest; current native managed asset create/inherit with six exports; full permission/secret and fixed qualification remain open','VC-RL-002',[]))
    single='docs/evidence/vectorcraft-single-round64-20261009.json'
    if (root/single).is_file():
        entries.append(bound_report(root,single,'model','Current Codex conversation actual native multi-size model assessment,one authorized revision,stagnation/shared budget and nine receipt guards; task9.21 only,no independent review or fixed-host distribution','VC-QA-003',['9.21']))
    review_reads='docs/evidence/vectorcraft-permissions-review-read-candidate64-20261009.json'
    if (root/review_reads).is_file():
        entries.append(bound_report(root,review_reads,'native-candidate','Authorize technical manifest before content reads,descriptor-safe captures and review digests;three red-green boundary tests,141 Node cases and actual four-attempt native revision stop. Full permission/host secrets/fixed qualification remain open','VC-RL-002',[]))
    controller_reads='docs/evidence/vectorcraft-permissions-controller-read-candidate64-20261009.json'
    if (root/controller_reads).is_file():
        entries.append(bound_report(root,controller_reads,'native-candidate','Descriptor-safe plan/source preflight and batched runtime input hashes;three ancestor-swap refusals,large-file/chunking regression and actual four-attempt native revision stop;source copies,delivery inspection,writes,host secrets and fixed qualification remain open','VC-RL-002',[]))
    delivery_reads='docs/evidence/vectorcraft-permissions-delivery-read-candidate64-20261009.json'
    if (root/delivery_reads).is_file():
        entries.append(bound_report(root,delivery_reads,'native-candidate','Frozen-root delivery reads and manifest-bound geometry/receipts;three red-green refusals,149 Node cases,six actual native geometry cases and four-attempt revision stop;source copies,writes,host secrets and fixed qualification remain open','VC-RL-002',[]))
    source_copy='docs/evidence/vectorcraft-permissions-source-copy-candidate64-20261009.json'
    if (root/source_copy).is_file():
        entries.append(bound_report(root,source_copy,'native-candidate','Descriptor-safe streaming source snapshot copy;source swap refusal,large-file and destination guards,actual native revision;remaining parent writes,host secrets and fixed installation qualification stay open','VC-RL-002',[]))
    state_write='docs/evidence/vectorcraft-permissions-state-write-candidate64-20261009.json'
    if (root/state_write).is_file():
        entries.append(bound_report(root,state_write,'native-candidate','Descriptor-safe Controller state/plan/event/control content writes;two old-code failures and actual native revision;directory creation,skill tree copy,other writers,host secrets and fixed qualification remain open','VC-RL-002',[]))
    tree_write='docs/evidence/vectorcraft-permissions-tree-write-candidate64-20261009.json'
    if (root/tree_write).is_file():
        entries.append(bound_report(root,tree_write,'native-candidate','Descriptor-bound Controller snapshot directory creation,skill tree copy and source tree digest;two original-code failures,target guards and actual native revision;other parent writers,host secrets and fixed qualification remain open','VC-RL-002',[]))
    technical_write='docs/evidence/vectorcraft-permissions-technical-write-candidate64-20261009.json'
    if (root/technical_write).is_file():
        entries.append(bound_report(root,technical_write,'native-candidate','Frozen technical-review requests and descriptor-safe snapshot/report writes;three external-write failures plus async request mutation;four adapter drift guards and actual native revision;database/launch audit,host secrets and fixed qualification remain open','VC-RL-002',[]))
    backup_write='docs/evidence/vectorcraft-permissions-backup-write-candidate64-20261009.json'
    if (root/backup_write).is_file():
        entries.append(bound_report(root,backup_write,'native-candidate','Private SQLite staging and descriptor-safe immutable backup publication;frozen task-output artifact hashes;three original-code failures,v1/v2 WAL/budget preservation and native revision;primary database/scratch/launch audit,host secrets and fixed qualification remain open','VC-RL-002',[]))
    commit64='docs/evidence/vectorcraft-public-commit64-install-20261009.json'
    if (root/commit64).is_file():
        entries.append(bound_report(root,commit64,'fixed-install','Actual Codex public-commit64/source46 installation;13 independent cold starts and12 native create/revise pairs,setup-only separately identified;installed Harness budget stop;not a public-tag release or model/full-domain qualification','VC-RL-004',[]))
    revision64='docs/evidence/vectorcraft-revision-commit64-20261009.json'
    if (root/revision64).is_file():
        entries.append(record(root,revision64,'fixed-install','PASS',[],'historical at original commit64/source46 execution identity; report retains internal fingerprints but its scripts/verify_revision_evidence.py pin was never committed and cannot be rebound; superseded as current VC-QA-002 evidence by the commit47b re-execution','VC-QA-002',[]))
    public64='docs/evidence/vectorcraft-public-tag64-install-20261009.json'
    if (root/public64).is_file():
        entries.append(bound_report(root,public64,'fixed-install','Post-publication public tag64/source46 actual Codex installation;13 independent cold starts,12 native create/revise pairs,zero skips and4 successful main/tag CI runs;product bytes equal pre-publication qualification;model/full-domain/secret-boundary acceptance remains open','VC-RL-004',[]))
    paint64='docs/evidence/vectorcraft-command-paint-fixed64-20261009.json'
    if (root/paint64).is_file():
        entries.append(bound_report(root,paint64,'command-execution','Public tag64/source46 owned signed desktop:22 paint commands,44 native save/reopen stages,88 decoded SVG/PNG exports;563 locked commands remain NOT_RUN;native canvas images only,not exhaustive GUI or creative acceptance','VC-CM-001',[]))
    command_families='docs/evidence/vectorcraft-command-families-fixed64-20261009.json'
    if (root/command_families).is_file():
        entries.append(bound_report(root,command_families,'command-execution','Public tag64/source46:44 of585 locked commands accepted across paint/swatch,88 save/reopen stages and176 decoded SVG/PNG exports;541 NOT_RUN;13 installed skill identities unchanged;no task closure or exhaustive GUI/creative acceptance','VC-CM-001',[]))
    command54='docs/evidence/vectorcraft-command-families54-fixed64-20261009.json'
    if (root/command54).is_file():
        entries.append(bound_report(root,command54,'command-execution','Public tag64/source46:54 of585 commands across paint/swatch/stroke,108 save/reopen stages,216 decoded exports and10 actual stroke pixel comparisons;531 NOT_RUN;private-session profile names only,no preference restart,creative/full-GUI/V1 or task closure','VC-CM-001',[]))
    command71='docs/evidence/vectorcraft-command-families71-fixed64-20261009.json'
    if (root/command71).is_file():
        entries.append(bound_report(root,command71,'command-execution','Public tag64/source46:71 of585 commands across paint/swatch/stroke/transparency,142 save/reopen stages and284 decoded exports;514 NOT_RUN;mask editing layers excluded from native saves;private-session defaults only,not preference restarts or exhaustive GUI/creative/V1 or task closure','VC-CM-001',[]))
    mask_window='docs/evidence/vectorcraft-mask-window-fixed64-20261009.json'
    if (root/mask_window).is_file():
        entries.append(bound_report(root,mask_window,'gui','Actual owned signed desktop1440x900 window: viewOpacityMask on shows grey coverage,off restores colored artwork while editing remains active;three interior pixel samples each,13 installed identities preserved;only this command/window/platform,not exhaustive GUI or task closure','VC-CM-001',[]))
    command81='docs/evidence/vectorcraft-command-families81-fixed64-20261009.json'
    if (root/command81).is_file():
        entries.append(bound_report(root,command81,'command-execution','Public tag64/source46:81 of585 commands accepted,162 save/reopen stages,324 decoded exports;504 NOT_RUN. Shape10 adds20 actual owned app-window captures and30 canvas/PNG/window pixel comparisons,with recorded1x/2x window scale normalization and bounded screenshot reads only;all13 installed identities preserved;not exhaustive GUI/creative/V1 or task closure','VC-CM-001',[]))
    command92='docs/evidence/vectorcraft-command-families92-fixed64-20261009.json'
    if (root/command92).is_file():
        entries.append(bound_report(root,command92,'command-execution','Public tag64/source46:92 of585 commands,184 save/reopen stages,368 decoded exports;493 NOT_RUN. Layer11 adds22 actual owned windows and33 image comparisons:state-only deliveries preserve canvas,visibility/clipping change pixels,session current/selection/target independently read back;13 skill identities preserved,no task closure or full GUI/creative/model/V1 claim','VC-CM-001',[]))
    command110='docs/evidence/vectorcraft-command-families110-fixed64-20261009.json'
    if (root/command110).is_file():
        entries.append(bound_report(root,command110,'command-execution','Public tag64/source46:110 of585 commands,220 save/reopen stages,440 decoded exports;475 NOT_RUN. GraphicStyle18 adds36 owned windows and54 image comparisons;relative gradients,link-aware redefine,append/delete preservation,unique names and library dedup/save/load assertions;private preference readback only,no restart,creative/model/full-GUI/V1 or task closure','VC-CM-001',[]))
    command126='docs/evidence/vectorcraft-command-families126-fixed64-20261009.json'
    if (root/command126).is_file():
        entries.append(bound_report(root,command126,'command-execution','Public tag64/source46:126 of585 commands,252 save/reopen stages,504 decoded exports;459 NOT_RUN. Appearance16 adds32 owned windows and48 image comparisons;stack/Contents order,paint-only additions,effects,copy/transfer and actual active-row/new-art probes restored by saved-checkpoint reopen;retained undo/reopen failure does not qualify undo. No preference restart,model/full-GUI/V1 or task closure','VC-CM-001',[]))
    command133='docs/evidence/vectorcraft-command-families133-fixed64-20261009.json'
    if (root/command133).is_file():
        entries.append(bound_report(root,command133,'command-execution','Public tag64/source46:133 of585 commands,266 save/reopen stages,532 decoded exports;452 NOT_RUN. Effect7 adds14 owned windows and21 image comparisons;independent complete45-entry catalog,parameter/stack edits,geometry and stroke-outline/raster/text/crop/copy/container expansion with allocation and control preservation;not all effect/brush/symbol variants,undo,creative/model/full-GUI/V1 or task closure','VC-CM-001',[]))
    command136='docs/evidence/vectorcraft-command-families136-fixed64-20261009.json'
    if (root/command136).is_file():
        entries.append(bound_report(root,command136,'command-execution','Public tag64/source46:136 of585 commands,272 save/reopen stages,544 decoded exports;449 NOT_RUN. Guide3 adds6 owned windows,9 image comparisons and28 independent presence/absence line-coordinate checks;artwork exports remain unchanged. Six locked/unlocked registry probes preserve models;disabled edits not submitted;undo,model/full-GUI/V1 and task closure unqualified','VC-CM-001',[]))
    command138='docs/evidence/vectorcraft-command-families138-fixed64-20261009.json'
    if (root/command138).is_file():
        entries.append(bound_report(root,command138,'command-execution','Public tag64/source46:138 of585 commands,276 save/reopen stages,552 decoded exports;447 NOT_RUN. Attributes2 adds4 actual panel windows,6 image comparisons,4 decoded SVG hyperlink bindings and8 checked/mixed/unchecked checkbox pixel checks;group/text/active-row targeting,mixed values,default cleanup and10-URL MRU;normal render only,not print simulation,undo,model/fullGUI/creative/V1 or task closure','VC-CM-001',[]))
    command140='docs/evidence/vectorcraft-command-families140-fixed64-20261009.json'
    if (root/command140).is_file():
        entries.append(bound_report(root,command140,'command-execution','Public tag64/source46:140 of585 commands,280 save/reopen stages,560 decoded exports;445 NOT_RUN. MagicWand2 adds4 actual panel windows,6 image comparisons and20 independent checkbox pixel checks;merge/reset/clamps,tool switching and same-session native reopen preserve settings and artwork. No app restart,selection matching,model/fullGUI/creative/V1 or task closure','VC-CM-001',[]))
    host47='docs/evidence/vc-qa-004/host-commit47.json'
    if (root/host47).is_file():
        entries.append(record(root,host47,'fixed-install','PASS',['plugin.json','skills.lock.json'],'Actual isolated Codex public-commit47 installation on macOS arm64; all14 locked source47 skills discovered enabled with unchanged tree digests; private acceptance catalog only,not a public-tag release or model qualification','VC-RL-004',[]))
    integrity47='docs/evidence/vc-qa-004/integrity-commit47.json'
    if (root/integrity47).is_file():
        entries.append(record(root,integrity47,'fixed-install','PASS',['plugin.json','skills.lock.json'],'installed public commit47 product source unchanged;external QA/verifier changes are separately fingerprinted'))
    revision47='docs/evidence/vectorcraft-revision-commit47-20261013.json'
    if (root/revision47).is_file():
        entries.append(record(root,revision47,'fixed-install','NOT_RUN',['skills/vectorcraft-harness/scripts/runtime.lock.json','skills/vectorcraft-harness/scripts/desktop.lock.json','docs/evidence/vc-qa-001/native-fixed61.json'],'historical blocked round: source47 re-qualification was honestly NOT_RUN in that environment because the fixed61 seed native project and VectorCraft signed desktop app were absent; superseded by the commit47b re-execution','VC-QA-002',[],historical=True))
    revision47b='docs/evidence/vectorcraft-revision-commit47b-20261014.json'
    if (root/revision47b).is_file():
        entries.append(bound_report(root,revision47b,'fixed-install','All four current VC-QA-002 scenarios on the relocated scripts/harness layout at public commit 3eb0c32/source47 macOS arm64; fresh pinned-runtime seed,6 native revisions,15 guards and one owned signed desktop stale-source mutation;explicit QA scores,not public-tag or model/full-V1 acceptance','VC-QA-002',['6.6']))
    # 明确归档变更前执行字节；保留报告原摘要，不能把旧运行重绑定到新实现。
    for entry in entries:
        archived={}
        for name,digest in entry['dependencies'].items():
            try:
                if sha(safe_file(root,name))==digest:continue
            except ValueError:pass
            resolved=resolve_dependency(root,name,digest)
            if resolved and resolved!=name:archived[name]=resolved
        if archived:
            entry['dependencies']={archived.get(name,name):digest for name,digest in entry['dependencies'].items()}
            entry['historical']=True
            entry['scope']='historical at original execution identity; '+entry['scope']
    return {'schema':'vectorcraft-evidence-index/v1',
            'identitySha256':sha(safe_file(root,'docs/current-identity.json')),
            'entries':entries,
            'commandAcceptance':'Frozen catalog retains its audit statuses; later native execution is recorded in digest-bound external command-family matrices; directory discovery never promotes NOT_RUN',
            'excluded':['complete V1','all commands','all GUI','model dispatch','source candidate fixed-install acceptance']}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    path=ROOT/'docs/evidence-index.json'
    data=build()
    if args.check:
        if not path.is_file() or json.loads(path.read_text())!=data: raise SystemExit('evidence_index_drift')
        if any(verify(ROOT,entry)['state']=='stale' for entry in data['entries']): raise SystemExit('stale_evidence')
    else:
        path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'result':'PASS','scope':'evidence integrity only; original levels preserved','entries':len(data['entries'])}))
