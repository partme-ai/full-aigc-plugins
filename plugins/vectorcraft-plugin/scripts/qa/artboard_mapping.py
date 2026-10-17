#!/usr/bin/env python3
"""外部QA：真实画板重排、稳定ID导出、全部映射预检与旧索引偏移拒绝。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

c=json.loads(Path(sys.argv[1]).read_text());root=Path(c['output']).resolve();root.mkdir(exist_ok=False);skill=Path(c['skill']).resolve();runtime=Path(c['runtime']).resolve()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def hashes(d):return {p.relative_to(d).as_posix():sha(p) for p in sorted(d.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
spec=importlib.util.spec_from_file_location('artboard_native_qa',skill/'scripts/workflow.py');w=importlib.util.module_from_spec(spec);spec.loader.exec_module(w);identity=hashes(skill)
boards=[(0,0,64,48,'Logo','#2366e8'),(120,20,32,24,'Icon','#22aa66'),(240,-20,28,36,'Portrait','#bb3300')]
ops=[{'command':'artboard.setProps','params':{'index':0,'name':'Logo'}}]
for i,(x,y,width,height,name,color) in enumerate(boards):
 if i:ops.append({'command':'artboard.new','params':{'x':x,'y':y,'width':width,'height':height,'name':name},'as':'variant'+str(i)})
 ops.extend([{'command':'shape.rectangle','params':{'x':x+width/4,'y':y+height/4,'width':width/2,'height':height/2}},{'command':'paint.setFill','params':{'color':color}},{'command':'paint.setStroke','params':{'none':True}}])
plan={'document':{'name':'Stable artboards','width':64,'height':48,'units':'Pixels'},'operations':ops,'exports':[{'format':fmt,'artboard':i} for i in range(3) for fmt in ['svg','png','pdf']]}
if c.get('expectEnforced',True):plan['exports'][4]['artboardId']={'$ref':'variant1.id'}
source=root/'source';first=w.execute(plan,source,runtime_home=runtime);native=json.loads((source/'native.json').read_text());ids=[b['id'] for b in native['artboards']];before=hashes(source);reorder={'command':'native.command','params':{'command':'artboard.reorder','params':{'index':0,'to':2}}}
def revision(ops,exports):return {'expectedProjectSha256':first['files']['project.vectorcraft'],'operations':ops,'exports':exports}
# 旧版实际公开副本会静默接受冲突ID，并在重排后将旧索引导出为其他画板。
if not c.get('expectEnforced',True):
 wrong=w.execute(revision([],[{'format':'png','artboard':0,'artboardId':ids[1]}]),root/'ignored-id',source=source,runtime_home=runtime)
 shifted=w.execute(revision([reorder],[{'format':'png','artboard':0}]),root/'shifted-index',source=source,runtime_home=runtime)
 assert wrong['outputs'][0]['artboardId']!=ids[1] and shifted['outputs'][0]['artboardId']!=ids[0]
 assert before==hashes(source) and identity==hashes(skill)
 proof={'schema':'vectorcraft-artboard-mapping-baseline/v1','result':'FAIL','expectedGapConfirmed':True,'ignoredExplicitId':{'requested':ids[1],'actual':wrong['outputs'][0]['artboardId']},'silentIndexShift':{'expected':ids[0],'actual':shifted['outputs'][0]['artboardId']},'originalAndSkillPreserved':True,'driverSha256':sha(__file__)}
else:
 from PIL import Image
 import fitz
 import xml.etree.ElementTree as ET
 def verify(directory,manifest):
  model=json.loads((directory/'native.json').read_text());actual={b['id']:b for b in model['artboards']};assert manifest['artboardOrder']==[b['id'] for b in model['artboards']];assert manifest['previewOrder']==[x['path'] for x in manifest['outputs'] if x['format']=='png']
  for item in manifest['outputs']:
   board=actual[item['artboardId']];rect=board['rect'];width,height=rect['x1']-rect['x0'],rect['y1']-rect['y0'];assert item['artboardRect']==rect and item['artboardName']==board['name'];assert model['artboards'][item['artboardIndex']]['id']==board['id'];assert sha(directory/item['path'])==manifest['files'][item['path']]
   original=ids.index(board['id']);color=tuple(bytes.fromhex(boards[original][5][1:]))
   if item['format']=='png':
    with Image.open(directory/item['path']) as im:assert im.size==(width,height) and im.convert('RGB').getpixel((int(width/2),int(height/2)))==color
   elif item['format']=='svg':assert list(map(float,ET.parse(directory/item['path']).getroot().attrib['viewBox'].split()))==[0,0,width,height]
   else:
    with fitz.open(directory/item['path']) as pdf:assert len(pdf)==1 and pdf[0].rect.width==width and pdf[0].rect.height==height
  assert manifest['artboards']==w.native_module().commands.load('artboard_mapping').snapshot(model)
 verify(source,first);cases=[{'name':'legacy-create','result':'PASS','manifest':first}]
 valid=revision([reorder],[{'format':'png','artboardId':ids[2]}]+[{'format':fmt,'artboardId':ids[0]} for fmt in ['svg','png','pdf']])
 moved=w.execute(valid,root/'stable-id',source=source,runtime_home=runtime);verify(root/'stable-id',moved);assert [o['artboardId'] for o in moved['outputs']]==[ids[2],ids[0],ids[0],ids[0]];assert moved['outputs'][1]['artboardIndex']==2;cases.append({'name':'stable-id-after-reorder','result':'PASS','manifest':moved})
 good=w.execute(revision([],[{'format':'png','artboard':1,'artboardId':ids[1]}]),root/'matching',source=source,runtime_home=runtime);verify(root/'matching',good);cases.append({'name':'matching-index-id','result':'PASS','manifest':good})
 failures=[]
 invalid=[('legacy-shift',[reorder],[{'format':'svg','artboardId':ids[2]},{'format':'png','artboard':0}],'artboard_mapping_conflict'),('conflicting-id',[],[{'format':'png','artboard':0,'artboardId':ids[1]}],'artboard_mapping_conflict'),('unknown-id',[],[{'format':'png','artboardId':9999999}],'artboard_id_not_found'),('duplicate-resolved',[],[{'format':'png','artboard':0},{'format':'png','artboardId':ids[0]}],'duplicate_export')]
 for name,operations,exports,reason in invalid:
  output=root/name
  try:w.execute(revision(operations,exports),output,source=source,runtime_home=runtime)
  except ValueError as e:assert reason in str(e);message=str(e)
  else:raise AssertionError('invalid mapping delivered')
  f=json.loads((output/'failure.json').read_text());stage=(output/f['stage']).resolve();assert stage.is_relative_to(root) and stage.is_dir();assert not (output/'manifest.json').exists() and not f['replayAllowed'];assert not list(stage.glob('artboard-*.*'))
  for name,record in f['files'].items():assert sha(stage/name)==record['sha256']
  failures.append({'reason':reason,'message':message,'noSuccessManifest':True,'noExportsBeforeFullMappingValidation':True,'replayAllowed':False,'retainedFiles':hashes(stage)})
 assert before==hashes(source) and identity==hashes(skill)
 proof={'schema':'vectorcraft-artboard-mapping-native/v1','result':'PASS','level':c['level'],'cases':cases,'failures':failures,'sourceAndSkillPreserved':True,'runtimeSha256':first['runtimeSha256'],'driverSha256':sha(__file__),'skillFiles':identity,'scope':'actual legacy create, explicit stable-ID reorder follow, index/ID agreement and four original-stage refusals; decoded SVG/PNG/PDF sizes and PNG color; no complete paint-bounds or PDF date claim'}
(root/'proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'result':proof['result'],'scope':proof.get('scope','baseline known gap')}))
