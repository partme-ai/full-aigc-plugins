"""品牌与文字验收不能凭场景名称或刷新摘要伪造通过。"""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]

def payload_source(name):
    """执行载荷收敛在 vectorcraft-harness：沙箱复制的 skills/<domain>/scripts/ 源按字节等价映射。"""
    if isinstance(name, str):
        prefix = 'skills/vectorcraft-'
        if name.startswith(prefix) and '/scripts/' in name and not (ROOT/name).is_file():
            candidate = 'skills/vectorcraft-harness/scripts/' + name.split('/scripts/', 1)[1]
            if (ROOT/candidate).is_file():
                return candidate
    return name

REPORT='docs/evidence/vectorcraft-brand-text-fixed53-20261009.json'
class BrandTextEvidenceTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name).resolve()
  self.report=json.loads((ROOT/REPORT).read_text())
  index=json.loads((ROOT/'docs/evidence-index.json').read_text())
  dependencies=next(e['dependencies'] for e in index['entries'] if e['path']==REPORT)
  for name in [REPORT,'docs/evidence-index.json',*self.report['fingerprints'],*dependencies]:
   dst=self.root/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(name),dst)
  spec=importlib.util.spec_from_file_location('brand_evidence',ROOT/'scripts/verify_brand_text_evidence.py');self.module=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.module);self.module.ROOT=self.root
 def save(self,name,data,rebind=False):
  path=self.root/name;path.write_text(json.dumps(data))
  if rebind:
   self.report['fingerprints'][name]=hashlib.sha256(path.read_bytes()).hexdigest();(self.root/REPORT).write_text(json.dumps(self.report))
 def run_check(self):
  with contextlib.redirect_stdout(io.StringIO()):self.module.main()
 def test_actual_immutable_fixed_evidence_passes(self):self.run_check()
 def test_modified_native_proof_without_binding_is_stale(self):
  name='docs/evidence/vc-dm-003/brand.json';data=json.loads((self.root/name).read_text());data['fixedInstalled']=False;self.save(name,data)
  with self.assertRaisesRegex(ValueError,'stale_brand_text_evidence'):self.run_check()
 def test_rebound_matrix_still_requires_all_scenarios(self):
  name=self.report['scenarioMatrix'];data=json.loads((self.root/name).read_text());data['entries'].pop();self.save(name,data,True)
  with self.assertRaisesRegex(ValueError,'scenario_coverage_mismatch'):self.run_check()
 def test_rebound_source_only_matrix_cannot_replace_native(self):
  name=self.report['scenarioMatrix'];data=json.loads((self.root/name).read_text())
  for c in data['entries'][0]['checks']:c['level']='source-unit'
  self.save(name,data,True)
  with self.assertRaisesRegex(ValueError,'missing_native_scenario_evidence'):self.run_check()
 def test_rebound_host_still_requires_fixed_commit(self):
  name=self.report['host'];data=json.loads((self.root/name).read_text());data['pluginCommit']='0'*40;self.save(name,data,True)
  with self.assertRaisesRegex(ValueError,'fixed_host_identity_mismatch'):self.run_check()
 def test_rebound_native_failure_cannot_pass_scenario(self):
  name='docs/evidence/vc-dm-003/outline.json';data=json.loads((self.root/name).read_text());data['cases'][1]['lossStatus']='unknown';self.save(name,data,True)
  with self.assertRaisesRegex(ValueError,'failed_scenario_check'):self.run_check()
