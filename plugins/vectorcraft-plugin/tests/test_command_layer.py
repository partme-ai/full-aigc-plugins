"""图层验收的独立树变换必须保全控制对象并区分会话状态。"""
import copy,importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class LayerTests(unittest.TestCase):
 def setUp(self):
  p=ROOT/'scripts/qa/command_layer.py';self.assertTrue(p.is_file(),'layer_acceptance_missing');s=importlib.util.spec_from_file_location('layer_qa',p);self.m=importlib.util.module_from_spec(s);s.loader.exec_module(self.m)
 def base(self):return {'layers':[self.m.layer(1,'Layer 1',0)],'next_id':2,'metadata':{}}
 def state(self):return {'currentLayer':1,'selection':[],'target':None,'pasteRemembersLayers':False}
 def test_new_inserts_above_current_not_always_top(self):
  b=self.base();b['layers'].append(self.m.layer(2,'Upper',1));b['next_id']=3
  e,st=self.m.expected('layer.new',b,{'name':'New'},self.state(),{'id':3});self.assertEqual([n['id'] for n in e['layers']],[1,3,2]);self.assertEqual(st['currentLayer'],3)
 def test_duplicate_assigns_fresh_preorder_ids(self):
  b=self.base();b['layers'][0]['kind']['children']=[self.m.layer(2,'Nested',2)];b['next_id']=3
  e,st=self.m.expected('layer.duplicate',b,{'id':1},self.state(),{'id':3});self.assertEqual([e['layers'][1]['id'],e['layers'][1]['kind']['children'][0]['id']],[3,4]);self.assertEqual(e['layers'][1]['name'],'Layer 1 copy');self.assertEqual(st['currentLayer'],1)
 def test_select_all_is_immediate_and_filters_hidden_locked(self):
  b=self.base();ch=[self.m.layer(i,str(i),0) for i in (2,3,4)];ch[1]['visible']=False;ch[2]['locked']=True;b['layers'][0]['kind']['children']=ch
  e,st=self.m.expected('layer.selectAll',b,{'id':1},self.state(),{});self.assertEqual(e,b);self.assertEqual(st['selection'],[2])
 def test_target_changes_session_without_serializing_target(self):
  b=self.base();e,st=self.m.expected('layer.target',b,{'id':1},self.state(),{'id':1,'selected':[]});self.assertEqual(e,b);self.assertEqual(st['target'],1)
 def test_paste_false_uses_absent_default(self):
  b=self.base();b['paste_remembers_layers']=True;e,st=self.m.expected('layer.pasteRemembersLayers',b,{'on':False},self.state(),{'on':False});self.assertNotIn('paste_remembers_layers',e)
 def test_wrong_new_return_id_rejected(self):
  with self.assertRaisesRegex(ValueError,'layer_return_id'):self.m.expected('layer.new',self.base(),{},self.state(),{'id':1})
 def test_unknown_command_cannot_pass(self):
  with self.assertRaisesRegex(ValueError,'layer_command_unknown'):self.m.expected('layer.future',self.base(),{},self.state(),{})
