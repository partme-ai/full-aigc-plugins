#!/usr/bin/env python3
"""从可移植身份同步薄宿主清单，保留宿主已有扩展。"""
import argparse,json
from pathlib import Path
NAMES='cadcraft designcraft effectcraft photocraft figcraft filmcraft lightcraft printcraft vectorcraft deckcraft soundcraft gridcraft wordcraft'.split()
def sync(root):
 base=json.loads((root/'plugin.json').read_text())
 interface=base.get('extensions',{}).get('com.openai',{}).get('interface',{})
 def existing(p):
  return json.loads((root/p).read_text()) if (root/p).exists() else {k:v for k,v in base.items() if k not in ('$schema','extensions')}
 for path in ['.codex-plugin/plugin.json','.claude-plugin/plugin.json','.zcode-plugin/plugin.json','kimi.plugin.json']:
  data=existing(path);data.update(name=base['name'],version=base['version'],skills='./skills/')
  if path.startswith('.codex'):data['mcpServers']='./.codex-plugin/mcp.json'
  if path.startswith('.zcode'):
   data.update(displayName=interface.get('displayName',base['name']),icon=interface.get('logo','./assets/official-logo.png'),mcpServers='./.mcp.json')
  if path=='kimi.plugin.json':
   data.setdefault('interface',interface)
   servers=json.loads((root/'.codex-plugin/mcp.json').read_text())['mcpServers']
   data['mcpServers']={**data.get('mcpServers',{}),**{name:{**config,'cwd':'./'} for name,config in servers.items()}}
  dest=root/path;dest.parent.mkdir(exist_ok=True);dest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repositories',type=Path,required=True);a=p.parse_args()
 for name in NAMES:sync(a.repositories/(name+'-plugin'))
 print('13 native adapter sets synchronized')
