#!/usr/bin/env python3
"""逐命令paint族原生验收：仅拥有的签名桌面、合成工程与显式固定安装。"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import shutil
import socket
import sys
import time
import xml.etree.ElementTree as ET

PAINT_COMMANDS=['paint.setFill','paint.setStroke','paint.swap','paint.default','paint.toggleActive','paint.none','paint.editGradient','paint.setGradientGeom','paint.sampleColor','paint.invert','paint.complement','paint.lastColor','paint.lastGradient','paint.recent','paint.proxies','paint.freeform.addPoint','paint.freeform.setPoint','paint.freeform.deletePoint','paint.freeform.addLine','paint.freeform.splitLine','paint.freeform.selectPoint','paint.freeform.get']
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def objects(model):
    result={}
    def visit(value):
        if not isinstance(value,dict) or type(value.get('id')) is not int or value['id'] in result:raise ValueError('paint_model')
        kind=value['kind'];result[value['id']]={**value,'kind':{k:v for k,v in kind.items() if k!='children'}}
        if 'children' in kind:result[value['id']]['kind']['children']=[x['id'] for x in kind['children']]
        for child in kind.get('children',[]):visit(child)
    for layer in model['layers']:visit(layer)
    return result

def paint(model,kind='fill'):
    return next(x['paint'] for x in objects(model)[2]['appearance']['items'] if x['kind']==kind)
def rgb(value):
    if isinstance(value,str):return tuple(int(value[i:i+2],16)/255 for i in (1,3,5))
    if isinstance(value,list) and len(value)==3 and all(type(x) in (int,float) and math.isfinite(x) and 0<=x<=1 for x in value):return tuple(value)
    if not isinstance(value,dict) or value.get('model')!='rgb':raise ValueError('paint_color')
    return tuple(value[k] for k in ('r','g','b'))
def close(actual,expected,reason):
    if len(actual)!=len(expected) or any(not math.isfinite(a) or abs(a-b)>2e-5 for a,b in zip(actual,expected)):raise ValueError(reason)
def color(actual,expected):
    if actual.get('type')!='solid':raise ValueError('paint_color')
    close(rgb(actual['color']),rgb(expected),'paint_color')

def validate_transition(command,stage):
    """从真实原生快照复核每条命令，拒绝未知命令、控制对象漂移和重开不一致。"""
    if command not in PAINT_COMMANDS:raise ValueError('paint_command_unknown')
    before,after,reopened=(stage[k] for k in ('before','after','reopened'));a,b,c=map(objects,(before,after,reopened));params=stage['params']
    if set(a)!=set(b) or any(a[k]!=b[k] for k in a if k!=2) or before['artboards']!=after['artboards'] or {k:v for k,v in a[2].items() if k!='appearance'}!={k:v for k,v in b[2].items() if k!='appearance'}:raise ValueError('paint_control')
    if b!=c or after['artboards']!=reopened['artboards']:raise ValueError('paint_reopen')
    fill=paint(after);pb,pa=stage['proxiesBefore'],stage['proxiesAfter'];fb,fa=stage['freeformBefore'],stage['freeformAfter'];ret=stage['returned']
    if command in ('paint.setFill','paint.sampleColor'):color(fill,params['color'])
    elif command=='paint.setStroke':color(paint(after,'stroke'),params['color'])
    elif command=='paint.swap':
        if fill!=paint(before,'stroke') or paint(after,'stroke')!=paint(before):raise ValueError('paint_swap')
    elif command=='paint.default':
        color(fill,'#ffffff');color(paint(after,'stroke'),'#000000')
        if next(x['width'] for x in b[2]['appearance']['items'] if x['kind']=='stroke')!=1:raise ValueError('paint_default_stroke')
    elif command=='paint.none':
        if fill!={'type':'none'}:raise ValueError('paint_none')
    elif command=='paint.toggleActive':
        if pa['fillActive'] is not params['fill'] or ret['fillActive'] is not params['fill'] or a!=b or pb['fillActive']==pa['fillActive']:raise ValueError('paint_active_proxy')
    elif command=='paint.editGradient':
        if fill['gradient']['kind'].lower()!=params['kind']:raise ValueError('paint_gradient')
        stops=fill['gradient']['stops']
        if len(stops)!=len(params['stops']):raise ValueError('paint_gradient')
        for actual,expected in zip(stops,params['stops']):
            close([actual['offset']],[expected['offset']],'paint_gradient');close(rgb(actual['color']),rgb(expected['color']),'paint_color')
    elif command=='paint.setGradientGeom':
        geom=fill['geom']
        for name in ('start','end'):close([geom[name]['x'],geom[name]['y']],params[name],'paint_gradient_geometry')
    elif command in ('paint.invert','paint.complement'):
        prior=rgb(paint(before)['color']);expected=[1-x for x in prior] if command=='paint.invert' else [max(prior)+min(prior)-x for x in prior]
        close(rgb(fill['color']),expected,'paint_color')
    elif command=='paint.lastColor':color(fill,stage['recentBefore']['lastColor']['color'])
    elif command=='paint.lastGradient':
        expected=stage['recentBefore']['lastGradient']
        if fill['gradient']!=expected['gradient']:raise ValueError('paint_last_gradient')
    elif command=='paint.recent':
        if a!=b or ret!=stage['recentAfter'] or ret['lastColor']['color']!=paint(after)['color']:raise ValueError('paint_recent')
    elif command=='paint.proxies':
        if a!=b or ret!=pa or ret['fill']!=fill:raise ValueError('paint_proxies')
    elif command=='paint.freeform.get':
        if a!=b or ret!=fa or len(ret['points'])<4:raise ValueError('paint_freeform_get')
    elif command=='paint.freeform.selectPoint':
        if a!=b or fa['selected']!=params['index'] or ret['index']!=params['index']:raise ValueError('paint_freeform_select')
    elif command in ('paint.freeform.addPoint','paint.freeform.setPoint'):
        index=ret['index'];point=fa['points'][index]
        if command.endswith('addPoint') and len(fa['points'])!=len(fb['points'])+1:raise ValueError('paint_freeform_count')
        if command.endswith('setPoint') and (index!=params['index'] or len(fa['points'])!=len(fb['points'])):raise ValueError('paint_freeform_count')
        close(point['at'],params['at'],'paint_freeform_point');close(rgb(point['color']),rgb(params['color']),'paint_color')
        for name in ('opacity','spread'):
            if name in params:close([point[name]],[params[name]],'paint_freeform_point')
        expected_selection=index if command.endswith('addPoint') else fb['selected']
        if fa['selected']!=expected_selection:raise ValueError('paint_freeform_select')
    elif command=='paint.freeform.deletePoint':
        if len(fa['points'])!=len(fb['points'])-1 or fa['points']!=[x for i,x in enumerate(fb['points']) if i!=params['index']]:raise ValueError('paint_freeform_delete')
    elif command=='paint.freeform.addLine':
        if fa['points']!=fb['points'] or len(fa['lines'])!=len(fb['lines'])+1 or fa['lines'][ret['line']]!=params['points']:raise ValueError('paint_freeform_line')
    elif command=='paint.freeform.splitLine':
        line,segment=params['line'],params['segment'];old=fb['lines'][line];new=fa['lines'][line];index=ret['index']
        if len(fa['points'])!=len(fb['points'])+1 or new!=old[:segment+1]+[index]+old[segment+1:] or fa['points'][:-1]!=fb['points']:raise ValueError('paint_freeform_split')
        if len(old)!=2:raise ValueError('paint_split_fixture')
        # 固定上游90e022b的两点Catmull-Rom曲线，端点重复；颜色仍按原始t插值。
        p,q=(fb['points'][i]['at'] for i in old);t=params['t'];u=.5*t+1.5*t*t-t*t*t
        close(fa['points'][index]['at'],[(1-u)*x+u*y for x,y in zip(p,q)],'paint_freeform_point')
        cp,cq=(rgb(fb['points'][i]['color']) for i in old)
        close(rgb(fa['points'][index]['color']),[(1-t)*x+t*y for x,y in zip(cp,cq)],'paint_color')
        if fa['selected']!=index:raise ValueError('paint_freeform_select')


def run(config):
    from PIL import Image
    root=Path(config['output']).resolve();root.mkdir(exist_ok=False);host=json.loads(Path(config['host']).read_text());entry=next(x for x in host['skills'] if x['name']=='vectorcraft-use');skill=Path(entry['path']);source=Path(config['source']);runtime=Path(config['runtime']);binary=runtime/'vectorcraft/0.2.0-craft.2/vectorcraft-cli'
    def load(name):
        spec=importlib.util.spec_from_file_location('command_paint_'+name,skill/'scripts'/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
    commands=load('commands');installed=skill.parent.parent;lock=json.loads((skill/'scripts/runtime.lock.json').read_text());assert sha(binary)==lock['artifacts']['darwin-arm64']['binarySha256']
    assert host['publicTagVerified'] is True and host['artifactRef']=='v0.1.0-dev.64'
    original_skill=load('asset_reader');catalog=json.loads((skill/'references/command-coverage.json').read_text());assert [x['id'] for x in catalog['commands'] if x['id'].startswith('paint.')]==PAINT_COMMANDS
    desktop_lock=json.loads((skill/'scripts/desktop.lock.json').read_text());desktop=load('desktop').inspect(runtime/'vectorcraft-desktop/0.2.0',desktop_lock)
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    owned=load('desktop_session').OwnedSession(commands.backend_argv(str(binary),root,'bridge',f'127.0.0.1:{port}'),desktop,'vectorcraft',root,port);cases=[];calls=[]
    def write(path,value):Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    def call(name,**params):
        record={'command':name,'params':params,'state':'submitted'};calls.append(record);write(root/'journal.json',calls)
        result=commands.parse_reply(owned.request('tools/call',{'name':'run_command','arguments':{'command':name,'params':params}}));record.update(state='completed',result=result);write(root/'journal.json',calls);return result
    def gradient(kind='linear'):
        return {'kind':kind,'stops':[{'offset':0,'color':'#ff0000'},{'offset':1,'color':'#0000ff'}]}
    def params_for(command,round_number):
        second=round_number==2;at=[48,36] if second else [24,24];value='#559944' if second else '#663399'
        if command in ('paint.setFill','paint.setStroke','paint.sampleColor'):return {'ids':[2],'color':value}
        if command=='paint.editGradient':return {'ids':[2],'kind':'radial' if second else 'linear','stops':gradient()['stops']}
        if command=='paint.setGradientGeom':return {'ids':[2],'start':[12,48] if second else [12,12],'end':[72,12] if second else [72,48]}
        if command=='paint.toggleActive':
            call('paint.toggleActive',fill=not second);return {'fill':second}
        if command in ('paint.default','paint.none'):
            call('paint.setFill',ids=[2],color=value);return {'ids':[2]} if command.endswith('default') else {}
        if command=='paint.lastColor':
            call('select.set',ids=[]);call('paint.setFill',color=value);call('select.set',ids=[2]);return {'ids':[2]}
        if command=='paint.lastGradient':
            call('paint.setFill',ids=[2],gradient=gradient('radial' if second else 'linear'));call('paint.setFill',ids=[2],color=value);return {'ids':[2]}
        if command in ('paint.recent','paint.proxies'):
            call('paint.setFill',ids=[2],color=value);return {}
        if command=='paint.freeform.addPoint':return {'ids':[2],'at':at,'color':value,'opacity':.8 if second else .5,'spread':.25}
        if command=='paint.freeform.setPoint':return {'ids':[2],'index':0,'at':at,'color':value,'opacity':.8 if second else .5,'spread':.25}
        if command=='paint.freeform.deletePoint':return {'ids':[2],'index':call('paint.freeform.addPoint',ids=[2],at=at,color=value)['index']}
        if command=='paint.freeform.addLine':return {'ids':[2],'points':[2,3] if second else [0,1]}
        if command=='paint.freeform.splitLine':
            line=call('paint.freeform.addLine',ids=[2],points=[2,3] if second else [0,1])['line'];return {'ids':[2],'line':line,'segment':0,'t':.25 if second else .5}
        if command=='paint.freeform.selectPoint':
            call('paint.freeform.selectPoint',index=None);return {'index':1 if second else 0}
        if command=='paint.freeform.get':
            if second:call('paint.freeform.addPoint',ids=[2],at=at,color=value)
            return {'stroke':False}
        return {'ids':[2]} if command in ('paint.swap','paint.invert','paint.complement') else {}
    try:
        with owned:
            discovery=owned.request('tools/list',{});write(root/'tools.json',discovery)
            registry=commands.runtime_rows(owned,mode='bridge');write(root/'registry.json',registry)
            expected={commands.backend_identifier(x['id'],mode='bridge') for x in catalog['commands']}
            if not expected.issubset({x['id'] for x in registry}):raise ValueError('paint_registry_missing_locked_command')
            for command in PAINT_COMMANDS:
                case=root/command;case.mkdir();seed=case/'source.vectorcraft';shutil.copyfile(source,seed);seed_sha=sha(seed)
                call('document.open',path=str(seed));call('select.set',ids=[2]);call('paint.toggleActive',fill=True);call('paint.setFill',ids=[2],color='#224466');call('paint.setStroke',ids=[2],color='#448822')
                if command.startswith('paint.freeform.'):call('paint.setFill',ids=[2],gradient=gradient('freeform'))
                elif command=='paint.setGradientGeom':call('paint.setFill',ids=[2],gradient=gradient())
                stages=[]
                for number in (1,2):
                    stage_dir=case/('v'+str(number));stage_dir.mkdir();call('select.set',ids=[2]);call('paint.toggleActive',fill=True);params=params_for(command,number)
                    state=next(x for x in commands.runtime_rows(owned,{'filter':command},mode='bridge') if x['id']==command);assert state['enabled'] is True
                    before=call('document.json');proxies_before=call('paint.proxies');recent_before=call('paint.recent');freeform_before=call('paint.freeform.get',stroke=False) if command.startswith('paint.freeform.') else None
                    returned=call(command,**params);after=call('document.json');proxies_after=call('paint.proxies');recent_after=call('paint.recent');freeform_after=call('paint.freeform.get',stroke=False) if command.startswith('paint.freeform.') else None
                    ui=commands.parse_reply(owned.request('tools/call',{'name':'inspect_ui','arguments':{}}));assert ui['activeDocument'] is not None
                    screenshot=commands.parse_reply(owned.request('tools/call',{'name':'screenshot','arguments':{}}),stage_dir,number)
                    image_record=next(x for x in screenshot['content'] if x['type']=='image');canvas=stage_dir/image_record['path'];assert sha(canvas)==image_record['sha256']
                    with Image.open(canvas) as image:image.load();assert image.size==(128,96)
                    project=stage_dir/'project.vectorcraft';call('document.save',path=str(project),modified=946684800+number)
                    exports=[]
                    for fmt in ('svg','png'):
                        path=stage_dir/('artboard-1.'+fmt);call('document.export',path=str(path),format=fmt,artboard=0,artboards=[0]);deadline=time.monotonic()+15
                        while not path.exists() and time.monotonic()<deadline:time.sleep(.05)
                        digest=sha(path)
                        if fmt=='svg':ET.fromstring(path.read_bytes())
                        else:
                            with Image.open(path) as image:image.load();assert image.size==(128,96)
                        assert sha(path)==digest;exports.append({'format':fmt,'sha256':digest,'decoded':True,'path':str(path.relative_to(root))})
                    call('document.open',path=str(project));reopened=call('document.json')
                    stage={'round':number,'context':state,'params':params,'before':before,'after':after,'reopened':reopened,'returned':returned,'proxiesBefore':proxies_before,'proxiesAfter':proxies_after,'recentBefore':recent_before,'recentAfter':recent_after,'freeformBefore':freeform_before,'freeformAfter':freeform_after,'ui':ui,'canvas':{**image_record,'path':str(canvas.relative_to(root)),'width':128,'height':96},'exports':exports,'nativeProjectSha256':sha(project)}
                    validate_transition(command,stage);stages.append(stage);write(case/'progress.json',stages)
                    if number==1:first_sha=sha(project)
                assert sha(seed)==seed_sha and sha(case/'v1/project.vectorcraft')==first_sha
                cases.append({'command':command,'result':'PASS','mode':'owned-signed-desktop-bridge','sourcePreserved':True,'previousDeliveryPreserved':True,'stages':stages});write(root/'progress.json',cases);print('PASS',command,flush=True);call('file.close')
        proof={'schema':'vectorcraft-command-family/v1','result':'PASS','family':'paint','pluginVersion':host['pluginVersion'],'pluginCommit':host['pluginCommit'],'sourceRef':host['skillSourceRef'],'sourceCommit':host['skillSourceCommit'],'hostVersion':host['hostVersion'],'platform':host['platform'],'runtimeSha256':sha(binary),'desktopBinarySha256':desktop_lock['binarySha256'],'driverSha256':sha(__file__),'catalogSha256':sha(skill/'references/command-coverage.json'),'sourceProjectSha256':sha(source),'cases':cases,'allOwnedProcessesStopped':owned.stopped and (owned.session is None or owned.session.process.poll() is not None),'listenerOwnedByPID':owned.listener_verified,'registeredCommands':len(registry),'scope':'22 paint commands in owned signed desktop contexts;44 native saves/reopens and88 SVG/PNG exports;native canvas images,not OS-window screenshots or human/model creative review'}
        write(root/'proof.json',proof);print(json.dumps({'result':'PASS','commands':len(cases),'stages':sum(len(x['stages']) for x in cases),'ownedStopped':owned.stopped}),flush=True)
    except BaseException as error:
        write(root/'failure.json',{'result':'FAIL','error':type(error).__name__+': '+str(error),'completedCommands':[x['command'] for x in cases],'allOwnedProcessesStopped':owned.stopped and (owned.session is None or owned.session.process.poll() is not None),'noAutomaticReplay':True});raise

if __name__=='__main__':run(json.loads(Path(sys.argv[1]).read_text()))
