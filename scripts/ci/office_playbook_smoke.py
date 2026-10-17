"""原生 Office 场景往返：执行技能源同一份步骤，核对计算与可编辑对象，不代替版面审阅。"""
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile

W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
P='http://schemas.openxmlformats.org/presentationml/2006/main'
C='http://schemas.openxmlformats.org/drawingml/2006/chart'


def require(ok, message):
    if not ok:raise AssertionError(message)


def verify_word(z, assertion):
    doc=ET.fromstring(z.read('word/document.xml'))
    text=''.join(doc.itertext())
    for value in assertion.get('textContains',[]):require(value in text,'DOCX text missing: '+value)
    for value in assertion.get('textAbsent',[]):require(value not in text,'DOCX old term remains: '+value)
    if assertion.get('headingRequired'):
        styles=ET.fromstring(z.read('word/styles.xml'))
        heading_ids={s.attrib.get('{'+W+'}styleId') for s in styles.findall('{'+W+'}style')
                     if s.find('{'+W+'}name') is not None and
                     s.find('{'+W+'}name').attrib.get('{'+W+'}val','').lower().replace(' ','')=='heading1'}
        applied={x.attrib.get('{'+W+'}val') for x in doc.findall('.//{'+W+'}pStyle')}
        require(bool(heading_ids&applied),'No applied first-level heading style')
    if 'heading2Minimum' in assertion:
        styles=ET.fromstring(z.read('word/styles.xml'))
        ids={s.attrib.get('{'+W+'}styleId') for s in styles.findall('{'+W+'}style')
             if s.find('{'+W+'}name') is not None and s.find('{'+W+'}name').attrib.get('{'+W+'}val','').lower().replace(' ','')=='heading2'}
        count=sum(x.attrib.get('{'+W+'}val') in ids for x in doc.findall('.//{'+W+'}pStyle'))
        require(count>=assertion['heading2Minimum'],'Document section heading styles missing')
    if 'tableCells' in assertion:
        tables=doc.findall('.//{'+W+'}tbl')
        require(len(tables)==1,'Expected one editable document table')
        rows=[[ ''.join(t.text or '' for t in cell.iter('{'+W+'}t')) for cell in row.findall('{'+W+'}tc')]
              for row in tables[0].findall('{'+W+'}tr')]
        require(rows==assertion['tableCells'],'Document table cell content/columns mismatch')
    if assertion.get('numberingRequired'):
        ids=[x.attrib.get('{'+W+'}val') for x in doc.findall('.//{'+W+'}numPr/{'+W+'}numId')]
        require(any(x not in (None,'0') for x in ids),'Numbered/bulleted paragraphs lost')
    if assertion.get('pageBreakRequired'):
        require(any(x.attrib.get('{'+W+'}type')=='page' for x in doc.findall('.//{'+W+'}br')),'Page break lost')
    if 'tableCount' in assertion:require(len(doc.findall('.//{'+W+'}tbl'))==assertion['tableCount'],'DOCX table count wrong')
    if 'columns' in assertion:
        require(any(x.attrib.get('{'+W+'}num')==str(assertion['columns']) for x in doc.findall('.//{'+W+'}cols')),'Section columns lost')
    for kind in ['header','footer']:
        if kind+'Contains' in assertion:
            texts=''.join(''.join(ET.fromstring(z.read(n)).itertext()) for n in z.namelist() if re.fullmatch('word/'+kind+r'\d+\.xml',n))
            require(assertion[kind+'Contains'] in texts,kind+' text missing')


def verify_deck(z, assertion):
    names=sorted(n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n))
    require(len(names)==assertion['slides'],'PPTX slide count wrong')
    slides=[ET.fromstring(z.read(n)) for n in names]
    text='\n'.join(x.text or '' for slide in slides for x in slide.iter('{'+A+'}t'))
    for value in assertion.get('textContains',[]):require(value in text,'PPTX text missing: '+value)
    notes='\n'.join(x.text or '' for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',n)
                    for x in ET.fromstring(z.read(n)).iter('{'+A+'}t'))
    for value in assertion.get('notesContains',[]):require(value in notes,'Speaker note lost: '+value)
    if 'hiddenSlides' in assertion:
        require(sum(s.attrib.get('show') in ('0','false') for s in slides)==assertion['hiddenSlides'],'Hidden answer slide lost')
    if 'tableCount' in assertion:require(sum(len(s.findall('.//{'+A+'}tbl')) for s in slides)==assertion['tableCount'],'PPTX editable table count wrong')
    if 'shapeMinimum' in assertion:require(sum(len(s.findall('.//{'+P+'}sp')) for s in slides)>=assertion['shapeMinimum'],'Diagram shapes lost')
    charts=[n for n in z.namelist() if re.fullmatch(r'ppt/charts/chart\d+\.xml',n)]
    if 'chartCount' in assertion:require(len(charts)==assertion['chartCount'],'PPTX editable chart count wrong')
    if 'chartValues' in assertion:
        values=[float(x.text) for n in charts for x in ET.fromstring(z.read(n)).findall('.//{'+C+'}numCache/{'+C+'}pt/{'+C+'}v')]
        require(sorted(values)==sorted(assertion['chartValues']),'Chart series data changed')


