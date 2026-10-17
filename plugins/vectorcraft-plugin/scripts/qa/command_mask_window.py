#!/usr/bin/env python3
"""拥有的窗口蒙版查看验收；窗口像素与原生编辑状态分别核验。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import socket
import sys
ROOT=Path(__file__).resolve().parents[2]
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def sample_check(samples,on):
    """要求画布内部样本在开启时灰度，关闭时为实际彩色。"""
    if len(samples)!=3 or any(len(p)!=3 for p in samples):raise ValueError('mask_window_samples')
    if on and any(not (p[0]==p[1]==p[2] and 50<p[0]<220) for p in samples):raise ValueError('mask_window_not_greyscale')
    if not on and any(max(p)-min(p)<10 for p in samples):raise ValueError('mask_window_not_colored')
def run(config):
    from PIL import Image
    out=Path(config['output']).resolve();out.mkdir(exist_ok=False);source=Path(config['maskSource']);shutil.copyfile(source,out/'masked.vectorcraft');seed_sha=sha(source)
    host=json.loads(Path(config['host']).read_text());skill=Path(next(x['path'] for x in host['skills'] if x['name']=='vectorcraft-use'))
    def load_path(name,path):
        spec=importlib.util.spec_from_file_location('window_'+name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
    load=lambda n:load_path(n,skill/'scripts'/(n+'.py'));vendor=load_path('vendor',ROOT/'scripts/vendor/skill_vendor.py')
    def ids():
        actual={s['name']:vendor.hash_skill_dir(Path(s['path'])) for s in host['skills']}
        if actual!={s['name']:s['sha256'] for s in host['skills']}:raise ValueError('mask_window_skill_drift')
        return actual
    before_ids=ids();runtime=Path(config['runtime']);binary=runtime/'vectorcraft/0.2.0-craft.2/vectorcraft-cli';lock=json.loads((skill/'scripts/runtime.lock.json').read_text());dl=json.loads((skill/'scripts/desktop.lock.json').read_text())
    if not host['publicTagVerified'] or host['artifactRef']!='v0.1.0-dev.64' or sha(binary)!=lock['artifacts']['darwin-arm64']['binarySha256']:raise ValueError('mask_window_runtime_identity')
    commands=load('commands');desktop=load('desktop').inspect(runtime/'vectorcraft-desktop/0.2.0',dl)
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    owned=load('desktop_session').OwnedSession(commands.backend_argv(str(binary),out,'bridge',f'127.0.0.1:{port}'),desktop,'vectorcraft',out,port);journal=[];stages=[]
    def write(name,value):(out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    def call(name,**params):
        record={'command':name,'params':params,'state':'submitted'};journal.append(record);write('journal.json',journal)
        value=commands.parse_reply(owned.request('tools/call',{'name':'run_command','arguments':{'command':name,'params':params}}));record.update(state='completed',returned=value);write('journal.json',journal);return value
    try:
        with owned:
            call('document.open',path=str(out/'masked.vectorcraft'));original=call('document.json')
            for number,on in ((1,True),(2,False)):
                returned=call('transparency.viewOpacityMask',id=2,on=on);info=call('transparency.info',id=2)
                if returned!={'id':2,'on':on} or info['editingMask']!=2:raise ValueError('mask_window_native_state')
                ui=commands.parse_reply(owned.request('tools/call',{'name':'inspect_ui','arguments':{}}))
                shot=commands.parse_reply(owned.request('tools/call',{'name':'screenshot','arguments':{'window':True,'path':str(out/('window-'+str(number)+'.png'))}}),out,number)
                record=next(c for c in shot['content'] if c['type']=='image');meta=next(c['value'] for c in shot['content'] if c['type']=='text');path=out/record['path']
                if meta.get('window') is not True or sha(path)!=record['sha256']:raise ValueError('mask_window_capture_identity')
                with Image.open(path) as im:
                    im.load()
                    if im.size!=(1440,900):raise ValueError('mask_window_capture_size')
                    rgb=im.convert('RGB');samples=[list(rgb.getpixel(p)) for p in ((250,270),(310,340),(380,410))]
                sample_check(samples,on);stages.append({'on':on,'returned':returned,'info':info,'ui':ui,'window':record,'width':1440,'height':900,'sampleCoordinates':[[250,270],[310,340],[380,410]],'samples':samples})
            call('transparency.stopEditingOpacityMask');final=call('document.json')
            # 进入编辑会给蒙版副本重新编号；其余逻辑艺术内容必须保全。
            a=original['layers'][0]['kind']['children'][0]['mask']['art'];b=final['layers'][0]['kind']['children'][0]['mask']['art']
            if {k:v for k,v in a.items() if k!='id'}!={k:v for k,v in b.items() if k!='id'}:raise ValueError('mask_window_art_loss')
        if sha(source)!=seed_sha or sha(out/'masked.vectorcraft')!=seed_sha:raise ValueError('mask_window_source_changed')
        proof={'schema':'vectorcraft-mask-window/v1','result':'PASS','command':'transparency.viewOpacityMask','pluginVersion':host['pluginVersion'],'pluginCommit':host['pluginCommit'],'sourceRef':host['skillSourceRef'],'sourceCommit':host['skillSourceCommit'],'hostVersion':host['hostVersion'],'platform':host['platform'],'runtimeSha256':sha(binary),'desktopBinarySha256':dl['binarySha256'],'driverSha256':sha(__file__),'sourceProjectSha256':seed_sha,'installedSkillsBefore':before_ids,'installedSkillsAfter':ids(),'stages':stages,'sourcePreserved':True,'maskArtPreserved':True,'listenerOwnedByPID':owned.listener_verified,'allOwnedProcessesStopped':owned.stopped and owned.session.process.poll() is not None,'tasksClosed':[],'scope':'Actual owned desktop window only for viewOpacityMask on/off;not all-command GUI,creative review,other platforms or V1'}
        write('proof.json',proof);print(json.dumps({'result':'PASS','windows':2,'ownedStopped':proof['allOwnedProcessesStopped']}))
    except BaseException as error:
        write('failure.json',{'result':'FAIL','error':type(error).__name__+': '+str(error),'allOwnedProcessesStopped':owned.stopped and (owned.session is None or owned.session.process.poll() is not None),'noAutomaticReplay':True});raise
if __name__=='__main__':run(json.loads(Path(sys.argv[1]).read_text()))
