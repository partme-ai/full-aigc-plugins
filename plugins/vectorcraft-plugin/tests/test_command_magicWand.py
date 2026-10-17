"""魔棒设置独立契约：默认值、参数合并和上下界。"""
import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class WandTests(unittest.TestCase):
 def setUp(self):
  p=ROOT/'scripts/qa/command_magicWand.py';self.assertTrue(p.exists(),'wand_contract_missing');s=importlib.util.spec_from_file_location('wand',p);self.m=importlib.util.module_from_spec(s);s.loader.exec_module(self.m)
 def test_defaults(self):self.assertEqual(self.m.DEFAULT,dict(fillColor=True,fillTolerance=32.,strokeColor=False,strokeTolerance=32.,strokeWeight=False,weightTolerance=5.,opacity=False,opacityTolerance=5.,blendingMode=False))
 def test_merge_preserves_omitted_settings(self):
  b={**self.m.DEFAULT,'strokeColor':True};a=self.m.expected(b,{'fillTolerance':12});self.assertTrue(a['strokeColor']);self.assertEqual(a['fillTolerance'],12);self.assertEqual(b['fillTolerance'],32)
 def test_reset_then_override(self):
  a=self.m.expected({**self.m.DEFAULT,'opacity':True},{'reset':True,'strokeColor':True});self.assertFalse(a['opacity']);self.assertTrue(a['strokeColor'])
 def test_all_clamps(self):
  a=self.m.expected(self.m.DEFAULT,dict(fillTolerance=-2,strokeTolerance=300,weightTolerance=1200,opacityTolerance=-1));self.assertEqual([a[k] for k in ('fillTolerance','strokeTolerance','weightTolerance','opacityTolerance')],[0,255,1000,0])
 def test_fractional_values(self):self.assertEqual(self.m.expected(self.m.DEFAULT,{'weightTolerance':3.75})['weightTolerance'],3.75)
 def test_unknown_key_ignored(self):self.assertEqual(self.m.expected(self.m.DEFAULT,{'ignored':True}),self.m.DEFAULT)
 def test_wrong_boolean_type_rejected(self):
  with self.assertRaises(ValueError):self.m.expected(self.m.DEFAULT,{'fillColor':1})
 def test_wrong_numeric_type_rejected(self):
  with self.assertRaises(ValueError):self.m.expected(self.m.DEFAULT,{'fillTolerance':True})
if __name__=='__main__':unittest.main()
