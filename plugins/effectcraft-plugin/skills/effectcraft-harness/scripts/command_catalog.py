"""离线核对固定命令目录；差异不是执行或宿主验收证据。"""
import copy
import json
import re

FIELDS=('label','params','ownerSkill','workflowMapped','runModes')


def validate(value):
    """拒绝歧义身份、缺失参数合同及重复目录，不运行任何原生进程。"""
    if (not isinstance(value,dict) or value.get('schema')!='craft-command-coverage/v1'
            or value.get('pluginId')!='effectcraft' or not isinstance(value.get('runtimeSha256'),str)
            or not re.fullmatch('[a-f0-9]{64}',value['runtimeSha256'])
            or not isinstance(value.get('commands'),list) or not isinstance(value.get('nativeTools'),list)):
        raise ValueError('command_catalog_invalid')
    identifiers=set()
    for row in value['commands']:
        if (not isinstance(row,dict) or not isinstance(row.get('id'),str) or not row['id'] or row['id'] in identifiers
                or any(k not in row for k in FIELDS if k!='runModes')
                or not isinstance(row['label'],str) or not isinstance(row['ownerSkill'],str)
                or (row['params'] is not None and not isinstance(row['params'],str))
                or type(row['workflowMapped']) is not bool
                or ('runModes' in row and not isinstance(row['runModes'],dict))):
            raise ValueError('command_catalog_invalid')
        identifiers.add(row['id'])
        for mode,contract in row.get('runModes',{}).items():
            if mode not in ('headless','desktop') or not isinstance(contract,dict):raise ValueError('command_catalog_invalid')
    tools=value['nativeTools']
    if any(not isinstance(t,str) or not t for t in tools) or len(set(tools))!=len(tools):raise ValueError('command_catalog_invalid')
    if 'nativeToolSchemas' in value:
        schemas=value['nativeToolSchemas']
        if not isinstance(schemas,dict) or set(schemas)!=set(tools) or any(not isinstance(s,dict) for s in schemas.values()):
            raise ValueError('command_catalog_invalid')
    try:json.dumps(value,allow_nan=False)
    except (TypeError,ValueError):raise ValueError('command_catalog_invalid') from None
    return value


def contract(row):
    """只提取调用合同，绝不从历史目录继承PASS声明。"""
    result={key:copy.deepcopy(row[key]) for key in FIELDS if key in row}
    for mode in result.get('runModes',{}).values():mode['acceptance']='NOT_RUN'
    return result


def compare(before,after):
    """返回稳定排序的新增/移除/变化及重验清单；缺少旧工具schema时明确NOT_RUN。"""
    validate(before);validate(after)
    old={r['id']:r for r in before['commands']};new={r['id']:r for r in after['commands']}
    added=sorted(new.keys()-old.keys());removed=sorted(old.keys()-new.keys());changed=[];unchanged=[]
    for name in sorted(old.keys()&new.keys()):
        a=contract(old[name]);b=contract(new[name]);fields=sorted(k for k in FIELDS if (k in a)!=(k in b) or a.get(k)!=b.get(k))
        if fields:changed.append({'id':name,'changedFields':fields,'before':a,'after':b,'executionAcceptance':'NOT_RUN'})
        else:unchanged.append(name)
    old_tools=set(before['nativeTools']);new_tools=set(after['nativeTools'])
    schemas_present='nativeToolSchemas' in before and 'nativeToolSchemas' in after
    schema_changed=(sorted(n for n in old_tools&new_tools if before['nativeToolSchemas'][n]!=after['nativeToolSchemas'][n]) if schemas_present else None)
    runtime_changed=before['runtimeSha256']!=after['runtimeSha256']
    revalidate=sorted(new) if runtime_changed else sorted(set(added)|{r['id'] for r in changed})
    if old_tools!=new_tools or not schemas_present or schema_changed:revalidate=sorted(new)
    additions=[]
    for name in added:
        row={'id':name,**contract(new[name]),'executionAcceptance':'NOT_RUN'}
        for mode in row.get('runModes',{}).values():mode['acceptance']='NOT_RUN'
        additions.append(row)
    return {'schema':'effectcraft-command-diff/v1','pluginId':'effectcraft',
            'beforeRuntimeSha256':before['runtimeSha256'],'afterRuntimeSha256':after['runtimeSha256'],
            'runtimeChanged':runtime_changed,'executionAcceptance':'NOT_RUN',
            'scope':'offline contract comparison only; no installation, native calls or acceptance inheritance',
            'commands':{'added':additions,'removed':removed,'changed':changed,'unchanged':unchanged},
            'tools':{'added':sorted(new_tools-old_tools),'removed':sorted(old_tools-new_tools),
                     'schemaComparison':'COMPARED' if schemas_present else 'NOT_RUN','schemaChanged':schema_changed},
            'requiresRevalidation':revalidate}
