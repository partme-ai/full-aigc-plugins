"""分阶段验证现有老照片配方，合成损伤样本不代表真实人物修复效果。"""
import hashlib
import json
import math
from pathlib import Path
import struct
import zlib
from craft_cli_windows import require
from photo_playbook_smoke import rgb_pixels


def verify_local_repair(clean,damaged,repaired,width,regions):
    require(len(clean)==len(damaged)==len(repaired),'Repair image dimensions changed')
    height=len(clean)//(width*3);before=after=outside=0
    for y in range(height):
        for x in range(width):
            selected=any(x0<=x<x1 and y0<=y<y1 for x0,y0,x1,y1 in regions)
            for c in range(3):
                i=(y*width+x)*3+c
                if selected:before+=abs(damaged[i]-clean[i]);after+=abs(repaired[i]-clean[i])
                else:outside+=abs(repaired[i]-damaged[i])
    require(outside==0,'Local healing changed protected pixels')
    require(before>0 and after<before*0.5,'Local healing did not reduce known damage error by half')
    return {'targetErrorBefore':before,'targetErrorAfter':after,'protectedDelta':outside}


def fixture(path,damage):
    width,height=256,192;rows=[]
    for y in range(height):
        row=bytearray()
        for x in range(width):
            value=int(75+x*0.3+8*math.cos(y/12)+4*math.sin(x/7))
            if damage and any((x-a)**2+(y-b)**2<=4 for a,b in [(42,31),(82,41)]):value=255
            row.extend([value]*3)
        rows.append(b'\0'+row)
    def chunk(kind,data):return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))
    path.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',width,height,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(b''.join(rows)))+chunk(b'IEND',b''))


def run_restoration(r,recipes):
    """执行相同canonical配方的局部前三步和整体后两步，检查阶段之间的真实PNG。"""
    recipe=next(x for x in json.loads(Path(recipes).read_text(encoding='utf-8'))['recipes'] if x['id']=='old-photo-conservative')
    require([x['command'] for x in recipe['steps']]==['layer.duplicate','paint.spotHealing','paint.healingBrush','filter.noise.reduceNoise','layer.newAdjustmentLayer.levels'],'Restoration phase split changed; review fixture and guide')
    original=r.work;r.work=original/'restoration-phases';r.work.mkdir()
    try:
        fixture(r.work/'clean-reference.png',False);fixture(r.work/'damaged-input.png',True)
        input_hash=hashlib.sha256((r.work/'damaged-input.png').read_bytes()).hexdigest()
        def execute(source,steps,target):
            args=['run',source]
            for step in steps:args.extend(['--cmd',step['command'],'--params',json.dumps(step['params'],ensure_ascii=False)])
            r.run(*args,'--out',target)
        execute('damaged-input.png',recipe['steps'][:3],'local-repair.pcraft');r.run('convert','local-repair.pcraft','local-repair.png')
        metrics=verify_local_repair(rgb_pixels(r.work/'clean-reference.png')[2],rgb_pixels(r.work/'damaged-input.png')[2],rgb_pixels(r.work/'local-repair.png')[2],256,[(36,26,49,37),(76,36,89,47)])
        execute('local-repair.pcraft',recipe['steps'][3:],'final.pcraft');r.run('convert','final.pcraft','final.png')
        info=json.loads(r.run('info','final.pcraft'));layers=info['layers'];require(len(layers)==3,'Expected original, repair copy and editable levels')
        working=next(x for x in layers if x['name']=='Restoration working copy');adjustment=next(x for x in layers if x['kind']=='Adjustment');source=next(x for x in layers if x['id'] not in [working['id'],adjustment['id']])
        execute('final.pcraft',[{'command':'layer.delete','params':{'layer':adjustment['id']}},{'command':'layer.delete','params':{'layer':working['id']}}],'source-only-check.pcraft');r.run('convert','source-only-check.pcraft','source-only-check.png')
        require(rgb_pixels(r.work/'source-only-check.png')==rgb_pixels(r.work/'damaged-input.png'),'Original source layer changed')
        require(rgb_pixels(r.work/'final.png')[:2]==(256,192),'Final dimensions changed')
        require(rgb_pixels(r.work/'final.png')[2]!=rgb_pixels(r.work/'local-repair.png')[2],'Global tone phase had no rendered effect')
        require(hashlib.sha256((r.work/'damaged-input.png').read_bytes()).hexdigest()==input_hash,'Original input file changed')
        record={'id':recipe['id'],'recipeSha256':hashlib.sha256(json.dumps(recipe,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'localRepair':metrics,'inputFileUnchanged':'PASS','originalLayerPixelRoundtrip':'PASS','editableWorkingAndLevels':'PASS','globalToneChangesPixels':'PASS','dimensions':'PASS','realPhotoQuality':'NOT_TESTED','hostEditorSync':'NOT_TESTED'}
        (r.work/'results.json').write_text(json.dumps(record,indent=2)+'\n');return record
    finally:r.work=original
