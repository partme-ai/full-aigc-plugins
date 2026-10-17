#!/usr/bin/env python3
"""图层两轮真实图像核验：显式区分应变化、应保全与只记录的像素。"""
import argparse,hashlib,json
from pathlib import Path
COMMANDS=['layer.'+n for n in ('new','newSublayer','delete','duplicate','setCurrent','setProps','collectInNew','selectAll','clippingMask.toggle','target','pasteRemembersLayers')]
CHANGED={'layer.setProps','layer.clippingMask.toggle'}
MEASURED={'layer.duplicate'}
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def expectation(command,kind):
    if command not in COMMANDS:raise ValueError('layer_render_command')
    return 'measured' if kind=='app-window' or command in MEASURED else 'different' if command in CHANGED else 'equal'
def validate_count(count,total,relation):
    if type(count) is not int or not 0<=count<=total or relation not in ('equal','different','measured') or relation=='equal' and count!=0 or relation=='different' and count==0:raise ValueError('layer_render_pixels')
def qualify(root,proof):
    from PIL import Image
    report=json.loads(Path(proof).read_text());cases=[]
    for case in report['cases']:
        command=case['command'];comparisons=[]
        for kind in ('native-canvas','png-export','app-window'):
            records=[s['window'] if kind=='app-window' else s['canvas'] if kind=='native-canvas' else next(e for e in s['exports'] if e['format']=='png') for s in case['stages']];pixels=[];size=(1440,900) if kind=='app-window' else (128,96)
            for record in records:
                relative=Path(record['path']);path=root/relative
                if relative.is_absolute() or '..' in relative.parts or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()) or sha(path)!=record['sha256']:raise ValueError('layer_render_identity')
                with Image.open(path) as im:
                    im.load();expected_size=(1440*record['pixelScale'],900*record['pixelScale']) if kind=='app-window' else size
                    if im.size!=expected_size:raise ValueError('layer_render_size')
                    rgb=im.convert('RGB')
                    if rgb.size!=size:rgb=rgb.resize(size,Image.Resampling.LANCZOS)
                    pixels.append(rgb.tobytes())
            count=sum(pixels[0][i:i+3]!=pixels[1][i:i+3] for i in range(0,len(pixels[0]),3));relation=expectation(command,kind);validate_count(count,size[0]*size[1],relation)
            m={'kind':kind,'expectation':relation,'width':size[0],'height':size[1],'totalPixels':size[0]*size[1],'changedPixels':count,'firstSha256':records[0]['sha256'],'secondSha256':records[1]['sha256']}
            if kind=='app-window':m.update(normalization='1440x900-logical-lanczos',sourcePixelScales=[r['pixelScale'] for r in records])
            comparisons.append(m)
        cases.append({'command':command,'comparisons':comparisons})
    return {'schema':'vectorcraft-command-layer-render/v1','result':'PASS','executionReportSha256':sha(proof),'checkerSha256':sha(__file__),'cases':cases,'scope':'Two native deliveries:explicit equal/different canvas contracts;window pixels measured only,session correctness checked independently;not creative judgment or full V1'}
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('root',type=Path);args=parser.parse_args();result=qualify(args.root,args.root/'proof.json');(args.root/'render-changes.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'result':'PASS','commands':len(result['cases']),'comparisons':33}))
