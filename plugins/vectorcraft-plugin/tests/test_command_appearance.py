"""外观堆栈的独立变换必须保留行序与Contents槽。"""
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class AppearanceTests(unittest.TestCase):
 def setUp(self):
  p=ROOT/'scripts/qa/command_appearance.py';self.assertTrue(p.is_file(),'appearance_acceptance_missing');s=importlib.util.spec_from_file_location('appearance_qa',p);self.m=importlib.util.module_from_spec(s);s.loader.exec_module(self.m)
 def test_insert_at_contents_boundary_preserves_below_side(self):
  ap={'items':[{'id':1},{'id':2}],'contents_index':1};self.m.insert(ap,1,{'id':3});self.assertEqual(ap['contents_index'],2);self.assertEqual([i['id'] for i in ap['items']],[1,3,2])
 def test_remove_below_contents_decrements_slot(self):
  ap={'items':[{'id':1},{'id':2}],'contents_index':1};self.m.remove(ap,0);self.assertNotIn('contents_index',ap)
 def test_move_keeps_side_when_adjacent_to_contents(self):
  ap={'items':[{'id':1},{'id':2},{'id':3}],'contents_index':2};self.assertEqual(self.m.move(ap,0,1),1);self.assertEqual(ap['contents_index'],2)
 def test_add_fill_copies_paint_only(self):
  n={'kind':{'type':'path'},'appearance':{'items':[{'kind':'fill','paint':{'type':'none'},'opacity':.2,'effects':[{'id':'x'}]}]}};self.m.add(n,True);self.assertEqual(n['appearance']['items'][-1],{'kind':'fill','paint':{'type':'none'}})
 def test_unknown_command_cannot_pass(self):
  with self.assertRaisesRegex(ValueError,'appearance_command_unknown'):self.m.expected('appearance.future',{}, {}, {}, {})

 def test_transfer_fixture_passes_ordered_ids_to_mask_command(self):
  calls=[]
  def call(command,**params):
   calls.append((command,params));return {'id':7} if command=='shape.rectangle' else None
  self.m.prepare(call,'appearance.transfer',1,Path('/owned'),{'layer':4,'source':5,'other':6})
  params=next(p for c,p in calls if c=='transparency.makeOpacityMask');self.assertEqual(params.get('ids'),[5,7])

 def test_transfer_mask_is_created_in_source_layer(self):
  calls=[]
  def call(command,**params):
   calls.append((command,params));return {'id':7} if command=='shape.rectangle' else None
  self.m.prepare(call,'appearance.transfer',1,Path('/owned'),{'layer':4,'source':5,'other':6})
  mask_index=next(i for i,(c,p) in enumerate(calls) if c=='shape.rectangle')
  self.assertIn(('layer.setCurrent',{'id':4}),calls[:mask_index])
