"""用实际技能入口生成宣传册，原生重开检查全文、文档字体及PDF。"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile
import fitz
from craft_cli_windows import Runner,require
from photo_playbook_smoke import fixture
from photo_more_smoke import fixture as alternate_fixture


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--font-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    g=p.add_mutually_exclusive_group(required=True);g.add_argument('--cli',type=Path);g.add_argument('--runtime-root',type=Path);a=p.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False);exe=a.cli.resolve() if a.cli else None
    if a.runtime_root:
        matches=list(a.runtime_root.resolve().rglob('designcraft-cli.exe'));require(len(matches)==1,'Expected one verified CLI');exe=matches[0];prior=json.loads((a.runtime_root/'result.json').read_text(encoding='utf-8'));require(hashlib.sha256(exe.read_bytes()).hexdigest()==prior['exeSha256'],'Runtime changed')
    root=Path(__file__).resolve().parents[2];lock=json.loads((root/'plugins/designcraft-plugin/ui/fonts.lock.json').read_text(encoding='utf-8'));font_root=a.font_root.resolve()/'fonts';font_names=['LXGWWenKai-Regular.ttf','OFL-LXGWWenKai.txt']
    for name in font_names:
        entry=next(x for x in lock['files'] if x['file']=='fonts/'+name);require(hashlib.sha256((font_root/name).read_bytes()).hexdigest()==entry['sha256'],'Font/notice differs from lock')
    skill=a.source.resolve()/'skills/designcraft-brochure';sample=json.loads((skill/'assets/product-input.json').read_text(encoding='utf-8'));chinese=json.loads(json.dumps(sample));chinese.update(fontFamily='LXGW WenKai',footer='内部校样');chinese['cover']={'heading':'办公套装 / 校样','text':'两款办公用品的虚构示例。\n发布前核实产品信息。'};chinese['products'][0].update(heading='桌面收纳',variant='蓝色',currency='CNY',price='24.5',description='整理小件文具。仅为样例。');chinese['products'][1].update(heading='文件袋',variant='橙色',currency='CNY',description='日常文件收纳。仅为样例。');chinese['contact']={'heading':'下一步','text':'核对尺寸、价格与供货情况。'};reports=[]
    for name,data in [('english',sample),('chinese',chinese)]:
        work=out/('宣传册 中文 '+name);work.mkdir();runner=Runner(exe,work,work);images=work/'brochure-input';images.mkdir()
        fixture(images/'organiser.png');alternate_fixture(images/'case.png')
        image_hashes={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in images.iterdir()};inp=work/'产品.json';inp.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8');original=inp.read_bytes();recipe_path=work/'filled-recipe.json';helper=[sys.executable,str(skill/'scripts/brochure_input.py'),'--input',str(inp),'--output',str(recipe_path)]
        proc=subprocess.run(helper,capture_output=True,text=True,encoding='utf-8');require(proc.returncode==0,'Input helper failed: '+proc.stderr);recipe_bytes=recipe_path.read_bytes();again=subprocess.run(helper,capture_output=True,text=True,encoding='utf-8');require(again.returncode!=0 and recipe_path.read_bytes()==recipe_bytes,'Existing recipe overwritten')
        proc=subprocess.run([sys.executable,str(skill/'scripts/write_script.py'),'--recipes',str(recipe_path),'--scene','brochure','--output',str(work/'layout.json')],capture_output=True,text=True,encoding='utf-8');require(proc.returncode==0,'Reference compiler failed: '+proc.stderr)
        compiled=json.loads(runner.run('script',work/'layout.json','--save','draft.designcraft'));require(compiled.get('failed') is None,'Native generated script incomplete')
        if name=='chinese':
            fonts=work/'Document Fonts';fonts.mkdir()
            for file in font_names:shutil.copy2(font_root/file,fonts/file)
        # 显式重开加载文档字体；禁止将首轮缺字草稿当作最终PDF。
        fonts=json.loads(runner.run('run','--in','draft.designcraft','--cmd','font.list'))
        if name=='chinese':require(any(f['family']=='LXGW WenKai' and f['source']=='document' and not f['missing'] and not f['styleMissing'] for f in fonts),'Document CJK font not loaded')
        info=json.loads(runner.run('run','--in','draft.designcraft','--cmd','document.inspect'));require(info['pageCount']==4 and len(info['stories'])==12 and not any(s['overset'] for s in info['stories']),'Four-page story structure or overset mismatch')
        with zipfile.ZipFile(work/'draft.designcraft') as package:
            document=json.loads(package.read('document.json'))
            for page_index,filename in [(1,'organiser.png'),(2,'case.png')]:
                graphics=[item for item in info['spreads'][page_index]['items'] if item['kind']=='<image>'];require(len(graphics)==1,'Product image frame missing')
                asset=graphics[0]['asset'];require(document['assets'][str(asset)]['link']=='brochure-input/'+filename,'Product image linked to wrong SKU page');require(package.read('assets/'+str(asset)+'.png')==(images/filename).read_bytes(),'Embedded product pixels differ from expected input')
        queries=[{'command':'story.get','params':{'story':s['id']}} for s in info['stories']];(work/'queries.json').write_text(json.dumps(queries),encoding='utf-8');readback=json.loads(runner.run('script',work/'queries.json','--in','draft.designcraft','--export','final.pdf','--export','final.idml'))['results'];recipe=json.loads(recipe_bytes);frames={item['id']:spread['index'] for spread in info['spreads'] for item in spread['items']}
        expected=[s for s in recipe['steps'] if s['command']=='frame.create' and s['params'].get('content')=='text']
        for step in expected:require(sum(s['text']==step['params']['text'] and frames[s['frames'][0]]==step['params']['spread'] and s['overset'] is None for s in readback)==1,'Generated story text/page mismatch: '+step['capture'])
        pdf=fitz.open(work/'final.pdf');require(len(pdf)==4,'PDF page count mismatch')
        for index,page in enumerate(pdf):require(recipe['pages'][index]['heading'] in page.get_text(),'PDF heading glyph/text missing')
        require(sum(len(page.get_images()) for page in pdf)==2,'PDF image count mismatch');pdf[0].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(work/'cover.png');require(inp.read_bytes()==original,'Input data changed');require(all(hashlib.sha256((images/n).read_bytes()).hexdigest()==h for n,h in image_hashes.items()),'Source image changed')
        reports.append({'variant':name,'status':'PASS','stories':12,'pages':4,'nativeProcesses':len(runner.calls),'pdfHeadings':'PASS actual extraction','font':fonts,'existingOutputProtection':'PASS','inputImagesUnchanged':'PASS','skuImageBindings':'PASS distinct embedded image bytes on correct page','commercialDesignQuality':'NOT_TESTED','installedHost':'NOT_TESTED'})
    result={'status':'PASS','platform':sys.platform,'scope':'synthetic two-product brochure; actual skill helper/CLI/PDF','variants':reports};(out/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=True))
if __name__=='__main__':main()
