"""原生VectorCraft场景保存重开，检查可编辑对象、几何与渲染像素。"""
import json
import math
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
        records.append({'id':recipe['id'],'technicalRoundtrip':'PASS','editableGeometry':'PASS','pixelChecks':'PASS' if a.get('ringPixels') or a.get('cropPixels') else 'NOT_SELECTED','designReview':'NOT_TESTED'})
    require(bool(records),'No Vector workflows selected');return records
