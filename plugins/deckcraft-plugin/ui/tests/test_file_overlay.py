"""验证main集中式文件模块保留native权限检查，浏览器使用显式文件字节。"""
from pathlib import Path
import importlib.util
import tempfile
import unittest
spec = importlib.util.spec_from_file_location('bridge', Path(__file__).resolve().parents[1] / 'runtime/deck_file_bridge.py')
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


class FileOverlayTest(unittest.TestCase):
    def test_legacy_inline_writer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            p = root / 'crates/engine/src/cmd/file.rs'
            p.parent.mkdir(parents=True)
            p.write_text('''#[cfg(not(target_arch = "wasm32"))]
fn open(s: &mut Session, p: &Value) -> Result<Value> {}
#[cfg(target_arch = "wasm32")]
fn open(_s: &mut Session, _p: &Value) -> Result<Value> {
    Err(EngineError::Other("use file.openBytes in the browser".into()))
}
fn write_file(_path: &str, _bytes: &[u8]) -> Result<()> {
    Err(EngineError::Other("saving to a path is not available in the browser".into()))
}''')
            def replace(name, old, new):
                path = root / name
                text = path.read_text()
                self.assertEqual(text.count(old), 1)
                path.write_text(text.replace(old, new, 1))
            bridge.patch_files(root, replace)
            self.assertIn('crate::craft_fs::write(path, bytes)', p.read_text())
            self.assertNotIn('fn open(_s:', p.read_text())

    def test_main_io(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            file = root / 'crates/engine/src/cmd/file.rs'
            file.parent.mkdir(parents=True)
            file.write_text('''#[cfg(not(target_arch = "wasm32"))]
fn open(s: &mut Session, p: &Value) -> Result<Value> {}
#[cfg(target_arch = "wasm32")]
fn open(_s: &mut Session, _p: &Value) -> Result<Value> {
    Err(EngineError::Other("use file.openBytes in the browser".into()))
}
#[cfg(not(target_arch = "wasm32"))]
pub fn read_presentation_file(path: &str) {}
crate::io::write_file(path, bytes).map_err(EngineError::Other)
''')
            io = file.parent.parent / 'io.rs'
            io.write_text('''#[cfg(not(target_arch = "wasm32"))]
fn native_write() { crate::file_access::check_write(path)?; }
#[cfg(target_arch = "wasm32")]
pub fn read_file(path: &str) -> Result<Vec<u8>, String> {
    Err(format!("{path}: files are opened through the browser on the web"))
}
#[cfg(target_arch = "wasm32")]
pub fn write_file(path: &str, _bytes: &[u8]) -> Result<(), String> {
    Err(format!("{path}: saving to a path is not available in the browser"))
}
pub fn file_len(_path: &str) -> Option<u64> {
    None
}
''')
            def replace(name, old, new):
                p = root / name
                text = p.read_text()
                self.assertEqual(text.count(old), 1)
                p.write_text(text.replace(old, new, 1))
            bridge.patch_files(root, replace)
            out = io.read_text()
            self.assertIn('crate::file_access::check_write(path)?;', out)
            self.assertIn('crate::craft_fs::read(path)', out)
            self.assertIn('crate::craft_fs::write(path, bytes)', out)
            self.assertIn('bytes.len() as u64', out)
            self.assertNotIn('fn open(_s:', file.read_text())
            self.assertNotIn('#[cfg(not(target_arch = "wasm32"))]\npub fn read_presentation_file', file.read_text())


if __name__ == '__main__':
    unittest.main()
