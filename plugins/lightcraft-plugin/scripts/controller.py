"""显式 Lightcraft 任务控制器；宿主和原生安装不是静态校验的副作用。"""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess

path = Path(__file__).with_name('task_core.py')
spec = importlib.util.spec_from_file_location('task_core',path)
core = importlib.util.module_from_spec(spec); spec.loader.exec_module(core)


def read(path):
    return core.module('command_gateway').strict_json(Path(path).read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['init','status','inspect','run','reconcile','stop','remaining','review-request','review','revise','deliver','session-inspect','raw-inspect','sam-inspect','craft-inspect','mobile-prepare','mobile-inspect'])
    parser.add_argument('task',type=Path)
    parser.add_argument('--payload',type=Path)
    parser.add_argument('--runtime-home',type=Path)
    args=parser.parse_args()
    try:
        payload=read(args.payload) if args.payload else {}
        action=args.action
        if action in ('mobile-prepare','mobile-inspect'):
            source=Path(__file__).with_name('mobile_delivery.py')
            mobile_spec=importlib.util.spec_from_file_location('mobile_delivery',source)
            mobile=importlib.util.module_from_spec(mobile_spec);mobile_spec.loader.exec_module(mobile)
            if action=='mobile-prepare':
                if set(payload)!={'report','report_sha256'}:raise ValueError('explicit_mobile_source_required')
                result=mobile.prepare(args.task,**payload)
            else:
                if payload:raise ValueError('mobile_inspect_has_no_write_payload')
                result=mobile.inspect(args.task)
        elif action=='craft-inspect':
            native=subprocess.run(['node',str(Path(__file__).with_name('craft_exchange.ts')),str(args.task)],capture_output=True,text=True)
            if native.returncode:raise ValueError('craft_inspection_failed: '+native.stdout.strip()+native.stderr.strip())
            result=core.module('command_gateway').strict_json(native.stdout)
            if result.get('executionAllowed') is not False or result.get('automaticReplay') is not False:raise ValueError('craft_inspection_permissions_invalid')
            result['taskExecutionAllowed']=False
        elif action=='sam-inspect':
            source=Path(__file__).with_name('sam_facts.py')
            sam_spec=importlib.util.spec_from_file_location('sam_facts',source)
            sam=importlib.util.module_from_spec(sam_spec);sam_spec.loader.exec_module(sam)
            result=sam.inspect_sam(args.task)
        elif action=='raw-inspect':
            source=Path(__file__).with_name('raw_facts.py')
            raw_spec=importlib.util.spec_from_file_location('raw_facts',source)
            raw=importlib.util.module_from_spec(raw_spec);raw_spec.loader.exec_module(raw)
            result=raw.inspect_raw(args.task)
        elif action=='session-inspect':
            source=Path(__file__).with_name('session_facts.py')
            session_spec=importlib.util.spec_from_file_location('session_facts',source)
            session=importlib.util.module_from_spec(session_spec);session_spec.loader.exec_module(session)
            result=session.inspect_session(args.task)
        elif action=='init': result=core.create(args.task,**payload)
        elif action in ('status','inspect'): result=core.inspect(args.task)
        elif action=='run': result=core.run(args.task,args.runtime_home)
        elif action=='review-request': result=core.review_request(args.task,**payload)
        elif action=='review': result=core.review(args.task,payload)
        elif action=='revise': result=core.revise(args.task,**payload)
        else: result=getattr(core,action)(args.task)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except (ValueError,OSError,KeyError,TypeError,subprocess.SubprocessError) as error:
        print(json.dumps({'error':str(error),'automaticReplay':False},ensure_ascii=False))
        return 1


if __name__=='__main__': raise SystemExit(main())
