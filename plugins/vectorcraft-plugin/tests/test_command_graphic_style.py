"""样式断言必须覆盖渐变相对坐标、唯一名称和追加外观保全。"""
import copy,importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class GraphicStyleTests(unittest.TestCase):
 def setUp(self):
  p=ROOT/'scripts/qa/command_graphicStyle.py';self.assertTrue(p.is_file(),'graphic_style_acceptance_missing');s=importlib.util.spec_from_file_location('graphic_style_qa',p);self.m=importlib.util.module_from_spec(s);s.loader.exec_module(self.m)
 def test_unique_names_use_first_free_suffix(self):self.assertEqual(self.m.unique('A',[{'name':'A'},{'name':'A 2'}]),'A 3')
 def test_gradient_rebases_points_not_aspect(self):
  a={'items':[{'kind':'fill','paint':{'type':'gradient','geom':{'start':{'x':10,'y':20},'end':{'x':30,'y':60},'aspect':.7}}}]};r=self.m.rebase(a,(10,20,20,40),(0,0,1,1));self.assertEqual(r['items'][0]['paint']['geom'],{'start':{'x':0,'y':0},'end':{'x':1,'y':1},'aspect':.7});self.assertEqual(a['items'][0]['paint']['geom']['start']['x'],10)
 def test_add_keeps_transparency_and_unlinks(self):
  n={'id':2,'kind':{'type':'path'},'opacity':.3,'graphic_style':9,'appearance':{'items':[{'kind':'fill','paint':{'type':'none'}}]}};g={'id':5,'opacity':.7,'appearance':{'items':[{'kind':'stroke','paint':{'type':'none'},'width':2}]}}
  self.m.apply(n,g,add=True);self.assertEqual(n['opacity'],.3);self.assertNotIn('graphic_style',n);self.assertEqual(len(n['appearance']['items']),2)
 def test_replace_transparency_restores_defaults(self):
  n={'id':2,'kind':{'type':'path'},'opacity':.3,'blend':'Multiply','appearance':{}};self.m.apply(n,{'id':5,'appearance':{'items':[]}});self.assertNotIn('opacity',n);self.assertNotIn('blend',n);self.assertEqual(n['graphic_style'],5)
 def test_unknown_command_rejected(self):
  with self.assertRaisesRegex(ValueError,'style_command_unknown'):self.m.expected('graphicStyle.future',{}, {}, {}, {})
