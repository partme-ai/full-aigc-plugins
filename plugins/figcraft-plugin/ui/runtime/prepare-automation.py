# Modified by Full AIGC Plugins: tolerate upstream OPENABLE already available on Web.
"""Apply the versioned live-editor overlay to an extracted, pinned upstream tree."""
from pathlib import Path
import sys
import re

runtime = Path(__file__).resolve().parent
root = Path(sys.argv[1])
name = sys.argv[2]

def replace(path, old, new):
    p = root / path
    s = p.read_text()
    if old not in s:
        raise RuntimeError(f'{name}: overlay anchor absent: {path}: {old[:100]}')
    p.write_text(s.replace(old, new, 1))

def dependency(path, key, value):
    p = root / path
    s = p.read_text()
    if re.search(r'^' + re.escape(key) + r'\s*=', s, re.M):
        return
    marker = '[target.\'cfg(target_arch = "wasm32")\'.dependencies]'
    line = f'{key} = {value}\n'
    if marker in s:
        s = s.replace(marker, marker + '\n' + line, 1)
    else:
        s += '\n' + marker + '\n' + line
    p.write_text(s)

def file_bridge():
    # Keep native behavior intact. Browser reads/writes can only access bytes explicitly
    # provided for the current MCP operation, and all outputs are committed by the host.
    for crate in (root/'crates').iterdir():
        lib = crate/'src/lib.rs'
        if not lib.exists():
            continue
        changed = False
        for p in (crate/'src').rglob('*.rs'):
            s = p.read_text()
            new = re.sub(r'std::fs::(read_to_string|read|write|create_dir_all)\(', r'crate::craft_fs::\1(', s)
            if new != s:
                p.write_text(new)
                changed = True
        if changed:
            lib.write_text(lib.read_text()+'\n#[allow(unused_imports, dead_code)]\npub(crate) mod craft_fs;\n')
            (crate/'src/craft_fs.rs').write_text((runtime/'rust/fs.rs').read_text())
            dependency(str(crate.relative_to(root)/'Cargo.toml'),'wasm-bindgen','"0.2"')
            dependency(str(crate.relative_to(root)/'Cargo.toml'),'js-sys','"0.3"')

file_bridge()
if name != 'figcraft': raise RuntimeError('This overlay requires FigCraft')
path='crates/engine/src/cmd/file.rs'
replace(path, 'Err(EngineError::Other(format!("{path}: no file system in the browser")))', 'crate::craft_fs::read(path).map_err(|e| EngineError::Other(e.to_string()))')
replace(path, 'pub(crate) fn write(path: &str, _bytes: &[u8])', 'pub(crate) fn write(path: &str, bytes: &[u8])')
replace(path, 'Err(EngineError::Other(format!("{path}: no file system in the browser")))', 'crate::craft_fs::write(path,bytes).map_err(|e| EngineError::Other(e.to_string()))')
# Browser capped reads validate staged bytes rather than native filesystem metadata.
replace(path, 'pub(crate) fn read_capped(path: &str, max: u64) -> Result<Vec<u8>> {', '#[cfg(not(target_arch = "wasm32"))]\npub(crate) fn read_capped(path: &str, max: u64) -> Result<Vec<u8>> {')
p=root/path;p.write_text(p.read_text()+'''\n#[cfg(target_arch = "wasm32")]
/// 从宿主暂存区读取文件，并检查最大字节数。
pub(crate) fn read_capped(path: &str, max: u64) -> Result<Vec<u8>> {
 let bytes=read(path)?;
 if bytes.len() as u64 > max { return Err(EngineError::Other("Staged input too large".into())); }
 Ok(bytes)
}
''')
for key,value in [('figcraft-mcp','{ path = "../mcp" }'),('wasm-bindgen','"0.2"'),('js-sys','"0.3"')]:dependency('crates/ui-egui/Cargo.toml',key,value)
ui='crates/ui-egui/src/lib.rs'
replace(ui,'pub mod control;','#[cfg(target_arch = "wasm32")]\nmod craft_bridge;\npub mod control;')
anchor='pub fn logic(&mut self, ctx: &egui::Context) {'
replace(ui,anchor,anchor+'\n #[cfg(target_arch = "wasm32")]\n craft_bridge::pump(self,ctx);')
template=(runtime/'rust/bridge.rs.in').read_text()
for key,value in {'APP':'FigApp','BUSY':'!app.control_input.is_empty()','MCP':'figcraft_mcp','CATALOG':'serde_json::json!(figcraft_mcp::tool_definitions())','CONTROL':'crate::control::handle(self.app,self.ctx,method,&params)','CALL':'figcraft_mcp::call_tool(&mut backend,name,&args).to_value()','SERVICES_BEGIN':'','SERVICES_END':''}.items():template=template.replace('__'+key+'__',value)
# Native Backend defaults use OS temporary paths; return engine bytes directly on Web.
anchor='    fn has_ui(&self) -> bool { true }'
addition='''
    fn render_png(&mut self, ids: &[u64], scale: f64) -> Result<Vec<u8>, String> {
        let ids = if ids.is_empty() { figcraft_mcp::page_children(self)? } else { ids.to_vec() };
        let result=self.app.session.execute("file.export", &json!({"format":"png","scale":scale,"ids":ids})).map_err(|e|e.to_string())?;
        figcraft_mcp::decode_data(&result)
    }
    fn screenshot_png(&mut self) -> Result<Vec<u8>, String> {
        use base64::Engine as _;
        let data=host_screenshot().map_err(|e|format!("{e:?}"))?;
        base64::engine::general_purpose::STANDARD.decode(data).map_err(|e|e.to_string())
    }
'''
template=template.replace(anchor,anchor+addition).replace('Craft live WASM editor','Full AIGC live WASM editor')
(root/'crates/ui-egui/src/craft_bridge.rs').write_text(template)
