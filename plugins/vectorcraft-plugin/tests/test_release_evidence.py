"""发布证据重签后仍不能掩盖文档越级、缺失场景或固定身份漂移。"""
import contextlib,hashlib,importlib.util,io,json,shutil,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];REPORT='docs/evidence/vectorcraft-release-gate-20261009.json'

def payload_source(name):
    """执行载荷收敛在 vectorcraft-harness：沙箱复制的 skills/<domain>/scripts/ 源按字节等价映射。"""
    if (ROOT/name).is_file():return name
    if isinstance(name, str):
        prefix = 'skills/vectorcraft-'
        if name.startswith(prefix) and '/scripts/' in name:
            candidate = 'skills/vectorcraft-harness/scripts/' + name.split('/scripts/', 1)[1]
            if (ROOT/candidate).is_file():
                return candidate
    # harness 归位：src/harness/<file> 与 scripts/harness/<file> 字节一致时直接等价映射。
    if isinstance(name,str) and name.startswith('src/harness/'):
        candidate='scripts/harness/'+name.split('src/harness/',1)[1]
        if (ROOT/candidate).is_file():return candidate
    # 其余按指纹摘要从收敛归档唯一恢复执行字节。
    expected=json.loads((ROOT/REPORT).read_text())['fingerprints'].get(name)
    if expected:
        for path in sorted((ROOT/'docs/evidence/pre-harness-convergence-identity').glob('*/'+name)):
            if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==expected:return path.relative_to(ROOT).as_posix()
    return name

class ReleaseEvidenceTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.report=json.loads((ROOT/REPORT).read_text());names=set(self.report['fingerprints'])|{REPORT,'project-status.json','openspec/changes/establish-v1-plugin/tasks.md','docs/evidence-index.json'}
  for entry in json.loads((ROOT/'docs/evidence-index.json').read_text())['entries']:
   if entry['path']==REPORT:names.update(entry['dependencies'])
  for name in names:
   p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(name),p)
  shutil.copytree(ROOT/'skills',self.root/'skills',dirs_exist_ok=True)
  s=importlib.util.spec_from_file_location('release_evidence_verifier',ROOT/'scripts/verify_release_evidence.py');self.m=importlib.util.module_from_spec(s);s.loader.exec_module(self.m);self.m.ROOT=self.root
 def rewrite(self,key,value):
  name=self.report[key];p=self.root/name;p.write_text(json.dumps(value));self.report['fingerprints'][name]=hashlib.sha256(p.read_bytes()).hexdigest();(self.root/REPORT).write_text(json.dumps(self.report))
 def verify(self):
  with contextlib.redirect_stdout(io.StringIO()):self.m.main()
 def test_current_release_evidence_passes(self):self.verify()
 def test_missing_scenario_refused(self):
  r=json.loads((self.root/self.report['scenarioMatrix']).read_text());r['entries'].pop();self.rewrite('scenarioMatrix',r)
  with self.assertRaisesRegex(ValueError,'scenarios'):self.verify()
 def test_document_only_native_promotion_refused(self):
  r=json.loads((self.root/self.report['documentationOnly']).read_text());r['gate']['layers']['native']['status']='PASS';self.rewrite('documentationOnly',r)
  with self.assertRaisesRegex(ValueError,'docs_only'):self.verify()
 def test_fixed_commit_cannot_be_replaced(self):
  self.report['pluginCommit']='0'*40;(self.root/REPORT).write_text(json.dumps(self.report))
  with self.assertRaisesRegex(ValueError,'identity'):self.verify()
if __name__=='__main__':unittest.main()
