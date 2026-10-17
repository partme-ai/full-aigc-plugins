#!/usr/bin/env python3
"""辅助线交付不进入画布导出，真实窗口按独立坐标检测青色覆盖。"""
import argparse,hashlib,importlib.util,json,math
from pathlib import Path
COMMANDS=['guide.add','guide.remove','guide.move']
CHANGED=set();MEASURED=set()
def load(name):
 s=importlib.util.spec_from_file_location('guide_pixel_'+name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def base():
 m=load('command_layer_render');m.COMMANDS=COMMANDS;m.CHANGED=CHANGED;m.MEASURED=MEASURED;return m
def expectation(command,kind):return base().expectation(command,kind)
def validate_count(count,total,relation):return base().validate_count(count,total,relation)
def checks_for(stage):
 ui=stage['ui'];attempts=stage['uiReadAttempts']
 if ui['view']['fitted'] is not True or stage['uiAfterCapture']!={k:ui[k] for k in ('view','canvasRect')}:raise ValueError('guide_ui_capture_drift')
 if not 1<=len(attempts)<=20 or [x['attempt'] for x in attempts]!=list(range(1,len(attempts)+1)) or [x['status'] for x in attempts]!=['awaiting-fit']*(len(attempts)-1)+['PASS']:raise ValueError('guide_ui_read_attempts')
 if stage['ui']['ui']['view']['guides'] is not True:raise ValueError('guide_visibility')
 after=stage['after']['guides'];rows=[(g,'present') for g in after]+[(g,'absent') for g in stage['before']['guides'] if g not in after]
 return [{'guide':g,'expectation':kind,'coordinate':load('command_guide').screen_coordinate(g,stage['ui'])} for g,kind in rows]
def validate_checks(cases,checks):
 expected=[(c['command'],s,row) for c in cases for s in c['stages'] for row in checks_for(s)]
 if len(checks)!=len(expected):raise ValueError('guide_pixels_coverage')
 for measured,(command,stage,row) in zip(checks,expected):
  if {k:measured[k] for k in ('guide','expectation','coordinate')}!=row or measured['command']!=command or measured['round']!=stage['round'] or measured['windowSha256']!=stage['window']['sha256'] or measured['pixelScale']!=stage['window']['pixelScale']:raise ValueError('guide_pixels_binding')
  count,total=measured['cyanSamples'],measured['totalSamples'];scale=measured['pixelScale'];r=stage['ui']['canvasRect'];axis=1 if row['guide']['vertical'] else 0
  if total!=math.floor((r[axis]+r[axis+2]-8)*scale)-math.ceil((r[axis]+8)*scale) or type(count) is not int or not 0<=count<=total:raise ValueError('guide_pixels_samples')
  if row['expectation']=='present' and count/total<.8 or row['expectation']=='absent' and count/total>.05:raise ValueError('guide_pixels_line')
def qualify_checks(root,proof):
 from PIL import Image
 rows=[]
 for case in proof['cases']:
  for stage in case['stages']:
   record=stage['window'];relative=Path(record['path']);path=root/relative
   if relative.is_absolute() or '..' in relative.parts or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()) or hashlib.sha256(path.read_bytes()).hexdigest()!=record['sha256']:raise ValueError('guide_pixels_identity')
   scale=record['pixelScale'];r=stage['ui']['canvasRect']
   with Image.open(path) as raw:
    raw.load()
    if raw.size!=(1440*scale,900*scale):raise ValueError('guide_pixels_size')
    im=raw.convert('RGB')
    for row in checks_for(stage):
     vertical=row['guide']['vertical'];axis=1 if vertical else 0;lo=math.ceil((r[axis]+8)*scale);hi=math.floor((r[axis]+r[axis+2]-8)*scale);cross=round(row['coordinate']*scale);count=0
     for pos in range(lo,hi):
      for delta in range(-2*scale,2*scale+1):
       x,y=(cross+delta,pos) if vertical else (pos,cross+delta)
       if not 0<=x<im.width or not 0<=y<im.height:raise ValueError('guide_pixels_bounds')
       red,green,blue=im.getpixel((x,y))
       if green>=170 and blue>=170 and green-red>=45 and blue-red>=45:count+=1;break
     rows.append({**row,'command':case['command'],'round':stage['round'],'windowSha256':record['sha256'],'pixelScale':scale,'totalSamples':hi-lo,'cyanSamples':count})
 validate_checks(proof['cases'],rows);return rows

def qualify(root):
 p=root/'proof.json';proof=json.loads(p.read_text());result=base().qualify(root,p);result['guideLineChecks']=qualify_checks(root,proof);result['schema']='vectorcraft-command-guide-render/v1';result['checkerSha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();result['scope']='9 actual canvas/PNG/window comparisons;6 windows with independent guide coordinates and present/absent cyan line coverage;guides preserve exported artwork;not creative/full GUI/V1';return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);a=p.parse_args();result=qualify(a.root);(a.root/'render-changes.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'result':'PASS','comparisons':9,'guideLineChecks':len(result['guideLineChecks'])}))
