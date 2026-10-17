#!/usr/bin/env python3
"""固定安装色板命令验收：关联色、组、色库及逐轮原生语义。"""
import importlib.util
import json
from pathlib import Path
import sys

def load_local(name):
    spec=importlib.util.spec_from_file_location('swatch_'+name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
paint=load_local('command_paint')
FAMILY='swatch'
COMMANDS=['swatch.new','swatch.delete','swatch.newGroup','swatch.duplicate','swatch.sortByName','swatch.edit','swatch.list','swatch.move','swatch.addUsedColors','swatch.unused','swatch.merge','swatch.ungroup','swatch.sortByKind','swatch.spotOptions','swatch.editGroup','swatch.setSpot','swatch.library.list','swatch.library.get','swatch.library.add','swatch.resetDefaults','swatch.library.save','swatch.library.load']

def native_swatches(model):
    return [(w,None) for w in model['swatches']]+[(w,g['name']) for g in model['swatch_groups'] for w in g['swatches']]
def by_name(model):return {w['name']:w for w,g in native_swatches(model)}
def stable(model):return {k:v for k,v in model.items() if k!='metadata'}
def assert_color(value,expected):
    try:paint.color(value,expected)
    except (ValueError,KeyError,TypeError):raise ValueError('swatch_color') from None

def validate_transition(command,s):
    """原生工程与读回色板双向一致；逐命令断言不能由PASS标记代替。"""
    if command not in COMMANDS:raise ValueError('swatch_command_unknown')
    before,after,reopened=(s[k] for k in ('before','after','reopened'));a,b=map(paint.objects,(before,after));p=s['params'];ret=s['returned'];fixture=s['fixture']
    if set(a)!=set(b) or any(a[k]!=b[k] for k in a if k!=2) or before['artboards']!=after['artboards'] or {k:v for k,v in a[2].items() if k!='appearance'}!={k:v for k,v in b[2].items() if k!='appearance'}:raise ValueError('swatch_control')
    if stable(after)!=stable(reopened):raise ValueError('swatch_reopen')
    if 'listReopened' in s and s['listReopened']!=s['listAfter']:raise ValueError('swatch_reopen_list')
    prior,current=by_name(before),by_name(after);rows={r['name']:r for r in s['listAfter']['swatches']}
    if set(rows)-{'[Registration]'}!=set(current):raise ValueError('swatch_list_native')
    for w,group in native_swatches(after):
        row=rows[w['name']]
        if row['group']!=group or row['global']!=w['global'] or row['spot']!=w['spot']:raise ValueError('swatch_list_native')
        if w['paint']['type']=='solid' and row['color']!=w['paint']['color']:raise ValueError('swatch_list_native_color')
    fill=paint.paint(after);old_fill=paint.paint(before)
    queries=('swatch.list','swatch.unused','swatch.library.list','swatch.library.get','swatch.library.save','swatch.library.load')
    if command in queries and stable(before)!=stable(after):raise ValueError('swatch_readonly')
    if command=='swatch.new':
        if ret['names']!=[p['name']] or ret['name']!=p['name'] or p['name'] in prior:raise ValueError('swatch_new')
        w=current[p['name']];assert_color(w['paint'],p['color'])
        if w['global'] is not p['global'] or w['spot'] is not False:raise ValueError('swatch_global')
    elif command=='swatch.delete':
        if p['name'] in current or ret['deleted']!=[p['name']] or ret['unlinked']<1 or fill.get('swatch') is not None:raise ValueError('swatch_delete')
        if fill['color']!=old_fill['color']:raise ValueError('swatch_delete_color')
    elif command=='swatch.newGroup':
        group=next(g for g in after['swatch_groups'] if g['name']==p['name'])
        if [w['name'] for w in group['swatches']]!=p['swatches'] or ret['name']!=p['name']:raise ValueError('swatch_group')
    elif command=='swatch.duplicate':
        old,new=prior[p['name']],current[ret['name']]
        if new['name'] in prior or {k:v for k,v in old.items() if k!='name'}!={k:v for k,v in new.items() if k!='name'}:raise ValueError('swatch_duplicate')
    elif command in ('swatch.sortByName','swatch.sortByKind'):
        def rank(w):
            t=w['paint']['type'];return 0 if t=='none' else (2 if w['spot'] else 1) if t=='solid' else 3 if t=='gradient' else 4
        key=(lambda w:(not w['name'].startswith('['),w['name'].lower())) if command.endswith('Name') else rank
        if after['swatches']!=sorted(before['swatches'],key=key):raise ValueError('swatch_sort')
        if [g['name'] for g in before['swatch_groups']]!=[g['name'] for g in after['swatch_groups']]:raise ValueError('swatch_sort_groups')
        for old,new in zip(before['swatch_groups'],after['swatch_groups']):
            if new['swatches']!=sorted(old['swatches'],key=key):raise ValueError('swatch_sort')
    elif command=='swatch.edit':
        name=p.get('newName',p['name']);assert_color(current[name]['paint'],p['color']);assert_color(fill,p['color'])
        if fill.get('swatch')!=name or ret['name']!=name or ret['relinked']<1:raise ValueError('swatch_relink')
        if name!=p['name'] and p['name'] in current:raise ValueError('swatch_rename')
    elif command=='swatch.list':
        expected=s['listAfter'] if 'group' not in p else {'swatches':[r for r in s['listAfter']['swatches'] if r['group']==p['group']],'groups':[g for g in s['listAfter']['groups'] if g['name']==p['group']]}
        if ret!=expected:raise ValueError('swatch_list_query')
    elif command=='swatch.move':
        if ret['moved']!=len(p['names']):raise ValueError('swatch_move')
        destination=next(g for g in after['swatch_groups'] if g['name']==p['group'])
        if [w['name'] for w in destination['swatches']][:len(p['names'])]!=p['names']:raise ValueError('swatch_move_order')
    elif command=='swatch.addUsedColors':
        if len(ret['added'])!=1 or ret['linked']<1:raise ValueError('swatch_add_used')
        name=ret['added'][0];assert_color(current[name]['paint'],fixture['color'])
        if fill.get('swatch')!=name or current[name]['global'] is not True:raise ValueError('swatch_add_used_link')
    elif command=='swatch.unused':
        if fixture['unused'] not in ret['names'] or fixture['used'] in ret['names'] or '[None]' in ret['names']:raise ValueError('swatch_unused')
    elif command=='swatch.merge':
        keep,gone=p['names'];assert_color(fill,prior[keep]['paint']['color'])
        if gone in current or keep not in current or ret['name']!=keep or ret['merged']!=[gone] or fill.get('swatch')!=keep or ret['relinked']<1:raise ValueError('swatch_merge')
    elif command=='swatch.ungroup':
        old=next(g for g in before['swatch_groups'] if g['name']==p['name']);names=[w['name'] for w in old['swatches']]
        if any(g['name']==p['name'] for g in after['swatch_groups']) or ret['swatches']!=names or after['swatches'][-len(names):]!=old['swatches']:raise ValueError('swatch_ungroup')
    elif command=='swatch.spotOptions':
        if ret['useLab'] is not p['useLab'] or after.get('spot_use_lab',True) is not p['useLab'] or before.get('spot_use_lab',True)==p['useLab'] or ret['relinked']<1:raise ValueError('swatch_spot_options')
        if fill.get('swatch')!=fixture['spot'] or fill['color']==old_fill['color']:raise ValueError('swatch_spot_relink')
    elif command=='swatch.editGroup':
        group=next(g for g in after['swatch_groups'] if g['name']==p['rename'])
        if ret['name']!=p['rename'] or len(group['swatches'])!=len(p['colors']) or ret['relinked']<1:raise ValueError('swatch_edit_group')
        for w,c in zip(group['swatches'],p['colors']):assert_color(w['paint'],c)
        assert_color(fill,p['colors'][0])
    elif command=='swatch.setSpot':
        w=current[p['name']]
        if w['spot'] is not p['spot'] or w['global'] is not True or ret['name']!=p['name'] or ret['spot'] is not p['spot']:raise ValueError('swatch_spot')
    elif command=='swatch.library.list':
        libraries=ret['libraries'];ids=[x['id'] for x in libraries]
        if not libraries or len(ids)!=len(set(ids)) or fixture['library'] not in ids or any(x['count']<0 for x in libraries):raise ValueError('swatch_library_list')
    elif command in ('swatch.library.get','swatch.library.load'):
        lib=ret if command.endswith('get') else s['observed']['library']
        if command.endswith('get') and lib['id']!=fixture['library']:raise ValueError('swatch_library_get')
        if [w['name'] for w in lib['swatches']]!=fixture['libraryNames']:raise ValueError('swatch_library_names')
        if command.endswith('load') and (lib['id']!=ret['library'] or ret['count']!=len(fixture['libraryNames'])):raise ValueError('swatch_library_load')
        for w,c in zip(lib['swatches'],fixture['libraryColors']):assert_color({'type':'solid','color':w['color']},c)
    elif command=='swatch.library.add':
        if ret['added']!=fixture['libraryNames'] or ret.get('existing')!=[] or ret['applied']!=fixture['libraryNames'][0]:raise ValueError('swatch_library_add')
        for name,c in zip(fixture['libraryNames'],fixture['libraryColors']):assert_color(current[name]['paint'],c)
        assert_color(fill,fixture['libraryColors'][0])
    elif command=='swatch.resetDefaults':
        defaults=fixture['defaults']
        if p['replace']:
            if after['swatches']!=defaults['swatches'] or after['swatch_groups']!=defaults['swatch_groups']:raise ValueError('swatch_defaults_replace')
        elif 'Black' not in current or fixture['custom'] not in current or 'Black' not in ret['added']:raise ValueError('swatch_defaults_add')
        if old_fill.get('color')!=fill.get('color'):raise ValueError('swatch_defaults_art')
    elif command=='swatch.library.save':
        observed=s['observed'];lib=observed['library']
        if ret['format']!=p['format'] or ret['count']!=2 or observed['decoded'] is not True or len(observed['sha256'])!=64:raise ValueError('swatch_library_save')
        if [w['name'] for w in lib['swatches']]!=p['names']:raise ValueError('swatch_library_save_names')
        for w,name in zip(lib['swatches'],p['names']):assert_color({'type':'solid','color':w['color']},current[name]['paint']['color'])
    if command not in ('swatch.delete','swatch.edit','swatch.addUsedColors','swatch.merge','swatch.spotOptions','swatch.editGroup','swatch.library.add','swatch.resetDefaults') and a!=b:raise ValueError('swatch_unrelated_art')

def initialize(call):
    call('swatch.resetDefaults',replace=True);defaults=call('document.json')
    call('paint.setFill',ids=[2],color='#224466');call('paint.setStroke',ids=[2],none=True)
    call('swatch.new',name='QA Base A',color='#663399',**{'global':True});call('swatch.new',name='QA Base B',color='#559944',**{'global':True})
    call('swatch.newGroup',name='QA Group',swatches=['QA Base A','QA Base B'])
    return {'defaults':defaults}

def prepare(call,command,number,directory,state):
    n=str(number);value='#559944' if number==2 else '#663399';fixture={}
    def new(name,color=value,**extra):return call('swatch.new',name=name,color=color,**extra)['name']
    def library():
        names=['QA Library A '+n,'QA Library B '+n];colors=['#123456','#aabbcc'] if number==1 else ['#225588','#bb7733']
        text='GIMP Palette\nName: QA Library '+n+'\nColumns: 2\n#\n'+'\n'.join(' '.join(str(int(c[i:i+2],16)) for i in (1,3,5))+' '+name for name,c in zip(names,colors))+'\n'
        loaded=call('swatch.library.load',data=text,name='QA Library '+n+'.gpl');fixture.update(library=loaded['library'],libraryNames=names,libraryColors=colors)
        return loaded['library'],text
    if command=='swatch.new':return {'name':'QA New '+n,'color':value,'global':True},fixture
    if command=='swatch.delete':
        name=new('QA Delete '+n,**{'global':True});call('paint.setFill',ids=[2],swatch=name);return {'name':name,'unlink':True},fixture
    if command=='swatch.newGroup':return {'name':'QA New Group '+n,'swatches':['QA Base A','QA Base B']},fixture
    if command=='swatch.duplicate':return {'name':'QA Base B' if number==2 else 'QA Base A'},fixture
    if command in ('swatch.sortByName','swatch.sortByKind'):
        new('Z QA Sort '+n);new('A QA Sort '+n,'#112233',spot=True);return {},fixture
    if command=='swatch.edit':
        name='QA Renamed 1' if number==2 else 'QA Base A';call('paint.setFill',ids=[2],swatch=name)
        return {'name':name,'newName':'QA Renamed '+n,'color':'#226688' if number==2 else '#bb5533'},fixture
    if command=='swatch.list':return ({'group':'QA Group'} if number==1 else {}),fixture
    if command=='swatch.move':
        destination='QA Destination '+n;call('swatch.newGroup',name=destination);return {'names':['QA Base B','QA Base A'],'group':destination,'to':0},fixture
    if command=='swatch.addUsedColors':
        fixture['color']='#13a579' if number==1 else '#9527b3';call('paint.setFill',ids=[2],color=fixture['color']);return {'selection':True,'global':True},fixture
    if command=='swatch.unused':
        fixture.update(unused=new('QA Unused '+n),used='QA Base A');call('paint.setFill',ids=[2],swatch='QA Base A');return {},fixture
    if command=='swatch.merge':
        names=[new('QA Merge A '+n,'#663399',**{'global':True}),new('QA Merge B '+n,'#559944',**{'global':True})];call('paint.setFill',ids=[2],swatch=names[1]);return {'names':names},fixture
    if command=='swatch.ungroup':
        name='QA Ungroup '+n;call('swatch.newGroup',name=name,swatches=['QA Base A','QA Base B']);return {'name':name},fixture
    if command=='swatch.spotOptions':
        if number==1:fixture['spot']=new('QA Lab Spot',{'l':60,'a':40,'b':20},spot=True)
        else:fixture['spot']='QA Lab Spot'
        call('paint.setFill',ids=[2],swatch=fixture['spot']);return {'useLab':number==2},fixture
    if command=='swatch.editGroup':
        name='QA Edited Group 1' if number==2 else 'QA Group';call('paint.setFill',ids=[2],swatch='QA Base A');return {'group':name,'colors':['#118855','#aa3366'] if number==1 else ['#bb7733','#225588'],'rename':'QA Edited Group '+n},fixture
    if command=='swatch.setSpot':return {'name':'QA Base A','spot':number==1},fixture
    if command in ('swatch.library.list','swatch.library.get','swatch.library.add'):
        lib,text=library()
        return ({} if command.endswith('list') else {'library':lib} if command.endswith('get') else {'library':lib,'apply':'fill'}),fixture
    if command=='swatch.resetDefaults':
        call('swatch.delete',name='Black');fixture.update(defaults=state['defaults'],custom=new('QA Custom '+n));call('paint.setFill',ids=[2],color='#123456');return {'replace':number==2},fixture
    if command=='swatch.library.save':return {'path':str(directory/('qa.vcswatches' if number==1 else 'qa.gpl')),'format':'vcswatches' if number==1 else 'gpl','names':['QA Base A','QA Base B'],'name':'QA Saved '+n},fixture
    if command=='swatch.library.load':
        if number==1:
            lib,text=library();return {'data':text.replace('QA Library','QA Loaded'),'name':'QA Loaded.gpl'},{'libraryNames':[x.replace('QA Library','QA Loaded') for x in fixture['libraryNames']],'libraryColors':fixture['libraryColors']}
        saved=call('swatch.library.save',format='vcswatches',names=['QA Base A','QA Base B'],name='QA Lossless')
        return {'data':saved['data'],'name':'QA Lossless.vcswatches'},{'libraryNames':['QA Base A','QA Base B'],'libraryColors':['#663399','#559944']}
    raise ValueError('swatch_prepare_unknown')

def observe(call,command,params,returned,directory,fixture):
    if command=='swatch.library.load':return {'library':call('swatch.library.get',library=returned['library'])}
    if command=='swatch.library.save':
        path=Path(params['path']);data=path.read_bytes();loaded=call('swatch.library.load',path=str(path));lib=call('swatch.library.get',library=loaded['library'])
        if params['format']=='vcswatches':json.loads(data)
        elif not data.startswith(b'GIMP Palette'):raise ValueError('swatch_saved_palette_format')
        import hashlib
        return {'library':lib,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'decoded':True}
    return {}

if __name__=='__main__':
    module=type('SwatchFamily',(),{'__file__':__file__,'FAMILY':FAMILY,'COMMANDS':COMMANDS,'initialize':staticmethod(initialize),'prepare':staticmethod(prepare),'observe':staticmethod(observe),'validate_transition':staticmethod(validate_transition)})
    load_local('command_family').run(json.loads(Path(sys.argv[1]).read_text()),module)
