#!/usr/bin/env python3
"""固定技能真实保存后的严格协议注入；原位置重开，禁止重放。"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from fixed_install import digest


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ('host','source','runtime','output'):parser.add_argument('--'+key,type=Path,required=True)
    args=parser.parse_args();root=args.output.resolve();root.mkdir(parents=True,exist_ok=False)
    host=json.loads(args.host.read_text());entry=next(x for x in host['skills'] if x['name']=='vectorcraft-use');skill=Path(entry['path']);assert digest(skill)==entry['sha256']
    fixture=args.source/'tests/fixtures/protocol_proxy.py';hook=args.source/'tests/fixtures/workflow_protocol_injection.py'
    proxy=root/'qa_protocol_proxy.py';original=fixture.read_text()
    additions='''        elif fault == 'wrong-id':
            reply['id'] = reply['id'] + 1000
            print(json.dumps(reply), flush=True)
        elif fault == 'duplicate-envelope':
            print('{"id":'+json.dumps(reply['id'])+',"id":'+json.dumps(reply['id'])+',"result":'+json.dumps(reply['result'])+'}', flush=True)
        elif fault in ('inner-nonfinite','inner-overflow','inner-duplicate'):
            texts={'inner-nonfinite':'{"saved":true,"value":NaN}', 'inner-overflow':'{"saved":true,"value":1e999}', 'inner-duplicate':'{"saved":true,"nested":{"value":1,"value":2}}'}
            reply['result']={'content':[{'type':'text','text':texts[fault]}]}
            print(json.dumps(reply), flush=True)
'''
    needle="        else:\n            reply['result'] = {'content': [None]}";assert needle in original
    proxy.write_text(original.replace(needle,additions+needle))
    records=[];env=dict(os.environ,PATH='/usr/bin:/bin')
    for key in ('CRAFT_RUNTIME_HOME','CRAFT_NODE_ARCHIVE','CRAFT_BUNDLE_DIRECTORY','CRAFT_NATIVE_ARCHIVE_DIRECTORY'):env.pop(key,None)
    for mode in ('direct','native-gateway'):
        operation={'command':'shape.rectangle','params':{'x':4,'y':4,'width':8,'height':8},'as':'shape'}
        if mode=='native-gateway':operation={'command':'native.command','params':{k:v for k,v in operation.items() if k!='as'},'as':'shape'}
        plan={'document':{'name':'Fixed strict reply','width':32,'height':32,'units':'Pixels'},'operations':[operation],'exports':[{'format':'png','artboard':0}]}
        for fault in ('malformed','scalar','missing','ambiguous','nonfinite','tool-content','wrong-id','duplicate-envelope','inner-nonfinite','inner-overflow','inner-duplicate'):
            case=root/(mode+'-'+fault);case.mkdir();path=case/'plan.json';path.write_text(json.dumps(plan));output=case/'delivery';log=case/'saves.jsonl'
            call=[sys.executable,'-I','-B',str(hook),str(proxy),fault,str(log),str(case/'proxy-capture.vectorcraft'),str(case/'reply.json'),str(skill/'scripts/workflow.py'),str(path),'--output',str(output),'--runtime-home',str(args.runtime)]
            result=subprocess.run(call,env=env,capture_output=True,text=True,timeout=120)
            (case/'stdout.log').write_text(result.stdout);(case/'stderr.log').write_text(result.stderr)
            assert result.returncode==1 and 'outcome_unknown' in json.loads(result.stdout)['error'],result.stdout+result.stderr
            saves=[json.loads(line) for line in log.read_text().splitlines()];assert len(saves)==1 and saves[0]['saveSucceeded']
            failure=json.loads((output/'failure.json').read_text());stage=output/failure['stage'];project=stage/'project.vectorcraft'
            assert failure['outcome']=='outcome_unknown' and not failure['replayAllowed']
            assert failure['lastAttempt']['phase']=='submitted' and sha(project)==saves[0]['sha256']
            assert not (output/'manifest.json').exists()
            inspect=case/'inspect.json';inspect.write_text(json.dumps({'schema':'craft-command-plan/v1','operations':[
                {'command':'document.open','params':{'path':{'$ref':'project.path'}}},{'command':'document.json','params':{}}]}))
            reopened=subprocess.run([sys.executable,'-I','-B',str(skill/'scripts/commands.py'),'run',str(inspect),'--input','project='+str(project),'--output',str(case/'inspection'),'--runtime-home',str(args.runtime)],capture_output=True,text=True,env=env,timeout=90)
            assert reopened.returncode==0,reopened.stdout+reopened.stderr
            assert sha(project)==saves[0]['sha256']
            repeated=subprocess.run(call,env=env,capture_output=True,text=True,timeout=60)
            assert repeated.returncode==1 and 'output_exists' in repeated.stdout and len(log.read_text().splitlines())==1
            assert all(sha(stage/name)==value['sha256'] for name,value in failure['files'].items())
            records.append({'mode':mode,'fault':fault,'result':'PASS','nativeSaveCount':1,'originalStageReopened':True,'replayRefused':True,'projectSha256':sha(project),'failureSha256':sha(output/'failure.json')})
            print('PASS',mode,fault,flush=True)
    assert digest(skill)==entry['sha256']
    proof={'schema':'vectorcraft-fixed-strict-protocol/v1','result':'PASS','pluginVersion':host['pluginVersion'],'sourceCommit':host['skillSourceCommit'],
        'installedSkillSha256':entry['sha256'],'nativeRuntimeSha256':json.loads((skill/'scripts/runtime.lock.json').read_text())['artifacts']['darwin-arm64']['binarySha256'],
        'driverSha256':sha(Path(__file__)),'originalProxySha256':sha(fixture),'hookSha256':sha(hook),'qaProxySha256':sha(proxy),'cases':records,
        'scope':'22 actual save faults through direct and native.command workflow; original retained projects reopened and repeated execution refused; not exhaustive commands'}
    (root/'proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':main()
