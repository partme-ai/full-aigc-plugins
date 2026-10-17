"""固定魔棒原生证据拒绝返回、会话、工程和面板像素篡改。"""
import copy,importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
class WandEvidenceTests(unittest.TestCase):
 def setUp(self):
  self.report=json.loads((ROOT/'docs/evidence/vectorcraft-command-magicWand-fixed64-20261009.json').read_text());self.m=load('wand_evidence',ROOT/'scripts/qa/command_magicWand.py');self.pixels=load('wand_pixels',ROOT/'scripts/qa/command_magicWand_render.py')
 def stage(self,number=1):return self.report['cases'][0]['stages'][number-1]
 def validate(self):
  for c in self.report['cases']:
   for s in c['stages']:self.m.validate_transition(c['command'],s)
  self.pixels.validate_checks(self.report['cases'],self.report['renderChanges']['checkboxChecks'])
 def test_all_native_semantics_and_pixels(self):self.validate()
 def test_full_fixed_identity_verifier(self):
  v=load('wand_family_verifier',ROOT/'scripts/verify_command_families.py');self.assertEqual(v.validate_family(ROOT,'magicWand','docs/evidence/vectorcraft-command-magicWand-fixed64-20261009.json'),self.m.COMMANDS)
 def test_clamped_return(self):
  self.stage()['returned']['weightTolerance']=1200
  with self.assertRaisesRegex(ValueError,'wand_return'):self.validate()
 def test_tool_switch_preservation(self):
  self.stage()['observed']['afterToolSwitch']['fillColor']=True
  with self.assertRaisesRegex(ValueError,'wand_session_preservation'):self.validate()
 def test_reopen_session_preservation(self):
  self.stage()['observed']['afterNativeReopen']['strokeColor']=False
  with self.assertRaisesRegex(ValueError,'wand_session_preservation'):self.validate()
 def test_document_cannot_change(self):
  self.m.shape.find(self.stage()['after'],2)['name']='bad'
  with self.assertRaisesRegex(ValueError,'wand_document_preservation'):self.validate()
 def test_reopened_document_cannot_change(self):
  self.m.shape.find(self.stage()['reopened'],3)['kind']['runs'][0]['text']='bad'
  with self.assertRaisesRegex(ValueError,'wand_document_preservation'):self.validate()
 def test_control_revision_is_bound(self):
  self.stage(2)['fixture']['revisionName']='bad'
  with self.assertRaisesRegex(ValueError,'wand_local_revision'):self.validate()
 def test_magic_wand_panel_required(self):
  self.stage()['ui']['ui']['open_panel']='attributes'
  with self.assertRaisesRegex(ValueError,'wand_panel_context'):self.validate()
 def test_checkbox_capture_digest(self):
  self.report['renderChanges']['checkboxChecks'][0]['windowSha256']='0'*64
  with self.assertRaisesRegex(ValueError,'wand_pixels_binding'):self.validate()
 def test_checked_pixel_count(self):
  self.report['renderChanges']['checkboxChecks'][1]['bluePixels']=0
  with self.assertRaisesRegex(ValueError,'wand_pixels_state'):self.validate()
 def test_unchecked_pixel_count(self):
  self.report['renderChanges']['checkboxChecks'][0]['bluePixels']=111
  with self.assertRaisesRegex(ValueError,'wand_pixels_state'):self.validate()
 def test_missing_checkbox(self):
  self.report['renderChanges']['checkboxChecks'].pop()
  with self.assertRaisesRegex(ValueError,'wand_pixels_coverage'):self.validate()
 def test_checkbox_value_uses_independent_settings(self):
  self.report['renderChanges']['checkboxChecks'][0]['value']=True
  with self.assertRaisesRegex(ValueError,'wand_pixels_binding'):self.validate()
if __name__=='__main__':unittest.main()
