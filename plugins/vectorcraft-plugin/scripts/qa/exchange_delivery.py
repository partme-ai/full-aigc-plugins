#!/usr/bin/env python3
"""原生工程与交换损失：独立重开、可编辑原源及双重重签后的语义拒绝。"""
import hashlib,importlib.util,json,shutil,sys
from pathlib import Path
c=json.loads(Path(sys.argv[1]).read_text());root=Path(c['output']).resolve();root.mkdir(parents=True,exist_ok=False)
skill=Path(c['skill']);runtime=Path(c['runtime']);binary=runtime/'vectorcraft/0.2.0-craft.2/vectorcraft-cli'
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def tree(path):return {p.relative_to(path).as_posix():sha(p) for p in sorted(path.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
w=load('exchange_delivery_workflow',skill/'scripts/workflow.py');loss=load('exchange_delivery_loss',skill/'scripts/exchange_loss.py');sessions=load('exchange_delivery_sessions',skill/'scripts/mcp_session.py');quality=load('exchange_delivery_quality',Path(c['quality']))
identity=tree(skill)
plan={'document':{'name':'Editable original and derivative losses','width':128,'height':96,'units':'Pixels'},'operations':[
 {'command':'native.command','params':{'command':'document.setup','params':{'exportText':'appearance'}}},
 {'command':'shape.rectangle','params':{'x':12,'y':12,'width':60,'height':36},'as':'gradient'},
 {'command':'native.command','params':{'command':'paint.setFill','params':{'gradient':{'kind':'freeform','stops':[{'offset':0,'color':'#ef5b36'},{'offset':1,'color':'#2366e8'}]}}}},
 {'command':'paint.setStroke','params':{'none':True}},
 {'command':'text.create','params':{'x':12,'y':72,'text':'Editable source','font':'Source Sans 3','size':12,'color':'#223344'},'as':'title'}],'exports':[]}
source=root/'source';first=w.execute(plan,source,runtime_home=runtime);source_files=tree(source)
export_plan={'expectedProjectSha256':first['files']['project.vectorcraft'],'operations':[],'exports':[{'format':fmt,'artboard':0} for fmt in ['svg','pdf','png']]}
out=root/'exported';manifest=w.execute(export_plan,out,source=source,runtime_home=runtime);out_files=tree(out);report=json.loads((out/'exchange-loss.json').read_text())
q=quality.check_delivery(out,manifest['runtimeSha256'],manifest['files']['project.vectorcraft']);assert q['technicalStatus']=='PASS',q
models=[]
for path in [source,out]:
 with sessions.Session([str(binary),'mcp','--headless']) as native:
  native.command('document.open',{'path':str(path/'project.vectorcraft')});model=native.command('document.json',{})
  native.command('select.set',{'ids':[first['bindings']['gradient']['id']]});points=native.command('paint.freeform.get',{})
 assert model==json.loads((path/'native.json').read_text());models.append({'model':model,'points':points})
assert models[0]['model']['layers']==models[1]['model']['layers'] and models[0]['points']==models[1]['points']
assert models[0]['model']['artboards']==models[1]['model']['artboards']
svg=next(r for r in report['outputs'] if r['format']=='svg');assert svg['observations']['svg']['image']==1
assert svg['observations']['nativeTextObjectIds'] and svg['observations']['svgTextExportMode']=='appearance'
assert next(x['status'] for x in svg['changes'] if x['code']=='live-text-editability')=='lost'
assert 'freeform gradients are written as images clipped to their shapes' in svg['warnings']
# 同一文件名下重签交换报告、清单及血缘；避免由旧血缘摘要提前挡住真正的语义缺口。
def fault_package(name,fmt=None):
 target=root/name;shutil.copytree(out,target);m=json.loads((target/'manifest.json').read_text());r=json.loads((target/'exchange-loss.json').read_text())
 row=next(x for x in r['outputs'] if x['format']==fmt) if fmt else r['outputs'][0]
 if name.startswith('native-substitute-'):row['nativeSubstitute']=True
 elif name=='wrong-native':r['native']['sha256']='0'*64
 elif name=='wrong-inspection':r['inspection']['sha256']='0'*64
 elif name=='wrong-export':row['sha256']='0'*64
 elif name=='false-font-fidelity':next(x for x in row['changes'] if x['code']=='font-portability')['status']='observed'
 elif name=='false-effect-fidelity':next(x for x in row['changes'] if x['code']=='effect-fidelity')['status']='observed'
 elif name=='missing-output':r['outputs'].pop()
 elif name=='duplicate-output':r['outputs'].append(dict(row))
 elif name=='false-approval':r['acceptance']='approved'
 elif name=='false-text-editability':next(x for x in row['changes'] if x['code']=='live-text-editability')['status']='observed'
 elif name=='wrong-text-mode':row['observations']['svgTextExportMode']='editable'
 elif name=='missing-report':(target/'exchange-loss.json').unlink();m['files'].pop('exchange-loss.json');m.pop('lossReport')
 elif name=='invalid-report-json':(target/'exchange-loss.json').write_text('{')
 elif name=='invalid-inspection':(target/'native.json').write_text('[]')
 elif name=='corrupt-png':(target/'artboard-1.png').write_bytes(b'\x89PNG\r\n\x1a\ncorrupt')
 elif name=='corrupt-pdf':(target/'artboard-1.pdf').write_bytes(b'%PDF-1.7\ncorrupt')
 elif name=='corrupt-svg':(target/'artboard-1.svg').write_text('<svg><broken>')
 if name not in ['missing-report','invalid-report-json','invalid-inspection','corrupt-png','corrupt-pdf','corrupt-svg']:(target/'exchange-loss.json').write_text(json.dumps(r))
 if name in ['corrupt-png','corrupt-pdf','corrupt-svg']:
  for entry in r['outputs']:entry['sha256']=sha(target/entry['location'])
  (target/'exchange-loss.json').write_text(json.dumps(r))
 for filename in m['files']:
  if filename!='lineage.json':m['files'][filename]=sha(target/filename)
 if 'lossReport' in m:m['lossReport']['sha256']=m['files']['exchange-loss.json']
 m['files'].pop('lineage.json');loss.write_lineage(target,m,'explicit-qa-rebind-'+name)
 (target/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
 checked=quality.check_delivery(target,m['runtimeSha256'],m['files']['project.vectorcraft'])
 return checked
if c.get('baseline'):
 refused=fault_package('native-substitute-pdf','pdf')
 assert refused['artifactIntegrityStatus']=='PASS' and refused['technicalStatus']=='PASS'
 proof={'schema':'vectorcraft-exchange-delivery-baseline/v1','result':'FAIL','expectedGapConfirmed':True,'wrongSubstituteAccepted':True,'quality':refused,'skillFiles':identity,'runtimeSha256':sha(binary),'qualitySha256':sha(c['quality']),'driverSha256':sha(__file__),'originalSourcePreserved':tree(source)==source_files}
else:
 assert q['exchangeStatus']=='PASS' and q['lineageStatus']=='PASS'
 refused=[]
 cases=[('native-substitute-'+fmt,fmt) for fmt in ['svg','pdf','png']]+[(n,'pdf' if 'fidelity' in n else None) for n in ['wrong-native','wrong-inspection','wrong-export','false-font-fidelity','false-effect-fidelity','missing-output','duplicate-output','false-approval','false-text-editability','wrong-text-mode','missing-report','invalid-report-json','invalid-inspection','corrupt-png','corrupt-pdf','corrupt-svg']]
 for name,fmt in cases:
  checked=fault_package(name,fmt);assert checked['artifactIntegrityStatus']=='PASS' and checked['technicalStatus']=='FAIL' and checked['acceptanceStatus']=='blocked',checked
  refused.append({'case':name,'result':'PASS','freshManifestAndLineageHashes':True,'quality':checked})
 edited=root/'edited';revised=w.execute({'expectedProjectSha256':first['files']['project.vectorcraft'],'operations':[
  {'command':'select.set','params':{'ids':[first['bindings']['gradient']['id']]}},
  {'command':'native.command','params':{'command':'paint.freeform.setPoint','params':{'index':0,'color':'#22aa66'}}},
  {'command':'text.setText','params':{'ids':[first['bindings']['title']['id']],'text':'Still editable'}}],'exports':[]},edited,source=source,runtime_home=runtime)
 with sessions.Session([str(binary),'mcp','--headless']) as native:
  native.command('document.open',{'path':str(edited/'project.vectorcraft')});edited_model=native.command('document.json',{})
  native.command('select.set',{'ids':[first['bindings']['gradient']['id']]});edited_points=native.command('paint.freeform.get',{})
 assert edited_model==json.loads((edited/'native.json').read_text());assert edited_points['points'][0]['color']!=models[0]['points']['points'][0]['color'] and edited_points['points'][1:]==models[0]['points']['points'][1:]
 assert 'Still editable' in json.dumps(edited_model)
 bad=root/'corrupt-native';bad.mkdir();(bad/'project.vectorcraft').write_bytes(b'corrupt native fixture')
 with sessions.Session([str(binary),'mcp','--headless']) as native:
  try:native.command('document.open',{'path':str(bad/'project.vectorcraft')})
  except RuntimeError as error:
   reason=str(error).replace(str(root),'QA_ROOT');assert 'outcome_unknown' not in reason
  else:raise AssertionError('corrupt native accepted')
 refused.append({'case':'corrupt-native','result':'PASS','knownNativeRefusal':reason})
 assert tree(source)==source_files and tree(out)==out_files and tree(skill)==identity
 proof={'schema':'vectorcraft-exchange-delivery-native/v1','result':'PASS','level':c['level'],'platform':'Darwin-arm64','runtimeSha256':sha(binary),'qualitySha256':sha(c['quality']),'driverSha256':sha(__file__),'skillFiles':identity,'plan':plan,'exportPlan':export_plan,'sourceFiles':source_files,'exportedFiles':out_files,'manifest':manifest,'lossReport':report,'quality':q,'independentReopens':models,'editedNativeModel':edited_model,'editedPoints':edited_points,'editedManifest':revised,'nativeTextAndGradientEditable':True,'sourceAndPreviousExportsPreserved':True,'installedSkillPreserved':True,'refusals':refused,'scope':'actual native project preservation, live text/freeform edit, SVG/PDF/PNG loss semantics and decode; no creative,GUI,other platform,external editor or universal fidelity claim'}
(root/'proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'result':proof['result'],'expectedGapConfirmed':proof.get('expectedGapConfirmed'),'refusals':len(proof.get('refusals',[]))}))
