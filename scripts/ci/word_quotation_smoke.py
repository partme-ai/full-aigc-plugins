"""使用技能原脚本和真实WordCraft CLI验证报价金额、DOCX表格与导出。"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import zipfile
import xml.etree.ElementTree as ET
from craft_cli_windows import Runner,require

W={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def run_quotes(r, source):
    home=Path(source)/'skills/wordcraft-quotation'
    spec=importlib.util.spec_from_file_location('quotation_skill',home/'scripts/quotation.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    sample=json.loads((home/'assets/example-input.json').read_text(encoding='utf-8'))
    fractional=copy.deepcopy(sample);fractional['items']=[{'description':'小额项目','quantity':3,'unit_price':'0.10'}];fractional['expected_total']='0.30'
    many=copy.deepcopy(sample);many['items']=[{'description':f'第{i+1}项：按双方确认范围交付的设计服务及其对应可编辑文件','quantity':1,'unit_price':'10.25'} for i in range(20)];many['expected_total']='205.00'
    commands=json.loads(r.run('commands','--json'));known={v['id'] for v in commands};results=[]
    for name,data,total in [('sample',sample,'2740.80'),('small-decimal',fractional,'0.30'),('many-items',many,'205.00')]:
        root=r.work/name;root.mkdir();input_path=root/'input.json';input_path.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8');before=hashlib.sha256(input_path.read_bytes()).hexdigest()
        plan=module.compile_quote(data);require(plan['total']==total,'Business total mismatch')
        require({s['command'] for s in plan['steps']}<=known,'Generated command missing from real runtime')
        (root/'steps.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
        args=['run']
        for step in plan['steps']:args+=['--cmd',step['command']+'='+json.dumps(step['params'],ensure_ascii=False,separators=(',',':'))]
        doc=root/'quotation.docx';pdf=root/'quotation.pdf'
        r.run(*args,'--save',str(doc));r.run('convert',str(doc),str(pdf))
        info=json.loads(r.run('info',str(doc)))
        with zipfile.ZipFile(doc) as archive:xml=ET.fromstring(archive.read('word/document.xml'))
        tables=xml.findall('.//w:tbl',W);require(len(tables)==1,'Expected one editable native table')
        rows=[[''.join(t.text or '' for t in c.findall('.//w:t',W)) for c in row.findall('w:tc',W)] for row in tables[0].findall('w:tr',W)]
        expected=[['项目','数量','单价','金额']]
        # 独立已知金额而非以编译器的steps作为期望。
        if name=='sample':expected += [['主视觉设计','2','1250.10','2500.20'],['尺寸适配','3','80.20','240.60']]
        elif name=='small-decimal':expected += [['小额项目','3','0.10','0.30']]
        else:expected += [[item['description'],'1','10.25','10.25'] for item in data['items']]
        expected += [['合计（CNY）','','',total]]
        require(rows==expected,'Reopened native cells, line amounts or total differ')
        native_rows=tables[0].findall('w:tr',W)
        require(all(row.find('w:trPr/w:cantSplit',W) is not None for row in native_rows),'A quotation row can split across pages')
        widths=[int(column.attrib['{'+W['w']+'}w']) for column in tables[0].findall('w:tblGrid/w:gridCol',W)]
        require(widths==[5000,900,1500,1620],'Quotation column widths lost')
        for row in native_rows:
            for cell in row.findall('w:tc',W)[1:]:
                align=cell.find('w:p/w:pPr/w:jc',W)
                require(align is not None and align.attrib.get('{'+W['w']+'}val')=='right','Numeric cell alignment lost')
        require(tables[0].find('.//w:tblHeader',W) is not None,'Repeated header lost')
        require(pdf.read_bytes().startswith(b'%PDF'),'Invalid PDF export')
        for page in range(1,info['pages']+1):
            png=root/f'page-{page}.png';r.run('render',str(doc),str(png),'--page',str(page),'--scale','1');require(png.read_bytes().startswith(b'\x89PNG'),'Page render missing')
        require(before==hashlib.sha256(input_path.read_bytes()).hexdigest(),'Source quote changed')
        results.append({'name':name,'itemCount':len(data['items']),'total':total,'pages':info['pages'],'nativeTableAndAmounts':'PASS','allRowsUnsplit':'PASS','columnWidthsAndNumericAlignment':'PASS','inputPreserved':'PASS','allPagesRendered':'PASS','visualReview':'NOT_PERFORMED_BY_CI'})
    return {'result':'PASS','variants':results,'scope':'specified fixtures and native structure; real quote approval, arbitrary typography and host sync not proven'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    group=parser.add_mutually_exclusive_group(required=True);group.add_argument('--cli',type=Path);group.add_argument('--runtime-root',type=Path);a=parser.parse_args()
    out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
    exe=a.cli.resolve() if a.cli else None
    if a.runtime_root:
        matches=list(a.runtime_root.resolve().rglob('wordcraft-cli.exe'));require(len(matches)==1,'Expected one previously verified Windows CLI');exe=matches[0]
        prior=json.loads((a.runtime_root/'result.json').read_text(encoding='utf-8'));require(hashlib.sha256(exe.read_bytes()).hexdigest()==prior['exeSha256'],'CLI changed since runtime verification')
    work=out/'报价 中文 workspace';work.mkdir();r=Runner(exe,work,out);r.run('--version')
    report=run_quotes(r,a.source.resolve());report['nativeProcesses']=len(r.calls);report['platform']=sys.platform
    (out/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
