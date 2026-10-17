#!/usr/bin/env python3
"""核验固定安装报告、原始子报告摘要及任务9.3／9.6矩阵完整性。"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]


def verify(root=ROOT):
    """只接受当前固定身份与完整矩阵；不提升模型、GUI或完整V1状态。"""
    def read(path):return json.loads((root/path).read_text())
    report=read('docs/evidence/vectorcraft-fixed38-optimization-20261008.json')
    manifest,lock=read('plugin.json'),read('skills.lock.json')['sources'][0]
    if report['result']!='PASS' or report['pluginVersion']!=manifest['version'] or report['sourceRef']!=lock['ref'] or report['sourceCommit']!=lock['sha']:raise ValueError('fixed_identity_mismatch')
    for name,expected in report['fingerprints'].items():
        path=root/name
        if Path(name).is_absolute() or '..' in Path(name).parts or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()) or not path.is_file():raise ValueError('invalid_fixed_evidence_path')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:raise ValueError('stale_fixed_evidence: '+name)
    reports={}
    for key,entry in report['reports'].items():
        if report['fingerprints'].get(entry['path'])!=entry['sha256']:raise ValueError('unbound_fixed_report')
        reports[key]=read(entry['path'])
    if set(reports)!= {'host','native','protocol','plan','brandEdges','brandGuard','gateway','commands','preserved'}:raise ValueError('missing_fixed_report')
    if any(value.get('result',value.get('status')) not in ('PASS','passed') for value in reports.values()):raise ValueError('fixed_report_not_pass')
    for key in ('host','native'):
        rows=reports[key]['skills' if key=='host' else 'cases']
        names=[value['name' if key=='host' else 'skill'] for value in rows]
        if len(names)!=13 or set(names)!=set(lock['skills']):raise ValueError('fixed_skill_inventory_incomplete')
        if any(value['sha256']!=lock['sha256'][name] for name,value in zip(names,rows)):raise ValueError('fixed_skill_digest_mismatch')
    cold=reports['native']['cases']
    if not all(row['freshRuntime'] and row['installedBytesPreserved'] and row['commandCount']==585 for row in cold):raise ValueError('fixed_cold_incomplete')
    if sum(row['createRevise']=='PASS' for row in cold)!=12:raise ValueError('fixed_scene_incomplete')
    if { (r['mode'],r['fault']) for r in reports['protocol']['cases']} != {(mode,fault) for mode in ('direct','native-gateway') for fault in ('malformed','scalar','missing','ambiguous','nonfinite','tool-content','wrong-id','duplicate-envelope','inner-nonfinite','inner-overflow','inner-duplicate')}:raise ValueError('fixed_protocol_incomplete')
    if not all(r['nativeSaveCount']==1 and r['originalStageReopened'] and r['replayRefused'] for r in reports['protocol']['cases']):raise ValueError('fixed_recovery_incomplete')
    if len(reports['commands']['cases'])!=9 or len(reports['plan']['cases'])!=10:raise ValueError('fixed_entry_matrix_incomplete')
    if not all(r['outputAbsent'] and r['runtimeAbsent'] for r in reports['plan']['cases']):raise ValueError('fixed_preflight_incomplete')
    if len(reports['brandGuard']['failures'])!=8 or {(r['mode'],r['case']) for r in reports['brandEdges']['cases']}!={(mode,case) for mode in ('direct','native-gateway') for case in ('consumer-closed','target-not-reached','verified_noop','no_effect')}:raise ValueError('fixed_brand_incomplete')
    if len(reports['gateway']['cases'])!=2 or not all(r['inheritedOutputs']==9 and r['unrelatedSVGPNGPDFFilesUnchanged'] and r['sourcePreserved'] for r in reports['gateway']['cases']):raise ValueError('fixed_export_incomplete')
    return {'result':'PASS','scope':'fixed technical9.3/9.6; no model routing or full V1 claim'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.parse_args();print(json.dumps(verify()))
