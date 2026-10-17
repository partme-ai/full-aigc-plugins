#!/usr/bin/env python3
"""固定安装的品牌字段边界：闭合性、目标未达成、无消费者与合法无需修改。"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from fixed_install import digest


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def files(p): return {x.relative_to(p).as_posix():sha(x) for x in p.rglob('*') if x.is_file()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ('host','brand','runtime','output'): parser.add_argument('--'+key,type=Path,required=True)
    args=parser.parse_args();root=args.output.resolve();root.mkdir(parents=True,exist_ok=False)
    host=json.loads(args.host.read_text());entry=next(x for x in host['skills'] if x['name']=='vectorcraft-cli-appearance')
    origin=Path(entry['path']);assert digest(origin)==entry['sha256']
    clean=root/'clean skill';shutil.copytree(origin,clean)
    # 既有受控测试副本包含透明记录的 QA-only 真实原生误改钩子。
    instrumented=root/'instrumented skill';shutil.copytree(args.brand/'.agents/skills/vectorcraft-cli-appearance',instrumented)
    source=args.brand/'source';original=files(source);manifest=json.loads((source/'manifest.json').read_text())
    native=json.loads((source/'native.json').read_text());target=manifest['bindings']['bound']['id']
    def find(value):
        if isinstance(value,dict):
            if value.get('id')==target and isinstance(value.get('kind'),dict): return value
            for child in value.values():
                result=find(child)
                if result is not None:return result
        if isinstance(value,list):
            for child in value:
                result=find(child)
                if result is not None:return result
    paths=find(native['layers'])['kind']['path']['subpaths']
    opened=json.loads(json.dumps(paths));assert opened[0]['closed'];opened[0]['closed']=False
    anchors=[{'x':a['p'][0],'y':a['p'][1]} for a in opened[0]['anchors']]
    change={'expectedProjectSha256':manifest['files']['project.vectorcraft'],'operations':[
        {'command':'swatch.edit','params':{'name':'Brand Primary','color':'#175cce'}}]}
    env=dict(os.environ,PATH='/usr/bin:/bin');records=[]
    def call(label,skill,plan,source=None,fault=None):
        path=root/(label+'.json');path.write_text(json.dumps(plan));output=root/label
        callenv=dict(env)
        for key in ('CRAFT_BRAND_FAULT_COMMAND','CRAFT_BRAND_FAULT_OBJECT','CRAFT_RUNTIME_HOME','CRAFT_NODE_ARCHIVE','CRAFT_NATIVE_ARCHIVE_DIRECTORY','CRAFT_BUNDLE_DIRECTORY'):callenv.pop(key,None)
        if fault:
            callenv.update(CRAFT_BRAND_FAULT_OBJECT=str(target),CRAFT_BRAND_FAULT_COMMAND=json.dumps(fault),CRAFT_BRAND_FAULT_LOG=str(root/(label+'-injection.jsonl')))
        argv=[sys.executable,'-I','-B',str(skill/'scripts/workflow.py'),str(path),'--output',str(output),'--runtime-home',str(args.runtime)]
        if source:argv+=['--source',str(source)]
        result=subprocess.run(argv,env=callenv,capture_output=True,text=True,timeout=180)
        (root/(label+'.stdout')).write_text(result.stdout);(root/(label+'.stderr')).write_text(result.stderr)
        return result,output
    for mode in ('direct','native-gateway'):
        plan=json.loads(json.dumps(change))
        if mode=='native-gateway':plan['operations']=[{'command':'native.command','params':plan['operations'][0]}]
        for fault,command in [('consumer-closed',{'command':'path.setAnchors','params':{'id':target,'subpaths':[{'anchors':anchors,'closed':False}]}}),
                              ('target-not-reached',{'command':'swatch.edit','params':{'name':'Brand Primary','color':'#2366e8'}})]:
            result,output=call(mode+'-'+fault,instrumented,plan,source,command)
            assert result.returncode!=0 and 'brand_dependency_violation' in result.stdout,result.stdout+result.stderr
            failure=json.loads((output/'failure.json').read_text());stage=output/failure['stage']
            assert not failure['replayAllowed'] and not (output/'manifest.json').exists()
            report=json.loads((stage/'brand-dependencies.json').read_text())['checks'][0]
            assert report['status']=='failed' and report['checkpointRetained']
            checkpoint=stage/report['checkpoint'];before=sha(checkpoint)
            inspect=root/(mode+'-'+fault+'-inspect.json');inspect.write_text(json.dumps({'schema':'craft-command-plan/v1','operations':[
                {'command':'document.open','params':{'path':{'$ref':'project.path'}}},{'command':'document.json','params':{}}]}))
            reopened=subprocess.run([sys.executable,'-I','-B',str(clean/'scripts/commands.py'),'run',str(inspect),'--input','project='+str(checkpoint),'--output',str(root/(mode+'-'+fault+'-inspection')),'--runtime-home',str(args.runtime)],capture_output=True,text=True,env=env,timeout=90)
            assert reopened.returncode==0,reopened.stdout+reopened.stderr
            assert before==sha(checkpoint) and files(source)==original
            records.append({'mode':mode,'case':fault,'result':'PASS','failureRetained':True,'checkpointReopened':True,'sourceUnchanged':True,'check':report})
        noop=json.loads(json.dumps(plan))
        edit=noop['operations'][0]['params'] if mode=='native-gateway' else noop['operations'][0]
        edit['params']['color']='#2366e8'
        result,output=call(mode+'-verified-noop',clean,noop,source)
        assert result.returncode==0,result.stdout+result.stderr
        report=json.loads((output/'brand-dependencies.json').read_text())['checks'][0]
        assert report['effect']=='verified_noop' and report['status']=='passed'
        records.append({'mode':mode,'case':'verified_noop','result':'PASS','check':report})
    empty={'document':{'name':'No consumer','width':32,'height':32,'units':'Pixels'},'operations':[
        {'command':'swatch.new','params':{'name':'Brand Primary','color':'#2366e8','global':True},'as':'primary'}],'exports':[]}
    created,no_consumer=call('no-consumer-source',clean,empty);assert created.returncode==0,created.stdout
    no_manifest=json.loads((no_consumer/'manifest.json').read_text())
    for mode in ('direct','native-gateway'):
        plan=json.loads(json.dumps(change));plan['expectedProjectSha256']=no_manifest['files']['project.vectorcraft']
        if mode=='native-gateway':plan['operations']=[{'command':'native.command','params':plan['operations'][0]}]
        result,output=call(mode+'-no-consumer',clean,plan,no_consumer)
        assert result.returncode!=0 and 'brand_dependency_violation' in result.stdout,result.stdout
        failure=json.loads((output/'failure.json').read_text());report=json.loads((output/failure['stage']/'brand-dependencies.json').read_text())['checks'][0]
        assert report['effect']=='no_effect' and report['status']=='failed'
        records.append({'mode':mode,'case':'no_effect','result':'PASS','check':report})
    assert digest(origin)==entry['sha256'] and digest(clean)==entry['sha256'] and files(source)==original
    proof={'schema':'vectorcraft-fixed-brand-edges/v1','result':'PASS','pluginVersion':host['pluginVersion'],'sourceCommit':host['skillSourceCommit'],
        'installedSkillSha256':entry['sha256'],'qaInstrumentedSkillSha256':digest(instrumented),'driverSha256':sha(Path(__file__)),
        'cases':records,'scope':'actual fixed install, two routes, closed path and target-value faults, original checkpoint readonly reopen, no_effect and verified_noop; technical evidence only'}
    (root/'proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print('PASS',len(records),'fixed brand boundary cases')


if __name__=='__main__':main()
