"""执行三个实际FilmCraft配方，检查运动、合成区域及编码音视频；不代替真实素材审阅。"""
import hashlib
import json
import math
from pathlib import Path
import struct
import wave
from craft_cli_windows import require
from film_playbook_smoke import avi_fixture,native_batch,resolve,TICKS
from photo_playbook_smoke import rgb_pixels

SCENES={'freeze-explainer','presenter-inset','jcut-dialogue'}

def verify_hold(selected,held,before,after):
    require(len(held)==3 and all(frame==selected for frame in held),'Hold did not preserve selected source frame')
    require(before!=selected and after!=selected,'Hold did not resume real motion')

def verify_jcut(video,audio):
    require(video==[(0,50),(50,125)],'J-cut video boundary or total duration changed')
    require(audio[1][0]<video[1][0],'Second voice has no lead before second picture')
    require(audio[0][1]<=audio[1][0],'Dialogue voices overlap')
    require(audio==[(0,25),(25,125)],'J-cut voice duration or gap changed')

def verify_inset_bounds(box):
    require(all(abs(a-b)<=1 for a,b in zip(box,[224,162,304,222])) and len(box)==4,'PiP position or source-relative size wrong')

def mean_rgb(path,box=(0,0,320,120)):
    w,h,pixels=rgb_pixels(path);x0,y0,x1,y1=box;count=(x1-x0)*(y1-y0)
    return [sum(pixels[(y*w+x)*3+c] for y in range(y0,y1) for x in range(x0,x1))/count for c in range(3)]

def tone(path,freq,seconds):
    with wave.open(str(path),'wb') as out:
        out.setparams((1,2,48000,round(seconds*48000),'NONE','not compressed'))
        out.writeframes(b''.join(struct.pack('<h',round(5000*math.sin(2*math.pi*freq*i/48000))) for i in range(round(seconds*48000))))

