"""重签摘要不能掩盖缺失场景、错误替代、不可编辑原源或伪造安装。"""
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

REPORT='docs/evidence/vectorcraft-native-exchange-fixed59-20261009.json'
class NativeExchangeEvidenceTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.report=json.loads((ROOT/REPORT).read_text())
  for n in set(self.report['fingerprints'])|{REPORT}:
   p=self.root/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(n),p)
  spec=importlib.util.spec_from_file_location('native_exchange_verifier',ROOT/'scripts/verify_native_exchange_evidence.py');self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m);self.m.ROOT=self.root
  p=self.root/'docs/evidence-index.json';p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/'docs/evidence-index.json',p)
  for entry in json.loads(p.read_text())['entries']:
   for name in entry['dependencies']:
    p=self.root/name
    if not p.exists():p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(name),p)
 def write(self,n,r):
  p=self.root/n;p.write_text(json.dumps(r));self.report['fingerprints'][n]=self.m.sha(p);(self.root/REPORT).write_text(json.dumps(self.report))
 def verify(self):
  with contextlib.redirect_stdout(io.StringIO()):self.m.main()
 def test_real_fixed_evidence_passes(self):self.verify()
 def test_missing_scene_refused(self):
  n=self.report['scenarioMatrix'];r=json.loads((self.root/n).read_text());r['entries'].pop();self.write(n,r)
  with self.assertRaisesRegex(ValueError,'scenario'):self.verify()
 def test_false_font_fidelity_refused(self):
  n=self.report['native'];r=json.loads((self.root/n).read_text());next(x for x in r['lossReport']['outputs'][1]['changes'] if x['code']=='font-portability')['status']='observed';self.write(n,r)
  with self.assertRaisesRegex(ValueError,'loss'):self.verify()
 def test_missing_native_substitute_refusal_refused(self):
  n=self.report['native'];r=json.loads((self.root/n).read_text());r['refusals']=[x for x in r['refusals'] if x['case']!='native-substitute-pdf'];self.write(n,r)
  with self.assertRaisesRegex(ValueError,'refusal'):self.verify()
 def test_forged_installed_skill_refused(self):
  n=self.report['host'];r=json.loads((self.root/n).read_text());r['skills'][0]['sha256']='0'*64;self.write(n,r)
  with self.assertRaisesRegex(ValueError,'installed'):self.verify()
 def test_changed_reopened_model_refused(self):
  n=self.report['native'];r=json.loads((self.root/n).read_text());r['independentReopens'][1]['model']['layers']=[];self.write(n,r)
  with self.assertRaisesRegex(ValueError,'native'):self.verify()
 def test_missing_decoded_export_refused(self):
  n=self.report['native'];r=json.loads((self.root/n).read_text());r['quality']['outputs'].pop();self.write(n,r)
  with self.assertRaisesRegex(ValueError,'decode'):self.verify()
if __name__=='__main__':unittest.main()
