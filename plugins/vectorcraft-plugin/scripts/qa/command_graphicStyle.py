#!/usr/bin/env python3
"""固定安装图形样式验收：完整外观／链接树、相对渐变、样式库及控制艺术。"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
FAMILY='graphicStyle'
COMMANDS=['graphicStyle.'+n for n in ('apply','new','delete','duplicate','list','redefine','breakLink','rename','unused','sortByName','merge','move','setOptions','libraries','library','addFromLibrary','saveLibrary','loadLibrary')]
_state={}
def load_local(name):
 s=importlib.util.spec_from_file_location('styles_'+name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
shape=load_local('command_shape')
def walk(model):
 def visit(n):
  yield n
  for c in n['kind'].get('children',[]):yield from visit(c)
 return [n for l in model['layers'] for n in visit(l)]
def unique(name,styles):
 names={g['name'] for g in styles};i=2;result=name
 while result in names:result=name+' '+str(i);i+=1
 return result
def bounds(n):
 points=[a['p'] for s in n['kind']['path']['subpaths'] for a in s['anchors']];xs,ys=zip(*points);return min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys)
def rebase(ap,src,dst):
 """夹具使用矩形的放置填充渐变；独立映射端点并保持aspect。"""
 ap=copy.deepcopy(ap)
 for item in ap.get('items',[]):
  p=item['paint']
  if p['type']=='gradient' and 'geom' in p:
   if item['kind']!='fill':raise ValueError('style_fixture_gradient_stroke')
   for key in ('start','end','focal'):
    if key in p['geom']:
     point=p['geom'][key]
     for axis,i in (('x',0),('y',1)):point[axis]=dst[i]+(point[axis]-src[i])/src[i+2]*dst[i+2]
 return ap
def appearance_on(g,n):
 ap=g['appearance']
 return rebase(ap,(0,0,1,1),bounds(n)) if g.get('unit_box') and any(i['paint']['type']=='gradient' and 'geom' in i['paint'] for i in ap.get('items',[])) else copy.deepcopy(ap)
def capture(n,name,id):
 g={'name':name,'id':id,'unit_box':True,'appearance':rebase(n['appearance'],bounds(n),(0,0,1,1))}
 for key in ('opacity','blend','isolate','knockout'):
  if key in n:g[key]=copy.deepcopy(n[key])
 return g
def apply(n,g,add=False):
 ap=appearance_on(g,n)
 if add:
  for key in ('items','effects'):
   if ap.get(key):n['appearance'].setdefault(key,[]).extend(ap[key])
  n.pop('graphic_style',None)
 else:
  n['appearance']=ap;n['graphic_style']=g['id']
  for key in ('opacity','blend','isolate','knockout'):
   if key in g:n[key]=copy.deepcopy(g[key])
   else:n.pop(key,None)
def synced(n,g):
 try:
  shape.near(n.get('appearance',{}),appearance_on(g,n),'style_sync')
  for key,default in (('opacity',1),('blend','Normal'),('isolate',False),('knockout','Neutral')):shape.near(n.get(key,default),g.get(key,default),'style_sync')
  return True
 except ValueError:return False

def same_look(a,b):
 try:shape.near({k:v for k,v in a.items() if k not in ('id','name')},{k:v for k,v in b.items() if k not in ('id','name')},'style_same_look');return True
 except ValueError:return False

def expected(command,b,p,f,returned):
 """逐命令构造完整工程期望；样式修改仅影响明确授权节点。"""
 if command not in COMMANDS:raise ValueError('style_command_unknown')
 e=copy.deepcopy(b);styles=e['graphic_styles'];name=command.split('.')[1]
 def g(n):return next(x for x in styles if x['name']==n)
 def nid():return max([x.get('id',0) for x in styles],default=0)+1
 def source():return shape.find(e,p.get('id',f.get('selection',[2])[0]))
 def returned_name(n):
  if returned!={'name':n}:raise ValueError('style_return_name')
 if name=='apply':
  for id in p.get('ids',f['selection']):apply(shape.find(e,id),g(p['name']),p.get('add',False))
 elif name=='new':
  n=source();nm=unique(p['name'],styles);style=capture(n,nm,nid());styles.append(style);n['graphic_style']=style['id'];returned_name(nm)
 elif name=='delete':
  names=p.get('names',[p.get('name')]);ids={g(n).get('id',0) for n in names};styles[:]=[x for x in styles if x['name'] not in names]
  for n in walk(e):
   if n.get('graphic_style') in ids:n.pop('graphic_style',None)
 elif name=='duplicate':
  old=g(p['name']);nm=unique(p['name']+' copy',styles);style=copy.deepcopy(old);style.update(id=nid(),name=nm);styles.insert(styles.index(old)+1,style);returned_name(nm)
 elif name=='redefine':
  src=source();old=g(p['name']);style=capture(src,old['name'],old['id'])
  for n in walk(e):
   if n['id']!=src['id'] and n.get('graphic_style')==old['id']:
    if synced(n,old):apply(n,style)
    else:n.pop('graphic_style',None)
  styles[styles.index(old)]=style;src['graphic_style']=style['id'];returned_name(style['name'])
 elif name=='breakLink':
  for id in p.get('ids',f['selection']):shape.find(e,id).pop('graphic_style',None)
 elif name=='rename':g(p['name'])['name']=p['to'];returned_name(p['to'])
 elif name=='sortByName':styles.sort(key=lambda x:(x['name']!='Default Graphic Style',x['name'].lower()))
 elif name=='merge':
  selected=[g(n) for n in p['names']];style=copy.deepcopy(selected[0]);style.update(id=nid(),name=unique(p['name'],styles))
  for extra in selected[1:]:
   for key in ('items','effects'):
    if extra['appearance'].get(key):style['appearance'].setdefault(key,[]).extend(copy.deepcopy(extra['appearance'][key]))
  styles.append(style);returned_name(style['name'])
 elif name=='move':
  style=g(p['name']);styles.remove(style);styles.insert(min(p['to'],len(styles)),style)
 elif name=='addFromLibrary':
  added=[];existing=[];library=f['libraryData']
  for original in library['styles']:
   if original['name'] not in p['names']:continue
   same=next((x for x in styles if x['name']==original['name'] and same_look(x,original)),None)
   if same:existing.append(same['name'])
   else:
    style=copy.deepcopy(original);style.update(name=unique(style['name'],styles),id=nid());styles.append(style);added.append(style['name'])
  applied=added[0] if added else existing[0]
  if returned!={'library':p['library'],'added':added,'existing':existing,'applied':applied}:raise ValueError('style_library_add')
  for id in p['ids']:apply(shape.find(e,id),g(applied),p.get('add',False))
 return e

def paint_label(p):
 if p['type']=='none':return 'None'
 if p['type']=='gradient':return p['gradient']['kind']+' gradient'
 if p['type']=='solid':
  c=p['color']
  if c['model']!='rgb':raise ValueError('style_fixture_color_model')
  return '#'+''.join(format(int(c[k]*255+.5),'02x') for k in ('r','g','b'))
 raise ValueError('style_fixture_paint')

def projection(g):
 ap=g['appearance'];items=ap.get('items',[])
 return {'name':g['name'],'fill':paint_label(next((i['paint'] for i in reversed(items) if i['kind']=='fill'),{'type':'none'})),'stroke':paint_label(next((i['paint'] for i in reversed(items) if i['kind']=='stroke'),{'type':'none'})),'fills':sum(i['kind']=='fill' for i in items),'strokes':sum(i['kind']=='stroke' for i in items),'effects':[x['id'] for x in ap.get('effects',[])],'opacity':int(g.get('opacity',1)*100+.5),'blend':g.get('blend','Normal'),'isolate':g.get('isolate',False),'knockout':g.get('knockout','Neutral').lower(),'strokeWidth':next((i['width'] for i in reversed(items) if i['kind']=='stroke'),0)}
def validate_list(model,value,selection):
 styles=model['graphic_styles'];rows=value['styles']
 if [x['name'] for x in rows]!=[g['name'] for g in styles]:raise ValueError('style_list_order')
 for g,row in zip(styles,rows):
  for key,expected_value in projection(g).items():
   if row[key]!=expected_value:raise ValueError('style_list_summary')
  linked=[n['id'] for n in walk(model) if n.get('graphic_style')==g.get('id') and synced(n,g)]
  if row['id']!=g.get('id',0) or row['linked']!=linked:raise ValueError('style_list_links')
 selected=None
 if selection:
  n=shape.find(model,selection[0]);selected=next((g['name'] for g in styles if g.get('id')==n.get('graphic_style') and synced(n,g)),None)
 if value['selected']!=selected:raise ValueError('style_list_selected')

def validate_transition(command,s):
 b,a,r=(s[k] for k in ('before','after','reopened'));p=s['params'];f=s['fixture'];ret=s['returned'];o=s['observed'];name=command.split('.')[1]
 if shape.stable(a)!=shape.stable(r):raise ValueError('style_reopen')
 shape.near(shape.stable(expected(command,b,p,f,ret)),shape.stable(a),'style_tree_transition')
 validate_list(a,o['list'],f['selection'])
 if name=='list' and ret!=o['list']:raise ValueError('style_list_query')
 if name=='unused':
  used={n.get('graphic_style') for n in walk(a) if any(n.get('graphic_style')==g.get('id') and synced(n,g) for g in a['graphic_styles'])}
  if ret!={'names':[g['name'] for g in a['graphic_styles'] if g.get('id',0) not in used]}:raise ValueError('style_unused')
 if name=='setOptions' and (ret!={'overrideCharColor':p['overrideCharColor']} or o['list']['overrideCharColor'] is not p['overrideCharColor']):raise ValueError('style_options')
 if name in ('library','loadLibrary','saveLibrary','libraries'):
  lib=ret if name=='library' else o.get('library')
  if name=='libraries':
   libs=ret['libraries'];builtin=[x['id'] for x in libs if x['category']=='builtIn']
   if builtin!=['shadows-glows','outlines-rules','hand-drawn','gradient-finishes','shape-effects','blends-transparency'] or not any(x['id']==f['libraryID'] and x['count']==2 for x in libs):raise ValueError('style_libraries')
  else:
   if lib['id']!=(ret['library'] if name=='loadLibrary' else f['libraryID'] if name=='library' else o['library']['id']):raise ValueError('style_library_identity')
   expected_rows=[projection(g) for g in f['libraryData']['styles']]
   if len(lib['styles'])!=len(expected_rows):raise ValueError('style_library_count')
   for row,exp in zip(lib['styles'],expected_rows):
    if any(row[k]!=v for k,v in exp.items()):raise ValueError('style_library_content')
   if name=='loadLibrary' and ret['count']!=2:raise ValueError('style_library_load')
   if name=='saveLibrary':
    data=o['savedData']
    if ret['count']!=2 or data.get('format')!='vcstyles' or data.get('version')!=1 or data.get('name')!=p['name'] or o['decoded'] is not True or len(o['sha256'])!=64:raise ValueError('style_library_save')
    shape.near(data['styles'],f['libraryData']['styles'],'style_saved_standalone')
 if s['round']==2:
  prior=copy.deepcopy(f['revisionBefore']);shape.find(prior,f['revisionID'])['name']=f['revisionName']
  if shape.stable(prior)!=shape.stable(b) or shape.find(f['revisionBefore'],f['revisionID']).get('name')==f['revisionName']:raise ValueError('style_local_revision')
 if o.get('preferenceRestartAcceptance')!='NOT_RUN':raise ValueError('style_preference_scope')

def initialize(call):
 call('view.drawMode',mode='normal');call('graphicStyle.setOptions',overrideCharColor=True);call('paint.setFill',ids=[2],color='#224466');call('paint.setStroke',ids=[2],color='#448822');call('stroke.set',ids=[2],weight=2);_state.clear();ids=[]
 for x,y,color in ((82,14,'#aa3311'),(90,42,'#3377aa')):
  id=call('shape.rectangle',x=x,y=y,width=24,height=20)['id'];call('paint.setFill',ids=[id],color=color);call('paint.setStroke',ids=[id],color='#448822');ids.append(id)
 a,b=ids;call('select.set',ids=[a]);call('paint.toggleActive',fill=True);call('paint.editGradient',kind='linear',stops=[{'offset':0,'color':'#aa3311'},{'offset':1,'color':'#ffee99'}]);call('paint.setGradientGeom',start=[82,14],end=[106,34]);call('transparency.set',ids=[a],item=None,opacity=65,blend='multiply');call('graphicStyle.new',name='Owned Zeta',id=a);call('graphicStyle.new',name='Owned Alpha',id=b);_state.update(a=a,b=b);return _state

def prepare(call,command,number,directory,state):
 name=command.split('.')[1];second=number==2;a,b=state['a'],state['b'];f={};p={}
 if name=='breakLink':call('graphicStyle.apply',name='Owned Zeta',ids=[2])
 if name=='delete':
  p={'name':'Owned Zeta'} if not second else {'names':['Owned Alpha']};call('graphicStyle.apply',name='Owned Alpha' if second else 'Owned Zeta',ids=[2])
 elif name=='apply':p={'name':'Owned Alpha' if second else 'Owned Zeta','ids':[2],'add':second}
 elif name=='new':p={'name':'Owned Fresh','id':2}
 elif name=='duplicate':p={'name':'Owned Zeta'}
 elif name=='redefine':
  call('graphicStyle.apply',name='Owned Zeta',ids=[2])
  if not second:state['edited']=call('shape.rectangle',x=80,y=64,width=12,height=10)['id']
  call('graphicStyle.apply',name='Owned Zeta',ids=[state['edited']]);call('paint.setFill',ids=[state['edited']],color='#993366');call('paint.setFill',ids=[a],color='#22aa88' if second else '#cc6622');call('transparency.set',ids=[a],item=None,opacity=45 if second else 75);p={'name':'Owned Zeta','id':a}
 elif name=='breakLink':p={'ids':[2]}
 elif name=='rename':p={'name':'Owned Renamed 1' if second else 'Owned Zeta','to':'Owned Renamed '+str(number)}
 elif name=='sortByName':call('graphicStyle.move',name='Owned Zeta',to=0)
 elif name=='merge':p={'names':['Owned Alpha','Owned Zeta'] if second else ['Owned Zeta','Owned Alpha'],'name':'Owned Combined'}
 elif name=='move':p={'name':'Owned Zeta','to':999 if second else 0}
 elif name=='setOptions':p={'overrideCharColor':second};call('graphicStyle.setOptions',overrideCharColor=not second)
 if name in ('libraries','library','addFromLibrary','saveLibrary','loadLibrary'):
  saved=call('graphicStyle.saveLibrary',names=['Owned Zeta','Owned Alpha'],name='Owned library');data=json.loads(saved['data']);f['libraryData']=data
  if name=='loadLibrary':
   p={'data':saved['data'],'name':'Owned.vcstyles'} if not second else {'path':str(directory/'input.vcstyles')};
   if second:Path(p['path']).write_text(saved['data'])
  elif name=='saveLibrary':p={'names':['Owned Zeta','Owned Alpha'],'name':'Owned saved '+str(number)};p.update({} if second else {'path':str(directory/'saved.vcstyles')})
  else:
   loaded=call('graphicStyle.loadLibrary',data=saved['data'],name='Owned.vcstyles');f['libraryID']=loaded['library']
   if name=='library':p={'library':loaded['library']}
   elif name=='addFromLibrary':
    # 第一轮名称冲突但外观不同，第二轮重用刚导入的同名同外观样式。
    if not second:
     modified=copy.deepcopy(data);modified['styles'][0]['name']='Owned Alpha';modified['styles'][1]['name']='Owned second';text=json.dumps(modified);loaded=call('graphicStyle.loadLibrary',data=text,name='Imported.vcstyles');state['importData']=modified;state['importID']=loaded['library']
    if second:state['importID']=call('graphicStyle.loadLibrary',data=json.dumps(state['importData']),name='Imported-second.vcstyles')['library']
    f['libraryData']=state['importData'];p={'library':state['importID'],'names':[g['name'] for g in state['importData']['styles']],'apply':True,'ids':[2],'add':second}
 if second:
  f.update(revisionBefore=call('document.json'),revisionID=b,revisionName='Owned revised source');call('layer.setProps',id=b,name=f['revisionName'])
 call('select.set',ids=[2]);f['selection']=[2];return p,f

def observe(call,command,params,returned,directory,fixture):
 o={'list':call('graphicStyle.list'),'preferenceRestartAcceptance':'NOT_RUN'};name=command.split('.')[1]
 if name=='addFromLibrary' and returned['added']:
  _state['importData']=copy.deepcopy(fixture['libraryData'])
  for style,nm in zip(_state['importData']['styles'],returned['added']):style['name']=nm
 if name=='loadLibrary':o['library']=call('graphicStyle.library',library=returned['library'])
 if name=='saveLibrary':
  text=Path(params['path']).read_text() if 'path' in params else returned['data'];o.update(savedData=json.loads(text),decoded=True,sha256=hashlib.sha256(text.encode()).hexdigest());loaded=call('graphicStyle.loadLibrary',data=text,name='Saved.vcstyles');o['library']=call('graphicStyle.library',library=loaded['library'])
 return o
if __name__=='__main__':
 common=load_local('command_family_window');family=type('StyleFamily',(),{'FAMILY':FAMILY,'COMMANDS':COMMANDS,'__file__':__file__,**{n:staticmethod(globals()[n]) for n in ('initialize','prepare','observe','validate_transition')}});common.run(json.loads(Path(sys.argv[1]).read_text()),family)
