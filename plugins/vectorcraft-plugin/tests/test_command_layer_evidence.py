"""图层固定证据不能用空树变换、伪状态或画布图替代真实窗口验收。"""
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

REPORT='docs/evidence/vectorcraft-command-layer-fixed64-20261009.json'
class LayerEvidenceTests(unittest.TestCase):
 def setUp(self):
  self.assertTrue((ROOT/REPORT).is_file(),'layer_fixed_evidence_missing');self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  for name in (REPORT,'docs/current-identity.json','docs/evidence/vectorcraft-public-tag64-install-20261009.json','skills/vectorcraft-use/references/command-coverage.json','scripts/qa/command_family_window.py','scripts/qa/command_layer_render.py','scripts/qa/command_paint.py','scripts/qa/command_shape.py','scripts/qa/command_layer.py'):
   p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(name),p)
  spec=importlib.util.spec_from_file_location('layer_evidence',ROOT/'scripts/verify_command_families.py');self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
 def change(self,command,mutate,round=1):
  p=self.root/REPORT;r=json.loads(p.read_text());s=next(c['stages'][round-1] for c in r['cases'] if c['command']=='layer.'+command);mutate(s);p.write_text(json.dumps(r))
 def validate(self):return self.m.validate_family(self.root,'layer',REPORT)
 def test_all_eleven_commands(self):self.assertEqual(len(self.validate()),11)
 def test_wrong_return_id(self):
  self.change('new',lambda s:s['returned'].update(id=2))
  with self.assertRaisesRegex(ValueError,'layer_return_id'):self.validate()
 def test_wrong_sibling_order(self):
  def mutate(s):s['after']['layers'].reverse();s['reopened']=copy.deepcopy(s['after'])
  self.change('new',mutate)
  with self.assertRaisesRegex(ValueError,'layer_tree_transition'):self.validate()
 def test_duplicate_missing_child(self):
  def mutate(s):s['after']['layers'][-1]['kind']['children'].pop();s['reopened']=copy.deepcopy(s['after'])
  self.change('duplicate',mutate)
  with self.assertRaisesRegex(ValueError,'layer_tree_transition'):self.validate()
 def test_control_text_change(self):
  def mutate(s):s['after']['layers'][0]['kind']['children'][1]['kind']['runs'][0]['text']='BAD';s['reopened']=copy.deepcopy(s['after'])
  self.change('collectInNew',mutate)
  with self.assertRaisesRegex(ValueError,'layer_tree_transition'):self.validate()
 def test_current_layer_is_real_session_state(self):
  self.change('setCurrent',lambda s:s['observed'].update(currentLayer=1))
  with self.assertRaisesRegex(ValueError,'layer_session_currentLayer'):self.validate()
 def test_hidden_locked_selection_pruned(self):
  self.change('setProps',lambda s:s['observed'].update(selection=s['fixture']['beforeInspect']['selection']))
  with self.assertRaisesRegex(ValueError,'layer_session_selection'):self.validate()
 def test_select_all_does_not_select_descendants(self):
  self.change('selectAll',lambda s:s['observed']['selection'].append(999))
  with self.assertRaisesRegex(ValueError,'layer_session_selection'):self.validate()
 def test_target_return_and_inspect_must_match(self):
  self.change('target',lambda s:s['observed'].update(target=None))
  with self.assertRaisesRegex(ValueError,'layer_session_target'):self.validate()
 def test_paste_option_must_persist(self):
  self.change('pasteRemembersLayers',lambda s:s['reopened'].pop('paste_remembers_layers',None))
  with self.assertRaisesRegex(ValueError,'layer_reopen'):self.validate()
 def test_local_revision_not_noop(self):
  def mutate(s):s['fixture']['revisionName']='wrong'
  self.change('new',mutate,2)
  with self.assertRaisesRegex(ValueError,'layer_local_revision'):self.validate()
 def test_window_not_canvas(self):
  self.change('new',lambda s:s['window'].update(width=128,height=96))
  with self.assertRaisesRegex(ValueError,'layer_window_capture'):self.validate()
 def test_clip_cannot_claim_zero_visual_change(self):
  p=self.root/REPORT;r=json.loads(p.read_text());next(c for c in r['renderChanges']['cases'] if c['command']=='layer.clippingMask.toggle')['comparisons'][0]['changedPixels']=0;p.write_text(json.dumps(r))
  with self.assertRaisesRegex(ValueError,'layer_render_pixels'):self.validate()
 def test_state_only_canvas_must_stay_same(self):
  p=self.root/REPORT;r=json.loads(p.read_text());r['renderChanges']['cases'][0]['comparisons'][0]['changedPixels']=1;p.write_text(json.dumps(r))
  with self.assertRaisesRegex(ValueError,'layer_render_pixels'):self.validate()
 def test_image_comparison_hash_binding(self):
  p=self.root/REPORT;r=json.loads(p.read_text());r['renderChanges']['cases'][0]['comparisons'][2]['firstSha256']='0'*64;p.write_text(json.dumps(r))
  with self.assertRaisesRegex(ValueError,'layer_render_binding'):self.validate()
