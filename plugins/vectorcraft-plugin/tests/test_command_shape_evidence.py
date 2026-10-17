"""固定形状报告必须核验真实几何、局部修订及窗口摘要。"""
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

REPORT='docs/evidence/vectorcraft-command-shape-fixed64-20261009.json'
class ShapeEvidenceTests(unittest.TestCase):
 def setUp(self):
  self.assertTrue((ROOT/REPORT).is_file(),'shape_fixed_evidence_missing');self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  for name in (REPORT,'docs/current-identity.json','docs/evidence/vectorcraft-public-tag64-install-20261009.json','skills/vectorcraft-use/references/command-coverage.json','scripts/qa/command_family_window.py','scripts/qa/command_render.py','scripts/qa/command_shape_render.py','scripts/qa/command_paint.py','scripts/qa/command_shape.py'):
   p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(name),p)
  spec=importlib.util.spec_from_file_location('shape_evidence',ROOT/'scripts/verify_command_families.py');self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
 def change(self,command,mutate,round=1):
  p=self.root/REPORT;r=json.loads(p.read_text());s=next(c['stages'][round-1] for c in r['cases'] if c['command']=='shape.'+command);mutate(s);p.write_text(json.dumps(r))
 def validate(self):return self.m.validate_family(self.root,'shape',REPORT)
 def test_all_ten_commands_with_actual_windows(self):self.assertEqual(len(self.validate()),10)
 def test_return_id_cannot_point_to_control(self):
  self.change('rectangle',lambda s:s['returned'].update(id=2))
  with self.assertRaisesRegex(ValueError,'shape_return_id'):self.validate()
 def test_wrong_anchor_geometry_rejected(self):
  def mutate(s):s['after']['layers'][0]['kind']['children'][-1]['kind']['path']['subpaths'][0]['anchors'][0]['p'][0]+=1;s['reopened']=copy.deepcopy(s['after'])
  self.change('ellipse',mutate)
  with self.assertRaisesRegex(ValueError,'shape_path_geometry'):self.validate()
 def test_wrong_live_polygon_sides_rejected(self):
  def mutate(s):s['after']['layers'][0]['kind']['children'][-1]['kind']['live']['sides']=99;s['reopened']=copy.deepcopy(s['after'])
  self.change('polygon',mutate)
  with self.assertRaisesRegex(ValueError,'shape_live_parameters'):self.validate()
 def test_flare_gradient_stop_rejected(self):
  def mutate(s):s['after']['layers'][0]['kind']['children'][-1]['kind']['children'][0]['appearance']['items'][0]['paint']['gradient']['stops'][0]['opacity']=.9;s['reopened']=copy.deepcopy(s['after'])
  self.change('flare',mutate)
  with self.assertRaisesRegex(ValueError,'shape_flare_stops'):self.validate()
 def test_grid_line_order_and_positions_rejected(self):
  def mutate(s):s['after']['layers'][0]['kind']['children'][-1]['kind']['children'].reverse();s['reopened']=copy.deepcopy(s['after'])
  self.change('rectangularGrid',mutate)
  with self.assertRaisesRegex(ValueError,'shape_path_geometry'):self.validate()
 def test_control_text_preserved(self):
  def mutate(s):s['after']['layers'][0]['kind']['children'][1]['kind']['runs'][0]['text']='BAD';s['reopened']=copy.deepcopy(s['after'])
  self.change('line',mutate)
  with self.assertRaisesRegex(ValueError,'shape_control'):self.validate()
 def test_local_revision_not_a_noop(self):
  def mutate(s):
   id=s['fixture']['revisionID']
   for model in ('before','after','reopened'):
    target=next(x for x in s[model]['layers'][0]['kind']['children'] if x['id']==id);target.pop('opacity',None)
  self.change('star',mutate,2)
  with self.assertRaisesRegex(ValueError,'shape_local_revision'):self.validate()
 def test_saved_native_geometry_loss_rejected(self):
  self.change('spiral',lambda s:s['reopened']['layers'][0]['kind']['children'].pop())
  with self.assertRaisesRegex(ValueError,'shape_reopen'):self.validate()
 def test_window_cannot_be_artboard_capture(self):
  self.change('arc',lambda s:s['window'].update(width=128,height=96))
  with self.assertRaisesRegex(ValueError,'shape_window_capture'):self.validate()
 def test_capture_retries_are_bounded_reads(self):
  self.change('arc',lambda s:s['window'].update(readAttempts=[{'attempt':1,'status':'edit-replayed'},{'attempt':2,'status':'PASS'}]))
  with self.assertRaisesRegex(ValueError,'shape_window_read_attempts'):self.validate()
 def test_render_window_hash_must_bind_actual_capture(self):
  p=self.root/REPORT;r=json.loads(p.read_text());r['renderChanges']['cases'][0]['comparisons'][2]['firstSha256']='0'*64;p.write_text(json.dumps(r))
  with self.assertRaisesRegex(ValueError,'shape_render_binding'):self.validate()
 def test_window_scale_normalization_is_explicit(self):
  p=self.root/REPORT;r=json.loads(p.read_text());r['renderChanges']['cases'][0]['comparisons'][2]['normalization']='unknown';p.write_text(json.dumps(r))
  with self.assertRaisesRegex(ValueError,'shape_window_normalization'):self.validate()
 def test_zero_pixel_marker_rejected(self):
  p=self.root/REPORT;r=json.loads(p.read_text());r['renderChanges']['cases'][0]['comparisons'][0]['changedPixels']=0;p.write_text(json.dumps(r))
  with self.assertRaisesRegex(ValueError,'shape_render_pixels'):self.validate()
