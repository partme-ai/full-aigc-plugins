#!/usr/bin/env python3
"""固定安装图层验收：独立树变换、会话读回与局部修订，保全控制艺术。"""
import copy
import importlib.util
import json
from pathlib import Path
import sys
FAMILY='layer'
COMMANDS=['layer.'+n for n in ('new','newSublayer','delete','duplicate','setCurrent','setProps','collectInNew','selectAll','clippingMask.toggle','target','pasteRemembersLayers')]
_state={}
def load_local(name):
    spec=importlib.util.spec_from_file_location('layer_'+name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
shape=load_local('command_shape')
def layer(id,name,color):return {'id':id,'name':name,'kind':{'type':'layer','color':{'Preset':color},'template':False,'printable':True,'children':[]}}
def walk(model):
    def visit(nodes):
        for n in nodes:
            yield n
            yield from visit(n['kind'].get('children',[]))
    return list(visit(model['layers']))
def location(model,id):
    def visit(nodes):
        for i,n in enumerate(nodes):
            if n['id']==id:return nodes,i
            value=visit(n['kind'].get('children',[]))
            if value is not None:return value
    result=visit(model['layers'])
    if result is None:raise ValueError('layer_node_missing')
    return result

def expected(command,b,p,state,returned):
    """按锁定文档契约计算完整树和可观察会话状态，不采信执行后的树。"""
    if command not in COMMANDS:raise ValueError('layer_command_unknown')
    e=copy.deepcopy(b);st={k:copy.deepcopy(state[k]) for k in ('currentLayer','selection','target','pasteRemembersLayers')};id=p.get('id',st['currentLayer']);name=command[6:]
    def node(id):return shape.find(e,id)
    def allocate():
        id=e['next_id'];e['next_id']+=1;return id
    def next_name():
        names=[n.get('name') for n in e['layers']];i=len(names)+1
        while 'Layer '+str(i) in names:i+=1
        return 'Layer '+str(i)
    def returned_id(value):
        if type(returned.get('id')) is not int or returned['id']!=value:raise ValueError('layer_return_id')
    def editable(id):
        def visit(nodes,parents=True):
            for n in nodes:
                yes=parents and n.get('visible',True) and not n.get('locked',False)
                if n['id']==id:return yes
                found=visit(n['kind'].get('children',[]),yes)
                if found is not None:return found
        return visit(e['layers']) is True
    def visible_children(id):return [n['id'] for n in node(id)['kind'].get('children',[]) if n.get('visible',True) and not n.get('locked',False)]
    if name in ('new','newSublayer','collectInNew'):
        new=allocate();returned_id(new)
        if name=='newSublayer':
            parent=p.get('parent',st['currentLayer']);children=node(parent)['kind']['children'];count=sum(c['kind']['type']=='layer' for c in children)
            children.append(layer(new,p.get('name','Layer '+str(len(walk(e)))),(len(e['layers'])+count+1)%27))
        else:
            n=layer(new,p.get('name',next_name()),len(e['layers'])%27)
            if name=='new':
                index=next((i+1 for i,n in enumerate(e['layers']) if n['id']==st['currentLayer']),len(e['layers']));e['layers'].insert(index,n);st['currentLayer']=new
            else:
                # 夹具只选择独立路径；排序取原树绘制顺序而非传入顺序。
                selected=[n['id'] for n in walk(e) if n['id'] in st['selection']]
                for selected_id in selected:
                    siblings,i=location(e,selected_id);n['kind']['children'].append(siblings.pop(i))
                e['layers'].append(n)
    elif name=='delete':
        removed={n['id'] for n in walk({'layers':[node(id)]})};siblings,i=location(e,id);siblings.pop(i);st['selection']=[v for v in st['selection'] if v not in removed]
        if st['currentLayer'] in removed:
            st['currentLayer']=next((n['id'] for n in reversed(e['layers']) if n.get('visible',True) and not n.get('locked',False)),e['layers'][-1]['id'])
    elif name=='duplicate':
        n=copy.deepcopy(node(id));n['name']=n.get('name','Layer')+' copy'
        def reid(n):
            n['id']=allocate()
            for c in n['kind'].get('children',[]):reid(c)
        reid(n);returned_id(n['id']);siblings,i=location(e,id);siblings.insert(i+1,n)
    elif name=='setCurrent':st['currentLayer']=id
    elif name=='setProps':
        n=node(id)
        if 'name' in p:n['name']=p['name']
        for key,default in (('visible',True),('locked',False)):
            if key in p:
                if p[key]==default:n.pop(key,None)
                else:n[key]=p[key]
        for key in ('template','printable'):
            if key in p:n['kind'][key]=p[key]
        if 'color' in p:n['kind']['color']={'Preset':p['color']%27}
        st['selection']=[v for v in st['selection'] if editable(v)]
    elif name=='selectAll':st['selection']=visible_children(id);st['target']=None
    elif name=='target':
        st['selection']=visible_children(id) if node(id)['kind']['type']=='layer' else [id];st['target']=id
        if node(id)['kind']['type']=='layer':st['currentLayer']=id
        if returned!={'id':id,'selected':st['selection']}:raise ValueError('layer_target_return')
    elif name=='clippingMask.toggle':
        n=node(id);on=not n['kind'].get('clip',False);children=n['kind']['children'];mask=children[-1] if on else children[0]
        if on:
            mask['appearance']={'items':[{'kind':'fill','paint':{'type':'none'}},{'kind':'stroke','paint':{'type':'none'},'width':0.0}]};mask['kind']['clipping']=True;children.insert(0,children.pop());n['kind']['clip']=True
        else:n['kind'].pop('clip',None);mask['kind'].pop('clipping',None)
        if returned!={'clip':on}:raise ValueError('layer_clip_return')
    elif name=='pasteRemembersLayers':
        on=p.get('on',not b.get('paste_remembers_layers',False));st['pasteRemembersLayers']=on
        if on:e['paste_remembers_layers']=True
        else:e.pop('paste_remembers_layers',None)
        if returned!={'on':on}:raise ValueError('layer_paste_return')
    return e,st

def validate_transition(command,s):
    """每一字段按期望树比较；重开只核对持久树，不伪称会话选择会持久化。"""
    b,a,r=(s[k] for k in ('before','after','reopened'))
    if shape.stable(a)!=shape.stable(r):raise ValueError('layer_reopen')
    e,st=expected(command,b,s['params'],s['fixture']['beforeInspect'],s['returned'])
    if shape.stable(e)!=shape.stable(a):raise ValueError('layer_tree_transition')
    for key,value in st.items():
        if s['observed'][key]!=value:raise ValueError('layer_session_'+key)
    if s['round']==2:
        f=s['fixture'];prior=copy.deepcopy(f['revisionBefore']);shape.find(prior,f['revisionID'])['name']=f['revisionName']
        if shape.stable(prior)!=shape.stable(b) or shape.find(f['revisionBefore'],f['revisionID']).get('name')==f['revisionName']:raise ValueError('layer_local_revision')

def initialize(call):
    call('view.drawMode',mode='normal');call('paint.setFill',ids=[2],color='#224466');call('paint.setStroke',ids=[2],color='#448822');call('stroke.set',ids=[2],weight=2)
    _state.clear();target=call('layer.new',name='Owned layer fixture')['id'];ids=[]
    for x,y in ((82,14),(90,26)):
        id=call('shape.rectangle',x=x,y=y,width=24,height=20)['id'];call('paint.setFill',ids=[id],color='#cc6633');ids.append(id)
    _state.update(target=target,art=ids);call('layer.setCurrent',id=1);return _state

def prepare(call,command,number,directory,state):
    name=command[6:];target=state['target'];art=state['art'];second=number==2
    if name in ('selectAll','target','duplicate') and not second:
        hidden=call('shape.rectangle',x=78,y=54,width=8,height=8)['id'];call('node.move',id=hidden,parent=target,index=999);call('layer.setProps',id=hidden,visible=False)
        locked=call('shape.rectangle',x=90,y=54,width=8,height=8)['id'];call('node.move',id=locked,parent=target,index=999);call('layer.setProps',id=locked,locked=True)
        sub=call('layer.newSublayer',parent=target,name='Owned nested')['id'];call('layer.setCurrent',id=sub);call('shape.rectangle',x=104,y=54,width=8,height=8);state.update(hidden=hidden,locked=locked,sub=sub)
    if name=='delete' and second:
        target=call('layer.new',name='Owned second deletion')['id'];new=call('shape.rectangle',x=82,y=54,width=24,height=20)['id'];state['deleteArt']=[new]
    fixture={}
    if second:
        revision=target if name=='delete' else state.get('createdID',target) if name in ('new','newSublayer') else target
        fixture={'revisionBefore':call('document.json'),'revisionID':revision,'revisionName':'Owned revised layer '+name};call('layer.setProps',id=revision,name=fixture['revisionName'])
    call('layer.setCurrent',id=1);call('select.set',ids=[2])
    if name=='new':params={'name':'Owned new '+str(number)}
    elif name=='newSublayer':params={'parent':state.get('createdID',target) if second else target,'name':'Owned sub '+str(number)}
    elif name=='delete':
        call('layer.setCurrent',id=target);call('select.set',ids=state['deleteArt'] if second else art);params={} if second else {'id':target}
    elif name=='duplicate':params={} if second else {'id':target};call('layer.setCurrent',id=target)
    elif name=='setCurrent':params={'id':1 if second else target}
    elif name=='setProps':
        if not second:call('select.set',ids=art)
        params={'id':target,'name':'Owned visible' if second else 'Owned hidden locked','visible':second,'locked':not second,'template':not second,'printable':second,'color':26 if second else 4}
    elif name=='collectInNew':call('select.set',ids=list(reversed(art)));params={}
    elif name=='selectAll':params={'id':state['sub'] if second else target}
    elif name=='clippingMask.toggle':params={'id':target}
    elif name=='target':params={'id':art[0] if second else target}
    else:params={} if second else {'on':True}
    fixture['beforeInspect']=call('document.inspect');return params,fixture

def observe(call,command,params,returned,directory,fixture):
    if command in ('layer.new','layer.newSublayer'):_state['createdID']=returned['id']
    return call('document.inspect')
if __name__=='__main__':
    common=load_local('command_family_window');family=type('LayerFamily',(),{'FAMILY':FAMILY,'COMMANDS':COMMANDS,'__file__':__file__,**{n:staticmethod(globals()[n]) for n in ('initialize','prepare','observe','validate_transition')}});common.run(json.loads(Path(sys.argv[1]).read_text()),family)
