#!/usr/bin/env python3
"""逐场景核对公开固定安装的真实血缘和拒绝证据；创作验收独立。"""
import hashlib,json,re
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

REPORT='docs/evidence/vectorcraft-lineage-fixed58-20261009.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def local(name):
 name = payload_name(name)
 if not isinstance(name,str) or Path(name).is_absolute() or '\\' in name or any(p in ('','.','..') for p in name.split('/')):raise ValueError('invalid_evidence_path')
 p=ROOT/name
 if not p.resolve().is_relative_to(ROOT.resolve()) or any(x.is_symlink() for x in [p,*p.parents] if x.is_relative_to(ROOT)):raise ValueError('invalid_evidence_path')
 return p
def digest(files):return hashlib.sha256(''.join(n+'\0'+h+'\n' for n,h in sorted(files.items())).encode()).hexdigest()
def main():
 report=json.loads(local(REPORT).read_text())
 index=json.loads(local('docs/evidence-index.json').read_text()) if local('docs/evidence-index.json').is_file() else {'entries':[]}
 known=next((x['dependencies'] for x in index['entries'] if x['path']==REPORT),{})
 def bound(name):
  h=report['fingerprints'][name];p=local(name)
  if p.is_file() and sha(p)==h:return p
  archive=[n for n,v in known.items() if v==h and n.endswith('/'+name)]
  if len(archive)!=1 or sha(local(archive[0]))!=h:raise ValueError('stale_lineage_evidence')
  return local(archive[0])
 def read(name):return json.loads(bound(name).read_text())
 for name in report['fingerprints']:bound(name)
 if report['result']!='PASS' or report['tasksClosed']!=['5.3']:raise ValueError('incomplete_lineage')
 spec_name='openspec/changes/establish-v1-plugin/specs/artifact-delivery/spec.md';spec_text=local(spec_name).read_text()
 if '### Requirement: VC-AR-001 ' not in spec_text:
  # 规格裁剪后 VC-AR-001 移出当前规格文件；历史证据按执行时归档规格核对。
  archived=[ROOT/p for p in known if p.endswith('/'+spec_name) and (ROOT/p).is_file() and '### Requirement: VC-AR-001 ' in (ROOT/p).read_text()]
  if len(archived)<1:raise ValueError('lineage_spec_archive')
  spec_text=archived[0].read_text()
 block=spec_text.split('### Requirement: VC-AR-001 ',1)[1].split('### Requirement:',1)[0]
 contracts={s.splitlines()[0].split()[0]:hashlib.sha256(s.strip().encode()).hexdigest() for s in block.split('#### Scenario: ')[1:]}
 matrix=read(report['scenarioMatrix'])
 if matrix['scenarioContracts']!=contracts or len(matrix['entries'])!=len(contracts) or {x['scenario'] for x in matrix['entries']}!=set(contracts) or any(x['level']!='native-fixed-install' or x['result']!='PASS' for x in matrix['entries']):raise ValueError('scenario_coverage')
 host=read(report['host']);integrity=read(report['integrity']);lock=read('skills.lock.json')['sources'][0]
 identities={x['name']:x['sha256'] for x in host['skills']}
 if len(host['skills'])!=13 or identities!=lock['sha256'] or integrity['digests']!=identities or integrity['skillsUnchanged']!=13 or integrity['result']!='PASS':raise ValueError('installed_identity')
 for field,target in [('pluginVersion','pluginVersion'),('pluginCommit','pluginCommit'),('skillSourceRef','sourceRef'),('skillSourceCommit','sourceCommit'),('platform','platform')]:
  if host[field]!=report[target]:raise ValueError('installed_identity')
 if lock['sha']!=report['sourceCommit'] or lock['ref']!=report['sourceRef'] or read('plugin.json')['version']!=report['pluginVersion'] or host['result']!='PASS':raise ValueError('installed_identity')
 native=read(report['native']);quality=read(report['publicQuality'])
 if native['result']!='PASS' or native['runtimeSha256']!=report['runtimeSha256'] or native['driverSha256']!=sha(bound(report['nativeDriver'])) or digest(native['skillFiles'])!=identities['vectorcraft-cli-export']:raise ValueError('native_identity')
 if not all(native[k] is True for k in ['movedNativeReopened','sourceUnchanged','preflightRefusedBeforeInstall']):raise ValueError('native_preservation')
 def lineage(row):
  m,r=row['manifest'],row['lineage'];files={k:v for k,v in m['files'].items() if k!='lineage.json'}
  h=hashlib.sha256((json.dumps(r,ensure_ascii=False,indent=2)+'\n').encode()).hexdigest()
  version=hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
  if r['schema']!='vectorcraft-artifact-lineage/v1' or r['files']!=files or r['version']!=version or m['files']['lineage.json']!=h or m['lineage']['sha256']!=h or m['lineage']['version']!=version or m['lineage']['logicalId']!=r['logicalId']:raise ValueError('lineage_binding')
  if not re.fullmatch(r'vectorcraft:[0-9a-f-]{36}',r['logicalId']) or r['sourceTask']!={'id':m['executionId'],'scope':'workflow-execution','planSha256':files['plan.json']} or not m['executionId']:raise ValueError('lineage_task')
  if r['native']!={'path':'project.vectorcraft','sha256':files['project.vectorcraft']} or r['outputs']!=[{'path':x['path'],'sha256':files[x['path']]} for x in m['outputs']]:raise ValueError('lineage_native_outputs')
  if r['assets']!={n:{k:a[k] for k in ['path','sha256']} for n,a in m['assets'].items()} or any(files[a['path']]!=a['sha256'] for a in r['assets'].values()) or not r['assets']:raise ValueError('lineage_dependency')
  if r['parent']!=m['lineage']['parent'] or r['parent']['projectSha256']!=m['sourceProjectSha256']:raise ValueError('lineage_parent')
  return m,r
 first,old=lineage(native['creation']);second,new=lineage(native['revision'])
 if old['parent']!={'projectSha256':None,'status':'creation'} or new['parent']!={'logicalId':old['logicalId'],'version':old['version'],'projectSha256':old['native']['sha256'],'status':'versioned'} or new['logicalId']!=old['logicalId'] or new['version']==old['version'] or new['sourceTask']['id']==old['sourceTask']['id']:raise ValueError('lineage_revision')
 if len(first['outputs'])!=3 or {r['format'] for r in first['outputs']}!={'svg','pdf','png'} or len(second['outputs'])!=1 or any(native['movedFiles'][k]!=v for k,v in first['files'].items()):raise ValueError('lineage_move')
 wanted={'same-name-replacement','asset-deletion','lineage-task-rebind','lineage-native-rebind','parent-version-rebind'}
 if len(native['refusals'])!=5 or {r['case'] for r in native['refusals']}!=wanted or any(r['result']!='PASS' for r in native['refusals']):raise ValueError('native_refusal')
 if quality['result']!='PASS' or quality['driverSha256']!=sha(bound(report['publicDriver'])) or quality['qualitySha256']!=sha(bound('src/evaluation/delivery_quality.py')) or quality['nativeProofSha256']!=sha(bound(report['native'])):raise ValueError('public_identity')
 rows={x['case']:x for x in quality['cases']}
 if len(quality['cases'])!=7 or set(rows)!=wanted|{'moved package with spaces','revised'}:raise ValueError('public_refusal_coverage')
 for name in wanted:
  row=rows[name]['quality']
  if rows[name]['result']!='PASS' or row['artifactIntegrityStatus']!='FAIL' or row['outputs'] or not row.get('error'):raise ValueError('public_refusal')
 for name,m,r in [('moved package with spaces',first,old),('revised',second,new)]:
  q=rows[name]['quality']
  if rows[name]['result']!='PASS' or any(q[k]!='PASS' for k in ['artifactIntegrityStatus','technicalStatus','lineageStatus']) or q['artifactLogicalId']!=r['logicalId'] or q['artifactVersion']!=r['version'] or q['sourceTask']!=r['sourceTask'] or q['projectRevision']!=m['files']['project.vectorcraft'] or q['files']!=m['files'] or q['runtimeIdentity']!=report['runtimeSha256'] or len(q['outputs'])!=len(m['outputs']) or any(x['status']!='PASS' for x in q['outputs']):raise ValueError('public_lineage')
 print(json.dumps({'result':'PASS','scope':'all current VC-AR-001 scenarios on actual Codex fixed58/source43 macOS arm64 only','scenarios':len(contracts),'publicCases':7,'taskClosed':'5.3'}))
if __name__=='__main__':main()
