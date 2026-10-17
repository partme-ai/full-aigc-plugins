#!/usr/bin/env python3
"""固定效果验收：独立目录、完整效果堆栈与多种展开产物。"""
import base64,copy,hashlib,importlib.util,io,json,math,sys,time
from pathlib import Path
import xml.etree.ElementTree as ET

FAMILY='effect'
COMMANDS=['effect.'+n for n in ('apply','list','remove','setParams','expandAppearance','duplicate','move')]
def load_local(name):
 s=importlib.util.spec_from_file_location('effect_'+name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
shape=load_local('command_shape');appearance=load_local('command_appearance')
CONTRACT=json.loads(Path(__file__).with_name('effect_catalog_contract.json').read_text())
CATALOG=CONTRACT['catalog'];DEFAULTS={e['id']:e['defaults'] for e in CATALOG}

def fx(id,params=None):return {'id':id,'params':{**copy.deepcopy(DEFAULTS[id]),**(params or {})},'visible':True}
def edit_list(name,items,p):
 i=p['index']
 if name=='remove':items.pop(i)
 elif name=='duplicate':items.insert(i+1,copy.deepcopy(items[i]))
 elif name=='setParams':
  items[i]['params'].update(copy.deepcopy(p.get('params',{})))
  if 'visible' in p:items[i]['visible']=p['visible']
 else:raise ValueError('effect_edit_unknown')
def move_list(src,dst,index,to,copying):
 item=copy.deepcopy(src[index]) if copying else src.pop(index);at=min(to,len(dst));dst.insert(at,item);return at
def item_of(p,f,key='item'):
 return p[key] if key in p else None if 'ids' in p or 'id' in p or p.get('target')=='contents' else f['activeItem']
def effects(n,item):return (n.setdefault('appearance',{}) if item is None else n['appearance']['items'][item]).setdefault('effects',[])
def expected(command,b,p,f,ret):
 if command not in COMMANDS:raise ValueError('effect_command_unknown')
 e=copy.deepcopy(b);name=command.split('.')[1]
 if name=='list':return e
 if name=='expandAppearance':raise ValueError('effect_expand_requires_geometry_contract')
 ids=appearance.targets(e,p,f);landed=None
 for id in ids:
  n=shape.find(e,id);item=item_of(p,f);stack=effects(n,item)
  if name=='apply':stack.append(fx(p['effect'],p.get('params')));landed=(len(stack)-1,item)
  elif name=='move':
   src=item_of(p,f,'fromItem');dst=p['toItem'] if 'toItem' in p else src;at=move_list(effects(n,src),effects(n,dst),p['from'],p['to'],p.get('copy',False));landed=landed or (at,dst)
  else:edit_list(name,stack,p)
  # 空效果列表在原生serde中省略。
  for row in [n.get('appearance',{}),*n.get('appearance',{}).get('items',[])]:
   if row.get('effects')==[]:row.pop('effects')
 returned={'ids':ids}
 if landed is not None:returned.update(index=landed[0],item=landed[1])
 if ret!=returned:raise ValueError('effect_return')
 return e

def walk(n):
 yield n
 for c in n['kind'].get('children',[]):yield from walk(c)
def bounds(n):
 points=[a['p'] for c in walk(n) for s in c['kind'].get('path',{}).get('subpaths',[]) for a in s['anchors']]
 if not points:raise ValueError('effect_geometry_empty')
 xs,ys=zip(*points);return [min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys)]
def rectangle(n,wanted):
 shape.near(bounds(n),wanted,'effect_expand_geometry')
 if n['kind']['type']!='path' or 'live' in n['kind']:raise ValueError('effect_expand_plain_path')
 s=n['kind']['path']['subpaths'];x,y,w,h=wanted
 if len(s)!=1 or s[0].get('closed') is not True or len(s[0]['anchors'])!=4:raise ValueError('effect_expand_geometry')
 points=sorted(a['p'] for a in s[0]['anchors']);shape.near(points,sorted([[x,y],[x+w,y],[x+w,y+h],[x,y+h]]),'effect_expand_geometry')
