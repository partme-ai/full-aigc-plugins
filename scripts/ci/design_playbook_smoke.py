"""原生DesignCraft排版步骤往返，检查故事、表格、跨页、溢出和IDML语义。"""
import importlib.util
import json
import copy
import hashlib
import math
from pathlib import Path
from urllib.parse import unquote
import xml.etree.ElementTree as ET
import zipfile


def require(ok,message):
    if not ok:raise AssertionError(message)


def near(a,b):return len(a)==len(b) and all(math.isclose(x,y,abs_tol=1e-5) for x,y in zip(a,b))


def verify(info,stories,bindings,a):
    require(info['pageCount']==a['pages'],'Page count changed')
    require(near([info['settings']['pageWidth'],info['settings']['pageHeight']],a['size']),'Page dimensions changed')
    items=[i for sp in info['spreads'] for i in sp['items']]
    require(len(items)==a['frameCount'],'Frame count changed')
    require(not any(s['overset'] for s in info['stories']),'Final text remains overset')
    text='\n'.join(s['text'] for s in stories)
    for phrase in a.get('texts',[]):require(phrase in text,'Reopened story text missing: '+phrase)
    for phrase in a.get('absent',[]):require(phrase not in text,'Old brand text remains')
    if 'thread' in a:
        first,second=a['thread'];ids=[bindings[first]['id'],bindings[second]['id']]
        require(any(s['frames']==ids for s in info['stories']),'Columns are not one threaded story in order')
    for index,phrase in a.get('pageTexts',{}).items():
        ids={i['id'] for i in info['spreads'][int(index)]['items']}
        require(any(s['frames'][0] in ids and phrase in s['text'] for s in stories),'Text assigned to wrong spread')
    if a.get('repairedBounds'):
        item=next(i for i in items if i['id']==bindings['copy']['id']);require(near(item['bounds'],a['repairedBounds']),'Repair frame geometry changed')
    if a.get('bleedBounds'):
        require(any(near(i['bounds'],a['bleedBounds']) for i in items),'Background does not reach bleed')
        if a.get('bleedNoStroke'):require(next(i for i in items if i['id']==bindings['bar']['id'])['stroke']['weight']==0,'Bleed background retains border')


def verify_table(table,a):
    require(len(table['rows'])==a['rows'] and len(table['columns'])==a['columns'],'Table dimensions wrong')
    require(table['headerRows']==a['headerRows'],'Table header lost')
    require([c['text'] for c in table['cells']]==a['cells'],'Table editable cell text changed')


def idml_check(path,a):
    with zipfile.ZipFile(path) as z:
        stories=[ET.fromstring(z.read(n)) for n in z.namelist() if n.startswith('Stories/') and n.endswith('.xml')]
        if a.get('paragraphStyle'):
            require(any(unquote(e.attrib.get('AppliedParagraphStyle','')).endswith('/'+a['paragraphStyle']) for story in stories for e in story.iter()),'Applied paragraph style lost')
        if a.get('oversetRepair'):
            sizes=[float(e.attrib['PointSize']) for story in stories for e in story.iter() if 'PointSize' in e.attrib]
            require(sizes and all(math.isclose(n,14) for n in sizes),'Overset fix scaled or changed text size')
        if a.get('bleedPdf'):
            xml=ET.fromstring(z.read('Resources/Preferences.xml'))
            attrs=next(e.attrib for e in xml.iter() if e.tag.endswith('DocumentPreference'))
            for name in ['DocumentBleedTopOffset','DocumentBleedBottomOffset','DocumentBleedInsideOrLeftOffset','DocumentBleedOutsideOrRightOffset']:
                require(math.isclose(float(attrs[name]),9),'Document bleed lost')


def run_script(r,steps,source=None,save=None,exports=()):
    script=r.work/'steps.json';script.write_text(json.dumps(steps,ensure_ascii=False),encoding='utf-8')
    args=['script',str(script)]+(['--in',source] if source else [])+(['--save',save] if save else [])
    for path in exports:args+=['--export',path]
    report=json.loads(r.run(*args));require(report.get('failed') is None and report['completed']==len(steps),'Native script incomplete')
    return report['results']


