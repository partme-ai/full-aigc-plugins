#!/usr/bin/env python3
"""从受控Git文件与固定制品组装完整包，禁止依赖工作区残留的ui/dist。"""
from pathlib import Path
import subprocess,json,shutil,zipfile,argparse,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts/ci'))
from craft_windows import safe_name

def stage(out):
 market=out/'staging-market';entries=[]
 for row in json.loads((out/'index.json').read_text()):
  n=row['plugin'];repo=ROOT.parent/'full-aigc-plugins-repositories'/(n+'-plugin');dest=market/'plugins'/(n+'-plugin');dest.mkdir(parents=True)
  files=set(subprocess.check_output(['git','ls-files'],cwd=repo,text=True).splitlines())|{'ui/bootstrap.mjs','ui/runtime.lock.json','docs/verification/release-candidate.json'}
  for rel in sorted(files):
   src=repo/rel
   if src.is_file():target=dest/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,target)
  runtime=Path(row['runtimeDirectory']);lock=json.loads((repo/'ui/runtime.lock.json').read_text())
  for rel,digest in lock['files'].items():
   safe_name(rel)
   if hashlib.sha256((runtime/rel).read_bytes()).hexdigest()!=digest:raise ValueError('Runtime differs from lock: '+n+'/'+rel)
  shutil.copytree(runtime,dest/'ui/dist')
  editorlock=json.loads((repo/'ui/editor.lock.json').read_text())
  for rel,digest in editorlock.get('files',{}).items():
   if hashlib.sha256((runtime/'editor'/rel).read_bytes()).hexdigest()!=digest:raise ValueError('Legacy editor lock differs from runtime: '+n+'/'+rel)
  entries.append({'name':n,'source':{'source':'local','path':'./plugins/'+n+'-plugin'},'policy':{'installation':'AVAILABLE','authentication':'ON_USE'},'category':'Creativity'})
  archive=out/(n+'-plugin-'+row['version']+'.zip')
  with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=4) as z:
   for p in sorted(dest.rglob('*')):
    if p.is_file():safe_name(p.relative_to(dest).as_posix());z.write(p,(Path(n+'-plugin')/p.relative_to(dest)).as_posix())
  print(n,flush=True)
 manifest=market/'.agents/plugins/marketplace.json';manifest.parent.mkdir(parents=True);manifest.write_text(json.dumps({'name':'craft-market-release-acceptance','plugins':entries}))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('release_directory',type=Path);args=parser.parse_args();stage(args.release_directory.resolve())
