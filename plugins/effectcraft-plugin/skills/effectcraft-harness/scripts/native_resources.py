"""只读原生字体／LUT依赖观察；内容、包闭合与保真分别记录。"""
import hashlib
import importlib.util
from pathlib import Path


def load(name):
    spec=importlib.util.spec_from_file_location('native_resources_'+name,Path(__file__).with_name(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def fail(reason):raise ValueError('native_resources: '+reason)
def sha(data):return hashlib.sha256(data).hexdigest()


def closure(inventories):
    reasons=[]
    for inventory in inventories:
        if inventory['fonts']:reasons.append('font_binary_resolution_unverified')
        if inventory['dynamic']:reasons.append('dynamic_resource_values_unverified')
        for lut in inventory['luts']:
            if not lut['packaged']:reasons.append('lut_content_unavailable_in_package')
            elif lut['source']=='file':reasons.append('lut_runtime_path_resolution_unverified')
    return {'status':'NOT_RUN' if reasons else 'PASS','reasons':sorted(set(reasons)),
            'scope':'static declared dependency containment only; visual fidelity NOT_RUN'}


def inspect(root,project,*,declared=None):
    """扫描固定schema1的全部合成属性、字符样式和关键帧；不读取包外文件。"""
    root=Path(root);lineage=load('artifact_lineage');path=lineage.file(root,project)
    if path.stat().st_size>64*1024*1024:fail('project_too_large')
    try:
        data=lineage.read(path)
        if not isinstance(data,dict) or data.get('schema')!=1 or not isinstance(data.get('items'),dict):fail('unsupported_native_schema')
        result={'schema':'effectcraft-native-resources/v1','project':project,'projectSha256':lineage.sha(path),
                'fonts':[],'luts':[],'dynamic':[],'fidelity':'NOT_RUN'}
        declared_luts={}
        if declared is not None:
            if not isinstance(declared,dict) or declared.get('schema')!=result['schema'] or declared.get('project')!=project or declared.get('projectSha256')!=result['projectSha256'] or not isinstance(declared.get('luts'),list):fail('relocation_binding_invalid')
            for resource in declared['luts']:
                if not isinstance(resource,dict) or not isinstance(resource.get('pointer'),str) or resource['pointer'] in declared_luts:fail('relocation_binding_invalid')
                declared_luts[resource['pointer']]=resource
        stack=[]
        for key,item in data['items'].items():
            if not isinstance(item,dict) or not isinstance(item.get('kind'),dict):fail('item_invalid')
            if item['kind']['type']!='Comp':continue
            layers=item['kind'].get('layers',[])
            if not isinstance(layers,list):fail('layers_invalid')
            for index,layer in enumerate(layers):
                if not isinstance(layer,dict):fail('layer_invalid')
                if 'props' in layer:stack.append((layer['props'],f'/items/{key}/kind/layers/{index}/props',None,0))
        nodes=0
        while stack:
            node,pointer,effect,depth=stack.pop();nodes+=1
            if nodes>200000 or depth>64:fail('property_tree_limit')
            if not isinstance(node,dict):fail('property_invalid')
            if 'children' in node:
                children=node['children']
                if not isinstance(children,list):fail('property_children_invalid')
                kind=node.get('kind',{})
                if not isinstance(kind,dict):fail('group_kind_invalid')
                current=kind.get('effect') if kind.get('kind')=='Effect' else effect
                stack.extend((child,pointer+'/children/'+str(i),current,depth+1) for i,child in enumerate(children));continue
            if 'value' not in node:fail('property_value_missing')
            match=node.get('match');is_lut=(effect=='ec.utility.applylut' and match=='lut') or (effect=='ec.color.lumetri' and match in ('inputLutFile','lookFile','basicCorrection/inputLutFile','creative/lookFile'))
            values=[(node['value'],pointer+'/value')];keys=node.get('keys',[])
            if not isinstance(keys,list):fail('property_keys_invalid')
            for index,key in enumerate(keys):
                if not isinstance(key,dict) or 'value' not in key:fail('keyframe_invalid')
                values.append((key['value'],pointer+'/keys/'+str(index)+'/value'))
            for value,where in values:
                if not isinstance(value,dict):fail('typed_value_invalid')
                if value.get('t')=='Text':
                    doc=value.get('v')
                    if not isinstance(doc,dict):fail('text_document_invalid')
                    styles=[(doc,where+'/v')];runs=doc.get('runs',[])
                    if not isinstance(runs,list):fail('text_runs_invalid')
                    for index,run in enumerate(runs):
                        if not isinstance(run,dict) or not isinstance(run.get('style'),dict):fail('text_run_invalid')
                        styles.append((run['style'],where+'/v/runs/'+str(index)+'/style'))
                    for style,location in styles:
                        font=style.get('font','Inter');face=style.get('style','Regular')
                        if not isinstance(font,str) or not isinstance(face,str) or max(len(font),len(face))>512:fail('font_declaration_invalid')
                        result['fonts'].append({'font':font,'style':face,'pointer':location,'status':'NOT_RUN',
                            'missingReason':'Font declaration only; selected binary, fallback glyph faces, licence and portability are unverified.'})
                if is_lut and value.get('t')=='Str':
                    source=value.get('v')
                    if not isinstance(source,str):fail('lut_value_invalid')
                    if source.strip():result['luts'].append(lut_record(root,path,source,where,declared_luts.get(where)))
            expression=node.get('expr')
            if expression is not None:
                if not isinstance(expression,dict):fail('expression_invalid')
                if expression.get('enabled') and (is_lut or any(v.get('t')=='Text' for v,_ in values)):
                    result['dynamic'].append({'pointer':pointer,'kind':'lut' if is_lut else 'font','status':'NOT_RUN','reason':'Expression may select resources beyond static and keyframe declarations.'})
        for key in ('fonts','luts','dynamic'):result[key].sort(key=lambda row:row['pointer'])
        result['closure']=closure([result]);return result
    except (OSError,KeyError,TypeError,RecursionError,ValueError) as error:
        if isinstance(error,ValueError) and str(error).startswith('native_resources:'):raise
        fail(str(error))


def lut_record(root,project,source,pointer,declared=None):
    """内联内容摘要不等同LUT有效性；路径资源不猜测引擎CWD或搬迁保真。"""
    if len(source.encode('utf-8'))>16*1024*1024:fail('lut_value_too_large')
    result={'pointer':pointer,'source':'inline' if '\n' in source or 'LUT_' in source else 'file','packaged':False,'fidelity':'NOT_RUN'}
    if result['source']=='inline':
        result.update(packaged=True,sha256=sha(source.encode('utf-8')),bytes=len(source.encode('utf-8')));return result
    result['runtimeResolution']='NOT_RUN';result['declarationSha256']=sha(source.encode('utf-8'))
    try:
        candidate=Path(source.strip())
        if candidate.is_absolute():
            # 包内绝对地址可以观察内容，但不在报告中保留本机前缀。
            candidate=candidate.relative_to(root)
        else:candidate=project.parent.relative_to(root)/candidate
        name=candidate.as_posix();payload=load('artifact_lineage').file(root,name)
        result.update(packaged=True,path=name,sha256=load('artifact_lineage').sha(payload),bytes=payload.stat().st_size)
    except (ValueError,OSError):result['missingReason']='LUT file missing, linked, unsafe or outside package; not read or copied.'
    if not result['packaged'] and declared and declared.get('packaged') and Path(source.strip()).is_absolute():
        # 只从绑定工程的相同属性声明重关联包内相对文件；不读取旧绝对地址。
        if declared.get('source')!='file' or declared.get('declarationSha256')!=result['declarationSha256']:fail('relocation_declaration_changed')
        payload=load('artifact_lineage').file(root,declared.get('path'))
        if load('artifact_lineage').sha(payload)!=declared.get('sha256') or payload.stat().st_size!=declared.get('bytes'):fail('relocation_content_changed')
        result.pop('missingReason',None);result.update(packaged=True,path=declared['path'],sha256=declared['sha256'],bytes=declared['bytes'])
    return result


def public_dependencies(inventory):
    """只输出已取得真实字节的LUT；未知字体保留私有原因，不伪造公共摘要。"""
    values={}
    for resource in inventory['luts']:
        if not resource['packaged']:continue
        content=resource['sha256'];values[content]={'assetRef':{'assetId':'effectcraft-lut:'+content,'version':content,'sha256':content},
            'kind':'lut','packaged':True,'missingReason':None}
    return [values[key] for key in sorted(values)]
