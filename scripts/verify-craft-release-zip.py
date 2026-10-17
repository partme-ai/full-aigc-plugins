#!/usr/bin/env python3
"""从公开Release下载完整ZIP，校验、解包，再通过真实Codex安装与调用。"""
from pathlib import Path
import argparse,json,sys,importlib.util,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts/ci'))
from craft_windows import download,extract_package
spec=importlib.util.spec_from_file_location('craft_market_install',ROOT/'scripts/verify-craft-market-install.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
def checked_tag_commit(text,version,expected):
 refs={parts[1]:parts[0] for line in text.splitlines() if len(parts:=line.split())==2}
 tag='refs/tags/v'+version
 actual=refs.get(tag+'^{}',refs.get(tag))
 if actual is None:raise ValueError('Release tag is absent: '+tag)
 if actual!=expected:raise ValueError('Release tag commit differs: expected '+expected+', actual '+actual)
 return actual

def verify_tag(row):
 url='https://github.com/full-aigc-plugins/'+row['plugin']+'-plugin.git';tag='refs/tags/v'+row['version']
 text=subprocess.check_output(['git','-c','http.version=HTTP/1.1','ls-remote',url,tag,tag+'^{}'],text=True,encoding='utf-8',timeout=90)
 return checked_tag_commit(text,row['version'],row['commit'])

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--app',default='all');p.add_argument('--output',type=Path,required=True);p.add_argument('--codex-js');a=p.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False);rows=json.loads((ROOT/'docs/craft-marketplace-candidate-releases.json').read_text());reports=[]
 if a.app!='all':rows=[r for r in rows if r['plugin']==a.app];assert len(rows)==1
 for r in rows:
  remote_commit=verify_tag(r)
  name=r['plugin'];folder=out/name;folder.mkdir();archive=folder/r['archive'];url=r['releaseUrl'].replace('/tag/','/download/')+'/'+r['archive'];download(url,archive,r['archiveSha256']);market=folder/'market';package=extract_package(archive,market/'plugins',name)
  manifest=market/'.agents/plugins/marketplace.json';manifest.parent.mkdir(parents=True);marketname='craft-release-zip-'+name;manifest.write_text(json.dumps({'name':marketname,'plugins':[{'name':name,'source':{'source':'local','path':'./plugins/'+name+'-plugin'},'policy':{'installation':'AVAILABLE','authentication':'ON_USE'},'category':'Creativity'}]}))
  module.run(str(market),folder/'native-host',False,['node',a.codex_js] if a.codex_js else None,[name],None,marketname)
  receipt=json.loads((folder/'native-host'/(name+'-install.json')).read_text());installed=Path(receipt['installedPath']);lock=json.loads((installed/'ui/runtime.lock.json').read_text())
  for file,digest in lock['files'].items():assert hashlib.sha256((installed/'ui/dist'/file).read_bytes()).hexdigest()==digest,'Installed ZIP runtime missing/corrupt: '+file
  report={'plugin':name,'version':r['version'],'source':url,'archiveSha256':r['archiveSha256'],'remoteTagCommit':remote_commit,'downloadedArchive':'PASS','cleanExtraction':'PASS','nativeCodexInstallAndMcp':'PASS','installedBundledRuntimeDigests':'PASS','embeddedUI':'NOT_TESTED','editingSync':'NOT_TESTED'};reports.append(report);(out/'results.json').write_text(json.dumps(reports,indent=2));print(json.dumps(report),flush=True)
