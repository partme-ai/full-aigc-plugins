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


def rgb_pixels(path):
    """解码原生导出的8位RGB/RGBA PNG，用像素而非编码字节判断是否真的处理。"""
    data=Path(path).read_bytes(); offset=8; compressed=bytearray(); width=height=bpp=None
    while offset<len(data):
        size=struct.unpack('>I',data[offset:offset+4])[0];kind=data[offset+4:offset+8];payload=data[offset+8:offset+8+size];offset+=size+12
        if kind==b'IHDR':
            width,height,depth,color,_,_,interlace=struct.unpack('>IIBBBBB',payload)
            if depth!=8 or color not in (2,6) or interlace!=0:raise ValueError('Smoke expects noninterlaced 8-bit RGB/RGBA PNG')
            bpp=3 if color==2 else 4
        elif kind==b'IDAT':compressed.extend(payload)
        elif kind==b'IEND':break
    raw=zlib.decompress(compressed); stride=width*bpp; prev=bytearray(stride); result=bytearray()
    for y in range(height):
        start=y*(stride+1);kind=raw[start];row=bytearray(raw[start+1:start+1+stride])
        for x in range(stride):
            a=row[x-bpp] if x>=bpp else 0;b=prev[x];c=prev[x-bpp] if x>=bpp else 0
            if kind==1:predictor=a
            elif kind==2:predictor=b
            elif kind==3:predictor=(a+b)//2
            elif kind==4:
                p=a+b-c;pa,pb,pc=abs(p-a),abs(p-b),abs(p-c);predictor=a if pa<=pb and pa<=pc else b if pb<=pc else c
            elif kind==0:predictor=0
            else:raise ValueError('Unknown PNG row filter')
            row[x]=(row[x]+predictor)&255
        for x in range(0,stride,bpp):result.extend(row[x:x+3])
        prev=row
    return width,height,bytes(result)


def local_effect(pixels, baseline, width, target, protected):
    """验证目标区确实变化且保护区逐像素保持；区域均为半开像素矩形。"""
    def delta(rect):
        x0,y0,x1,y1=rect
        return sum(abs(pixels[(y*width+x)*3+c]-baseline[(y*width+x)*3+c])
                   for y in range(y0,y1) for x in range(x0,x1) for c in range(3))
    if len(pixels)!=len(baseline):raise ValueError('Local edit changed pixel dimensions')
    if delta(target)<=100:raise ValueError('Local target had no observable effect')
    if delta(protected)!=0:raise ValueError('Local operation changed protected pixels')


def run_playbooks(r, path):
    from craft_cli_windows import require
    selected={'old-photo-conservative','hairline-scratch','fold-line-background','faded-gray-tones','red-cast-aging',
              'jpeg-block-reduction','portrait-small-blemish','portrait-white-balance','product-neutral-packshot',
              'scan-deskew-border','web-image-downsample','print-resolution-tag','duotone-editorial',
              'window-highlight-local','portrait-subject-lift','background-desaturate-focus','selective-accent-color'}
    recipes=json.loads(Path(path).read_text(encoding='utf-8'))['recipes']
    fixture(r.work/'场景原片.png')
    original_pixels=rgb_pixels(r.work/'场景原片.png')[2]
    r.run('run','场景原片.png','--cmd','select.deselect','--params','{}','--out','baseline.pcraft')
    r.run('convert','baseline.pcraft','baseline.png')
    baseline=rgb_pixels(r.work/'baseline.png')[2]
    regions={
        'window-highlight-local':((160,32,208,96),(0,128,128,192)),
        'portrait-subject-lift':((96,64,128,96),(0,0,32,32)),
        'background-desaturate-focus':((8,8,32,32),(96,72,160,120)),
        'selective-accent-color':((8,8,32,32),(104,72,152,136)),
    }
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
        pixel_check='NOT_APPLICABLE'
        local_check='NOT_APPLICABLE'
        if recipe['id'] in {'old-photo-conservative','faded-gray-tones','red-cast-aging','duotone-editorial','portrait-white-balance','product-neutral-packshot'}:
            pixels=rgb_pixels(r.work/png)[2]
            require(len(pixels)==len(original_pixels),'Unexpected pixel size change')
            require(sum(abs(a-b) for a,b in zip(pixels,original_pixels))>100,'Color treatment had no observable pixel effect')
            pixel_check='PASS'
        if recipe['id'] in regions:
            require(len(info['layers'])>=3,'Masked adjustment layer lost')
            target_rect,protected=regions[recipe['id']]
            local_effect(rgb_pixels(r.work/png)[2],baseline,256,target_rect,protected)
            local_check='PASS'
        records.append({'id':recipe['id'],'technicalRoundtrip':'PASS','pixelEffect':pixel_check,
                        'locality':local_check,'creativeAcceptance':'NOT_TESTED'})
    require({x['id'] for x in records}==selected,'Missing required recipe')
    return records
