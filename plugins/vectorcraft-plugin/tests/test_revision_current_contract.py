"""当前安装的检查器依赖须完整绑定；发布门禁须验证所选报告而非旧报告常量。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
verifier=load('revision_current_verifier',ROOT/'scripts/verify_revision_evidence.py')
foundation=load('release_gate_fixture',ROOT/'tests/test_release_gate.py')

class CurrentCheckerContractTests(unittest.TestCase):
 def test_current_contract_captures_all_ten_source_declared_dependencies(self):
  report={'schema':'vectorcraft-revision-fixed/v2'}
  files=verifier.checker_contract(report,lambda name:ROOT/verifier.payload_name(name))
  self.assertEqual(len(files),10)
  self.assertEqual(files['scripts/harness/authorized_tree.py'],verifier.sha(ROOT/'scripts/harness/authorized_tree.py'))
 def test_legacy_schema_preserves_original_three_file_contract(self):
  self.assertEqual(len(verifier.checker_contract({'schema':'vectorcraft-revision-fixed/v1'},lambda name:ROOT/verifier.payload_name(name))),3)
 def test_unknown_schema_cannot_silently_downgrade_to_legacy(self):
  with self.assertRaisesRegex(ValueError,'revision_schema'):
   verifier.checker_contract({'schema':'vectorcraft-revision-fixed/v999'},lambda name:ROOT/name)
 def test_bundle_itself_must_be_bound_before_parsing(self):
  calls=[]
  def bound(name):
   calls.append(name);raise ValueError('unbound_checker')
  with self.assertRaisesRegex(ValueError,'unbound_checker'):
   verifier.checker_contract({'schema':'vectorcraft-revision-fixed/v2'},bound)
  self.assertEqual(calls,['src/evaluation/checker_bundle.ts'])
 def test_duplicate_or_empty_declarations_are_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'bundle.ts'
   for source in ("const paths=[];", "const paths=['a','a'];", "const paths={};"):
    p.write_text(source)
    with self.subTest(source=source),self.assertRaisesRegex(ValueError,'revision_checker_contract'):
     verifier.checker_contract({'schema':'vectorcraft-revision-fixed/v2'},lambda name:p)
 def test_release_gate_checks_selected_technical_report(self):
  fixture=foundation.ReleaseGateTests(methodName='test_original_fixed_snapshot_passes_six_layers_as_development_only')
  fixture.setUp();self.addCleanup(fixture.doCleanups)
  old=fixture.bundle['technical'];new='docs/evidence/selected-current-revision.json'
  data=json.loads((fixture.root/old).read_text());fixture.write(new,data)
  fixture.bundle['technical']=new
  (fixture.root/'docs/release-evidence.json').write_text(json.dumps(fixture.bundle))
  (fixture.root/old).unlink()
  result=fixture.assess()
  self.assertEqual(result['layers']['native']['status'],'PASS',result)
