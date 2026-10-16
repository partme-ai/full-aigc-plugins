"""用真实 CLI 执行场景中的同一份步骤；合成输入只证明技术路径，不证明照片修复画质。"""
import json
from pathlib import Path
import struct
import zlib


def fixture(path):
    def chunk(kind,data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))
    rows=[]
    for y in range(192):
        row=bytearray()
        for x in range(256):
            c=(x//2+50,y//2+50,100)
            if (x-40)**2+(y-30)**2 < 4: c=(255,255,255)
            row.extend(c)
        rows.append(b'\0'+row)
    path.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',256,192,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(b''.join(rows)))+chunk(b'IEND',b''))


def run_playbooks(r, path):
    from craft_cli_windows import require
    selected={'old-photo-conservative','hairline-scratch','fold-line-background','faded-gray-tones','red-cast-aging',
              'jpeg-block-reduction','portrait-small-blemish','portrait-white-balance','product-neutral-packshot',
              'scan-deskew-border','web-image-downsample','print-resolution-tag','duotone-editorial'}
    recipes=json.loads(Path(path).read_text(encoding='utf-8'))['recipes']
    fixture(r.work/'场景原片.png')
    records=[]
    for recipe in recipes:
        if recipe['id'] not in selected: continue
        target=recipe['id']+'.pcraft'; png=recipe['id']+'.png'
        args=['run','场景原片.png']
        for step in recipe['steps']:
            args += ['--cmd',step['command'],'--params',json.dumps(step['params'],ensure_ascii=False)]
        r.run(*args,'--out',target)
        info=json.loads(r.run('info',target))
        require(info['width']>0 and info['height']>0,'Saved document empty')
        if recipe['id']=='print-resolution-tag': require(info['resolution']==300,'Resolution metadata not saved')
        if recipe['id']=='scan-deskew-border': require((info['width'],info['height'])==(240,176),'Crop not saved')
        if recipe['id']=='web-image-downsample': require((info['width'],info['height'])==(256,192),'Resize not saved')
        r.run('convert',target,png)
        data=(r.work/png).read_bytes()
        require(data.startswith(b'\x89PNG'),'Export not PNG')
        require(struct.unpack('>II',data[16:24])==(info['width'],info['height']),'Reopened/exported dimensions diverge')
        if recipe['id'] in {'old-photo-conservative','faded-gray-tones','red-cast-aging','duotone-editorial','portrait-white-balance'}:
            require(len(info['layers'])>=3,'Editable adjustment layer lost')
        records.append({'id':recipe['id'],'technicalRoundtrip':'PASS','creativeAcceptance':'NOT_TESTED'})
    require({x['id'] for x in records}==selected,'Missing required recipe')
    return records
