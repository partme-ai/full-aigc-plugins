#!/usr/bin/env python3
"""验证插件入口可重定位，且不依赖其他产品的专用宿主配置。"""
from pathlib import Path
import argparse,json,re
p=argparse.ArgumentParser();p.add_argument('--repositories',type=Path,required=True);a=p.parse_args()
names='cadcraft designcraft effectcraft photocraft figcraft filmcraft lightcraft printcraft vectorcraft deckcraft soundcraft gridcraft wordcraft'.split();errors=[]
for n in names:
 root=a.repositories/(n+'-plugin');key=n+'-editor'
 try:
  configs=[('mcp.json','${PLUGIN_ROOT}/ui/dist/adapter.mjs',None),('.mcp.json','${CLAUDE_PLUGIN_ROOT}/ui/dist/adapter.mjs',None),('.codex-plugin/mcp.json','ui/dist/adapter.mjs','.')]
  for file,arg,cwd in configs:
   c=json.loads((root/file).read_text())['mcpServers'][key]
   assert c['command']=='node' and c['args']==[arg],file
   assert c.get('cwd')==cwd,file
   assert not re.search(r'/Users/|/home/|[A-Z]:\\',json.dumps(c)),file
  c=json.loads((root/'.codex-plugin/plugin.json').read_text());assert c['mcpServers']=='./.codex-plugin/mcp.json'
  c=json.loads((root/'.claude-plugin/plugin.json').read_text());assert c['name']==n and c['skills']=='./skills/'
  assert {p.name for p in root.glob('.*-plugin') if p.is_dir()} <= {'.codex-plugin','.claude-plugin','.zcode-plugin'},'obsolete host directory'
 except (OSError,KeyError,AssertionError) as e:errors.append(f'{n}: {e}')
if errors:raise SystemExit('\n'.join(errors))
print('13 portable/Codex/Claude entry sets valid')
