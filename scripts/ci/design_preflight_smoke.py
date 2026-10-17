"""用原生缺链/低PPI/溢出样例验证印前修复，分段检查后才导出。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile
from design_playbook_smoke import run_script,require,near
from design_core_smoke import catalog_png


def verify_repaired(before,after):
    require({'missingLink','lowResolution','overset'} <= {i['kind'] for i in before['issues']},'Fixture did not expose all target defects')
    require(not any(i['severity']=='error' or i['kind'] in {'missingLink','lowResolution','overset'} for i in after['issues']),'Unresolved print issues; export must stop')


def run_preflight(r,skills):
    root=Path(skills)/'designcraft-print-preflight';recipe=json.loads((root/'references/craft-steps.json').read_text(encoding='utf-8'))
    spec=importlib.util.spec_from_file_location('preflight_compiler',root/'scripts/write_script.py');compiler=importlib.util.module_from_spec(spec);spec.loader.exec_module(compiler)
    inputs=r.work/'preflight-input';inputs.mkdir()
    for name,color,scale in [('blue-low.png',(20,75,210),1),('missing-low.png',(210,110,20),1),('blue-high.png',(20,75,210),2),('orange-high.png',(210,110,20),2)]:catalog_png(inputs/name,color,scale)
    image_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs.iterdir()}
    text=' '.join(['Preflight review preserves the complete approved message and its original type size.','Image changes require a confirmed source with enough genuine detail.','A missing linked file must be recovered before final delivery, even when its cached preview still renders.','After checking the page boundaries and nearby content, the editor may enlarge this frame without scaling the text.','Recheck at the same effective resolution threshold and retain all unresolved warnings for review.'])
    footer='APPROVED FOOTER - KEEP CONTENT AND POSITION'
    seed=[{'command':'file.new','params':{'width':595,'height':842,'pages':1,'facingPages':False,'bleed':0,'title':'Preflight fixture'}},
          {'command':'frame.create','params':{'rect':[42,60,286,230],'content':'graphic'}},
          {'command':'file.place','params':{'frame':'$1.id','path':'preflight-input/blue-low.png','link':True}},
          {'command':'frame.create','params':{'rect':[309,60,553,230],'content':'graphic'}},
          {'command':'file.place','params':{'frame':'$3.id','path':'preflight-input/missing-low.png','link':True}},
          {'command':'frame.create','params':{'rect':[42,300,553,324],'content':'text','text':text}},
          {'command':'text.select','params':{'story':'$5.story','anchor':0,'focus':len(text.encode())}},
          {'command':'type.char','params':{'attrs':{'fontFamily':'Source Sans 3','size':11}}},
          {'command':'frame.create','params':{'rect':[42,740,553,790],'content':'text','text':footer}},
          {'command':'text.select','params':{'story':'$8.story','anchor':0,'focus':len(footer.encode())}},
          {'command':'type.char','params':{'attrs':{'fontFamily':'Source Sans 3','size':11}}}]
    source='preflight-original.designcraft';created=run_script(r,seed,save=source);source_hash=hashlib.sha256((r.work/source).read_bytes()).hexdigest()
    links=run_script(r,[{'command':'links.list','params':{}}],source=source)[0]
    low=next(x['asset'] for x in links if Path(x['path']).name=='blue-low.png');missing=next(x['asset'] for x in links if Path(x['path']).name=='missing-low.png')
    absent=inputs/'missing-low.png';offline=inputs/'missing-low.offline';absent.rename(offline)
    try:
        compiled,names=compiler.compile_steps(recipe,phase='inspect');out=run_script(r,compiled,source=source);before={n:out[i] for n,i in names.items()}
        bindings={'lowResolutionAsset':low,'lowResolutionReplacement':'preflight-input/blue-high.png','missingAsset':missing,'missingReplacement':'preflight-input/orange-high.png','oversetFrame':created[5]['id'],'oldTextBounds':[42,300,553,324],'approvedTextBounds':[42,300,553,700],'bleedPoints':9}
        compiled,names=compiler.compile_steps(recipe,inputs=bindings,phase='repair');target='preflight-fixed.designcraft';out=run_script(r,compiled,source=source,save=target);fixed={n:out[i] for n,i in names.items()}
        verify_repaired(before['before_preflight'],fixed['final_preflight'])
        require(fixed['fixed_story']['text']==text and fixed['fixed_story']['overset'] is None,'Repair lost or still hides text')
        require(all(link['status']=='ok' and all(u['ppi']>=300 for u in link['uses']) for link in fixed['final_links']),'Repair did not restore full-resolution linked images')
        info=json.loads(r.run('run','--in',target,'--cmd','document.inspect'))
        require(info['pageCount']==1 and near([info['settings']['pageWidth'],info['settings']['pageHeight']],[595,842]),'Repair changed trim dimensions or page count')
        items=[i for spread in info['spreads'] for i in spread['items']];old_items=[i for spread in before['before_inspect']['spreads'] for i in spread['items']]
        require(next(i for i in items if i['id']==created[8]['id'])==next(i for i in old_items if i['id']==created[8]['id']),'Unrelated footer object changed')
        kept=run_script(r,[{'command':'story.get','params':{'frame':created[8]['id']}}],source=target)[0];require(kept['text']==footer,'Unrelated footer text changed')
        # Export is a separate native process, reached only after the report is checked.
        compiled,names=compiler.compile_steps(recipe,phase='export');out=run_script(r,compiled,source=target);export={n:out[i] for n,i in names.items()}
        r.run('run','--in',target,'--export','preflight-fixed.idml')
        with zipfile.ZipFile(r.work/'preflight-fixed.idml') as archive:
            sizes=[]
            for name in archive.namelist():
                if name.startswith('Stories/') and name.endswith('.xml'):
                    sizes += [float(e.attrib['PointSize']) for e in ET.fromstring(archive.read(name)).iter() if 'PointSize' in e.attrib]
            require(sizes and all(n==11 for n in sizes),'Repair scaled or changed text size')
        require(hashlib.sha256((r.work/source).read_bytes()).hexdigest()==source_hash,'Original project changed')
        require(hashlib.sha256(offline.read_bytes()).hexdigest()==image_hashes['missing-low.png'],'Missing source fixture bytes changed')
        require(all(hashlib.sha256((inputs/n).read_bytes()).hexdigest()==h for n,h in image_hashes.items() if n!='missing-low.png'),'Input image bytes changed')
        (r.work/'core-preflight-inspection.json').write_text(json.dumps({'before':before,'fixed':fixed,'export':export,'info':info,'inputBindings':bindings,'sourceSha256':source_hash},ensure_ascii=False,indent=2),encoding='utf-8')
    finally:offline.rename(absent)
    return {'id':'print-preflight','coreSkill':'designcraft-print-preflight','technicalRoundtrip':'PASS','threeRealDefectsDetectedAndRepaired':'PASS','samePpiThreshold':'PASS','sourceUnchanged':'PASS','unrelatedFooterAndTextSizePreserved':'PASS','phaseGateBeforeExport':'PASS','pdfXOrPrintCertification':'NOT_TESTED','layoutReview':'NOT_TESTED','hostSameCanvas':'NOT_TESTED'}
