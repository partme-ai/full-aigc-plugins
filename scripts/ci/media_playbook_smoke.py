"""用原生 CLI 验证音频样本和照片库往返；合成素材不代替真实试听/画质验收。"""
import hashlib
import json
import math
from pathlib import Path
import struct
import wave
import zlib
from photo_playbook_smoke import rgb_pixels


def require(ok,message):
    if not ok:raise AssertionError(message)


def audio_fixture(path,stereo=False):
    rate=48000;frames=rate*4;channels=2 if stereo else 1
    with wave.open(str(path),'wb') as f:
        f.setparams((channels,2,rate,frames,'NONE','not compressed'))
        out=bytearray()
        for i in range(frames):
            t=i/rate
            if stereo:values=[0.16*math.sin(2*math.pi*220*t),0.08*math.sin(2*math.pi*660*t)]
            else:values=[0.08+(0.22-0.025*t)*math.sin(2*math.pi*440*t)+0.035*math.sin(2*math.pi*997*t)]
            for value in values:out+=struct.pack('<h',round(value*32767))
        f.writeframes(out)


def wave_data(path):
    with wave.open(str(path),'rb') as f:
        require(f.getsampwidth()==2,'Test requires actual 16-bit PCM output')
        channels=f.getnchannels();rate=f.getframerate();n=f.getnframes()
        raw=struct.unpack('<'+'h'*(n*channels),f.readframes(n))
        return rate,[[raw[i*channels+c]/32768 for i in range(n)] for c in range(channels)]


def verify_audio(data,baseline,original,assertion):
    rate,channels=data;br,bch=baseline
    require(rate==48000 and br==48000,'Sample rate changed unexpectedly')
    require(all(len(c)==round(assertion['seconds']*rate) for c in channels),'Export duration/frame count mismatch')
    require(len(channels)==len(bch),'Mix output channel count changed')
    check=assertion['check'];peak=max(abs(x) for c in channels for x in c);bp=max(abs(x) for c in bch for x in c)
    require(peak<0.9999,'Output clipping')
    if check=='gain':require(abs(peak/bp-10**(assertion['db']/20))<0.002,'Clip gain did not affect rendered audio')
    elif check=='normalize':
        ip=max(abs(x) for c in original[1] for x in c)
        require(abs(peak/bp-10**(assertion['targetDb']/20)/ip)<0.005,'Peak normalization target not applied')
    elif check in {'reverse','invert','excerpt'}:
        errors=[]
        for c,base in zip(channels,bch):
            expected=list(reversed(base)) if check=='reverse' else [-x for x in base] if check=='invert' else base[round(assertion['offset']*rate):round((assertion['offset']+assertion['seconds'])*rate)]
            require(len(c)==len(expected),'Reference sample count mismatch')
            errors.append(sum(abs(a-b) for a,b in zip(c,expected))/len(c))
        require(max(errors)<0.00015,'Rendered sample content did not match '+check)
    elif check=='dc-offset':
        old=abs(sum(bch[0][-rate:])/rate);new=abs(sum(channels[0][-rate:])/rate)
        require(old>0.01 and new<old*0.1,'DC bias was not removed from stable audio')
    elif check=='fades':
        rms=lambda x:math.sqrt(sum(v*v for v in x)/max(1,len(x)))
        edge=rate//100
        require(rms(channels[0][:edge])<rms(bch[0][:edge])*0.2,'Head fade not rendered')
        require(rms(channels[0][-edge:])<rms(bch[0][-edge:])*0.2,'Tail fade not rendered')
        a=channels[0][rate:rate*3];b=bch[0][rate:rate*3]
        require(sum(abs(x-y) for x,y in zip(a,b))/len(a)<0.00015,'Edge fade changed protected middle')
    else:raise ValueError('Unknown audio result check '+check)


