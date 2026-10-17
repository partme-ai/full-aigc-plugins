"""固定效果证据拒绝目录、列表、展开产物、目标与保全篡改。"""
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

REPORT='docs/evidence/vectorcraft-command-effect-fixed64-20261009.json'
class EffectEvidenceTests(unittest.TestCase):
 def setUp(self):
  self.assertTrue((ROOT/REPORT).is_file(),'effect_fixed_evidence_missing');self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  for name in (REPORT,'docs/current-identity.json','docs/evidence/vectorcraft-public-tag64-install-20261009.json','skills/vectorcraft-use/references/command-coverage.json',*[f'scripts/qa/{n}.py' for n in ('command_family_window','command_family_window_diagnostic','command_effect_render','command_layer_render','command_paint','command_shape','command_graphicStyle','command_appearance','command_effect')]):
   p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(name),p)
  name='scripts/qa/effect_catalog_contract.json';p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(name),p)
  spec=importlib.util.spec_from_file_location('effect_evidence',ROOT/'scripts/verify_command_families.py');self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
 def change(self,command,mutate,round=1):
  p=self.root/REPORT;r=json.loads(p.read_text());s=next(c['stages'][round-1] for c in r['cases'] if c['command']=='effect.'+command);mutate(s);p.write_text(json.dumps(r))
 def validate(self):return self.m.validate_family(self.root,'effect',REPORT)
 def model_change(self,command,mutate,round=1):
  def change(s):mutate(s['after']);s['reopened']=copy.deepcopy(s['after'])
  self.change(command,change,round)
 def node(self,model,id):
  spec=importlib.util.spec_from_file_location('effect_shape',ROOT/'scripts/qa/command_shape.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m.find(model,id)
 def expand_change(self,key,mutate):
  def change(s):
   mutate(self.node(s['after'],s['fixture'][key]));s['reopened']=copy.deepcopy(s['after'])
  self.change('expandAppearance',change,2)
 def test_all_seven_commands(self):self.assertEqual(len(self.validate()),7)
 def test_apply_keeps_unknown_parameter(self):
  self.model_change('apply',lambda m:self.node(m,2)['appearance']['effects'][-1]['params'].pop('ownedMarker'))
  with self.assertRaisesRegex(ValueError,'effect_tree_transition'):self.validate()
 def test_explicit_contents_ignore_active_row(self):
  def mutate(m):
   n=self.node(m,5);n['appearance']['items'][0].setdefault('effects',[]).append(n['appearance']['effects'].pop())
  self.model_change('apply',mutate,2)
  with self.assertRaisesRegex(ValueError,'effect_tree_transition'):self.validate()
 def test_full_catalog_cannot_lose_an_entry(self):
  self.change('list',lambda s:s['returned']['catalog'].pop())
  with self.assertRaisesRegex(ValueError,'effect_catalog_contract'):self.validate()
 def test_readback_active_item_is_real(self):
  self.change('list',lambda s:s['returned'].update(activeItem=99))
  with self.assertRaisesRegex(ValueError,'effect_active_item_readback'):self.validate()
 def test_parameter_merge_keeps_unmentioned_join(self):
  self.model_change('setParams',lambda m:self.node(m,2)['appearance']['effects'][1]['params'].pop('joins'))
  with self.assertRaisesRegex(ValueError,'effect_tree_transition'):self.validate()
 def test_effect_edits_preserve_object_opacity(self):
  self.model_change('setParams',lambda m:self.node(m,2).update(opacity=.2),2)
  with self.assertRaisesRegex(ValueError,'effect_tree_transition'):self.validate()
 def test_remove_preserves_remaining_order(self):
  self.model_change('remove',lambda m:self.node(m,2)['appearance']['effects'].reverse())
  with self.assertRaisesRegex(ValueError,'effect_tree_transition'):self.validate()
 def test_duplicate_goes_immediately_after_source(self):
  self.model_change('duplicate',lambda m:self.node(m,2)['appearance']['effects'].reverse())
  with self.assertRaisesRegex(ValueError,'effect_tree_transition'):self.validate()
 def test_cross_list_copy_keeps_original(self):
  self.model_change('move',lambda m:self.node(m,2)['appearance']['items'][0]['effects'].pop(1),2)
  with self.assertRaisesRegex(ValueError,'effect_tree_transition'):self.validate()
 def test_expand_rectangle_geometry(self):
  self.model_change('expandAppearance',lambda m:self.node(m,2)['kind']['path']['subpaths'][0]['anchors'][0]['p'].__setitem__(0,99))
  with self.assertRaisesRegex(ValueError,'effect_expand_geometry'):self.validate()
 def test_expand_preserves_mask(self):
  self.model_change('expandAppearance',lambda m:self.node(m,2)['mask'].update(clip=False))
  with self.assertRaisesRegex(ValueError,'effect_expand_identity_transparency'):self.validate()
 def test_expand_allocates_unique_node_ids(self):
  self.expand_change('multi',lambda n:n['kind']['children'][0].update(id=n['id']))
  with self.assertRaisesRegex(ValueError,'effect_expand_allocation'):self.validate()
 def test_expanded_stroke_retains_its_paint(self):
  self.expand_change('multi',lambda n:n['kind']['children'][1]['appearance']['items'][0].update(paint={'type':'none'}))
  with self.assertRaisesRegex(ValueError,'effect_expand_stroke_paint'):self.validate()
 def test_shadow_image_stays_below_vector_art(self):
  self.expand_change('shadow',lambda n:n['kind']['children'].reverse())
  with self.assertRaisesRegex(ValueError,'effect_expand_shadow_order|effect_expand_image'):self.validate()
 def test_embedded_images_contain_decoded_pixels(self):
  self.change('expandAppearance',lambda s:[m.update(nontransparentPixels=0) for m in s['observed']['embeddedImages']],2)
  with self.assertRaisesRegex(ValueError,'effect_expand_image_pixels'):self.validate()
 def test_blur_replaces_vector_art(self):
  self.expand_change('blur',lambda n:n.update(kind={'type':'path'}))
  with self.assertRaisesRegex(ValueError,'effect_expand_image'):self.validate()
 def test_own_painted_type_is_outlined(self):
  self.expand_change('text',lambda n:n.update(kind={'type':'text'}))
  with self.assertRaisesRegex(ValueError,'effect_expand_text_outlines'):self.validate()
 def test_crop_marks_are_real_geometry(self):
  self.expand_change('crop',lambda n:n['kind']['children'].pop())
  with self.assertRaisesRegex(ValueError,'effect_expand_crop_marks'):self.validate()
 def test_transform_copies_are_baked(self):
  self.expand_change('transform',lambda n:n['kind']['children'].pop())
  with self.assertRaisesRegex(ValueError,'effect_expand_transform_copies'):self.validate()
 def test_native_reopen_preserves_effect_stacks(self):
  self.change('apply',lambda s:self.node(s['reopened'],2)['appearance']['effects'].pop())
  with self.assertRaisesRegex(ValueError,'effect_reopen'):self.validate()
 def test_control_text_cannot_change(self):
  self.model_change('remove',lambda m:self.node(m,3)['kind']['runs'][0].update(text='BAD'))
  with self.assertRaisesRegex(ValueError,'effect_tree_transition'):self.validate()
 def test_window_cannot_be_canvas(self):
  self.change('list',lambda s:s['window'].update(width=128,height=96))
  with self.assertRaisesRegex(ValueError,'effect_window_capture'):self.validate()

 def test_raster_image_region_is_computed_from_source_effect(self):
  self.expand_change('blur',lambda n:n['kind']['xf'].__setitem__(5,999))
  with self.assertRaisesRegex(ValueError,'effect_image_region'):self.validate()
 def test_text_knockout_policy_is_explicit(self):
  self.expand_change('text',lambda n:n.update(knockout='on'))
  with self.assertRaisesRegex(ValueError,'effect_expand_identity_transparency'):self.validate()
 def test_crop_wrapper_preserves_original_live_geometry(self):
  self.expand_change('crop',lambda n:n['kind']['children'][0]['kind'].pop('live'))
  with self.assertRaisesRegex(ValueError,'effect_expand_crop_original'):self.validate()
 def test_shadow_pixels_are_knocked_out_under_vector_center(self):
  p=self.root/REPORT;r=json.loads(p.read_text());r['renderChanges']['expandedImageChecks'][0]['centerRGBA']=[0,0,0,255];p.write_text(json.dumps(r))
  with self.assertRaisesRegex(ValueError,'effect_image_pixel_contract'):self.validate()
 def test_image_pixels_bind_to_actual_svg(self):
  p=self.root/REPORT;r=json.loads(p.read_text());r['renderChanges']['expandedImageChecks'][1]['svgSha256']='0'*64;p.write_text(json.dumps(r))
  with self.assertRaisesRegex(ValueError,'effect_image_pixel_binding'):self.validate()
