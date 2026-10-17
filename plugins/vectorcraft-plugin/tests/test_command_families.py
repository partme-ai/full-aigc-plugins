"""命令族汇总保留完整目录、排除重复计数与伪造原生成功。"""
import importlib.util
from pathlib import Path
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

class CommandFamilyMatrixTests(unittest.TestCase):
 def setUp(self):
  p=ROOT/'scripts/verify_command_families.py';self.assertTrue(p.is_file(),'command_family_matrix_missing')
  spec=importlib.util.spec_from_file_location('family_verify',p);self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
 def test_disjoint_families_accumulate(self):self.assertEqual(self.m.merge_ids({'paint.setFill'},['swatch.new']),{'paint.setFill','swatch.new'})
 def test_repeated_family_cannot_inflate_coverage(self):
  with self.assertRaisesRegex(ValueError,'command_family_overlap'):self.m.merge_ids({'paint.setFill'},['paint.setFill'])
 def test_duplicate_cases_cannot_inflate_coverage(self):
  with self.assertRaisesRegex(ValueError,'command_family_duplicate'):self.m.merge_ids(set(),['swatch.new','swatch.new'])
 def fixed_fixture(self):
  import shutil,tempfile
  self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);root=Path(self.temp.name)
  for name in ('docs/evidence/vectorcraft-command-swatch-fixed64-20261009.json','docs/current-identity.json','docs/evidence/vectorcraft-public-tag64-install-20261009.json','skills/vectorcraft-use/references/command-coverage.json','scripts/qa/command_paint.py','scripts/qa/command_family.py','scripts/qa/command_swatch.py'):
   target=root/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(name),target)
  return root
 def mutate(self,root,change):
  import json
  p=root/'docs/evidence/vectorcraft-command-swatch-fixed64-20261009.json';report=json.loads(p.read_text());change(report);p.write_text(json.dumps(report))
 def validate(self,root):return self.m.validate_family(root,'swatch','docs/evidence/vectorcraft-command-swatch-fixed64-20261009.json')
 def test_all_current_swatch_cases_have_real_semantics(self):self.assertEqual(len(self.validate(self.fixed_fixture())),22)
 def test_installed_skill_drift_is_rejected(self):
  root=self.fixed_fixture();self.mutate(root,lambda r:r['installedSkillsAfter'].update({'vectorcraft-use':'0'*64}))
  with self.assertRaisesRegex(ValueError,'family_installed_identity'):self.validate(root)
 def test_missing_command_does_not_pass_family(self):
  root=self.fixed_fixture();self.mutate(root,lambda r:r['cases'].pop())
  with self.assertRaisesRegex(ValueError,'family_command_coverage'):self.validate(root)
 def test_relink_success_flag_cannot_hide_wrong_native_color(self):
  import copy
  root=self.fixed_fixture()
  def change(r):
   stage=next(c for c in r['cases'] if c['command']=='swatch.edit')['stages'][0]
   self.m.load('paint_test',root/'scripts/qa/command_paint.py').paint(stage['after'])['color']['r']=0
   stage['reopened']=copy.deepcopy(stage['after'])
  self.mutate(root,change)
  with self.assertRaisesRegex(ValueError,'swatch_color'):self.validate(root)

 def test_swatch_edit_cannot_change_unrequested_stroke(self):
  import copy
  root=self.fixed_fixture()
  def change(r):
   stage=next(c for c in r['cases'] if c['command']=='swatch.edit')['stages'][0]
   objects=self.m.load('protected_stroke_test',root/'scripts/qa/command_paint.py').objects(stage['after'])
   next(item for item in objects[2]['appearance']['items'] if item['kind']=='stroke')['width']=99
   stage['reopened']=copy.deepcopy(stage['after'])
  self.mutate(root,change)
  with self.assertRaisesRegex(ValueError,'family_protected_appearance'):self.validate(root)
