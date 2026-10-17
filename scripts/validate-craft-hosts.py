#!/usr/bin/env python3
"""检查三个原生入口及版本一致性；本脚本不声称完成真实安装。"""
from pathlib import Path
import argparse,json
p=argparse.ArgumentParser();p.add_argument('--repositories',type=Path,required=True);a=p.parse_args()
names='cadcraft designcraft effectcraft photocraft figcraft filmcraft lightcraft printcraft vectorcraft deckcraft soundcraft gridcraft wordcraft'.split();errors=[]
for n in names:
 r=a.repositories/(n+'-plugin');base=json.loads((r/'plugin.json').read_text())
 if n not in {'effectcraft','filmcraft','lightcraft'}:
  try:
   meta=json.loads((r/'.zcode-plugin/panel-meta.json').read_text())
   assert meta == {'zcode/csp':{'wasmUnsafeEval':True}},'missing WASM panel capability'
   entry=json.loads((r/'.mcp.json').read_text())['mcpServers'][n+'-editor']
   assert entry['env']['CRAFT_PANEL_METADATA_FILE']=='${CLAUDE_PLUGIN_ROOT}/.zcode-plugin/panel-meta.json','host metadata path missing'
  except (OSError,KeyError,AssertionError) as e:errors.append(f'{n}: panel metadata: {e}')
 for file in ['.codex-plugin/plugin.json','.zcode-plugin/plugin.json','kimi.plugin.json','.claude-plugin/plugin.json']:
  try:
   d=json.loads((r/file).read_text());assert d['name']==base['name'] and d['version']==base['version'],'identity/version mismatch'
   if file=='kimi.plugin.json':
    c=d['mcpServers'][n+'-editor'];assert c['command']=='node' and c['args']==['ui/bootstrap.mjs'] and c['cwd']=='./','nonportable editor MCP'
   if file=='.zcode-plugin/plugin.json':assert d['mcpServers']=='./.mcp.json','editor MCP missing'
  except (OSError,KeyError,AssertionError) as e:errors.append(f'{n}: {file}: {e}')
if errors:raise SystemExit('\n'.join(errors))
print('13 host adapter sets and versions valid')
