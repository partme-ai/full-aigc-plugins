#!/usr/bin/env python3
"""外部QA：真实矢量、实时滤镜、展开栅格的三格式解码及原生重开。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import shutil

config=json.loads(Path(sys.argv[1]).read_text())
root=Path(config['output']).resolve();root.mkdir(exist_ok=False)
skill=Path(config['skill']).resolve();runtime=Path(config['runtime']).resolve()
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def tree(path):return {p.relative_to(path).as_posix():sha(p) for p in sorted(path.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
w=load('exchange_workflow',skill/'scripts/workflow.py');session=load('exchange_session',skill/'scripts/mcp_session.py')
identity=tree(skill);cases=[]
quality=load('exchange_quality',Path(config['quality'])) if config.get('quality') else None
refusals=[]
import fitz
from PIL import Image
for name in (['expanded-raster'] if config.get('baseline') else ['vector','live-filter','expanded-raster']):
    ops=[{'command':'shape.rectangle','params':{'x':20,'y':20,'width':30,'height':20}},
         {'command':'paint.setFill','params':{'color':'#2366e8'}},{'command':'paint.setStroke','params':{'none':True}}]
    if name!='vector':ops.append({'command':'native.command','params':{'command':'effect.apply','params':{'effect':'blur.gaussian','params':{'radius':3}}}})
    if name=='expanded-raster':ops.append({'command':'native.command','params':{'command':'effect.expandAppearance','params':{}}})
    plan={'document':{'name':name,'width':80,'height':64,'units':'Pixels'},'operations':ops,'exports':[{'format':fmt,'artboard':0} for fmt in ['svg','pdf','png']]}
    out=root/name;manifest=w.execute(plan,out,runtime_home=runtime);before=tree(out)
    binary=runtime/'vectorcraft/0.2.0-craft.2/vectorcraft-cli'
    with session.Session([str(binary),'mcp','--headless']) as native:
        native.command('document.open',{'path':str(out/'project.vectorcraft')})
        reopened=native.command('document.json',{})
    assert reopened==json.loads((out/'native.json').read_text())
    loss=json.loads((out/'exchange-loss.json').read_text());row=next(row for row in loss['outputs'] if row['format']=='svg')
    if config.get('baseline'):
        assert row['observations']['svg']['image']==1 and 'rasterizationScope' not in row['observations']
        assert tree(out)==before and tree(skill)==identity
        proof={'schema':'vectorcraft-exchange-baseline/v1','result':'FAIL','expectedGapConfirmed':True,'imageCount':1,'scopeAbsent':True,
               'nativeReopenEqual':True,'sourceAndSkillPreserved':True,'driverSha256':sha(__file__),'lossReport':loss,'skillFiles':identity,'runtimeSha256':sha(binary)}
        (root/'proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({'result':'FAIL','expectedGapConfirmed':True}));sys.exit(0)
    scope=row['observations']['rasterizationScope'];assert scope['losslessVectorClaimAllowed'] is False
    assert len(scope['elements'])==(1 if name=='expanded-raster' else 0)
    if name=='expanded-raster':assert scope['elements'][0]['classification']=='embedded-raster'
    decoded=[]
    for fmt in ['svg','pdf']:
        with fitz.open(out/('artboard-1.'+fmt)) as doc:
            assert len(doc)==1 and doc[0].rect.width==80 and doc[0].rect.height==64
            assert doc[0].get_pixmap().width==80
            decoded.append({'format':fmt,'size':[80,64],'decoder':'PyMuPDF','result':'PASS'})
    with Image.open(out/'artboard-1.png') as im:
        assert im.size==(80,64);im.verify()
        decoded.append({'format':'png','size':[80,64],'decoder':'Pillow','result':'PASS'})
    assert before==tree(out)
    checked=None
    if quality:
        checked=quality.check_delivery(out,manifest['runtimeSha256'],manifest['files']['project.vectorcraft'])
        assert checked['technicalStatus']=='PASS',checked
        if name=='expanded-raster':
            for fault in ['missing-disclosure','wrong-scope','unblocked-claim','changed-svg']:
                target=root/fault;shutil.copytree(out,target)
                saved=json.loads((target/'manifest.json').read_text())
                if fault=='missing-disclosure':saved.pop('lossReport')
                elif fault=='changed-svg':
                    path=target/'artboard-1.svg';path.write_text(path.read_text().replace('width="80"','width="81"',1))
                    saved['files'][path.name]=sha(path)
                else:
                    path=target/'exchange-loss.json';loss_copy=json.loads(path.read_text());svg=next(row for row in loss_copy['outputs'] if row['format']=='svg')
                    if fault=='wrong-scope':svg['observations']['rasterizationScope']['elements']=[]
                    else:svg['changes']=[c for c in svg['changes'] if c['code']!='lossless-vector-claim']
                    path.write_text(json.dumps(loss_copy));saved['files'][path.name]=sha(path);saved['lossReport']['sha256']=sha(path)
                (target/'manifest.json').write_text(json.dumps(saved))
                failed=quality.check_delivery(target,manifest['runtimeSha256'],manifest['files']['project.vectorcraft'])
                assert failed['technicalStatus']=='FAIL' and 'raster_disclosure' in failed['error'],failed
                refusals.append({'fault':fault,'explicitQaMutation':True,'result':'PASS','quality':failed})
            assert tree(out)==before
    cases.append({'name':name,'result':'PASS','plan':plan,'nativeReopenEqual':True,'sourcePreserved':True,'nativeJsonSha256':sha(out/'native.json'),
                  'projectSha256':sha(out/'project.vectorcraft'),'manifest':manifest,'lossReport':loss,'decoded':decoded,'quality':checked})
assert tree(skill)==identity
proof={'schema':'vectorcraft-exchange-native/v1','result':'PASS','level':config['level'],'cases':cases,'skillPreserved':True,
       'skillFiles':identity,'driverSha256':sha(__file__),'runtimeSha256':sha(binary),'refusals':refusals,
       'scope':'three native source/export cases, nine independently decoded outputs, editable project separately reopened; no GUI/creative/other-platform acceptance'}
(root/'proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'result':'PASS','cases':3,'decoded':9}))