def sound(r,data):
    audio_fixture(r.work/'input.wav');audio_fixture(r.work/'bed.wav',True)
    original=wave_data(r.work/'input.wav');hashes={f:hashlib.sha256((r.work/f).read_bytes()).hexdigest() for f in ['input.wav','bed.wav']}
    init=data['recipes'][0]['steps'][:4]
    def run(steps,target):
        args=['run']
        for s in steps:args+=['--cmd',s['command']+'='+json.dumps(s['params'],ensure_ascii=False,separators=(',',':'))]
        return r.run(*args,'--save',target)
    bounce=lambda path,start=0,end=4:{'path':path,'format':'wav','bit_depth':16,'start':{'seconds':start},'end':{'seconds':end},'normalize':False,'dither':False}
    run(init+[{'command':'file.bounce_mix','params':bounce('baseline.wav')}],'baseline.scraft')
    baseline=wave_data(r.work/'baseline.wav');records=[]
    for recipe in data['recipes']:
        target=recipe['id']+'.scraft';run(recipe['steps'],target)
        r.run('info',target)
        assertion=recipe['assertions']
        if assertion['check']=='stems':
            files=sorted((r.work/'stems').glob('*.wav'))
            track_name=lambda p:p.stem.rsplit(' - ',1)[-1].lower()
            require(len(files)==2 and {track_name(p) for p in files}=={'voice','bed'},'Stem track-name set mismatch')
            for p in files:
                rate,ch=wave_data(p);require(rate==48000 and all(len(x)==192000 for x in ch),'Stem rate/duration changed')
                if track_name(p)=='bed':require(len(ch)==2 and sum(abs(a-b) for a,b in zip(*ch))/len(ch[0])>0.01,'Stereo bed collapsed')
            r.run('run','--in',target,'--cmd','file.bounce_stems='+json.dumps({'dir':'reopened-stems','format':'wav','bit_depth':16,'start':{'seconds':0},'end':{'seconds':4}}))
            reopened=sorted((r.work/'reopened-stems').glob('*.wav'))
            require({track_name(p) for p in reopened}=={'voice','bed'},'Reopened stem tracks lost')
            for first,second in zip(files,reopened):
                rate,a=wave_data(first);other_rate,b=wave_data(second)
                require(rate==other_rate and len(a)==len(b) and all(len(x)==len(y) for x,y in zip(a,b)),'Reopened stem geometry changed')
                require(max(sum(abs(x-y) for x,y in zip(c,d))/len(c) for c,d in zip(a,b))<0.00015,'Reopened stem content changed beyond dither tolerance')
        else:
            first=wave_data(r.work/'result.wav');verify_audio(first,baseline,original,assertion)
            a=bounce('reopened.wav',assertion.get('offset',0),assertion.get('offset',0)+assertion['seconds'])
            r.run('run','--in',target,'--cmd','file.bounce_mix='+json.dumps(a))
            second=wave_data(r.work/'reopened.wav');verify_audio(second,baseline,original,assertion)
            require(first==second,'Saved audio editing state changed after reopen')
            (r.work/'result.wav').replace(r.work/(recipe['id']+'.wav'))
        require(all(hashlib.sha256((r.work/f).read_bytes()).hexdigest()==h for f,h in hashes.items()),'Source audio changed')
        records.append({'id':recipe['id'],'technicalRoundtrip':'PASS','signalChecks':'PASS','auditoryAcceptance':'NOT_TESTED'})
    return records


def image_fixture(path,alternate=False):
    def chunk(kind,data):return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))
    rows=[]
    for y in range(48):
        row=bytearray()
        for x in range(64):
            rgb=(50+x*2,60+y*2,90) if not alternate else (90,40+x*2,70+y*2)
            if 12<=x<21 and 19<=y<29:rgb=(180,145,110)
            row.extend(rgb)
        rows.append(b'\0'+row)
    path.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',64,48,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(b''.join(rows)))+chunk(b'IEND',b''))


