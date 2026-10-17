#!/usr/bin/env python3
"""固定属性面板验收：完整树、叠印目标、混合值与URL导出。"""
import copy,hashlib,importlib.util,json,sys,time
from pathlib import Path
import xml.etree.ElementTree as ET
FAMILY='attributes';COMMANDS=['attributes.info','attributes.set'];_recent=[]
def load_local(name):
 s=importlib.util.spec_from_file_location('attrs_'+name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
shape=load_local('command_shape')
def same(values):return values[0] if values and all(v==values[0] for v in values) else None
def center_default(n):return n['kind']['type']=='path' and 'live' in n['kind'] and n['kind']['live']['shape']!='line'
def edit_attrs(n,p):
 a=copy.deepcopy(n.get('attrs',{}))
 if 'showCenter' in p:
  if p['showCenter']==center_default(n):a.pop('showCenter',None)
  else:a['showCenter']=p['showCenter']
 for key in ('url','note','imageMap'):
  if key not in p:continue
  value=p[key].strip();value=value.lower() if key=='imageMap' else value
  if value==('none' if key=='imageMap' else ''):a.pop(key,None)
  else:a[key]=value
 if a:n['attrs']=a
 else:n.pop('attrs',None)
def recent(values,url):
 url=url.strip();return ([url]+[x for x in values if x!=url])[:10] if url else list(values)
def item_for(p,f,fill,first):
 if 'item' in p:return p['item']
 if 'ids' in p:return None
 index=f['activeItem'];items=first.get('appearance',{}).get('items',[])
 return index if index is not None and index<len(items) and (items[index]['kind']=='fill')==fill else None
def leaves(n):
 if n['kind']['type'] in ('group','layer'):return [v for c in n['kind']['children'] for v in leaves(c)]
 return [n]
def path_values(n):
 k=n['kind'];rules=[];directions=[]
 if k['type']=='path' and not k.get('guide',False):
  rules.append('evenOdd' if k.get('rule','NonZero').lower().replace('_','')=='evenodd' else 'nonZero')
  for sub in k['path']['subpaths']:
   a=[v['p'] for v in sub['anchors']];area=sum(a[i][0]*a[(i+1)%len(a)][1]-a[(i+1)%len(a)][0]*a[i][1] for i in range(len(a))) if a else 0;directions.append(area<0)
 elif 'children' in k:
  for c in k['children']:
   r,d=path_values(c);rules+=r;directions+=d
 return rules,directions
def flags(n,fill,index):
 items=n.get('appearance',{}).get('items',[]);selected=[it for i,it in enumerate(items) if (i==index if index is not None else (it['kind']=='fill')==fill)]
 if index is not None and (not selected or (selected[0]['kind']=='fill')!=fill):return []
 out=[it.get('overprint',False) for it in selected]
 if index is None and n['kind']['type']=='text':out += [r['style'].get('overprint_fill' if fill else 'overprint_stroke',False) for r in n['kind']['runs']]
 return out
def info(model,p,f,urls):
 ids=p.get('ids',f['selection']);nodes=[shape.find(model,i) for i in ids];out={'ids':ids,'recentUrls':urls}
 attrs=[n.get('attrs',{}) for n in nodes];out['showCenter']=same([a.get('showCenter',center_default(n)) for n,a in zip(nodes,attrs)])
 for key,default in (('imageMap','none'),('url',''),('note','')):out[key]=same([a.get(key,default) for a in attrs])
 rules=[];dirs=[]
 for n in nodes:r,d=path_values(n);rules+=r;dirs+=d
 out.update(fillRule=same(rules),reversed=same(dirs))
 for fill,key in ((True,'overprintFill'),(False,'overprintStroke')):
  index=item_for(p,f,fill,nodes[0]) if nodes else None;values=[]
  for n in nodes:
   for v in ([n] if index is not None else leaves(n)):values+=flags(v,fill,index)
  out[key]=same(values)
 return out
def expected(command,b,p,f):
 if command not in COMMANDS:raise ValueError('attributes_unknown')
 e=copy.deepcopy(b);urls=list(f['recentBefore']);changed=set();ids=p.get('ids',f['selection']);nodes=[shape.find(e,i) for i in ids]
 if command=='attributes.set':
  for fill,key in ((True,'overprintFill'),(False,'overprintStroke')):
   if key not in p:continue
   index=item_for(p,f,fill,nodes[0]) if nodes else None
   for n in nodes:
    for v in ([n] if index is not None else leaves(n)):
     before=copy.deepcopy(v);items=v.get('appearance',{}).get('items',[])
     for i,it in enumerate(items):
      if (i==index if index is not None else (it['kind']=='fill')==fill):
       if p[key]:it['overprint']=True
       else:it.pop('overprint',None)
     if index is None and v['kind']['type']=='text':
      k='overprint_fill' if fill else 'overprint_stroke'
      for r in v['kind']['runs']:
       if p[key]:r['style'][k]=True
       else:r['style'].pop(k,None)
     if v!=before:changed.add(v['id'])
  for n in nodes:
   before=copy.deepcopy(n);edit_attrs(n,p)
   if n!=before:changed.add(n['id'])
  if ids and 'url' in p:urls=recent(urls,p['url'])
 return e,urls,{'changed':len(changed)} if command=='attributes.set' else info(e,p,f,urls)
def validate_transition(command,s):
 f=s['fixture'];e,urls,ret=expected(command,s['before'],s['params'],f);shape.near(shape.stable(e),shape.stable(s['after']),'attributes_tree');shape.near(ret,s['returned'],'attributes_return');shape.near(shape.stable(s['after']),shape.stable(s['reopened']),'attributes_reopen')
 for row in s['observed']['queries']:shape.near(info(e,row['params'],f,urls),row['value'],'attributes_readback')
 if s['round']==2:
  prior=copy.deepcopy(f['revisionBefore']);shape.find(prior,2)['name']=f['revisionName'];shape.near(shape.stable(prior),shape.stable(s['before']),'attributes_local_revision')
 if s['observed']['svgLinks']!=sorted(n['attrs']['url'] for n in walk(e) if n.get('attrs',{}).get('url')):raise ValueError('attributes_svg_links')
def walk(model):
 def visit(n):return [n]+[v for c in n['kind'].get('children',[]) for v in visit(c)]
 return [v for n in model['layers'] for v in visit(n)]
def aset(call,**p):
 value=call('attributes.set',**p)
 if p.get('ids') and 'url' in p:_recent[:]=recent(_recent,p['url'])
 return value
def initialize(call):
 call('view.drawMode',mode='normal');call('view.overprintPreview',on=False)
 opened=call('window.panel',panel='attributes')
 if opened.get('open') is None:opened=call('window.panel',panel='attributes')
 if opened.get('open')!='attributes':raise ValueError('attributes_panel_open')
 call('appearance.clear',ids=[2]);call('paint.setFill',ids=[2],color='#224466');call('paint.setStroke',ids=[2],color='#448822');call('stroke.set',ids=[2],weight=2);call('appearance.addFill',ids=[2]);call('appearance.setItem',ids=[2],index=2,color='#224466')
 ids=[]
 for x,y in ((82,14),(98,32)):
  id=call('shape.rectangle',x=x,y=y,width=16,height=14)['id'];call('paint.setFill',ids=[id],color='#cc6633');ids.append(id)
 call('path.reverse',ids=[ids[0]],reversed=True);call('select.set',ids=ids);group=call('object.group')['id']
 text=call('text.create',x=82,y=64,text='Owned QA',size=8,font='Source Sans 3',color='#663399')['id'];call('appearance.addFill',ids=[text]);call('appearance.setItem',ids=[text],index=0,color='#663399');call('appearance.addStroke',ids=[text]);call('appearance.setItem',ids=[text],index=1,color='#448822')
 aset(call,ids=[text],overprintFill=True,overprintStroke=True,url='https://example.invalid/text',note='Owned text');aset(call,ids=[text],item=0,overprintFill=False)
 aset(call,ids=[2],overprintFill=True,overprintStroke=True,showCenter=False,imageMap='polygon',url='https://example.invalid/source',note='source note');call('path.setFillRule',ids=[2],rule='evenOdd');aset(call,ids=[ids[1]],overprintFill=True,overprintStroke=True)
 aset(call,ids=[group],imageMap='rectangle',note='group note')
 for i in range(12):aset(call,ids=[group],url='https://example.invalid/history-'+str(i))
 call('select.set',ids=[2]);return {'group':group,'text':text,'children':ids}
def prepare(call,command,number,directory,state):
 f={}
 if number==2:
  f={'revisionBefore':call('document.json'),'revisionName':'Owned revised attributes control'};call('layer.setProps',id=2,name=f['revisionName'])
 selection=[2,state['text']];call('select.set',ids=selection);call('appearance.setActiveItem',index=0)
 if command=='attributes.info':p={'ids':[2,state['group']]} if number==1 else {'ids':[state['text']],'item':0}
 else:p={'ids':[2,state['group'],state['text']],'overprintFill':True,'overprintStroke':True,'showCenter':False,'imageMap':' Rectangle ','url':' https://example.invalid/new-link ','note':'  Owned combined note  '} if number==1 else {'overprintFill':False,'overprintStroke':False,'showCenter':True,'imageMap':'none','url':'','note':''}
 f.update(selection=selection,activeItem=0,recentBefore=list(_recent),state=copy.deepcopy(state));return p,f
def observe(call,command,params,returned,directory,fixture):
 if command=='attributes.set' and fixture['selection'] and 'url' in params:_recent[:]=recent(_recent,params['url'])
 state=fixture['state'];queries=[]
 for p in ({'ids':[2]},{'ids':[state['group']]},{'ids':[state['text']]},{'ids':[state['text']],'item':0},{}):queries.append({'params':p,'value':call('attributes.info',**p)})
 path=directory/'attribute-links.svg';call('document.export',path=str(path),format='svg',artboard=0,artboards=[0]);deadline=time.monotonic()+15
 while not path.exists() and time.monotonic()<deadline:time.sleep(.05)
 data=path.read_bytes();links=sorted(el.get('href',el.get('{http://www.w3.org/1999/xlink}href')) for el in ET.fromstring(data).iter() if el.tag.split('}')[-1]=='a');return {'queries':queries,'svgLinks':links,'svgSha256':hashlib.sha256(data).hexdigest(),'svgPath':str(path.name),'svgDecoded':True}
if __name__=='__main__':
 family=type('AttributesFamily',(),{'FAMILY':FAMILY,'COMMANDS':COMMANDS,'__file__':__file__,**{n:staticmethod(globals()[n]) for n in ('initialize','prepare','observe','validate_transition')}});load_local('command_family_window_diagnostic').run(json.loads(Path(sys.argv[1]).read_text()),family)
