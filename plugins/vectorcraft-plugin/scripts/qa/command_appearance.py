#!/usr/bin/env python3
"""固定外观验收：完整堆栈、Contents槽、原生活动行／新艺术探针与保全。"""
import copy,hashlib,importlib.util,json
from pathlib import Path
import sys
FAMILY='appearance'
COMMANDS=['appearance.'+n for n in ('addFill','addStroke','clear','reduceToBasic','setItem','removeItem','addEffect','duplicateItem','moveItem','copyFrom','setActiveItem','showAllHidden','targetContents','transfer','setNewArtBasic','newArt')]
_state={}
def load_local(name):
 s=importlib.util.spec_from_file_location('appearance_'+name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
shape=load_local('command_shape');style=load_local('command_graphicStyle')
def slot(ap,k):
 k=min(k,len(ap['items']))
 if k:ap['contents_index']=k
 else:ap.pop('contents_index',None)
def insert(ap,at,item):
 k=min(ap.get('contents_index',0),len(ap['items']));at=min(at,len(ap['items']));ap['items'].insert(at,copy.deepcopy(item))
 if at<k or at==k and k>0:slot(ap,k+1)
def remove(ap,i):
 k=min(ap.get('contents_index',0),len(ap['items']));it=ap['items'].pop(i)
 if i<k:slot(ap,k-1)
 return it
def move(ap,src,dst):
 below=src<ap.get('contents_index',0);it=remove(ap,src);k=min(ap.get('contents_index',0),len(ap['items']));dst=min(dst,len(ap['items']));ap['items'].insert(dst,it);slot(ap,k+int(dst<=k if below else dst<k));return dst
def add(n,fill):
 items=n['appearance']['items'];kind='fill' if fill else 'stroke';old=next(i for i in reversed(items) if i['kind']==kind);new={'kind':kind,'paint':copy.deepcopy(old['paint'])}
 if not fill:new['width']=max(1,old['width'])
 items.append(new)
def clear(n):
 if n['kind']['type'] in ('group','layer'):n.pop('appearance',None)
 else:n['appearance']={'items':[{'kind':'fill','paint':{'type':'none'}},{'kind':'stroke','paint':{'type':'none'},'width':1.0}]}
 for key in ('opacity','blend'):n.pop(key,None)
def reduce(n):
 ap=n['appearance'];items=ap.get('items',[]);fill=next((i for i in reversed(items) if i['kind']=='fill' and i.get('visible',True)),None);stroke=next((i for i in reversed(items) if i['kind']=='stroke' and i.get('visible',True)),None);out=[]
 if fill is not None or n['kind']['type'] not in ('group','layer'):out.append({'kind':'fill','paint':copy.deepcopy(fill['paint']) if fill else {'type':'none'}})
 if stroke:
  stroke=copy.deepcopy(stroke)
  for key in ('effects','opacity','blend'):stroke.pop(key,None)
  out.append(stroke)
 n['appearance']={'items':out} if out else {}
def targets(model,p,f):
 ids=p.get('ids',f['selection'])
 if p.get('target')=='contents':
  def leaves(n):
   ch=n['kind'].get('children');return [id for c in ch for id in leaves(c)] if ch is not None else [n['id']]
  return [id for v in ids for id in leaves(shape.find(model,v))]
 return ids

def expected(command,b,p,f,ret):
 """按锁定契约构造完整期望；任何未授权字段变化都会失败。"""
 if command not in COMMANDS:raise ValueError('appearance_command_unknown')
 e=copy.deepcopy(b);name=command.split('.')[1]
 if name in ('setActiveItem','targetContents','setNewArtBasic','newArt'):return e
 ids=targets(e,p,f)
 if name=='copyFrom':
  src=shape.find(e,p['source']);ids=p['ids']
  if p.get('reverse'):src=shape.find(e,ids[0]);ids=[p['source']]
  for id in ids:
   n=shape.find(e,id);ap=style.rebase(src['appearance'],style.bounds(src),style.bounds(n))
   if p.get('append'):
    for key in ('items','effects'):
     if ap.get(key):n['appearance'].setdefault(key,[]).extend(copy.deepcopy(ap[key]))
   else:n['appearance']=ap
   for key in ('opacity','blend'):
    if key in src:n[key]=src[key]
    else:n.pop(key,None)
  if ret!={'ids':ids}:raise ValueError('appearance_copy_return')
  return e
 if name=='transfer':
  src=shape.find(e,p['source']);n=shape.find(e,p['target']);n['appearance']=style.rebase(src['appearance'],style.bounds(src),style.bounds(n));n['appearance'].pop('contents_index',None)
  for key in ('opacity','blend','isolate','knockout','knockout_shape'):
   if key in src:n[key]=src[key]
   else:n.pop(key,None)
  if not p.get('copy',False):
   clear(src)
   for key in ('isolate','knockout','knockout_shape'):src.pop(key,None)
  if ret!={'source':p['source'],'target':p['target']}:raise ValueError('appearance_transfer_return')
  return e
 for id in ids:
  n=shape.find(e,id);ap=n.setdefault('appearance',{});items=ap.setdefault('items',[])
  if name=='addFill':add(n,True)
  elif name=='addStroke':add(n,False)
  elif name=='clear':clear(n)
  elif name=='reduceToBasic':reduce(n)
  elif name=='setItem':
   item=items[p['index']]
   if 'color' in p:item['paint']={'type':'solid','color':dict(zip(('r','g','b'),shape.paint.rgb(p['color']))),};item['paint']['color']['model']='rgb'
   for key,default in (('opacity',1),('blend','Normal'),('visible',True)):
    if key in p:
     value=p[key]/100 if key=='opacity' else p[key].capitalize() if key=='blend' else p[key]
     if value==default:item.pop(key,None)
     else:item[key]=value
   if 'weight' in p and item['kind']=='stroke':item['width']=p['weight']
  elif name in ('removeItem','duplicateItem'):
   indices=sorted(set(p.get('indices',[p.get('index')])),reverse=True)
   for i in indices:
    if name=='removeItem':remove(ap,i)
    else:insert(ap,min(p.get('to',i+1),len(items)),items[i])
  elif name=='moveItem':
   if p['from']=='contents':slot(ap,p['to']);value={'contents':ap.get('contents_index',0)}
   else:value={'index':move(ap,p['from'],p['to'])}
   if ret!=value:raise ValueError('appearance_move_return')
  elif name=='addEffect':
   item=p.get('item');fx=(ap if item is None else items[item]).setdefault('effects',[]);fx.append({'id':'distort.twist','params':{'angle':p['params']['angle']},'visible':True})
   if ret!={'ids':ids,'index':len(fx)-1,'item':item}:raise ValueError('appearance_effect_return')
  elif name=='showAllHidden':
   for row in [ap,*items]:
    row.pop('visible',None)
    for fx in row.get('effects',[]):fx['visible']=True
   if ret!={'ids':ids}:raise ValueError('appearance_hidden_return')
 return e

def validate_new_art(s):
 p,f,o=s['params'],s['fixture'],s['observed'];name=s['context']['id'].split('.')[1];on=p['on'] if name=='setNewArtBasic' else f['basic'];n=shape.find(s['after'],2);ap=copy.deepcopy(n['appearance'])
 if on:
  top=copy.deepcopy(next(i for i in reversed(ap['items']) if i['kind']=='stroke'))
  for key in ('opacity','blend','visible','effects'):top.pop(key,None)
  fill=copy.deepcopy(next(i['paint'] for i in reversed(ap['items']) if i['kind']=='fill'));ap={'items':[{'kind':'fill','paint':fill},top]}
 expected={'basic':on,'appearance':ap,'opacity':100 if on else int(n.get('opacity',1)*100+.5),'blend':'Normal' if on else n.get('blend','Normal'),'graphicStyle':None,'inherited':True}
 shape.near(o['newArt'],expected,'appearance_new_art_template')
 probe=o['newArtProbe'];actual=probe['node'];shape.near(actual['appearance'],ap,'appearance_new_art_actual');shape.near(actual.get('opacity',1),1 if on else n.get('opacity',1),'appearance_new_art_actual')
 if actual.get('blend','Normal')!=expected['blend'] or probe['restored'] is not True:raise ValueError('appearance_new_art_actual')
 if name=='newArt' and s['returned']!=o['newArt']:raise ValueError('appearance_new_art_query')
 if name=='setNewArtBasic' and s['returned']!={'on':on}:raise ValueError('appearance_basic_return')

def validate_transition(command,s):
 b,a,r=(s[k] for k in ('before','after','reopened'));name=command.split('.')[1];p=s['params'];o=s['observed'];f=s['fixture']
 if shape.stable(a)!=shape.stable(r):raise ValueError('appearance_reopen')
 shape.near(shape.stable(expected(command,b,p,f,s['returned'])),shape.stable(a),'appearance_tree_transition')
 if name=='setActiveItem':
  idx=p['index'];paint=o['inspect']['paint']
  if s['returned']!={'index':idx} or paint['appearanceItem']!=idx or idx is not None and paint['fillActive'] is not (shape.find(a,2)['appearance']['items'][idx]['kind']=='fill'):raise ValueError('appearance_active_item')
  prior=copy.deepcopy(a);index=idx if idx is not None else max(i for i,it in enumerate(shape.find(prior,2)['appearance']['items']) if it['kind']=='fill');shape.find(prior,2)['appearance']['items'][index]['paint']={'type':'solid','color':{'model':'rgb','r':.2,'g':.4,'b':.6}}
  shape.near(shape.stable(prior),shape.stable(o['activeProbe']['after']),'appearance_active_probe')
  if o['activeProbe']['restored'] is not True:raise ValueError('appearance_probe_restore')
 if name=='targetContents':
  selected=[n['id'] for n in shape.find(a,p['ids'][0])['kind']['children'] if n.get('visible',True) and not n.get('locked',False)]
  if s['returned']!={'ids':selected} or o['inspect']['selection']!=selected:raise ValueError('appearance_contents_selection')
 if name in ('setNewArtBasic','newArt'):validate_new_art(s)
 if s['round']==2:
  prior=copy.deepcopy(f['revisionBefore']);shape.find(prior,f['revisionID'])['name']=f['revisionName']
  if shape.stable(prior)!=shape.stable(b) or shape.find(f['revisionBefore'],f['revisionID']).get('name')==f['revisionName']:raise ValueError('appearance_local_revision')
 if o.get('preferenceRestartAcceptance')!='NOT_RUN':raise ValueError('appearance_preference_scope')

def decorate(call,id):
 call('appearance.clear',ids=[id]);call('paint.setFill',ids=[id],color='#224466');call('paint.setStroke',ids=[id],color='#448822');call('stroke.set',ids=[id],weight=2);call('appearance.addFill',ids=[id]);call('appearance.setItem',ids=[id],index=2,color='#aa3311',opacity=40,blend='multiply');call('effect.apply',ids=[id],item=2,effect='distort.twist',params={'angle':6});call('appearance.addStroke',ids=[id]);call('appearance.setItem',ids=[id],index=3,color='#331199',opacity=55,visible=False);call('effect.apply',ids=[id],item=None,effect='distort.twist',params={'angle':4});call('transparency.set',ids=[id],item=None,opacity=72,blend='multiply',isolate=True,knockout='on',knockoutShape=True)
def source_look(call,id):
 call('appearance.clear',ids=[id]);call('paint.setFill',ids=[id],color='#aa3311');call('paint.setStroke',ids=[id],color='#448822');call('stroke.set',ids=[id],weight=2);call('select.set',ids=[id]);call('paint.toggleActive',fill=True);call('paint.editGradient',kind='linear',stops=[{'offset':0,'color':'#aa3311'},{'offset':1,'color':'#ffee99'}]);call('paint.setGradientGeom',start=[82,14],end=[106,34]);call('transparency.set',ids=[id],item=None,opacity=65,blend='multiply',isolate=True,knockout='on',knockoutShape=True)
def initialize(call):
 call('view.drawMode',mode='normal');call('appearance.setNewArtBasic',on=True);decorate(call,2);_state.clear();layer=call('layer.new',name='Owned appearance fixture')['id'];ids=[]
 for x,y in ((82,14),(90,42)):ids.append(call('shape.rectangle',x=x,y=y,width=24,height=20)['id'])
 source_look(call,ids[0]);call('paint.setFill',ids=[ids[1]],color='#3377aa');_state.update(layer=layer,source=ids[0],other=ids[1]);call('layer.setCurrent',id=1);call('select.set',ids=[2]);return _state

def prepare(call,command,number,directory,state):
 name=command.split('.')[1];second=number==2;layer,src,other=(state[k] for k in ('layer','source','other'));p={'ids':[2]};f={}
 if name in ('addFill','addStroke') and second:p={'ids':[layer],'target':'contents'}
 elif name in ('clear','reduceToBasic') and second:
  call('appearance.addFill',ids=[layer]);call('appearance.addStroke',ids=[layer]);call('appearance.setItem',ids=[layer],index=0,opacity=30);call('effect.apply',ids=[layer],item=None,effect='distort.twist',params={'angle':8});p={'ids':[layer]}
 elif name=='setItem':p.update(index=1 if second else 2,color='#11aa44' if second else '#aa8833',opacity=85 if second else 25,blend='multiply' if second else 'screen',visible=second);p.update({'weight':7} if second else {})
 elif name=='removeItem':
  if second:decorate(call,2)
  p.update(indices=[0,2] if second else [3,2,3])
 elif name=='addEffect':p.update(effect='distort.twist',params={'angle':21 if second else 9},item=None if second else 2)
 elif name=='duplicateItem':p.update({'indices':[1,3]} if second else {'index':2,'to':0})
 elif name=='moveItem':
  if second:
   call('appearance.addFill',ids=[layer]);call('appearance.addStroke',ids=[layer]);p={'ids':[layer],'from':'contents','to':1}
  else:p.update({'from':0,'to':2})
 elif name=='copyFrom':p.update(source=src,reverse=second,append=second,pickUp={'appearance':True,'character':False,'paragraph':False},apply={'appearance':True,'character':False,'paragraph':False})
 elif name=='setActiveItem':p={'index':None if second else 0}
 elif name=='showAllHidden':
  call('appearance.setItem',ids=[2],index=1 if second else 0,visible=False);call('effect.setParams',ids=[2],index=0,item=None,visible=False);call('effect.setParams',ids=[2],index=0,item=2,visible=False)
 elif name=='targetContents':
  if not second:call('layer.setProps',id=other,locked=True)
  else:call('layer.setProps',id=other,locked=False)
  p={'ids':[layer]}
 elif name=='transfer':
  if not second:
   call('layer.setCurrent',id=layer);mask=call('shape.rectangle',x=82,y=14,width=24,height=20)['id'];call('paint.setFill',ids=[mask],color='#ffffff');call('select.set',ids=[src,mask]);call('transparency.makeOpacityMask',ids=[src,mask])
  else:source_look(call,src)
  p={'source':src,'target':other if second else 2,'copy':second}
 elif name in ('setNewArtBasic','newArt'):
  basic=second;call('appearance.setNewArtBasic',on=not basic if name=='setNewArtBasic' else basic);p={'on':basic} if name=='setNewArtBasic' else {};f['basic']=basic
 call('select.set',ids=[2]);call('paint.toggleActive',fill=True)
 if second:
  f.update(revisionBefore=call('document.json'),revisionID=other,revisionName='Owned revised appearance control');call('layer.setProps',id=other,name=f['revisionName'])
 f['selection']=[2];return p,f

def observe(call,command,params,returned,directory,fixture):
 name=command.split('.')[1];o={'inspect':call('document.inspect'),'preferenceRestartAcceptance':'NOT_RUN'}
 if name not in ('setNewArtBasic','newArt','setActiveItem'):return o
 # 探针在自有文档执行后从已落盘快照恢复；不依赖尚未验收的undo链。
 before=call('document.json');checkpoint=directory/'probe-checkpoint.vectorcraft';call('document.save',path=str(checkpoint),modified=946684700)
 checkpoint_sha=hashlib.sha256(checkpoint.read_bytes()).hexdigest()
 if name in ('setNewArtBasic','newArt'):
  o['newArt']=call('appearance.newArt');id=call('shape.rectangle',x=82,y=70,width=20,height=12)['id'];probe={'node':copy.deepcopy(shape.find(call('document.json'),id))}
 else:
  call('paint.setFill',color='#336699');probe={'after':call('document.json')}
 probe_path=directory/'probe-result.vectorcraft';call('document.save',path=str(probe_path),modified=946684701);call('document.open',path=str(checkpoint));restored=shape.stable(call('document.json'))==shape.stable(before)
 if not restored or hashlib.sha256(checkpoint.read_bytes()).hexdigest()!=checkpoint_sha:raise ValueError('appearance_probe_restore')
 probe.update(restored=restored,restoration='native-saved-checkpoint-reopen',checkpointSha256=checkpoint_sha,probeProjectSha256=hashlib.sha256(probe_path.read_bytes()).hexdigest())
 o['newArtProbe' if name in ('setNewArtBasic','newArt') else 'activeProbe']=probe
 return o
if __name__=='__main__':
 common=load_local('command_family_window_diagnostic');family=type('AppearanceFamily',(),{'FAMILY':FAMILY,'COMMANDS':COMMANDS,'__file__':__file__,**{n:staticmethod(globals()[n]) for n in ('initialize','prepare','observe','validate_transition')}});common.run(json.loads(Path(sys.argv[1]).read_text()),family)
