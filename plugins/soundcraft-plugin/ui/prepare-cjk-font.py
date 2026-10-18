"""仅对独立构建副本注入可再分发中文后备；不读系统字体、不改上游仓库。"""
import argparse
import hashlib
import json
from pathlib import Path


def prepare(source,fonts):
    ui=Path(__file__).resolve().parent
    lock=json.loads((ui/'fonts.lock.json').read_text(encoding='utf-8'))
    checked={}
    for entry in lock['files']:
        path=fonts/entry['file'];data=path.read_bytes()
        if len(data)!=entry['bytes'] or hashlib.sha256(data).hexdigest()!=entry['sha256']:
            raise ValueError('Font or license differs from locked source: '+entry['file'])
        checked[entry['file']]=data
    target=source/'crates/ui-egui/src/fonts.rs';text=target.read_text(encoding='utf-8')
    anchor='    fonts\n}'
    if text.count(anchor)!=1 or 'craft-cjk-fallback' in text:
        raise ValueError('Font overlay anchor changed or overlay already applied')
    code='''    // 插件构建副本的中文后备；保留既有拉丁字形和桌面字体优先级。
    #[cfg(target_arch = "wasm32")]
    {
        fonts.font_data.insert("craft-cjk-fallback".into(), Arc::new(FontData::from_static(include_bytes!("craft_cjk.ttf"))));
        for family in fonts.families.values_mut() {
            family.push("craft-cjk-fallback".into());
        }
    }
    fonts
}'''
    font=target.with_name('craft_cjk.ttf')
    if font.exists():raise ValueError('Refusing existing font build input')
    notices=source/'assets/craft-fonts';notices.mkdir(parents=True,exist_ok=True)
    (notices/'OFL-LXGWWenKai.txt').write_bytes(checked['fonts/OFL-LXGWWenKai.txt'])
    font.write_bytes(checked['fonts/LXGWWenKai-Regular.ttf'])
    target.write_text(text.replace(anchor,code),encoding='utf-8')
    return {'fontSha256':lock['files'][0]['sha256'],'families':'all existing families, appended fallback','scope':'wasm32 build copy only'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--fonts',type=Path,required=True);a=p.parse_args()
    print(json.dumps(prepare(a.source.resolve(),a.fonts.resolve())))
