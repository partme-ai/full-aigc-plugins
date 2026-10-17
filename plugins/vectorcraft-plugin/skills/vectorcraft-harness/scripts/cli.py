#!/usr/bin/env python3
"""从当前独立技能安装/核验固定 CLI，然后按 argv 调用；不依赖 PATH 或兄弟技能。"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
sys.dont_write_bytecode=True
import importlib.util

def _native_environment():
    # 计划和安装锁的原有错误诊断先执行；进入原生进程前安全资源必须存在。
    import runpy
    security=runpy.run_path(str(Path(__file__).with_name('input_security.py')))
    return security['native_environment']()

ALLOWED={'--version', 'perf', 'help', 'info', 'mcp', 'convert', 'commands', 'run', 'bench'}
def setup_failure(runtime_home):
 """安装器缺失时也保留当前技能自身的恢复位置，不读取兄弟技能。"""
 return {'skill':'vectorcraft-cli-setup','bootstrapScript':str(Path(__file__).with_name('bootstrap.py').resolve()),'runtimeHome':str(Path(runtime_home).expanduser().absolute()),'automaticRetry':False}
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--runtime-home',default=os.environ.get('CRAFT_RUNTIME_HOME',str(Path.home()/'.local/share/craft-runtimes')))
 parser.add_argument('--archive',type=Path)
 parser.add_argument('--read-root',action='append',default=[],help='trusted authorized native input root; repeatable')
 parser.add_argument('--write-root',action='append',default=[],help='trusted authorized native output root; repeatable')
 parser.add_argument('arguments',nargs=argparse.REMAINDER)
 args=parser.parse_args();argv=args.arguments
 if argv[:1]==['--']:argv=argv[1:]
 if not argv or argv[0] not in ALLOWED:parser.error('unsupported_cli_subcommand: put the native subcommand first after --')
 installation_completed=False
 try:
  path=Path(__file__).with_name('bootstrap.py');spec=importlib.util.spec_from_file_location('craft_bootstrap',path)
  module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  installed=module.install(json.loads(path.with_name('runtime.lock.json').read_text()),args.runtime_home,args.archive)
  installation_completed=True
  import runpy
  filesystem=runpy.run_path(str(Path(__file__).with_name('filesystem_scope.py')))
  launch=filesystem['launch']([installed['executable'],*argv],{'readRoots':args.read_root,'writeRoots':args.write_root})
  result=subprocess.run(launch,timeout=600,env=_native_environment())
  return result.returncode
 except (ValueError,OSError,subprocess.SubprocessError) as error:
  reply={'error':str(error),'result':'unknown' if isinstance(error,subprocess.TimeoutExpired) else 'failed'}
  if not installation_completed:reply['dependencySetup']=setup_failure(args.runtime_home)
  print(json.dumps(reply));return 1
if __name__=='__main__':raise SystemExit(main())
