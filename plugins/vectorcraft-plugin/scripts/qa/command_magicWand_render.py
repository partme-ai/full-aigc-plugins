#!/usr/bin/env python3
"""固定魔棒面板五项复选框像素和艺术导出保全验收。"""
import argparse,hashlib,importlib.util,json
from pathlib import Path
COMMANDS=['magicWand.set','magicWand.options']
CHANGED=set();MEASURED=set()
ROWS=[('fillColor',159),('strokeColor',209),('strokeWeight',241),('opacity',291),('blendingMode',323)]
def load(name):
 s=importlib.util.spec_from_file_location('wand_pixel_'+name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def base():
 m=load('command_layer_render');m.COMMANDS=COMMANDS;m.CHANGED=CHANGED;m.MEASURED=MEASURED;return m
def expectation(command,kind):return base().expectation(command,kind)
def validate_count(count,total,relation):return base().validate_count(count,total,relation)
def expected_settings(command,stage):
 m=load('command_magicWand');f=stage['fixture'];return m.expected(f['settingsBefore'],stage['params']) if command=='magicWand.set' else f['settingsBefore']
def validate_checks(cases,checks):
 expected=[(c['command'],s,k,y) for c in cases for s in c['stages'] for k,y in ROWS]
 if len(checks)!=len(expected):raise ValueError('wand_pixels_coverage')
 for row,(command,s,k,y) in zip(checks,expected):
  scale=s['window']['pixelScale'];want=expected_settings(command,s)[k]
  if any(row[key]!=v for key,v in dict(command=command,round=s['round'],field=k,value=want,roi=[851,y,13,13],pixelScale=scale,windowSha256=s['window']['sha256']).items()):raise ValueError('wand_pixels_binding')
  count=row['bluePixels']
  if type(count) is not int or not 0<=count<=169*scale*scale or (want and count<16*scale*scale) or (not want and count!=0):raise ValueError('wand_pixels_state')
def qualify(root):
 from PIL import Image
 p=root/'proof.json';proof=json.loads(p.read_text());result=base().qualify(root,p);checks=[]
 for c in proof['cases']:
  for s in c['stages']:
   r=s['window'];rel=Path(r['path']);path=root/rel;scale=r['pixelScale'];want=expected_settings(c['command'],s)
   if rel.is_absolute() or '..' in rel.parts or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()) or hashlib.sha256(path.read_bytes()).hexdigest()!=r['sha256']:raise ValueError('wand_pixels_identity')
   with Image.open(path) as raw:
    raw.load()
    if raw.size!=(1440*scale,900*scale):raise ValueError('wand_pixels_size')
    im=raw.convert('RGB')
    for k,y in ROWS:
     pixels=[im.getpixel((x,j)) for x in range(851*scale,864*scale) for j in range(y*scale,(y+13)*scale)];count=sum(b>150 and b>r+30 and g>r+5 for r,g,b in pixels);checks.append(dict(command=c['command'],round=s['round'],field=k,value=want[k],roi=[851,y,13,13],pixelScale=scale,windowSha256=r['sha256'],bluePixels=count))
 validate_checks(proof['cases'],checks);result.update(schema='vectorcraft-command-magic-wand-render/v1',checkerSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),checkboxChecks=checks,scope='6 measured image comparisons,artwork preserved;20 independent settings-derived checkbox checks on owned1440x900 windows;not GUI text OCR,app restart,selection matching or fullV1');return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);a=p.parse_args();result=qualify(a.root);(a.root/'render-changes.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'result':'PASS','comparisons':6,'checkboxChecks':len(result['checkboxChecks'])}))
