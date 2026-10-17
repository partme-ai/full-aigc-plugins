"""逐项执行独立PDF交付配方，不借用SDK代替原生CLI。"""
import hashlib
import importlib.util
import json
from pathlib import Path
from craft_cli_windows import require
from pdf_playbook_smoke import write_pdf,json_values,verify_page_order

SCENES=['report-bookmarks','review-watermark','invoice-split','section-pagination','linked-agenda','revision-compare']


def fixture(path,pages):
    """原创纯文本夹具，不依赖外部有版权PDF。"""
    count=len(pages);font=3+2*count
    objects=[b'<< /Type /Catalog /Pages 2 0 R >>',f'<< /Type /Pages /Kids [{" ".join(str(3+2*i)+" 0 R" for i in range(count))}] /Count {count} >>'.encode()]
    for i,lines in enumerate(pages):
        page=3+2*i;objects.append(f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 200] /Resources << /Font << /F1 {font} 0 R >> >> /Contents {page+1} 0 R >>'.encode())
        content=('BT /F1 12 Tf 20 170 Td '+ ' 0 -30 Td '.join('('+line.replace('\\','\\\\').replace('(','\\(').replace(')','\\)')+') Tj' for line in lines)+' ET\n').encode('ascii')
        objects.append(f'<< /Length {len(content)} >>\nstream\n'.encode()+content+b'endstream')
    objects.append(b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>');write_pdf(path,objects)


def execute(r,skill,recipe):
    spec=importlib.util.spec_from_file_location('pdf_'+recipe['id'].replace('-','_'),skill/'scripts/write_script.py');compiler=importlib.util.module_from_spec(spec);spec.loader.exec_module(compiler)
    steps=compiler.compile_steps(recipe,preopen=['decoy.pdf']);path=r.work/'steps.json';path.write_text(json.dumps(steps,ensure_ascii=False,indent=2),encoding='utf-8')
    rows=json_values(r.run('run','--script',str(path),'--root',str(r.work)))
    opens=len(recipe['sourceFiles'])+1
    require([row['doc'] for row in rows[:opens]]==list(range(1,opens+1)),'Fresh CLI open-order IDs differ from declared script slots')
    require(len(rows)==len(steps),'PDF delivery tool count mismatch')
    return rows[opens:]


def query(r,path,tool,**args):
    p=r.work/'reopen.json';p.write_text(json.dumps([{'tool':'doc_open','args':{'path':path}},{'tool':tool,'args':{'doc':1,**args}}]),encoding='utf-8')
    return json_values(r.run('run','--script',str(p),'--root',str(r.work)))[-1]


def verify_navigation(bookmarks):
    # Native bookmark_list returns a nested list; reject wrong targets rather than counting entries only.
    expected=[{'title':'Report','page':1,'children':[{'title':'Findings','page':2,'children':[]}]},{'title':'Appendix','page':3,'children':[]}]
    def slim(items):return [{'title':x['title'],'page':x.get('page'),'children':slim(x.get('children',[]))} for x in items]
    actual=bookmarks.get('bookmarks',bookmarks) if isinstance(bookmarks,dict) else bookmarks
    require(slim(actual)==expected,'Report bookmark hierarchy or destination changed')


def verify_agenda_links(report,finds):
    require(report['count']==2 and len(report['links'])==2,'Agenda link count changed')
    by_page={link['page']:link for link in report['links']}
    require({page:link.get('to_page') for page,link in by_page.items()}=={1:3,3:1},'Agenda link destination wrong')
    for find in finds:
        require(find['complete'] and find['count']==1 and len(find['matches'])==1,'Agenda label is missing or ambiguous')
        match=find['matches'][0];box=by_page[match['page']]['rect']
        for rect in match['rects']:
            require(box[0]<=rect[0] and box[1]<=rect[1] and box[2]>=rect[2] and box[3]>=rect[3],'Agenda hotspot misses label')


def verify_revision(report):
    require(not report['identical'] and report['replaced']==1 and report['inserted']==0 and report['deleted']==0,'Revision change count wrong')
    require(len(report['changes'])==1 and report['changes'][0]['old']['text']=='100' and report['changes'][0]['new']['text']=='120','Revision old/new direction wrong')
    require(report['changes'][0]['old']['page']==1 and report['changes'][0]['new']['page']==1,'Unchanged appendix incorrectly reported')


def run_recipe(r,skill):
    recipe=json.loads((skill/'references/craft-steps.json').read_text(encoding='utf-8'));name=recipe['id'];(r.work/'output').mkdir()
    pages=[['PAGE ONE','PUBLIC KEEP'],['PAGE TWO','PUBLIC KEEP'],['PAGE THREE','PUBLIC KEEP']]
    if name=='report-bookmarks':pages=[['REPORT','PUBLIC KEEP'],['FINDINGS','PUBLIC KEEP'],['APPENDIX','PUBLIC KEEP']]
    if name=='invoice-split':pages=[[label,'ORIGINAL RECORD'] for label in ['INVOICE-A / 1 OF 2','INVOICE-A / 2 OF 2','INVOICE-B / 1 OF 1','INVOICE-C / 1 OF 3','INVOICE-C / 2 OF 3','INVOICE-C / 3 OF 3']]
    if name=='section-pagination':pages=[[label,'PUBLIC KEEP'] for label in ['PREFACE','BODY ONE','BODY TWO','BODY THREE']]
    if name=='linked-agenda':pages=[['Meeting agenda','Open appendix','PUBLIC KEEP'],['Budget notes','PUBLIC KEEP'],['Appendix: sources','PUBLIC KEEP','Back to agenda']]
    fixture(r.work/'decoy.pdf',[['DECOY / DO NOT MODIFY']]);fixture(r.work/'input.pdf',pages)
    if name=='revision-compare':
        fixture(r.work/'newer.pdf',[['REPORT','Amount: 120'],['Unchanged appendix','PUBLIC KEEP']]);fixture(r.work/'older.pdf',[['REPORT','Amount: 100'],['Unchanged appendix','PUBLIC KEEP']])
    originals={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in r.work.glob('*.pdf')};baseline=r.run('text','input.pdf');rows=execute(r,skill,recipe)
    (r.work/'results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    result={'id':name,'technicalRoundtrip':'PASS','sourceUnchanged':'PASS','hostEditorSync':'NOT_TESTED','realDocumentQuality':'NOT_TESTED'}
    if name=='report-bookmarks':
        bookmarks=query(r,'output/navigable-report.pdf','bookmark_list');verify_navigation(bookmarks);require(r.run('text','output/navigable-report.pdf')==baseline,'Bookmarks changed report content')
    elif name=='review-watermark':
        text=r.run('text','output/review-copy.pdf').split('\f');text=[p for p in text if p.strip()]
        require(len(text)==3 and ['REVIEW ONLY' in p for p in text]==[True,False,True],'Watermark scope differs from selected pages')
        for i,label in enumerate(['PAGE ONE','PAGE TWO','PAGE THREE']):require(label in text[i] and 'PUBLIC KEEP' in text[i],'Watermark removed source text')
        r.run('render','input.pdf','--page','2','--dpi','72','--out','untouched-before.png');r.run('render','output/review-copy.pdf','--page','2','--dpi','72','--out','untouched-after.png')
        from photo_playbook_smoke import rgb_pixels
        require(rgb_pixels(r.work/'untouched-before.png')==rgb_pixels(r.work/'untouched-after.png'),'Unselected page pixels changed')
    elif name=='invoice-split':
        files=sorted((r.work/'output/invoices').glob('*.pdf'));require(len(files)==3,'Expected three invoice documents')
        expected=[['INVOICE-A / 1 OF 2','INVOICE-A / 2 OF 2'],['INVOICE-B / 1 OF 1'],['INVOICE-C / 1 OF 3','INVOICE-C / 2 OF 3','INVOICE-C / 3 OF 3']]
        for file,labels in zip(files,expected):verify_page_order(r.run('text',str(file.relative_to(r.work))),labels)
    elif name=='section-pagination':
        text=[p for p in r.run('text','output/numbered-report.pdf').split('\f') if p.strip()];require(len(text)==4,'Pagination page count wrong')
        for i,phrase in enumerate(['i','Page 1 of 3','Page 2 of 3','Page 3 of 3']):require(phrase in text[i] and pages[i][0] in text[i],'Visible pagination or original body missing')
        require(all('Page ' not in text[0] and phrase not in text[0] for phrase in ['Page 1 of 3','Page 2 of 3','Page 3 of 3']),'Preface received body page numbering')
    elif name=='linked-agenda':
        queries=query(r,'output/linked-agenda.pdf','link_list')
        verify_agenda_links(queries,[rows[1],rows[3]])
        (r.work/'reopened-links.json').write_text(json.dumps(queries,indent=2),encoding='utf-8');require(r.run('text','output/linked-agenda.pdf')==baseline,'Agenda text changed')
    elif name=='revision-compare':
        compare=rows[2];verify_revision(compare);report=r.run('text','output/revision-report.pdf');require('100' in report and '120' in report,'Revision report lost old or new amount');require('100' in json.dumps(compare) and '120' in json.dumps(compare),'Comparison direction or changed text missing')
        result['visualComparison']='NOT_TESTED'
    require(all(hashlib.sha256((r.work/name).read_bytes()).hexdigest()==digest for name,digest in originals.items()),'PDF delivery modified an original')
    return result


def run_delivery(r,skills):
    original=r.work;records=[]
    try:
        for name in SCENES:
            r.work=original/('delivery-'+name);r.work.mkdir();records.append(run_recipe(r,Path(skills)/('printcraft-'+name)))
    finally:r.work=original
    return records
