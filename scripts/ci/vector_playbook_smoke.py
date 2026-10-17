"""原生VectorCraft场景保存重开，检查可编辑对象、几何与渲染像素。"""
import json
import math
import hashlib
from pathlib import Path
import xml.etree.ElementTree as ET
from photo_playbook_smoke import rgb_pixels


def require(ok,message):
    if not ok:raise AssertionError(message)


def nodes(info):
    def walk(node):
        yield node
        for child in node.get('children',[]):yield from walk(child)
    return [n for layer in info['layers'] for n in walk(layer)]


def near(a,b):return len(a)==len(b) and all(math.isclose(x,y,abs_tol=1e-6) for x,y in zip(a,b))


def verify(info,a):
    ns=nodes(info);ab=info['artboards'];require(len(ab)==1 and near([ab[0]['width'],ab[0]['height']],a['artboard']),'Artboard dimensions changed')
    for kind,count in a.get('kindCounts',{}).items():require(sum(n['kind']==kind for n in ns)==count,'Object kind count changed: '+kind)
    texts=[n.get('text','') for n in ns if n['kind']=='Type']
    for text in a.get('texts',[]):require(text in texts,'Editable text missing: '+text)
    if 'textCount' in a:require(len(texts)==a['textCount'],'Outlined delivery retains live text')
    for color in a.get('fills',[]):require(any(n.get('fill','').lower()==color for n in ns),'Object fill missing: '+color)
    if a.get('compoundRequired'):require(any('compound' in n['kind'].lower() for n in ns),'No compound hole geometry')
    if a.get('outlinedRequired'):require(any('compound' in n['kind'].lower() for n in ns),'Outlined glyph geometry missing')
    if 'rectangles' in a:
        bounds=[[n['bounds'][k] for k in ('x','y','width','height')] for n in ns if n['kind']=='Rectangle']
        for expected in a['rectangles']:require(any(near(b,expected) for b in bounds),'Bar geometry changed')
    if 'cropBounds' in a:
        art=[n for n in ns if n['kind']!='Layer' and not n.get('children')]
        require(len(art)==1 and near([art[0]['bounds'][k] for k in ('x','y','width','height')],a['cropBounds']),'Real crop bounds wrong')
        require(art[0].get('closed') is True,'Cropped fill is not closed')
    if 'stroke' in a:
        paths=[n for n in ns if n['kind']=='Path'];require(len(paths)==1,'Stroke path missing')
        p=paths[0];st=a['stroke'];require(math.isclose(p['strokeWidth'],st['width']),'Stroke width wrong')
        for k,v in st.items():
            if k!='width':require(p.get('strokeOptions',{}).get(k)==v,'Stroke option lost: '+k)


def verify_pixels(path,a):
    w,h,p=rgb_pixels(path);require(near([w,h],a['artboard']),'Rendered size changed')
    def pixel(x,y):return list(p[(y*w+x)*3:(y*w+x)*3+3])
    if a.get('ringPixels'):
        require(near(pixel(120,120),[255,255,255]),'Ring center filled')
        require(near(pixel(60,120),[37,99,235]),'Ring band missing')
        require(near(pixel(10,10),[255,255,255]),'Outside background changed')
    if a.get('cropPixels'):
        require(near(pixel(80,120),[124,58,237]),'Retained half missing')
        require(near(pixel(160,120),[255,255,255]),'Discarded half still rendered')


def inspect(r,target):
    rows=[json.loads(x) for x in r.run('run','--in',target,'--cmd','document.inspect').splitlines()]
    return next(x['result'] for x in rows if x.get('command')=='document.inspect')


def run_playbooks(r,path):
    data=json.loads(Path(path).read_text(encoding='utf-8'));require(data['application']=='vectorcraft','Wrong application');records=[]
    for recipe in data['recipes']:
        args=['run']
        for step in recipe['steps']:args+=['--cmd',step['command'],'--params',json.dumps(step['params'],ensure_ascii=False,separators=(',',':'))]
        target=recipe['id']+'.vectorcraft';r.run(*args,'--export',target)
        a=recipe['assertions'];info=inspect(r,target);verify(info,a)
        if a.get('outlinedFile'):verify(inspect(r,a['outlinedFile']),a)
        if a.get('liveMaster'):
            master=inspect(r,a['liveMaster']);require([n.get('text') for n in nodes(master) if n['kind']=='Type']==[a['masterText']],'Editable wordmark master lost')
        svg=recipe['id']+'.svg';r.run('convert',target,svg);tree=ET.fromstring((r.work/svg).read_bytes())
        require(any(e.tag.endswith(('path','rect','ellipse','text')) for e in tree.iter()),'No exported vector objects')
        if a.get('outlinedRequired'):require(not any(e.tag.endswith('}text') for e in tree.iter()),'Outlined SVG has live text')
        png=recipe['id']+'.png';r.run('convert',target,png);verify_pixels(r.work/png,a)
        if recipe['id']=='dimension-unit-delivery':
            group=next(n for n in nodes(info) if n['kind']=='Group')
            changed='dimension-reopened-inches.vectorcraft'
            r.run('run','--in',target,'--cmd','dimension.update','--params',json.dumps({'ids':[group['id']],'options':{'units':'in','precision':2}}),'--export',changed)
            require(any(n.get('text')=='2.00 in' for n in nodes(inspect(r,changed))),'Reopened dimension lost unit editing')
        if recipe['id']=='intertwine-overlap-order':
            def pixel(path,x,y):
                w,h,p=rgb_pixels(path);return list(p[(y*w+x)*3:(y*w+x)*3+3])
            require(pixel(r.work/png,100,80)==[255,0,0],'Intertwine did not change the overlap order')
            released='intertwine-released.vectorcraft'
            r.run('run','--in',target,'--cmd','select.all','--cmd','object.intertwine.release','--export',released)
            require(not any(n['kind']=='Intertwine' for n in nodes(inspect(r,released))),'Intertwine release lost editability')
            r.run('convert',released,'intertwine-released.png')
            require(pixel(r.work/'intertwine-released.png',100,80)==[0,0,255],'Release did not restore original stacking')
            require(pixel(r.work/png,30,80)==pixel(r.work/'intertwine-released.png',30,80)==[255,0,0],
                    'Intertwine changed non-overlap artwork')
        if recipe['id']=='csv-text-variants':
            changed='dataset-reopened-alpha.vectorcraft'
            output=r.run('run','--in',target,'--cmd','dataset.select','--params',json.dumps({'name':'A'}),'--cmd','dataset.export','--export',changed)
            require(any(n.get('text')=='ALPHA' for n in nodes(inspect(r,changed))),'Saved datasets cannot switch text')
            exported=next(x['result']['csv'] for x in map(json.loads,output.splitlines()) if x.get('command')=='dataset.export')
            require('A,ALPHA' in exported and 'B,BETA' in exported,'Dataset export lost variants')
        records.append({'id':recipe['id'],'technicalRoundtrip':'PASS','editableGeometry':'PASS','pixelChecks':'PASS' if a.get('ringPixels') or a.get('cropPixels') else 'NOT_SELECTED','designReview':'NOT_TESTED'})
    require(bool(records),'No Vector workflows selected')
    records.append(existing_document(r))
    return records


