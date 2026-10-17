#!/usr/bin/env python3
"""原生文字导出模式与三个公开定位入口；候选／固定副本由配置身份区分。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
config=json.loads(Path(sys.argv[1]).read_text());root=Path(config['output']).resolve();root.mkdir();skill=Path(config['skill']).resolve();runtime=Path(config['runtime']).resolve()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def tree(folder):return {p.relative_to(folder).as_posix():sha(p) for p in sorted(folder.rglob('*')) if p.is_file()}
def module(name):
 spec=importlib.util.spec_from_file_location('outline_qa_'+name,skill/'scripts'/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
identity=tree(skill);workflow=module('workflow');commands=module('commands');Session=module('mcp_session').Session;lock=json.loads((skill/'scripts/runtime.lock.json').read_text());binary=runtime/'vectorcraft'/lock['resolvedVersion']/'vectorcraft-cli';cases=[]
for mode in ['editable','appearance']:
 plan=json.loads((skill/'examples/chinese-text.json').read_text());plan['operations'].append({'command':'native.command','params':{'command':'document.setup','params':{'exportText':mode}}});output=root/mode;manifest=workflow.execute(plan,output,runtime_home=runtime)
 assert sha(binary)==lock['artifacts']['darwin-arm64']['binarySha256'];loss=json.loads((output/'exchange-loss.json').read_text());record=next(x for x in loss['outputs'] if x['format']=='svg');changes={x['code']:x['status'] for x in record['changes']};expected='lost' if mode=='appearance' else 'observed';assert record['observations']['svgTextExportMode']==mode,record;assert changes['live-text-editability']==expected;assert changes['font-portability']=='unknown';assert record['sha256']==sha(output/record['location']);assert loss['native']['sha256']==sha(output/'project.vectorcraft')
 tags=[e.tag.split('}')[-1] for e in ET.fromstring((output/record['location']).read_bytes()).iter()];assert tags.count('text')==0 if mode=='appearance' else tags.count('text')>=2;assert tags.count('path')>0 if mode=='appearance' else True
 before=tree(output)
 with Session([str(binary),'mcp','--headless']) as session:
  session.command('document.open',{'path':str(output/'project.vectorcraft')});native=session.command('document.json',{});fonts=session.command('text.fonts',{});assert '新品上市' in json.dumps(native,ensure_ascii=False);assert 'SAFE' in json.dumps(native);assert fonts and all(not f['missing'] for f in fonts)
 assert session.process.returncode is not None and tree(output)==before
 assert all(not f['missing'] for f in manifest['fontDependencies']);assert record['observations']['nativeTextObjectIds']==sorted([manifest['bindings']['headline']['id'],manifest['bindings']['footer']['id']])
 cases.append({'name':mode,'result':'PASS','lossStatus':expected,'reportedMode':record['observations']['svgTextExportMode'],'svgTextCount':tags.count('text'),'svgPathCount':tags.count('path'),'nativeTextIds':record['observations']['nativeTextObjectIds'],'fontDependencies':manifest['fontDependencies'],'nativeIndependentlyReopened':True,'nativeLiveTextPreserved':True,'fontPortability':'unknown','files':manifest['files'],'lossNativeSha256':loss['native']['sha256'],'lossSvgSha256':record['sha256'],'reopenDidNotModifyDelivery':True,'reopenSessionExited':True})
invalid=[{'text':'新标题'},{'id':True,'text':'新标题'},{'ids':[],'text':'新标题'},{'id':1,'text':'新标题','font':'Other'},{'id':1,'text':42},{'id':1,'ids':[2],'text':'新标题'}];refused=[]
for route in ['direct','gateway','complete']:
 for i,params in enumerate(invalid):
  output=root/(route+'-invalid-'+str(i));fresh=root/(route+'-fresh-runtime-'+str(i));operation={'command':'text.setText','params':params}
  plan={'operations':[{'command':'native.command','params':operation}] if route=='gateway' else [operation]}
  if route=='complete':plan={'schema':'craft-command-plan/v1','operations':[operation]}
  try:
   if route=='complete':commands.execute(plan,output,runtime_home=fresh)
   else:workflow.execute(plan,output,runtime_home=fresh)
  except ValueError as error:assert 'invalid_text_edit' in str(error)
  else:raise AssertionError('invalid text mutation admitted')
  assert not output.exists() and not fresh.exists();refused.append({'route':route,'case':i,'result':'PASS','outputAbsent':True,'runtimeAbsent':True})
assert identity==tree(skill)
proof={'schema':'vectorcraft-text-outline-native/v1','result':'PASS','level':config['level'],'runtimeIdentity':sha(binary),'driverSha256':sha(__file__),'skillFiles':identity,'cases':cases,'preflightRefusals':refused,'skillUnchanged':True,'scope':'two actual native text export modes with independent reopening, retained original live text/font dependencies and18 pre-install explicit-target refusals; no font substitution or per-object visible outline mapping'}
(root/'proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'result':'PASS','nativeCases':2,'preflightRefusals':18}))
