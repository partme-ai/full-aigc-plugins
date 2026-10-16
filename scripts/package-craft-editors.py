#!/usr/bin/env python3
"""打包本地候选，包含已构建编辑器；不提交、安装或发布。"""
from pathlib import Path
import argparse, hashlib, json, subprocess, zipfile
p=argparse.ArgumentParser();p.add_argument('--repositories',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
p.add_argument('--runtime-overrides',type=Path,help='独立构建的 <plugin>/ui/dist 与 editor.lock.json；不替换活动工作区')
a=p.parse_args()
names="cadcraft designcraft effectcraft photocraft figcraft filmcraft lightcraft printcraft vectorcraft deckcraft soundcraft gridcraft wordcraft".split()
a.output.mkdir(parents=True,exist_ok=True);result=[]
for name in names:
 root=a.repositories/f'{name}-plugin'
 subprocess.run(['python3',str(root/'scripts/validate_editor_scenes.py')],check=True,capture_output=True)
 assert (root/'ui/dist/adapter.mjs').is_file(),name
 allowed={'com.anthropic.claude-code','.codex-plugin','.claude-plugin','.zcode-plugin','skills','scripts','resources','agents','commands','hooks','assets','docs','ui','hosts','schemas'}
 omitted={'node_modules','__pycache__','.local','.git','tests','.runtime'}
 excluded={'scripts/configure_editor_host.py','scripts/qa/command_charStyle.py','scripts/qa/command_charStyle_render.py'}
 files=[]
 override=a.runtime_overrides/f'{name}-plugin' if a.runtime_overrides else None
 if override and not (override/'ui/dist/adapter.mjs').is_file():raise SystemExit(f'{name}: missing requested runtime override; refusing stale fallback')
 for f in root.rglob('*'):
  rel=f.relative_to(root)
  if not f.is_file() or f.is_symlink() or any(x in omitted for x in rel.parts) or str(rel) in excluded:continue
  if any(x in {'verification','evidence'} for x in rel.parts) or rel.parts[:2]==('hosts','workbuddy'):continue
  if override and (rel.parts[:2]==('ui','dist') or str(rel)=='ui/editor.lock.json'):continue
  if len(rel.parts)>1 and rel.parts[0] not in allowed:continue
  if len(rel.parts)==1 and not (f.suffix in {'.json','.md'} or f.name.startswith(('LICENSE','NOTICE'))):continue
  files.append(f)
 out=a.output/f'{name}-editor-scenes-local.zip'
 if out.exists():raise SystemExit(f'Refusing overwrite: {out}')
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=3) as z:
  for f in sorted(files):z.write(f,Path(f'{name}-plugin')/f.relative_to(root))
  if override:
   assert (override/'ui/editor.lock.json').is_file(),f'{name}: missing runtime lock'
   for f in sorted((override/'ui/dist').rglob('*'))+[override/'ui/editor.lock.json']:
    if f.is_file():z.write(f,Path(f'{name}-plugin')/f.relative_to(override))
  count=len(z.infolist())
 result.append({'plugin':name,'file':out.name,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'files':count,'runtimeOverride':bool(override),'status':'local-unreleased'})
(a.output/'index.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