def outer(n):return {k:v for k,v in n.items() if k not in ('kind','appearance')}
def expected_outer(n):
 return {**outer(n),**({'knockout':'off'} if n['kind']['type']=='text' else {})}
def crop_original(n,id):
 result=copy.deepcopy(n);result['id']=id
 for k in ('name','opacity','blend','isolate','mask','attrs'):result.pop(k,None)
 result['appearance'].pop('effects',None);return result
def basic(n):
 for c in walk(n):
  ap=c.get('appearance',{})
  if ap.get('effects') or any(i.get('effects') or not i.get('visible',True) for i in ap.get('items',[])):raise ValueError('effect_expand_residual')
def image_node(n,model,observed):
 k=n['kind']
 if k['type']!='image' or k.get('link') is not None or model['images'].get(k['key'])!={'mime':'image/png'}:raise ValueError('effect_expand_image')
 shape.near(k['xf'][:4],[1,0,0,1],'effect_expand_image_scale')
 if not k['width']>0 or not k['height']>0:raise ValueError('effect_expand_image')
 if not any(m['width']==k['width'] and m['height']==k['height'] and m['nontransparentPixels']>0 and m['translucentPixels']>0 and m['decoded'] is True for m in observed['embeddedImages']):raise ValueError('effect_expand_image_pixels')

