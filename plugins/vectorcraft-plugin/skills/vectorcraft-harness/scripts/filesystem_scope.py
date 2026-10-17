"""固定 macOS 原生进程的文件能力；策略只来自可信调用层，不来自计划参数。"""
import json
from pathlib import Path
import platform

SYSTEM_READ_ROOTS=('/System/Library','/usr/lib','/usr/share','/Library/Fonts','/Library/ColorSync','/Library/Apple')
SYSTEM_READ_FILES=('/dev/null','/dev/zero','/dev/random','/dev/urandom','/private/etc/localtime','/private/etc/passwd')

def physical(value):
    if not isinstance(value,(str,Path)) or not str(value) or any(ord(c)<32 for c in str(value)):
        raise ValueError('invalid_filesystem_root')
    path=Path(value)
    if not path.is_absolute():raise ValueError('absolute_filesystem_root_required')
    return str(path.resolve())

def profile(executable, policy):
    """生成只读资源与显式工程写入范围；未知字段、相对路径和超长策略拒绝。"""
    if not isinstance(policy,dict) or set(policy)-{'readRoots','writeRoots','resources','ports','graphics'}:
        raise ValueError('invalid_filesystem_policy')
    if type(policy.get('graphics',False)) is not bool:raise ValueError('invalid_filesystem_graphics')
    exe=physical(executable);roots={}
    for name in ('readRoots','writeRoots','resources'):
        values=policy.get(name,[])
        if not isinstance(values,list) or len(values)>256:raise ValueError('invalid_filesystem_policy')
        roots[name]=sorted(set(map(physical,values)))
    ports=policy.get('ports',[])
    if not isinstance(ports,list) or any(type(p) is not int or not 1024<=p<=65535 for p in ports):raise ValueError('invalid_filesystem_ports')
    quote=lambda value:json.dumps(value,ensure_ascii=False)
    read=sorted(set(SYSTEM_READ_ROOTS)|set(roots['readRoots'])|set(roots['writeRoots'])|set(roots['resources']))
    literal=sorted(set(SYSTEM_READ_FILES)|{exe})
    # /var、/tmp 等系统别名只获得祖先元数据，不获得子树读取权限。
    lexical=[str(executable)]+[str(value) for name in ('readRoots','writeRoots','resources') for value in policy.get(name,[])]
    ancestors=sorted({str(parent) for value in read+literal+lexical for parent in Path(value).parents})
    lines=['(version 1)','(deny default)','(allow process-exec (literal '+quote(exe)+'))',
           '(allow process-fork)','(allow file-read-data (literal "/"))','(allow signal)','(allow sysctl-read)','(allow mach-lookup)',
           '(allow file-read* '+ ' '.join('(subpath '+quote(p)+')' for p in read)+' '+ ' '.join('(literal '+quote(p)+')' for p in literal)+')',
           '(allow file-read-metadata '+' '.join('(literal '+quote(p)+')' for p in ancestors)+')',
           '(allow file-write* (literal "/dev/null") '+ ' '.join('(subpath '+quote(p)+')' for p in roots['writeRoots'])+')']
    if policy.get('graphics',False):
        # 固定 macOS arm64 Metal/窗口资源；不允许任意 IOKit 客户端。
        lines += ['(allow iokit-get-properties)',
                  '(allow iokit-open (iokit-user-client-class "IOSurfaceRootUserClient") (iokit-user-client-class "AGXDeviceUserClient") (iokit-user-client-class "AGXSharedUserClient") (iokit-user-client-class "IOHIDParamUserClient"))']
    for port in sorted(set(ports)):
        lines+=['(allow network-outbound (remote ip "localhost:'+str(port)+'"))',
                '(allow network-inbound (local ip "localhost:'+str(port)+'"))',
                '(allow network-bind (local ip "localhost:'+str(port)+'"))']
    text='\n'.join(lines)
    if len(text.encode())>60000:raise ValueError('filesystem_policy_too_large')
    return text

def launch(argv,policy):
    """不支持的平台不退回未受限的原生执行；调用方保留原有生命周期控制。"""
    if platform.system()!='Darwin':raise ValueError('filesystem_adapter_platform_unqualified')
    if not isinstance(argv,list) or not argv or not isinstance(argv[0],str):raise ValueError('invalid_native_argv')
    return ['/usr/bin/sandbox-exec','-p',profile(argv[0],policy),*argv]

# 路径字段来自固定 VectorCraft 命令合同；几何对象的 path/paths 参数不是文件。
READ_FIELDS = {
    'file.open': ('path',), 'document.open': ('path',), 'document.pdfInfo': ('path',),
    'file.newFromTemplate': ('path',), 'file.place': ('path',), 'file.place.info': ('path',),
    'file.place.queue': ('paths',), 'links.relink': ('path', 'folder'),
    'color.loadProfile': ('path',), 'swatch.library.load': ('path',),
    'graphicStyle.loadLibrary': ('path',), 'flattener.presets.import': ('path',),
    'pdf.preset.import': ('path',),
}
WRITE_FIELDS = {
    command: ('folder',) if command in ('file.package', 'file.exportForScreens', 'document.exportForScreens') else ('path',)
    for command in ('file.save', 'document.save', 'file.saveAs', 'file.saveCopy', 'file.saveAsTemplate',
                    'file.export', 'document.export', 'document.exportSelection', 'document.exportDxf',
                    'document.exportForOffice', 'file.exportForScreens', 'document.exportForScreens',
                    'file.package', 'links.unembed', 'swatch.library.save', 'graphicStyle.saveLibrary',
                    'flattener.presets.export', 'pdf.preset.export')
}

def authorize_command(command, params, policy):
    """已知文件命令在发送前拒绝越界，避免 GUI 后台保存先返回受理成功。

    未显式携带路径的原生行为及未知命令仍由内核策略约束；不把异步受理当作落盘证明。
    """
    if not isinstance(params, dict):
        return
    for mode, fields in (('read', READ_FIELDS.get(command, ())), ('write', WRITE_FIELDS.get(command, ()))):
        roots = policy.get('writeRoots', [])
        if mode == 'read':
            roots = roots + policy.get('readRoots', []) + policy.get('resources', [])
        authorized = [Path(physical(root)) for root in roots]
        for field in fields:
            if field not in params:
                continue
            values = params[field] if field == 'paths' else [params[field]]
            if not isinstance(values, list):
                raise ValueError('invalid_native_filesystem_path')
            for value in values:
                path = Path(physical(value))
                if not any(path.is_relative_to(root) for root in authorized):
                    raise ValueError('filesystem_' + mode + '_outside_root')
