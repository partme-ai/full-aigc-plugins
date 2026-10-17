"""只读探测已验证CLI；不安装、不连接已有桌面、不调用任何编辑或渲染。"""
import importlib.util
from pathlib import Path
import subprocess


def load(name):
    spec=importlib.util.spec_from_file_location('diagnostic_'+name,Path(__file__).with_name(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def observe(executable,catalog,expected_version):
    """调用者须先核对完整性及系统条件；仅启动本次拥有的空headless会话，异常不重试。"""
    result={'status':'NOT_RUN','scope':'readonly native version, registry identity and tool input-schema discovery only',
            'executionAcceptance':'NOT_RUN','mode':'headless','desktopAcceptance':'NOT_RUN'}
    try:
        version=subprocess.run([str(executable),'--version'],capture_output=True,text=True,encoding='utf-8',timeout=5)
        result['actualVersionOutput']=version.stdout.strip()
        if version.returncode!=0 or result['actualVersionOutput']!=expected_version:
            raise ValueError('native_version_mismatch')
        with load('mcp_session').Session([str(executable),'--empty','mcp'],timeout=15) as session:
            reply=session.request('tools/list',{})
            tools=reply.get('tools') if isinstance(reply,dict) else None
            if (not isinstance(tools,list) or any(not isinstance(t,dict) or not isinstance(t.get('name'),str)
                    or not isinstance(t.get('inputSchema'),dict) for t in tools)
                    or len({t['name'] for t in tools})!=len(tools)):raise ValueError('native_tool_identity_invalid')
            reply=session.request('tools/call',{'name':'list_commands','arguments':{}})
            if not isinstance(reply,dict) or reply.get('isError'):raise ValueError('native_registry_query_failed')
            content=reply.get('content')
            if not isinstance(content,list):raise ValueError('native_command_identity_invalid')
            texts=[c['text'] for c in content if isinstance(c,dict) and c.get('type')=='text' and isinstance(c.get('text'),str)]
            if len(texts)!=1:raise ValueError('native_command_identity_invalid')
            data=load('commands').reply_json(texts[0]);rows=data.get('commands') if isinstance(data,dict) else data
            if (not isinstance(rows,list) or any(not isinstance(r,dict) or not isinstance(r.get('id'),str) or not r['id'] for r in rows)
                    or len({r['id'] for r in rows})!=len(rows)):raise ValueError('native_command_identity_invalid')
        current={t['name']:t['inputSchema'] for t in tools};expected=catalog['nativeToolSchemas']
        old_ids={r['id'] for r in catalog['commands']};new_ids={r['id'] for r in rows}
        changed=sorted(n for n in current.keys()&expected.keys() if current[n]!=expected[n])
        result.update(commandCount=len(rows),toolCount=len(tools),missingCommands=sorted(old_ids-new_ids),addedCommands=sorted(new_ids-old_ids),
                      missingTools=sorted(expected.keys()-current.keys()),addedTools=sorted(current.keys()-expected.keys()),changedTools=changed)
        result['status']='FAIL' if any(result[k] for k in ('missingCommands','addedCommands','missingTools','addedTools','changedTools')) else 'PASS'
    except ValueError as error:
        result.update(status='FAIL',error=str(error))
    except (OSError,RuntimeError,TimeoutError,subprocess.SubprocessError) as error:
        result.update(status='NOT_RUN',error=type(error).__name__+': '+str(error))
    return result
