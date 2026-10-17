"""从 portable manifest 生成宿主兼容元数据，不改变产品身份或宣称宿主已验收。"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def generate():
    source=json.loads((ROOT/'plugin.json').read_text())
    base={k:v for k,v in source.items() if k not in {'$schema','extensions'}}
    interface=source.get('extensions',{}).get('com.openai',{}).get('interface',{})
    target={**base,'skills':'./skills/'}
    target.update(source.get('extensions',{}).get('com.openai',{}))
    target['mcpServers']='./.codex-plugin/mcp.json'
    claude={**base,'skills':'./skills/'}
    claude.setdefault('author',{'name':'Full AIGC Plugins','url':'https://github.com/full-aigc-plugins'})
    kimi={**base,'interface':interface,'skills':'./skills/','mcpServers':{name:{**config,'cwd':'./'} for name,config in json.loads((ROOT/'.codex-plugin/mcp.json').read_text())['mcpServers'].items()}}
    panel={**base,'displayName':interface.get('displayName','PdfCraft Use'),'icon':interface.get('logo','./assets/official-logo.png'),'skills':'./skills/','mcpServers':'./.mcp.json'}
    for relative,data in (('.codex-plugin/plugin.json',target),('.claude-plugin/plugin.json',claude),('kimi.plugin.json',kimi),('.zcode-plugin/plugin.json',panel)):
        path=ROOT/relative;path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    return target
if __name__=='__main__':generate()
