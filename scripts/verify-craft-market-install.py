#!/usr/bin/env python3
"""使用真实Codex安装及原生app-server验证市场入口，保留逐包RPC。"""
from pathlib import Path
import sys,json,os,subprocess,argparse
from urllib.request import urlopen
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts/ci'))
from craft_windows import NativeHost,wait_connected
NAMES='cadcraft designcraft effectcraft photocraft figcraft filmcraft lightcraft printcraft vectorcraft deckcraft soundcraft gridcraft wordcraft'.split()
def run(market,output,public=False,cli=None,names=None,ref=None,marketplace_name=None):
 cli=cli or ['codex']; names=names or NAMES
 if not public: market=str(Path(market).resolve())
 output.mkdir(parents=True,exist_ok=False);env={**os.environ,'CODEX_HOME':str(output/'home'),'CRAFT_EDITOR_UPDATE':'off'};Path(env['CODEX_HOME']).mkdir()
 result=subprocess.run(cli+['plugin','marketplace','add',str(market)]+(['--ref',ref] if ref else []),env=env,capture_output=True,text=True);(output/'market-add.log').write_text(result.stdout+result.stderr);assert result.returncode==0,result.stderr
 marketname=marketplace_name or ('full-aigc-plugins' if public else 'craft-market-release-acceptance')
 listing_dir=output/'listing-before-install';listing_dir.mkdir()
 listing_host=NativeHost(cli,env,listing_dir)
 try:
  listing_host.call('initialize',{'clientInfo':{'name':'craft-icon-listing','version':'1'},'capabilities':{'experimentalApi':True}});listing_host.process.stdin.write('{"method":"initialized"}\n');listing_host.process.stdin.flush()
  listing=listing_host.call('plugin/list',{'marketplaceKinds':['local'],'forceRefetch':False})
  entries=[p for m in listing['marketplaces'] if m['name']==marketname for p in m['plugins']]
  for name in names:
   plugin=next(p for p in entries if p['name']==name)
   assert not plugin['installed'], 'Listing verification must precede install'
   for field in ['logo','composerIcon']:
    value=plugin['interface'].get(field);assert value and Path(value).is_file(), name+' missing native pre-install '+field
  (output/'icons-before-install.json').write_text(json.dumps({'plugins':names,'status':'PASS','scope':'real native plugin/list before installation'},indent=2))
 finally:listing_host.close()
 for name in names:
  result=subprocess.run(cli+['plugin','add',name+'@'+marketname,'--json'],env=env,capture_output=True,text=True,timeout=180);(output/(name+'-install.json')).write_text(result.stdout+result.stderr);assert result.returncode==0,(name,result.stderr)
 host=NativeHost(cli,env,output);rows=[]
 try:
  host.call('initialize',{'clientInfo':{'name':'craft-market-install-verifier','version':'1'},'capabilities':{'experimentalApi':True}});host.process.stdin.write('{"method":"initialized"}\n');host.process.stdin.flush()
  work=output/'中文 工作区';work.mkdir()
  discovered=host.call('skills/list',{'cwds':[str(work)],'forceReload':True})
  skills=[skill for entry in discovered['data'] for skill in entry['skills']]
  for name in names:
   installed=json.loads((output/(name+'-install.json')).read_text())['installedPath'];expected=list((Path(installed)/'skills').glob('*/SKILL.md'));actual={str(Path(s['path']).resolve()) for s in skills if s.get('enabled')}
   assert expected, 'Installed plugin has no skills: '+name
   missing=[str(p) for p in expected if str(p.resolve()) not in actual]
   assert not missing, 'Installed skills were not discovered: '+str(missing)
  (output/'skills-discovery.json').write_text(json.dumps({'scope':'real Codex skills/list; installed plugin paths only','plugins':names,'count':sum(len(list((Path(json.loads((output/(name+'-install.json')).read_text())['installedPath'])/'skills').glob('*/SKILL.md'))) for name in names),'status':'PASS'},indent=2))
  thread=host.call('thread/start',{'cwd':str(work),'approvalPolicy':'never','sandbox':'workspace-write'})['thread']['id']
  for name in names:wait_connected(host,thread,name,timeout=150)
  for name in names:
   try:
    server=wait_connected(host,thread,name,timeout=150)
    expected_version=json.loads((output/(name+'-install.json')).read_text())['version']
    assert server['serverInfo']['version']==expected_version, 'MCP/plugin version mismatch'
    values={}
    for tool,args in [('editor_status',{}),('open_browser_editor',{'workspace':str(work)})]:
     value=host.call('mcpServer/tool/call',{'threadId':thread,'server':name+'-editor','tool':tool,'arguments':args});assert not value.get('isError'),value;values[tool]=value
    assert Path(values['open_browser_editor']['structuredContent']['workspace']).resolve()==work.resolve(), 'Wrong editor workspace'
    url=values['open_browser_editor']['structuredContent']['editorUrl']
    with urlopen(url,timeout=30) as response:
     assert response.status==200 and 'html' in response.headers.get('Content-Type',''), 'Editor HTML unavailable'
    row={'editorHtml':'PASS','plugin':name,'installation':'PASS','nativeMcp':'PASS','editorUrl':values['open_browser_editor']['structuredContent']['editorUrl'],'embeddedUI':'NOT_TESTED','editingSync':'NOT_TESTED'}
   except Exception as error:row={'plugin':name,'status':'FAIL','error':str(error)[:600]}
   rows.append(row);(output/'results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(json.dumps(row,ensure_ascii=False),flush=True)
 finally:host.close()
 assert len(rows)==len(names) and all(r.get('nativeMcp')=='PASS' for r in rows)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('market');p.add_argument('output',type=Path);p.add_argument('--public',action='store_true');p.add_argument('--ref');p.add_argument('--codex-js');p.add_argument('--marketplace-name');p.add_argument('--app',choices=NAMES);a=p.parse_args()
 run(a.market,a.output.resolve(),a.public,['node',a.codex_js] if a.codex_js else None,[a.app] if a.app else None,a.ref,a.marketplace_name)
