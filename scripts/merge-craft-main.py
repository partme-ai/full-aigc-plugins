#!/usr/bin/env python3
"""按已授权的feature→test→main合并，保护脏工作区和未推送main。"""
from pathlib import Path
import argparse,json,subprocess
ROOT=Path(__file__).resolve().parents[1];FEATURE='feature/REQ-20261016-wandl-craft-ui-skills';TEST='test/20261017'
NAMES='cadcraft designcraft effectcraft photocraft figcraft filmcraft lightcraft printcraft vectorcraft deckcraft soundcraft gridcraft wordcraft'.split()
def git(repo,*args,required=True):
 r=subprocess.run(['git',*args],cwd=repo,capture_output=True,text=True,timeout=180)
 if required and r.returncode:raise RuntimeError(str(args)+': '+r.stderr[-2000:]+r.stdout[-2000:])
 return r.stdout.strip() if r.returncode==0 else None
def merge(repo):
 assert git(repo,'rev-parse','--show-toplevel')==str(repo.resolve())
 assert not git(repo,'status','--porcelain'), 'dirty worktree'
 git(repo,'fetch','origin');feature=git(repo,'rev-parse',FEATURE);remote_main=git(repo,'rev-parse','--verify','refs/remotes/origin/main',required=False);local_main=git(repo,'rev-parse','--verify','refs/heads/main',required=False)
 if remote_main and local_main:
  ahead=int(git(repo,'rev-list','--count','origin/main..main'));assert ahead==0,'local main has unpublished commits'
 base='origin/main' if remote_main else ('main' if local_main else FEATURE)
 if git(repo,'show-ref','--verify','refs/heads/'+TEST,required=False):
  git(repo,'checkout',TEST)
  if git(repo,'rev-parse','--verify','refs/remotes/origin/'+TEST,required=False):git(repo,'merge','--ff-only','origin/'+TEST)
 elif git(repo,'rev-parse','--verify','refs/remotes/origin/'+TEST,required=False):git(repo,'checkout','-b',TEST,'origin/'+TEST)
 else:git(repo,'checkout','-b',TEST,base)
 git(repo,'merge','--no-ff',FEATURE,'-m','合并Craft候选到测试分支');git(repo,'push','-u','origin',TEST)
 if local_main:git(repo,'checkout','main')
 else:git(repo,'checkout','-b','main','origin/main' if remote_main else TEST)
 if remote_main:git(repo,'merge','--ff-only','origin/main')
 git(repo,'merge','--no-ff',TEST,'-m','发布Craft可安装候选到main');git(repo,'push','-u','origin','main');head=git(repo,'rev-parse','HEAD');remote=git(repo,'ls-remote','origin','refs/heads/main').split()[0];assert head==remote
 git(repo,'merge-base','--is-ancestor',feature,'main')
 return {'repository':git(repo,'remote','get-url','origin'),'featureCommit':feature,'mainCommit':head,'remoteMainVerified':True,'worktreeClean':not bool(git(repo,'status','--porcelain'))}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--group',choices=['skills','plugins','hub'],required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();repos=[ROOT] if a.group=='hub' else [ROOT.parent/('full-aigc-'+a.group+'-repositories')/(n+('-skills' if a.group=='skills' else '-plugin')) for n in NAMES];rows=[]
 for repo in repos:
  try:row=merge(repo)
  except Exception as e:row={'repository':repo.name,'error':str(e),'status':'FAIL'}
  rows.append(row);a.output.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n');print(json.dumps(row,ensure_ascii=False),flush=True)
 assert all(r.get('remoteMainVerified') for r in rows)