def validate_expand(s):
 b,a,p,f=(s[k] for k in ('before','after','params','fixture'));roots=f['expandRoots'];ids=s['returned']['ids']
 if ids!=roots:raise ValueError('effect_expand_return')
 left,right=copy.deepcopy(b),copy.deepcopy(a)
 for id in roots:
  old,new=shape.find(b,id),shape.find(a,id)
  if expected_outer(old)!=outer(new):raise ValueError('effect_expand_identity_transparency')
  basic(new)
  for model in (left,right):
   node=shape.find(model,id);node.clear();node.update(id=id,kind={'type':'qualified-expansion'})
 for model in (left,right):model.pop('next_id');model.pop('images')
 shape.near(shape.stable(left),shape.stable(right),'effect_expand_protected_tree')
 allnodes=[n for l in a['layers'] for n in walk(l)];allnodes += [c for n in list(allnodes) if n.get('mask') for c in walk(n['mask']['art'])];allids=[n['id'] for n in allnodes]
 oldnodes=[n for l in b['layers'] for n in walk(l)];oldnodes += [c for n in list(oldnodes) if n.get('mask') for c in walk(n['mask']['art'])];oldids={n['id'] for n in oldnodes}
 if any(id not in oldids and id<b['next_id'] for id in allids):raise ValueError('effect_expand_allocation')
 if len(allids)!=len(set(allids)) or max(allids)>=a['next_id'] or a['next_id']<b['next_id']:raise ValueError('effect_expand_allocation')
 if any(a['images'].get(k)!=v for k,v in b['images'].items()):raise ValueError('effect_expand_old_images')
 if s['round']==1:
  n=shape.find(a,2);rectangle(n,[7,7,70,46]);shape.near(n['appearance'],{'items':[{'kind':'fill','paint':shape.find(b,2)['appearance']['items'][0]['paint']}]},'effect_expand_fill')
  if a['images']!=b['images']:raise ValueError('effect_expand_unexpected_image')
 else:
  n=shape.find(a,f['multi']);ch=n['kind'].get('children',[])
  if n['kind']['type']!='group' or len(ch)!=2:raise ValueError('effect_expand_paint_order')
  rectangle(ch[0],[80,12,28,24]);shape.near(ch[0].get('opacity',1),.4,'effect_expand_item_transparency')
  if ch[0].get('blend')!='Multiply' or ch[0]['appearance']['items'][0]['paint']!=shape.find(b,f['multi'])['appearance']['items'][0]['paint']:raise ValueError('effect_expand_paint_order')
  shape.near(ch[1].get('appearance',{}),{'items':[{'kind':'fill','paint':shape.find(b,f['multi'])['appearance']['items'][1]['paint']}]},'effect_expand_stroke_paint')
  shape.near(bounds(ch[1]),[79,11,30,26],'effect_expand_stroke_outline')
  paths=[sp for c in walk(ch[1]) for sp in c['kind'].get('path',{}).get('subpaths',[])];area=0
  for sp in paths:
   pts=[v['p'] for v in sp['anchors']];area+=sum(x[0]*y[1]-y[0]*x[1] for x,y in zip(pts,pts[1:]+pts[:1]))/2
  shape.near(abs(area),208,'effect_expand_stroke_outline')
  shadow=shape.find(a,f['shadow']);parts=shadow['kind'].get('children',[])
  if shadow['kind']['type']!='group' or len(parts)!=2 or parts[1]['kind']['type']!='path':raise ValueError('effect_expand_shadow_order')
  image_node(parts[0],a,s['observed']);image_node(shape.find(a,f['blur']),a,s['observed'])
  text=shape.find(a,f['text']);nodes=list(walk(text))
  if any(n['kind']['type']=='text' for n in nodes) or not any(n['kind']['type'] in ('path','compound') for n in nodes):raise ValueError('effect_expand_text_outlines')
  tb=bounds(text)
  if not 10<tb[2]<24 or not 6<tb[3]<15:raise ValueError('effect_expand_text_bounds')
  crop=shape.find(a,f['crop']);parts=crop['kind'].get('children',[])
  if crop['kind']['type']!='group' or len(parts)!=2:raise ValueError('effect_expand_crop_marks')
  shape.near(bounds(parts[0]),[86,62,10,8],'effect_expand_crop_marks');shape.near(parts[0],crop_original(shape.find(b,f['crop']),parts[0]['id']),'effect_expand_crop_original');cb=bounds(parts[1])
  if not cb[0]<86 or not cb[1]<62 or cb[0]+cb[2]<=96 or cb[1]+cb[3]<=70:raise ValueError('effect_expand_crop_marks')
  transformed=shape.find(a,f['transform']);shape.near(bounds(transformed),[82,84,12,4],'effect_expand_transform_copies')
  if transformed['kind']['type']!='compound' or len(transformed['kind']['children'])!=2:raise ValueError('effect_expand_transform_copies')
  group=shape.find(a,f['group']);shape.near(bounds(group),[80,75,18,4],'effect_expand_group_geometry')
  if group['kind']['type']!='group' or group.get('appearance',{}).get('items'):raise ValueError('effect_expand_group_contents')
  if len(a['images'])-len(b['images'])!=2 or len(s['observed']['embeddedImages'])!=2:raise ValueError('effect_expand_image_count')

def validate_list(value,model,selection,active):
 shape.near(value['catalog'],CATALOG,'effect_catalog_contract')
 rows=[]
 for id in selection:
  ap=shape.find(model,id).get('appearance',{});rows.append({'id':id,'effects':ap.get('effects',[]),'items':[{'index':i,'kind':it['kind'],'effects':it.get('effects',[])} for i,it in enumerate(ap.get('items',[]))]})
 shape.near(value['applied'],rows,'effect_applied_readback')
 if value['activeItem']!=active:raise ValueError('effect_active_item_readback')
def validate_transition(command,s):
 b,a,r=(s[k] for k in ('before','after','reopened'));f=s['fixture']
 if shape.stable(a)!=shape.stable(r):raise ValueError('effect_reopen')
 if command=='effect.expandAppearance':validate_expand(s)
 else:shape.near(shape.stable(expected(command,b,s['params'],f,s['returned'])),shape.stable(a),'effect_tree_transition')
 if command=='effect.list':validate_list(s['returned'],b,f['selection'],f['activeItem'])
 validate_list(s['observed']['effectList'],a,f['selection'],f['activeItem'])
 if s['round']==2:
  previous=copy.deepcopy(f['revisionBefore']);shape.find(previous,f['revisionID'])['name']=f['revisionName']
  if shape.stable(previous)!=shape.stable(b) or shape.find(f['revisionBefore'],f['revisionID']).get('name')==f['revisionName']:raise ValueError('effect_local_revision')

