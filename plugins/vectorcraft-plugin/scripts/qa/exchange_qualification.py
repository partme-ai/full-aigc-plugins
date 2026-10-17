#!/usr/bin/env python3
"""VC-DM-005外部验收：自动自由渐变退化、原生编辑保全与格式/披露拒绝。"""
import base64
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys
import xml.etree.ElementTree as ET

c=json.loads(Path(sys.argv[1]).read_text());root=Path(c['output']).resolve();root.mkdir(exist_ok=False)
skill=Path(c['skill']).resolve();runtime=Path(c['runtime']).resolve();binary=runtime/'vectorcraft/0.2.0-craft.2/vectorcraft-cli'
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def tree(path):return {p.relative_to(path).as_posix():sha(p) for p in sorted(path.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
w=load('qualified_workflow',skill/'scripts/workflow.py');sessions=load('qualified_sessions',skill/'scripts/mcp_session.py')
loss_module=load('qualified_loss',skill/'scripts/exchange_loss.py');quality=load('qualified_quality',Path(c['quality']))
identity=tree(skill)
plan={'document':{'name':'Automatic freeform exchange','width':96,'height':80,'units':'Pixels'},'operations':[
    {'command':'shape.rectangle','params':{'x':12,'y':16,'width':60,'height':40}},
    {'command':'native.command','params':{'command':'paint.setFill','params':{'gradient':{'kind':'freeform','stops':[{'offset':0,'color':'#ef5b36'},{'offset':1,'color':'#2366e8'}]}}}},
    {'command':'paint.setStroke','params':{'none':True}}],'exports':[]}
source=root/'source';first=w.execute(plan,source,runtime_home=runtime);source_before=tree(source)
source_model=json.loads((source/'native.json').read_text())
def paths(nodes):
    result=[]
    for node in nodes:
        if node['kind']['type']=='path':result.append(node)
        result+=paths(node['kind'].get('children',[]))
    return result
objects=paths(source_model['layers']);assert len(objects)==1
target=objects[0]['id'];assert target>0 and objects[0]['appearance']['items'][0]['paint']['gradient']['kind']=='Freeform'
def inspect(directory):
    with sessions.Session([str(binary),'mcp','--headless']) as native:
        native.command('document.open',{'path':str(directory/'project.vectorcraft')})
        model=native.command('document.json',{})
        assert model==json.loads((directory/'native.json').read_text())
        native.command('select.set',{'ids':[target]})
        points=native.command('paint.freeform.get',{})
    return model,points
_,original_points=inspect(source);assert len(original_points['points'])>=2
out=root/'exported';export_plan={'expectedProjectSha256':first['files']['project.vectorcraft'],'operations':[],
    'exports':[{'format':fmt,'artboard':0} for fmt in ['svg','pdf','png']]}
manifest=w.execute(export_plan,out,source=source,runtime_home=runtime);export_before=tree(out)
model,points=inspect(out)
assert model['layers']==source_model['layers'] and model['artboards']==source_model['artboards']
assert model['metadata']['created']==source_model['metadata']['created'] and points==original_points
loss=json.loads((out/'exchange-loss.json').read_text());svg=next(row for row in loss['outputs'] if row['format']=='svg')
scope=svg['observations']['rasterizationScope'];assert len(scope['elements'])==1
element=scope['elements'][0]
assert element['classification']=='embedded-raster' and element['geometry']=={'x':'12','y':'16','width':'60','height':'40'}
assert scope['vectorOnly'] is False and scope['losslessVectorClaimAllowed'] is False and scope['completePaintBounds'] is False
assert 'freeform gradients are written as images clipped to their shapes' in svg['warnings']
assert svg['observations']['svg']['clipPath']==1
xml=ET.parse(out/'artboard-1.svg').getroot();image=next(n for n in xml.iter() if n.tag.rsplit('}',1)[-1]=='image')
href=image.get('href',image.get('{http://www.w3.org/1999/xlink}href'));payload=base64.b64decode(href.split(',',1)[1],validate=True)
assert hashlib.sha256(payload).hexdigest()==element['payloadSha256']
from PIL import Image
import fitz
with Image.open(io.BytesIO(payload)) as im:
    # 固定引擎 grid_size：长边120设备像素／4，向上取2的幂为32，短边ceil(32*40/60)=22。
    assert im.size==(32,22);im.verify()
with Image.open(out/'artboard-1.png') as im:
    im.verify()
with Image.open(out/'artboard-1.png') as im:
    rgba=im.convert('RGBA');assert rgba.size==(96,80) and rgba.getpixel((2,2))[3]==0
    white=Image.new('RGBA',rgba.size,'white');white.alpha_composite(rgba);reference=white.convert('RGB')
samples=[(16,20),(40,35),(68,52),(2,2),(94,78)];decoded=[]
for fmt in ['svg','pdf']:
    with fitz.open(out/('artboard-1.'+fmt)) as doc:
        assert len(doc)==1 and doc[0].rect.width==96 and doc[0].rect.height==80
        pix=doc[0].get_pixmap(alpha=False);render=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
        delta=max(abs(a-b) for xy in samples for a,b in zip(render.getpixel(xy),reference.getpixel(xy)))
        assert delta<=5,(fmt,delta)
        decoded.append({'format':fmt,'result':'PASS','size':[96,80],'sampleMaxChannelDelta':delta,'samples':[{'at':list(xy),'rgb':list(render.getpixel(xy))} for xy in samples]})
decoded.append({'format':'png','result':'PASS','size':[96,80],'outsideAlpha':0})
checked=quality.check_delivery(out,manifest['runtimeSha256'],manifest['files']['project.vectorcraft']);assert checked['technicalStatus']=='PASS'
# 在新修订中编辑真实控制点，原始源工程和既有导出均保持字节不变。
edited=root/'edited';edited_manifest=w.execute({'expectedProjectSha256':first['files']['project.vectorcraft'],'operations':[
    {'command':'select.set','params':{'ids':[target]}},
    {'command':'native.command','params':{'command':'paint.freeform.setPoint','params':{'index':0,'color':'#22aa66'}}}],
    'exports':[]},edited,source=source,runtime_home=runtime)
edited_model,edited_points=inspect(edited)
assert paths(edited_model['layers'])[0]['appearance']['items'][0]['paint']['gradient']['kind']=='Freeform'
assert len(edited_points['points'])==len(original_points['points'])
assert edited_points['points'][0]['color']!=original_points['points'][0]['color']
for before,after in zip(original_points['points'],edited_points['points']):
    assert {k:v for k,v in before.items() if k!='color'}=={k:v for k,v in after.items() if k!='color'}
assert edited_points['points'][1:]==original_points['points'][1:]
refusals=[]
for fault in ['undisclosed-raster','wrong-scope','unblocked-claim','corrupt-embedded-png','corrupt-pdf','corrupt-png']:
    directory=root/fault;shutil.copytree(out,directory)
    saved=json.loads((directory/'manifest.json').read_text());report=json.loads((directory/'exchange-loss.json').read_text())
    row=next(r for r in report['outputs'] if r['format']=='svg')
    if fault=='undisclosed-raster':row['observations'].pop('rasterizationScope')
    elif fault=='wrong-scope':row['observations']['rasterizationScope']['elements'][0]['geometry']['width']='1'
    elif fault=='unblocked-claim':row['changes']=[x for x in row['changes'] if x['code']!='lossless-vector-claim']
    else:
        if fault=='corrupt-embedded-png':
            data=bytearray(payload);data[29]^=1;altered=href.split(',',1)[0]+','+base64.b64encode(data).decode()
            f=directory/'artboard-1.svg';f.write_text(f.read_text().replace(href,altered))
        elif fault=='corrupt-pdf':(directory/'artboard-1.pdf').write_bytes(b'%PDF-1.7\ncorrupt fixture\n')
        else:
            f=directory/'artboard-1.png';data=bytearray(f.read_bytes());data[-1]^=1;f.write_bytes(data[:33])
        report=loss_module.write_report(directory,[x['path'] for x in manifest['outputs']],{x['path']:x['warnings'] for x in manifest['outputs']},{'artboard-1.svg':svg['observations']['svgTextExportMode']})
    (directory/'exchange-loss.json').write_text(json.dumps(report))
    for name in saved['files']:saved['files'][name]=sha(directory/name)
    saved['lossReport']['sha256']=saved['files']['exchange-loss.json'];(directory/'manifest.json').write_text(json.dumps(saved))
    failed=quality.check_delivery(directory,manifest['runtimeSha256'],manifest['files']['project.vectorcraft'])
    assert failed['artifactIntegrityStatus']=='PASS' and failed['technicalStatus']=='FAIL' and failed['acceptanceStatus']=='blocked',failed
    refusals.append({'fault':fault,'explicitQaMutation':True,'freshMatchingManifestHashes':True,'quality':failed,'result':'PASS'})
bad=root/'corrupt-native';shutil.copytree(source,bad);(bad/'project.vectorcraft').write_bytes(b'invalid native fixture')
with sessions.Session([str(binary),'mcp','--headless']) as native:
    try:native.command('document.open',{'path':str(bad/'project.vectorcraft')})
    except RuntimeError as error:
        reason=str(error).replace(str(root),'QA_ROOT');assert 'outcome_unknown' not in reason
    else:raise AssertionError('invalid native document opened')
refusals.append({'fault':'corrupt-native','explicitQaMutation':True,'knownNativeRefusal':reason,'result':'PASS'})
assert tree(source)==source_before and tree(out)==export_before and tree(skill)==identity
proof={'schema':'vectorcraft-exchange-qualification-native/v1','result':'PASS','level':'fixed-install','platform':'Darwin-arm64',
    'runtimeSha256':sha(binary),'driverSha256':sha(__file__),'skillFiles':identity,'plan':plan,'exportPlan':export_plan,
    'sourceNativeModel':source_model,'exportedNativeModel':model,'originalPoints':original_points,'editedPoints':edited_points,
    'originalFiles':source_before,'exportedFiles':export_before,'manifest':manifest,'lossReport':loss,'quality':checked,'decoded':decoded,
    'sourceAndPreviousExportsPreserved':True,'nativeGradientEditableAfterIndependentReopen':True,'automaticRasterizationWithoutExpand':True,
    'rasterPayloadDecodedSize':[32,22],'rasterPayloadSha256':hashlib.sha256(payload).hexdigest(),'refusals':refusals,
    'scope':'actual public55/source41 installed export and quality code; automatic freeform gradient SVG fallback; original live gradient reopened and edited in a new revision; seven explicit disclosure/format refusals; no GUI,creative,other-platform or universal fidelity claim'}
(root/'proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'result':'PASS','refusals':7,'decoded':3}))
