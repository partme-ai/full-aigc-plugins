#!/usr/bin/env python3
"""将独立候选 ZIP 组合为相对路径本地市场；不安装或改写宿主配置。"""
from pathlib import Path
import argparse,json,zipfile,hashlib,stat
p=argparse.ArgumentParser();p.add_argument('--archives',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
if a.output.exists():raise SystemExit('Refusing existing output directory')
entries=json.loads((a.archives/'index.json').read_text());a.output.mkdir(parents=True);plugins=a.output/'plugins';plugins.mkdir()
codex=[];claude=[];kimi=[]
for entry in entries:
 name=entry['plugin'];source='./plugins/'+name+'-plugin'
 archive=a.archives/entry['file']
 if hashlib.sha256(archive.read_bytes()).hexdigest()!=entry['sha256']:raise ValueError('archive digest mismatch')
 with zipfile.ZipFile(archive) as z:
  if z.testzip():raise ValueError('corrupt archive')
  for item in z.infolist():
   target=(plugins/item.filename).resolve()
   if not target.is_relative_to(plugins.resolve()) or stat.S_ISLNK(item.external_attr >> 16):raise ValueError('unsafe archive member')
  z.extractall(plugins)
  for item in z.infolist():
   if not item.is_dir() and item.external_attr >> 16:
    (plugins/item.filename).chmod((item.external_attr >> 16) & 0o777)
 codex.append({'name':name,'source':{'source':'local','path':source},'policy':{'installation':'AVAILABLE','authentication':'ON_INSTALL'},'category':'Creativity'})
 claude.append({'name':name,'source':source})
 kimi.append({'id':name,'displayName':json.loads((plugins/(name+'-plugin')/'plugin.json').read_text())['extensions']['com.openai']['interface']['displayName'],'source':source})
for path,data in [('kimi.marketplace.json',{'version':'2','plugins':kimi}),('.zcode-plugin/marketplace.json',{'name':'craft-use-local','owner':{'name':'Full AIGC Plugins'},'plugins':claude}),('.agents/plugins/marketplace.json',{'name':'craft-use-local','plugins':codex}),('.claude-plugin/marketplace.json',{'name':'craft-use-local','owner':{'name':'Full AIGC Plugins'},'metadata':{'description':'13 Craft Use editor plugins with same-session MCP and scenario skills.'},'plugins':claude})]:
 dest=a.output/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(a.output/'README.md').write_text('''# Craft Use 本地插件市场

整个目录可以搬迁，插件源均相对于本市场根目录。需要 Node.js 24+；编辑器、官方图标及场景技能已包含。

在 Claude Code 中，通过 `/plugin marketplace add` 添加本目录，再用 `/plugin install photocraft@craft-use-local` 安装所需插件。市场目录的位置只需提供一次，不需要给每个 MCP 手写本机路径。

在支持本地插件市场的 Codex 中添加本目录作为市场根，选择所需插件。市场入口为 `.agents/plugins/marketplace.json`。安装后重载插件；当前包仍是本地开发候选，未发布到公共市场。

支持标准 Agent Plugins 的宿主使用各插件根的 `plugin.json` 和 `mcp.json`。各宿主入口适配不同路径解析约定，不能互相复制配置文件冒充原生安装。

ZCode 使用 `plugins marketplace add` 添加本目录，再用 `plugins install photocraft@craft-use-local` 安装。Kimi 使用 `/plugins install <本市场目录>/plugins/photocraft-plugin`；安装后新建会话或重连 MCP。`kimi.marketplace.json` 提供 Kimi v2 市场索引。终端命令名称及可执行路径取决于宿主安装方式。

CADCraft、DeckCraft 默认启动包内编辑器 MCP；需要外部 CLI 服务时，先安装相应 CLI，再采用 `hosts/native-cli/mcp.json` 的可选配置。

打开编辑器时显式指定用户任务的 workspace；安装目录不会自动成为任务目录。内置界面依赖宿主提供 MCP Apps 或浏览器面板，终端宿主不能仅凭 stdio 显示编辑器。
''')
print(f'{len(entries)} plugins packaged at {a.output}')
