"""透明度验收拒绝蒙版、控制对象及保存重开错误。"""
import copy, importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class TransparencyTests(unittest.TestCase):
 def setUp(self):
  p=ROOT/'scripts/qa/command_transparency.py';self.assertTrue(p.is_file(),'transparency_acceptance_missing')
  spec=importlib.util.spec_from_file_location('transparency_qa',p);self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
 def stage(self):
  model={'layers':[{'id':1,'kind':{'children':[{'id':2,'opacity':1.,'kind':{'type':'path'},'appearance':{'items':[]}},{'id':3,'kind':{'type':'text','text':'CONTROL'}}]}}],'next_id':4}
  after=copy.deepcopy(model);after['layers'][0]['kind']['children'][0].update(opacity=.6,blend='Multiply',isolate=True,knockout='off',knockout_shape=True)
  return {'params':{'ids':[2],'item':None,'opacity':60,'blend':'Multiply','isolate':True,'knockout':'off','knockoutShape':True},'before':model,'after':after,'reopened':copy.deepcopy(after),'returned':None,'fixture':{},'observed':{'info':{'ids':[2],'opacity':60,'blend':'Multiply','isolate':True,'knockout':'off','knockoutShape':True,'editingMask':None,'pageIsolatedBlending':False,'pageKnockoutGroup':False},'maskInfo':[]}}
 def test_opacity_and_all_flags(self):self.m.validate_transition('transparency.set',self.stage())
 def test_wrong_percentage(self):
  s=self.stage();s['after']['layers'][0]['kind']['children'][0]['opacity']=60;s['reopened']=copy.deepcopy(s['after'])
  with self.assertRaisesRegex(ValueError,'transparency_native_semantics'):self.m.validate_transition('transparency.set',s)
 def test_control_preservation(self):
  s=self.stage();s['after']['layers'][0]['kind']['children'][1]['kind']['text']='WRONG';s['reopened']=copy.deepcopy(s['after'])
  with self.assertRaisesRegex(ValueError,'transparency_native_semantics'):self.m.validate_transition('transparency.set',s)
 def test_reopen_loss(self):
  s=self.stage();s['reopened']=s['before']
  with self.assertRaisesRegex(ValueError,'transparency_reopen'):self.m.validate_transition('transparency.set',s)
 def test_readback_must_match_model(self):
  s=self.stage();s['observed']['info']['opacity']=61
  with self.assertRaisesRegex(ValueError,'transparency_info'):self.m.validate_transition('transparency.set',s)
 def test_unknown_never_passes(self):
  with self.assertRaisesRegex(ValueError,'transparency_command_unknown'):self.m.validate_transition('transparency.unknown',self.stage())
 def test_mask_art_ids_are_not_ignored_in_saved_project(self):
  s=self.stage();s['after']['layers'][0]['kind']['children'][0]['mask']={'art':{'id':4}};s['reopened']=copy.deepcopy(s['after']);s['reopened']['layers'][0]['kind']['children'][0]['mask']['art']['id']=5
  with self.assertRaisesRegex(ValueError,'transparency_reopen'):self.m.validate_transition('transparency.set',s)
