#!/usr/bin/env python3
"""固定辅助线验收：独立列表变换、局部修订及真实窗口坐标。"""
import copy,importlib.util,json,math,sys
from pathlib import Path
FAMILY='guide'
COMMANDS=['guide.add','guide.remove','guide.move']
def load_local(name):
 s=importlib.util.spec_from_file_location('guide_'+name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
shape=load_local('command_shape')
def expected(command,b,p,returned):
 if command not in COMMANDS:raise ValueError('guide_unknown')
 e=copy.deepcopy(b);guides=e['guides']
 if command=='guide.add':
  if returned!={'index':len(guides)}:raise ValueError('guide_return')
  guides.append({'vertical':p.get('vertical',False),'pos':p['pos']})
 elif command=='guide.remove':guides.pop(p['index'])
 else:guides[p['index']]['pos']=p['pos']
 return e

def screen_coordinate(guide,ui):
 """将零旋转的文档辅助线映射到实际逻辑画布坐标。"""
 r=ui['canvasRect'];v=ui['view'];axis=0 if guide['vertical'] else 1
 if v['rotation']!=0:raise ValueError('guide_view_rotation')
 return r[axis]+r[axis+2]/2+(guide['pos']-v['center']['x' if axis==0 else 'y'])*v['zoom']

def validate_transition(command,s):
 e=expected(command,s['before'],s['params'],s['returned']);shape.near(shape.stable(e),shape.stable(s['after']),'guide_tree')
 shape.near(shape.stable(s['after']),shape.stable(s['reopened']),'guide_reopen')
 if command!='guide.add' and s['returned'] is not None:raise ValueError('guide_return')
 if s['round']==2:
  f=s['fixture'];prior=copy.deepcopy(f['revisionBefore']);shape.find(prior,2)['name']=f['revisionName'];shape.near(shape.stable(prior),shape.stable(s['before']),'guide_local_revision')
  if shape.find(f['revisionBefore'],2).get('name')==f['revisionName']:raise ValueError('guide_local_revision')

def validate_context(probe):
 """锁定只禁用移动／删除；所有探针均须保全持久工程并恢复解锁。"""
 if probe['lockOn']!={'locked':True} or probe['lockOff']!={'locked':False}:raise ValueError('guide_lock_return')
 for key in ('locked','unlocked'):
  rows=probe[key]
  if [r['id'] for r in rows]!=COMMANDS or [r['enabled'] for r in rows]!=([True,False,False] if key=='locked' else [True,True,True]):raise ValueError('guide_lock_context')
 shape.near(shape.stable(probe['before']),shape.stable(probe['after']),'guide_lock_preservation')
def probe_context(call,query):
 before=call('document.json');on=call('view.guides.lock',locked=True);locked=query();off=call('view.guides.lock',locked=False);unlocked=query();after=call('document.json')
 probe={'before':before,'after':after,'lockOn':on,'lockOff':off,'locked':locked,'unlocked':unlocked};validate_context(probe);return probe

def initialize(call):
 call('view.drawMode',mode='normal');call('view.guides.lock',locked=False);call('view.guides.clear');call('paint.setFill',ids=[2],color='#224466')
 for vertical,pos in ((True,24),(False,60),(True,100),(False,84)):call('guide.add',vertical=vertical,pos=pos)
 return {}
def prepare(call,command,number,directory,state):
 fixture={}
 if number==2:
  fixture={'revisionBefore':call('document.json'),'revisionName':'Owned revised guide control'};call('layer.setProps',id=2,name=fixture['revisionName'])
 if command=='guide.add':params={'vertical':True,'pos':88} if number==1 else {'pos':36}
 elif command=='guide.remove':params={'index':1 if number==1 else 0}
 else:params={'index':0 if number==1 else 1,'pos':40 if number==1 else 70}
 return params,fixture
def observe(call,command,params,returned,directory,fixture):return call('document.inspect')
if __name__=='__main__':
 family=type('GuideFamily',(),{'FAMILY':FAMILY,'COMMANDS':COMMANDS,'__file__':__file__,**{n:staticmethod(globals()[n]) for n in ('initialize','prepare','observe','validate_transition','probe_context')}});load_local('command_family_guide').run(json.loads(Path(sys.argv[1]).read_text()),family)
