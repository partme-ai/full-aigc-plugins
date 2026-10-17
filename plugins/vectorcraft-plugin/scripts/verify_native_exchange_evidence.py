#!/usr/bin/env python3
"""逐场景核验固定安装原生保全、交换损失和真实拒绝证据。"""
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

REPORT='docs/evidence/vectorcraft-native-exchange-fixed59-20261009.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def serialized(value):return hashlib.sha256((json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest()
def local(n):
 n = payload_name(n)
 if not isinstance(n,str) or Path(n).is_absolute() or '\\' in n or any(p in ('','.','..') for p in n.split('/')):raise ValueError('invalid_evidence_path')
 p=ROOT/n
 if not p.resolve().is_relative_to(ROOT.resolve()) or any(x.is_symlink() for x in [p,*p.parents] if x.is_relative_to(ROOT)):raise ValueError('invalid_evidence_path')
 return p
def digest(files):return hashlib.sha256(''.join(n+'\0'+h+'\n' for n,h in sorted(files.items())).encode()).hexdigest()
def main():
 r=json.loads(local(REPORT).read_text());index=json.loads(local('docs/evidence-index.json').read_text()) if local('docs/evidence-index.json').is_file() else {'entries':[]};known=next((x['dependencies'] for x in index['entries'] if x['path']==REPORT),{})
 def bound(n):
  h=r['fingerprints'][n];p=local(n)
  if p.is_file() and sha(p)==h:return p
  candidates=[name for name,value in known.items() if value==h and name.endswith('/'+n)]
  if len(candidates)!=1 or sha(local(candidates[0]))!=h:raise ValueError('stale_native_exchange')
  return local(candidates[0])
 def read(n):return json.loads(bound(n).read_text())
 for n in r['fingerprints']:bound(n)
 if r['result']!='PASS' or r['tasksClosed']!=['5.6']:raise ValueError('incomplete_native_exchange')
 block=local('openspec/changes/establish-v1-plugin/specs/artifact-delivery/spec.md').read_text().split('### Requirement: VC-AR-002 ',1)[1].split('### Requirement:',1)[0]
 contracts={s.splitlines()[0]:hashlib.sha256(s.strip().encode()).hexdigest() for s in block.split('#### Scenario: ')[1:]};matrix=read(r['scenarioMatrix'])
 if matrix['scenarioContracts']!=contracts or len(matrix['entries'])!=len(contracts) or {x['scenario'] for x in matrix['entries']}!=set(contracts) or any(x['level']!='native-fixed-install' or x['result']!='PASS' for x in matrix['entries']):raise ValueError('scenario_coverage')
 h=read(r['host']);integrity=read(r['integrity']);lock=read('skills.lock.json')['sources'][0];identities={x['name']:x['sha256'] for x in h['skills']}
 if len(h['skills'])!=13 or identities!=lock['sha256'] or integrity['digests']!=identities or integrity['result']!='PASS' or integrity['skillsUnchanged']!=13:raise ValueError('installed_identity')
 for field,target in [('pluginVersion','pluginVersion'),('pluginCommit','pluginCommit'),('skillSourceRef','sourceRef'),('skillSourceCommit','sourceCommit'),('platform','platform')]:
  if h[field]!=r[target]:raise ValueError('installed_identity')
 if lock['sha']!=r['sourceCommit'] or lock['ref']!=r['sourceRef'] or read('plugin.json')['version']!=r['pluginVersion'] or h['result']!='PASS':raise ValueError('installed_identity')
 n=read(r['native']);m=n['manifest'];loss=n['lossReport'];q=n['quality']
 if n['result']!='PASS' or n['level']!='fixed-install' or n['platform']!=r['platform'] or n['runtimeSha256']!=r['runtimeSha256'] or n['driverSha256']!=sha(bound(r['driver'])) or n['qualitySha256']!=sha(bound('src/evaluation/delivery_quality.py')) or digest(n['skillFiles'])!=identities['vectorcraft-cli-export']:raise ValueError('native_identity')
 if not all(n[k] is True for k in ['nativeTextAndGradientEditable','sourceAndPreviousExportsPreserved','installedSkillPreserved']):raise ValueError('native_preservation')
 before,after=n['independentReopens']
 if before['model']['layers']!=after['model']['layers'] or before['model']['artboards']!=after['model']['artboards'] or before['points']!=after['points'] or serialized(before['model'])!=n['sourceFiles']['native.json'] or serialized(after['model'])!=n['exportedFiles']['native.json']:raise ValueError('native_reopen')
 if serialized(n['plan'])!=n['sourceFiles']['plan.json'] or m['sourceProjectSha256']!=n['sourceFiles']['project.vectorcraft'] or any(n['exportedFiles'][name]!=value for name,value in m['files'].items()) or serialized(m)!=n['exportedFiles']['manifest.json']:raise ValueError('native_file_binding')
 points=before['points']['points'];edited=n['editedPoints']['points']
 if len(points)<2 or len(points)!=len(edited) or points[0]['color']==edited[0]['color'] or points[1:]!=edited[1:] or {k:v for k,v in points[0].items() if k!='color'}!={k:v for k,v in edited[0].items() if k!='color'} or 'Still editable' not in json.dumps(n['editedNativeModel']) or n['editedManifest']['sourceProjectSha256']!=n['sourceFiles']['project.vectorcraft']:raise ValueError('native_editability')
 if serialized(loss)!=m['files']['exchange-loss.json'] or m['lossReport']!={'path':'exchange-loss.json','sha256':m['files']['exchange-loss.json']}:raise ValueError('loss_binding')
 if loss['native']!={'location':'project.vectorcraft','sha256':m['files']['project.vectorcraft']} or loss['inspection']!={'location':'native.json','sha256':m['files']['native.json']} or loss['acceptance']!='technical-observations-only':raise ValueError('loss_identity')
 if len(loss['outputs'])!=3 or {row['format'] for row in loss['outputs']}!={'svg','pdf','png'}:raise ValueError('loss_coverage')
 for row in loss['outputs']:
  if row['role']!='derivative' or row['nativeSubstitute'] is not False or row['sha256']!=m['files'][row['location']]:raise ValueError('loss_derivative')
  states={x['code']:x['status'] for x in row['changes']}
  if len(states)!=len(row['changes']) or states.get('native-editing-model')!='lost' or any(x not in ('lost','observed','unknown','blocked') for x in states.values()):raise ValueError('loss_semantics')
  if row['format'] in ('svg','pdf') and any(states.get(code)!='unknown' for code in ['font-portability','effect-fidelity']):raise ValueError('loss_unknown_fidelity')
  if row['format']=='png' and (states.get('editable-layers-paths-text')!='lost' or states.get('effect-keyframe-parameters')!='lost'):raise ValueError('loss_flattening')
  if row['format']=='svg':
   obs=row['observations'];scope=obs['rasterizationScope']
   if not obs['nativeTextObjectIds'] or obs['svgTextExportMode']!='appearance' or states.get('live-text-editability')!='lost' or states.get('lossless-vector-claim')!='blocked' or scope['losslessVectorClaimAllowed'] is not False or scope['vectorOnly'] is not False or len(scope['elements'])!=1 or scope['elements'][0]['classification']!='embedded-raster' or 'freeform gradients are written as images clipped to their shapes' not in row['warnings']:raise ValueError('loss_svg_disclosure')
 if any(q[k]!='PASS' for k in ['artifactIntegrityStatus','lineageStatus','exchangeStatus','technicalStatus']) or q['files']!=m['files'] or q['projectRevision']!=m['files']['project.vectorcraft'] or q['runtimeIdentity']!=r['runtimeSha256']:raise ValueError('decode_identity')
 if len(q['outputs'])!=3 or {x['path'] for x in q['outputs']}!={x['path'] for x in m['outputs']} or any(x['status']!='PASS' or x['sha256']!=m['files'][x['path']] for x in q['outputs']):raise ValueError('decode_coverage')
 if q['nativeReopenStatus']!='NOT_RUN' or q['creativeStatus']!='NOT_RUN' or q['acceptanceStatus']!='pending':raise ValueError('decode_claim_escalation')
 wanted={'native-substitute-'+fmt for fmt in ['svg','pdf','png']}|{'wrong-native','wrong-inspection','wrong-export','false-font-fidelity','false-effect-fidelity','missing-output','duplicate-output','false-approval','false-text-editability','wrong-text-mode','missing-report','invalid-report-json','invalid-inspection','corrupt-png','corrupt-pdf','corrupt-svg','corrupt-native'}
 if len(n['refusals'])!=20 or {x['case'] for x in n['refusals']}!=wanted:raise ValueError('refusal_coverage')
 for row in n['refusals']:
  if row['result']!='PASS':raise ValueError('refusal_failed')
  if row['case']=='corrupt-native':
   if not row['knownNativeRefusal'] or 'outcome_unknown' in row['knownNativeRefusal']:raise ValueError('native_corruption_refusal')
  elif row['freshManifestAndLineageHashes'] is not True or row['quality']['artifactIntegrityStatus']!='PASS' or row['quality']['technicalStatus']!='FAIL' or row['quality']['acceptanceStatus']!='blocked' or not row['quality'].get('error') and not any(x['status']=='FAIL' for x in row['quality']['outputs']):raise ValueError('refusal_invalid')
 print(json.dumps({'result':'PASS','scope':'all current VC-AR-002 scenarios on actual public59/source43 Codex macOS arm64 only','scenarios':len(contracts),'decodedExports':3,'refusals':20,'taskClosed':'5.6'}))
if __name__=='__main__':main()
