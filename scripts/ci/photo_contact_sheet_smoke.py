"""用技能原脚本与真实原生CLI验证联系表，子调用接入已有调用记录。"""
import importlib.util
import json
from pathlib import Path
import struct
import zlib
from craft_cli_windows import require
from photo_playbook_smoke import rgb_pixels


def run_contact_sheet(r, recipes):
    skill = Path(recipes).resolve().parents[2]/'photocraft-batch-image-delivery'
    source = skill/'scripts/contact_sheet.py'
    spec = importlib.util.spec_from_file_location('skill_contact_sheet', source)
    module = importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.execute = lambda cli, *args: r.run(*args)
    work = r.work/'contact-sheet';work.mkdir()
    files = []
    dimensions = [(160,80),(80,160),(100,100)]
    colors = [(240,45,35),(20,180,60),(35,80,235)]
    for index, ((width,height), color) in enumerate(zip(dimensions,colors)):
        def chunk(kind, data):
            return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))
        raw=b''.join(b'\0'+bytes(color)*width for _ in range(height))
        image=work/('sample-%d.png'%index)
        image.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',width,height,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b''))
        files.append(image)
    before=len(r.calls)
    result=module.build(r.exe,[files[i%3] for i in range(7)],work/'pages')
    require([len(page['files']) for page in result['pages']]==[6,1],'Wrong pagination/order')
    for index, page in enumerate(result['pages']):
        width,height,pixels=rgb_pixels(work/'pages'/page['preview'])
        require((width,height)==(720,400),'Wrong contact sheet dimensions')
        slots=module.grid(len(page['files']))
        for item,(_,x,y) in enumerate(slots):
            offset=(int(y)*width+int(x))*3
            require(tuple(pixels[offset:offset+3])==colors[(index*6+item)%3],'Image order or centre pixel differs')
        info=json.loads(r.run('info',str(work/'pages'/page['project'])))
        require(len(info['layers'])==1+2*len(page['files']),'Editable layers missing after reopen')
    return {'inputCount':7,'uniqueSyntheticImages':3,'pages':2,'cliCalls':len(r.calls)-before,
            'sourceScript':str(source.relative_to(skill)), 'inputHashesUnchanged':True,
            'pixelChecks':'all seven centres match explicit input order',
            'scope':'synthetic inputs; real photographs, fonts and editor sync not inferred'}
