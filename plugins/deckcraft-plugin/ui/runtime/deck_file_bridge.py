"""在隔离副本接入DeckCraft旧版与main的浏览器文件入口。"""
from pathlib import Path


def patch_files(root, replace):
    root = Path(root)
    path = 'crates/engine/src/cmd/file.rs'
    replace(path, '#[cfg(not(target_arch = "wasm32"))]\nfn open(s: &mut Session, p: &Value) -> Result<Value> {',
            'fn open(s: &mut Session, p: &Value) -> Result<Value> {')
    replace(path, '#[cfg(target_arch = "wasm32")]\nfn open(_s: &mut Session, _p: &Value) -> Result<Value> {\n    Err(EngineError::Other("use file.openBytes in the browser".into()))\n}\n', '')
    if 'crate::io::write_file(path, bytes).map_err(EngineError::Other)' in (root / path).read_text():
        # main把所有按路径读写汇聚到io模块；只替换WASM分支，保留原生权限与原子写入。
        replace(path, '#[cfg(not(target_arch = "wasm32"))]\npub fn read_presentation_file(',
                'pub fn read_presentation_file(')
        io = 'crates/engine/src/io.rs'
        replace(io, 'Err(format!("{path}: files are opened through the browser on the web"))',
                'crate::craft_fs::read(path).map_err(|e| format!("{path}: {e}"))')
        replace(io, 'pub fn write_file(path: &str, _bytes: &[u8])',
                'pub fn write_file(path: &str, bytes: &[u8])')
        replace(io, 'Err(format!("{path}: saving to a path is not available in the browser"))',
                'crate::craft_fs::write(path, bytes).map_err(|e| format!("{path}: {e}"))')
        replace(io, 'pub fn file_len(_path: &str) -> Option<u64> {\n    None\n}',
                'pub fn file_len(path: &str) -> Option<u64> {\n    crate::craft_fs::read(path).ok().map(|bytes| bytes.len() as u64)\n}')
    else:
        replace(path, 'fn write_file(_path: &str, _bytes: &[u8]) -> Result<()> {\n    Err(EngineError::Other("saving to a path is not available in the browser".into()))\n}',
                'fn write_file(path: &str, bytes: &[u8]) -> Result<()> {\n    crate::craft_fs::write(path, bytes).map_err(|e| EngineError::Other(format!("{path}: {e}")))\n}')