def light(r,data):
    image_fixture(r.work/'input.png');image_fixture(r.work/'second.png',True)
    input_hash=hashlib.sha256((r.work/'input.png').read_bytes()).hexdigest()
    def run(library,steps,imports=()):
        args=['run','--library',library]
        for path in imports:args+=['--import',path]
        return [json.loads(row) for row in r.run(*args,'--script','-',stdin='\n'.join(json.dumps({'command':x['command'],'params':x['params']},ensure_ascii=False) for x in steps)+'\n').splitlines()]
    base_export={'command':'app.export','params':{'path':'baseline.png','format':'png','bitDepth':8,'longEdge':0,'dontEnlarge':True,'colorSpace':'srgb','metadata':'none'}}
    run('baseline-library',[base_export],['input.png']);base=rgb_pixels(r.work/'baseline.png');records=[]
    controls=r.run('controls','--json');(r.output/'develop-controls.json').write_text(controls,encoding='utf-8')
    for recipe in data['recipes']:
        library='library-'+recipe['id'];a=recipe['assertions'];rows=run(library,recipe['steps'],a.get('inputFiles',['input.png']))
        reopen=run(library,[{'command':'develop.get','params':{}}])[-1]['result']
        for key,value in a.get('settings',{}).items():
            actual=reopen
            for part in key.split('.'):actual=actual[part]
            require(actual==value,'Develop setting not persisted: '+key)
        if 'contactPhotos' in a:
            result=next(x['result'] for x in rows if x['command']=='export.contactSheet')
            require(result['photos']==a['contactPhotos'] and result['pages']==a['contactPages'],'Contact sheet selection/count wrong')
            require((r.work/'contact.pdf').read_bytes().startswith(b'%PDF'),'Contact sheet not PDF')
        elif a.get('dualExport'):
            require(rgb_pixels(r.work/'screen.png')[:2]==(64,48),'Screen export resized unexpectedly')
            tiff=(r.work/'print.tif').read_bytes();require(tiff[:4] in (b'II*\x00',b'MM\x00*'),'Print export not TIFF')
            # 用TIFF IFD的BitsPerSample标签检查真正的16位通道。
            endian='<' if tiff[:2]==b'II' else '>';offset=struct.unpack_from(endian+'I',tiff,4)[0];n=struct.unpack_from(endian+'H',tiff,offset)[0];bits=None
            for i in range(n):
                tag,kind,count,value=struct.unpack_from(endian+'HHII',tiff,offset+2+i*12)
                if tag==258:
                    bits=[value&65535] if count==1 else list(struct.unpack_from(endian+'H'*count,tiff,value))
            require(bits and all(x==16 for x in bits),'TIFF channel depth not 16 bit')
        else:
            w,h,pixels=rgb_pixels(r.work/'result.png')
            require((w,h)==tuple(a.get('dimensions',[64,48])),'Develop output geometry mismatch')
            if a.get('pixelChange'):require(sum(abs(x-y) for x,y in zip(pixels,base[2]))>100,'Develop operation had no rendered effect')
            if a.get('grayscale'):require(max(max(pixels[i:i+3])-min(pixels[i:i+3]) for i in range(0,len(pixels),3))<=2,'Black-and-white output still colored')
            if 'neutralPoint' in a:
                x,y=a['neutralPoint'];idx=(y*w+x)*3
                old=base[2][idx:idx+3];new=pixels[idx:idx+3]
                require(max(new)-min(new)<max(old)-min(old)-5,'Gray-card correction did not reduce channel imbalance')
            export=next(x for x in recipe['steps'] if x['command']=='app.export')
            reopened_path='reopened-'+recipe['id']+'.png'
            params=dict(export['params'],path=reopened_path)
            run(library,[{'command':'app.export','params':params}])
            require(rgb_pixels(r.work/reopened_path)==(w,h,pixels),'Saved photo edit changed after library reopen')
            (r.work/'result.png').replace(r.work/(recipe['id']+'.png'))
        require(hashlib.sha256((r.work/'input.png').read_bytes()).hexdigest()==input_hash,'Original photo changed')
        records.append({'id':recipe['id'],'technicalRoundtrip':'PASS','renderOrStructureChecks':'PASS','creativeAcceptance':'NOT_TESTED'})
    return records


def run_playbooks(r,path,app):
    data=json.loads(Path(path).read_text(encoding='utf-8'));require(data['application']==app,'Wrong media scenario application')
    if app == 'soundcraft':
        records = sound(r, data)
        from sound_core_smoke import run_core
        from sound_more_core_smoke import run_more_core
        from sound_production_smoke import run_production
        root = Path(path).resolve().parents[2]
        return records + run_core(r, root) + run_more_core(r, root) + run_production(r, root)
    records = light(r, data)
    from light_core_smoke import run_core as run_light_core
    return records + run_light_core(r, Path(path).resolve().parents[2])
