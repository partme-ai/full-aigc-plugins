#!/usr/bin/env python3
"""使用真实Codex安装及原生app-server验证市场入口，保留逐包RPC。"""
from pathlib import Path
import sys,json,os,subprocess,argparse
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts/ci'))
from craft_windows import NativeHost,wait_connected
NAMES='cadcraft designcraft effectcraft photocraft figcraft filmcraft lightcraft printcraft vectorcraft deckcraft soundcraft gridcraft wordcraft'.split()
def run(market,output,public=False,cli=None,names=None,ref=None):
 cli=cli or ['codex']; names=names or NAMES
 if not public: market=str(Path(market).resolve())
 output.mkdir(parents=True,exist_ok=False);env={**os.environ,'CODEX_HOME':str(output/'home'),'CRAFT_EDITOR_UPDATE':'off'};Path(env['CODEX_HOME']).mkdir()
 result=subprocess.run(cli+['plugin','marketplace','add',str(market)]+(['--ref',ref] if ref else []),env=env,capture_output=True,text=True);(output/'market-add.log').write_text(result.stdout+result.stderr);assert result.returncode==0,result.stderr
 marketname='full-aigc-plugins' if public else 'craft-market-release-acceptance'
 for name in names:
  result=subprocess.run(cli+['plugin','add',name+'@'+marketname,'--json'],env=env,capture_output=True,text=True,timeout=180);(output/(name+'-install.json')).write_text(result.stdout+result.stderr);assert result.returncode==0,(name,result.stderr)
 host=NativeHost(cli,env,output);rows=[]
 try:
  host.call('initialize',{'clientInfo':{'name':'craft-market-install-verifier','version':'1'},'capabilities':{'experimentalApi':True}});host.process.stdin.write('{"method":"initialized"}\n');host.process.stdin.flush()
  work=output/'中文 工作区';work.mkdir();thread=host.call('thread/start',{'cwd':str(work),'approvalPolicy':'never','sandbox':'workspace-write'})['thread']['id']
  for name in names:
   try:
    server=wait_connected(host,thread,name,timeout=150)
    values={}
    for tool,args in [('editor_status',{}),('open_browser_editor',{'workspace':str(work)})]:
     value=host.call('mcpServer/tool/call',{'threadId':thread,'server':name+'-editor','tool':tool,'arguments':args});assert not value.get('isError'),value;values[tool]=value
    row={'plugin':name,'installation':'PASS','nativeMcp':'PASS','editorUrl':values['open_browser_editor']['structuredContent']['editorUrl'],'embeddedUI':'NOT_TESTED','editingSync':'NOT_TESTED'}
   except Exception as error:row={'plugin':name,'status':'FAIL','error':str(error)}
   rows.append(row);(output/'results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(json.dumps(row,ensure_ascii=False),flush=True)
 finally:host.close()
 assert len(rows)==len(names) and all(r.get('nativeMcp')=='PASS' for r in rows)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('market');p.add_argument('output',type=Path);p.add_argument('--public',action='store_true');p.add_argument('--ref');p.add_argument('--codex-js');p.add_argument('--app',choices=NAMES);a=p.parse_args()
 run(a.market,a.output.resolve(),a.public,['node',a.codex_js] if a.codex_js else None,[a.app] if a.app else None,a.ref)
