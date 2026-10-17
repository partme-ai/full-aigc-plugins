#!/usr/bin/env python3
"""核验当前质量分离三个场景；高分、重新散列或任务勾选不能替代技术证据。"""
import hashlib,json
from pathlib import Path
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

REPORT='docs/evidence/vectorcraft-quality-fixed61-20261009.json'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def local(name):
 name = payload_name(name)
 if not isinstance(name,str) or Path(name).is_absolute() or '\\' in name or any(p in ('','.','..') for p in name.split('/')):raise ValueError('invalid_evidence_path')
 p=ROOT/name
 if not p.resolve().is_relative_to(ROOT.resolve()) or any(x.is_symlink() for x in [p,*p.parents] if x.is_relative_to(ROOT)):raise ValueError('invalid_evidence_path')
 return p
def main():
 r=json.loads(local(REPORT).read_text());index=json.loads(local('docs/evidence-index.json').read_text()) if local('docs/evidence-index.json').is_file() else {'entries':[]};known=next((x['dependencies'] for x in index['entries'] if x['path']==REPORT),{})
 def bound(name):
  expected=r['fingerprints'][name];p=local(name)
  if p.is_file() and sha(p)==expected:return p
  candidates=[n for n,h in known.items() if h==expected and n.endswith('/'+name)]
  if len(candidates)!=1 or sha(local(candidates[0]))!=expected:raise ValueError('stale_quality_evidence')
  return local(candidates[0])
 def read(name):return json.loads(bound(name).read_text())
 for name in r['fingerprints']:bound(name)
 if r['result']!='PASS' or r['tasksClosed']!=['6.3']:raise ValueError('quality_closure')
 block=bound('openspec/changes/establish-v1-plugin/specs/quality-review/spec.md').read_text().split('### Requirement: VC-QA-001 ',1)[1].split('### Requirement:',1)[0]
 contracts={s.splitlines()[0]:hashlib.sha256(s.strip().encode()).hexdigest() for s in block.split('#### Scenario: ')[1:]}
 matrix=read(r['scenarioMatrix'])
 if matrix['scenarioContracts']!=contracts or len(matrix['entries'])!=len(contracts) or {e['scenario'] for e in matrix['entries']}!=set(contracts) or any(e['result']!='PASS' or e['level']!='native-fixed-install' for e in matrix['entries']):raise ValueError('quality_scenario_coverage')
 host=read(r['host']);integrity=read(r['integrity']);lock=read('skills.lock.json')['sources'][0];ids={s['name']:s['sha256'] for s in host['skills']}
 if host['result']!='PASS' or len(host['skills'])!=13 or ids!=lock['sha256'] or integrity['digests']!=ids or integrity['skillsUnchanged']!=13 or integrity['result']!='PASS':raise ValueError('quality_installed_identity')
 for field,target in [('pluginVersion','pluginVersion'),('pluginCommit','pluginCommit'),('skillSourceRef','sourceRef'),('skillSourceCommit','sourceCommit'),('platform','platform')]:
  if host[field]!=r[target]:raise ValueError('quality_installed_identity')
 if read('plugin.json')['version']!=r['pluginVersion'] or lock['sha']!=r['sourceCommit'] or lock['ref']!=r['sourceRef']:raise ValueError('quality_installed_identity')
 n=read(r['native']);q=read(r['quality']);manifest=n['manifest']
 if n['result']!='PASS' or n['level']!='fixed-install' or n['driverSha256']!=sha(bound(r['nativeDriver'])) or n['runtimeSha256']!=r['runtimeSha256'] or q['nativeProofSha256']!=sha(bound(r['native'])):raise ValueError('quality_native_identity')
 if q['result']!='PASS' or q['level']!='fixed-install' or q['driverSha256']!=sha(bound(r['qualityDriver'])) or q['pluginVersion']!=r['pluginVersion'] or q['runtimeIdentity']!=r['runtimeSha256'] or q['platform']!='darwin-arm64':raise ValueError('quality_execution_identity')
 if not all(n[k] is True for k in ['nativeTextAndGradientEditable','sourceAndPreviousExportsPreserved','installedSkillPreserved']) or q['nativeSourceAndExportsPreserved'] is not True or q['installedCodePreserved'] is not True:raise ValueError('quality_preservation')
 if n['independentReopens'][0]['model']['layers']!=n['independentReopens'][1]['model']['layers'] or n['independentReopens'][0]['points']!=n['independentReopens'][1]['points'] or manifest['sourceProjectSha256']!=n['sourceFiles']['project.vectorcraft']:raise ValueError('quality_native_reopen')
 if any(n['quality'][k]!='PASS' for k in ['artifactIntegrityStatus','lineageStatus','exchangeStatus','technicalStatus']) or len(n['quality']['outputs'])!=3 or any(o['status']!='PASS' for o in n['quality']['outputs']):raise ValueError('quality_native_decode')
 if any(q['originalFiles']['exported/'+name]!=digest for name,digest in n['exportedFiles'].items()):raise ValueError('quality_input_identity')
 rows=q['records'];cases={x['case']:x for x in rows}
 drift={'stale-'+s for s in ['native','candidate','manifest','auxiliary','target','rubric']}|{'stale-checker-'+s for s in ['src/evaluation/delivery_quality.py','src/harness/process_runner.py','skills/vectorcraft-use/scripts/exchange_loss.py']}
 required=drift|{'healthy-persistent-decode','real-decoder-unavailable','json-evidence-injection','legacy-unverified-origin','timeout-owned-group-and-restart','coordinator-sigkill-unknown-no-replay','shared-budget-before-snapshot'}|{'undecodable-'+f+'-maximal-qa-score' for f in ['png','pdf','svg']}
 if len(rows)!=19 or set(cases)!=required or any(x['result']!='PASS' for x in rows):raise ValueError('quality_boundary_coverage')
 checker={name:sha(bound(name)) for name in ['src/evaluation/delivery_quality.py','src/harness/process_runner.py','skills/vectorcraft-use/scripts/exchange_loss.py']}
 def checked(row,status):
  request=row['request'];i=request['input'];e=i['technicalEvidence'];snapshot=row['snapshot']
  if i['technicalEvidenceOrigin']!='checked-decoder' or i['technicalStatus']!=status or e['technicalStatus']!=status or e['artifactIntegrityStatus']!='PASS' or e['runtimeIdentity']!=r['runtimeSha256'] or e['projectRevision']!=i['projectRevision'] or e['checkerFiles']!=checker or e['checkerSha256']!=checker['src/evaluation/delivery_quality.py'] or e['launcherSha256']!=checker['src/harness/process_runner.py']:raise ValueError('quality_checked_identity')
  if any(e[k]!='NOT_RUN' for k in ['engineeringStatus','nativeReopenStatus','creativeStatus']) or e['acceptanceStatus']!=('blocked' if status=='FAIL' else 'pending'):raise ValueError('quality_claim_escalation')
  folder=i['native'].removesuffix('/project.vectorcraft').removeprefix('QA_NATIVE/')
  expected={name:q['originalFiles'][folder+'/'+name] for name in e['files']}
  if expected!=e['files'] or e['manifestSha256']!=q['originalFiles'][folder+'/manifest.json'] or request['fingerprints'][i['native']]!=i['projectRevision']:raise ValueError('quality_file_binding')
  if snapshot['checkerFiles']!=checker or snapshot['state']!='review_ready' or snapshot['attempts']!=1 or snapshot['budget']['attempts']!=1 or snapshot['bytes']!=snapshot['budget']['bytes'] or snapshot['bytes']<=0 or snapshot['readonlySnapshotFiles']!=len(e['files'])+1 or snapshot['bindingVerified'] is not True or snapshot['taskId']!=i['technicalCheckId']:raise ValueError('quality_snapshot_budget')
  rejected_svg=status=='FAIL' and row['case']=='undecodable-svg-maximal-qa-score' and e.get('error')=='exchange_report_invalid_svg' and not e['outputs']
  if not rejected_svg and (len(e['outputs'])!=3 or {o['path'] for o in e['outputs']}!={o['path'] for o in manifest['outputs']} or any(o['sha256']!=e['files'][o['path']] for o in e['outputs'])):raise ValueError('quality_output_binding')
  return e
 healthy=cases['healthy-persistent-decode'];e=checked(healthy,'PASS')
 if any(o['status']!='PASS' for o in e['outputs']) or healthy['restartDeduplicated'] is not True or healthy['engineeringNativeReopenNotPromoted'] is not True:raise ValueError('quality_positive')
 for fmt in ['png','pdf','svg']:
  row=cases['undecodable-'+fmt+'-maximal-qa-score'];e=checked(row,'FAIL');response=row['response'];receipt=row['receipt']
  if row['explicitQaReceipt'] is not True or row['explicitQaMutation'] is not True or receipt['scores']!={k:4 for k in ['structure','text','brand','layout','legibility']} or 'explicit QA' not in receipt['reviewer']['identity'] or receipt['reviewer']['independenceEvidence'] is not None:raise ValueError('quality_synthetic_receipt_disclosure')
  if response['technicalStatus']!='FAIL' or response['creativeStatus']!='PASS' or response['engineeringStatus']!='NOT_RUN' or response['acceptanceStatus']!='blocked' or response['state']!='technical_failed' or response['independent'] is not False or response['independenceStatus']!='not_claimed' or not (any(o['path'].endswith('.'+fmt) and o['status']=='FAIL' for o in e['outputs']) or fmt=='svg' and e.get('error')=='exchange_report_invalid_svg' and not e['outputs']) or 'duplicate_review_receipt' not in row['duplicateReceiptRefusal']['error']:raise ValueError('quality_failure_override')
 missing=cases['real-decoder-unavailable'];e=checked(missing,'NOT_RUN')
 if missing['missingModules']!={'PIL':True,'fitz':True} or any(o['status']!='NOT_RUN' or o['reason']!='decoder_unavailable' for o in e['outputs']) or missing['response']['acceptanceStatus']!='pending' or missing['response']['state']!='technical_pending':raise ValueError('quality_not_run_escalation')
 if cases['legacy-unverified-origin']['origin']!='caller_unverified' or len(cases['json-evidence-injection']['refusals'])!=2 or any('technical_evidence_requires_check' not in x['error'] for x in cases['json-evidence-injection']['refusals']):raise ValueError('quality_origin_injection')
 for name in drift:
  row=cases[name]
  if row['beforeSha256']==row['afterSha256'] or 'stale_review_binding' not in row['refusal']['error']:raise ValueError('quality_stale_refusal')
  if name.startswith('stale-checker-') and (row['isolatedPublishedCodeCopy'] is not True or row['beforeSha256']!=checker[name.removeprefix('stale-checker-')]):raise ValueError('quality_checker_identity')
 for name in ['timeout-owned-group-and-restart','coordinator-sigkill-unknown-no-replay']:
  row=cases[name];before=row['beforeDecoder']
  if before['taskAttempts']!=1 or before['budgetAttempts']!=1 or before['budgetBytes']<=0 or before['snapshotFiles']!=len(manifest['files'])+4 or before['allReadonly'] is not True or 'reconcile_required' not in row['restart']['error'] or row['budgetAttemptsAfterRestart']!=1:raise ValueError('quality_replay_budget')
  if name.startswith('timeout') and (row['stopped'] is not True or row['state']!='reconciling' or 'technical_check_interrupted' not in row['error']['error']):raise ValueError('quality_timeout_stop')
  if name.startswith('coordinator') and (row['recordedState']!='running' or row['liveOwnedGroupAfterCrash'] is not True or row['ownedGroupStopped'] is not True):raise ValueError('quality_unknown_stop')
 row=cases['shared-budget-before-snapshot']
 if row['budgetAttempts']!=1 or row['unlaunchedSnapshotAbsent'] is not True or 'budget_exceeded' not in row['error']['error']:raise ValueError('quality_shared_budget')
 print(json.dumps({'result':'PASS','scenarios':len(contracts),'nativeBoundaryCases':19,'taskClosed':'6.3','scope':'actual public61/source43 on Codex macOS arm64; creative judgment not executed'}))
if __name__=='__main__':main()
