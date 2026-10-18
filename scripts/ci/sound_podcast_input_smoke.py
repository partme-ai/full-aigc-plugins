"""实际输入助手、非零起点片段、原生保存重开和采样核对。"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from sound_core_smoke import fixture,pcm,close
from sound_more_core_smoke import track_clips

def run_input(r,skill_root):
    skill=Path(skill_root)/'soundcraft-podcast-cleanup'
    fixture(r.work/'voice.wav');fixture(r.work/'other.wav',997)
    (r.work/'审核').mkdir()
    data={'track':'访谈 主轨','startSeconds':1.25,'endSeconds':5.25,'fadeInSeconds':0.02,'fadeOutSeconds':0.05,'gainDb':-2.5,'output':'审核/访谈.wav'}
    (r.work/'input.json').write_text(json.dumps(data),encoding='utf-8')
    result=subprocess.run([sys.executable,str(skill/'scripts/podcast_input.py'),'--input',str(r.work/'input.json'),'--output',str(r.work/'recipe.json')],capture_output=True,text=True)
    assert result.returncode==0,result.stderr
    recipe=json.loads((r.work/'recipe.json').read_text())
    def run(steps,source=None,save=None):
        args=['run']+(['--in',source] if source else [])
        for command,params in steps:args+=['--cmd',command+'='+json.dumps(params,ensure_ascii=False,separators=(',',':'))]
        if save:args+=['--save',save]
        return r.run(*args)
    def bounce(path):return ('file.bounce_mix',{'path':path,'format':'wav','bit_depth':24,'start':{'seconds':1.25},'end':{'seconds':5.25},'normalize':False,'dither':False})
    run([('session.new',{'name':'Input helper fixture','sample_rate':48000,'bit_depth':24,'template':'blank'}),('track.new',{'name':data['track'],'format':'mono','kind':'audio'}),('file.import_audio',{'path':'voice.wav','track':data['track'],'new_tracks':False,'at':{'seconds':1.25}}),('file.import_audio',{'path':'other.wav','track':data['track'],'new_tracks':False,'at':{'seconds':10}})],save='input.scraft')
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [r.work/'voice.wav',r.work/'other.wav',r.work/'input.scraft']}
    before=json.loads((r.work/'input.scraft').read_text());run([bounce('baseline.wav')],source='input.scraft')
    run([(s['command'],s['params']) for s in recipe['steps']],source='input.scraft',save='result.scraft')
    after=json.loads((r.work/'result.scraft').read_text());_,oldclips=track_clips(before,data['track']);_,newclips=track_clips(after,data['track'])
    oldclips=sorted(oldclips,key=lambda c:c['start']);newclips=sorted(newclips,key=lambda c:c['start'])
    assert len(newclips)==2 and oldclips[1]==newclips[1],'Unselected later clip changed'
    clip=newclips[0];assert clip['start']==60000 and clip['length']==192000
    assert clip['fade_in']['len']==960 and clip['fade_out']['len']==2400,'Absolute input fades placed incorrectly'
    sr,width,actual=pcm(r.work/data['output']);base=pcm(r.work/'baseline.wav')[2]
    assert (sr,width,len(actual))==(48000,3,2) and all(len(c)==192000 for c in actual)
    gain=10**(-2.5/20)
    close([c[4800:-4800] for c in actual],[[v*gain for v in c[4800:-4800]] for c in base])
    def energy(c):return sum(v*v for v in c)
    assert all(energy(a[:240])<energy(b[:240])*0.2 and energy(a[-240:])<energy(b[-240:])*0.2 for a,b in zip(actual,base)),'Edge attenuation missing'
    run([bounce('reopened.wav')],source='result.scraft');close(pcm(r.work/'reopened.wav')[2],actual)
    assert all(hashlib.sha256((r.work/name).read_bytes()).hexdigest()==sha for name,sha in hashes.items())
    return {'result':'PASS','scope':'actual generated recipe; offset 1.25s, 4s synthetic clip; unselected later clip preserved','nativeProcesses':len(r.calls),'pcm48k24bitStereo':'PASS','middleGainAndEdgeSamples':'PASS','nativeFadeLengths':'PASS','saveReopenSamples':'PASS','inputsUnchanged':'PASS','auditoryAcceptance':'NOT_TESTED','installedHostSync':'NOT_TESTED'}