def run_playbooks(r,path):
    path=Path(path);data=json.loads(path.read_text(encoding='utf-8'));require(data['application']=='designcraft','Wrong app')
    spec=importlib.util.spec_from_file_location('design_compiler',path.parent.parent/'scripts/write_script.py');compiler=importlib.util.module_from_spec(spec);spec.loader.exec_module(compiler)
    records=[]
    for recipe in data['recipes']:
        compiled,names=compiler.compile_steps(recipe);target=recipe['id']+'.designcraft';pdf=recipe['id']+'.pdf';idml=recipe['id']+'.idml'
        results=run_script(r,compiled,save=target,exports=[pdf,idml]);bindings={n:results[i] for n,i in names.items()}
        info=json.loads(r.run('run','--in',target,'--cmd','document.inspect'))
        frame_results=[bindings[n] for n,i in names.items() if compiled[i]['command']=='frame.create' and 'story' in bindings[n]]
        queries=[{'command':'story.get','params':{'frame':x['id']}} for x in frame_results]
        stories=run_script(r,queries,source=target);a=recipe['assertions'];verify(info,stories,bindings,a)
        # Query the native model's complete story, not only a preview or a known phrase.
        by_frame={value['id']:story for value,story in zip(frame_results,stories)}
        for name,index in names.items():
            step=compiled[index]
            if step['command']!='frame.create' or not step['params'].get('text'):continue
            if a.get('table') and name=='grid':continue  # cell contents checked through table.get
            expected=step['params']['text']
            if 'replacementCount' in a:expected=expected.replace('ACME','Craft Studio')
            require(by_frame[bindings[name]['id']]['text']==expected,'Full story text changed or was truncated: '+name)
        preflight=run_script(r,[{'command':'preflight.run','params':{}}],source=target)[0]
        require(not any(i['severity']=='error' for i in preflight['issues']),'Preflight reports errors: '+str(preflight['issues']))
        if a.get('oversetRepair'):require(any(s['overset'] for s in bindings['before_repair']['stories']),'Test input was never overset')
        if 'replacementCount' in a:require(bindings['replacement']['count']==a['replacementCount'],'Replacement scope/count wrong')
        if 'table' in a:
            table=run_script(r,[{'command':'table.get','params':{'story':bindings['grid']['story'],'table':bindings['table']['table']}}],source=target)[0];verify_table(table,a['table'])
        if a.get('hyperlink'):
            links=run_script(r,[{'command':'hyperlink.list','params':{}}],source=target)[0]
            require(a['hyperlink'] in json.dumps(links),'Hyperlink destination lost')
        idml_check(r.work/idml,a);require((r.work/pdf).read_bytes().startswith(b'%PDF'),'PDF invalid')
        (r.work/(recipe['id']+'-inspection.json')).write_text(json.dumps({'info':info,'stories':stories,'preflight':preflight},ensure_ascii=False,indent=2),encoding='utf-8')
        records.append({'id':recipe['id'],'technicalRoundtrip':'PASS','editableSemantics':'PASS','finalPreflight':'PASS','layoutReview':'NOT_TESTED'})
    require(bool(records),'No Design workflows')
    records.append(existing_story_revision(r,compiler,data))
    from design_core_smoke import run_newsletter,run_catalog,run_long_document,run_brochure
    records.append(run_newsletter(r,path.parents[2]))
    records.append(run_catalog(r,path.parents[2]))
    records.append(run_long_document(r,path.parents[2]))
    records.append(run_brochure(r,path.parents[2]))
    from design_poster_smoke import run_poster
    records.append(run_poster(r,path.parents[2]))
    from design_preflight_smoke import run_preflight
    records.append(run_preflight(r,path.parents[2]))
    records.append(run_badge_merge(r,path))
    return records


def existing_story_revision(r,compiler,data):
    original='ACME USER NOTE - DO NOT CHANGE'
    results=run_script(r,[{'command':'file.new','params':{'width':595,'height':842,'facingPages':False}}, {'command':'frame.create','params':{'rect':[42,42,553,120],'content':'text','text':original}}],save='existing-user.designcraft')
    source=r.work/'existing-user.designcraft';digest=hashlib.sha256(source.read_bytes()).hexdigest();old=results[1]
    before=run_script(r,[{'command':'story.get','params':{'frame':old['id']}}],source=str(source))[0]
    recipe=copy.deepcopy(next(x for x in data['recipes'] if x['id']=='brand-copy-revision'))
    next(x for x in recipe['steps'] if x.get('capture')=='copy')['params']['rect']=[42,300,553,650]
    steps,names=compiler.compile_steps(recipe,existing=True)
    require(not any(s['command']=='file.new' for s in steps),'Existing source was initialized')
    target='existing-revised.designcraft';results=run_script(r,steps,source=str(source),save=target,exports=['existing-revised.pdf'])
    after=run_script(r,[{'command':'story.get','params':{'frame':old['id']}}],source=target)[0]
    require(before==after and after['text']==original,'Non-target story changed')
    new_id=results[names['copy']]['id'];new_story=run_script(r,[{'command':'story.get','params':{'frame':new_id}}],source=target)[0]
    require('ACME' not in new_story['text'] and new_story['text'].count('Craft Studio')==2,'Target replacement did not stay scoped')
    require(hashlib.sha256(source.read_bytes()).hexdigest()==digest,'Original input changed')
    return {'id':'existing-story-scope-preservation','technicalRoundtrip':'PASS','originalStoryUnchanged':'PASS','sourceUnchanged':'PASS','nativeReferenceReindexing':'PASS','layoutReview':'NOT_TESTED'}


