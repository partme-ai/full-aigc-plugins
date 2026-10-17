"""重新签摘要也不能将未验、损坏、高分覆盖或缺失停止证据变成完成。"""
import contextlib,hashlib,importlib.util,io,json,shutil,tempfile,unittest
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

REPORT='docs/evidence/vectorcraft-quality-fixed61-20261009.json'
class QualityEvidenceTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.report=json.loads((ROOT/REPORT).read_text())
  names=set(self.report['fingerprints'])|{REPORT,'docs/evidence-index.json'}
  for entry in json.loads((ROOT/'docs/evidence-index.json').read_text())['entries']:
   if entry['path']==REPORT:names.update(entry['dependencies'])
  for name in names:
   p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(name),p)
  spec=importlib.util.spec_from_file_location('quality_verifier',ROOT/'scripts/verify_quality_evidence.py');self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m);self.m.ROOT=self.root
 def rewrite(self,name,value):
  p=self.root/name;p.write_text(json.dumps(value));self.report['fingerprints'][name]=self.m.sha(p);(self.root/REPORT).write_text(json.dumps(self.report))
 def quality(self):return json.loads((self.root/self.report['quality']).read_text())
 def row(self,q,name):return next(x for x in q['records'] if x['case']==name)
 def verify(self):
  with contextlib.redirect_stdout(io.StringIO()):self.m.main()
 def test_actual_fixed_evidence_passes(self):self.verify()
 def test_missing_scenario_refused(self):
  name=self.report['scenarioMatrix'];r=json.loads((self.root/name).read_text());r['entries'].pop();self.rewrite(name,r)
  with self.assertRaisesRegex(ValueError,'scenario'):self.verify()
 def test_forged_installed_skill_refused(self):
  name=self.report['host'];r=json.loads((self.root/name).read_text());r['skills'][0]['sha256']='0'*64;self.rewrite(name,r)
  with self.assertRaisesRegex(ValueError,'installed'):self.verify()
 def test_high_score_cannot_replace_blocked_acceptance(self):
  q=self.quality();self.row(q,'undecodable-png-maximal-qa-score')['response']['acceptanceStatus']='accepted';self.rewrite(self.report['quality'],q)
  with self.assertRaisesRegex(ValueError,'failure_override'):self.verify()
 def test_not_run_cannot_be_pass(self):
  q=self.quality();self.row(q,'real-decoder-unavailable')['request']['input']['technicalStatus']='PASS';self.rewrite(self.report['quality'],q)
  with self.assertRaisesRegex(ValueError,'checked_identity'):self.verify()
 def test_decoder_cannot_claim_engineering_pass(self):
  q=self.quality();self.row(q,'healthy-persistent-decode')['request']['input']['technicalEvidence']['engineeringStatus']='PASS';self.rewrite(self.report['quality'],q)
  with self.assertRaisesRegex(ValueError,'claim_escalation'):self.verify()
 def test_missing_checker_dependency_refused(self):
  q=self.quality();self.row(q,'healthy-persistent-decode')['request']['input']['technicalEvidence']['checkerFiles'].pop('skills/vectorcraft-use/scripts/exchange_loss.py');self.rewrite(self.report['quality'],q)
  with self.assertRaisesRegex(ValueError,'checked_identity'):self.verify()
 def test_missing_decode_refused(self):
  q=self.quality();self.row(q,'healthy-persistent-decode')['request']['input']['technicalEvidence']['outputs'].pop();self.rewrite(self.report['quality'],q)
  with self.assertRaisesRegex(ValueError,'output_binding'):self.verify()
 def test_budget_must_precede_decoder(self):
  q=self.quality();self.row(q,'timeout-owned-group-and-restart')['beforeDecoder']['budgetAttempts']=0;self.rewrite(self.report['quality'],q)
  with self.assertRaisesRegex(ValueError,'replay_budget'):self.verify()
 def test_crashed_owned_group_stop_required(self):
  q=self.quality();self.row(q,'coordinator-sigkill-unknown-no-replay')['ownedGroupStopped']=False;self.rewrite(self.report['quality'],q)
  with self.assertRaisesRegex(ValueError,'unknown_stop'):self.verify()
 def test_missing_corruption_boundary_refused(self):
  q=self.quality();q['records']=[x for x in q['records'] if x['case']!='undecodable-pdf-maximal-qa-score'];self.rewrite(self.report['quality'],q)
  with self.assertRaisesRegex(ValueError,'boundary_coverage'):self.verify()
 def test_stale_candidate_refusal_required(self):
  q=self.quality();self.row(q,'stale-candidate')['refusal']['error']='accepted';self.rewrite(self.report['quality'],q)
  with self.assertRaisesRegex(ValueError,'stale_refusal'):self.verify()
if __name__=='__main__':unittest.main()
