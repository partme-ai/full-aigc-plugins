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

ROOT = Path(__file__).resolve().parents[2]


def resolve_reference(version, requested, git):
    """默认验证公开标签；候选只接受与公开main完全一致的完整提交身份。"""
    ref = requested or 'v'+version
    if ref != 'v'+version and not re.fullmatch('[0-9a-f]{40}', ref):
        raise ValueError('invalid_fixed_reference')
    commit = git('rev-parse', ref+'^{commit}')
    if ref == 'v'+version:
        remote = git('ls-remote','origin','refs/tags/'+ref,'refs/tags/'+ref+'^{}').splitlines()
        if not any(line.split()[0] == commit for line in remote):
            raise ValueError('remote_release_mismatch')
        return {'ref':ref,'commit':commit,'kind':'public-tag'}
    if commit != ref:
        raise ValueError('fixed_commit_mismatch')
    remote = git('ls-remote','origin','refs/heads/main').splitlines()
    if not any(line.split() == [commit,'refs/heads/main'] for line in remote):
        raise ValueError('remote_commit_mismatch')
    return {'ref':ref,'commit':commit,'kind':'public-commit'}


def digest(directory):
    """普通文件树摘要与发布锁算法一致；不接受任何链接。"""
    if directory.is_symlink() or any(p.is_symlink() for p in directory.rglob('*')):
        raise ValueError('linked_installation')
    return hashlib.sha256(''.join(p.relative_to(directory).as_posix()+'\0'+hashlib.sha256(p.read_bytes()).hexdigest()+'\n'
        for p in sorted(directory.rglob('*')) if p.is_file()).encode()).hexdigest()


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
    parser.add_argument('--ref', help='公开main完整提交SHA；省略则必须验证当前版本公开标签')
    args=parser.parse_args();root=args.output.resolve()
    manifest=json.loads((ROOT/'plugin.json').read_text());lock=json.loads((ROOT/'skills.lock.json').read_text())['sources'][0]
    version=manifest['version']
    def git(*argv): return subprocess.check_output(['git',*argv],cwd=ROOT,text=True,timeout=60).strip()
    reference=resolve_reference(version,args.ref,git);ref=reference['ref'];commit=reference['commit']
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
        {'name':'vectorcraft','source':{'source':'url','url':'https://github.com/full-aigc-plugins/vectorcraft-plugin.git','ref':ref},
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
    assert set(found)=={'vectorcraft:'+name for name in lock['skills']}
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
    proof={'schema':'vectorcraft-fixed-host-install/v1','result':'PASS','pluginVersion':version,'pluginCommit':commit,
        'artifactRef':ref,'artifactKind':reference['kind'],'publicTagVerified':reference['kind']=='public-tag',
        'skillSourceRef':lock['ref'],'skillSourceCommit':lock['sha'],'hostVersion':host_version,'hostIdentity':identity,
        'platform':os.uname().sysname+'-'+os.uname().machine,'skills':records,
        'scope':'isolated actual '+reference['kind']+' plugin installation and host discovery; private acceptance catalog only',
        'excluded':['model implicit routing','GUI','complete V1','public marketplace eligibility']}
    (root/'proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'result':'PASS','skills':len(records),'hostVersion':host_version,'pluginVersion':version}))


if __name__=='__main__': main()
