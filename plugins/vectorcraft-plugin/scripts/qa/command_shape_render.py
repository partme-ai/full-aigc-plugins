#!/usr/bin/env python3
"""核对形状两轮画布、导出及真实应用窗口的像素差异。"""
import argparse,hashlib,importlib.util,json
from pathlib import Path
COMMANDS=['shape.'+x for x in ('rectangle','ellipse','polygon','star','flare','line','spiral','arc','rectangularGrid','polarGrid')]
def qualify(root,proof):
    from PIL import Image
    path=Path(__file__).with_name('command_render.py');spec=importlib.util.spec_from_file_location('shape_render_base',path);base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base);base.COMMANDS=COMMANDS
    result=base.qualify(root,proof);report=json.loads(Path(proof).read_text())
    for case in result['cases']:
        stages=next(c['stages'] for c in report['cases'] if c['command']==case['command']);records=[s['window'] for s in stages];pixels=[]
        for record in records:
            relative=Path(record['path']);path=root/relative
            if relative.is_absolute() or '..' in relative.parts or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()) or base.sha(path)!=record['sha256']:raise ValueError('shape_window_identity')
            with Image.open(path) as im:
                im.load()
                if im.size!=(record['width'],record['height']) or record['pixelScale'] not in (1,2) or im.size!=(1440*record['pixelScale'],900*record['pixelScale']):raise ValueError('shape_window_size')
                rgb=im.convert('RGB')
                if record['pixelScale']==2:rgb=rgb.resize((1440,900),Image.Resampling.LANCZOS)
                pixels.append(rgb.tobytes())
        count=base.changed_pixels(*pixels,1440,900);case['comparisons'].append({'kind':'app-window','normalization':'1440x900-logical-lanczos','sourcePixelScales':[r['pixelScale'] for r in records],'width':1440,'height':900,'changedPixels':count,'totalPixels':1296000,'firstSha256':records[0]['sha256'],'secondSha256':records[1]['sha256']})
    result['checkerSha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();result['scope']='Actual pixels for10 shape creation/revision pairs on native canvas,PNG and owned app windows;not creative judgment or complete V1';return result
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('root',type=Path);args=parser.parse_args();result=qualify(args.root,args.root/'proof.json');(args.root/'render-changes.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'result':'PASS','commands':len(result['cases']),'comparisons':30}))
