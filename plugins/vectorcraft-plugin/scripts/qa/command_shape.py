#!/usr/bin/env python3
"""固定形状验收：独立几何预期、局部修订、控制艺术及真实窗口交付。"""
import copy
import importlib.util
import json
import math
from pathlib import Path
import sys
FAMILY='shape'
COMMANDS=['shape.'+n for n in ('rectangle','ellipse','polygon','star','flare','line','spiral','arc','rectangularGrid','polarGrid')]
K=.5522847498307936
_state={}

def load_local(name):
    s=importlib.util.spec_from_file_location('shape_'+name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
paint=load_local('command_paint')
def stable(model):return {k:v for k,v in model.items() if k!='metadata'}
def find(model,id):
    def walk(n):
        if n['id']==id:return n
        for ch in n['kind'].get('children',[]):
            r=walk(ch)
            if r is not None:return r
    return next(r for l in model['layers'] if (r:=walk(l)) is not None)
def near(a,b,reason):
    if type(a) in (int,float) and type(b) in (int,float):
        if not math.isfinite(a) or abs(a-b)>2e-6:raise ValueError(reason)
    elif isinstance(a,dict) and isinstance(b,dict):
        if set(a)!=set(b):raise ValueError(reason)
        for k in a:near(a[k],b[k],reason)
    elif isinstance(a,list) and isinstance(b,list):
        if len(a)!=len(b):raise ValueError(reason)
        for x,y in zip(a,b):near(x,y,reason)
    elif type(a)!=type(b) or a!=b:raise ValueError(reason)
def anchor(p,hin=None,hout=None,smooth=False):
    a={'p':list(p)}
    if hin is not None and list(hin)!=list(p):a['in']=list(hin)
    if hout is not None and list(hout)!=list(p):a['out']=list(hout)
    if smooth:a['kind']='Smooth'
    return a
def poly(points,closed):return {'anchors':[anchor(p) for p in points],'closed':closed}
def rect(x,y,w,h,r=0):
    if r<=1e-9:return poly([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],True)
    r=min(r,w/2,h/2);k=r*K;u=x+w;v=y+h
    return {'closed':True,'anchors':[anchor((x+r,y),(x+r-k,y),(x+r,y)),anchor((u-r,y),(u-r,y),(u-r+k,y)),anchor((u,y+r),(u,y+r-k),(u,y+r)),anchor((u,v-r),(u,v-r),(u,v-r+k)),anchor((u-r,v),(u-r+k,v),(u-r,v)),anchor((x+r,v),(x+r,v),(x+r-k,v)),anchor((x,v-r),(x,v-r+k),(x,v-r)),anchor((x,y+r),(x,y+r),(x,y+r-k))]}
def ellipse(cx,cy,rx,ry):
    return {'closed':True,'anchors':[anchor((cx-rx,cy),(cx-rx,cy+ry*K),(cx-rx,cy-ry*K),True),anchor((cx,cy-ry),(cx-rx*K,cy-ry),(cx+rx*K,cy-ry),True),anchor((cx+rx,cy),(cx+rx,cy-ry*K),(cx+rx,cy+ry*K),True),anchor((cx,cy+ry),(cx+rx*K,cy+ry),(cx-rx*K,cy+ry),True)]}
def geometry(command,p):
    """独立按锁定生成器公式构造各路径；未知命令不接受。"""
    if command not in COMMANDS:raise ValueError('shape_command_unknown')
    n=command.split('.')[1];live=None;paths=[]
    if n in ('rectangle','ellipse','rectangularGrid','polarGrid'):
        x,y,w,h=(p[k] for k in ('x','y','width','height'));x,y=min(x,x+w),min(y,y+h);w,h=abs(w),abs(h);cx,cy=x+w/2,y+h/2
        if n=='rectangle':
            r=max(0,p.get('radius',0));paths=[rect(x,y,w,h,r)];live={'shape':'rectangle','w':w,'h':h,'radii':[r]*4,'xf':[1,0,0,1,x,y]}
        elif n=='ellipse':paths=[ellipse(cx,cy,w/2,h/2)];live={'shape':'ellipse','w':w,'h':h,'pie':[0,360],'xf':[1,0,0,1,x,y]}
        elif n=='rectangularGrid':
            rows,cols=p['rows'],p['columns'];paths=[poly([(x,y+h*i/(rows+1)),(x+w,y+h*i/(rows+1))],False) for i in range(1,rows+1)]+[poly([(x+w*i/(cols+1),y),(x+w*i/(cols+1),y+h)],False) for i in range(1,cols+1)]+[rect(x,y,w,h)]
        else:
            c,rad=p['concentric'],max(1,p['radial']);paths=[ellipse(cx,cy,w*i/(c+1)/2,h*i/(c+1)/2) for i in range(1,c+2)]+[poly([(cx,cy),(cx+w/2*math.cos(-math.pi/2+math.tau*i/rad),cy+h/2*math.sin(-math.pi/2+math.tau*i/rad))],False) for i in range(rad)]
    elif n in ('polygon','star'):
        cx,cy=p['cx'],p['cy'];rot=math.radians(p.get('rotation',0));count=p['sides'] if n=='polygon' else p['points']*2
        radii=[p['radius']]*count if n=='polygon' else [p['radius1'] if i%2==0 else p['radius2'] for i in range(count)]
        paths=[poly([(cx+r*math.cos(-math.pi/2+rot+math.tau*i/count),cy+r*math.sin(-math.pi/2+rot+math.tau*i/count)) for i,r in enumerate(radii)],True)]
        if n=='polygon':live={'shape':'polygon','radius':p['radius'],'sides':count,'xf':[math.cos(rot),math.sin(rot),-math.sin(rot),math.cos(rot),cx,cy]}
    elif n in ('line','arc'):
        x,y,u,v=(p[k] for k in ('x1','y1','x2','y2'))
        if n=='line':paths=[poly([(x,y),(u,v)],False)];live={'shape':'line','a':{'x':x,'y':y},'b':{'x':u,'y':v}}
        else:
            anchors=[anchor((x,y),(x,y),(x+(u-x)*K,y)),anchor((u,v),(u,v+(y-v)*K),(u,v))]
            if p.get('closed',False):anchors.append(anchor((x,v)))
            paths=[{'anchors':anchors,'closed':p.get('closed',False)}]
    elif n=='spiral':
        cx,cy,r=p['cx'],p['cy'],p['radius'];dec=p['decay']/100;count=p['segments'];sign=1 if p['clockwise'] else -1;anchors=[]
        for i in range(count+1):
            a=sign*i*math.pi/2;pt=[cx+r*math.cos(a),cy+r*math.sin(a)];t=[-math.sin(a)*sign,math.cos(a)*sign];hin=[pt[j]-t[j]*K*(r+r/dec)/2 for j in (0,1)];hout=[pt[j]+t[j]*K*(r+r*dec)/2 for j in (0,1)]
            anchors.append(anchor(pt,hin if i else pt,hout if i<count else pt,True));r*=dec
        # 反转路径同时互换入／出手柄，保持中心端起点。
        rev=[]
        for a in reversed(anchors):rev.append(anchor(a['p'],a.get('out',a['p']),a.get('in',a['p']),True))
        paths=[{'anchors':rev,'closed':False}]
    elif n=='flare':paths=[part['path'] for part in flare(p)]
    return paths,live

def assert_path(actual,expected):
    def normalized(paths):
        return [{'closed':s['closed'],'anchors':[{'p':a['p'],'in':a.get('in',a['p']),'out':a.get('out',a['p']),'kind':a.get('kind','Corner')} for a in s['anchors']]} for s in paths]
    if set(actual)!={'subpaths'}:raise ValueError('shape_path_geometry')
    near(normalized(actual['subpaths']),normalized(expected),'shape_path_geometry')

def flare(p):
    """按固定64位xorshift种子构造每个光晕节点的几何与径向渐变。"""
    seed=p['seed']|1;mask=(1<<64)-1
    def rnd():
        nonlocal seed
        seed^=(seed<<13)&mask;seed^=seed>>7;seed^=(seed<<17)&mask;return (seed>>11)/(1<<53)
    cx,cy=p['cx'],p['cy'];r=p['diameter']/2;fuzz=p['fuzziness']/100;inner=min(.95,max(.05,1-fuzz*.6));halo=r*(1+p['growth']/100)*1.6
    def part(name,x,y,radius,path,stops,opacity=1):return {'name':name,'path':path,'center':[x,y],'radius':radius,'stops':stops,'opacity':opacity}
    parts=[part('Halo',cx,cy,halo,ellipse(cx,cy,halo,halo),[(0,0),(inner*.75,0),(inner,.5),(1,0)])]
    if p['rays']:
        paths=[];reach=0
        for i in range(p['rays']):
            a=math.tau*(i+rnd()*.6)/p['rays'];length=r*p['longest']/100*max(.1,1-p['rayFuzziness']/100*.75*rnd());reach=max(reach,length);dx,dy=math.cos(a),math.sin(a);w=r*.035;nx,ny=-dy*w,dx*w
            paths.append(poly([(cx+nx,cy+ny),(cx+dx*length,cy+dy*length),(cx-nx,cy-ny),(cx-dx*w*4,cy-dy*w*4)],True))
        parts.append(part('Rays',cx,cy,reach,paths,[(0,.9),(.25,.35),(1,0)]))
    parts.append(part('Center',cx,cy,r,ellipse(cx,cy,r,r),[(0,1),(.25+p['brightness']/100*.5,.6),(1,0)],p['opacity']/100))
    for _ in range(p['rings']):
        t=rnd();x=cx+(p['x2']-cx)*t;y=cy+(p['y2']-cy)*t;rr=max(.5,r*p['largest']/100*(.25+rnd()*.75));solid=rnd()<.5;stops=[(0,.25),(.8,.2),(1,0)] if solid else [(0,0),(.7,.05),(.92,.35),(1,0)]
        parts.append(part('Ring',x,y,rr,ellipse(x,y,rr,rr),stops))
    return parts

def validate_transition(command,s):
    """核对唯一新增子树、完整几何与样式，并保全源／控制艺术和前轮修订。"""
    if command not in COMMANDS:raise ValueError('shape_command_unknown')
    b,a,r=(s[k] for k in ('before','after','reopened'));p=s['params'];id=s['returned'].get('id')
    if stable(a)!=stable(r):raise ValueError('shape_reopen')
    if type(id) is not int or id in paint.objects(b):raise ValueError('shape_return_id')
    n=find(a,id);e=copy.deepcopy(a);children=e['layers'][0]['kind']['children']
    if children[-1]['id']!=id:raise ValueError('shape_insertion_order')
    children.pop();e['next_id']=b['next_id']
    if stable(e)!=stable(b):raise ValueError('shape_control')
    new=paint.objects({'layers':[n]})
    if sorted(new)!=list(range(b['next_id'],a['next_id'])):raise ValueError('shape_allocations')
    paths,live=geometry(command,p);name=command.split('.')[1]
    if name in ('rectangularGrid','polarGrid','flare'):
        if n['kind']['type']!='group' or len(n['kind']['children'])!=len(paths):raise ValueError('shape_group_parts')
        if name=='flare':
            if n.get('name')!='Flare' or id!=a['next_id']-1:raise ValueError('shape_flare_group')
            for child,part in zip(n['kind']['children'],flare(p)):
                assert_path(child['kind']['path'],part['path'] if part['name']=='Rays' else [part['path']])
                if child['name']!=part['name'] or child.get('blend')!='Screen':raise ValueError('shape_flare_part')
                near(child.get('opacity',1),part['opacity'],'shape_flare_opacity')
                items=child['appearance']['items'];gradient=next(x['paint'] for x in items if x['kind']=='fill')
                if gradient['type']!='gradient' or gradient['gradient']['kind']!='Radial' or next(x['paint'] for x in items if x['kind']=='stroke')!={'type':'none'}:raise ValueError('shape_flare_gradient')
                near(gradient['geom'],{'start':{'x':part['center'][0],'y':part['center'][1]},'end':{'x':part['center'][0]+part['radius'],'y':part['center'][1]},'aspect':1},'shape_flare_gradient')
                stops=gradient['gradient']['stops']
                near([[x['offset'],x['opacity']] for x in stops],[list(x) for x in part['stops']],'shape_flare_stops')
                for stop in stops:paint.color({'type':'solid','color':stop['color']},'#ffffff')
        else:
            for child,path in zip(n['kind']['children'],paths):
                assert_path(child['kind']['path'],[path]);items=child['appearance']['items'];paint.color(next(x['paint'] for x in items if x['kind']=='stroke'),'#448822')
                if next(x['paint'] for x in items if x['kind']=='fill')!={'type':'none'}:raise ValueError('shape_grid_fill')
                near(next(x['width'] for x in items if x['kind']=='stroke'),2,'shape_grid_stroke_width')
    else:
        if n['kind']['type']!='path':raise ValueError('shape_node_type')
        assert_path(n['kind']['path'],paths)
        if live is not None:near(n['kind'].get('live'),live,'shape_live_parameters')
        elif 'live' in n['kind']:raise ValueError('shape_unexpected_live')
        items=n['appearance']['items'];fill=next(x['paint'] for x in items if x['kind']=='fill');stroke=next(x for x in items if x['kind']=='stroke')
        if name=='line':
            if fill!={'type':'none'}:raise ValueError('shape_line_fill')
        else:paint.color(fill,'#224466')
        paint.color(stroke['paint'],'#448822');near(stroke['width'],2,'shape_stroke_width')
    if s['round']==2:
        prior=copy.deepcopy(s['fixture']['revisionBefore']);target=find(prior,s['fixture']['revisionID']);target['opacity']=.65
        actual=find(b,s['fixture']['revisionID']);near(actual.get('opacity',1),.65,'shape_local_revision');target['opacity']=actual['opacity']
        if stable(prior)!=stable(b):raise ValueError('shape_revision_control')
    if s['observed']['selected']!=[id]:raise ValueError('shape_native_selection')

def initialize(call):
    call('view.drawMode',mode='normal');call('paint.setFill',ids=[2],color='#224466');call('paint.setStroke',ids=[2],color='#448822');call('stroke.set',ids=[2],weight=2);_state.clear();return _state
def prepare(call,command,number,directory,state):
    second=number==2;name=command.split('.')[1];x,y,w,h=82,44 if second else 14,30,20;fixture={}
    if name=='flare' and not second:
        backdrop=call('shape.rectangle',x=76,y=6,width=48,height=58)['id'];call('paint.setFill',ids=[backdrop],color='#101820');call('paint.setStroke',ids=[backdrop],color='#101820');call('paint.setFill',ids=[2],color='#224466');call('paint.setStroke',ids=[2],color='#448822');call('select.set',ids=[2]);fixture['backdropID']=backdrop
    if second:
        fixture={'revisionBefore':call('document.json'),'revisionID':state['createdID']};call('transparency.set',ids=[state['createdID']],item=None,opacity=65);call('select.set',ids=[2])
    if name in ('rectangle','ellipse','rectangularGrid','polarGrid'):p={'x':x,'y':y,'width':w,'height':h}
    elif name in ('polygon','star','spiral'):p={'cx':x+15,'cy':y+10}
    elif name in ('line','arc'):p={'x1':x,'y1':y,'x2':x+w,'y2':y+h}
    else:p={'cx':x+15,'cy':y+10,'diameter':10 if second else 8,'opacity':70 if second else 45,'brightness':50 if second else 30,'growth':30 if second else 20,'fuzziness':60 if second else 50,'rays':4 if second else 3,'longest':170 if second else 150,'rayFuzziness':70 if second else 100,'x2':112,'y2':64 if second else 34,'rings':3 if second else 2,'largest':60 if second else 50,'seed':37 if second else 19}
    if name=='rectangle':p['radius']=5 if second else 2
    elif name=='polygon':p.update(radius=10,sides=7 if second else 5,rotation=30 if second else 10)
    elif name=='star':p.update(radius1=10,radius2=5 if second else 4,points=6 if second else 5,rotation=20 if second else 0)
    elif name=='spiral':p.update(radius=10,decay=75 if second else 80,segments=7 if second else 5,clockwise=not second)
    elif name=='arc':p['closed']=second
    elif name=='rectangularGrid':p.update(rows=3 if second else 2,columns=2 if second else 3)
    elif name=='polarGrid':p.update(concentric=3 if second else 2,radial=6 if second else 4)
    state['round']=number;return p,fixture
def observe(call,command,params,returned,directory,fixture):
    # 初始化钩子的状态通过prepare持有；下轮定位使用原生返回的实际ID。
    _state['createdID']=returned['id'];return {'selected':call('document.inspect')['selection']}
if __name__=='__main__':
    common=load_local('command_family_window');family=type('ShapeFamily',(),{'FAMILY':FAMILY,'COMMANDS':COMMANDS,'__file__':__file__,**{n:staticmethod(globals()[n]) for n in ('initialize','prepare','observe','validate_transition')}});common.run(json.loads(Path(sys.argv[1]).read_text()),family)
