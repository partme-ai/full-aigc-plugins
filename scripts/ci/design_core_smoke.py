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


def catalog_png(path,color,scale=1):
    """生成原创600×400测试素材；不使用外部商品图片。"""
    import struct
    import zlib
    def chunk(kind,data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
    rows=[]
    for y in range(400*scale):
        row=b''.join(bytes(color if 80*scale<=x<520*scale and 60*scale<=y<340*scale else (245,245,245)) for x in range(600*scale))
        rows.append(b'\0'+row)
    path.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',600*scale,400*scale,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(b''.join(rows)))+chunk(b'IEND',b''))


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
        import shutil
        transfer=r.work/'catalog-transfer'/'received'
        shutil.copytree(package,transfer)
        package_offline=r.work/'catalog-package-offline';package.rename(package_offline)
        previous_work=r.work
        try:
            r.work=transfer
            transferred_native=next(transfer.glob('*.designcraft'))
            relocated_links=run_script(r,[{'command':'links.list','params':{}}],source=str(transferred_native))[0]
            verify_catalog_links(relocated_links,recipe['products'],bindings)
            r.run('run','--in',str(transferred_native),'--export','relocated-proof.pdf')
            require((transfer/'relocated-proof.pdf').read_bytes().startswith(b'%PDF'),'Relocated package PDF invalid')
        finally:
            r.work=previous_work
            package_offline.rename(package)
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
    (r.work/'core-catalog-inspection.json').write_text(json.dumps({'info':info,'stories':stories,'links':links,'packagedLinks':packaged_links,'relocatedLinks':relocated_links,'packageResult':bindings['package'],'preflight':preflight,'inputHashes':hashes},ensure_ascii=False,indent=2),encoding='utf-8')
    return {'id':'catalog','coreSkill':'designcraft-catalog','technicalRoundtrip':'PASS','skuTextAndImageBindings':'PASS','editableParagraphStyles':'PASS','detachedPackageReopen':'PASS','relocatedPackageReopen':'PASS','sourceImagesUnchanged':'PASS','layoutReview':'NOT_TESTED','hostSameCanvas':'NOT_TESTED'}


def verify_toc_entries(entries,chapters,pages):
    require(len(entries)==len(chapters),'Unexpected TOC entry count (body text may use heading style)')
    require([e['text'] for e in entries]==[c['heading'] for c in chapters],'TOC chapter order/text changed')
    require([str(e['page']) for e in entries]==[str(p) for p in pages],'TOC page labels are stale')


def run_long_document(r,skills):
    root=Path(skills)/'designcraft-long-document'
    recipe=json.loads((root/'references/craft-steps.json').read_text(encoding='utf-8'))
    spec=importlib.util.spec_from_file_location('book_compiler',root/'scripts/write_script.py')
    compiler=importlib.util.module_from_spec(spec);spec.loader.exec_module(compiler)
    steps,names=compiler.compile_steps(recipe)
    target='core-book.designcraft';pdf='core-book.pdf';idml='core-book.idml'
    results=run_script(r,steps,save=target,exports=[pdf,idml]);bindings={n:results[i] for n,i in names.items()}
    require(bindings['before_continuation']['overset'] is not None,'Chapter fixture did not exercise continuation')
    verify_toc_entries(bindings['toc_before'],recipe['chapters'],[2,4])
    verify_toc_entries(bindings['toc_final'],recipe['chapters'],[2,5])
    info=json.loads(r.run('run','--in',target,'--cmd','document.inspect'))
    queries=[{'command':'story.get','params':{'frame':bindings[c['key']]['id']}} for c in recipe['chapters']]
    stories=run_script(r,queries,source=target)
    verify(info,stories,bindings,recipe['assertions'])
    for index,(chapter,story) in enumerate(zip(recipe['chapters'],stories)):
        expected=chapter['text']+('\ue00a' if index==1 else '')
        require(story['text']==expected and story['overset'] is None,'Chapter text changed or remains overset')
    notes=run_script(r,[{'command':'footnote.list','params':{'story':bindings['chapter2']['story']}}],source=target)[0]
    require(len(notes)==1 and notes[0]['text']==recipe['note'],'Source footnote text/count changed')
    require(notes[0]['anchor']==len(recipe['chapters'][1]['text'].encode('utf-8')),'Source footnote anchor changed')
    toc_story=run_script(r,[{'command':'story.get','params':{'story':bindings['toc']['story']}}],source=target)[0]
    for chapter,page in zip(recipe['chapters'],[2,5]):
        require(chapter['heading']+'\t'+str(page) in toc_story['text'],'Saved TOC story has stale page label')
    entries=next(s['params'] for s in recipe['steps'] if s.get('capture')=='toc_final')
    reopened_toc=run_script(r,[{'command':'toc.entries','params':entries}],source=target)[0]
    verify_toc_entries(reopened_toc,recipe['chapters'],[2,5])
    preflight=run_script(r,[{'command':'preflight.run','params':{'minPpi':150}}],source=target)[0]
    require(not any(i['severity']=='error' for i in preflight['issues']),'Book preflight errors: '+str(preflight))
    with zipfile.ZipFile(r.work/idml) as archive:
        roots=[ET.fromstring(archive.read(n)) for n in archive.namelist() if n.startswith('Stories/') and n.endswith('.xml')]
        for chapter in recipe['chapters']:
            matches=[x for x in roots if chapter['heading'] in ''.join(e.text or '' for e in x.iter() if e.tag.endswith('Content'))]
            # The TOC also contains the heading: identify the body story through a unique body phrase.
            phrase=chapter['text'].split('\n')[1]
            matches=[x for x in matches if phrase in ''.join(e.text or '' for e in x.iter() if e.tag.endswith('Content'))]
            require(len(matches)==1,'Chapter body story missing or duplicated in IDML')
            xml_story=next(e for e in matches[0].iter() if e.tag=='Story')
            styles=[unquote(e.attrib.get('AppliedParagraphStyle','')).split('/')[-1] for e in xml_story if e.tag=='ParagraphStyleRange']
            require(styles==['Chapter Heading']+['Book Body']*(len(chapter['text'].split('\n'))-1),'Chapter/Body paragraph styles lost or applied to wrong range')
    package=r.work/'book-package';native=list(package.glob('*.designcraft'))
    require(len(native)==1,'Packaged book missing')
    packed_stories=run_script(r,queries,source=str(native[0]))
    require([s['text'] for s in packed_stories]==[s['text'] for s in stories],'Packaged chapter text changed')
    packed_notes=run_script(r,[{'command':'footnote.list','params':{'story':bindings['chapter2']['story']}}],source=str(native[0]))[0]
    require(packed_notes==notes,'Packaged source footnote changed')
    (r.work/'core-book-inspection.json').write_text(json.dumps({'info':info,'stories':stories,'notes':notes,'tocStory':toc_story,'tocBefore':bindings['toc_before'],'tocAfter':reopened_toc,'preflight':preflight,'package':bindings['package']},ensure_ascii=False,indent=2),encoding='utf-8')
    return {'id':'long-document','coreSkill':'designcraft-long-document','technicalRoundtrip':'PASS','fullChapterTextAndThread':'PASS','tocPaginationUpdate':'PASS','nativeFootnoteTextAndAnchor':'PASS','chapterBodyStylesInIdml':'PASS','packagedNativeReopen':'PASS','layoutReview':'NOT_TESTED','hostSameCanvas':'NOT_TESTED'}


def verify_brochure(info,stories,bindings,recipe):
    """核对阅读页序、完整正文和逐SKU图片绑定；不把零退出当交付。"""
    verify(info,stories,bindings,recipe['assertions'])
    story_map={s['frames'][0]:s for s in stories}
    for index,page in enumerate(recipe['pages']):
        page_ids={i['id'] for i in info['spreads'][index]['items']}
        for suffix,expected in [('heading',page['heading']),('copy',page['text']),('footer',f'{index+1} / 4  |  Review copy')]:
            key=page['key']+'_'+suffix;frame=bindings[key]['id']
            require(frame in page_ids,'Brochure text placed on wrong page: '+key)
            require(story_map[frame]['text']==expected,'Brochure full text changed: '+key)
            require(story_map[frame]['overset'] is None,'Brochure remains overset: '+key)
        if page.get('image'):require(bindings[page['key']+'_image']['id'] in page_ids,'Brochure SKU image placed on wrong page')


def run_brochure(r,skills):
    import hashlib
    root=Path(skills)/'designcraft-brochure'
    recipe=json.loads((root/'references/craft-steps.json').read_text(encoding='utf-8'))
    spec=importlib.util.spec_from_file_location('brochure_compiler',root/'scripts/write_script.py')
    compiler=importlib.util.module_from_spec(spec);spec.loader.exec_module(compiler)
    inputs=r.work/'brochure-input';inputs.mkdir()
    catalog_png(inputs/'organiser.png',(25,80,210));catalog_png(inputs/'case.png',(225,110,20))
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs.iterdir()}
    steps,names=compiler.compile_steps(recipe)
    target='core-brochure.designcraft';pdf='core-brochure.pdf';idml='core-brochure.idml'
    results=run_script(r,steps,save=target,exports=[pdf,idml]);bindings={n:results[i] for n,i in names.items()}
    info=json.loads(r.run('run','--in',target,'--cmd','document.inspect'))
    text_steps=[s for s in recipe['steps'] if s['command']=='frame.create' and s['params']['content']=='text']
    queries=[{'command':'story.get','params':{'frame':bindings[s['capture']]['id']}} for s in text_steps]
    stories=run_script(r,queries,source=target)
    verify_brochure(info,stories,bindings,recipe)
    products=[{'key':p['key'],'sku':p['key'],'image':p['image']} for p in recipe['pages'] if p.get('image')]
    links=run_script(r,[{'command':'links.list','params':{}}],source=target)[0]
    verify_catalog_links(links,products,bindings)
    preflight=run_script(r,[{'command':'preflight.run','params':{'minPpi':150}}],source=target)[0]
    require(not preflight['issues'],'Brochure preflight issues: '+str(preflight))
    with zipfile.ZipFile(r.work/idml) as archive:
        xmls=[ET.fromstring(archive.read(n)) for n in archive.namelist() if n.startswith('Stories/') and n.endswith('.xml')]
        for step in text_steps:
            expected=step['params']['text'];found=[xml for xml in xmls if ''.join(e.text or '' for e in xml.iter() if e.tag.endswith('Content'))==expected.replace('\n','')]
            # IDML paragraphs may preserve LF or use individual Content elements.
            if not found:found=[xml for xml in xmls if ''.join(e.text or '' for e in xml.iter() if e.tag.endswith('Content'))==expected]
            require(len(found)==1,'Brochure IDML story missing or duplicated: '+step['capture'])
            suffix=step['capture'].rsplit('_',1)[1];style={'heading':'Brochure Heading','copy':'Brochure Body','footer':'Brochure Footer'}[suffix]
            paragraphs=[e for e in found[0].iter() if e.tag.endswith('ParagraphStyleRange')]
            require(paragraphs and all(unquote(e.attrib.get('AppliedParagraphStyle','')).endswith('/'+style) for e in paragraphs),'Brochure editable style lost: '+step['capture'])
    package_results=run_script(r,recipe['deliverySteps'],source=target)
    bindings['package']=package_results[0]
    package=r.work/'brochure-package';native=list(package.glob('*.designcraft'))
    require(len(native)==1,'Brochure packaged project missing')
    packaged_info=json.loads(r.run('run','--in',str(native[0]),'--cmd','document.inspect'))
    packaged_stories=run_script(r,queries,source=str(native[0]));verify_brochure(packaged_info,packaged_stories,bindings,recipe)
    for name,digest in hashes.items():
        require(hashlib.sha256((inputs/name).read_bytes()).hexdigest()==digest,'Brochure input changed')
        require(hashlib.sha256((package/'Links'/name).read_bytes()).hexdigest()==digest,'Brochure packaged image changed')
    require((r.work/pdf).read_bytes().startswith(b'%PDF'),'Brochure PDF invalid')
    (r.work/'core-brochure-inspection.json').write_text(json.dumps({'info':info,'stories':stories,'bindings':bindings,'links':links,'preflight':preflight,'inputHashes':hashes},ensure_ascii=False,indent=2),encoding='utf-8')
    return {'id':'brochure','coreSkill':'designcraft-brochure','technicalRoundtrip':'PASS','fourPageReadingOrder':'PASS','allTwelveStoriesAndStyles':'PASS','twoProductImageBindings':'PASS','packagedReopen':'PASS','sourceImagesUnchanged':'PASS','layoutReview':'NOT_TESTED','hostSameCanvas':'NOT_TESTED'}
