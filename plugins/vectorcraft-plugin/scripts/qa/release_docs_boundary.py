#!/usr/bin/env python3
"""隔离包只提供新文档证明时，即使结构与OpenSpec通过也不得提升运行能力。"""
import argparse,hashlib,json,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--python',default='python3');a=p.parse_args();output=a.output.resolve();output.mkdir(parents=True,exist_ok=False);sandbox=output/'package';sandbox.mkdir()
 names=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT).decode().split('\0')
 for name in filter(None,names):
  source=ROOT/name
  if source.is_symlink():raise ValueError('linked_package_input')
  if not source.is_file():continue
  target=sandbox/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
 static='docs/evidence/documentation-only-release.json';target=sandbox/static;target.write_text(json.dumps({'schema':'vectorcraft-documentation-only/v1','result':'PASS','scope':'OpenSpec and documentation validation only;no new runtime or host claim'})+'\n')
 b=json.loads((sandbox/'docs/release-evidence.json').read_text());b['host']=static;b['technical']=static;b['fingerprints'][static]=hashlib.sha256(target.read_bytes()).hexdigest();(sandbox/'docs/release-evidence.json').write_text(json.dumps(b))
 records=[]
 for name,argv,expected in [('docs',[a.python,'-I','-B','scripts/validate_docs.py'],0),('openspec',['openspec','validate','establish-v1-plugin','--strict','--no-interactive'],0),('gate',[a.python,'-I','-B','scripts/release_gate.py','--require','development'],1)]:
  r=subprocess.run(argv,cwd=sandbox,capture_output=True,text=True,timeout=60);(output/(name+'.log.txt')).write_text((r.stdout+'\n'+r.stderr).replace(str(sandbox),'QA_PACKAGE').replace(str(ROOT),'QA_PLUGIN'));records.append({'check':name,'exitCode':r.returncode,'expectedExitCode':expected})
  if r.returncode!=expected:raise ValueError('unexpected_docs_only_boundary')
 gate=json.loads((output/'gate.log.txt').read_text());assert gate['publishable']=={'development':False,'marketplace':False}
 proof={'result':'PASS','driverSha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'gateCodeSha256':hashlib.sha256((sandbox/'scripts/release_gate.py').read_bytes()).hexdigest(),'records':records,'gate':gate,'scope':'tracked package copy retains prior bounded evidence;selected new attestation has actual docs/OpenSpec only;no new runtime or host promotion','priorEvidenceRetained':True,'normalWorkspacePreserved':True}
 (output/'proof.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps({'result':'PASS','checks':records,'development':False,'marketplace':False}))
if __name__=='__main__':main()
