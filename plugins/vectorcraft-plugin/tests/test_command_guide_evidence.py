"""辅助线原生证据拒绝坐标、工程和交付篡改。"""
import copy,importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
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

REPORT='docs/evidence/vectorcraft-command-guide-fixed64-20261009.json'
class GuideEvidenceTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  for name in (REPORT,'docs/current-identity.json','docs/evidence/vectorcraft-public-tag64-install-20261009.json','skills/vectorcraft-use/references/command-coverage.json',*[f'scripts/qa/{n}.py' for n in ('command_family_window_diagnostic','command_family_guide','command_guide','command_guide_render','command_layer_render','command_shape','command_paint')]):
   p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(name),p)
  s=importlib.util.spec_from_file_location('guide_evidence',ROOT/'scripts/verify_command_families.py');self.m=importlib.util.module_from_spec(s);s.loader.exec_module(self.m)
 def change(self,fn):
  p=self.root/REPORT;r=json.loads(p.read_text());fn(r);p.write_text(json.dumps(r))
 def validate(self):return self.m.validate_family(self.root,'guide',REPORT)
 def stage(self,r,cmd,round=1):return next(c['stages'][round-1] for c in r['cases'] if c['command']=='guide.'+cmd)
 def test_complete_family(self):self.assertEqual(self.validate(),['guide.add','guide.remove','guide.move'])
 def test_add_return_index(self):
  self.change(lambda r:self.stage(r,'add')['returned'].update(index=0))
  with self.assertRaisesRegex(ValueError,'guide_return'):self.validate()
 def test_guide_position(self):
  def mutate(r):
   s=self.stage(r,'move');s['after']['guides'][0]['pos']=999;s['reopened']=copy.deepcopy(s['after'])
  self.change(mutate)
  with self.assertRaisesRegex(ValueError,'guide_tree'):self.validate()
 def test_control_text(self):
  self.change(lambda r:self.stage(r,'add')['after']['layers'][0]['kind']['children'][1]['kind']['runs'][0].update(text='bad'))
  with self.assertRaisesRegex(ValueError,'guide_tree'):self.validate()
 def test_reopened_guides(self):
  self.change(lambda r:self.stage(r,'move')['reopened']['guides'].pop())
  with self.assertRaisesRegex(ValueError,'guide_reopen'):self.validate()
 def test_local_revision(self):
  self.change(lambda r:self.stage(r,'remove',2)['fixture'].update(revisionName='bad'))
  with self.assertRaisesRegex(ValueError,'guide_local_revision'):self.validate()
 def test_window_identity(self):
  self.change(lambda r:r['renderChanges']['guideLineChecks'][0].update(windowSha256='0'*64))
  with self.assertRaisesRegex(ValueError,'guide_pixels_binding'):self.validate()
 def test_window_coordinate(self):
  self.change(lambda r:r['renderChanges']['guideLineChecks'][0].update(coordinate=0))
  with self.assertRaisesRegex(ValueError,'guide_pixels_binding'):self.validate()
 def test_missing_present_line(self):
  self.change(lambda r:r['renderChanges']['guideLineChecks'][0].update(cyanSamples=0))
  with self.assertRaisesRegex(ValueError,'guide_pixels_line'):self.validate()
 def test_removed_line_is_absent(self):
  def mutate(r):
   row=next(x for x in r['renderChanges']['guideLineChecks'] if x['expectation']=='absent');row['cyanSamples']=row['totalSamples']
  self.change(mutate)
  with self.assertRaisesRegex(ValueError,'guide_pixels_line'):self.validate()
 def test_sample_length(self):
  self.change(lambda r:r['renderChanges']['guideLineChecks'][0].update(totalSamples=1))
  with self.assertRaisesRegex(ValueError,'guide_pixels_samples'):self.validate()
 def test_canvas_artwork_unchanged(self):
  self.change(lambda r:r['renderChanges']['cases'][0]['comparisons'][0].update(changedPixels=1))
  with self.assertRaisesRegex(ValueError,'layer_render_pixels'):self.validate()
 def test_window_is_real_window(self):
  self.change(lambda r:self.stage(r,'add')['window'].update(window=False))
  with self.assertRaisesRegex(ValueError,'guide_window_capture'):self.validate()

 def test_locked_move_context_is_disabled(self):
  self.change(lambda r:self.stage(r,'move')['contextProbe']['locked'][2].update(enabled=True))
  with self.assertRaisesRegex(ValueError,'guide_lock_context'):self.validate()
 def test_lock_probe_preserves_document(self):
  self.change(lambda r:self.stage(r,'remove')['contextProbe']['after']['guides'].pop())
  with self.assertRaisesRegex(ValueError,'guide_lock_preservation'):self.validate()

 def test_capture_view_matches_ready_view(self):
  self.change(lambda r:self.stage(r,'move')['uiAfterCapture']['view'].update(zoom=1))
  with self.assertRaisesRegex(ValueError,'guide_ui_capture_drift'):self.validate()
 def test_unfitted_ui_cannot_be_used(self):
  self.change(lambda r:self.stage(r,'add')['ui']['view'].update(fitted=False))
  with self.assertRaisesRegex(ValueError,'guide_ui_capture_drift'):self.validate()
 def test_ui_read_attempts_are_bounded(self):
  self.change(lambda r:self.stage(r,'remove').update(uiReadAttempts=[]))
  with self.assertRaisesRegex(ValueError,'guide_ui_read_attempts'):self.validate()
