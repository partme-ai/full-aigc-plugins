"""辅助线独立树变换与窗口坐标验收。"""
import copy, importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class GuideTests(unittest.TestCase):
 def setUp(self):
  path=ROOT/'scripts/qa/command_guide.py';self.assertTrue(path.is_file(),'guide_acceptance_missing');s=importlib.util.spec_from_file_location('guide_qa',path);self.m=importlib.util.module_from_spec(s);s.loader.exec_module(self.m)
 def seed(self):return {'guides':[{'vertical':True,'pos':10},{'vertical':False,'pos':20}],'layers':[{'id':2,'name':'control'}]}
 def test_add_appends_and_returns_original_length(self):
  b=self.seed();a=self.m.expected('guide.add',b,{'vertical':False,'pos':42},{'index':2});self.assertEqual(a['guides'][-1],{'vertical':False,'pos':42});self.assertEqual(len(b['guides']),2)
 def test_add_index_is_checked(self):
  with self.assertRaisesRegex(ValueError,'guide_return'):self.m.expected('guide.add',self.seed(),{'vertical':True,'pos':42},{'index':0})
 def test_move_changes_only_position(self):
  b=self.seed();a=self.m.expected('guide.move',b,{'index':1,'pos':-5},{});self.assertEqual(a['guides'],[{'vertical':True,'pos':10},{'vertical':False,'pos':-5}]);self.assertEqual(a['layers'],b['layers'])
 def test_remove_compacts_indices(self):self.assertEqual(self.m.expected('guide.remove',self.seed(),{'index':0},{})['guides'],[{'vertical':False,'pos':20}])
 def test_unknown_command_is_rejected(self):
  with self.assertRaisesRegex(ValueError,'guide_unknown'):self.m.expected('guide.future',self.seed(),{}, {})
 def test_window_coordinates_apply_center_and_zoom(self):
  ui={'canvasRect':[76,84,1030,767],'view':{'center':{'x':64,'y':48},'zoom':2,'rotation':0}};self.assertEqual(self.m.screen_coordinate({'vertical':True,'pos':100},ui),663);self.assertEqual(self.m.screen_coordinate({'vertical':False,'pos':30},ui),431.5)
 def test_guide_model_has_no_other_changes(self):
  b=self.seed();s={'before':b,'after':self.m.expected('guide.move',b,{'index':0,'pos':40},{}),'params':{'index':0,'pos':40},'returned':{},'round':1};s['reopened']=copy.deepcopy(s['after']);s['after']['layers'][0]['name']='bad'
  with self.assertRaisesRegex(ValueError,'guide_tree'):self.m.validate_transition('guide.move',s)

 def test_remove_returns_native_null(self):
  b=self.seed();a=self.m.expected('guide.remove',b,{'index':0},None);self.m.validate_transition('guide.remove',{'before':b,'after':a,'reopened':copy.deepcopy(a),'params':{'index':0},'returned':None,'round':1})

 def lock_probe(self):
  b=self.seed();return {'before':b,'after':copy.deepcopy(b),'lockOn':{'locked':True},'lockOff':{'locked':False},'locked':[{'id':c,'enabled':c=='guide.add'} for c in self.m.COMMANDS],'unlocked':[{'id':c,'enabled':True} for c in self.m.COMMANDS]}
 def test_locked_context_disables_remove_and_move(self):self.m.validate_context(self.lock_probe())
 def test_locked_move_cannot_be_enabled(self):
  p=self.lock_probe();p['locked'][2]['enabled']=True
  with self.assertRaisesRegex(ValueError,'guide_lock_context'):self.m.validate_context(p)
 def test_lock_probe_cannot_change_project(self):
  p=self.lock_probe();p['after']['guides'].pop()
  with self.assertRaisesRegex(ValueError,'guide_lock_preservation'):self.m.validate_context(p)

 def test_ready_ui_waits_for_fit_without_edit(self):
  from unittest.mock import patch
  m=self.m.load_local('command_family_guide');replies=iter([{'view':{'fitted':False}},{'view':{'fitted':True}}]);calls=[]
  class Owned:
   def request(self,method,params):calls.append((method,params));return next(replies)
  class Commands:
   @staticmethod
   def parse_reply(value):return value
  with patch.object(m.time,'sleep') as pause:ui,attempts=m.ready_ui(Owned(),Commands())
  self.assertTrue(ui['view']['fitted']);self.assertEqual([x['status'] for x in attempts],['awaiting-fit','PASS']);self.assertEqual(len(calls),2);pause.assert_called_once_with(.05);self.assertTrue(all(p['name']=='inspect_ui' for _,p in calls))
 def test_ready_ui_timeout_stops_after_twenty_reads(self):
  from unittest.mock import patch
  m=self.m.load_local('command_family_guide');calls=[]
  class Owned:
   def request(self,method,params):calls.append(params);return {'view':{'fitted':False}}
  class Commands:
   @staticmethod
   def parse_reply(value):return value
  with patch.object(m.time,'sleep'):
   with self.assertRaisesRegex(ValueError,'guide_ui_fit_timeout'):m.ready_ui(Owned(),Commands())
  self.assertEqual(len(calls),20)
