#!/usr/bin/env python3
"""核验发布门禁两场景和原范围复用；静态通过不能提升市场或运行时声明。"""
import builtins,hashlib,importlib.util,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT='docs/evidence/vectorcraft-release-gate-20261009.json'
def main():
 r=json.loads((ROOT/REPORT).read_text());index=json.loads((ROOT/'docs/evidence-index.json').read_text());known=builtins.next((x['dependencies'] for x in index['entries'] if x['path']==REPORT),{})
 def bound(name):
  if not isinstance(name,str) or Path(name).is_absolute() or '\\' in name or any(p in ('','.','..') for p in name.split('/')):raise ValueError('release_qualification_path')
  p=ROOT/name
  if not p.resolve().is_relative_to(ROOT.resolve()) or any(x.is_symlink() for x in [p,*p.parents] if x.is_relative_to(ROOT)):raise ValueError('release_qualification_changed')
  expected=r['fingerprints'][name]
  if p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==expected:return p
  candidates=[n for n,h in known.items() if h==expected and n.endswith('/'+name)]
  if len(candidates)!=1:raise ValueError('release_qualification_changed')
  name=candidates[0]
  if Path(name).is_absolute() or '\\' in name or any(x in ('','.','..') for x in name.split('/')):raise ValueError('release_qualification_changed')
  archived=ROOT/name
  if not archived.resolve().is_relative_to(ROOT.resolve()) or not archived.is_file() or any(x.is_symlink() for x in [archived,*archived.parents] if x.is_relative_to(ROOT)) or hashlib.sha256(archived.read_bytes()).hexdigest()!=expected:raise ValueError('release_qualification_changed')
  return archived
 for name in r['fingerprints']:bound(name)
 read=lambda name:json.loads(bound(name).read_text())
 foundation=bound('docs/evidence/vc-rl-001/docs-only-input/tasks.md.txt').read_text()
 if any(re.search(r'^- \[ \] '+str(section)+r'\.',foundation,re.M) or not re.search(r'^- \[x\] '+str(section)+r'\.',foundation,re.M) for section in range(1,7)):raise ValueError('release_foundation_preconditions')
 if r['result']!='PASS' or r['tasksClosed']!=['7.1','7.2','7.3']:raise ValueError('release_qualification_closure')
 spec=bound('openspec/changes/establish-v1-plugin/specs/release-compatibility/spec.md').read_text().split('### Requirement: VC-RL-001 ',1)[1].split('### Requirement:',1)[0];contracts={s.splitlines()[0]:hashlib.sha256(s.strip().encode()).hexdigest() for s in spec.split('#### Scenario: ')[1:]};matrix=read(r['scenarioMatrix'])
 if matrix['scenarioContracts']!=contracts or len(matrix['entries'])!=2 or {x['scenario'] for x in matrix['entries']}!=set(contracts) or any(x['result']!='PASS' for x in matrix['entries']):raise ValueError('release_qualification_scenarios')
 code=bound('scripts/release_gate.py');s=importlib.util.spec_from_file_location('qualified_release_gate',code);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);positive=read(r['positive']);negative=read(r['marketplaceNegative']);doc=read(r['documentationOnly']);current_files=all((ROOT/name).is_file() and hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest for name,digest in r['fingerprints'].items());current=m.assess(ROOT) if current_files else positive
 bundle=read('docs/release-evidence.json');host=read(bundle['host']);lock=read('skills.lock.json')['sources'][0];technical=read(bundle['technical'])
 if host['pluginVersion']!=r['pluginVersion'] or host['skillSourceRef']!=r['sourceRef'] or host['pluginCommit']!=r['pluginCommit'] or host['skillSourceCommit']!=r['sourceCommit'] or {x['name']:x['sha256'] for x in host['skills']}!=lock['sha256'] or technical['pluginVersion']!=r['pluginVersion']:raise ValueError('release_qualification_identity')
 native_spec=importlib.util.spec_from_file_location('release_original_native',bound('scripts/verify_revision_evidence.py'));native_module=importlib.util.module_from_spec(native_spec);native_spec.loader.exec_module(native_module)
 import contextlib,io
 with contextlib.redirect_stdout(io.StringIO()):native_module.verify(ROOT)
 if current!=positive or positive!=negative or any(x['status']!='PASS' for x in positive['layers'].values()) or positive['publishable']!={'development':True,'marketplace':False}:raise ValueError('release_qualification_layers')
 if doc.get('driverSha256')!=hashlib.sha256(bound('scripts/qa/release_docs_boundary.py').read_bytes()).hexdigest() or doc.get('gateCodeSha256')!=hashlib.sha256(bound('scripts/release_gate.py').read_bytes()).hexdigest():raise ValueError('release_qualification_boundary_identity')
 if [x['check'] for x in doc['records']]!=['docs','openspec','gate'] or [x['exitCode'] for x in doc['records']]!=[0,0,1] or doc['gate']['publishable']!={'development':False,'marketplace':False} or doc['gate']['layers']['host']['status']=='PASS' or doc['gate']['layers']['native']['status']=='PASS' or doc['priorEvidenceRetained'] is not True:raise ValueError('release_qualification_docs_only')
 if 'failures=12' not in bound(r['red']).read_text() or 'release_gate_behavior_missing' not in bound(r['red']).read_text() or 'Ran 12 tests' not in bound(r['green']).read_text() or '\nOK' not in bound(r['green']).read_text():raise ValueError('release_qualification_tests')
 print(json.dumps({'result':'PASS','scenarios':2,'tasksClosed':r['tasksClosed'],'scope':'external release tooling;existing fixed63 native proof reused unchanged;no new native/model/marketplace claim'}))
if __name__=='__main__':main()
