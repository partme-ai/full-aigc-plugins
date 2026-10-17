"""使用已验证的原Python只读核对权威任务，再交接原控制器；不安装当前Python。"""
import importlib.util
from pathlib import Path
import sys
import json


def main():
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,"reconfigure"):stream.reconfigure(encoding="utf-8")
    here=Path(__file__).parent
    def load(name):
        spec=importlib.util.spec_from_file_location('preflight_'+name,here/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
    managed=load('managed');args=managed.parser().parse_args()
    # 入口参数解析复用管理层；解析入口由管理层提供，不另建公开参数契约。
    if args.action not in ('resume','reconcile','review','revise','inspect','cancel'):raise ValueError('bound_entry_action_invalid')
    store=load('task_store').Store(args.state_root);binding=load('runtime_binding')
    bound=binding.resolve(store,args.task);binding.verify_entry(store,args.task,Path(bound['script']).parent.parent)
    if Path(sys.executable).resolve()!=Path(bound['python']).resolve():raise ValueError('bound_entry_python_mismatch')
    binding.handoff(store,args,here/'task_entry.py')

if __name__=='__main__':
    try:main()
    except (OSError,ValueError,KeyError,TypeError) as error:
        print(json.dumps({'error':str(error),'result':'failed'},ensure_ascii=False));raise SystemExit(1)
