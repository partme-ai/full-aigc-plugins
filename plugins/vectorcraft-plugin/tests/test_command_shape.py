"""形状验收必须拒绝错几何、漏对象及不明返回ID。"""
import copy,importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class ShapeTests(unittest.TestCase):
 def setUp(self):
  p=ROOT/'scripts/qa/command_shape.py';self.assertTrue(p.is_file(),'shape_acceptance_missing');s=importlib.util.spec_from_file_location('shape_qa',p);self.m=importlib.util.module_from_spec(s);s.loader.exec_module(self.m)
 def test_line_endpoints(self):
  paths,_=self.m.geometry('shape.line',{'x1':1,'y1':2,'x2':8,'y2':9});self.assertEqual(paths[0],{'anchors':[{'p':[1,2]},{'p':[8,9]}],'closed':False})
 def test_grid_divider_count_is_not_cell_count(self):
  paths,_=self.m.geometry('shape.rectangularGrid',{'x':0,'y':0,'width':30,'height':20,'rows':2,'columns':3});self.assertEqual(len(paths),6)
 def test_spiral_starts_at_inner_end(self):
  paths,_=self.m.geometry('shape.spiral',{'cx':0,'cy':0,'radius':10,'decay':50,'segments':4,'clockwise':True});self.assertAlmostEqual(paths[0]['anchors'][0]['p'][0],.625)
 def test_unknown_has_no_generic_pass(self):
  with self.assertRaisesRegex(ValueError,'shape_command_unknown'):self.m.geometry('shape.future',{})
 def test_wrong_anchor_is_rejected(self):
  with self.assertRaisesRegex(ValueError,'shape_path_geometry'):self.m.assert_path({'subpaths':[{'anchors':[{'p':[1,2]}],'closed':False}]},[{'anchors':[{'p':[1,3]}],'closed':False}])
 def test_wrong_curve_handle_is_rejected(self):
  with self.assertRaisesRegex(ValueError,'shape_path_geometry'):self.m.assert_path({'subpaths':[{'anchors':[{'p':[1,2],'out':[5,6]}],'closed':False}]},[{'anchors':[{'p':[1,2],'out':[5,7]}],'closed':False}])
 def test_wrong_closed_flag_is_rejected(self):
  with self.assertRaisesRegex(ValueError,'shape_path_geometry'):self.m.assert_path({'subpaths':[{'anchors':[{'p':[1,2]}],'closed':True}]},[{'anchors':[{'p':[1,2]}],'closed':False}])
