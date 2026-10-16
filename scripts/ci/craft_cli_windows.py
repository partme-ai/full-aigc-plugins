"""在真实 Windows 上执行固定官方 Craft CLI 的业务往返，不使用 MCP 替代。"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import struct
import subprocess
import sys
import wave
import zipfile
import zlib

from craft_windows import download, safe_name


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def png_fixture(path):
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    rows = b''.join(b'\0' + b''.join(bytes((x * 4, y * 4, 80)) for x in range(64)) for y in range(48))
    path.write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 64, 48, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(rows)) + chunk(b'IEND', b''))


def pdf_fixture(path):
    objects = [b'<< /Type /Catalog /Pages 2 0 R >>', b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>', b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 100] /Contents 4 0 R >>', b'<< /Length 0 >>\nstream\n\nendstream']
    data = b'%PDF-1.4\n'; offsets = [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(data)); data += f'{i} 0 obj\n'.encode() + obj + b'\nendobj\n'
    start = len(data)
    data += b'xref\n0 5\n0000000000 65535 f \n' + b''.join(f'{o:010d} 00000 n \n'.encode() for o in offsets[1:])
    path.write_bytes(data + f'trailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n{start}\n%%EOF\n'.encode())


class Runner:
    def __init__(self, exe, work, output):
        self.exe, self.work, self.output = exe, work, output
        self.calls = []

    def run(self, *args, stdin=None):
        argv = [str(self.exe), *map(str, args)]
        result = subprocess.run(argv, cwd=self.work, input=stdin, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=120)
        self.calls.append({'argv': argv, 'exitCode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
        (self.output / 'calls.json').write_text(json.dumps(self.calls, ensure_ascii=False, indent=2), encoding='utf-8')
        require(result.returncode == 0, f'CLI failed ({result.returncode}): {args}; {result.stderr}')
        return result.stdout


def verify_photo(info, filename, layer_name):
    # 官方 0.9.0 Save As 将文档身份更新为目标文件名；内容由图层/几何单独核验。
    require(info['name'] == filename, 'Saved document identity mismatch')
    require((info['width'], info['height']) == (64, 48), 'Document dimensions lost')
    layer = next((x for x in info['layers'] if x['name'] == layer_name), None)
    require(layer is not None, 'Unicode layer name lost')
    require(layer['kind'] == 'Pixel' and layer['bounds'][2] > 30 and layer['bounds'][3] > 20,
            'Painted layer content bounds lost')


def business(name, r):
    j = lambda v: json.dumps(v, ensure_ascii=False, separators=(',', ':'))
    marker = 'Windows 中文业务 42'
    if name == 'cadcraft':
        r.run('run', '--metric', '--cmd', 'circle ' + j({'center':[10,10],'radius':4}), '--save', '图纸.dxf')
        info = json.loads(r.run('info', '图纸.dxf'))
        require(info['entityCount'] == 1, 'Circle missing after reopen')
        r.run('convert', '图纸.dxf', '图纸.svg')
        require('<svg' in (r.work/'图纸.svg').read_text(), 'SVG export missing')
    elif name == 'gridcraft':
        r.run('run', '--cmd', 'range.setValues=' + j({'range':'A1','values':[[marker,21],['total','=B1*2']]}), '--out', '工作表.xlsx', '--quiet')
        require(r.run('cat','工作表.xlsx','--range','B1:B2').split() == ['21','42'], 'Formula/value roundtrip mismatch')
        require('=B1*2' in r.run('cat','工作表.xlsx','--range','B2','--formulas'), 'Formula not preserved')
        r.run('convert','工作表.xlsx','工作表.csv')
        require(marker in (r.work/'工作表.csv').read_text(encoding='utf-8'), 'Unicode lost')
    elif name == 'wordcraft':
        r.run('run','--cmd','text.insert='+j({'text':marker}), '--save','文档.docx')
        require(marker in r.run('text','文档.docx'), 'Text missing after reopen')
        r.run('convert','文档.docx','文档.pdf')
        require((r.work/'文档.pdf').read_bytes().startswith(b'%PDF'), 'Invalid PDF')
    elif name == 'deckcraft':
        r.run('run','--cmd','slide.new='+j({'layout':'titleAndContent','title':marker,'body':'Business test'}),'--save','演示.deckcraft')
        require(marker in r.run('info','演示.deckcraft'), 'Slide title lost')
        r.run('convert','演示.deckcraft','演示.pptx')
        with zipfile.ZipFile(r.work/'演示.pptx') as z:
            require(any(marker in z.read(n).decode('utf-8') for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')), 'PPTX title missing')
    elif name == 'photocraft':
        r.run('run','--new',j({'width':64,'height':48,'name':marker}),'--cmd','layer.new.layer','--params',j({'name':marker}),'--cmd','paint.stroke','--params',j({'points':[[2,2,1],[40,30,1]],'size':5,'color':'#00ff00'}),'--out','图片.pcraft')
        info=json.loads(r.run('info','图片.pcraft'))
        verify_photo(info, '图片.pcraft', marker)
        r.run('convert','图片.pcraft','图片.png')
        require(struct.unpack('>II',(r.work/'图片.png').read_bytes()[16:24])==(64,48),'PNG dimensions mismatch')
    elif name == 'vectorcraft':
        r.run('run','--cmd','file.new','--params',j({'width':200,'height':100}),'--cmd','shape.ellipse','--params',j({'x':10,'y':10,'width':80,'height':60}),'--cmd','paint.setFill','--params',j({'color':'#3366ff'}),'--export','矢量.vectorcraft')
        rows=r.run('run','--in','矢量.vectorcraft','--cmd','document.inspect').splitlines()
        require(json.loads(rows[-1])['result']['artboards'][0]['width']==200,'Artboard lost')
        r.run('convert','矢量.vectorcraft','矢量.svg')
        require('3366ff' in (r.work/'矢量.svg').read_text().lower(),'Fill lost')
    elif name == 'designcraft':
        r.run('script','-','--save','排版.designcraft',stdin='frame.create '+j({'rect':[72,72,300,200],'content':'text','text':marker})+'\nstory.get {"story":"$0.story"}\n')
        result=r.run('run','--in','排版.designcraft','--cmd','document.inspect','--export','排版.idml')
        with zipfile.ZipFile(r.work/'排版.idml') as z:
            require(any(marker in z.read(n).decode('utf-8') for n in z.namelist() if n.startswith('Stories/') and n.endswith('.xml')), 'Story not preserved')
    elif name == 'effectcraft':
        r.run('exec','comp.new','--params',j({'name':'Main','width':320,'height':180,'duration':3}),'--empty','--save-as','合成.ecproj')
        r.run('exec','layer.newSolid',j({'color':'#00ff00','name':'Green'}),'合成.ecproj','--save')
        r.run('set','Main','Green','transform/opacity','25','--project','合成.ecproj','--save')
        require(json.loads(r.run('get','Main','Green','transform/opacity','合成.ecproj'))['value']==25,'Opacity lost')
    elif name == 'filmcraft':
        r.run('--demo','exec','file.newBin','name='+marker,'--save-as','剪辑.fcproj')
        require(marker in r.run('--project','剪辑.fcproj','inspect','project'),'Bin lost after reopen')
        r.run('--project','剪辑.fcproj','--save','run','-',stdin=j({'id':'file.newBin','params':{'name':'Second'}})+'\n')
        require('Second' in r.run('--project','剪辑.fcproj','inspect','project'),'Second edit lost')
    elif name == 'lightcraft':
        png_fixture(r.work/'原片.png')
        r.run('run','--library','照片库','--import','原片.png','develop.set','control=light.exposure','value=0.75','app.export','path=调色.jpg','width=60')
        rows=r.run('run','--library','照片库','--import','原片.png','develop.get').splitlines()
        require(json.loads(rows[0])['result']['light']['exposure']==0.75,'Exposure not persisted')
        require((r.work/'调色.jpg').read_bytes().startswith(b'\xff\xd8'),'JPEG missing')
    elif name == 'soundcraft':
        with wave.open(str(r.work/'声音.wav'),'wb') as w:
            w.setparams((1,2,44100,4410,'NONE','not compressed'))
            w.writeframes(b''.join(struct.pack('<h',int(2000*math.sin(2*math.pi*440*i/44100))) for i in range(4410)))
        r.run('convert','声音.wav','重采样.wav','--rate','48000','--normalize','--bit-depth','16')
        info=json.loads(r.run('info','重采样.wav'))
        require(info['sample_rate']==48000 and info['frames']>4000,'Resampling failed')
        with wave.open(str(r.work/'重采样.wav'),'rb') as w:
            samples=struct.unpack('<'+'h'*w.getnframes(),w.readframes(w.getnframes()))
            require(max(map(abs,samples))>20000,'Normalization failed')
    elif name == 'printcraft':
        pdf_fixture(r.work/'原件.pdf')
        r.run('edit','原件.pdf','--out','修订.pdf','--title',marker,'--rotate','1:90','--full')
        info=json.loads(r.run('info','修订.pdf'))
        require(marker in json.dumps(info,ensure_ascii=False),'PDF title lost')
        r.run('extract','修订.pdf','--pages','1','--out','提取.pdf')
        require((r.work/'提取.pdf').read_bytes().startswith(b'%PDF'),'Extract failed')
    elif name == 'figcraft':
        (r.work/'输入.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="120" height="80"><rect x="10" y="10" width="60" height="40" fill="#3366ff"/></svg>')
        r.run('convert','输入.svg','设计.figcraft')
        r.run('info','设计.figcraft','--json')
        r.run('convert','设计.figcraft','设计.svg')
        require('3366ff' in (r.work/'设计.svg').read_text().lower(),'Shape fill lost')
    else:
        raise ValueError(name)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--plugin',required=True); parser.add_argument('--output',type=Path,required=True); parser.add_argument('--playbook',type=Path)
    a=parser.parse_args(); out=a.output.resolve(); out.mkdir(parents=True,exist_ok=False)
    report={'plugin':a.plugin,'platform':sys.platform,'business':'FAIL'}
    try:
        require(sys.platform=='win32','Requires a real Windows runner')
        lock=json.loads(Path(__file__).with_name('craft_cli_windows.lock.json').read_text())[a.plugin]
        report['runtime']=lock
        archive=out/'runtime.zip'; download(lock['url'],archive,lock['sha256'])
        dest=out/'中文 CLI Runtime';dest.mkdir()
        with zipfile.ZipFile(archive) as z:
            for member in z.infolist(): safe_name(member.filename)
            z.extractall(dest)
        matches=list(dest.rglob(lock['executable'])); require(len(matches)==1,'Expected one '+lock['executable'])
        exe=matches[0]; report['exeSha256']=hashlib.sha256(exe.read_bytes()).hexdigest()
        work=out/'中文 业务 workspace';work.mkdir(); r=Runner(exe,work,out)
        r.run('--version')
        catalog_args = ['tools'] if a.plugin == 'printcraft' else ['commands']
        if a.plugin in {'photocraft','figcraft','gridcraft','wordcraft','effectcraft','filmcraft','lightcraft'}:
            catalog_args.append('--json')
        if a.plugin == 'soundcraft':
            ids = [line.split()[0] for line in r.run('commands').splitlines() if line.strip()]
            catalog = [json.loads(r.run('describe', command)) for command in ids]
        else:
            catalog = json.loads(r.run(*catalog_args))
        require(isinstance(catalog, (list, dict)) and bool(catalog), 'Empty command catalog')
        (out/'commands.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding='utf-8')
        business(a.plugin,r)
        if a.playbook:
            if a.plugin == 'photocraft':
                from photo_playbook_smoke import run_playbooks
                report['playbooks'] = run_playbooks(r, a.playbook.resolve())
            elif a.plugin in {'gridcraft','wordcraft','deckcraft'}:
                from office_playbook_smoke import run_playbooks
                report['playbooks'] = run_playbooks(r, a.playbook.resolve(), a.plugin)
            elif a.plugin == 'cadcraft':
                from cad_playbook_smoke import run_playbooks
                report['playbooks'] = run_playbooks(r, a.playbook.resolve())
            elif a.plugin in {'soundcraft','lightcraft'}:
                from media_playbook_smoke import run_playbooks
                report['playbooks'] = run_playbooks(r, a.playbook.resolve(), a.plugin)
            else:
                raise ValueError('No playbook driver for '+a.plugin)
        report['business']='PASS';report['processCount']=len(r.calls)
        report['outputs']=[{'path':str(p.relative_to(work)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in work.rglob('*') if p.is_file()]
    except Exception as e:
        report['error']=str(e); raise
    finally:
        (out/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__': main()
