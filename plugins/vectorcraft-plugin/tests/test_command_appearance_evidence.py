"""固定外观证据拒绝错堆栈、错目标、蒙版丢失以及仅声明生效的偏好。"""
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

REPORT='docs/evidence/vectorcraft-command-appearance-fixed64-20261009.json'
class AppearanceEvidenceTests(unittest.TestCase):
 def setUp(self):
  self.assertTrue((ROOT/REPORT).is_file(),'appearance_fixed_evidence_missing');self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  for name in (REPORT,'docs/current-identity.json','docs/evidence/vectorcraft-public-tag64-install-20261009.json','skills/vectorcraft-use/references/command-coverage.json',*[f'scripts/qa/{n}.py' for n in ('command_family_window','command_family_window_diagnostic','command_appearance_render','command_layer_render','command_paint','command_shape','command_graphicStyle','command_appearance')]):
   p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(name),p)
  spec=importlib.util.spec_from_file_location('appearance_evidence',ROOT/'scripts/verify_command_families.py');self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m)
 def change(self,command,mutate,round=1):
  p=self.root/REPORT;r=json.loads(p.read_text());s=next(c['stages'][round-1] for c in r['cases'] if c['command']=='appearance.'+command);mutate(s);p.write_text(json.dumps(r))
 def validate(self):return self.m.validate_family(self.root,'appearance',REPORT)
 def model_change(self,command,mutate,round=1):
  def change(s):mutate(s['after']);s['reopened']=copy.deepcopy(s['after'])
  self.change(command,change,round)
 def test_all_sixteen_commands(self):self.assertEqual(len(self.validate()),16)
 def test_new_fill_does_not_copy_item_opacity(self):
  self.model_change('addFill',lambda m:m['layers'][0]['kind']['children'][0]['appearance']['items'][-1].update(opacity=.4))
  with self.assertRaisesRegex(ValueError,'appearance_tree_transition'):self.validate()
 def test_clear_resets_object_blend(self):
  self.model_change('clear',lambda m:m['layers'][0]['kind']['children'][0].update(blend='Multiply'))
  with self.assertRaisesRegex(ValueError,'appearance_tree_transition'):self.validate()
 def test_reduce_drops_item_effects(self):
  self.model_change('reduceToBasic',lambda m:m['layers'][0]['kind']['children'][0]['appearance']['items'][0].update(effects=[{'id':'distort.twist','params':{'angle':6},'visible':True}]))
  with self.assertRaisesRegex(ValueError,'appearance_tree_transition'):self.validate()
 def test_remove_duplicate_indices_only_once(self):
  self.model_change('removeItem',lambda m:m['layers'][0]['kind']['children'][0]['appearance']['items'].pop(0))
  with self.assertRaisesRegex(ValueError,'appearance_tree_transition'):self.validate()
 def test_duplicate_copies_nested_effects(self):
  self.model_change('duplicateItem',lambda m:m['layers'][0]['kind']['children'][0]['appearance']['items'][0].pop('effects'))
  with self.assertRaisesRegex(ValueError,'appearance_tree_transition'):self.validate()
 def test_contents_slot_is_persistent(self):
  self.model_change('moveItem',lambda m:m['layers'][1]['appearance'].update(contents_index=2),2)
  with self.assertRaisesRegex(ValueError,'appearance_tree_transition'):self.validate()
 def test_copy_maps_gradient_to_target_bounds(self):
  self.model_change('copyFrom',lambda m:m['layers'][0]['kind']['children'][0]['appearance']['items'][0]['paint']['geom']['end'].update(x=999))
  with self.assertRaisesRegex(ValueError,'appearance_tree_transition'):self.validate()
 def test_transfer_preserves_source_mask(self):
  self.model_change('transfer',lambda m:m['layers'][1]['kind']['children'][0].pop('mask'))
  with self.assertRaisesRegex(ValueError,'appearance_tree_transition'):self.validate()
 def test_transfer_move_clears_source(self):
  self.model_change('transfer',lambda m:m['layers'][1]['kind']['children'][0].update(opacity=.65))
  with self.assertRaisesRegex(ValueError,'appearance_tree_transition'):self.validate()
 def test_active_item_probe_edits_the_actual_row(self):
  self.change('setActiveItem',lambda s:s['observed']['activeProbe']['after']['layers'][0]['kind']['children'][0]['appearance']['items'][2].update(paint={'type':'none'}))
  with self.assertRaisesRegex(ValueError,'appearance_active_probe'):self.validate()
 def test_new_art_actual_object_matches_preference(self):
  self.change('setNewArtBasic',lambda s:s['observed']['newArtProbe']['node'].update(opacity=.1))
  with self.assertRaisesRegex(ValueError,'appearance_new_art_actual'):self.validate()
 def test_probe_restore_must_preserve_document(self):
  self.change('newArt',lambda s:s['observed']['newArtProbe'].update(restored=False))
  with self.assertRaisesRegex(ValueError,'appearance_new_art_actual'):self.validate()
 def test_control_text_cannot_change(self):
  self.model_change('setItem',lambda m:m['layers'][0]['kind']['children'][1]['kind']['runs'][0].update(text='BAD'))
  with self.assertRaisesRegex(ValueError,'appearance_tree_transition'):self.validate()
 def test_target_contents_filters_locked_children(self):
  self.change('targetContents',lambda s:s['observed']['inspect']['selection'].append(999))
  with self.assertRaisesRegex(ValueError,'appearance_contents_selection'):self.validate()
 def test_hidden_effect_stays_hidden_is_rejected(self):
  self.model_change('showAllHidden',lambda m:m['layers'][0]['kind']['children'][0]['appearance']['effects'][0].update(visible=False))
  with self.assertRaisesRegex(ValueError,'appearance_tree_transition'):self.validate()
 def test_native_reopen_preserves_all_rows(self):
  self.change('addStroke',lambda s:s['reopened']['layers'][0]['kind']['children'][0]['appearance']['items'].pop())
  with self.assertRaisesRegex(ValueError,'appearance_reopen'):self.validate()
 def test_window_cannot_be_canvas(self):
  self.change('newArt',lambda s:s['window'].update(width=128,height=96))
  with self.assertRaisesRegex(ValueError,'appearance_window_capture'):self.validate()

 def test_undo_flag_cannot_replace_checkpoint_restoration(self):
  self.change('setActiveItem',lambda s:s['observed']['activeProbe'].update(restoration='undo-only'))
  with self.assertRaisesRegex(ValueError,'appearance_probe_restoration'):self.validate()
 def test_probe_artifacts_require_digests(self):
  self.change('newArt',lambda s:s['observed']['newArtProbe'].update(probeProjectSha256=''))
  with self.assertRaisesRegex(ValueError,'appearance_probe_identity'):self.validate()
