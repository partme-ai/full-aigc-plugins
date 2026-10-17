"""重算摘要仍不能掩盖缺失场景、伪造任务、依赖或宿主身份。"""
import contextlib,importlib.util,io,json,shutil,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

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

REPORT='docs/evidence/vectorcraft-lineage-fixed58-20261009.json'
class LineageEvidenceTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.report=json.loads((ROOT/REPORT).read_text())
  for name in set(self.report['fingerprints'])|{REPORT}:
   p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(name),p)
  spec=importlib.util.spec_from_file_location('lineage_verifier',ROOT/'scripts/verify_lineage_evidence.py');self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m);self.m.ROOT=self.root
  p=self.root/'docs/evidence-index.json';p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/'docs/evidence-index.json',p)
  for entry in json.loads(p.read_text())['entries']:
   for name in entry['dependencies']:
    p=self.root/name
    if not p.exists():p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(name),p)
 def write(self,name,value):
  p=self.root/name;p.write_text(json.dumps(value));self.report['fingerprints'][name]=self.m.sha(p);(self.root/REPORT).write_text(json.dumps(self.report))
 def verify(self):
  with contextlib.redirect_stdout(io.StringIO()):self.m.main()
 def test_actual_fixed_proof_passes(self):self.verify()
 def test_missing_scene_rejected(self):
  n=self.report['scenarioMatrix'];r=json.loads((self.root/n).read_text());r['entries'].pop();self.write(n,r)
  with self.assertRaisesRegex(ValueError,'scenario'):self.verify()
 def test_forged_host_digest_rejected(self):
  n=self.report['host'];r=json.loads((self.root/n).read_text());r['skills'][0]['sha256']='0'*64;self.write(n,r)
  with self.assertRaisesRegex(ValueError,'installed'):self.verify()
 def test_rebound_execution_task_rejected(self):
  n=self.report['native'];r=json.loads((self.root/n).read_text());r['creation']['lineage']['sourceTask']['id']='wrong-task';self.write(n,r)
  with self.assertRaisesRegex(ValueError,'lineage'):self.verify()
 def test_deleted_asset_dependency_rejected(self):
  n=self.report['native'];r=json.loads((self.root/n).read_text());r['creation']['lineage']['assets']={};self.write(n,r)
  with self.assertRaisesRegex(ValueError,'lineage'):self.verify()
 def test_missing_refusal_rejected(self):
  n=self.report['publicQuality'];r=json.loads((self.root/n).read_text());r['cases'].pop();self.write(n,r)
  with self.assertRaisesRegex(ValueError,'refusal'):self.verify()
 def test_unreopened_move_rejected(self):
  n=self.report['native'];r=json.loads((self.root/n).read_text());r['movedNativeReopened']=False;self.write(n,r)
  with self.assertRaisesRegex(ValueError,'native'):self.verify()
if __name__=='__main__':unittest.main()