def existing_document(r):
    def run(target,commands,source=None):
        args=['run']+(['--in',source] if source else [])
        for command,params in commands:args+=['--cmd',command,'--params',json.dumps(params,separators=(',',':'))]
        rows=[json.loads(x) for x in r.run(*args,'--export',target).splitlines()]
        return [x for x in rows if x.get('step')=='cmd']
    run('existing-user.vectorcraft',[
        ('file.new',{'width':520,'height':280,'units':'Pixels','backgroundContents':'white'}),
        ('shape.rectangle',{'x':20,'y':20,'width':60,'height':50}),
        ('paint.setFill',{'color':'#d97706'}),('paint.setStroke',{'none':True}),
        ('text.create',{'x':20,'y':250,'text':'KEEP ME','size':24,'font':'Arial','color':'#172033'})])
    original_hash=hashlib.sha256((r.work/'existing-user.vectorcraft').read_bytes()).hexdigest()
    original=nodes(inspect(r,'existing-user.vectorcraft'));owned={n['id']:n for n in original if n['kind']!='Layer'}
    created=run('existing-with-circles.vectorcraft',[
        ('shape.ellipse',{'x':300,'y':60,'width':160,'height':160}),('paint.setFill',{'color':'#2563eb'}),('paint.setStroke',{'none':True}),
        ('shape.ellipse',{'x':340,'y':100,'width':80,'height':80}),('paint.setFill',{'color':'#2563eb'}),('paint.setStroke',{'none':True})],'existing-user.vectorcraft')
    circle_ids=[x['result']['id'] for x in created if x['command']=='shape.ellipse']
    require(len(circle_ids)==2,'Actual circle IDs not captured')
    created=run('existing-wordmark-live.vectorcraft',[
        ('object.pathfinder.minusFront',{'ids':circle_ids}),
        ('text.create',{'x':200,'y':250,'text':'CRAFT','size':32,'font':'Arial','color':'#172033'})],'existing-with-circles.vectorcraft')
    target_id=next(x['result']['id'] for x in created if x['command']=='text.create')
    run('existing-wordmark-outlined.vectorcraft',[
        ('select.set',{'ids':[target_id]}),('type.createOutlines',{})],'existing-wordmark-live.vectorcraft')
    for name in ['existing-wordmark-live.vectorcraft','existing-wordmark-outlined.vectorcraft']:
        ns=nodes(inspect(r,name));now={n['id']:n for n in ns}
        for id,before in owned.items():require(now.get(id)==before,'Pre-existing user object changed')
        require(any('compound' in n['kind'].lower() for n in ns),'Owned ring geometry missing')
        texts=[n.get('text') for n in ns if n['kind']=='Type']
        require('KEEP ME' in texts,'User text outlined or lost')
        require(('CRAFT' in texts)==('live' in name),'Target wordmark state incorrect')
    r.run('convert','existing-wordmark-outlined.vectorcraft','existing-preserved.png')
    w,h,p=rgb_pixels(r.work/'existing-preserved.png')
    require((w,h)==(520,280),'Existing canvas changed')
    for x,y,color in [(380,140,[255,255,255]),(320,140,[37,99,235])]:
        require(list(p[(y*w+x)*3:(y*w+x)*3+3])==color,'Owned ring render incorrect')
    require(hashlib.sha256((r.work/'existing-user.vectorcraft').read_bytes()).hexdigest()==original_hash,'Input file modified')
    return {'id':'existing-user-content-preservation','technicalRoundtrip':'PASS','actualIdBinding':'PASS','preservedOriginalObjects':len(owned),'sourceUnchanged':'PASS','designReview':'NOT_TESTED'}
