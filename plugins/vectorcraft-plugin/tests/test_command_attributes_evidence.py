"""属性命令原生证据拒绝目标、读回、重开及面板像素篡改。"""
import copy,importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];REPORT='docs/evidence/vectorcraft-command-attributes-fixed64-20261009.json'

def payload_source(name):
    """执行载荷收敛在 vectorcraft-harness：沙箱复制的 skills/<domain>/scripts/ 源按字节等价映射。"""
    if isinstance(name, str):
        prefix = 'skills/vectorcraft-'
        if name.startswith(prefix) and '/scripts/' in name and not (ROOT/name).is_file():
            candidate = 'skills/vectorcraft-harness/scripts/' + name.split('/scripts/', 1)[1]
            if (ROOT/candidate).is_file():
                return candidate
    return name

class AttributesEvidenceTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
  for name in (REPORT,'docs/current-identity.json','docs/evidence/vectorcraft-public-tag64-install-20261009.json','skills/vectorcraft-use/references/command-coverage.json',*[f'scripts/qa/{n}.py' for n in ('command_family_window_diagnostic','command_attributes','command_attributes_render','command_layer_render','command_shape','command_paint')]):
   p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(name),p)
  s=importlib.util.spec_from_file_location('attributes_evidence',ROOT/'scripts/verify_command_families.py');self.m=importlib.util.module_from_spec(s);s.loader.exec_module(self.m)
 def stage(self,r,cmd='set',round=1):return next(c['stages'][round-1] for c in r['cases'] if c['command']=='attributes.'+cmd)
 def change(self,fn):
  p=self.root/REPORT;r=json.loads(p.read_text());fn(r);p.write_text(json.dumps(r))
 def model(self,fn,round=1):
  def mutate(r):
   s=self.stage(r,round=round);fn(s);s['reopened']=copy.deepcopy(s['after'])
  self.change(mutate)
 def validate(self):return self.m.validate_family(self.root,'attributes',REPORT)
 def node(self,m,id):
  s=importlib.util.spec_from_file_location('attributes_shape',ROOT/'scripts/qa/command_shape.py');module=importlib.util.module_from_spec(s);s.loader.exec_module(module);return module.find(m,id)
 def test_all_commands(self):self.assertEqual(self.validate(),['attributes.info','attributes.set'])
 def test_changed_count_deduplicates_nodes(self):
  self.change(lambda r:self.stage(r)['returned'].update(changed=99))
  with self.assertRaisesRegex(ValueError,'attributes_return'):self.validate()
 def test_source_metadata(self):
  self.model(lambda s:self.node(s['after'],2)['attrs'].update(note='bad'))
  with self.assertRaisesRegex(ValueError,'attributes_tree'):self.validate()
 def test_group_metadata_stays_on_group(self):
  self.model(lambda s:self.node(s['after'],s['fixture']['state']['children'][0]).update(attrs={'note':'bad'}))
  with self.assertRaisesRegex(ValueError,'attributes_tree'):self.validate()
 def test_character_overprint_changes_with_whole_text(self):
  self.model(lambda s:self.node(s['after'],s['fixture']['state']['text'])['kind']['runs'][0]['style'].pop('overprint_fill'))
  with self.assertRaisesRegex(ValueError,'attributes_tree'):self.validate()
 def test_active_fill_preserves_character_flag(self):
  self.model(lambda s:self.node(s['after'],s['fixture']['state']['text'])['kind']['runs'][0]['style'].pop('overprint_fill'),2)
  with self.assertRaisesRegex(ValueError,'attributes_tree'):self.validate()
 def test_default_attribute_cleanup(self):
  self.model(lambda s:self.node(s['after'],2).update(attrs={'showCenter':True}),2)
  with self.assertRaisesRegex(ValueError,'attributes_tree'):self.validate()
 def test_recent_urls_bound(self):
  self.change(lambda r:self.stage(r,'info')['returned']['recentUrls'].pop())
  with self.assertRaisesRegex(ValueError,'attributes_return'):self.validate()
 def test_mixed_readback_is_null(self):
  self.change(lambda r:self.stage(r,'info')['returned'].update(overprintFill=True))
  with self.assertRaisesRegex(ValueError,'attributes_return'):self.validate()
 def test_item_stroke_readback_is_null(self):
  self.change(lambda r:self.stage(r,'info',2)['returned'].update(overprintStroke=False))
  with self.assertRaisesRegex(ValueError,'attributes_return'):self.validate()
 def test_reopen_preserves_attrs(self):
  self.change(lambda r:self.node(self.stage(r)['reopened'],2).pop('attrs'))
  with self.assertRaisesRegex(ValueError,'attributes_reopen'):self.validate()
 def test_local_revision_preserves_other_fields(self):
  self.change(lambda r:self.stage(r,round=2)['fixture'].update(revisionName='bad'))
  with self.assertRaisesRegex(ValueError,'attributes_local_revision'):self.validate()
 def test_control_text_is_preserved(self):
  self.model(lambda s:self.node(s['after'],3)['kind']['runs'][0].update(text='bad'))
  with self.assertRaisesRegex(ValueError,'attributes_tree'):self.validate()
 def test_svg_href_matches_model(self):
  self.change(lambda r:self.stage(r)['observed']['svgLinks'].pop())
  with self.assertRaisesRegex(ValueError,'attributes_svg_links'):self.validate()
 def test_decoded_svg_hash_is_bound(self):
  self.change(lambda r:r['renderChanges']['svgLinkChecks'][0].update(sha256='0'*64))
  with self.assertRaisesRegex(ValueError,'attributes_svg_binding'):self.validate()
 def test_panel_must_be_attributes(self):
  self.change(lambda r:self.stage(r)['ui']['ui'].update(open_panel=None))
  with self.assertRaisesRegex(ValueError,'attributes_panel_state'):self.validate()
 def test_checkbox_hash_is_bound(self):
  self.change(lambda r:r['renderChanges']['checkboxChecks'][0].update(windowSha256='0'*64))
  with self.assertRaisesRegex(ValueError,'attributes_checkbox_binding'):self.validate()
 def test_mixed_checkbox_has_dash(self):
  self.change(lambda r:r['renderChanges']['checkboxChecks'][0].update(dashPixels=0))
  with self.assertRaisesRegex(ValueError,'attributes_checkbox_state'):self.validate()
 def test_checked_checkbox_has_blue_pixels(self):
  self.change(lambda r:r['renderChanges']['checkboxChecks'][1].update(bluePixels=0))
  with self.assertRaisesRegex(ValueError,'attributes_checkbox_state'):self.validate()
 def test_unchecked_checkbox_has_no_dash(self):
  self.change(lambda r:r['renderChanges']['checkboxChecks'][-1].update(dashPixels=14))
  with self.assertRaisesRegex(ValueError,'attributes_checkbox_state'):self.validate()
