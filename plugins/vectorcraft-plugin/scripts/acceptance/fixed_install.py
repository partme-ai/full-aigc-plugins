#!/usr/bin/env python3
"""在全新隔离 Codex 配置中安装公开固定标签，核对实际技能与宿主发现。"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import queue
import re
import shutil
import subprocess
import threading
import time
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
REPOSITORY = 'full-aigc-plugins/vectorcraft-plugin'
GIT_URL = 'https://github.com/'+REPOSITORY+'.git'


def verify_public_commit(commit):
    """Query the fixed GitHub repository without credentials; fail closed on any mismatch."""
    base='https://api.github.com/repos/'+REPOSITORY
    def get(path):
        url=base+path
        with urlopen(Request(url,headers={'User-Agent':'vectorcraft-fixed-acceptance','Accept':'application/vnd.github+json'}),timeout=20) as response:
            if response.status!=200 or response.geturl()!=url: raise ValueError('public_commit_unverified')
            return json.loads(response.read(1_000_001))
    try:
        repo=get('')
        result=get('/commits/'+commit)
        if repo.get('full_name')!=REPOSITORY or repo.get('private') is not False or repo.get('visibility')!='public' or result.get('sha')!=commit:
            raise ValueError('public_commit_unverified')
    except Exception as error:
        raise ValueError('public_commit_unverified') from error
    return commit


def resolve_reference(version, requested, git, candidate_branch=None, public_verify=verify_public_commit):
    """Pin a remote ref to an exact SHA and independently verify public retrieval."""
    def confirmed_public(commit):
        try:
            if public_verify(commit)!=commit: raise ValueError('public_commit_unverified')
        except Exception as error:
            raise ValueError('public_commit_unverified') from error
    ref = requested or 'v'+version
    if ref != 'v'+version and not re.fullmatch('[0-9a-f]{40}', ref):
        raise ValueError('invalid_fixed_reference')
    commit = git('rev-parse', ref+'^{commit}')
    if ref == 'v'+version:
        remote = git('ls-remote',GIT_URL,'refs/tags/'+ref,'refs/tags/'+ref+'^{}').splitlines()
        if not any(line.split()[0] == commit for line in remote):
            raise ValueError('remote_release_mismatch')
        confirmed_public(commit)
        return {'ref':ref,'commit':commit,'kind':'public-tag'}
    if commit != ref:
        raise ValueError('fixed_commit_mismatch')
    if candidate_branch is not None:
        if not re.fullmatch(r'fix/[a-z0-9][a-z0-9/_-]*',candidate_branch) or '..' in candidate_branch or '//' in candidate_branch:
            raise ValueError('invalid_candidate_branch')
        branch='refs/heads/'+candidate_branch
    else:
        branch='refs/heads/main'
    remote = git('ls-remote',GIT_URL,branch).splitlines()
    if not any(line.split() == [commit,branch] for line in remote):
        raise ValueError('remote_commit_mismatch')
    confirmed_public(commit)
    return {'ref':ref,'commit':commit,'kind':'public-commit'}


def digest(directory):
    """普通文件树摘要与发布锁算法一致；不接受任何链接。"""
    if directory.is_symlink() or any(p.is_symlink() for p in directory.rglob('*')):
        raise ValueError('linked_installation')
    return hashlib.sha256(''.join(p.relative_to(directory).as_posix()+'\0'+hashlib.sha256(p.read_bytes()).hexdigest()+'\n'
        for p in sorted(directory.rglob('*')) if p.is_file()).encode()).hexdigest()


def expected_skills(lock, local_policy):
    """Require both immutable source skills and declared plugin-local skills."""
    local=local_policy['skills']
    if local_policy['version']!=1 or local_policy['dest'] not in ('skills','skills/') or len(local)!=len(set(local)) or set(local)&set(lock['skills']):
        raise ValueError('invalid_local_skill_inventory')
    return {'vectorcraft:'+name for name in [*lock['skills'],*local]}


def discover(codex, root, env):
    """调用真实宿主发现接口；不调用模型，不推断隐式路由已经验收。"""
    with (root/'app-server.stderr.log').open('w') as errors:
        process = subprocess.Popen([codex,'app-server','--listen','stdio://'],cwd=root,env=env,
            stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=errors,text=True,bufsize=1)
        messages=queue.Queue()
        def read():
            for line in process.stdout:
                try: messages.put(json.loads(line))
                except ValueError: messages.put({'error':line})
            messages.put(None)
        thread=threading.Thread(target=read,daemon=True);thread.start()
        def request(identifier,method,params):
            process.stdin.write(json.dumps({'id':identifier,'method':method,'params':params})+'\n');process.stdin.flush()
            deadline=time.monotonic()+45
            while time.monotonic()<deadline:
                reply=messages.get(timeout=max(.01,deadline-time.monotonic()))
                if reply is None: raise RuntimeError('host_stopped')
                if reply.get('id')==identifier:
                    if 'error' in reply: raise RuntimeError(str(reply['error']))
                    return reply['result']
            raise TimeoutError('host_timeout')
        try:
            identity=request(1,'initialize',{'clientInfo':{'name':'vectorcraft-fixed-acceptance','version':'1.0'},'capabilities':{'experimentalApi':True}})
            process.stdin.write(json.dumps({'method':'initialized','params':{}})+'\n');process.stdin.flush()
            response=request(2,'skills/list',{'cwds':[str(root)],'forceReload':True})
            return identity,response
        finally:
            process.stdin.close();process.terminate()
            try: process.wait(timeout=5)
            except subprocess.TimeoutExpired: process.kill();process.wait(timeout=5)
            thread.join(timeout=1);process.stdout.close()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--codex',default=shutil.which('codex'))
    parser.add_argument('--ref', help='公开可检索的完整提交SHA；省略则验证当前版本公开标签')
    parser.add_argument('--candidate-branch', help='要求完整SHA精确等于此远端fix分支头')
    args=parser.parse_args();root=args.output.resolve()
    manifest=json.loads((ROOT/'plugin.json').read_text());lock=json.loads((ROOT/'skills.lock.json').read_text())['sources'][0]
    local_policy=json.loads((ROOT/'plugin-local-skills.json').read_text())
    version=manifest['version']
    def git(*argv): return subprocess.check_output(['git',*argv],cwd=ROOT,text=True,timeout=60).strip()
    reference=resolve_reference(version,args.ref,git,args.candidate_branch);ref=reference['ref'];commit=reference['commit']
    if git('show',ref+':plugin.json').encode()+b'\n'!=(ROOT/'plugin.json').read_bytes(): raise ValueError('release_manifest_drift')
    root.mkdir(parents=True,exist_ok=False);home=root/'codex home';home.mkdir(mode=0o700)
    env=dict(os.environ,CODEX_HOME=str(home))
    def run(*argv):
        result=subprocess.run([args.codex,*argv],cwd=root,env=env,capture_output=True,text=True,timeout=240)
        with (root/'host-calls.jsonl').open('a') as stream:
            stream.write(json.dumps({'argv':argv,'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr})+'\n')
        if result.returncode: raise RuntimeError('host_command_failed: '+result.stderr+result.stdout)
        return result.stdout
    host_version=run('--version').strip()
    market=root/'private acceptance market';path=market/'.agents/plugins/marketplace.json';path.parent.mkdir(parents=True)
    path.write_text(json.dumps({'name':'vectorcraft-private-acceptance','owner':{'name':'Full AIGC Plugins'},'plugins':[
        {'name':'vectorcraft','source':{'source':'url','url':GIT_URL,'ref':ref},
         'policy':{'installation':'AVAILABLE','authentication':'ON_USE'},'version':version,'category':'Creativity'}]}))
    run('plugin','marketplace','add',str(market),'--json')
    run('plugin','add','vectorcraft@vectorcraft-private-acceptance','--json')
    identity,response=discover(args.codex,root,env)
    (root/'discovery.json').write_text(json.dumps(response,ensure_ascii=False,indent=2)+'\n')
    rows=response['data'];assert not any(row.get('errors') for row in rows)
    # codex>=0.162 的 skills/list 会把宿主内置 .system 技能也冠以 vectorcraft: 前缀报出；
    # 插件技能只可能位于安装缓存 plugins/cache/ 下，宿主系统技能不在其内，精确集合断言保持不变。
    found={skill['name']:skill for row in rows for skill in row.get('skills',[])
        if skill['name'].startswith('vectorcraft:') and 'plugins/cache/' in Path(skill['path']).as_posix()}
    assert set(found)==expected_skills(lock,local_policy)
    records=[]
    for name in lock['skills']:
        skill=found['vectorcraft:'+name];directory=Path(skill['path']).resolve().parent
        assert skill['enabled'] and directory.is_relative_to(home)
        installed=directory.parent.parent
        assert (installed/'plugin.json').read_bytes()==(ROOT/'plugin.json').read_bytes()
        assert json.loads((installed/'skills.lock.json').read_text())['sources'][0]==lock
        assert digest(directory)==lock['sha256'][name]
        records.append({'name':name,'path':str(directory),'sha256':digest(directory),'enabled':True,
            'implicitPolicy':(directory/'agents/openai.yaml').read_text()})
    local_records=[]
    for name in local_policy['skills']:
        skill=found['vectorcraft:'+name];directory=Path(skill['path']).resolve().parent
        assert skill['enabled'] and directory.is_relative_to(home)
        assert (directory/'SKILL.md').read_bytes()==(ROOT/'skills'/name/'SKILL.md').read_bytes()
        local_records.append({'name':name,'path':str(directory),'skillSha256':hashlib.sha256((directory/'SKILL.md').read_bytes()).hexdigest(),'enabled':True})
    proof={'schema':'vectorcraft-fixed-host-install/v1','result':'PASS','pluginVersion':version,'pluginCommit':commit,
        'artifactRef':ref,'artifactKind':reference['kind'],'candidateBranch':args.candidate_branch,'publicTagVerified':reference['kind']=='public-tag',
        'skillSourceRef':lock['ref'],'skillSourceCommit':lock['sha'],'hostVersion':host_version,'hostIdentity':identity,
        'platform':os.uname().sysname+'-'+os.uname().machine,'skills':records,'localSkills':local_records,
        'scope':'isolated actual '+reference['kind']+' plugin installation and host discovery; private acceptance catalog only',
        'excluded':['model implicit routing','GUI','complete V1','public marketplace eligibility']}
    (root/'proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'result':'PASS','sourceSkills':len(records),'localSkills':len(local_records),'hostVersion':host_version,'pluginVersion':version}))


if __name__=='__main__': main()
