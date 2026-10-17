"""重新计算摘要不能掩盖停止、最佳候选、作用域或桌面拒绝证据缺失。"""
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

REPORT='docs/evidence/vectorcraft-revision-limits-fixed62-20261009.json'
class RevisionLimitsEvidenceTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  self.report=json.loads((ROOT/REPORT).read_text())
  names=set(self.report['fingerprints'])|{REPORT,'docs/evidence-index.json'}
  for entry in json.loads((ROOT/'docs/evidence-index.json').read_text())['entries']:
   if entry['path']==REPORT:names.update(entry['dependencies'])
  for name in names:
   p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(name),p)
  spec=importlib.util.spec_from_file_location('revision_limits_verifier',ROOT/'scripts/verify_revision_limits_evidence.py');self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
 def case(self,key):return json.loads((self.root/self.report['cases'][key]).read_text())
 def rewrite(self,key,value):
  name=self.report['cases'][key];p=self.root/name;p.write_text(json.dumps(value));self.report['fingerprints'][name]=self.m.sha(p);(self.root/REPORT).write_text(json.dumps(self.report))
 def verify(self):
  with contextlib.redirect_stdout(io.StringIO()):self.m.verify(self.root)
 def test_actual_evidence_passes(self):self.verify()
 def test_installed_integrity_cannot_be_forged(self):
  name='docs/evidence/vc-qa-002/integrity-limits-fixed62.json';p=self.root/name;r=json.loads(p.read_text());r['digests']['vectorcraft-use']='0'*64;p.write_text(json.dumps(r));self.report['fingerprints'][name]=self.m.sha(p);(self.root/REPORT).write_text(json.dumps(self.report))
  with self.assertRaisesRegex(ValueError,'installed_integrity'):self.verify()
 def test_small_improvement_must_retain_new_best(self):
  r=self.case('small-improvement');r['best']['requestId']=r['initialRequest']['id'];self.rewrite('small-improvement',r)
  with self.assertRaisesRegex(ValueError,'best'):self.verify()
 def test_lower_score_must_retain_initial_best(self):
  r=self.case('lower-score');r['best']['requestId']=r['nextRequest']['id'];self.rewrite('lower-score',r)
  with self.assertRaisesRegex(ValueError,'best'):self.verify()
 def test_stagnation_cannot_be_active(self):
  r=self.case('small-improvement');r['cycle']['state']='active';self.rewrite('small-improvement',r)
  with self.assertRaisesRegex(ValueError,'stop'):self.verify()
 def test_pending_cannot_be_accepted(self):
  r=self.case('round-limit');r['best']['acceptanceStatus']='accepted';self.rewrite('round-limit',r)
  with self.assertRaisesRegex(ValueError,'claim'):self.verify()
 def test_authority_must_be_narrowed(self):
  r=self.case('round-limit');r['proposal']['authorization']['objects'].append(3);self.rewrite('round-limit',r)
  with self.assertRaisesRegex(ValueError,'authority'):self.verify()
 def test_gui_stale_must_not_charge_revision(self):
  r=self.case('stale-gui');r['sharedAttempts']=3;self.rewrite('stale-gui',r)
  with self.assertRaisesRegex(ValueError,'stale'):self.verify()
 def test_gui_owned_processes_must_stop(self):
  r=self.case('stale-gui');r['gui']['ownedProcessesStopped']=False;self.rewrite('stale-gui',r)
  with self.assertRaisesRegex(ValueError,'gui'):self.verify()
 def test_control_text_must_be_preserved(self):
  r=self.case('lower-score');r['revisedModel']['layers']=[];self.rewrite('lower-score',r)
  with self.assertRaisesRegex(ValueError,'control'):self.verify()
if __name__=='__main__':unittest.main()
