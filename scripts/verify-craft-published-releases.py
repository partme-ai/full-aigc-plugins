#!/usr/bin/env python3
"""核验远端不可变标签及GitHub计算的制品摘要；不下载或执行制品。"""
from pathlib import Path
import json,subprocess,argparse,concurrent.futures

def api(path):return json.loads(subprocess.check_output(['gh','api',path],text=True))
def verify(row):
 repo='full-aigc-plugins/'+row['plugin']+'-plugin';tag='v'+row['version'];ref=api('repos/'+repo+'/git/ref/tags/'+tag)
 assert ref['object']['type']=='commit' and ref['object']['sha']==row['commit'],(repo,'remote commit mismatch')
 release=api('repos/'+repo+'/releases/tags/'+tag);assert release['prerelease'] and not release['draft']
 assets={a['name']:a for a in release['assets']}
 assert assets[row['archive']]['digest']=='sha256:'+row['archiveSha256'],(repo,'package digest mismatch')
 runtimeRelease=api('repos/'+repo+'/releases/tags/'+row['runtimeRef']) if row.get('reuseRuntime') else release
 runtimeAssets={asset['name']:asset for asset in runtimeRelease['assets']}
 assert runtimeAssets[row['runtime']]['digest']=='sha256:'+row['sha256'],(repo,'runtime digest mismatch')
 return {**row,'remoteTagCommit':'PASS','publishedPrerelease':'PASS','remoteAssetDigests':'PASS'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('release_directory',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();rows=json.loads((a.release_directory/'published.json').read_text());assert len(rows)==13
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(verify,rows))
 a.output.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n');print('13 remote tags, prereleases and 26 GitHub asset digests PASS')
