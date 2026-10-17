"""固定样式证据必须拒绝错绑定、丢外观和伪库回执。"""
import copy,importlib.util,json,shutil,tempfile
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]

def payload_source(name):
    """执行载荷收敛在 vectorcraft-harness：沙箱复制的 skills/<domain>/scripts/ 源按字节等价映射。"""
    if isinstance(name, str):
        prefix = 'skills/vectorcraft-'
        if name.startswith(prefix) and '/scripts/' in name and not (ROOT/name).is_file():
            candidate = 'skills/vectorcraft-harness/scripts/' + name.split('/scripts/', 1)[1]
            if (ROOT/candidate).is_file():
                return candidate
    return name

REPORT='docs/evidence/vectorcraft-command-graphicStyle-fixed64-20261009.json'
class GraphicStyleEvidenceTests(unittest.TestCase):
 def setUp(self):
  self.assertTrue((ROOT/REPORT).is_file(),'graphic_style_fixed_evidence_missing');self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  for name in (REPORT,'docs/current-identity.json','docs/evidence/vectorcraft-public-tag64-install-20261009.json','skills/vectorcraft-use/references/command-coverage.json',*[f'scripts/qa/{n}.py' for n in ('command_family_window','command_graphicStyle_render','command_layer_render','command_paint','command_shape','command_graphicStyle')]):
   p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(name),p)
  spec=importlib.util.spec_from_file_location('style_evidence',ROOT/'scripts/verify_command_families.py');self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
 def change(self,command,mutate,round=1):
  p=self.root/REPORT;r=json.loads(p.read_text());s=next(c['stages'][round-1] for c in r['cases'] if c['command']=='graphicStyle.'+command);mutate(s);p.write_text(json.dumps(r))
 def validate(self):return self.m.validate_family(self.root,'graphicStyle',REPORT)
 def model_change(self,command,mutate,round=1):
  def change(s):mutate(s['after']);s['reopened']=copy.deepcopy(s['after'])
  self.change(command,change,round)
 def test_all_eighteen_commands(self):self.assertEqual(len(self.validate()),18)
 def test_apply_gradient_stays_relative(self):
  self.model_change('apply',lambda m:m['layers'][0]['kind']['children'][0]['appearance']['items'][0]['paint']['geom']['end'].update(x=999))
  with self.assertRaisesRegex(ValueError,'style_tree_transition'):self.validate()
 def test_add_cannot_replace_existing_stack(self):
  self.model_change('apply',lambda m:m['layers'][0]['kind']['children'][0]['appearance']['items'].pop(0),2)
  with self.assertRaisesRegex(ValueError,'style_tree_transition'):self.validate()
 def test_delete_keeps_look_but_unlinks(self):
  self.model_change('delete',lambda m:m['layers'][0]['kind']['children'][0].update(graphic_style=5))
  with self.assertRaisesRegex(ValueError,'style_tree_transition'):self.validate()
 def test_duplicate_must_get_unique_id(self):
  self.model_change('duplicate',lambda m:next(g for g in m['graphic_styles'] if g['name']=='Owned Zeta copy').update(id=5))
  with self.assertRaisesRegex(ValueError,'style_tree_transition'):self.validate()
 def test_control_text_preserved(self):
  self.model_change('rename',lambda m:m['layers'][0]['kind']['children'][1]['kind']['runs'][0].update(text='BAD'))
  with self.assertRaisesRegex(ValueError,'style_tree_transition'):self.validate()
 def test_redefine_does_not_overwrite_edited_object(self):
  def mutate(m):m['layers'][0]['kind']['children'][-1]['appearance']=copy.deepcopy(m['layers'][0]['kind']['children'][0]['appearance'])
  self.model_change('redefine',mutate)
  with self.assertRaisesRegex(ValueError,'style_tree_transition'):self.validate()
 def test_merge_stack_order(self):
  self.model_change('merge',lambda m:m['graphic_styles'][-1]['appearance']['items'].reverse())
  with self.assertRaisesRegex(ValueError,'style_tree_transition'):self.validate()
 def test_list_cannot_claim_missing_links(self):
  self.change('list',lambda s:s['observed']['list']['styles'][-1].update(linked=[]))
  with self.assertRaisesRegex(ValueError,'style_list_links'):self.validate()
 def test_unused_must_exclude_bound_styles(self):
  self.change('unused',lambda s:s['returned']['names'].append('Owned Zeta'))
  with self.assertRaisesRegex(ValueError,'style_unused'):self.validate()
 def test_library_reimport_must_deduplicate(self):
  self.change('addFromLibrary',lambda s:s['returned'].update(existing=[]),2)
  with self.assertRaisesRegex(ValueError,'style_library_add'):self.validate()
 def test_loaded_library_cannot_change_color(self):
  self.change('loadLibrary',lambda s:s['observed']['library']['styles'][1].update(fill='#ffffff'))
  with self.assertRaisesRegex(ValueError,'style_library_content'):self.validate()
 def test_saved_library_is_standalone(self):
  self.change('saveLibrary',lambda s:s['observed']['savedData']['styles'][0].update(id=5))
  with self.assertRaisesRegex(ValueError,'style_saved_standalone'):self.validate()
 def test_option_scope_not_restart(self):
  self.change('setOptions',lambda s:s['observed'].update(preferenceRestartAcceptance='PASS'))
  with self.assertRaisesRegex(ValueError,'style_preference_scope'):self.validate()
 def test_saved_project_preserves_style(self):
  self.change('new',lambda s:s['reopened']['graphic_styles'].pop())
  with self.assertRaisesRegex(ValueError,'style_reopen'):self.validate()
 def test_local_revision_not_noop(self):
  self.change('sortByName',lambda s:s['fixture'].update(revisionName='bad'),2)
  with self.assertRaisesRegex(ValueError,'style_local_revision'):self.validate()
 def test_window_not_canvas(self):
  self.change('library',lambda s:s['window'].update(width=128,height=96))
  with self.assertRaisesRegex(ValueError,'graphicStyle_window_capture'):self.validate()
 def test_render_preservation_contract(self):
  p=self.root/REPORT;r=json.loads(p.read_text());r['renderChanges']['cases'][1]['comparisons'][0]['changedPixels']=1;p.write_text(json.dumps(r))
  with self.assertRaisesRegex(ValueError,'layer_render_pixels'):self.validate()
