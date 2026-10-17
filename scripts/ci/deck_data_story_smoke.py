"""实际DeckCraft CLI验证参数化数据叙事的多系列图表和来源备注。"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
import zipfile
from craft_cli_windows import Runner, require

C='http://schemas.openxmlformats.org/drawingml/2006/chart'
A='http://schemas.openxmlformats.org/drawingml/2006/main'

def verify_chart(path, data):
    with zipfile.ZipFile(path) as archive:
        charts=[n for n in archive.namelist() if n.startswith('ppt/charts/chart') and n.endswith('.xml')]
        require(len(charts)==1,'Expected one editable chart')
        root=ET.fromstring(archive.read(charts[0]));series=root.findall('.//{'+C+'}ser')
        require(len(series)==len(data['series']),'Chart series lost')
        for actual,expected in zip(series,data['series']):
            values=[float(x.text) for x in actual.findall('.//{'+C+'}val/{'+C+'}numRef/{'+C+'}numCache/{'+C+'}pt/{'+C+'}v')]
            require(values==expected['values'],'Chart values changed')
            labels=[x.text for x in actual.findall('.//{'+C+'}cat/{'+C+'}strRef/{'+C+'}strCache/{'+C+'}pt/{'+C+'}v')]
            require(labels==data['categories'],'Category order lost')
        notes=''.join(x.text or '' for n in archive.namelist() if n.startswith('ppt/notesSlides/notesSlide') and n.endswith('.xml') for x in ET.fromstring(archive.read(n)).iter('{'+A+'}t'))
        for key in ('source','period','definition','limitations','unit'):
            require(data[key] in notes,'Provenance missing: '+key)

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    group=p.add_mutually_exclusive_group(required=True);group.add_argument('--cli',type=Path);group.add_argument('--runtime-root',type=Path);a=p.parse_args()
    out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
    exe=a.cli.resolve() if a.cli else None
    if a.runtime_root:
        matches=list(a.runtime_root.resolve().rglob('deckcraft-cli.exe'));require(len(matches)==1,'Expected one verified runtime');exe=matches[0]
        prior=json.loads((a.runtime_root/'result.json').read_text(encoding='utf-8'));require(hashlib.sha256(exe.read_bytes()).hexdigest()==prior['exeSha256'],'Runtime changed')
    home=a.source.resolve()/'skills/deckcraft-data-story'
    spec=importlib.util.spec_from_file_location('story',home/'scripts/data_story.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    sample=json.loads((home/'assets/example-input.json').read_text(encoding='utf-8'))
    multi=copy.deepcopy(sample);multi['title']='分类指标对比';multi['categories']=['第一组','第二组','第三组'];multi['series']=[{'name':'本期','values':[-2,0,4.5]},{'name':'上期','values':[1,3,2.25]}]
    work=out/'数据 中文 workspace';work.mkdir();r=Runner(exe,work,out);results=[]
    for name,data in [('sample',sample),('multi-negative-zero',multi)]:
        root=work/name;root.mkdir();inp=root/'input.json';inp.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8');before=inp.read_bytes()
        plan=m.compile_story(data);(root/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8');args=['run']
        for c in plan['commands']:args+=['--cmd',c['command']+'='+json.dumps(c['params'],ensure_ascii=False,separators=(',',':'))]
        native=root/'story.deckcraft';pptx=root/'story.pptx';reopened=root/'reopened.deckcraft';roundtrip=root/'roundtrip.pptx'
        r.run(*args,'--save',native);r.run('convert',native,pptx);verify_chart(pptx,data)
        r.run('convert',pptx,reopened);r.run('convert',reopened,roundtrip);verify_chart(roundtrip,data)
        require(before==inp.read_bytes(),'Input changed')
        results.append({'name':name,'chartDataCategoryOrderAndNotes':'PASS','editablePptxRoundtrip':'PASS','inputPreserved':'PASS'})
    result={'status':'PASS','platform':sys.platform,'nativeProcesses':len(r.calls),'variants':results,'visualReview':'NOT_TESTED','hostSync':'NOT_TESTED'}
    (out/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
