#!/usr/bin/env python3
"""固定字符样式验收：完整树、字节范围、局部覆盖及样式引用。"""
import copy,importlib.util,json,sys
from pathlib import Path
FAMILY='charStyle';COMMANDS=['charStyle.'+v for v in ('list','new','apply','redefine','setAttrs','duplicate','rename','delete')]
NORMAL='[Normal Character Style]'
DEFAULT=dict(font_family='Source Sans 3',font_style='Regular',size=12.,tracking=0.,baseline_shift=0.,h_scale=100.,v_scale=100.,rotation=0.,fill={'type':'solid','color':{'model':'rgb','r':0.,'g':0.,'b':0.}},stroke={'type':'none'},stroke_width=0.,underline=False,strikethrough=False,all_caps=False)
BLUE={'type':'solid','color':{'model':'rgb','r':0.,'g':0.,'b':1.}};RED={'type':'solid','color':{'model':'rgb','r':1.,'g':0.,'b':0.}}
def load_local(name):
 s=importlib.util.spec_from_file_location('char_'+name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
shape=load_local('command_shape')
def texts(model):
 def walk(n):
  if n['kind']['type']=='text':yield n
  for child in n['kind'].get('children',[]):yield from walk(child)
 return [n for l in model['layers'] for n in walk(l)]
def attrs(style):return {k:copy.deepcopy(v) for k,v in style.items() if k!='style_name'}
def definition(model,name):
 return next((copy.deepcopy(s['attrs']) for s in model.get('char_styles',[]) if s['name']==name),{} if name==NORMAL else None)
def unique(base,defs,copy_name=False):
 names={s['name'] for s in defs}|{NORMAL};i=1
 while True:
  name=base if copy_name and i==1 else base+' '+str(i)
  if name not in names:return name
  i+=1
def restyle(cur,old,new):
 out=copy.deepcopy(cur)
 for k,v in new.items():
  if k not in old or cur.get(k)==old[k]:out[k]=copy.deepcopy(v)
 return out
def style_at(runs,byte):
 off=0
 for r in runs:
  off+=len(r['text'].encode())
  if byte<=off:return attrs(r['style'])
 return attrs(runs[-1]['style'])
def style_range(runs,start,end,fn):
 """按UTF8字节向下对齐字符边界，应用范围后合并相邻同样式片段。"""
 chars=[]
 for run in runs:
  for ch in run['text']:chars.append((ch,copy.deepcopy(run['style'])))
 if not chars:return [{'text':'','style':fn(copy.deepcopy(runs[0]['style']))}]
 positions=[0]
 for ch,_ in chars:positions.append(positions[-1]+len(ch.encode()))
 floor=lambda n:max(v for v in positions if v<=min(max(0,n),positions[-1]))
 a,b=sorted((floor(start),floor(end)));out=[]
 for pos,(ch,style) in zip(positions,chars):
  if a<=pos<b:style=fn(style)
  if out and out[-1]['style']==style:out[-1]['text']+=ch
  else:out.append({'text':ch,'style':style})
 return out
def listing(model):
 defs=model.get('char_styles',[]);names=[NORMAL]+[s['name'] for s in defs if s['name']!=NORMAL]
 return {'styles':[{'name':name,'attrs':definition(model,name),'uses':sum(r['style'].get('style_name')==(None if name==NORMAL else name) for n in texts(model) for r in n['kind']['runs'])} for name in names]}
def expected(command,b,p,f):
 e=copy.deepcopy(b);defs=e.setdefault('char_styles',[]);verb=command.split('.')[1];name=p.get('name');ret=None
 if command not in COMMANDS:raise ValueError('char_style_unknown')
 if verb=='list':return e,listing(e)
 if verb=='new':
  name=name if name is not None else unique('Character Style',defs);value=p.get('attrs',style_at(shape.find(e,f['selection'][0])['kind']['runs'],0));defs.append({'name':name,'attrs':copy.deepcopy(value)});ret={'name':name}
 elif verb=='duplicate':
  newname=unique(name+' copy',defs,True);defs.append({'name':newname,'attrs':definition(e,name)});ret={'name':newname}
 elif verb=='apply':
  value=definition(e,name);normal=definition(e,NORMAL);ids=[p['id']] if 'id' in p else p.get('ids',f['selection']);ret={'count':len(ids)}
  def apply(cur):
   base={**copy.deepcopy(DEFAULT),**normal} if p.get('clearOverrides',False) else copy.deepcopy(cur)
   base.update(copy.deepcopy(value));base.pop('style_name',None)
   if name!=NORMAL:base['style_name']=name
   return base
  for id in ids:
   n=shape.find(e,id)
   if n['kind']['type']!='text':continue
   runs=n['kind']['runs'];length=sum(len(r['text'].encode()) for r in runs);n['kind']['runs']=style_range(runs,p.get('start',0) if 'id' in p else 0,p.get('end',length) if 'id' in p else length,apply)
 elif verb in ('setAttrs','redefine'):
  old=definition(e,name);new=p['attrs'] if verb=='setAttrs' else style_at(shape.find(e,p.get('id',f['selection'][0]))['kind']['runs'],p.get('start',0))
  target=next((d for d in defs if d['name']==name),None)
  if target is None:defs.append({'name':name,'attrs':copy.deepcopy(new)})
  else:target['attrs']=copy.deepcopy(new)
  for n in texts(e):
   for r in n['kind']['runs']:
    if r['style'].get('style_name')==(None if name==NORMAL else name):r['style']=restyle(r['style'],old,new)
 elif verb in ('rename','delete'):
  to=p.get('to','').strip()
  if verb=='rename':next(d for d in defs if d['name']==name)['name']=to
  else:e['char_styles']=[d for d in defs if d['name']!=name]
  for n in texts(e):
   for r in n['kind']['runs']:
    if r['style'].get('style_name')==name:
     if verb=='rename':r['style']['style_name']=to
     else:r['style'].pop('style_name',None)
 return e,ret

def validate_transition(command,s):
 e,ret=expected(command,s['before'],s['params'],s['fixture']);shape.near(shape.stable(e),shape.stable(s['after']),'char_style_tree');shape.near(ret,s['returned'],'char_style_return');shape.near(shape.stable(e),shape.stable(s['reopened']),'char_style_reopen');shape.near(listing(e),s['observed']['list'],'char_style_list')
 if s['ui']['ui'].get('open_panel')!='charStyles':raise ValueError('char_style_panel')
 if s['listBefore']!=s['listAfter'] or s['listAfter']!=s['listReopened']:raise ValueError('char_style_swatch_preservation')
 if s['round']==2:
  f=s['fixture'];prior=copy.deepcopy(f['revisionBefore']);shape.find(prior,2)['name']=f['revisionName'];shape.near(shape.stable(prior),shape.stable(s['before']),'char_style_local_revision')
  if shape.find(f['revisionBefore'],2).get('name')==f['revisionName']:raise ValueError('char_style_local_revision')

def initialize(call):
 call('view.drawMode',mode='normal');ids=[]
 for y,text in ((54,'Ownéd QA'),(86,'Owned Ref')):ids.append(call('text.create',x=78,y=y,text=text,size=8,font='Source Sans 3',color='#000000')['id'])
 call('charStyle.new',name='Owned Alpha',attrs={'size':8.,'font_family':'Source Sans 3','underline':True,'strikethrough':False,'fill':BLUE})
 call('charStyle.new',name='Owned Beta',attrs={'size':8.,'font_family':'Source Sans 3','underline':False,'strikethrough':True,'fill':RED})
 call('charStyle.new',name='Owned Control',attrs={'underline':False})
 call('charStyle.apply',name='Owned Alpha',ids=[ids[0]]);call('charStyle.apply',name='Owned Beta',ids=[ids[1]])
 call('text.setRangeStyle',id=ids[0],start=0,end=3,underline=False)
 panel=call('window.panel',panel='charStyles')
 if panel.get('open') is None:call('window.panel',panel='charStyles')
 return {'ids':ids}
def prepare(call,command,number,directory,state):
 a,b=state['ids'];selection=[a,b] if command=='charStyle.apply' and number==2 else [a];call('select.set',ids=selection);verb=command.split('.')[1]
 if verb=='apply' and number==1:
  call('charStyle.apply',name=NORMAL,ids=[a]);call('text.setRangeStyle',id=a,strikethrough=True)
 if verb=='list' and number==2:call('charStyle.new',name='Owned Extra',attrs={'underline':True})
 if verb=='redefine' and number==2:call('text.setRangeStyle',id=b,underline=True,strikethrough=False,fill='#0000ff')
 params={}
 if verb=='new':params={'name':'Owned New','attrs':{'underline':True,'fill':RED}} if number==1 else {}
 elif verb=='apply':params={'name':'Owned Alpha','id':a,'start':6,'end':4} if number==1 else {'name':'Owned Alpha','clearOverrides':True}
 elif verb=='redefine':params={'name':'Owned Alpha','id':b,'start':4}
 elif verb=='setAttrs':params={'name':'Owned Alpha','attrs':{'underline':False,'strikethrough':True}} if number==1 else {'name':'Owned Alpha','attrs':{'underline':True,'strikethrough':False,'fill':RED}}
 elif verb=='duplicate':params={'name':'Owned Alpha'}
 elif verb=='rename':params={'name':'Owned Alpha' if number==1 else 'Owned Renamed 1','to':' Owned Renamed '+str(number)+' '}
 elif verb=='delete':params={'name':'Owned Alpha' if number==1 else 'Owned Beta'}
 f={'selection':selection,'state':copy.deepcopy(state)}
 if number==2:
  f.update(revisionBefore=call('document.json'),revisionName='Owned revised character style control');call('layer.setProps',id=2,name=f['revisionName'])
 return params,f
def observe(call,command,params,returned,directory,fixture):return {'list':call('charStyle.list')}
if __name__=='__main__':
 family=type('CharFamily',(),{'FAMILY':FAMILY,'COMMANDS':COMMANDS,'__file__':__file__,**{n:staticmethod(globals()[n]) for n in ('initialize','prepare','observe','validate_transition')}});load_local('command_family_window_diagnostic').run(json.loads(Path(sys.argv[1]).read_text()),family)
