"""原生A3海报往返：全文、二维码、入口、图片比例与独立交付。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import zipfile
import xml.etree.ElementTree as ET
from urllib.parse import unquote
from design_playbook_smoke import run_script,require,near,verify
from design_core_smoke import catalog_png


def verify_qr_bounds(actual,rect):
    # Native QR reports ink path bounds; its reserved white edge lies inside rect.
    import math
    x0,y0,x1,y1=actual;left,top,right,bottom=rect
    require(left<x0<x1<right and top<y0<y1<bottom,'QR ink has no reserved white border')
    require(math.isclose(x1-x0,y1-y0,abs_tol=1e-5),'QR ink is stretched')
    require(math.isclose(x0+x1,left+right,abs_tol=1e-5) and math.isclose(y0+y1,top+bottom,abs_tol=1e-5),'QR ink is not centred in reserved square')


def verify_registration(destination,qr_content,visible,registration_id,hyperlinks):
    require(qr_content==destination,'QR encoded a different destination')
    require(destination in visible,'Visible registration URL differs from approved destination')
    require(len(hyperlinks)==1 and hyperlinks[0].get('dest')=={'kind':'url','value':destination},'Poster registration hyperlink lost or changed')
    require(hyperlinks[0].get('source')=={'id':registration_id,'kind':'item'},'Poster link bound to wrong frame')


def verify_poster(info,stories,bindings,recipe,links,hyperlinks):
    verify(info,stories,bindings,recipe['assertions'])
    text_steps=[s for s in recipe['steps'] if s['command']=='frame.create' and s['params'].get('content')=='text']
    by_frame={s['frames'][0]:s for s in stories}
    for step in text_steps:
        story=by_frame[bindings[step['capture']]['id']]
        require(story['text']==step['params']['text'],'Poster full text changed: '+step['capture'])
        require(story['overset'] is None,'Poster remains overset: '+step['capture'])
    destination=recipe['approvedDestination']
    verify_registration(destination,bindings['qr']['content'],by_frame[bindings['registration']['id']]['text'],bindings['registration']['id'],hyperlinks)
    require(len(links)==1 and links[0]['status']=='ok','Poster image link missing')
    uses=links[0]['uses'];require(len(uses)==1 and uses[0]['id']==bindings['hero']['id'],'Poster image bound to wrong frame')
    require(uses[0]['ppi']>=150,'Poster image effective PPI below threshold')
    items={i['id']:i for sp in info['spreads'] for i in sp['items']}
    qr_step=next(s for s in recipe['steps'] if s['command']=='object.qrCode')
    verify_qr_bounds(items[bindings['qr']['id']]['bounds'],qr_step['params']['rect'])


def run_poster(r,skills):
    root=Path(skills)/'designcraft-poster-layout';recipe=json.loads((root/'references/craft-steps.json').read_text(encoding='utf-8'))
    spec=importlib.util.spec_from_file_location('poster_compiler',root/'scripts/write_script.py');compiler=importlib.util.module_from_spec(spec);spec.loader.exec_module(compiler)
    inputs=r.work/'poster-input';inputs.mkdir();image=inputs/'hero.png';catalog_png(image,(25,80,210),3);digest=hashlib.sha256(image.read_bytes()).hexdigest()
    steps,names=compiler.compile_steps(recipe)
    target='core-poster.designcraft';pdf='core-poster.pdf';idml='core-poster.idml'
    results=run_script(r,steps,save=target,exports=[pdf,idml]);bindings={n:results[i] for n,i in names.items()}
    info=json.loads(r.run('run','--in',target,'--cmd','document.inspect'))
    text_steps=[s for s in recipe['steps'] if s['command']=='frame.create' and s['params'].get('content')=='text']
    queries=[{'command':'story.get','params':{'frame':bindings[s['capture']]['id']}} for s in text_steps]
    stories=run_script(r,queries,source=target)
    links,hyperlinks,preflight=run_script(r,[{'command':c,'params':{'minPpi':150} if c=='preflight.run' else {}} for c in ['links.list','hyperlink.list','preflight.run']],source=target)
    (r.work/'core-poster-inspection.json').write_text(json.dumps({'info':info,'stories':stories,'bindings':bindings,'links':links,'hyperlinks':hyperlinks,'preflight':preflight},ensure_ascii=False,indent=2),encoding='utf-8')
    verify_poster(info,stories,bindings,recipe,links,hyperlinks)
    require(not preflight['issues'],'Poster preflight issues: '+str(preflight))
    with zipfile.ZipFile(r.work/idml) as archive:
        xmls=[ET.fromstring(archive.read(n)) for n in archive.namelist() if n.startswith('Stories/') and n.endswith('.xml')]
        for step in text_steps:
            expected=step['params']['text'];found=[xml for xml in xmls if ''.join(e.text or '' for e in xml.iter() if e.tag.endswith('Content')) in [expected,expected.replace('\n','')]]
            require(len(found)==1,'Poster IDML full text missing or duplicated')
            select_index=next(i for i,s in enumerate(recipe['steps']) if s['command']=='text.select' and s['params']['story']=={'$ref':step['capture']+'.story'})
            style=recipe['steps'][select_index+1]['params']['name'];paragraphs=[e for e in found[0].iter() if e.tag.endswith('ParagraphStyleRange')]
            require(paragraphs and all(unquote(e.attrib.get('AppliedParagraphStyle','')).endswith('/'+style) for e in paragraphs),'Poster editable style lost')
    r.run('run','--in',target,'--export','core-poster.png')
    require((r.work/'core-poster.png').read_bytes().startswith(b'\x89PNG'),'Poster PNG invalid')
    require((r.work/pdf).read_bytes().startswith(b'%PDF'),'Poster PDF invalid')
    run_script(r,recipe['deliverySteps'],source=target)
    package=r.work/'poster-package';native=list(package.glob('*.designcraft'));require(len(native)==1,'Poster packaged project missing')
    packaged_stories=run_script(r,queries,source=str(native[0]));require(packaged_stories==stories,'Packaged poster text changed')
    require(hashlib.sha256(image.read_bytes()).hexdigest()==digest,'Poster input image changed')
    require(hashlib.sha256((package/'Links/hero.png').read_bytes()).hexdigest()==digest,'Poster package image changed')
    return {'id':'poster-layout','coreSkill':'designcraft-poster-layout','technicalRoundtrip':'PASS','a3Dimensions':'PASS','fiveStoriesAndStyles':'PASS','nativeQrAndHyperlinkDestination':'PASS','imageBindingAndPpi':'PASS','sourceImageUnchanged':'PASS','packagedReopen':'PASS','exportedQrDecode':'NOT_TESTED','layoutReview':'NOT_TESTED','hostSameCanvas':'NOT_TESTED'}
