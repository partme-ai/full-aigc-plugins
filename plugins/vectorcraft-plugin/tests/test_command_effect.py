"""效果独立断言覆盖参数合并、列表移动和完整保全。"""
import copy
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class EffectTests(unittest.TestCase):
 def setUp(self):
  path=ROOT/'scripts/qa/command_effect.py';self.assertTrue(path.is_file(),'effect_acceptance_missing');s=importlib.util.spec_from_file_location('effect_qa',path);self.m=importlib.util.module_from_spec(s);s.loader.exec_module(self.m)
 def test_parameter_merge_preserves_unmentioned_keys(self):
  fx=[{'id':'distort.twist','params':{'angle':10,'owned':7},'visible':True}];self.m.edit_list('setParams',fx,{'index':0,'params':{'angle':20},'visible':False});self.assertEqual(fx,[{'id':'distort.twist','params':{'angle':20,'owned':7},'visible':False}])
 def test_duplicate_is_a_deep_copy_after_source(self):
  fx=[{'id':'distort.twist','params':{'angle':10},'visible':False}];self.m.edit_list('duplicate',fx,{'index':0});fx[1]['params']['angle']=99;self.assertEqual(fx[0]['params']['angle'],10);self.assertFalse(fx[1]['visible'])
 def test_move_removes_before_clamping_destination(self):
  a=[{'id':'a'},{'id':'b'}];self.assertEqual(self.m.move_list(a,a,0,99,False),1);self.assertEqual(a,[{'id':'b'},{'id':'a'}])
 def test_cross_list_copy_preserves_source(self):
  a=[{'id':'a'}];b=[];self.assertEqual(self.m.move_list(a,b,0,5,True),0);self.assertEqual(a,b);self.assertIsNot(a[0],b[0])
 def test_unknown_command_does_not_pass(self):
  with self.assertRaisesRegex(ValueError,'effect_command_unknown'):self.m.expected('effect.future',{}, {}, {}, {})

 def test_explicit_ids_ignore_panel_active_item(self):self.assertIsNone(self.m.item_of({'ids':[2]},{'activeItem':0}))
 def test_implicit_target_uses_panel_active_item(self):self.assertEqual(self.m.item_of({}, {'activeItem':1}),1)

 def test_layer_expansion_uses_layer_target_context(self):
  self.m.prepare_expand=lambda *args:({'ids':[4]}, {'expandRoots':[5]});calls=[]
  def call(command,**params):calls.append((command,params));return {}
  self.m.prepare(call,'effect.expandAppearance',2,Path('/owned'),{'layer':4,'children':[5,6]})
  self.assertIn(('layer.target',{'id':4}),calls)

 def test_text_outlines_have_explicit_knockout_off(self):
  old={'id':10,'kind':{'type':'text'},'opacity':.7};self.assertEqual(self.m.expected_outer(old),{'id':10,'opacity':.7,'knockout':'off'})
 def test_path_knockout_is_preserved_exactly(self):
  old={'id':2,'kind':{'type':'path'},'knockout':'on'};self.assertEqual(self.m.expected_outer(old),{'id':2,'knockout':'on'})

 def test_catalog_parser_keeps_nested_commas_inside_expressions(self):
  parser=self.m.load_local('effect_catalog_contract');self.assertEqual(parser.split_args('"a,b", json!({"k":[1,2]})'),['"a,b"','json!({"k":[1,2]})'])
 def test_catalog_parser_rejects_unclosed_expression(self):
  with self.assertRaisesRegex(ValueError,'effect_contract_syntax'):self.m.load_local('effect_catalog_contract').split_args('json!({')

 def test_crop_wrapper_preserves_original_live_shape(self):
  old={'id':11,'kind':{'type':'path','live':{'shape':'rectangle'}},'appearance':{'effects':[{'id':'cropMarks'}],'items':[]}}
  got=self.m.crop_original(old,36);self.assertEqual(got['kind'],old['kind']);self.assertEqual(got['id'],36);self.assertNotIn('effects',got['appearance']);self.assertIn('effects',old['appearance'])

 def test_embedded_svg_is_beside_exports_not_tool_image_cache(self):
  m=self.m.load_local('command_effect_render');s={'canvas':{'path':'effect.expandAppearance/v2/tool-images/canvas.png'},'exports':[{'path':'effect.expandAppearance/v2/artboard-1.svg'}]};self.assertEqual(m.embedded_path(s),Path('effect.expandAppearance/v2/expanded-images.svg'))
