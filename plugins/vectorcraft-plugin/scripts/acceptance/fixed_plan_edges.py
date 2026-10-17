#!/usr/bin/env python3
"""在实际安装入口验证歧义计划于安装运行时及输出创建前失败。"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from fixed_install import digest


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--host',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();root=args.output.resolve();root.mkdir(parents=True,exist_ok=False)
    host=json.loads(args.host.read_text());entry=next(x for x in host['skills'] if x['name']=='vectorcraft-use');skill=Path(entry['path']);assert digest(skill)==entry['sha256']
    values={'duplicate-top':'{"operations":[],"operations":[]}', 'duplicate-nested':'{"operations":[],"nested":{"x":1,"x":2}}',
        'nan':'{"operations":[],"value":NaN}', 'infinity':'{"operations":[],"value":Infinity}', 'overflow':'{"operations":[],"value":1e999}'}
    records=[]
    for script in ('commands.py','workflow.py'):
        for name,text in values.items():
            case=root/(script+'-'+name);case.mkdir();plan=case/'plan.json';plan.write_text(text);output=case/'output';runtime=case/'empty runtime'
            argv=[sys.executable,'-I','-B',str(skill/'scripts'/script)]
            if script=='commands.py':argv+=['run']
            argv+=[str(plan),'--output',str(output),'--runtime-home',str(runtime)]
            result=subprocess.run(argv,capture_output=True,text=True,timeout=30)
            (case/'stdout.log').write_text(result.stdout);(case/'stderr.log').write_text(result.stderr)
            assert result.returncode==1 and isinstance(json.loads(result.stdout)['error'],str),result.stdout+result.stderr
            assert not runtime.exists() and not output.exists()
            records.append({'entry':script,'fault':name,'result':'PASS','error':json.loads(result.stdout)['error'],'outputAbsent':True,'runtimeAbsent':True})
    assert digest(skill)==entry['sha256']
    proof={'schema':'vectorcraft-fixed-plan-preflight/v1','result':'PASS','pluginVersion':host['pluginVersion'],
        'installedSkillSha256':entry['sha256'],'driverSha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'cases':records}
    (root/'proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print('PASS',len(records),'preflight cases')


if __name__=='__main__':main()
