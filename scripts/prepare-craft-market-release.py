#!/usr/bin/env python3
"""准备固定发行资源和宿主入口，不修改上游源码或冻结技能快照。"""
from pathlib import Path
import json, subprocess, hashlib, tarfile, shutil, argparse
ROOT=Path(__file__).resolve().parents[1]
NAMES='cadcraft designcraft effectcraft photocraft figcraft filmcraft lightcraft printcraft vectorcraft deckcraft soundcraft gridcraft wordcraft'.split()
VERSION='0.1.0-dev.20261017.2'
def write(p,value):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--runtime-map',type=Path,required=True);args=parser.parse_args();out=args.output.resolve();out.mkdir(exist_ok=False);runtime_map=json.loads(args.runtime_map.read_text())
 rows=[];catalog=json.loads((ROOT/'catalog.json').read_text());catalog['candidatePlugins']=[c for c in catalog['candidatePlugins'] if c['id'] not in NAMES]
 for name in NAMES:
  repo=ROOT.parent/'full-aigc-plugins-repositories'/(name+'-plugin')
  assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo,text=True).strip(),name+' dirty'
  assert subprocess.check_output(['git','branch','--show-current'],cwd=repo,text=True).strip()=='feature/REQ-20261016-wandl-craft-ui-skills'
  for rel in ['plugin.json','.codex-plugin/plugin.json','.zcode-plugin/plugin.json','.claude-plugin/plugin.json','kimi.plugin.json','package.json']:
   p=repo/rel
   if p.exists():
    value=json.loads(p.read_text());value['version']=VERSION
    if rel=='plugin.json':display=value['extensions']['com.openai']['interface']['displayName']
    write(p,value)
  for rel in ['mcp.json','.mcp.json','.codex-plugin/mcp.json','kimi.plugin.json','scripts/configure_editor_host.py']:
   p=repo/rel
   if p.exists():p.write_text(p.read_text().replace('ui/dist/adapter.mjs','ui/bootstrap.mjs'))
  codex=repo/'.codex-plugin/mcp.json';v=json.loads(codex.read_text())
  for server in v['mcpServers'].values():server['startup_timeout_sec']=120
  write(codex,v)
  shutil.copy2(ROOT/'scripts/templates/craft-runtime-bootstrap.mjs',repo/'ui/bootstrap.mjs')
  dist=Path(runtime_map[name]).resolve();runtime=out/(name+'-runtime.tgz')
  if (dist/'editor/assets.json').exists():
   assets=json.loads((dist/'editor/assets.json').read_text());editor_lock={k:assets[k] for k in ['name','version','buildKind','upstream'] if k in assets};editor_lock['files']={p.relative_to(dist/'editor').as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((dist/'editor').rglob('*')) if p.is_file()};write(repo/'ui/editor.lock.json',editor_lock)
  marketplace=repo/'.agents/plugins/marketplace.json'
  if marketplace.exists():
   metadata=json.loads(marketplace.read_text());entry=metadata['plugins'][0];entry['version']=VERSION;entry['source']['ref']='v'+VERSION;url=f'https://cdn.jsdelivr.net/gh/full-aigc-plugins/{name}-plugin@v{VERSION}/assets/official-logo.png';entry['icon']=url;entry.setdefault('interface',{})['logo']=url;entry['interface']['displayName']=display;metadata.setdefault('interface',{})['displayName']=display;write(marketplace,metadata)
  files=sorted(p for p in dist.rglob('*') if p.is_file())
  assert files and (dist/'adapter.mjs').is_file()
  with tarfile.open(runtime,'w:gz',format=tarfile.USTAR_FORMAT) as tar:
   for p in files:
    assert not p.is_symlink();tar.add(p,arcname=p.relative_to(dist).as_posix(),recursive=False)
  hashes={p.relative_to(dist).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
  lock={'name':name,'version':VERSION,'url':f'https://github.com/full-aigc-plugins/{name}-plugin/releases/download/v{VERSION}/{runtime.name}','sha256':hashlib.sha256(runtime.read_bytes()).hexdigest(),'files':hashes,'scope':'Pinned editor artifact; bundled upstream/build provenance remains in editor/BUILD.json or config.json. This does not certify all upstream main capabilities.'}
  write(repo/'ui/runtime.lock.json',lock)
  write(repo/'docs/verification/release-candidate.json',{'releaseStatus':'BLOCKED','currentVersion':VERSION,'releaseTag':'v'+VERSION,'installableDevelopmentCandidate':True,'limitations':['Full creative/domain and all-host UI acceptance remains incomplete.','Production promotion is blocked; first Git launch requires network or an existing verified cache.','Web artifact versions are recorded independently; this release does not qualify every upstream main capability.']})
  note='\n## Installable editor development candidate\n\n`'+VERSION+'` is distributed through the Full AIGC plugin marketplace as a development prerelease. Node.js 24 is required. Git installations use `ui/bootstrap.mjs` to download and verify the pinned editor archive on first start; complete release ZIPs also include that archive unpacked for offline startup. No Rust build or npm installation is required. Startup diagnostics use stderr; stdio remains MCP-only. The editor shares its session with Agent commands. Full creative quality and all-host embedded UI acceptance are still incomplete. Existing dated validation below describes its original version.\n'
  for rel in ['README.md','README.zh-CN.md']:
   p=repo/rel
   if p.exists():
    text=p.read_text();first,sep,rest=text.partition('\n');rest=rest.replace('## Installable editor development candidate','## Previous development candidate');p.write_text(first+'\n'+note+'\n'+rest)
  catalog['candidatePlugins'].append({'id':name,'displayName':display,'repository':f'full-aigc-plugins/{name}-plugin','localDirectory':name+'-plugin','version':VERSION,'status':'release_candidate_installable','releaseGate':'docs/verification/release-candidate.json','description':'Development prerelease: scene skills, stdio MCP and an editor sharing the Agent session. Node.js 24 required; first Git startup downloads checksummed resources. Full creative and all-host acceptance pending.','shortDescription':'Scene skills and a shared-session editor · Development','category':'Productivity' if name in ['wordcraft','gridcraft','printcraft','deckcraft'] else 'Creativity','tags':[name,'craft','development','mcp','editor'],'logo':'assets/official-logo.png'})
  rows.append({'plugin':name,'version':VERSION,'runtime':runtime.name,'sha256':lock['sha256'],'bytes':runtime.stat().st_size,'runtimeDirectory':str(dist)})
 write(ROOT/'catalog.json',catalog);write(out/'index.json',rows)
 print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
