"""描边验收必须检查原生宽度、点单位及未授权外观保全。"""
import copy,importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class StrokeCommandTests(unittest.TestCase):
 def setUp(self):
  p=ROOT/'scripts/qa/command_stroke.py';self.assertTrue(p.is_file(),'stroke_command_acceptance_missing')
  spec=importlib.util.spec_from_file_location('stroke_qa',p);self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
 def stage(self):
  model={'layers':[{'id':1,'kind':{'type':'layer','children':[{'id':2,'kind':{'type':'path','path':{'subpaths':[{'closed':True}]}},'appearance':{'items':[{'kind':'fill','paint':{'type':'none'}},{'kind':'stroke','paint':{'type':'solid'},'width':4}]}},{'id':3,'kind':{'type':'text','text':'CONTROL'}}]}}],'artboards':[]}
  after=copy.deepcopy(model);after['layers'][0]['kind']['children'][0]['appearance']['items'][1]['width']=6
  return {'params':{'ids':[2],'weight':6},'before':model,'after':after,'reopened':copy.deepcopy(after),'fixture':{'pathContext':'closed','profilesBefore':{'profiles':[]}},'observed':{'profilesAfter':{'profiles':[]}},'returned':None}
 def test_native_width_and_reopen_are_checked(self):self.m.validate_transition('stroke.set',self.stage())
 def test_wrong_width_is_rejected(self):
  s=self.stage();s['after']=copy.deepcopy(s['before']);s['reopened']=copy.deepcopy(s['after'])
  with self.assertRaisesRegex(ValueError,'stroke_weight'):self.m.validate_transition('stroke.set',s)
 def test_control_text_mutation_is_rejected(self):
  s=self.stage();s['after']['layers'][0]['kind']['children'][1]['kind']['text']='WRONG'
  with self.assertRaisesRegex(ValueError,'stroke_control'):self.m.validate_transition('stroke.set',s)
 def test_unrequested_fill_mutation_is_rejected(self):
  s=self.stage();s['after']['layers'][0]['kind']['children'][0]['appearance']['items'][0]['paint']={'type':'solid'}
  with self.assertRaisesRegex(ValueError,'stroke_protected_appearance'):self.m.validate_transition('stroke.set',s)
 def test_reopen_loss_is_rejected(self):
  s=self.stage();s['reopened']=copy.deepcopy(s['before'])
  with self.assertRaisesRegex(ValueError,'stroke_reopen'):self.m.validate_transition('stroke.set',s)
 def test_unknown_command_has_no_generic_pass(self):
  with self.assertRaisesRegex(ValueError,'stroke_command_unknown'):self.m.validate_transition('stroke.futureUnknown',self.stage())

 def test_setup_respects_disabled_reset_without_saved_profiles(self):
  seen=[]
  def call(command,**params):
   seen.append(command)
   if command=='stroke.widthProfile.list':return {'profiles':[{'builtIn':True}]}
   if command=='stroke.widthProfile.reset':raise AssertionError('reset disabled')
  self.m.initialize(call)
  self.assertNotIn('stroke.widthProfile.reset',seen)
 def test_add_rounds_require_distinct_unlisted_profiles(self):
  points=[]
  def call(command,**params):
   if command=='stroke.widthProfile.set':points.append(params['points'])
   if command=='stroke.widthProfile.list':return {'profiles':[]}
  for n in (1,2):self.m.prepare(call,'stroke.widthProfile.add',n,Path('/tmp'),{})
  self.assertEqual(len(points),2)
  self.assertNotEqual(points[0],points[1])
