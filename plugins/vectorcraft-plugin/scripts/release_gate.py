#!/usr/bin/env python3
"""分别核验固定发布的六层证据；只读门禁不自动修改宿主支持或市场资格。"""
import argparse,contextlib,hashlib,importlib.util,io,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def tree_digest(directory):
 if directory.is_symlink() or any(p.is_symlink() for p in directory.rglob('*')):raise ValueError('linked_skill')
 return hashlib.sha256(''.join(p.relative_to(directory).as_posix()+'\0'+sha(p)+'\n' for p in sorted(directory.rglob('*')) if p.is_file()).encode()).hexdigest()
def assess(root=ROOT):
 """返回结构、技能源、运行时、宿主、任务、原生交付各自状态与发布范围。"""
 root=Path(root);layers={k:{'status':'NOT_RUN','reason':'evidence_not_checked'} for k in ['structure','skills','runtime','host','task','native']}
 def safe(name):
  if not isinstance(name,str) or Path(name).is_absolute() or '\\' in name or any(p in ('','.','..') for p in name.split('/')):raise ValueError('release_evidence_path')
  # 执行载荷收敛在 vectorcraft-harness：历史证据绑定的 skills/<domain>/scripts/ 路径按字节等价映射。
  prefix='skills/vectorcraft-'
  if isinstance(name,str) and name.startswith(prefix) and '/scripts/' in name and not (root/name).is_file():
   candidate=root/('skills/vectorcraft-harness/scripts/'+name.split('/scripts/',1)[1])
   if candidate.is_file():name=candidate.relative_to(root).as_posix()
  p=root/name
  if not p.resolve().is_relative_to(root.resolve()) or any(x.is_symlink() for x in [p,*p.parents] if x.is_relative_to(root)):raise ValueError('release_evidence_path')
  return p
 def read(name):return json.loads(safe(name).read_text())
 try:bundle=read('docs/release-evidence.json')
 except (OSError,ValueError,TypeError):return {'schema':'vectorcraft-release-readiness/v1','layers':layers,'publishable':{'development':False,'marketplace':False},'marketplaceBlockers':['release_bundle_unavailable']}
 def bound(name):
  if name not in bundle.get('fingerprints',{}):raise ValueError('unbound_release_evidence')
  p=safe(name)
  if sha(p)!=bundle['fingerprints'][name]:raise ValueError('release_evidence_changed')
  return p
 def bjson(name):return json.loads(bound(name).read_text())
 def check(name,fn):
  try:layers[name]={'status':'PASS',**fn()}
  except FileNotFoundError:layers[name]={'status':'NOT_RUN','reason':'release_evidence_missing'}
  except Exception as error:
   message=str(error);layers[name]={'status':'FAIL','reason':message if re.fullmatch('[a-z_]+',message) else 'release_check_failed'}
 def structure():
  if set(bundle)!={'schema','pluginVersion','sourceRef','sourceCommit','host','technical','integrity','fingerprints'} or bundle['schema']!='vectorcraft-release-evidence/v1':raise ValueError('invalid_release_bundle')
  p=bjson('plugin.json');identity=bjson('docs/current-identity.json');bound('scripts/release_gate.py')
  if p['name']!='vectorcraft' or not re.fullmatch(r'0\.1\.0-dev\.\d+',p['version']) or p['version']!=bundle['pluginVersion'] or identity['pluginVersion']!=p['version'] or not p.get('license') or not p.get('description'):raise ValueError('release_manifest_identity')
  return {'evidence':['plugin.json','docs/current-identity.json'],'pluginVersion':p['version']}
 def skills():
  lock=bjson('skills.lock.json')['sources']
  if len(lock)!=1:raise ValueError('ambiguous_skill_authority')
  source=lock[0]
  if source['ref']!=bundle['sourceRef'] or source['sha']!=bundle['sourceCommit'] or len(source['skills'])!=14 or set(source['skills'])!=set(source['sha256']):raise ValueError('release_skill_identity')
  if any(tree_digest(root/'skills'/name)!=digest for name,digest in source['sha256'].items()):raise ValueError('release_skill_drift')
  return {'evidence':['skills.lock.json'],'sourceRef':source['ref'],'sourceCommit':source['sha'],'skills':14}
 def technical():
  r=bjson(bundle['technical'])
  if r.get('schema') not in ('vectorcraft-revision-fixed/v1','vectorcraft-revision-fixed/v2') or r.get('result')!='PASS' or r['pluginVersion']!=bundle['pluginVersion'] or r['sourceRef']!=bundle['sourceRef'] or r['sourceCommit']!=bundle['sourceCommit']:raise ValueError('release_technical_identity')
  for name,digest in r['fingerprints'].items():
   if sha(bound(name))!=digest:raise ValueError('release_technical_dependency')
  return r
 def runtime():
  r=technical();identity=bjson('docs/current-identity.json');lock=json.loads((root/'skills/vectorcraft-harness/scripts/runtime.lock.json').read_text());integrity=bjson(bundle['integrity'])
  if r['runtimeSha256']!=identity['runtime']['binarySha256'] or r['runtimeSha256']!=lock['artifacts']['darwin-arm64']['binarySha256']:raise ValueError('release_runtime_identity')
  for name,digest in integrity['installedCodeDigests'].items():
   if sha(bound(name))!=digest:raise ValueError('release_installed_code_drift')
  return {'evidence':[bundle['technical'],bundle['integrity']],'runtimeSha256':r['runtimeSha256'],'platform':r['platform']}
 def host():
  r=bjson(bundle['host']);source=bjson('skills.lock.json')['sources'][0];integrity=bjson(bundle['integrity']);p=bjson('plugin.json')
  # 技能数与未变技能数一律以锁定源身份（source['sha256'] 键数）为准，不得硬编码历史域技能数。
  count=len(source['sha256'])
  if r['result']!='PASS' or r['pluginVersion']!=p['version'] or r['skillSourceRef']!=source['ref'] or r['skillSourceCommit']!=source['sha'] or len(r['skills'])!=count or any(x['enabled'] is not True for x in r['skills']) or {x['name']:x['sha256'] for x in r['skills']}!=source['sha256'] or integrity['digests']!=source['sha256'] or integrity['skillsUnchanged']!=count:raise ValueError('release_host_identity')
  return {'evidence':[bundle['host']],'hostVersion':r['hostVersion'],'platform':r['platform'],'scope':r['scope'],'excluded':r['excluded']}
 def task():
  r=technical();n=bjson(r['cases']['guards']);execution=n['execution'];first=n['initialRequest'];next_request=n['nextRequest']
  if n['result']!='PASS' or n['pluginVersion']!=bundle['pluginVersion'] or n['sourceRef']!=bundle['sourceRef'] or execution['state']!='awaiting_review' or not execution['executionTaskId'] or next_request['input']['native']!=execution['output']+'/project.vectorcraft' or n['proposal']['expectedProjectRevision']!=first['input']['projectRevision'] or n['allGroupsStopped'] is not True:raise ValueError('release_task_execution')
  return {'evidence':[r['cases']['guards']],'executionTaskId':execution['executionTaskId'],'scope':'actual installed native task;explicit QA feedback,no model routing claim'}
 def native():
  technical();module_path=bound('scripts/verify_revision_evidence.py');spec=importlib.util.spec_from_file_location('release_native_verifier',module_path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.REPORT=bundle['technical']
  with contextlib.redirect_stdout(io.StringIO()):module.verify(root)
  return {'evidence':[bundle['technical']],'scope':'current four-scenario native revision evidence;creative judgment and other platforms excluded'}
 for name,fn in [('structure',structure),('skills',skills),('runtime',runtime),('host',host),('task',task),('native',native)]:check(name,fn)
 development=all(x['status']=='PASS' for x in layers.values());blockers=[]
 if not development:blockers.append('six_layer_evidence_incomplete')
 try:
  status=read('project-status.json');text=safe('openspec/changes/establish-v1-plugin/tasks.md').read_text();open_tasks=re.findall(r'^- \[ \] (\d+\.\d+) ',text,re.M);all_tasks=set(re.findall(r'^- \[[xX ]\] (\d+\.\d+) ',text,re.M))
  if open_tasks:blockers.append('implementation_tasks_open')
  if status['implementation']!='complete':blockers.append('implementation_not_complete')
  if status['marketplaceEligible'] is not True or not status['supportedPluginHosts']:blockers.append('marketplace_approval_missing')
  index=read('docs/evidence-index.json');entries=index['entries'];coverage=set()
  for e in entries:
   try:
    if e['status']!='PASS' or sha(safe(e['path']))!=e['sha256'] or any(sha(safe(name))!=digest for name,digest in e['dependencies'].items()):continue
    coverage.update(task for task in e['tasks'] if status['taskEvidence'].get(task)==e['path'])
   except (OSError,ValueError,KeyError,TypeError):continue
  if not all_tasks.issubset(coverage):blockers.append('full_task_evidence_coverage_missing')
  if layers['host'].get('excluded'):blockers.append('host_scope_exclusions_open')
 except (OSError,ValueError,KeyError,TypeError):blockers.append('full_release_status_unverified')
 return {'schema':'vectorcraft-release-readiness/v1','pluginVersion':bundle.get('pluginVersion'),'sourceRef':bundle.get('sourceRef'),'layers':layers,'publishable':{'development':development,'marketplace':development and not blockers},'marketplaceBlockers':blockers,'scope':'readonly release evidence gate;development scope does not assert complete V1 or modify host/marketplace approval'}
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--require',choices=['development','marketplace'],default='development');args=parser.parse_args();result=assess();print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if result['publishable'][args.require] else 1
if __name__=='__main__':raise SystemExit(main())