def plain(call,id,color='#224466',stroke=False):
 call('appearance.clear',ids=[id]);call('paint.setFill',ids=[id],color=color)
 if stroke:call('paint.setStroke',ids=[id],color='#448822');call('stroke.set',ids=[id],weight=2,join='miter')
def apply(call,id,effect,params=None,item=None):return call('effect.apply',ids=[id],effect=effect,params=params or {},item=item)
def initialize(call):
 call('view.drawMode',mode='normal');call('appearance.setNewArtBasic',on=True);plain(call,2,stroke=True)
 apply(call,2,'distort.twist',{'angle':10});apply(call,2,'path.offsetPath',{'offset':1});apply(call,2,'stylize.dropShadow',{'x':1,'y':1,'blur':1});apply(call,2,'distort.twist',{'angle':4},0);apply(call,2,'path.offsetPath',{'offset':1},0);apply(call,2,'distort.twist',{'angle':3},1)
 layer=call('layer.new',name='Owned effect fixtures')['id'];children=[]
 for x,y in ((82,14),(90,42)):
  id=call('shape.rectangle',x=x,y=y,width=24,height=20)['id'];plain(call,id,stroke=True);apply(call,id,'distort.twist',{'angle':2});apply(call,id,'distort.twist',{'angle':1},0);children.append(id)
 call('layer.setCurrent',id=1);call('select.set',ids=[2]);return {'layer':layer,'children':children}

def prepare_expand(call,number,state):
 layer=state['layer'];f={}
 if number==1:
  plain(call,2);apply(call,2,'path.offsetPath',{'offset':3});apply(call,2,'path.offsetPath',{'offset':2},0);call('appearance.addFill',ids=[2]);call('appearance.setItem',ids=[2],index=2,color='#ff0000',visible=False);apply(call,2,'distort.twist',{'angle':90},2);call('transparency.set',ids=[2],opacity=72,blend='multiply',isolate=True)
  call('layer.setCurrent',id=1);mask=call('shape.rectangle',x=12,y=12,width=60,height=36)['id'];plain(call,mask,'#ffffff');call('transparency.makeOpacityMask',ids=[2,mask]);return {'ids':[2]},{'expandRoots':[2]}
 call('layer.setCurrent',id=layer);multi,shadow=state['children'];plain(call,multi,'#aa3311',True);apply(call,multi,'path.offsetPath',{'offset':2});call('appearance.setItem',ids=[multi],index=0,opacity=40,blend='multiply');call('appearance.addFill',ids=[multi]);call('appearance.setItem',ids=[multi],index=2,color='#0000ff',visible=False);call('transparency.set',ids=[multi],opacity=65,blend='multiply')
 plain(call,shadow,'#3377aa');apply(call,shadow,'stylize.dropShadow',{'x':2,'y':1,'blur':1})
 def rect(x,y,w,h):
  id=call('shape.rectangle',x=x,y=y,width=w,height=h)['id'];plain(call,id,'#aa6633');return id
 blur=rect(108,42,12,12);apply(call,blur,'blur.gaussian',{'radius':1})
 text=call('text.create',x=82,y=60,text='QA',size=12,font='Source Sans 3',color='#663399')['id'];call('appearance.addFill',ids=[text]);call('appearance.setItem',ids=[text],index=0,color='#663399')
 crop=rect(86,62,10,8);apply(call,crop,'cropMarks',{'style':'roman'})
 transform=rect(82,84,4,4);apply(call,transform,'distort.transform',{'moveH':8,'copies':1})
 g1=rect(80,74,4,4);g2=rect(94,74,4,4);call('select.set',ids=[g1,g2]);group=call('object.group')['id'];call('appearance.addFill',ids=[group]);call('appearance.setItem',ids=[group],index=0,color='#447744');apply(call,group,'distort.transform',{'moveV':1})
 f.update(multi=multi,shadow=shadow,blur=blur,text=text,crop=crop,transform=transform,group=group,expandRoots=[multi,shadow,blur,text,crop,transform,group]);return {'ids':[layer]},f

