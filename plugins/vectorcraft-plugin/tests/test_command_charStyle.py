"""字符样式独立契约与UTF8范围行为。"""
import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CharStyleTests(unittest.TestCase):
 def setUp(self):
  p=ROOT/'scripts/qa/command_charStyle.py';self.assertTrue(p.exists(),'char_style_contract_missing');s=importlib.util.spec_from_file_location('char_style',p);self.m=importlib.util.module_from_spec(s);s.loader.exec_module(self.m)
 def test_restyle_keeps_local_override(self):self.assertEqual(self.m.restyle({'underline':False,'strikethrough':False},{'underline':True,'strikethrough':False},{'underline':True,'strikethrough':True}),{'underline':False,'strikethrough':True})
 def test_restyle_omitted_old_key_updates(self):self.assertEqual(self.m.restyle({'underline':False},{},{'underline':True}),{'underline':True})
 def test_removed_definition_key_does_not_reset_user(self):self.assertEqual(self.m.restyle({'underline':True},{'underline':True},{}),{'underline':True})
 def test_utf8_range_floors_character_boundary_and_merges(self):
  r=[{'text':'Ownéd QA','style':{'underline':False}}];out=self.m.style_range(r,6,4,lambda s:{**s,'underline':True});self.assertEqual([(x['text'],x['style']['underline']) for x in out],[('Own',False),('éd',True),(' QA',False)])
 def test_zero_width_range_preserves_nonempty_text(self):
  r=[{'text':'abc','style':{'underline':False}}];self.assertEqual(self.m.style_range(r,1,1,lambda s:{**s,'underline':True}),r)
 def test_empty_text_retains_changed_style(self):self.assertEqual(self.m.style_range([{'text':'','style':{'underline':False}}],0,0,lambda s:{**s,'underline':True}),[{'text':'','style':{'underline':True}}])
 def test_unique_copy_name(self):self.assertEqual(self.m.unique('Owned copy',[{'name':'Owned copy'},{'name':'Owned copy 2'}],copy_name=True),'Owned copy 3')
 def test_style_at_boundary_uses_preceding_run(self):
  r=[{'text':'ab','style':{'underline':False}},{'text':'cd','style':{'underline':True}}];self.assertFalse(self.m.style_at(r,2)['underline']);self.assertTrue(self.m.style_at(r,3)['underline'])
if __name__=='__main__':unittest.main()
