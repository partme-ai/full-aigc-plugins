"""色板验收需核对原生颜色、关联、控制对象及保存重开。"""
import copy,importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class SwatchCommandTests(unittest.TestCase):
 def setUp(self):
  path=ROOT/'scripts/qa/command_swatch.py';self.assertTrue(path.is_file(),'swatch_command_acceptance_missing')
  spec=importlib.util.spec_from_file_location('swatch_qa',path);self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
 def stage(self):
  rgb={'model':'rgb','r':.4,'g':.2,'b':.6}
  target={'id':2,'kind':{'type':'path'},'appearance':{'items':[{'kind':'fill','paint':{'type':'solid','color':rgb}}]}}
  model={'layers':[{'id':1,'kind':{'type':'layer','children':[target,{'id':3,'kind':{'type':'text','text':'CONTROL'}}]}}],'artboards':[], 'swatches':[], 'swatch_groups':[], 'setup':{}}
  after=copy.deepcopy(model);after['swatches']=[{'name':'QA New','global':True,'spot':False,'paint':{'type':'solid','color':rgb}}]
  row={'name':'QA New','kind':'color','global':True,'spot':False,'group':None,'color':rgb}
  return {'params':{'name':'QA New','color':'#663399','global':True},'before':model,'after':after,'reopened':copy.deepcopy(after),'returned':{'name':'QA New','names':['QA New']},'listBefore':{'swatches':[],'groups':[]},'listAfter':{'swatches':[row],'groups':[]},'fixture':{}}
 def test_new_swatch_native_color_and_reopen(self):self.m.validate_transition('swatch.new',self.stage())
 def test_forged_color_is_rejected(self):
  s=self.stage();s['after']['swatches'][0]['paint']['color']['r']=0;s['reopened']=copy.deepcopy(s['after'])
  with self.assertRaisesRegex(ValueError,'swatch_color'):self.m.validate_transition('swatch.new',s)
 def test_control_text_is_preserved(self):
  s=self.stage();s['after']['layers'][0]['kind']['children'][1]['kind']['text']='WRONG'
  with self.assertRaisesRegex(ValueError,'swatch_control'):self.m.validate_transition('swatch.new',s)
 def test_lost_swatch_after_reopen_is_rejected(self):
  s=self.stage();s['reopened']=copy.deepcopy(s['before'])
  with self.assertRaisesRegex(ValueError,'swatch_reopen'):self.m.validate_transition('swatch.new',s)
 def test_unknown_command_has_no_generic_pass(self):
  with self.assertRaisesRegex(ValueError,'swatch_command_unknown'):self.m.validate_transition('swatch.futureUnknown',self.stage())