def prepare(call,command,number,directory,state):
 name=command.split('.')[1];second=number==2;p={'ids':[2]};f={'selection':[2],'activeItem':0}
 if name=='expandAppearance':
  p,more=prepare_expand(call,number,state);f.update(more);f['selection']=p['ids'];f['activeItem']=None
 elif name=='apply':p.update(effect='stylize.dropShadow' if second else 'distort.twist',params={'x':2,'blur':1} if second else {'angle':17,'ownedMarker':9});p.update({'ids':[state['layer']],'target':'contents'} if second else {'item':None})
 elif name=='setParams':p.update(index=0 if second else 1,params={'angle':15,'ownedRound':2} if second else {'offset':5},visible=second);p.update({} if second else {'item':None})
 elif name=='remove':p.update(index=0);p.update({} if second else {'item':None})
 elif name=='duplicate':p.update(index=0 if second else 1,item=1 if second else None)
 elif name=='move':p.update({'from':1,'to':1,'fromItem':0,'toItem':None,'copy':True} if second else {'from':0,'to':99,'fromItem':None,'toItem':0,'copy':False})
 elif name=='list':p={};f.update(selection=state['children'] if second else [2],activeItem=1 if second else 0)
 if second and name in ('setParams','remove'):p.pop('ids')
 call('select.set',ids=f['selection'])
 if name=='expandAppearance' and second:call('layer.target',id=state['layer'])
 call('appearance.setActiveItem',index=f['activeItem'])
 if second:
  id=state['children'][1];f.update(revisionBefore=call('document.json'),revisionID=id,revisionName='Owned revised effect control');call('layer.setProps',id=id,name=f['revisionName'])
 return p,f

def observe(call,command,params,returned,directory,fixture):
 result={'effectList':call('effect.list')}
 if command=='effect.expandAppearance' and 'blur' in fixture:
  from PIL import Image
  path=directory/'expanded-images.svg';call('document.export',path=str(path),format='svg',artboard=0,artboards=[0]);deadline=time.monotonic()+15
  while not path.exists() and time.monotonic()<deadline:time.sleep(.05)
  rows=[]
  for element in ET.fromstring(path.read_bytes()).iter():
   if element.tag.split('}')[-1]!='image':continue
   href=element.get('href',element.get('{http://www.w3.org/1999/xlink}href',''))
   if not href.startswith('data:image/png;base64,'):raise ValueError('effect_embedded_image_encoding')
   data=base64.b64decode(href.split(',',1)[1],validate=True)
   with Image.open(io.BytesIO(data)) as im:
    im.load();alpha=list(im.convert('RGBA').getchannel('A').getdata());rows.append({'sha256':hashlib.sha256(data).hexdigest(),'width':im.width,'height':im.height,'nontransparentPixels':sum(a>0 for a in alpha),'translucentPixels':sum(0<a<255 for a in alpha),'decoded':True})
  result.update(embeddedImages=rows,embeddedSvgSha256=hashlib.sha256(path.read_bytes()).hexdigest())
 return result

if __name__=='__main__':
 runner=load_local('command_family_window_diagnostic');family=type('EffectFamily',(),{'FAMILY':FAMILY,'COMMANDS':COMMANDS,'__file__':__file__,**{n:staticmethod(globals()[n]) for n in ('initialize','prepare','observe','validate_transition')}});runner.run(json.loads(Path(sys.argv[1]).read_text()),family)
