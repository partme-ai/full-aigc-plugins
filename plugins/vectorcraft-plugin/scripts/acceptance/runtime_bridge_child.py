"""在登记进程组内启动固定签名桌面，验证同会话schema并保持真实bridge供排空验收。"""
import argparse,hashlib,importlib.util,json,socket,sys,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('marker');p.add_argument('skill',type=Path);p.add_argument('binary',type=Path);p.add_argument('desktop',type=Path);p.add_argument('output',type=Path);p.add_argument('requirements',type=Path);p.add_argument('--source',type=Path);a=p.parse_args()
if json.loads(sys.stdin.readline())!={'task':a.marker,'go':True}:raise ValueError('launch_not_authorized')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load(name):
 spec=importlib.util.spec_from_file_location('bridge_acceptance_'+name,a.skill/'scripts'/f'{name}.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
runtime=json.loads((a.skill/'scripts/runtime.lock.json').read_text());expected=runtime['artifacts']['darwin-arm64']['binarySha256']
if sha(a.binary)!=expected:raise ValueError('runtime_identity_mismatch')
desktop_lock=json.loads((a.skill/'scripts/desktop.lock.json').read_text());desktop=load('desktop').inspect(a.desktop,desktop_lock)
requirements=json.loads(a.requirements.read_text());a.output.mkdir()
with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
commands=load('commands');owned=load('desktop_session').OwnedSession(commands.backend_argv(str(a.binary),a.output,'bridge',f'127.0.0.1:{port}'),desktop,'vectorcraft',a.output,port)
with owned:
 rows=commands.runtime_rows(owned,mode='bridge');tools=owned.request('tools/list',{})['tools'];registry={row['id']:row['params'] for row in rows};tool_registry={row['name']:row['inputSchema'] for row in tools}
 for name,signature in requirements['commands'].items():
  if name not in registry or registry[name]!=signature:raise ValueError('live_bridge_command_schema_mismatch: '+name)
 for name,signature in requirements['tools'].items():
  if name not in tool_registry or tool_registry[name]!=signature:raise ValueError('live_bridge_tool_schema_mismatch: '+name)
 def command(name,params):return commands.parse_reply(owned.request('tools/call',{'name':'run_command','arguments':{'command':name,'params':params}}))
 if a.source:command('document.open',{'path':str(a.source)})
 else:
  command('file.new',{'name':'Registered bridge drain','width':48,'height':48,'units':'Points'})
  command('shape.rectangle',{'x':3,'y':3,'width':16,'height':16})
 command('document.save',{'path':str(a.output/'project.vectorcraft')})
 proof={'runtimeIdentity':expected,'desktopBinarySha256':desktop_lock['binarySha256'],'desktopVersion':desktop_lock['version'],'listenerOwnedByPID':owned.listener_verified,'desktopPID':owned.process.pid,'projectSha256':sha(a.output/'project.vectorcraft'),'commandCount':len(rows),'toolCount':len(tools),'requirementsSha256':sha(a.requirements)}
 (a.output/'ready.json').write_text(json.dumps(proof))
 until=time.monotonic()+30
 while not (a.output/'release.json').exists():
  if time.monotonic()>=until:raise TimeoutError('bridge_hold_expired; no replay')
  time.sleep(.025)
 command('document.open',{'path':str(a.output/'project.vectorcraft')});command('document.inspect',{})
proof.update({'reopened':True,'ownedProcessesStopped':owned.stopped})
if sha(a.binary)!=expected:raise ValueError('runtime_identity_changed')
print(json.dumps(proof))
