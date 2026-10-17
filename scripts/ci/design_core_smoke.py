"""验证核心刊物的原生故事链、完整内容、栏数和可编辑样式。"""
import importlib.util
import json
import zipfile
import xml.etree.ElementTree as ET
from urllib.parse import unquote
from pathlib import Path
from design_playbook_smoke import run_script,require,verify,idml_check


def verify_newsletter(info,story,bindings,expected,assertions):
    verify(info,[story],bindings,assertions)
    require(story['overset'] is None,'Newsletter remains overset')
    require(story['text']==expected,'Newsletter full text changed')
    expected_ids=[bindings['body']['id'],bindings['continuation']['id']]
    require(story['frames']==expected_ids,'Newsletter story order changed')
    items={i['id']:i for spread in info['spreads'] for i in spread['items']}
    require(all(items[i]['columns']==3 for i in expected_ids),'Newsletter three-column settings lost')


def run_newsletter(r,skills):
    root=Path(skills)/'designcraft-newsletter'
    recipe=json.loads((root/'references/craft-steps.json').read_text(encoding='utf-8'))
    spec=importlib.util.spec_from_file_location('newsletter_compiler',root/'scripts/write_script.py')
    compiler=importlib.util.module_from_spec(spec);spec.loader.exec_module(compiler)
    steps,names=compiler.compile_steps(recipe)
    target='core-newsletter.designcraft';pdf='core-newsletter.pdf';idml='core-newsletter.idml'
    results=run_script(r,steps,save=target,exports=[pdf,idml]);bindings={n:results[i] for n,i in names.items()}
    require(bindings['before_thread']['overset'] is not None,'Fixture did not exercise continuation')
    info=json.loads(r.run('run','--in',target,'--cmd','document.inspect'))
    story=run_script(r,[{'command':'story.get','params':{'frame':bindings['body']['id']}}],source=target)[0]
    expected=next(s['params']['text'] for s in recipe['steps'] if s.get('capture')=='body')
    verify_newsletter(info,story,bindings,expected,recipe['assertions'])
    preflight=run_script(r,[{'command':'preflight.run','params':{'minPpi':150}}],source=target)[0]
    require(not any(i['severity']=='error' for i in preflight['issues']),'Newsletter preflight errors: '+str(preflight))
    idml_check(r.work/idml,recipe['assertions'])
    with zipfile.ZipFile(r.work/idml) as archive:
        body_roots=[]
        for name in archive.namelist():
            if name.startswith('Stories/') and name.endswith('.xml'):
                root=ET.fromstring(archive.read(name))
                content=''.join(e.text or '' for e in root.iter() if e.tag.endswith('Content'))
                if expected.split('\n')[0] in content:body_roots.append(root)
        require(len(body_roots)==1,'Newsletter body story missing or duplicated in IDML')
        paragraphs=[e for e in body_roots[0].iter() if e.tag.endswith('ParagraphStyleRange')]
        require(len(paragraphs)==len(expected.split('\n')),'Newsletter paragraph structure changed')
        require(all(unquote(e.attrib.get('AppliedParagraphStyle','')).endswith('/Newsletter Body') for e in paragraphs),'Newsletter body paragraph style missing')
    require((r.work/pdf).read_bytes().startswith(b'%PDF'),'Newsletter PDF invalid')
    (r.work/'core-newsletter-inspection.json').write_text(json.dumps({'info':info,'story':story,'bindings':bindings,'preflight':preflight},ensure_ascii=False,indent=2),encoding='utf-8')
    return {'id':'newsletter','coreSkill':'designcraft-newsletter','technicalRoundtrip':'PASS','fullStory':'PASS','threadOrder':'PASS','threeColumns':'PASS','editableParagraphStyle':'PASS','finalPreflight':'PASS','layoutReview':'NOT_TESTED','hostSameCanvas':'NOT_TESTED'}


