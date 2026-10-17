"""使用技能自带返回ID绑定脚本驱动真实FigCraft CLI，重开检查节点与布局。"""
import importlib.util
import json
import math
from pathlib import Path
import struct
import xml.etree.ElementTree as ET


def require(ok,message):
    if not ok:raise AssertionError(message)


def near(a,b):return math.isclose(a,b,abs_tol=0.02)


def verify(nodes,bindings,a):
    root=nodes['root'];require(all(near(root[k],v) for k,v in zip(('width','height'),a['rootSize'])),'Root size wrong')
    children={c['id'] for c in root.get('children',[])}
    for name in a.get('children',[]):require(bindings[name]['id'] in children,'Node is outside target frame: '+name)
    texts=[n.get('characters') for n in nodes.values()]
    for value in a.get('texts',[]):require(value in texts,'Editable text lost: '+value)
    for parent,names in a.get('nested',{}).items():
        ids={c['id'] for c in nodes[parent].get('children',[])}
        for name in names:require(bindings[name]['id'] in ids,'Nested child lost')
    if 'layout' in a:
        expected=a['layout'];layout=root.get('layout',{})
        require(str(layout.get('mode','')).lower()==expected['mode'],'Auto layout mode lost')
        require(near(layout['gap'],expected['gap']),'Auto layout gap lost')
        axis,size=('x','width') if expected['mode']=='horizontal' else ('y','height')
        for prev,next_name in zip(a['children'],a['children'][1:]):
            first,last=nodes[prev],nodes[next_name]
            require(near(last[axis]-first[axis]-first[size],expected['gap']),'Actual auto layout spacing wrong')
    for name,width in a.get('fillWidths',{}).items():
        require(near(nodes[name]['width'],width),'Fill width did not respond to container resize')
        require(near(nodes[name]['x'],24),'Responsive left padding lost')
    if a.get('component'):require('component' in root['type'].lower(),'Card is not component')
    if a.get('errorStroke'):require(nodes[a['errorStroke']].get('strokes'),'Error border lost')


def read_nodes(r,target,bindings):
    steps=[{'command':'node.get','params':{'id':v['id']}} for v in bindings.values()]
    script=r.work/'inspect-nodes.json';script.write_text(json.dumps(steps),encoding='utf-8')
    rows=[json.loads(x) for x in r.run('run',script,'--in',target).splitlines()]
    require(len(rows)==len(bindings) and all(x['ok'] for x in rows),'Node query failed')
    return {key:row['result'] for key,row in zip(bindings,rows)}


def run_playbooks(r,path):
    path=Path(path);data=json.loads(path.read_text(encoding='utf-8'));require(data['application']=='figcraft','Wrong app')
    helper=path.parent.parent/'scripts/run_recipe.py';spec=importlib.util.spec_from_file_location('fig_recipe',helper);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    records=[]
    for recipe in data['recipes']:
        target=recipe['id']+'.figcraft';receipt=m.execute_recipe(recipe,r.run,r.work,r.work/target)
        bindings=receipt['bindings'];nodes=read_nodes(r,target,bindings);verify(nodes,bindings,recipe['assertions'])
        (r.work/(recipe['id']+'-nodes.json')).write_text(json.dumps(nodes,ensure_ascii=False,indent=2),encoding='utf-8')
        if recipe['assertions'].get('component'):
            script=r.work/'components.json';script.write_text('[{"command":"component.list","params":{}}]')
            result=json.loads(r.run('run',script,'--in',target).splitlines()[0])['result'];require(any(x['id']==bindings['root']['id'] for x in result),'Component registry missing card')
        root_id=str(bindings['root']['id']);png=recipe['id']+'.png';svg=recipe['id']+'.svg'
        r.run('export',target,'--node',root_id,'-o',png,'--format','png')
        require(list(struct.unpack('>II',(r.work/png).read_bytes()[16:24]))==recipe['assertions']['rootSize'],'Root export pixel size wrong')
        r.run('export',target,'--node',root_id,'-o',svg,'--format','svg');ET.fromstring((r.work/svg).read_bytes())
        records.append({'id':recipe['id'],'technicalRoundtrip':'PASS','returnedIdBinding':'PASS','layoutStructure':'PASS','designReview':'NOT_TESTED'})
    require(bool(records),'No Fig scenes');return records
