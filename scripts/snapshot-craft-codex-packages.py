#!/usr/bin/env python3
"""从不可变独立仓提交生成Codex市场内完整薄包，安装前即可解析包内图标。"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

ROOT=Path(__file__).resolve().parents[1]
NAMES='cadcraft designcraft effectcraft photocraft figcraft filmcraft lightcraft printcraft vectorcraft deckcraft soundcraft gridcraft wordcraft'.split()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--releases',type=Path,required=True);parser.add_argument('--output',type=Path);args=parser.parse_args()
    rows=json.loads(args.releases.read_text(encoding='utf-8'))
    if {r['plugin'] for r in rows}!=set(NAMES):raise ValueError('Exactly thirteen verified releases required')
    snapshots=args.output.resolve() if args.output else ROOT/'plugins';snapshots.mkdir(parents=True,exist_ok=True);records=[]
    for row in rows:
        name=row['plugin'];repo=ROOT.parent/'full-aigc-plugins-repositories'/(name+'-plugin');target=snapshots/(name+'-plugin')
        if target.exists():raise ValueError('Refusing existing snapshot: '+str(target))
        raw=subprocess.check_output(['git','archive',row['commit']],cwd=repo)
        hashes={};target.mkdir()
        with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
            for item in archive:
                relative=Path(item.name)
                if relative.is_absolute() or '..' in relative.parts:raise ValueError('Unsafe source path')
                if item.name.startswith(('evidence/','docs/evidence/','.github/')) or relative.name=='.gitignore':continue
                if item.isdir():continue
                if not item.isfile():raise ValueError('Non-regular source member: '+item.name)
                data=archive.extractfile(item).read();dest=target/relative;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);dest.chmod(item.mode & 0o777)
                hashes[relative.as_posix()]=hashlib.sha256(data).hexdigest()
        manifest=json.loads((target/'plugin.json').read_text(encoding='utf-8'))
        assert manifest['name']==name and manifest['version']==row['version']
        for field in ['logo','composerIcon']:
            path=target/manifest['extensions']['com.openai']['interface'][field]
            assert path.is_file() and path.resolve().is_relative_to(target.resolve())
        records.append({'plugin':name,'version':row['version'],'repository':'full-aigc-plugins/'+name+'-plugin','commit':row['commit'],'tag':'v'+row['version'],'fileCount':len(hashes),'treeSha256':hashlib.sha256(json.dumps(hashes,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'excluded':['evidence/','docs/evidence/','.github/','**/.gitignore'],'runtime':'unchanged pinned bootstrap; no ui/dist bundled in Git snapshot'})
        print(name,'snapshot',len(hashes),'files',flush=True)
    (snapshots/'source-lock.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

if __name__=='__main__':main()
