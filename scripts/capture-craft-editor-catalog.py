#!/usr/bin/env python3
"""提取固定制品的MCP描述符供轻量握手使用；不作为真实宿主验收。"""
from pathlib import Path
import json,subprocess,threading,queue,argparse
ROOT=Path(__file__).resolve().parents[1]
def capture(runtime):
 process=subprocess.Popen(['node',str(runtime/'adapter.mjs')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True);messages=queue.Queue()
 def reader():
  for line in process.stdout:
   try:messages.put(json.loads(line))
   except json.JSONDecodeError:pass
 threading.Thread(target=reader,daemon=True).start();seq=0
 def call(method,params={}):
  nonlocal seq;seq+=1;process.stdin.write(json.dumps({'jsonrpc':'2.0','id':seq,'method':method,'params':params})+'\n');process.stdin.flush()
  while True:
   r=messages.get(timeout=20)
   if r.get('id')==seq:return r
 try:
  r=call('initialize',{'protocolVersion':'2025-03-26','capabilities':{},'clientInfo':{'name':'catalog-packager','version':'1'}});assert 'result' in r,r
  process.stdin.write('{"jsonrpc":"2.0","method":"notifications/initialized"}\n');process.stdin.flush()
  tools=call('tools/list')['result']['tools'];resources=call('resources/list')['result']['resources'];templates=call('resources/templates/list').get('result',{}).get('resourceTemplates',[])
  return {'tools':tools,'resources':resources,'resourceTemplates':templates}
 finally:
  process.terminate()
  try:process.wait(timeout=5)
  except subprocess.TimeoutExpired:process.kill();process.wait()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('runtime_map',type=Path);a=p.parse_args()
 for name,directory in json.loads(a.runtime_map.read_text()).items():
  value=capture(Path(directory));dest=ROOT.parent/'full-aigc-plugins-repositories'/(name+'-plugin')/'ui/catalog.lock.json';dest.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');print(name,len(value['tools']),flush=True)
