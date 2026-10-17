"""真实窗口证据不能用普通画布或伪造样本代替。"""
import importlib.util,json,shutil,tempfile
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

class MaskWindowTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  spec=importlib.util.spec_from_file_location('window_verify',ROOT/'scripts/verify_mask_window_evidence.py');self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
  self.report=self.m.REPORT;r=json.loads((ROOT/self.report).read_text())
  for name in {*r['fingerprints'],self.report,'docs/current-identity.json'}:
   p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(name),p)
 def mutate(self,fn):
  p=self.root/self.report;r=json.loads(p.read_text());fn(r);p.write_text(json.dumps(r))
 def test_current_two_real_windows(self):self.assertEqual(self.m.verify(self.root)['windows'],2)
 def test_colored_mask_view_is_rejected(self):
  self.mutate(lambda r:r['stages'][0]['samples'].__setitem__(0,[100,120,140]))
  with self.assertRaisesRegex(ValueError,'mask_window_not_greyscale'):self.m.verify(self.root)
 def test_gray_normal_view_is_rejected(self):
  self.mutate(lambda r:r['stages'][1]['samples'].__setitem__(0,[128,128,128]))
  with self.assertRaisesRegex(ValueError,'mask_window_not_colored'):self.m.verify(self.root)
 def test_default_artboard_dimensions_cannot_pass_as_window(self):
  self.mutate(lambda r:r['stages'][0].update(width=128,height=96))
  with self.assertRaisesRegex(ValueError,'mask_window_native_state'):self.m.verify(self.root)
 def test_view_off_must_still_edit_mask(self):
  self.mutate(lambda r:r['stages'][1]['info'].update(editingMask=None))
  with self.assertRaisesRegex(ValueError,'mask_window_native_state'):self.m.verify(self.root)
 def test_not_stopped_processes_cannot_pass(self):
  self.mutate(lambda r:r.update(allOwnedProcessesStopped=False))
  with self.assertRaisesRegex(ValueError,'mask_window_ownership'):self.m.verify(self.root)

 def test_source_project_must_bind_actual_command_stage(self):
  self.mutate(lambda r:r.update(sourceProjectSha256='0'*64))
  with self.assertRaisesRegex(ValueError,'mask_window_source_binding'):self.m.verify(self.root)
