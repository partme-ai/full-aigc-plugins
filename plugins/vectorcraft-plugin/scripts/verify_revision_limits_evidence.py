#!/usr/bin/env python3
"""核验固定62停滞、轮数上限与桌面陈旧源子集；不关闭完整6.6。"""
import builtins,hashlib,json
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

REPORT='docs/evidence/vectorcraft-revision-limits-fixed62-20261009.json'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def verify(root=ROOT):
 root=Path(root)
 def local(name):
  name = payload_name(name)
  if not isinstance(name,str) or Path(name).is_absolute() or '\\' in name or any(p in ('','.','..') for p in name.split('/')):raise ValueError('invalid_evidence_path')
  p=root/name
  if not p.is_file() or not p.resolve().is_relative_to(root.resolve()) or any(x.is_symlink() for x in [p,*p.parents] if x.is_relative_to(root)):raise ValueError('invalid_evidence_path')
  return p
 r=json.loads(local(REPORT).read_text())
 index=json.loads((root/'docs/evidence-index.json').read_text()) if (root/'docs/evidence-index.json').is_file() else {'entries':[]}
 known=builtins.next((x['dependencies'] for x in index['entries'] if x['path']==REPORT),{})
 def bound(name):
  expected=r['fingerprints'][name];p=local(name)
  if sha(p)==expected:return p
  candidates=[n for n,h in known.items() if h==expected and n.endswith('/'+name)]
  if len(candidates)!=1 or sha(local(candidates[0]))!=expected:raise ValueError('stale_revision_limits_evidence')
  return local(candidates[0])
 for name in r['fingerprints']:bound(name)
 def read(name):
  if name not in r['fingerprints']:raise ValueError('unbound_revision_limits_evidence')
  return json.loads(bound(name).read_text())
 if r['result']!='PASS' or r['tasksClosed']!=[] or set(r['cases'])!={'small-improvement','lower-score','round-limit','stale-gui','guiSnapshots'}:raise ValueError('limits_scope')
 lock=read('skills.lock.json')['sources'][0]
 if read('plugin.json')['version']!=r['pluginVersion'] or lock['ref']!=r['sourceRef']:raise ValueError('limits_identity')
 host=read('docs/evidence/vc-qa-002/host-fixed62.json')
 if host['pluginVersion']!=r['pluginVersion'] or host['pluginCommit']!=r['pluginCommit'] or {x['name']:x['sha256'] for x in host['skills']}!=lock['sha256']:raise ValueError('limits_host_identity')
 integrity=read('docs/evidence/vc-qa-002/integrity-limits-fixed62.json')
 if integrity['result']!='PASS' or integrity['skillsUnchanged']!=13 or integrity['digests']!=lock['sha256']:raise ValueError('limits_installed_integrity')
 field='appearance.items.0.paint';value={'type':'solid','color':{'model':'rgb','r':0,'g':1,'b':0}}
 def common(n,driver):
  if n['result']!='PASS' or n['pluginVersion']!=r['pluginVersion'] or n['sourceRef']!=r['sourceRef'] or n['platform']!=r['platform'] or n['driverSha256']!=sha(bound(driver)):raise ValueError('limits_execution_identity')
  first=n['initialRequest'];p=n['proposal'];auth=first['input']['authorization'];a=p['authorization']
  if p['requestId']!=first['id'] or p['bindingHash']!=first['bindingHash'] or p['expectedProjectRevision']!=first['input']['projectRevision'] or p['changes']!=[{'objectId':2,'field':field,'value':value}] or a!={**auth,'objects':[2],'fields':[field]}:raise ValueError('limits_authority')
  if n['best']['engineeringStatus']!='NOT_RUN' or n['best']['acceptanceStatus']!='pending':raise ValueError('limits_claim_escalation')
  e=first['input']['technicalEvidence']
  if first['input']['technicalEvidenceOrigin']!='checked-decoder' or first['input']['technicalStatus']!='PASS' or e['technicalStatus']!='PASS' or len(e['outputs'])!=3 or any(x['status']!='PASS' for x in e['outputs']):raise ValueError('limits_checked_decode')
 def obj(model,id):
  result=[]
  def walk(v):
   if isinstance(v,dict):
    if v.get('id')==id:result.append(v)
    for x in v.values():walk(x)
   elif isinstance(v,list):
    for x in v:walk(x)
  walk(model['layers'])
  if len(result)!=1:raise ValueError('limits_control_object')
  return result[0]
 for mode,score,reason in [('small-improvement',2.05,'stagnation'),('lower-score',1.9,'stagnation'),('round-limit',3,'round_limit')]:
  n=read(r['cases'][mode]);common(n,'scripts/qa/revision_limits.ts');first=n['initialRequest'];next=n['nextRequest'];best=n['best'];cycle=n['cycle'];chosen=next if score>2 else first
  if n['mode']!=mode or n['feedbackScore']!=score or cycle['state']!='stopped' or cycle['reason']!=reason or cycle['rounds']!=1 or cycle['latest']!=next['id'] or cycle['policy']!={'maxRounds':1 if mode=='round-limit' else 2,'stagnationLimit':1,'minImprovement':.1}:raise ValueError('limits_stop')
  if best['requestId']!=chosen['id'] or cycle['best']!=chosen['id'] or best['score']!=max(2,score) or best['projectRevision']!=chosen['input']['projectRevision'] or best['latestRequestId']!=next['id'] or best['reason']!=reason or not best['unresolvedIssues']:raise ValueError('limits_best')
  if n['sharedAttempts']!=(5 if score>2 else 4) or best['sharedBudget']['attempts']!=n['sharedAttempts'] or cycle['budget']!=n['proposal']['authorization']['budgetId']:raise ValueError('limits_budget')
  if obj(n['sourceModel'],3)!=obj(n['revisedModel'],3) or obj(n['revisedModel'],2)['appearance']['items'][0]['paint']!=value or n['sourceModel']['artboards']!=n['revisedModel']['artboards'] or n['sourcePreserved'] is not True or n['controlTextPreserved'] is not True:raise ValueError('limits_control')
  if n['allGroupsStopped'] is not True or n['registeredGroups']<1:raise ValueError('limits_process_stop')
  e=next['input']['technicalEvidence'];m=n['manifest'];execution=n['execution']
  if next['input']['technicalEvidenceOrigin']!='checked-decoder' or e['technicalStatus']!='PASS' or len(e['outputs'])!=3 or any(x['status']!='PASS' for x in e['outputs']) or e['files']!=m['files'] or m['sourceProjectSha256']!=first['input']['projectRevision'] or next['input']['native']!=execution['output']+'/project.vectorcraft' or execution['state']!='awaiting_review':raise ValueError('limits_lineage')
 n=read(r['cases']['stale-gui']);common(n,'scripts/qa/revision_stale_gui.ts');gui=n['gui']
 if n['guiDriverSha256']!=sha(bound('scripts/qa/revision_gui_edit.py')) or any(gui[x] is not True for x in ['listenerOwnedByPID','ownedProcessesStopped','nativeDocumentChanged','nativeReopened','persistedContentMatches']) or gui['sourceBeforeSha256']==gui['sourceAfterSha256']:raise ValueError('limits_gui')
 if 'stale_review_binding' not in n['refusal'] or n['sharedAttempts']!=2 or n['registeredGroupsBefore']!=n['registeredGroupsAfter'] or n['newOutputAbsent'] is not True or n['originalSourcePreserved'] is not True or n['allGroupsStopped'] is not True or n['best']['requestId']!=n['initialRequest']['id']:raise ValueError('limits_stale')
 if sha(bound(r['cases']['guiSnapshots']))!=gui['snapshotsSha256']:raise ValueError('limits_gui_snapshots')
 snapshots=read(r['cases']['guiSnapshots']);modified=snapshots['modified'];reopened=snapshots['reopened']
 if obj(snapshots['original'],2)==obj(modified,2) or obj(snapshots['original'],3)!=obj(modified,3) or reopened!={**modified,'metadata':{**modified['metadata'],'modified':reopened['metadata']['modified']}}:raise ValueError('limits_gui_snapshots')
 print(json.dumps({'result':'PASS','nativeRevisions':3,'ownedDesktopStaleCase':1,'tasksClosed':[],'scope':'fixed62 subset; full6.6 remains open'}))
if __name__=='__main__':verify()
