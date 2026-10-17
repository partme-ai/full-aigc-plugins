"""Runtime边界验收的真实MCP子进程；先等待父账本放行，按需保持会话以检验排空。"""
import argparse,hashlib,importlib.util,json,sys,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('marker');p.add_argument('skill',type=Path);p.add_argument('binary',type=Path);p.add_argument('output',type=Path);p.add_argument('--source',type=Path);p.add_argument('--hold',action='store_true');a=p.parse_args()
if json.loads(sys.stdin.readline())!={'task':a.marker,'go':True}:raise SystemExit('launch_not_authorized')
lock=json.loads((a.skill/'scripts/runtime.lock.json').read_text());expected=lock['artifacts']['darwin-arm64']['binarySha256']
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
if sha(a.binary)!=expected:raise ValueError('runtime_identity_mismatch')
a.output.mkdir()
spec=importlib.util.spec_from_file_location('runtime_boundary_session',a.skill/'scripts/mcp_session.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
with module.Session([str(a.binary),'mcp','--headless'],timeout=10) as session:
    if a.source:session.command('document.open',{'path':str(a.source)})
    else:
        session.command('file.new',{'name':'Runtime boundary','width':48,'height':48,'units':'Points'})
        session.command('shape.rectangle',{'x':3,'y':3,'width':16,'height':16})
    session.command('document.save',{'path':str(a.output/'project.vectorcraft')})
    proof={'runtimeIdentity':expected,'projectSha256':sha(a.output/'project.vectorcraft'),'nativeFormat':json.loads((a.output/'project.vectorcraft').read_text())['version']}
    (a.output/'ready.json').write_text(json.dumps(proof))
    if a.hold:
        until=time.monotonic()+20
        while not (a.output/'release.json').exists():
            if time.monotonic()>=until:raise TimeoutError('boundary_hold_expired; no replay')
            time.sleep(.025)
    session.command('document.open',{'path':str(a.output/'project.vectorcraft')})
    session.command('document.inspect',{})
if sha(a.binary)!=expected:raise ValueError('runtime_identity_changed')
proof['reopened']=True
print(json.dumps(proof))
