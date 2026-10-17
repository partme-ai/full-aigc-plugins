#!/usr/bin/env python3
"""固定安装描边命令验收：参数、宽度点单位、轮廓及受保护外观。"""
import importlib.util
import json
from pathlib import Path
import sys

def load_local(name):
    spec=importlib.util.spec_from_file_location('stroke_'+name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
paint=load_local('command_paint')
FAMILY='stroke'
COMMANDS=['stroke.set','stroke.setAdvanced','stroke.widthProfile.add','stroke.widthProfile.delete','stroke.widthProfile.reset','stroke.widthProfile.list','stroke.widthPoint.set','stroke.widthPoint.remove','stroke.widthPoint.copy','stroke.widthProfile.set']
DEFAULTS={'width':1,'cap':'Butt','join':'Miter','miter_limit':4,'align':'Center','arrow_align':'Extend','arrow_scale':[100,100],'start_arrow':None,'end_arrow':None,'dash':None,'profile':None,'brush':None}
def stroke(model):return next(x for x in paint.objects(model)[2]['appearance']['items'] if x['kind']=='stroke')
def normalized(value):return {**DEFAULTS,**value}
def stable(model):return {k:v for k,v in model.items() if k!='metadata'}
def profiles(stage,when):return stage['fixture']['profilesBefore'] if when=='before' else stage['observed']['profilesAfter']
def custom(stage,when):return [p for p in profiles(stage,when)['profiles'] if not p['builtIn']]
def points(value):return [list(p) for p in value['profile']['points']] if value['profile'] else [[0,1,1],[1,1,1]]

def validate_transition(command,s):
    """逐命令计算预期原生描边；保持其余对象、填充及文档字段。"""
    if command not in COMMANDS:raise ValueError('stroke_command_unknown')
    before,after,reopened=(s[k] for k in ('before','after','reopened'));a,b=map(paint.objects,(before,after));p=s['params'];ret=s['returned']
    if set(a)!=set(b) or any(a[k]!=b[k] for k in a if k!=2) or {k:v for k,v in a[2].items() if k!='appearance'}!={k:v for k,v in b[2].items() if k!='appearance'} or {k:v for k,v in before.items() if k not in ('layers','metadata')}!={k:v for k,v in after.items() if k not in ('layers','metadata')}:raise ValueError('stroke_control')
    def protected(value):return {**value,'items':[i for i in value['items'] if i['kind']!='stroke']}
    if protected(a[2]['appearance'])!=protected(b[2]['appearance']):raise ValueError('stroke_protected_appearance')
    if stable(after)!=stable(reopened):raise ValueError('stroke_reopen')
    expected_context='open' if command=='stroke.setAdvanced' or command.startswith('stroke.widthPoint.') or command=='stroke.widthProfile.set' else 'closed'
    if s['fixture'].get('pathContext')!=expected_context or any(path['closed'] is not (expected_context=='closed') for path in a[2]['kind']['path']['subpaths']):raise ValueError('stroke_applicable_path_context')
    prior,current=normalized(stroke(before)),normalized(stroke(after));expected={**prior}
    if command=='stroke.set':
        for param,key in (('weight','width'),('miterLimit','miter_limit')):
            if param in p:expected[key]=p[param]
        for param,key in (('cap','cap'),('join','join'),('align','align'),('arrowAlign','arrow_align')):
            if param in p:expected[key]=p[param].title()
        for param,key in (('startArrow','start_arrow'),('endArrow','end_arrow')):
            if param in p:expected[key]=p[param]
        if 'dash' in p:expected['dash']=None if p['dash'] is None else {**(prior['dash'] or {'pattern':[],'offset':0,'align_corners':False}),'pattern':p['dash']}
        if expected['dash']:
            if 'dashOffset' in p:expected['dash']={**expected['dash'],'offset':p['dashOffset']}
            if 'alignDashes' in p:expected['dash']={**expected['dash'],'align_corners':p['alignDashes']}
        if 'profile' in p:expected['profile']=None if p['profile']=='uniform' else {'points':next(x['points'] for x in profiles(s,'before')['profiles'] if x['id']==p['profile'])}
        if current['width']!=expected['width']:raise ValueError('stroke_weight')
    elif command=='stroke.setAdvanced':
        expected['arrow_scale']=list(p['arrowScale'])
        if p.get('swapArrows'):
            expected['start_arrow'],expected['end_arrow']=prior['end_arrow'],prior['start_arrow'];expected['arrow_scale'].reverse()
        previous=points(prior)
        expected['profile']={'points':[[t,r,l] for t,l,r in previous]} if p['flipProfile']=='across' else {'points':sorted([[1-t,l,r] for t,l,r in previous])}
    elif command=='stroke.widthProfile.add':
        added=[x for x in custom(s,'after') if x['id']==p['name']]
        if ret['name']!=p['name'] or len(added)!=1 or added[0]['points']!=points(prior) or len(custom(s,'after'))!=len(custom(s,'before'))+1:raise ValueError('stroke_profile_add')
    elif command=='stroke.widthProfile.delete':
        if ret['deleted']!=p['name'] or [x for x in custom(s,'before') if x['id']!=p['name']]!=custom(s,'after'):raise ValueError('stroke_profile_delete')
    elif command=='stroke.widthProfile.reset':
        if ret['removed']!=len(custom(s,'before')) or not ret['removed'] or custom(s,'after'):raise ValueError('stroke_profile_reset')
    elif command=='stroke.widthProfile.list':
        if ret!=profiles(s,'after') or ret['current']!=s['fixture']['current'] or next(x['points'] for x in ret['profiles'] if x['id']==ret['current'])!=points(prior):raise ValueError('stroke_profile_list')
    elif command=='stroke.widthProfile.set':expected['profile']=None if p['points'] is None else {'points':p['points']}
    elif command=='stroke.widthPoint.set':
        previous=points(prior)
        if 'index' in p:previous.pop(p['index'])
        else:previous=[x for x in previous if abs(x[0]-p['t'])>1e-10]
        # 固定引擎distortcmds.rs：侧宽pt / (描边weight / 2)。
        point=[p['t'],2*p['left']/prior['width'],2*p['right']/prior['width']];expected['profile']={'points':sorted(previous+[point])}
        if expected['profile']['points'][ret['index']]!=point:raise ValueError('stroke_width_point_index')
    elif command=='stroke.widthPoint.remove':
        previous=points(prior);previous.pop(p['index']);expected['profile']={'points':previous} if previous else None
    elif command=='stroke.widthPoint.copy':
        previous=points(prior);point=[p['t'],*previous[p['index']][1:]];expected['profile']={'points':sorted(previous+[point])}
        if expected['profile']['points'][ret['index']]!=point:raise ValueError('stroke_width_point_index')
    if current!=expected:raise ValueError('stroke_native_semantics')
    before_builtin=[x for x in profiles(s,'before')['profiles'] if x['builtIn']];after_builtin=[x for x in profiles(s,'after')['profiles'] if x['builtIn']]
    if before_builtin!=after_builtin:raise ValueError('stroke_builtin_profiles')
    if command not in ('stroke.widthProfile.add','stroke.widthProfile.delete','stroke.widthProfile.reset') and custom(s,'before')!=custom(s,'after'):raise ValueError('stroke_unrequested_preferences')

def initialize(call):
    if any(not x['builtIn'] for x in call('stroke.widthProfile.list')['profiles']):call('stroke.widthProfile.reset')
    call('paint.setFill',ids=[2],color='#224466');call('paint.setStroke',ids=[2],color='#448822')
    call('stroke.set',ids=[2],weight=4,startArrow='Triangle',endArrow='Circle',profile='uniform')
    call('stroke.widthProfile.set',ids=[2],points=[[0,1,2],[.25,2,3],[1,3,1]])
    return {}

def prepare(call,command,number,directory,state):
    second=number==2;n=str(number);open_path=command=='stroke.setAdvanced' or command.startswith('stroke.widthPoint.') or command=='stroke.widthProfile.set';fixture={'pathContext':'open' if open_path else 'closed'}
    if open_path and not second:call('path.setAnchors',id=2,subpaths=[{'anchors':[{'x':12,'y':12},{'x':72,'y':12},{'x':72,'y':48}],'closed':False}])
    if command=='stroke.set':p={'ids':[2],'weight':6 if second else 3,'cap':'square' if second else 'round','join':'round' if second else 'bevel','miterLimit':8 if second else 6,'align':'inside' if second else 'outside','dash':[1,3] if second else [3,2],'dashOffset':2 if second else 1,'alignDashes':second,'startArrow':'Arrow' if second else 'Triangle','endArrow':'Diamond' if second else 'Circle','arrowAlign':'extend' if second else 'tip','profile':'wave' if second else 'lens'}
    elif command=='stroke.setAdvanced':p={'ids':[2],'arrowScale':[60,200] if second else [150,75],'swapArrows':True,'flipProfile':'along' if second else 'across'}
    elif command=='stroke.widthProfile.add':
        call('stroke.widthProfile.set',ids=[2],points=[[0,1,2],[.6 if second else .3,number+2,3],[1,3,1]]);p={'name':'QA Width Added '+n}
    elif command=='stroke.widthProfile.delete':
        name='QA Width Delete '+n;call('stroke.widthProfile.add',name=name);call('stroke.set',ids=[2],profile=name);p={'name':name}
    elif command=='stroke.widthProfile.reset':
        for i,suffix in enumerate(('A','B')):
            call('stroke.widthProfile.set',ids=[2],points=[[0,1,2],[.2+.1*i,number+2+i,3],[1,3,1]])
            call('stroke.widthProfile.add',name='QA Width Reset '+n+suffix)
        p={}
    elif command=='stroke.widthProfile.list':
        fixture['current']='taperEnd' if second else 'lens';call('stroke.set',ids=[2],profile=fixture['current']);p={}
    elif command=='stroke.widthPoint.set':
        p={'id':2,'t':.65 if second else .4,'left':3 if second else 2,'right':5 if second else 6}
        if second:p['index']=next(i for i,x in enumerate(stroke(call('document.json'))['profile']['points']) if x[0]==.4)
    elif command=='stroke.widthPoint.remove':
        added=call('stroke.widthPoint.set',id=2,t=.65 if second else .4,left=2,right=6);p={'id':2,'index':added['index']}
    elif command=='stroke.widthPoint.copy':p={'id':2,'index':1,'t':.65 if second else .4}
    elif command=='stroke.widthProfile.set':p={'ids':[2],'points':None if second else [[0,1,2],[.5,3,1],[1,2,4]]}
    else:raise ValueError('stroke_prepare_unknown')
    fixture['profilesBefore']=call('stroke.widthProfile.list');return p,fixture

def observe(call,command,params,returned,directory,fixture):return {'profilesAfter':call('stroke.widthProfile.list'),'preferenceRestartAcceptance':'NOT_RUN','preferenceScope':'owned no-preferences desktop session only;native project profile persistence is checked separately'}

if __name__=='__main__':
    module=type('StrokeFamily',(),{'__file__':__file__,'FAMILY':FAMILY,'COMMANDS':COMMANDS,'initialize':staticmethod(initialize),'prepare':staticmethod(prepare),'observe':staticmethod(observe),'validate_transition':staticmethod(validate_transition)})
    load_local('command_family').run(json.loads(Path(sys.argv[1]).read_text()),module)
