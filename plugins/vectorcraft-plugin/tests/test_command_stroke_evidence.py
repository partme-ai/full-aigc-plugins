"""固定描边证据需拒绝漏命令、单位错误及虚假的轮廓记录。"""
import copy,importlib.util,json,shutil,tempfile
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

REPORT='docs/evidence/vectorcraft-command-stroke-fixed64-20261009.json'
class StrokeEvidenceTests(unittest.TestCase):
 def setUp(self):
  self.assertTrue((ROOT/REPORT).is_file(),'stroke_fixed_evidence_missing')
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  for name in (REPORT,'docs/current-identity.json','docs/evidence/vectorcraft-public-tag64-install-20261009.json','skills/vectorcraft-use/references/command-coverage.json','scripts/qa/command_family.py','scripts/qa/command_render.py','scripts/qa/command_paint.py','scripts/qa/command_stroke.py'):
   p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(name),p)
  spec=importlib.util.spec_from_file_location('stroke_evidence',ROOT/'scripts/verify_command_families.py');self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
 def change(self,mutate):
  p=self.root/REPORT;r=json.loads(p.read_text());mutate(r);p.write_text(json.dumps(r))
 def validate(self):return self.m.validate_family(self.root,'stroke',REPORT)
 def test_all_ten_commands_have_two_native_rounds(self):self.assertEqual(len(self.validate()),10)
 def test_missing_command_is_rejected(self):
  self.change(lambda r:r['cases'].pop())
  with self.assertRaisesRegex(ValueError,'family_command_coverage'):self.validate()
 def test_width_point_wrong_unit_is_rejected(self):
  def mutate(r):
   stage=next(c for c in r['cases'] if c['command']=='stroke.widthPoint.set')['stages'][0]
   driver=self.m.load('stroke_unit_test',self.root/'scripts/qa/command_stroke.py');point=driver.stroke(stage['after'])['profile']['points'][stage['returned']['index']];point[1]/=2;point[2]/=2;stage['reopened']=copy.deepcopy(stage['after'])
  self.change(mutate)
  with self.assertRaisesRegex(ValueError,'stroke_native_semantics'):self.validate()
 def test_fake_saved_profile_points_are_rejected(self):
  def mutate(r):
   stage=next(c for c in r['cases'] if c['command']=='stroke.widthProfile.add')['stages'][0]
   next(x for x in stage['observed']['profilesAfter']['profiles'] if not x['builtIn'])['points'][0][1]=99
  self.change(mutate)
  with self.assertRaisesRegex(ValueError,'stroke_profile_add'):self.validate()
 def test_fake_positive_render_marker_with_zero_pixels_is_rejected(self):
  self.change(lambda r:r['renderChanges']['cases'][0]['comparisons'][0].update(changedPixels=0))
  with self.assertRaisesRegex(ValueError,'stroke_render_pixels'):self.validate()
 def test_render_measurement_must_bind_actual_stage_image(self):
  self.change(lambda r:r['renderChanges']['cases'][0]['comparisons'][0].update(firstSha256='0'*64))
  with self.assertRaisesRegex(ValueError,'stroke_render_binding'):self.validate()
 def test_restart_not_run_cannot_be_promoted_by_flag(self):
  self.change(lambda r:r.update(preferenceRestartAcceptance='PASS'))
  with self.assertRaisesRegex(ValueError,'stroke_preference_scope'):self.validate()
