#!/usr/bin/env python3
"""生成 13 款 Craft stdio MCP 的宿主配置；不安装插件、不修改宿主设置。"""
import argparse,json,pathlib,shutil
p=argparse.ArgumentParser();p.add_argument('--repositories',type=pathlib.Path,required=True);p.add_argument('--workspace',type=pathlib.Path,required=True);p.add_argument('--host',choices=['codex','workbuddy'],required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
workspace=a.workspace.resolve(strict=True)
if not workspace.is_dir():p.error('workspace must be a directory')
node=shutil.which('node')
if not node:p.error('Node.js 24+ required')
names='cadcraft designcraft effectcraft photocraft figcraft filmcraft lightcraft printcraft vectorcraft deckcraft soundcraft gridcraft wordcraft'.split();servers={}
for n in names:
 entry=(a.repositories/(n+'-plugin')/'ui/dist/adapter.mjs').resolve(strict=True)
 servers[n+'-editor']={'type':'stdio','command':node,'args':[str(entry)],'cwd':str(workspace),'env':{'CRAFT_WORKSPACE_ROOT':str(workspace)}}
if a.host=='workbuddy':text=json.dumps({'mcpServers':servers},ensure_ascii=False,indent=2)+'\n'
else:
 lines=[];q=lambda v:json.dumps(v,ensure_ascii=False)
 for name,s in servers.items():
  lines.extend([f'[mcp_servers.{q(name)}]',f'command = {q(node)}',f'args = [{q(s["args"][0])}]',f'cwd = {q(str(workspace))}','tool_timeout_sec = 180',f'[mcp_servers.{q(name)}.env]',f'CRAFT_WORKSPACE_ROOT = {q(str(workspace))}',''])
 text='\n'.join(lines)
a.output.parent.mkdir(parents=True,exist_ok=True)
with a.output.open('x') as f:f.write(text)
print(a.output)