def read_wave(path):
    data=Path(path).read_bytes();require(data[:4]==b'RIFF' and data[8:12]==b'WAVE','Expected real decoded WAV')
    offset=12;fmt=payload=None
    while offset+8<=len(data):
        tag=data[offset:offset+4];length=struct.unpack_from('<I',data,offset+4)[0];chunk=data[offset+8:offset+8+length]
        if tag==b'fmt ':fmt=chunk
        if tag==b'data':payload=chunk
        offset+=8+length+(length%2)
    require(fmt is not None and payload is not None,'WAV missing format or data')
    kind,channels,rate,_,align,bits=struct.unpack_from('<HHIIHH',fmt)
    if kind==65534:kind=struct.unpack_from('<I',fmt,24)[0]
    require(kind in [1,3] and bits in [16,24,32] and align==channels*(bits//8),'Unexpected WAV sample format')
    size=bits//8;values=[]
    for start in range(0,len(payload)-align+1,align):
        samples=[]
        for c in range(channels):
            raw=payload[start+c*size:start+(c+1)*size]
            samples.append(struct.unpack('<f',raw)[0] if kind==3 else int.from_bytes(raw,'little',signed=True)/(2**(bits-1)))
        values.append(sum(samples)/channels)
    return rate,values

def verify_voice(rate,values,seconds,expected):
    chunk=values[round((seconds-.15)*rate):round((seconds+.15)*rate)]
    require(len(chunk)==round(.3*rate),'Decoded voice sample window is incomplete')
    rms=math.sqrt(sum(x*x for x in chunk)/len(chunk));require(rms>.03,'Decoded voice is silent or unexpectedly quiet')
    def energy(freq):
        cosine=sum(v*math.cos(2*math.pi*freq*i/rate) for i,v in enumerate(chunk));sine=sum(v*math.sin(2*math.pi*freq*i/rate) for i,v in enumerate(chunk));return cosine*cosine+sine*sine
    wanted=energy(expected);other=max(energy(f) for f in [440,660,880] if f!=expected)
    require(wanted>50*max(other,1e-10),'Decoded voice belongs to wrong speaker or overlaps another voice')
    return {'time':seconds,'dominantFixtureHz':expected,'rms':rms}

def run_recipe(r,recipe):
    name=recipe['id'];(r.work/'input').mkdir();(r.work/'output').mkdir()
    if name=='freeze-explainer':avi_fixture(r.work/'input/action.avi',moving=True)
    elif name=='presenter-inset':
        avi_fixture(r.work/'input/screen.avi');avi_fixture(r.work/'input/presenter.avi',warm=True);tone(r.work/'input/narration.wav',660,4)
    else:
        avi_fixture(r.work/'input/shot-a.avi');avi_fixture(r.work/'input/shot-b.avi',warm=True);tone(r.work/'input/voice-a.wav',440,1);tone(r.work/'input/voice-b.wav',880,4)
    originals={p.relative_to(r.work).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (r.work/'input').iterdir()}
    captures={};project=None;groups=[]
    for step in recipe['steps']:
        if not groups or groups[-1][0]!=step['batch']:groups.append((step['batch'],[]))
        groups[-1][1].append(step)
    import shutil
    for batch,group in groups:
        steps=[{'command':step['command'],'params':resolve(step['params'],captures)} for step in group]
        if batch=='hold':shutil.copyfile(r.work/'scene.fcproj',r.work/'unheld-reference.fcproj')
        rows=native_batch(r,steps,project)
        for step,row in zip(group,rows):
            if step.get('capture'):captures[step['capture']]=row['result']
        project='scene.fcproj'
    sequence=json.loads(r.run('--project',project,'inspect','sequence'))
    clips=[clip for track in sequence['video'] for clip in track['items']];audio=[clip for track in sequence['audio'] for clip in track['items']]
    def frame(seconds,filename,source=project):
        r.run('--project',source,'render','--seconds',str(seconds),'--out',filename);return r.work/filename
    def image_hash(path,top=None):
        w,h,data=rgb_pixels(path);require((w,h)==(320,240),'Rendered picture dimensions changed')
        return hashlib.sha256(data if top is None else data[:w*min(top,h)*3]).hexdigest()
    result={'id':name,'sourceInputsUnchanged':'PASS','nativeSaveAndMedia':'PASS','hostEditorSync':'NOT_TESTED','realFootageSpeechQuality':'NOT_TESTED'}
    if name=='freeze-explainer':
        require(sequence['durationFrames']==125,'Frame hold did not produce five-second sequence')
        ordered=sorted(clips,key=lambda x:x['startFrame']);require([(x['startFrame'],x['endFrame']) for x in ordered]==[(0,50),(50,75),(75,125)],'Hold segment boundaries wrong')
        reference=image_hash(frame(2,'selected-source.png','unheld-reference.fcproj'),120)
        held=[image_hash(frame(t,f'held-{t}.png'),120) for t in [2,2.5,2.96]]
        verify_hold(reference,held,image_hash(frame(1.96,'before-hold.png'),120),image_hash(frame(3.04,'after-hold.png'),120))
        caption=(r.work/'output/freeze.srt').read_text(encoding='utf-8-sig');require('00:00:02,000 --> 00:00:03,000' in caption and caption.count('Confirmed step')==1,'Freeze explanation subtitle timing changed')
    elif name=='presenter-inset':
        require(sequence['durationFrames']==100 and len(clips)==2 and len(audio)==1,'PiP video or narration missing')
        current=frame(1,'inset.png');shutil.copyfile(r.work/project,r.work/'inset-reference.fcproj')
        r.run('--project','inset-reference.fcproj','--save','exec','clip.enable',json.dumps({'clips':[captures['inset']['clips'][0]]}))
        reference=frame(1,'screen-only.png','inset-reference.fcproj')
        w,h,actual=rgb_pixels(current);_,_,base=rgb_pixels(reference)
        changed=[(i//3%w,i//3//w) for i in range(0,len(actual),3) if actual[i:i+3]!=base[i:i+3]]
        require(changed,'PiP overlay is missing')
        box=[min(x for x,y in changed),min(y for x,y in changed),max(x for x,y in changed)+1,max(y for x,y in changed)+1]
        verify_inset_bounds(box)
        result['actualInsetChangedBounds']=box
    else:
        verify_jcut(sorted((x['startFrame'],x['endFrame']) for x in clips),sorted((x['startFrame'],x['endFrame']) for x in audio))
        require(sorted(x['sourceIn'] for x in clips)==[0,TICKS],'J-cut B picture does not use matching source time')
        frame(1.5,'native-a.png');frame(2.5,'native-b.png')
    media=json.loads(r.run('probe','output/review.mp4'));expected=4 if name=='presenter-inset' else 5
    require(media['kind']=='Movie' and abs(media['duration']-expected*TICKS)<=TICKS//25,'Encoded movie duration exceeds one frame tolerance')
    require((media['video']['width'],media['video']['height'])==(320,240),'Encoded dimensions changed')
    require(media['video']['frame_rate']=={'num':25,'den':1},'Encoded frame rate wrong')
    decode=r.work/'decoded';decode.mkdir();original=r.work;r.work=decode
    try:
        imported=native_batch(r,[{'command':'file.import','params':{'paths':['../output/review.mp4']}}]);item=imported[0]['result']['items'][0]
        native_batch(r,[{'command':'file.newSequence','params':{'name':'Decoded','width':320,'height':240,'fps':25}},{'command':'timeline.place','params':{'item':item,'track':'V1','seconds':0,'insert':False,'video':True,'audio':True}}],'scene.fcproj')
        for time in [0.04,expected/2,expected-.08]:
            filename=f'decoded-{time}.png';r.run('--project','scene.fcproj','render','--seconds',str(time),'--out',filename);require(sum(rgb_pixels(r.work/filename)[2])>1000,'Encoded frame did not decode')
        if name=='freeze-explainer':
            selected_mean=mean_rgb(original/'selected-source.png')[0];held=[]
            for time in [2,2.5,2.96]:
                filename=f'hold-decoded-{time}.png';r.run('--project','scene.fcproj','render','--seconds',str(time),'--out',filename);held.append(mean_rgb(r.work/filename)[0])
            require(all(abs(value-selected_mean)<2 for value in held),'Encoded hold lost selected source frame')
            require(mean_rgb(r.work/f'decoded-{expected-.08}.png')[0]>selected_mean+20,'Encoded freeze never resumed motion')
            result['encodedHoldRedMeans']=held
        elif name=='jcut-dialogue':
            for time,reference in [(1.5,'native-a.png'),(2.5,'native-b.png')]:
                filename=f'jcut-decoded-{time}.png';r.run('--project','scene.fcproj','render','--seconds',str(time),'--out',filename)
                require(max(abs(a-b) for a,b in zip(mean_rgb(r.work/filename),mean_rgb(original/reference)))<2,'Encoded J-cut picture boundary changed')
        else:
            for box in [(230,170,290,210),(10,10,80,80)]:
                require(max(abs(a-b) for a,b in zip(mean_rgb(r.work/'decoded-2.0.png',box),mean_rgb(original/'inset.png',box)))<2,'Encoded PiP lost overlay or background')
        if name in ['presenter-inset','jcut-dialogue']:
            r.run('--project','scene.fcproj','export','decoded-audio.wav','--format','wav');rate,values=read_wave(r.work/'decoded-audio.wav')
            times=[(.5,660),(2,660),(3.5,660)] if name=='presenter-inset' else [(.5,440),(1.5,880),(3,880),(4.5,880)]
            result['decodedVoiceWindows']=[verify_voice(rate,values,t,f) for t,f in times]
    finally:r.work=original
    for filename,digest in originals.items():require(hashlib.sha256((r.work/filename).read_bytes()).hexdigest()==digest,'Scenario modified a source input')
    return result

def run_delivery(r,skills):
    original=r.work;results=[]
    try:
        for name in sorted(SCENES):
            r.work=original/name;r.work.mkdir();results.append(run_recipe(r,json.loads((Path(skills)/('filmcraft-'+name)/'references/craft-steps.json').read_text(encoding='utf-8'))))
    finally:r.work=original
    return results
