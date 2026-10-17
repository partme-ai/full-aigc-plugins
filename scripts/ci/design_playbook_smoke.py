"""原生DesignCraft排版步骤往返，检查故事、表格、跨页、溢出和IDML语义。"""
import importlib.util
import json
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
    if a.get('bleedBounds'):require(any(near(i['bounds'],a['bleedBounds']) for i in items),'Background does not reach bleed')


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
    require(bool(records),'No Design workflows');return records
