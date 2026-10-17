"""属性面板独立契约：默认值、目标范围与混合读回。"""
import copy,importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class AttributesTests(unittest.TestCase):
 def setUp(self):
  p=ROOT/'scripts/qa/command_attributes.py';self.assertTrue(p.is_file(),'attributes_acceptance_missing');s=importlib.util.spec_from_file_location('attrs',p);self.m=importlib.util.module_from_spec(s);s.loader.exec_module(self.m)
 def path(self,id=2):return {'id':id,'kind':{'type':'path','live':{'shape':'rectangle'},'path':{'subpaths':[{'anchors':[{'p':[0,0]},{'p':[10,0]},{'p':[10,10]},{'p':[0,10]}],'closed':True}]}},'appearance':{'items':[{'kind':'fill','paint':{'type':'none'}},{'kind':'stroke','paint':{'type':'none'}}]}}
 def test_default_center_is_not_stored(self):
  n=self.path();n['attrs']={'showCenter':False};self.m.edit_attrs(n,{'showCenter':True});self.assertNotIn('attrs',n)
 def test_text_center_override_is_stored(self):
  n={'kind':{'type':'text'}};self.m.edit_attrs(n,{'showCenter':True});self.assertEqual(n['attrs'],{'showCenter':True})
 def test_strings_are_trimmed(self):
  n=self.path();self.m.edit_attrs(n,{'url':'  https://example.invalid/a  ','note':'  note  '});self.assertEqual(n['attrs'],{'url':'https://example.invalid/a','note':'note'})
 def test_empty_attributes_are_removed(self):
  n=self.path();n['attrs']={'url':'a','imageMap':'polygon','note':'x'};self.m.edit_attrs(n,{'url':'','note':'','imageMap':'none'});self.assertNotIn('attrs',n)
 def test_explicit_ids_ignore_active_row(self):self.assertIsNone(self.m.item_for({'ids':[2]},{'activeItem':0},True,self.path()))
 def test_implicit_row_applies_only_to_its_kind(self):
  f={'activeItem':0};self.assertEqual(self.m.item_for({},f,True,self.path()),0);self.assertIsNone(self.m.item_for({},f,False,self.path()))
 def test_mixed_values_return_null(self):self.assertIsNone(self.m.same([True,False]));self.assertIsNone(self.m.same([]));self.assertEqual(self.m.same(['a','a']),'a')
 def test_recent_urls_are_unique_newest_first_and_bounded(self):self.assertEqual(self.m.recent(['a','b'],' b '),['b','a']);self.assertEqual(len(self.m.recent([str(i) for i in range(10)],'x')),10)
 def test_rectangle_winding_is_clockwise(self):self.assertEqual(self.m.path_values(self.path()),(['nonZero'],[False]))
 def test_group_metadata_does_not_change_children(self):
  child=self.path();n={'id':9,'kind':{'type':'group','children':[copy.deepcopy(child)]}};self.m.edit_attrs(n,{'note':'group'});self.assertEqual(n['kind']['children'],[child])
 def fixture(self):return {'selection':[2],'activeItem':0,'recentBefore':[]}
 def test_change_count_deduplicates_multiple_fields(self):
  b={'layers':[self.path()]};a,urls,r=self.m.expected('attributes.set',b,{'ids':[2],'overprintFill':True,'note':'n','url':'u'},self.fixture());self.assertEqual(r,{'changed':1});self.assertEqual(urls,['u']);self.assertNotIn('attrs',b['layers'][0])
 def test_unknown_command_is_rejected(self):
  with self.assertRaisesRegex(ValueError,'attributes_unknown'):self.m.expected('attributes.future',{}, {},{})
 def test_no_selection_info_has_null_values(self):
  result=self.m.info({'layers':[]},{'ids':[]},self.fixture(),[]);self.assertEqual(result['ids'],[]);self.assertIsNone(result['fillRule']);self.assertIsNone(result['overprintFill'])
 def test_explicit_fill_row_has_no_stroke_value(self):
  r=self.m.info({'layers':[self.path()]},{'ids':[2],'item':0},self.fixture(),[]);self.assertFalse(r['overprintFill']);self.assertIsNone(r['overprintStroke'])
 def text(self):return {'id':3,'kind':{'type':'text','runs':[{'text':'qa','style':{}}]},'appearance':{'items':[{'kind':'fill','paint':{'type':'none'}}]}}
 def test_whole_text_changes_character_flag(self):
  b={'layers':[self.text()]};f=self.fixture();a,_,r=self.m.expected('attributes.set',b,{'ids':[3],'overprintFill':True},f);self.assertTrue(a['layers'][0]['kind']['runs'][0]['style']['overprint_fill']);self.assertEqual(r,{'changed':1})
 def test_active_fill_leaves_character_flag_unchanged(self):
  b={'layers':[self.text()]};f=self.fixture();f['selection']=[3];a,_,_=self.m.expected('attributes.set',b,{'overprintFill':True},f);self.assertEqual(a['layers'][0]['kind']['runs'][0]['style'],{})
 def test_group_overprint_changes_leaf_but_note_stays_on_group(self):
  b={'layers':[{'id':9,'kind':{'type':'group','children':[self.path()]}}]};a,_,r=self.m.expected('attributes.set',b,{'ids':[9],'overprintFill':True,'note':'group'},self.fixture());self.assertEqual(r,{'changed':2});self.assertEqual(a['layers'][0]['attrs'],{'note':'group'});self.assertNotIn('attrs',a['layers'][0]['kind']['children'][0])
 def test_mixed_winding_reads_null(self):
  a=self.path(2);b=self.path(3);b['kind']['path']['subpaths'][0]['anchors'].reverse();r=self.m.info({'layers':[a,b]},{'ids':[2,3]},self.fixture(),[]);self.assertIsNone(r['reversed'])
