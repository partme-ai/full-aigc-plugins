#!/usr/bin/env python3
"""逐项执行实际宿主安装技能的空缓存安装及已声明创建／返工合同。"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
_spec=importlib.util.spec_from_file_location('craft_fixed_install',Path(__file__).with_name('fixed_install.py'))
_install=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_install)
digest,ROOT=_install.digest,_install.ROOT


def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def files(root): return {p.relative_to(root).as_posix():sha(p) for p in root.rglob('*') if p.is_file()}


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--host',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();host=json.loads(args.host.read_text());root=args.output.resolve();root.mkdir(parents=True,exist_ok=False)
    manifest=json.loads((ROOT/'plugin.json').read_text());source=json.loads((ROOT/'skills.lock.json').read_text())['sources'][0]
    assert host['result']=='PASS' and host['pluginVersion']==manifest['version']
    assert host['skillSourceRef']==source['ref'] and host['skillSourceCommit']==source['sha']
    def git(*argv):
        return subprocess.check_output(['git',*argv],cwd=ROOT,text=True,timeout=60).strip()
    reference=_install.resolve_reference(manifest['version'],host.get('artifactRef'),git)
    assert host['pluginCommit']==reference['commit']
    assert host.get('artifactKind', 'public-tag')==reference['kind']
    assert host.get('publicTagVerified', True)==(reference['kind']=='public-tag')
    env=dict(os.environ,PATH='/usr/bin:/bin')
    for key in ('CRAFT_RUNTIME_HOME','CRAFT_NODE_ARCHIVE','CRAFT_BUNDLE_DIRECTORY','CRAFT_NATIVE_ARCHIVE_DIRECTORY'): env.pop(key,None)
    records=[]
    for entry in host['skills']:
        origin=Path(entry['path']);assert digest(origin)==entry['sha256']
        case=root/entry['name'];case.mkdir();skill=case/'only skill'/entry['name'];shutil.copytree(origin,skill)
        runtime=case/'empty runtime';assert not runtime.exists()
        def run(label,script,*argv):
            call=[sys.executable,'-I','-B',str(skill/'scripts'/script),*map(str,argv)]
            result=subprocess.run(call,env=env,capture_output=True,text=True,timeout=300)
            (case/(label+'.stdout')).write_text(result.stdout);(case/(label+'.stderr')).write_text(result.stderr)
            with (case/'calls.jsonl').open('a') as stream: stream.write(json.dumps({'argv':call,'returncode':result.returncode,'stdoutSha256':sha(case/(label+'.stdout'))})+'\n')
            if result.returncode: raise RuntimeError(entry['name']+' '+label+': '+result.stdout+result.stderr)
            return result.stdout
        install=json.loads(run('setup','bootstrap.py','--runtime-home',runtime));assert install['reused'] is False
        native_lock=json.loads((skill/'scripts/runtime.lock.json').read_text());binary=Path(install['executable'])
        assert binary.is_relative_to(runtime) and sha(binary)==native_lock['artifacts']['darwin-arm64']['binarySha256']
        version=run('version','cli.py','--runtime-home',runtime,'--','--version').strip()
        assert native_lock['resolvedVersion'] in version
        catalog=json.loads(run('catalog','cli.py','--runtime-home',runtime,'--','commands','--json'));assert len(catalog)==585
        contract=json.loads((skill/'references/operation-contract.json').read_text())['examples'];created=case/'created';revised=case/'revised'
        if contract:
            create=skill/contract['create']['path'];revision=json.loads((skill/contract['revise']['path']).read_text())
            if contract['create']['format']=='vectorcraft-workflow':
                result=json.loads(run('create','workflow.py',create,'--output',created,'--runtime-home',runtime))
                revision['expectedProjectSha256']=result['files']['project.vectorcraft'];plan=case/'revision.json';plan.write_text(json.dumps(revision))
                original=files(created)
                run('revise','workflow.py',plan,'--source',created,'--output',revised,'--runtime-home',runtime)
                for directory in (created,revised):
                    manifest=json.loads((directory/'manifest.json').read_text())
                    assert all(sha(directory/path)==value for path,value in manifest['files'].items())
            else:
                result=json.loads(run('create','commands.py','run',create,'--output',created,'--runtime-home',runtime))
                assert result['result']=='PASS'
                target=next(step['result'] for step in result['steps'] if step['command']=='shape.rectangle')
                assert isinstance(target['id'],int)
                # target.id 是待绑定模板；--input 仅登记路径与摘要，不加载 JSON 字段。
                def bind(value):
                    if value=={'$ref':'target.id'}: return target['id']
                    if isinstance(value,dict): return {key:bind(child) for key,child in value.items()}
                    if isinstance(value,list): return [bind(child) for child in value]
                    return value
                revision=bind(revision)
                (case/'target-binding.json').write_text(json.dumps({'targetId':target['id'],'createReceiptSha256':sha(case/'create.stdout'),'projectSha256':sha(created/'project.vectorcraft')},indent=2)+'\n')
                target_file=case/'target.json';target_file.write_text(json.dumps(target))
                plan=case/'revision.json';plan.write_text(json.dumps(revision));original=files(created)
                result=json.loads(run('revise','commands.py','run',plan,'--input','project='+str(created/'project.vectorcraft'),'--input','target='+str(target_file),'--output',revised,'--runtime-home',runtime))
                assert result['result']=='PASS'
                before=next(step['result'] for step in result['steps'] if step['index']==1)
                after=next(step['result'] for step in result['steps'] if step['index']==3)
                assert before!=after
            assert original==files(created)
            assert (created/'project.vectorcraft').is_file() and (revised/'project.vectorcraft').is_file()
            assert sha(created/'project.vectorcraft')!=sha(revised/'project.vectorcraft')
        assert digest(origin)==entry['sha256'] and digest(skill)==entry['sha256']
        record={'skill':entry['name'],'sha256':entry['sha256'],'runtimeSha256':sha(binary),'runtimeVersion':version,'freshRuntime':True,
            'commandCount':len(catalog),'createRevise':'PASS' if contract else 'NOT_APPLICABLE_SETUP_ONLY','installedBytesPreserved':True,
            'contractSha256':sha(skill/'references/operation-contract.json'),'case':str(case),'runtimeHome':str(runtime)}
        records.append(record);(root/'progress.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
        print('PASS',entry['name'],record['createRevise'],flush=True)
    proof={'schema':'vectorcraft-fixed-standalone-native/v1','result':'PASS','hostProofSha256':sha(args.host),'pluginVersion':host['pluginVersion'],
        'pluginCommit':host['pluginCommit'],'skillSourceRef':host['skillSourceRef'],'skillSourceCommit':host['skillSourceCommit'],
        'artifactRef':reference['ref'],'artifactKind':reference['kind'],'publicTagVerified':reference['kind']=='public-tag',
        'python':sys.version,'platform':host['platform'],'driverSha256':sha(Path(__file__)),'cases':records,
        'scope':'13 installed skills independently cold-start; 12 declared create/revise pairs, setup-only excluded; not model routing or exhaustive domain acceptance'}
    (root/'proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': main()
