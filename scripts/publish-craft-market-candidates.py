#!/usr/bin/env python3
"""发布已准备好的13个开发候选；不修改既有标签或既有发行资源。"""
from pathlib import Path
import json,subprocess,shutil,zipfile,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
def call(args,cwd=None):
 r=subprocess.run(args,cwd=cwd,capture_output=True,text=True,timeout=900)
 if r.returncode:raise RuntimeError(str(args[:3])+': '+r.stdout+r.stderr)
 return r.stdout.strip()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('release_directory',type=Path);args=parser.parse_args();out=args.release_directory.resolve();rows=json.loads((out/'index.json').read_text());reports=[]
 for row in rows:
  name=row['plugin'];repo=ROOT.parent/'full-aigc-plugins-repositories'/(name+'-plugin');tag='v'+row['version'];remote='full-aigc-plugins/'+name+'-plugin'
  if call(['git','ls-remote','origin','refs/tags/'+tag],repo):raise RuntimeError('Refusing to replace existing '+tag+' '+name)
  call(['git','diff','--check'],repo)
  call(['git','add','plugin.json','mcp.json','.mcp.json','.codex-plugin','.zcode-plugin','kimi.plugin.json','ui/bootstrap.mjs','ui/runtime.lock.json','ui/catalog.lock.json','ui/editor.lock.json','docs/verification/release-candidate.json','README.md'],repo)
  for rel in ['.claude-plugin/plugin.json','.agents/plugins/marketplace.json','README.zh-CN.md','package.json','scripts/configure_editor_host.py']:
   if (repo/rel).exists():call(['git','add',rel],repo)
  call(['git','commit','-m','发布可安装Craft开发候选并校验首次启动资源'],repo);sha=call(['git','rev-parse','HEAD'],repo)
  call(['git','push','origin','HEAD:feature/REQ-20261016-wandl-craft-ui-skills'],repo)
  call(['git','tag',tag,sha],repo);call(['git','push','origin','refs/tags/'+tag],repo)
  # 更新完整发行包中的轻量元数据，运行资源保持其固定摘要。
  stage=out/'staging-market/plugins'/(name+'-plugin')
  for rel in call(['git','ls-files'],repo).splitlines():
   if rel.startswith(('evidence/','docs/evidence/')):continue
   p=repo/rel
   if p.is_file():target=stage/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
  archive=out/(name+'-plugin-'+row['version']+'.zip')
  with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=4) as z:
   for p in sorted(stage.rglob('*')):
    if p.is_file():z.write(p,(Path(name+'-plugin')/p.relative_to(stage)).as_posix())
  notes=out/(name+'-release-notes.md');notes.write_text('# 可安装开发预发布\n\n包含场景技能、官方图标、stdio MCP 与同会话编辑器。Node.js 24；Git 安装首次启动下载固定资源并校验 SHA-256，完整 ZIP 自带运行资源。\n\n生产发布仍 BLOCKED；不是所有上游 main 能力、真实素材效果或 Codex/ZCode/Kimi 内嵌同步均已验收。运行资源自身的上游版本与来源保留在 BUILD/config 元数据中，与插件版本分别记录。\n\nGit commit: '+sha+'\nRuntime SHA-256: '+row['sha256']+'\n')
  call(['gh','release','create',tag,'--repo',remote,'--verify-tag','--prerelease','--title',name+' Use '+row['version']+' (Development)','--notes-file',str(notes),*([str(out/row['runtime'])] if not row.get('reuseRuntime') else []),str(archive)],repo)
  report={**{k:v for k,v in row.items() if k!='runtimeDirectory'},'commit':sha,'archive':archive.name,'archiveSha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'releaseUrl':f'https://github.com/{remote}/releases/tag/{tag}'};reports.append(report);(out/'published.json').write_text(json.dumps(reports,indent=2));print(json.dumps(report),flush=True)
if __name__=='__main__':main()
