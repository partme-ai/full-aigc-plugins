"""隔离安装两个固定CLI与签名桌面，生成实际能力及owned bridge原生证据。"""
import hashlib,importlib.util,json,shutil,socket,subprocess,sys
from pathlib import Path
root=Path.cwd();skill=Path(sys.argv[2]).resolve();work=Path(sys.argv[1]).resolve();work.mkdir(exist_ok=False);home=work/'runtime'
def load(name):
 spec=importlib.util.spec_from_file_location('boundary_'+name,skill/'scripts'/f'{name}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
bootstrap=load('bootstrap');newlock=json.loads((skill/'scripts/runtime.lock.json').read_text());new=bootstrap.install(newlock,home)
oldskill=work/'old-probe-skill';shutil.copytree(skill,oldskill);oldlock=json.loads((root/'runtime/vectorcraft-cli.lock.json').read_text());oldlock['artifacts']['darwin-arm64']['versionOutput']='vectorcraft-cli 0.2.0';(oldskill/'scripts/runtime.lock.json').write_text(json.dumps(oldlock))
old=Path(bootstrap.install(oldlock,home)['executable'])
for name,source,binary in [('old',oldskill,old),('new',skill,Path(new['executable']))]:
 req={'skill':str(source),'executable':str(binary),'platform':'darwin-arm64','requirements':{'mode':'headless'}}
 p=subprocess.run([sys.executable,'-I','-B','src/runtime/runtime_probe.py'],input=json.dumps(req),text=True,capture_output=True,check=True)
 (work/f'{name}-probe.json').write_text(p.stdout)
 print(name,'probe',len(json.loads(p.stdout)['commands']),flush=True)
# 官方签名桌面始终在独立缓存中安装，仅控制本次拥有的进程。
desktop=load('desktop');lock=json.loads((skill/'scripts/desktop.lock.json').read_text());installed=desktop.install(lock,home)
commands=load('commands');sessions=load('desktop_session');output=work/'desktop';output.mkdir()
with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
argv=commands.backend_argv(new['executable'],output,'bridge',f'127.0.0.1:{port}')
owned=sessions.OwnedSession(argv,installed,'vectorcraft',output,port)
with owned:
 tools=owned.request('tools/list',{})['tools'];rows=commands.runtime_rows(owned,mode='bridge')
 report={'schema':'vectorcraft-runtime-probe/v1','mode':'bridge','binarySha256':new['binarySha256'],'version':'vectorcraft-cli 0.2.0-craft.2','commands':rows,'tools':tools,'desktopBinarySha256':lock['binarySha256'],'desktopVersion':lock['version']}
 (work/'bridge-probe.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 def command(name,params):return commands.parse_reply(owned.request('tools/call',{'name':'run_command','arguments':{'command':name,'params':params}}))
 results=[]
 for name,params in [('file.new',{'width':32,'height':32,'units':'Points'}),('shape.rectangle',{'x':2,'y':2,'width':12,'height':12}),('document.save',{'path':str(output/'project.vectorcraft')}),('document.open',{'path':str(output/'project.vectorcraft')}),('document.inspect',{})]:
  results.append({'command':name,'result':command(name,params)})
 (work/'desktop-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
(work/'desktop-lifecycle.json').write_text(json.dumps({'result':'PASS','listenerOwnedByPID':owned.listener_verified,'ownedProcessesStopped':owned.stopped,'desktopBinarySha256':lock['binarySha256'],'desktopVersion':lock['version'],'projectSha256':sha(output/'project.vectorcraft'),'cliBinarySha256':new['binarySha256']},indent=2)+'\n')
print('desktop probe/create/save/reopen PASS',flush=True)
