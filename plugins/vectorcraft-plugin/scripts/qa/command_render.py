#!/usr/bin/env python3
"""只读核对实际原生画布及PNG的逐轮像素变化，不替代创意或窗口验收。"""
import argparse
import hashlib
import json
from pathlib import Path
COMMANDS=['stroke.set','stroke.setAdvanced','stroke.widthPoint.set','stroke.widthPoint.copy','stroke.widthProfile.set']
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def changed_pixels(before,after,width,height):
    """计数RGB实际变化像素；尺寸不符或渲染未变化必须失败。"""
    if type(width) is not int or type(height) is not int or min(width,height)<=0 or len(before)!=width*height*3 or len(after)!=len(before):raise ValueError('command_render_shape')
    count=sum(before[i:i+3]!=after[i:i+3] for i in range(0,len(before),3))
    if not count:raise ValueError('command_render_unchanged')
    return count

def qualify(root,proof):
    """只读取已完成运行的文件，并与执行时摘要绑定；不重放任何命令。"""
    from PIL import Image
    report=json.loads(Path(proof).read_text());results=[]
    for command in COMMANDS:
        case=next(c for c in report['cases'] if c['command']==command);stages=case['stages'];records=[]
        for kind in ('native-canvas','png-export'):
            references=[s['canvas'] if kind=='native-canvas' else next(e for e in s['exports'] if e['format']=='png') for s in stages]
            images=[]
            for record in references:
                relative=Path(record['path']);path=root/relative
                if relative.is_absolute() or '..' in relative.parts or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()) or sha(path)!=record['sha256']:raise ValueError('command_render_identity')
                with Image.open(path) as image:
                    image.load()
                    if image.size!=(128,96):raise ValueError('command_render_shape')
                    images.append(image.convert('RGB').tobytes())
            count=changed_pixels(*images,128,96)
            if references[0]['sha256']==references[1]['sha256']:raise ValueError('command_render_identity')
            records.append({'kind':kind,'width':128,'height':96,'changedPixels':count,'totalPixels':128*96,'firstSha256':references[0]['sha256'],'secondSha256':references[1]['sha256']})
        results.append({'command':command,'comparisons':records})
    return {'schema':'vectorcraft-command-render-changes/v1','result':'PASS','executionReportSha256':sha(proof),'checkerSha256':sha(__file__),'cases':results,'scope':'Actual RGB pixel changes for five explicit native style revisions;not creative quality,OS-window screenshots or preference restart persistence'}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('root',type=Path);args=parser.parse_args();result=qualify(args.root,args.root/'proof.json');(args.root/'render-changes.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'result':'PASS','commands':len(result['cases']),'comparisons':sum(len(c['comparisons']) for c in result['cases'])}))
