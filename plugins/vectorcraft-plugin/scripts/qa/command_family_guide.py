#!/usr/bin/env python3
"""辅助线窗口验收驱动，增加真实锁定上下文探针；旧驱动保留。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import socket
import time
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def load_path(name,path):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
def write(path,value):Path(path).write_text(json.dumps(value,ensure_ascii=False,separators=(',',':'))+'\n')

def capture_window(owned,commands,directory,number,root):
    """只对纯读取窗口捕获最多三次尝试；从不重放编辑请求。"""
    from PIL import Image
    directory.mkdir();attempts=[]
    for attempt in range(1,4):
        target=directory/('capture-'+str(attempt)+'.png')
        reply=owned.request('tools/call',{'name':'screenshot','arguments':{'window':True,'path':str(target)}})
        try:capture=commands.parse_reply(reply,directory,number*10+attempt)
        except RuntimeError:
            attempts.append({'attempt':attempt,'status':'native-read-error'});write(directory/'attempts.json',attempts)
            write(directory/('error-'+str(attempt)+'.json'),reply)
            if attempt==3:raise
            continue
        record=next(x for x in capture['content'] if x['type']=='image');meta=next(x['value'] for x in capture['content'] if x['type']=='text');path=directory/record['path']
        if meta.get('window') is not True or sha(path)!=record['sha256']:raise ValueError('family_window_digest')
        with Image.open(path) as image:
            image.load()
            width,height=image.size;scale=width/1440
            if scale not in (1,2) or height!=900*scale or (meta.get('width',width),meta.get('height',height))!=(width,height):raise ValueError('family_window_size')
        attempts.append({'attempt':attempt,'status':'PASS'});write(directory/'attempts.json',attempts)
        return {**record,'path':str(path.relative_to(root)),'width':width,'height':height,'pixelScale':int(scale),'window':True,'decoded':True,'readAttempts':attempts}

def ready_ui(owned,commands):
    """最多20次纯读取等待新文档自动适配；不重放编辑。"""
    attempts=[]
    for number in range(1,21):
        ui=commands.parse_reply(owned.request('tools/call',{'name':'inspect_ui','arguments':{}}))
        ready=ui.get('view',{}).get('fitted') is True
        attempts.append({'attempt':number,'status':'PASS' if ready else 'awaiting-fit'})
        if ready:return ui,attempts
        time.sleep(.05)
    raise ValueError('guide_ui_fit_timeout')

def run(config,family):
    """只执行显式命令族断言；未知结果停止，不重试编辑请求。"""
    from PIL import Image
    root=Path(config['output']).resolve();root.mkdir(exist_ok=False)
    host=json.loads(Path(config['host']).read_text());entry=next(x for x in host['skills'] if x['name']=='vectorcraft-use');skill=Path(entry['path'])
    source=Path(config['source']).resolve();runtime=Path(config['runtime']);binary=runtime/'vectorcraft/0.2.0-craft.2/vectorcraft-cli'
    load=lambda name:load_path('family_installed_'+name,skill/'scripts'/(name+'.py'))
    commands=load('commands');vendor=load_path('family_vendor',ROOT/'scripts/vendor/skill_vendor.py')
    if not host['publicTagVerified'] or host['artifactRef']!='v0.1.0-dev.64':raise ValueError('family_public_tag')
    def identities():
        result={x['name']:vendor.hash_skill_dir(Path(x['path'])) for x in host['skills']}
        if result!={x['name']:x['sha256'] for x in host['skills']}:raise ValueError('family_installed_skill_drift')
        return result
    before_ids=identities();catalog_path=skill/'references/command-coverage.json';catalog=json.loads(catalog_path.read_text())
    if [x['id'] for x in catalog['commands'] if x['id'].startswith(family.FAMILY+'.')]!=family.COMMANDS:raise ValueError('family_catalog_drift')
    lock=json.loads((skill/'scripts/runtime.lock.json').read_text());desktop_lock=json.loads((skill/'scripts/desktop.lock.json').read_text())
    if sha(binary)!=lock['artifacts']['darwin-arm64']['binarySha256']:raise ValueError('family_runtime_drift')
    desktop=load('desktop').inspect(runtime/'vectorcraft-desktop/0.2.0',desktop_lock)
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    owned=load('desktop_session').OwnedSession(commands.backend_argv(str(binary),root,'bridge',f'127.0.0.1:{port}'),desktop,'vectorcraft',root,port)
    journal=[];cases=[]
    def call(command,**params):
        record={'command':command,'params':params,'state':'submitted'};journal.append(record);write(root/'journal.json',journal)
        reply=owned.request('tools/call',{'name':'run_command','arguments':{'command':command,'params':params}})
        if reply.get('isError'):
            write(root/'native-error.json',reply);record['state']='returned-error-outcome-unknown';write(root/'journal.json',journal)
        value=commands.parse_reply(reply)
        record.update(state='completed',result=value);write(root/'journal.json',journal);return value
    try:
        with owned:
            registry=commands.runtime_rows(owned,mode='bridge');write(root/'registry.json',registry)
            if not {commands.backend_identifier(x['id'],mode='bridge') for x in catalog['commands']}.issubset({x['id'] for x in registry}):raise ValueError('family_registry_drift')
            for command in family.COMMANDS:
                case=root/command;case.mkdir();seed=case/'source.vectorcraft';shutil.copyfile(source,seed);seed_sha=sha(seed)
                call('document.open',path=str(seed));call('select.set',ids=[2]);call('paint.toggleActive',fill=True)
                state=family.initialize(call);stages=[];first_sha=None
                for number in (1,2):
                    directory=case/('v'+str(number));directory.mkdir();call('select.set',ids=[2]);call('paint.toggleActive',fill=True)
                    params,fixture=family.prepare(call,command,number,directory,state)
                    context_probe=family.probe_context(call,lambda:commands.runtime_rows(owned,{'filter':'guide.'},mode='bridge'))
                    context=next(x for x in commands.runtime_rows(owned,{'filter':command},mode='bridge') if x['id']==command)
                    if context['enabled'] is not True:raise ValueError('family_command_disabled:'+command)
                    before=call('document.json');list_before=call('swatch.list')
                    returned=call(command,**params);after=call('document.json');list_after=call('swatch.list')
                    observed=family.observe(call,command,params,returned,directory,fixture)
                    ui,ui_attempts=ready_ui(owned,commands)
                    if ui['activeDocument'] is None:raise ValueError('family_no_gui_document')
                    screen=commands.parse_reply(owned.request('tools/call',{'name':'screenshot','arguments':{}}),directory,number)
                    canvas=next(x for x in screen['content'] if x['type']=='image');image_path=directory/canvas['path']
                    if sha(image_path)!=canvas['sha256']:raise ValueError('family_canvas_digest')
                    with Image.open(image_path) as image:
                        image.load()
                        if image.size!=(128,96):raise ValueError('family_canvas_size')
                    window=capture_window(owned,commands,directory/'window',number,root)
                    ui_after=commands.parse_reply(owned.request('tools/call',{'name':'inspect_ui','arguments':{}}))
                    if {k:ui_after[k] for k in ('view','canvasRect')}!={k:ui[k] for k in ('view','canvasRect')}:raise ValueError('guide_ui_capture_drift')
                    project=directory/'project.vectorcraft';call('document.save',path=str(project),modified=946684800+number);exports=[]
                    for fmt in ('svg','png'):
                        path=directory/('artboard-1.'+fmt);call('document.export',path=str(path),format=fmt,artboard=0,artboards=[0]);deadline=time.monotonic()+15
                        while not path.exists() and time.monotonic()<deadline:time.sleep(.05)
                        digest=sha(path)
                        if fmt=='svg':ET.fromstring(path.read_bytes())
                        else:
                            with Image.open(path) as image:
                                image.load()
                                if image.size!=(128,96):raise ValueError('family_export_size')
                        if sha(path)!=digest:raise ValueError('family_export_changed')
                        exports.append({'format':fmt,'path':str(path.relative_to(root)),'sha256':digest,'decoded':True})
                    call('document.open',path=str(project));reopened=call('document.json');list_reopened=call('swatch.list')
                    stage={'round':number,'uiReadAttempts':ui_attempts,'uiAfterCapture':{k:ui_after[k] for k in ('view','canvasRect')},'contextProbe':context_probe,'context':context,'params':params,'fixture':fixture,'before':before,'after':after,'reopened':reopened,'returned':returned,'listBefore':list_before,'listAfter':list_after,'listReopened':list_reopened,'observed':observed,'ui':ui,'window':window,'canvas':{**canvas,'path':str(image_path.relative_to(root)),'width':128,'height':96},'exports':exports,'nativeProjectSha256':sha(project)}
                    write(directory/'stage.json',stage);family.validate_transition(command,stage);stages.append(stage)
                    if number==1:first_sha=sha(project)
                if sha(seed)!=seed_sha or sha(case/'v1/project.vectorcraft')!=first_sha:raise ValueError('family_previous_delivery_changed')
                cases.append({'command':command,'result':'PASS','mode':'owned-signed-desktop-bridge','sourcePreserved':True,'previousDeliveryPreserved':True,'stages':stages});write(root/'progress.json',cases);print('PASS',command,flush=True);call('file.close')
        proof={'schema':'vectorcraft-command-family/v1','result':'PASS','family':family.FAMILY,'pluginVersion':host['pluginVersion'],'pluginCommit':host['pluginCommit'],'sourceRef':host['skillSourceRef'],'sourceCommit':host['skillSourceCommit'],'hostVersion':host['hostVersion'],'platform':host['platform'],'runtimeSha256':sha(binary),'desktopBinarySha256':desktop_lock['binarySha256'],'driverSha256':sha(family.__file__),'runnerPath':'scripts/qa/command_family_guide.py','runnerSha256':sha(__file__),'catalogSha256':sha(catalog_path),'sourceProjectSha256':sha(source),'installedSkillsBefore':before_ids,'installedSkillsAfter':identities(),'cases':cases,'allOwnedProcessesStopped':owned.stopped and owned.session.process.poll() is not None,'listenerOwnedByPID':owned.listener_verified,'registeredCommands':len(registry),'scope':'Explicit family native semantics,owned signed desktop context and actual app-window captures;not creative review or exhaustive V1'}
        write(root/'proof.json',proof);print(json.dumps({'result':'PASS','family':family.FAMILY,'commands':len(cases),'stages':2*len(cases),'ownedStopped':proof['allOwnedProcessesStopped']}),flush=True)
    except BaseException as error:
        write(root/'failure.json',{'result':'FAIL','error':type(error).__name__+': '+str(error),'completedCommands':[x['command'] for x in cases],'allOwnedProcessesStopped':owned.stopped and (owned.session is None or owned.session.process.poll() is not None),'noAutomaticReplay':True});raise
