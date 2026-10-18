"""字体/许可漂移必须在修改源码副本前拒绝。"""
import hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class FontOverlayContract(unittest.TestCase):
    def fixture(self,root):
        spec=importlib.util.spec_from_file_location('font_overlay',ROOT/'ui/prepare-cjk-font.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
        ui=root/'ui';ui.mkdir();m.__file__=str(ui/'prepare-cjk-font.py');fonts=root/'inputs';(fonts/'fonts').mkdir(parents=True);entries=[]
        for name,value in [('LXGWWenKai-Regular.ttf',b'font fixture'),('OFL-LXGWWenKai.txt',b'license fixture')]:
            (fonts/'fonts'/name).write_bytes(value);entries.append({'file':'fonts/'+name,'bytes':len(value),'sha256':hashlib.sha256(value).hexdigest()})
        (ui/'fonts.lock.json').write_text(json.dumps({'files':entries}),encoding='utf-8');source=root/'source';target=source/'crates/ui-egui/src/fonts.rs';target.parent.mkdir(parents=True);target.write_text('fn definitions() {\n    let fonts = defaults();\n    fonts\n}\n',encoding='utf-8')
        return m,source,fonts,target
    def test_fallback_append_license_and_repeat_refusal(self):
        with tempfile.TemporaryDirectory() as t:
            m,source,fonts,target=self.fixture(Path(t));m.prepare(source,fonts)
            self.assertIn('family.push("craft-cjk-fallback".into())',target.read_text(encoding='utf-8'))
            self.assertEqual((source/'assets/craft-fonts/OFL-LXGWWenKai.txt').read_bytes(),b'license fixture')
            with self.assertRaisesRegex(ValueError,'already applied'):m.prepare(source,fonts)
    def test_changed_license_preserves_source(self):
        with tempfile.TemporaryDirectory() as t:
            m,source,fonts,target=self.fixture(Path(t));before=target.read_bytes();(fonts/'fonts/OFL-LXGWWenKai.txt').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'differs'):m.prepare(source,fonts)
            self.assertEqual(target.read_bytes(),before);self.assertFalse(target.with_name('craft_cjk.ttf').exists())
if __name__=='__main__':unittest.main()
