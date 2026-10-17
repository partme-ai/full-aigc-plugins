#!/usr/bin/env python3
"""只更新轻量MCP入口并复用已核验的运行资源，不重写既有标签。"""
from pathlib import Path
import json,hashlib,shutil,argparse
ROOT=Path(__file__).resolve().parents[1]
VERSION='0.1.0-dev.20261017.3'
def write(p,j):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('previous',type=Path);parser.add_argument('output',type=Path);a=parser.parse_args();a.output.mkdir(exist_ok=False);rows=[]
 for old in json.loads((a.previous/'index.json').read_text()):
  n=old['plugin'];repo=ROOT.parent/'full-aigc-plugins-repositories'/(n+'-plugin')
  for rel in ['plugin.json','.codex-plugin/plugin.json','.zcode-plugin/plugin.json','.claude-plugin/plugin.json','kimi.plugin.json','package.json']:
   p=repo/rel
   if p.exists():v=json.loads(p.read_text());v['version']=VERSION;write(p,v)
  p=repo/'.codex-plugin/mcp.json';v=json.loads(p.read_text())
  for server in v['mcpServers'].values():server.pop('startup_timeout_sec',None)
  write(p,v)
  p=repo/'.agents/plugins/marketplace.json'
  if p.exists():
   v=json.loads(p.read_text());e=v['plugins'][0];e['version']=VERSION;e['source']['ref']='v'+VERSION;logo=f'https://cdn.jsdelivr.net/gh/full-aigc-plugins/{n}-plugin@v{VERSION}/assets/official-logo.png';e['icon']=logo;e['interface']['logo']=logo;write(p,v)
  shutil.copy2(ROOT/'scripts/templates/craft-runtime-bootstrap.mjs',repo/'ui/bootstrap.mjs');p=repo/'ui/runtime.lock.json';v=json.loads(p.read_text());v['version']=VERSION;v['catalogSha256']=hashlib.sha256((repo/'ui/catalog.lock.json').read_bytes()).hexdigest();write(p,v)
  p=repo/'docs/verification/release-candidate.json';v=json.loads(p.read_text());v['currentVersion']=VERSION;v['releaseTag']='v'+VERSION;write(p,v)
  for rel in ['README.md','README.zh-CN.md']:
   p=repo/rel
   if p.exists():p.write_text(p.read_text().replace('`0.1.0-dev.20261017.2` is distributed','`'+VERSION+'` is distributed')+'\n### 候选启动修正\n\n本候选先完成轻量MCP握手及能力发现，在首次工具或资源调用时校验/获取固定编辑器资源。修复多个编辑器首次下载阻塞宿主握手的问题。Windows通过Git安装时须启用Git长路径支持（`git config --global core.longpaths true`）；完整ZIP不包含历史验收记录，可避免Git检出长路径的问题。运行资源沿用已核验的dev.20261017.2制品，不以入口版本号冒充上游升级。\n')
  rows.append({**old,'version':VERSION,'runtimeRef':'v'+old['version'],'reuseRuntime':True})
 write(a.output/'index.json',rows)
 catalog=json.loads((ROOT/'catalog.json').read_text())
 for c in catalog['candidatePlugins']:
  if c['id'] in {r['plugin'] for r in rows}:c['version']=VERSION
 write(ROOT/'catalog.json',catalog)
 print('Prepared 13 lazy-handshake candidates; runtime resources reused')
