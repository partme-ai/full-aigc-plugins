"""原生EffectCraft片头片尾配方检查；不声称宿主同步或成片质量验收。"""
import hashlib
import json
from pathlib import Path
from craft_cli_windows import require
from effect_playbook_smoke import property_value, alpha_metrics
from photo_playbook_smoke import rgb_pixels

SCENES={'chapter-card','countdown-intro','credits-roll'}

def verify_countdown(layers,frames):
    require(layers=={'Three':('3',0,1),'Two':('2',1,2),'One':('1',2,3),'Start':('START',3,4)},'Countdown timing or label changed')
    require(len(frames)==8 and all(frames[i]==frames[i+1] for i in range(0,8,2)),'Countdown changes inside its one-second interval')
    require(len(set(frames))==4,'Countdown must render four distinct labels')

def verify_credit_motion(values,start):
    require(values==[[960,start,0],[960,start-1015,0],[960,start-2030,0]],'Credits scroll direction, speed or horizontal alignment changed')

def verify_chapter(number,subtitle,line):
    require(number==[0,100,100],'Chapter number fade or hold missing')
    require(subtitle==[0,100,100],'Chapter subtitle fade or hold missing')
    require(line==[0,100,100],'Chapter rule growth or hold missing')

def run_recipe(r,recipe):
    name=recipe['id'];args=['run','--empty']
    for step in recipe['steps']:args.extend([step['command'],json.dumps(step['params'],ensure_ascii=False)])
    r.run(*args,'--save-as','scene.ecproj')
    info=json.loads(r.run('info','--project','scene.ecproj','--json'))['activeComp']
    initial=recipe['steps'][0]['params']
    for field in ['width','height','duration','frameRate','name']:require(info[field]==initial[field],'Saved composition changed '+field)
    def props(layer):return json.loads(r.run('props',info['name'],layer,'--project','scene.ecproj','--json'))['properties']
    def get(layer,path,time):return json.loads(r.run('get',info['name'],layer,path,'--time',str(time),'--project','scene.ecproj','--json'))['value']
    def frame(time):
        file=r.work/f'frame-{time}.png';r.run('render-frame','--project','scene.ecproj','--comp',info['name'],'--time',str(time),'--max-side','480','--transparent','--out',str(file));return file
    def raster_hash(path):
        width,height,data=rgb_pixels(path,include_alpha=True);require((width,height)==(480,270),'Unexpected output dimensions');return hashlib.sha256(data).hexdigest()
    if name=='countdown-intro':
        layers={layer['name']:(property_value(props(layer['name']),'text/sourceText'),layer['in'],layer['out']) for layer in info['layers']}
        times=[0,0.96,1,1.96,2,2.96,3,3.96];frames=[frame(t) for t in times]
        require(all(alpha_metrics(p)[0]>1000 for p in frames),'Countdown boundary frame is blank')
        verify_countdown(layers,[raster_hash(p) for p in frames])
    elif name=='credits-roll':
        expected=['Direction','Approved Director','Camera','Approved Camera','Sound','Approved Sound']
        for i,text in enumerate(expected):
            layer='Credit'+str(i+1);require(property_value(props(layer),'text/sourceText')==text,'Credits role/name order changed')
            verify_credit_motion([get(layer,'transform/position',t) for t in [0,6,12]],1180+i*130)
        require(alpha_metrics(frame(0))[0]==0 and alpha_metrics(frame(11.96))[0]==0,'Credits first or last valid frame is not clear')
        require(all(alpha_metrics(frame(t))[0]>1000 for t in [3,6,9]),'Credits middle frame is blank')
    elif name=='chapter-card':
        require(property_value(props('Chapter'),'text/sourceText')=='CHAPTER 01','Chapter number changed')
        require(property_value(props('Title'),'text/sourceText')=='Confirmed topic','Chapter title changed')
        verify_chapter([get('Chapter','transform/opacity',t) for t in [0,1,3.96]],[get('Title','transform/opacity',t) for t in [0,1,3.96]],[get('Rule','transform/scale',t)[0] for t in [0,1,3.96]])
        start=frame(0);held=frame(1);last=frame(3.96)
        require(alpha_metrics(start)[0]==0,'Chapter first frame should be transparent')
        require(alpha_metrics(held)[0]>1000 and raster_hash(held)==raster_hash(last),'Chapter complete card did not hold')
        middle=frame(0.6);require(raster_hash(middle)!=raster_hash(held) and alpha_metrics(middle)[0]>1000,'Chapter delayed reveal did not render')
    else:raise ValueError('Unknown delivery scene '+name)
    sequence=r.work/'sequence';sequence.mkdir()
    r.run('render','--project','scene.ecproj','--comp',info['name'],'--start','0','--end',str(info['duration']),'--fps','25','--format','png','--channels','rgba','--resolution','quarter','--out',str(sequence/'frames.png'))
    frames=sorted(sequence.glob('frames_*.png'))
    require(len(frames)==int(info['duration']*25),'PNG sequence frame count differs from duration × fps')
    for png in frames:raster_hash(png)
    return {'id':name,'sequenceFrames':len(frames),'allFramesDecoded':'PASS','savedProjectAndSampledFrames':'PASS','hostEditorSync':'NOT_TESTED','actualProductionPlayback':'NOT_TESTED'}

def run_delivery(r,skills):
    original=r.work;records=[]
    try:
        for name in sorted(SCENES):
            r.work=original/name;r.work.mkdir();recipe=json.loads((Path(skills)/('effectcraft-'+name)/'references/craft-steps.json').read_text(encoding='utf-8'));records.append(run_recipe(r,recipe))
    finally:r.work=original
    return records
