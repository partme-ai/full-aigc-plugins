#!/usr/bin/env python3
"""只读探测固定二进制；默认首用允许固定安装，不升级、不发送编辑请求。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    request=json.load(sys.stdin)
    skill=Path(request['skill']).resolve()
    if request.get('install'):
        # 普通任务先沿用独立技能的计划验证，再进行固定版本安装；不激活别的版本。
        spec=importlib.util.spec_from_file_location('craft_runtime_preflight',skill/'scripts/workflow.py')
        workflow=importlib.util.module_from_spec(spec);spec.loader.exec_module(workflow)
        workflow.validate(request['plan'])
        spec=importlib.util.spec_from_file_location('craft_runtime_install',skill/'scripts/bootstrap.py')
        bootstrap=importlib.util.module_from_spec(spec);spec.loader.exec_module(bootstrap)
        installed=bootstrap.install(json.loads((skill/'scripts/runtime.lock.json').read_text()),request['runtimeHome'])
        executable=Path(installed['executable'])
    else:
        executable=Path(request['executable'])
    if executable.is_symlink() or not executable.is_file():
        raise ValueError('invalid_runtime_executable')
    lock=json.loads((skill/'scripts/runtime.lock.json').read_text())
    artifact=lock['artifacts'][request['platform']]
    expected=artifact['binarySha256']
    if digest(executable)!=expected:
        raise ValueError('runtime_identity_mismatch')
    version=subprocess.check_output([str(executable.resolve()),'--version'],timeout=10,text=True).strip()
    if version!=artifact['versionOutput']:
        raise ValueError('runtime_version_mismatch')
    spec=importlib.util.spec_from_file_location('craft_runtime_probe_session',skill/'scripts/mcp_session.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    # 沿用固定技能的连接校验和已验证的桌面注册表规范化；不回退headless。
    mode=request['requirements']['mode']
    argv=module._commands.backend_argv(str(executable.resolve()),Path('.'),mode,request.get('connect'))
    session=module.Session(argv,timeout=10)
    try:
        tools=session.request('tools/list',{})['tools']
        commands=module._commands.runtime_rows(session,mode=mode)
    finally:
        session.close()
    if digest(executable)!=expected:
        raise ValueError('runtime_identity_changed')
    return {'schema':'vectorcraft-runtime-probe/v1','mode':mode,'version':version,
            'binarySha256':expected,'commands':commands,'tools':tools}


if __name__=='__main__':
    print(json.dumps(main(),ensure_ascii=False,allow_nan=False))
