"""执行字幕技能原脚本，覆盖精度补偿、正负偏移及非目标轨道保护。"""
import importlib.util
import json
from pathlib import Path
from craft_cli_windows import require
from film_playbook_smoke import avi_fixture, native_batch
from photo_playbook_smoke import rgb_pixels


def run_subtitle_sync(r, skills):
    script=Path(skills)/'filmcraft-subtitle-delivery/scripts/sync_srt.py'
    spec=importlib.util.spec_from_file_location('film_subtitle_skill',script)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.execute=lambda cli,*args:r.run(*args)
    original=r.work;r.work=original/'subtitle-precision';r.work.mkdir()
    before=len(r.calls)
    try:
        source=r.work/'input.srt'
        source.write_text('1\n00:00:00,523 --> 00:00:01,487\n第一句\nHello.\n\n2\n00:00:01,601 --> 00:00:02,569\n第二句 & sample\n\n3\n00:00:02,701 --> 00:00:03,203\n最后一句\n',encoding='utf-8-sig')
        avi_fixture(r.work/'interview.avi')
        rows=native_batch(r,[{'command':'file.import','params':{'paths':['interview.avi']}}])
        item=rows[0]['result']['items'][0]
        created=native_batch(r,[
            {'command':'file.newSequence','params':{'name':'Subtitle source','width':320,'height':180,'fps':25}},
            {'command':'source.open','params':{'item':item}},
            {'command':'markers.markIn','params':{'target':'source','frame':0}},
            {'command':'markers.markOut','params':{'target':'source','frame':99}},
            {'command':'source.insert','params':{}},
            {'command':'captions.newTrack','params':{'name':'Reference','language':'en'}},
            {'command':'captions.add','params':{'track':'C1','text':'Unchanged reference','seconds':0,'durationSeconds':.4}},
            {'command':'captions.setTrack','params':{'track':'C1','enabled':False}},
        ],'scene.fcproj')
        project=r.work/'scene.fcproj';results=[];reference=created[5]['result']['track']
        baseline=r.work/'frame-zero-before.png'
        r.run('--project',str(project),'render','--seconds','0','--out',str(baseline))
        for name,offset in [('later',500),('earlier',-500)]:
            result=module.sync(r.exe,source,r.work/name,offset,project)
            require(result['precisionRepairOperations']==6,'Odd-ms fixture did not exercise precision restoration')
            require(result['targetTrack']!=reference,'Target should be returned import ID rather than existing reference ID')
            render_root=r.work
            try:
                r.work=render_root/name
                r.run('--project','synced.fcproj','render','--seconds','0','--out','frame-zero.png')
            finally:r.work=render_root
            require(rgb_pixels(baseline)==rgb_pixels(render_root/name/'frame-zero.png'),'Media changed or failed to reopen from delivery directory')
            result['unrelatedWorkingDirectoryRender']='PASS'
            results.append(result)
        standalone=module.sync(r.exe,source,r.work/'standalone',500)
        count=len(r.calls)
        try:module.sync(r.exe,source,r.work/'invalid-negative',-1000,project)
        except ValueError as error:require('zero' in str(error),'Wrong negative offset rejection')
        else:raise AssertionError('Negative start accepted')
        require(count==len(r.calls) and not (r.work/'invalid-negative').exists(),'Rejected offset touched CLI/output')
        return {'variants':results,'standalone':standalone,'nativeProcesses':len(r.calls)-before,
                'negativeRejectedBeforeCli':True,'scope':'known offset and synthetic timeline; no ASR or speech synchronization judgement'}
    finally:r.work=original