def verify_grid(r, target, assertion):
    def read(cell,formulas=False):
        params={'range':cell,'formulas':formulas,'formatted':False}
        rows=r.run('run','--in',target,'--cmd','sheet.read='+json.dumps(params,separators=(',',':'))).splitlines()
        result=next(json.loads(row)['result'] for row in rows if json.loads(row).get('command')=='sheet.read')
        return result['values'][0][0]
    for cell, expected in assertion.get('cells',{}).items():
        actual=read(cell)
        require(type(actual) in (int,float),'Computed cell is not a number: '+cell)
        require(math.isclose(actual,expected,rel_tol=1e-8,abs_tol=1e-8),'Computed value mismatch '+cell+': '+str(actual))
    for cell, expected in assertion.get('texts',{}).items():
        require(read(cell)==expected,'Cell text mismatch '+cell)
    for cell, expected in assertion.get('formulas',{}).items():
        require(expected in str(read(cell,formulas=True)),'Formula missing '+cell)
    with zipfile.ZipFile(r.work/target) as z:
        sheet=z.read('xl/worksheets/sheet1.xml').decode('utf-8')
        for value in assertion.get('xmlContains',[]):require(value in sheet,'Worksheet rule/structure lost: '+value)
        for prefix,key in [('xl/charts/chart','chartCount'),('xl/tables/table','tableCount')]:
            if key in assertion:require(sum(bool(re.fullmatch(re.escape(prefix)+r'\d+\.xml',n)) for n in z.namelist())==assertion[key],key+' mismatch')


def source_skills(path, data):
    """显式路径相对于配方文件，旧的技能内布局保持原语义。"""
    recipe=Path(path).resolve()
    return (recipe.parent/data['sourceSkills']).resolve() if data.get('sourceSkills') else recipe.parents[2]


def run_playbooks(r,path,app):
    data=json.loads(Path(path).read_text(encoding='utf-8'));require(data['application']==app,'Wrong scenario application')
    records=[]
    for recipe in data['recipes']:
        extension={'gridcraft':'xlsx','wordcraft':'docx','deckcraft':'deckcraft'}[app]
        target=recipe['id']+'.'+extension
        args=['run']
        for step in recipe['steps']:args += ['--cmd',step['command']+'='+json.dumps(step['params'],ensure_ascii=False,separators=(',',':'))]
        args += ['--out' if app=='gridcraft' else '--save',target]
        if app=='gridcraft':args+=['--quiet']
        r.run(*args)
        assertion=recipe['assertions']
        if app=='gridcraft':verify_grid(r,target,assertion)
        elif app=='wordcraft':
            text=r.run('text',target)
            for expected in assertion.get('textContains',[]):require(expected in text,'Native reopened text missing')
            with zipfile.ZipFile(r.work/target) as z:verify_word(z,assertion)
            r.run('convert',target,recipe['id']+'.pdf')
            require((r.work/(recipe['id']+'.pdf')).read_bytes().startswith(b'%PDF'),'PDF export invalid')
        else:
            r.run('info',target)
            pptx=recipe['id']+'.pptx';r.run('convert',target,pptx)
            with zipfile.ZipFile(r.work/pptx) as z:verify_deck(z,assertion)
        records.append({'id':recipe['id'],'technicalRoundtrip':'PASS','semanticChecks':'PASS','layoutAcceptance':'NOT_TESTED'})
    require(bool(records),'No Office scenarios selected')
    if app=='gridcraft':
        from grid_core_smoke import run_playbooks as run_core
        records.extend(run_core(r, source_skills(path,data)))
        from grid_templates_smoke import run_templates
        records.extend(run_templates(r, source_skills(path,data)))
    if app=='wordcraft':
        from word_core_smoke import run_playbooks as run_core
        records.extend(run_core(r, source_skills(path,data)))
        from word_publishing_smoke import run_playbooks as run_publishing
        records.extend(run_publishing(r, source_skills(path,data)))
    if app=='deckcraft':
        from deck_comparison_smoke import run_comparison
        records.append(run_comparison(r, source_skills(path,data)))
        from deck_core_smoke import run_core
        records.extend(run_core(r, source_skills(path,data)))
        # 真实组合两条手册，防止后一个file.new清空已有页。
        combined=[next(x for x in data['recipes'] if x['id']==id) for id in ['option-comparison-table','trend-actual-plan']]
        args=['run']; initialized=False
        for recipe in combined:
            for step in recipe['steps']:
                if step.get('newDocumentOnly'):
                    if initialized:continue
                    initialized=True
                args+=['--cmd',step['command']+'='+json.dumps(step['params'],ensure_ascii=False,separators=(',',':'))]
        r.run(*args,'--save','combined-decision.deckcraft')
        r.run('info','combined-decision.deckcraft')
        r.run('convert','combined-decision.deckcraft','combined-decision.pptx')
        with zipfile.ZipFile(r.work/'combined-decision.pptx') as z:
            verify_deck(z,{'slides':2,'textContains':['方案比较','实际与计划'],
                           'tableCount':1,'chartCount':1,'chartValues':[80,95,110,90,100,105],
                           'notesContains':['最终选择由决策人确认','三个月趋势不支持全年预测']})
        records.append({'id':'combined-comparison-trend','technicalRoundtrip':'PASS','semanticChecks':'PASS','layoutAcceptance':'NOT_TESTED'})
    return records
