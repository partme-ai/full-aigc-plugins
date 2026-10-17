"""逐命令验收必须验证原生语义、无关对象与重开结果，不能只记录PASS布尔值。"""
import copy
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'scripts/qa/command_paint.py'

class PaintCommandEvidenceTests(unittest.TestCase):
 def setUp(self):
  self.assertTrue(PATH.is_file(),'paint_command_acceptance_missing')
  spec=importlib.util.spec_from_file_location('paint_command_qa',PATH);self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
 def model(self,color):
  return {'layers':[{'id':1,'kind':{'type':'layer','children':[{'id':2,'kind':{'type':'path'},'appearance':{'items':[{'kind':'fill','paint':{'type':'solid','color':color}}]}},{'id':3,'kind':{'type':'text','runs':[{'text':'CONTROL'}]}}]}}],'artboards':[{'id':1,'width':128,'height':96}]}
 def stage(self):
  before=self.model({'model':'rgb','r':1,'g':0,'b':0});after=self.model({'model':'rgb','r':34/255,'g':170/255,'b':102/255})
  return {'params':{'color':'#22aa66','ids':[2]},'before':before,'after':after,'reopened':copy.deepcopy(after),'proxiesBefore':{},'proxiesAfter':{},'freeformBefore':None,'freeformAfter':None,'returned':{}}
 def test_color_transition_and_reopen_are_checked(self):self.m.validate_transition('paint.setFill',self.stage())
 def test_returned_pass_cannot_hide_wrong_native_color(self):
  s=self.stage();s['after']=copy.deepcopy(s['before']);s['reopened']=copy.deepcopy(s['after'])
  with self.assertRaisesRegex(ValueError,'paint_color'):self.m.validate_transition('paint.setFill',s)
 def test_control_text_mutation_is_refused(self):
  s=self.stage();s['after']['layers'][0]['kind']['children'][1]['kind']['runs'][0]['text']='WRONG'
  with self.assertRaisesRegex(ValueError,'paint_control'):self.m.validate_transition('paint.setFill',s)
 def test_saved_project_must_reopen_to_checked_native_objects(self):
  s=self.stage();s['reopened']=copy.deepcopy(s['before'])
  with self.assertRaisesRegex(ValueError,'paint_reopen'):self.m.validate_transition('paint.setFill',s)
 def test_unknown_command_cannot_get_generic_success(self):
  with self.assertRaisesRegex(ValueError,'paint_command_unknown'):self.m.validate_transition('paint.futureUnknown',self.stage())

 def test_freeform_native_rgb_array_retains_color_assertions(self):
  self.assertEqual(self.m.rgb([.4,.2,.6]),(.4,.2,.6))
  for bad in ([1,2,3],[0,0],[True,0,0],[float('nan'),0,0]):
   with self.assertRaisesRegex(ValueError,'paint_color'):self.m.rgb(bad)
