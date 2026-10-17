"""旧版和main字体后备表均须保留中文后备且数组长度正确。"""
import pathlib, subprocess, tempfile, unittest
SCRIPT=pathlib.Path(__file__).resolve().parents[1]/'runtime/prepare-fonts.py'
class FontOverlayTest(unittest.TestCase):
 def apply(self,text):
  with tempfile.TemporaryDirectory() as tmp:
   root=pathlib.Path(tmp);p=root/'crates/text/src/fontdb.rs';p.parent.mkdir(parents=True);p.write_text(text)
   ui=root/'crates/ui-egui/src';ui.mkdir(parents=True);(ui/'lib.rs').write_text('fn init(ctx: &egui::Context) { ctx.set_fonts(egui::FontDefinitions::default()); }')
   r=subprocess.run(['python3',str(SCRIPT),str(root),'figcraft'],capture_output=True,text=True)
   self.assertEqual(r.returncode,0,r.stderr);return p.read_text()
 def test_main_sized_fallback_table(self):
  out=self.apply('const FALLBACK_FAMILIES: [&str; 2] = [\n    "Inter",\n    "Noto Sans",\n];\n')
  self.assertIn('[&str; 3]',out);self.assertEqual(out.count('"LXGW WenKai"'),1)
 def test_old_inline_fallbacks(self):
  out=self.apply('        for fam in [\n            "Inter",\n            "Noto Sans",\n        ] {}\n')
  self.assertIn('"LXGW WenKai",\n            "Noto Sans"',out)
if __name__=='__main__':unittest.main()
