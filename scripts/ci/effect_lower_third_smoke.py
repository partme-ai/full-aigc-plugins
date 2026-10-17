"""执行技能原始人物条计划，检查入退场、安全区和保存后关键帧。"""
import json
from pathlib import Path
from craft_cli_windows import require
from effect_playbook_smoke import verify_fade, alpha_metrics
from photo_playbook_smoke import rgb_pixels


def verify_stages(alpha):
    require(len(alpha)==5, 'Expected five sampled stages')
    verify_fade(alpha[:4])
    require(alpha[-1]==0, 'Exit frame must be transparent')


def verify_caption_bounds(width,height,rgba):
    require((width,height)==(960,540),'Wrong frame size')
    white=[]
    for i in range(0,len(rgba),4):
        red,green,blue,alpha=rgba[i:i+4]
        if min(red,green,blue)>140 and alpha>200:white.append(((i//4)%width,(i//4)//width))
    require(white and all(80<=x<=520 and 415<=y<=492 for x,y in white),'Caption escapes safe plate area')
    require(sum(415<=y<=453 for x,y in white)>100,'Name did not render in intended band')
    require(sum(457<=y<=485 for x,y in white)>30,'Role did not render in intended band')


def run_lower_third(r, skills):
    skill=Path(skills)/'effectcraft-lower-thirds'
    plan=json.loads((skill/'references/animated-lower-third.json').read_text(encoding='utf-8'))
    original=r.work;result=[]
    try:
        for variant in ['standard','long-name']:
            r.work=original/('animated-lower-third-'+variant);r.work.mkdir()
            steps=json.loads(json.dumps(plan['steps']))
            if variant=='long-name':
                name=next(s['params'] for s in steps if s['command']=='layer.newText' and s['params']['name']=='Name')
                name.update(plan['longNameVariant'])
            argv=['run','--empty']
            for step in steps:argv += [step['command'],json.dumps(step['params'],ensure_ascii=False)]
            r.run(*argv,'--save-as','scene.ecproj','--json')
            info=json.loads(r.run('info','--project','scene.ecproj','--json'))['activeComp']
            require({v['name'] for v in info['layers']}=={'Name','Role','Plate'},'Wrong saved layers')
            for layer in ['Name','Role','Plate']:
                for time,expected in [(0,0),(.2,50),(.4,100),(5.4,100),(5.96,0)]:
                    value=json.loads(r.run('get',info['name'],layer,'transform/opacity','--time',str(time),'--project','scene.ecproj','--json'))['value']
                    require(abs(value-expected)<.001,'Saved opacity timing changed')
            for step in steps:
                if step['command']=='layer.newText':
                    actual=json.loads(r.run('get',info['name'],step['params']['name'],'text/sourceText','--project','scene.ecproj','--json'))['value']
                    require(actual==step['params']['text'],'Saved caption text changed')
            frames=[]
            for time in plan['sampleTimes']:
                path=r.work/('frame-'+str(time)+'.png')
                r.run('render-frame','--project','scene.ecproj','--time',str(time),'--max-side','960','--transparent','--out',str(path))
                frames.append(path)
            sums=[alpha_metrics(p)[0] for p in frames];verify_stages(sums)
            verify_caption_bounds(*rgb_pixels(frames[2],include_alpha=True))
            record={'variant':variant,'layers':3,'sampleTimes':plan['sampleTimes'],'alphaSums':sums,'captionSafeArea':'PASS'}
            if variant=='standard':
                r.run('render','--project','scene.ecproj','--out','delivery.png','--format','png','--start','0','--end','6','--fps','25','--resolution','half','--channels','rgba')
                files=sorted(r.work.glob('delivery_*.png'))
                require([p.name for p in files]==['delivery_%05d.png'%n for n in range(150)],'Wrong sequence range or missing frame')
                for path in files:
                    raw=path.read_bytes();require(raw[:8]==b'\x89PNG\r\n\x1a\n' and raw[25]==6,'Sequence frame lost RGBA encoding')
                sequence_sums=[alpha_metrics(files[n])[0] for n in [0,5,10,135,149]]
                verify_stages(sequence_sums)
                require(sequence_sums==sums,'Sequence and standalone sampled frames differ')
                record.update(rgbaSequenceFrames=len(files),sequenceSampleAlphaSums=sequence_sums)
            result.append(record)
    finally:r.work=original
    return {'variants':result,'scope':'sample text; no universal font fit or full host acceptance inferred'}