def run_badge_merge(r,path):
    """独立Python入口调用原生CLI，核对多语言、长姓名、缺字与拒绝覆盖。"""
    import subprocess
    import os
    import sys
    entry=Path(path).resolve().parents[2]/'designcraft-data-merge-badges/scripts/build_badges.py'
    root=r.work/'中文 胸牌';root.mkdir();font=root/'fonts'
    fetched=subprocess.run([sys.executable,str(entry.with_name('fetch_font.py')),'--directory',str(font.resolve())],capture_output=True,timeout=240)
    require(fetched.returncode==0,fetched.stderr.decode('utf-8',errors='replace'));font_file=json.loads(fetched.stdout)['fontFile']
    receipts=[]
    for name,text,use_font,should_pass in [
        ('bilingual','Name,Role\nGuest A,Speaker\n"Guest, B",Visitor\n访客丙,演讲者\n',True,True),
        ('long','Name,Role\nA long conference participant name for review only,Speaker\n',False,True),
        ('missing-glyph','Name,Role\nGuest '+chr(0x10ffff)+',Visitor\n',False,False),
        ('extreme','Name,Role\n'+('Long name '*60)+',Speaker\n',False,False)]:
        csv_file=root/(name+'.csv');csv_file.write_text(text,encoding='utf-8-sig');before=csv_file.read_bytes();out=root/name
        argv=[sys.executable,str(entry),'--cli',str(Path(r.exe).resolve()),'--csv',str(csv_file.resolve()),'--output-dir',str(out.resolve())]+(['--font-file',font_file] if use_font else [])
        p=subprocess.run(argv,env={**os.environ,'PYTHONIOENCODING':'ascii'},capture_output=True,timeout=240)
        (root/(name+'-stdout.json')).write_bytes(p.stdout);(root/(name+'-stderr.txt')).write_bytes(p.stderr)
        require(csv_file.read_bytes()==before,'CSV source changed')
        if should_pass:
            require(p.returncode==0,p.stderr.decode('utf-8',errors='replace'));receipt=json.loads(p.stdout.decode('ascii'))
            require(receipt['result']=='PASS' and receipt['preflight']=='PASS','Missing native preflight')
            require(Path(receipt['output']).resolve()==(out/'badges.designcraft').resolve(),'Chinese output path changed')
            require(receipt['records']==(3 if name=='bilingual' else 1),'Record count changed')
            if name=='long':require(receipt['nameSize']<22,'Long input never exercised font reduction')
            native=run_script(r,[{'command':'document.inspect','params':{}},{'command':'preflight.run','params':{}}],source=out/'badges.designcraft')
            require(native[0]['pageCount']==receipt['records'] and not native[1]['errors'],'Independent native reopen failed')
            for image in (out/'pages').glob('*.png'):require(image.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'),'Invalid PNG page')
            rejected=subprocess.run(argv,capture_output=True,timeout=60);require(rejected.returncode!=0,'Existing output overwritten')
            receipts.append({'variant':name,'result':'PASS','records':receipt['records'],'nameSize':receipt['nameSize'],'nativeProcessesInChild':receipt['nativeProcesses']})
        else:
            require(p.returncode!=0,'Invalid output accepted')
            expected=b'missing glyphs' if name=='missing-glyph' else b'text remains overset at14pt'
            require(expected in p.stderr,'Wrong failure reason')
            require(not (out/'badges.designcraft').exists(),'Unqualified merged file published')
            receipts.append({'variant':name,'rejectedWithExpectedReason':'PASS'})
    return {'id':'data-merge-badges','variants':receipts,'technicalRoundtrip':'PASS','scope':'actual standalone native entry; nested CLI counts in receipts, not direct Runner count; host sync NOT_TESTED'}