def catalog_png(path,color):
    """生成原创600×400测试素材；不使用外部商品图片。"""
    import struct
    import zlib
    def chunk(kind,data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
    rows=[]
    for y in range(400):
        row=b''.join(bytes(color if 80<=x<520 and 60<=y<340 else (245,245,245)) for x in range(600))
        rows.append(b'\0'+row)
    path.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',600,400,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(b''.join(rows)))+chunk(b'IEND',b''))


def verify_catalog_links(links,products,bindings):
    require(len(links)==len(products),'Catalog linked asset count wrong')
    for product in products:
        name=Path(product['image']).name
        matches=[link for link in links if Path(link.get('path','')).name==name]
        require(len(matches)==1,'Catalog SKU asset missing or duplicated: '+product['sku'])
        link=matches[0];require(link['status']=='ok','Catalog asset is not linked and available: '+product['sku'])
        uses=link['uses'];expected=bindings[product['key']+'_image']['id']
        require([use['id'] for use in uses]==[expected],'Catalog image bound to wrong SKU frame')
        require(all(use['ppi']>=150 for use in uses),'Catalog effective image PPI below threshold')


def run_catalog(r,skills):
    import hashlib
    root=Path(skills)/'designcraft-catalog'
    recipe=json.loads((root/'references/craft-steps.json').read_text(encoding='utf-8'))
    spec=importlib.util.spec_from_file_location('catalog_compiler',root/'scripts/write_script.py')
    compiler=importlib.util.module_from_spec(spec);spec.loader.exec_module(compiler)
    inputs=r.work/'catalog-input';inputs.mkdir()
    catalog_png(inputs/'sku-101.png',(25,80,210));catalog_png(inputs/'sku-205.png',(225,110,20))
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs.iterdir()}
    steps,names=compiler.compile_steps(recipe)
    target='core-catalog.designcraft';pdf='core-catalog.pdf';idml='core-catalog.idml'
    results=run_script(r,steps,save=target,exports=[pdf,idml]);bindings={n:results[i] for n,i in names.items()}
    info=json.loads(r.run('run','--in',target,'--cmd','document.inspect'))
    queries=[{'command':'story.get','params':{'frame':bindings[p['key']+'_copy']['id']}} for p in recipe['products']]
    stories=run_script(r,queries,source=target)
    verify(info,stories,bindings,recipe['assertions'])
    for product,story in zip(recipe['products'],stories):
        require(story['text']==product['text'] and story['overset'] is None,'Catalog SKU text changed or overset')
    links=run_script(r,[{'command':'links.list','params':{}}],source=target)[0]
    verify_catalog_links(links,recipe['products'],bindings)
    preflight=run_script(r,[{'command':'preflight.run','params':{'minPpi':150}}],source=target)[0]
    require(not any(i['severity']=='error' for i in preflight['issues']),'Catalog preflight errors: '+str(preflight))
    package=r.work/'catalog-package';native=list(package.glob('*.designcraft'))
    require(len(native)==1,'Packaged native project missing or ambiguous')
    for name,digest in hashes.items():
        copy=package/'Links'/name
        require(copy.is_file() and hashlib.sha256(copy.read_bytes()).hexdigest()==digest,'Packaged image bytes changed')
    # Test fixture isolation only: user inputs are never moved by the skill.
    offline=r.work/'catalog-input-offline';inputs.rename(offline)
    try:
        packaged_links=run_script(r,[{'command':'links.list','params':{}}],source=str(native[0]))[0]
        verify_catalog_links(packaged_links,recipe['products'],bindings)
        packaged_stories=run_script(r,queries,source=str(native[0]))
        require([s['text'] for s in packaged_stories]==[p['text'] for p in recipe['products']],'Packaged SKU text changed')
        r.run('run','--in',str(native[0]),'--export','core-catalog-detached.pdf')
        require((r.work/'core-catalog-detached.pdf').read_bytes().startswith(b'%PDF'),'Detached catalog PDF invalid')
    finally:
        offline.rename(inputs)
    require(all(hashlib.sha256((inputs/name).read_bytes()).hexdigest()==digest for name,digest in hashes.items()),'Original product assets changed')
    # Every product story must retain the applied paragraph style, not only a named style definition.
    with zipfile.ZipFile(r.work/idml) as archive:
        for product in recipe['products']:
            roots=[]
            for name in archive.namelist():
                if name.startswith('Stories/') and name.endswith('.xml'):
                    xml=ET.fromstring(archive.read(name));text=''.join(e.text or '' for e in xml.iter() if e.tag.endswith('Content'))
                    if product['sku'] in text:roots.append(xml)
            require(len(roots)==1,'Product story missing or duplicated in IDML')
            paragraphs=[e for e in roots[0].iter() if e.tag.endswith('ParagraphStyleRange')]
            require(len(paragraphs)==len(product['text'].split('\n')),'Product paragraphs changed')
            require(all(unquote(e.attrib.get('AppliedParagraphStyle','')).endswith('/Catalog Product') for e in paragraphs),'Product paragraph style missing')
    (r.work/'core-catalog-inspection.json').write_text(json.dumps({'info':info,'stories':stories,'links':links,'packagedLinks':packaged_links,'packageResult':bindings['package'],'preflight':preflight,'inputHashes':hashes},ensure_ascii=False,indent=2),encoding='utf-8')
    return {'id':'catalog','coreSkill':'designcraft-catalog','technicalRoundtrip':'PASS','skuTextAndImageBindings':'PASS','editableParagraphStyles':'PASS','detachedPackageReopen':'PASS','sourceImagesUnchanged':'PASS','layoutReview':'NOT_TESTED','hostSameCanvas':'NOT_TESTED'}
