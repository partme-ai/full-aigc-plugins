#!/usr/bin/env python3
"""透明度固定安装验收：对象参数、蒙版拓扑、临时编辑层及原生重开。"""
import copy
import importlib.util
import json
from pathlib import Path
import sys

def load_local(name):
    spec=importlib.util.spec_from_file_location('transparency_'+name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
paint=load_local('command_paint')
FAMILY='transparency'
COMMANDS=['transparency.'+x for x in ('set','makeOpacityMask','releaseOpacityMask','disableOpacityMask','enableOpacityMask','unlinkOpacityMask','linkOpacityMask','setOpacityMask','toggleNewMasksClipping','toggleNewMasksInverted','opacityMaskInfo','info','togglePageIsolatedBlending','togglePageKnockoutGroup','editOpacityMask','stopEditingOpacityMask','viewOpacityMask')]
def stable(model):return {k:v for k,v in model.items() if k!='metadata'}
def node(model):
    def walk(n):
        if n['id']==2:return n
        for child in n['kind'].get('children',[]):
            found=walk(child)
            if found is not None:return found
    return next(found for layer in model['layers'] if (found:=walk(layer)) is not None)
def layers_without_edit(model):return [l for l in model['layers'] if l.get('name')!='Opacity Mask Editing']
def saved(model):return {**stable(model),'layers':layers_without_edit(model)}
def expected_info(model,editing):
    n=node(model)
    return {'ids':[2],'opacity':round(n.get('opacity',1)*100,2),'blend':n.get('blend','Normal'),'isolate':n.get('isolate',False),'knockout':n.get('knockout','neutral'),'knockoutShape':n.get('knockout_shape',False),'editingMask':editing,'pageIsolatedBlending':model.get('page_isolate',False),'pageKnockoutGroup':model.get('page_knockout',False)}
def mask_info(model):
    m=node(model).get('mask')
    return [] if m is None else [{'id':2,**{k:m[k] for k in ('clip','invert','disabled','linked')},'art':m['art']['id']}]
def validate_transition(command,s):
    """按固定引擎语义计算模型；只有编辑入口允许已核实的临时层及新ID。"""
    if command not in COMMANDS:raise ValueError('transparency_command_unknown')
    b,a,r=(s[k] for k in ('before','after','reopened'));p=s['params'];ret=s['returned'];o=s['observed'];name=command.split('.')[1]
    if saved(a)!=stable(r):raise ValueError('transparency_reopen')
    expected=copy.deepcopy(b);n=node(expected);editing=None
    if name=='set':
        if p.get('item','absent') is not None:raise ValueError('transparency_object_item')
        n.update(opacity=p['opacity']/100,blend=p['blend'],isolate=p['isolate'],knockout=p['knockout'],knockout_shape=p['knockoutShape'])
        for key in ('isolate','knockout_shape'):
            if n[key] is False:n.pop(key)
        if abs(node(a).get('opacity',1)-n['opacity'])<1e-6:n['opacity']=node(a).get('opacity',1)
    elif name=='makeOpacityMask':
        mid=s['fixture']['maskId'];art=copy.deepcopy(paint.objects(b)[mid]);n['mask']={'art':art,'clip':p['clip'],'invert':p['invert'],'disabled':False,'linked':True}
        for layer in expected['layers']:layer['kind']['children']=[x for x in layer['kind']['children'] if x['id']!=mid]
        if ret!={'id':2,'editing':False}:raise ValueError('transparency_make_result')
    elif name=='releaseOpacityMask':
        art=n.pop('mask')['art'];art['id']=b['next_id'];expected['next_id']=b['next_id']+1
        children=expected['layers'][0]['kind']['children'];index=next(i for i,x in enumerate(children) if x['id']==2);children.insert(index+1,art)
    elif name in ('disableOpacityMask','enableOpacityMask','unlinkOpacityMask','linkOpacityMask','setOpacityMask'):
        updates={'disableOpacityMask':{'disabled':True},'enableOpacityMask':{'disabled':False},'unlinkOpacityMask':{'linked':False},'linkOpacityMask':{'linked':True}}.get(name,{k:v for k,v in p.items() if k in ('clip','invert','disabled','linked')})
        n['mask'].update(updates)
    elif name.startswith('togglePage'):
        key='page_isolate' if name=='togglePageIsolatedBlending' else 'page_knockout'
        if p['value']:expected[key]=True
        else:expected.pop(key,None)
        if ret!={'value':p['value']}:raise ValueError('transparency_page_result')
    elif name.startswith('toggleNewMasks'):
        key='clip' if name=='toggleNewMasksClipping' else 'invert'
        probe=o['defaultProbe'];actual=paint.objects(probe['document'])[probe['target']]['mask']
        if probe['mask']!=actual:raise ValueError('transparency_default_model_binding')
        if ret!={'value':p['value']} or o['defaultProbe']['mask'][key] is not p['value'] or o['defaultProbe']['restoredOriginal'] is not True or o['preferenceRestartAcceptance']!='NOT_RUN':raise ValueError('transparency_default_probe')
    elif name in ('editOpacityMask','viewOpacityMask'):
        editing=2
        if name=='editOpacityMask' or p['on']:
            lid=b['next_id'];aid=lid+1;art=copy.deepcopy(n['mask']['art']);art['id']=aid;n['mask']['art']=art
            temporary=[l for l in a['layers'] if l.get('name')=='Opacity Mask Editing']
            if len(temporary)!=1 or temporary[0]['id']!=lid or temporary[0]['kind'].get('children')!=[art]:raise ValueError('transparency_edit_layer')
            expected['layers'].append(copy.deepcopy(temporary[0]));expected['next_id']=lid+2
        if name=='editOpacityMask' and ret!={'layer':b['next_id']}:raise ValueError('transparency_edit_result')
        if name=='viewOpacityMask' and ret!={'id':2,'on':p['on']}:raise ValueError('transparency_view_result')
    elif name=='stopEditingOpacityMask':
        expected['layers']=layers_without_edit(expected)
        if ret!={'id':2}:raise ValueError('transparency_stop_result')
    # 其余查询不得改变原生模型；严格保全所有控制对象和未授权字段。
    if stable(expected)!=stable(a):raise ValueError('transparency_native_semantics')
    if o['info']!=expected_info(a,editing):raise ValueError('transparency_info')
    if o['maskInfo']!=mask_info(a):raise ValueError('transparency_mask_info')
    if name=='info' and ret!=o['info']:raise ValueError('transparency_query_info')
    if name=='opacityMaskInfo' and ret!=o['maskInfo']:raise ValueError('transparency_query_mask')

def initialize(call):
    call('paint.setFill',ids=[2],color='#224466');return {}
def prepare(call,command,number,directory,state):
    name=command.split('.')[1];second=number==2;fixture={}
    if name not in ('set','makeOpacityMask','toggleNewMasksClipping','toggleNewMasksInverted','togglePageIsolatedBlending','togglePageKnockoutGroup','info'):
        if not call('transparency.opacityMaskInfo',id=2):
            mid=call('shape.rectangle',x=12,y=12,width=30,height=36)['id'];call('paint.setFill',ids=[mid],color='#808080');call('transparency.makeOpacityMask',ids=[2,mid],clip=True,invert=False)
    if name=='set':p={'ids':[2],'item':None,'opacity':35 if second else 60,'blend':'Screen' if second else 'Multiply','isolate':not second,'knockout':'on' if second else 'off','knockoutShape':not second}
    elif name=='makeOpacityMask':
        if second:call('transparency.releaseOpacityMask',id=2)
        mid=call('shape.rectangle',x=12,y=12,width=45 if second else 30,height=36)['id'];call('paint.setFill',ids=[mid],color='#cccccc' if second else '#808080');fixture['maskId']=mid;p={'ids':[2,mid],'clip':not second,'invert':second}
    elif name in ('disableOpacityMask','enableOpacityMask','unlinkOpacityMask','linkOpacityMask'):
        opposite={'disableOpacityMask':{'disabled':False},'enableOpacityMask':{'disabled':True},'unlinkOpacityMask':{'linked':True},'linkOpacityMask':{'linked':False}}[name];call('transparency.setOpacityMask',id=2,**opposite);p={'id':2}
    elif name=='setOpacityMask':p={'id':2,'clip':second,'invert':not second,'disabled':not second,'linked':second}
    elif name.startswith('toggle'):p={'value':not second}
    elif name=='stopEditingOpacityMask':call('transparency.editOpacityMask',id=2);p={}
    elif name=='viewOpacityMask':
        if second:call('transparency.viewOpacityMask',id=2,on=True)
        p={'id':2,'on':not second}
    else:p={'id':2}
    call('select.set',ids=[2]);return p,fixture

def observe(call,command,params,returned,directory,fixture):
    result={'info':call('transparency.info',id=2),'maskInfo':call('transparency.opacityMaskInfo',id=2),'preferenceRestartAcceptance':'NOT_RUN'}
    if command in ('transparency.toggleNewMasksClipping','transparency.toggleNewMasksInverted'):
        original=call('document.json');call('file.new',width=128,height=96)
        a=call('shape.rectangle',x=12,y=12,width=60,height=36)['id'];b=call('shape.rectangle',x=12,y=12,width=30,height=36)['id']
        call('transparency.makeOpacityMask',ids=[a,b]);probe=call('document.json');m=paint.objects(probe)[a]['mask'];call('document.save',path=str(directory/'defaults-probe.vectorcraft'),modified=946684800);call('file.close')
        result['defaultProbe']={'document':probe,'target':a,'mask':m,'restoredOriginal':call('document.json')==original}
    return result
if __name__=='__main__':
    common=load_local('command_family');family=type('TransparencyFamily',(),{'FAMILY':FAMILY,'COMMANDS':COMMANDS,'__file__':__file__,**{n:staticmethod(globals()[n]) for n in ('initialize','prepare','observe','validate_transition')}})
    common.run(json.loads(Path(sys.argv[1]).read_text()),family)
