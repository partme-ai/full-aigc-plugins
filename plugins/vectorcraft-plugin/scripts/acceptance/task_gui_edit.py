"""通过本用例拥有的签名桌面bridge修改源工程；不接管用户已有桌面进程。"""
import argparse,hashlib,importlib.util,json,socket
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('skill',type=Path);p.add_argument('binary',type=Path);p.add_argument('desktop',type=Path);p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load(name):
 s=importlib.util.spec_from_file_location('task_gui_'+name,a.skill/'scripts'/f'{name}.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
runtime=json.loads((a.skill/'scripts/runtime.lock.json').read_text());expected=runtime['artifacts']['darwin-arm64']['binarySha256'];assert sha(a.binary)==expected
desktop_lock=json.loads((a.skill/'scripts/desktop.lock.json').read_text());desktop=load('desktop').inspect(a.desktop,desktop_lock);a.output.mkdir()
with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
commands=load('commands');owned=load('desktop_session').OwnedSession(commands.backend_argv(str(a.binary),a.output,'bridge',f'127.0.0.1:{port}'),desktop,'vectorcraft',a.output,port)
before=sha(a.source)
with owned:
 def command(name,params):return commands.parse_reply(owned.request('tools/call',{'name':'run_command','arguments':{'command':name,'params':params}}))
 command('document.open',{'path':str(a.source)});original=command('document.json',{})
 command('swatch.edit',{'name':'Brand Primary','color':'#663399'});modified=command('document.json',{});assert original!=modified
 command('document.save',{'path':str(a.source)});after=sha(a.source);assert before!=after
 command('document.open',{'path':str(a.source)});reopened=command('document.json',{})
 (a.output/'snapshots.json').write_text(json.dumps({'original':original,'modified':modified,'reopened':reopened},indent=2))
 # 原生保存会推进文档修改时间；其余持久语义必须逐字保持。
 saved_timestamp=reopened['metadata']['modified'];assert isinstance(saved_timestamp,int) and saved_timestamp>=modified['metadata']['modified']
 assert reopened=={**modified,'metadata':{**modified['metadata'],'modified':saved_timestamp}}
proof={'result':'PASS','actor':'owned signed desktop bridge; real GUI document mutation and save, not manual human interaction','runtimeIdentity':expected,'desktopBinarySha256':desktop_lock['binarySha256'],'desktopVersion':desktop_lock['version'],'listenerOwnedByPID':owned.listener_verified,'desktopPID':owned.process.pid,'sourceBeforeSha256':before,'sourceAfterSha256':after,'nativeDocumentChanged':True,'nativeReopened':True,'persistedContentMatches':True,'nativeSaveTimestamp':{'before':modified['metadata']['modified'],'after':saved_timestamp},'snapshotsSha256':sha(a.output/'snapshots.json'),'ownedProcessesStopped':owned.stopped}
(a.output/'proof.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof))
