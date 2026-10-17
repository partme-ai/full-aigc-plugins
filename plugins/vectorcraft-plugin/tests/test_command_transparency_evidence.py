"""实际固定安装证据：蒙版拓扑、选项、临时层及渲染不能由通过标记代替。"""
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

REPORT='docs/evidence/vectorcraft-command-transparency-fixed64-20261009.json'
class TransparencyEvidenceTests(unittest.TestCase):
 def setUp(self):
  self.assertTrue((ROOT/REPORT).is_file(),'transparency_fixed_evidence_missing');self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  for name in (REPORT,'docs/current-identity.json','docs/evidence/vectorcraft-public-tag64-install-20261009.json','skills/vectorcraft-use/references/command-coverage.json','scripts/qa/command_family.py','scripts/qa/command_render.py','scripts/qa/command_transparency_render.py','scripts/qa/command_paint.py','scripts/qa/command_transparency.py'):
   p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(name),p)
  spec=importlib.util.spec_from_file_location('transparency_evidence',ROOT/'scripts/verify_command_families.py');self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
 def change(self,command,mutate):
  p=self.root/REPORT;r=json.loads(p.read_text());s=next(c['stages'][0] for c in r['cases'] if c['command']=='transparency.'+command);mutate(s);p.write_text(json.dumps(r))
 def validate(self):return self.m.validate_family(self.root,'transparency',REPORT)
 def test_all_seventeen_commands_two_rounds(self):self.assertEqual(len(self.validate()),17)
 def test_flag_noop_is_rejected(self):
  def mutate(s):s['after']=copy.deepcopy(s['before']);s['reopened']=copy.deepcopy(s['after'])
  self.change('disableOpacityMask',mutate)
  with self.assertRaisesRegex(ValueError,'transparency_native_semantics'):self.validate()
 def test_released_art_geometry_must_survive(self):
  def mutate(s):s['after']['layers'][0]['kind']['children'][1]['kind']['path']['subpaths'][0]['anchors'][0]['p'][0]+=1;s['reopened']=copy.deepcopy(s['after'])
  self.change('releaseOpacityMask',mutate)
  with self.assertRaisesRegex(ValueError,'transparency_native_semantics'):self.validate()
 def test_mask_creation_cannot_keep_top_art_in_layer(self):
  def mutate(s):s['after']['layers'][0]['kind']['children'].append(copy.deepcopy(s['before']['layers'][0]['kind']['children'][-1]));s['reopened']=copy.deepcopy(s['after'])
  self.change('makeOpacityMask',mutate)
  with self.assertRaisesRegex(ValueError,'transparency_native_semantics'):self.validate()
 def test_edit_layer_geometry_is_checked(self):
  def mutate(s):s['after']['layers'][-1]['kind']['children'][0]['kind']['path']['subpaths'][0]['anchors'][0]['p'][0]+=1
  self.change('editOpacityMask',mutate)
  with self.assertRaisesRegex(ValueError,'transparency_edit_layer'):self.validate()
 def test_edit_layer_must_not_be_serialized(self):
  def mutate(s):s['reopened']['layers'].append(copy.deepcopy(s['after']['layers'][-1]))
  self.change('editOpacityMask',mutate)
  with self.assertRaisesRegex(ValueError,'transparency_reopen'):self.validate()
 def test_default_probe_cannot_be_unbound(self):
  def mutate(s):s['observed']['defaultProbe']['mask']['clip']=False
  self.change('toggleNewMasksClipping',mutate)
  with self.assertRaisesRegex(ValueError,'transparency_default_model_binding'):self.validate()
 def test_failed_return_to_original_cannot_pass(self):
  self.change('toggleNewMasksClipping',lambda s:s['observed']['defaultProbe'].update(restoredOriginal=False))
  with self.assertRaisesRegex(ValueError,'transparency_default_probe'):self.validate()
 def test_view_off_still_edits_mask(self):
  p=self.root/REPORT;r=json.loads(p.read_text());s=next(c for c in r['cases'] if c['command']=='transparency.viewOpacityMask')['stages'][1];s['observed']['info']['editingMask']=None;p.write_text(json.dumps(r))
  with self.assertRaisesRegex(ValueError,'transparency_info'):self.validate()
 def test_render_zero_pixels_is_rejected(self):
  p=self.root/REPORT;r=json.loads(p.read_text());r['renderChanges']['cases'][0]['comparisons'][0]['changedPixels']=0;p.write_text(json.dumps(r))
  with self.assertRaisesRegex(ValueError,'transparency_render_pixels'):self.validate()
 def test_preferences_restart_cannot_be_promoted(self):
  p=self.root/REPORT;r=json.loads(p.read_text());r['preferenceRestartAcceptance']='PASS';p.write_text(json.dumps(r))
  with self.assertRaisesRegex(ValueError,'transparency_preference_scope'):self.validate()
