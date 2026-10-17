#!/usr/bin/env python3
"""字符样式真实像素验收：非目标保全和独立选中行检查。"""
import argparse,hashlib,importlib.util,json
from pathlib import Path
COMMANDS=['charStyle.'+v for v in ('list','new','apply','redefine','setAttrs','duplicate','rename','delete')]
CHANGED={'charStyle.apply','charStyle.redefine','charStyle.setAttrs'};MEASURED=set()
TARGETS=[[78,44,50,16],[78,76,50,16]]
def load(name):
 s=importlib.util.spec_from_file_location('char_pixels_'+name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def base():
 m=load('command_layer_render');m.COMMANDS=COMMANDS;m.CHANGED=CHANGED;m.MEASURED=MEASURED;return m
def expectation(command,kind):return base().expectation(command,kind)
def validate_count(count,total,relation):return base().validate_count(count,total,relation)
def panel_rows(command,s):
 m=load('command_charStyle');e,_=m.expected(command,s['before'],s['params'],s['fixture']);rows=m.listing(e)['styles'];style=m.shape.find(e,s['fixture']['selection'][0])['kind']['runs'][0]['style'];current=style.get('style_name',m.NORMAL)
 return [{'name':r['name'],'selected':r['name']==current,'roi':[1030,154+27*i,40,20]} for i,r in enumerate(rows)]
def validate_panels(cases,checks):
 expected=[(c['command'],s,row) for c in cases for s in c['stages'] for row in panel_rows(c['command'],s)]
 if len(checks)!=len(expected):raise ValueError('char_style_panel_coverage')
 for row,(command,s,want) in zip(checks,expected):
  scale=s['window']['pixelScale'];bind={**want,'command':command,'round':s['round'],'windowSha256':s['window']['sha256'],'pixelScale':scale}
  if any(row[k]!=v for k,v in bind.items()):raise ValueError('char_style_panel_binding')
  count=row['highlightPixels']
  if type(count) is not int or not 0<=count<=800*scale*scale or (want['selected'] and count<600*scale*scale) or (not want['selected'] and count!=0):raise ValueError('char_style_panel_pixels')
def validate_regions(cases,checks):
 expected=[(c['command'],s,kind) for c in cases for s in c['stages'] for kind in ('native-canvas','png-export')]
 if len(checks)!=len(expected):raise ValueError('char_style_region_coverage')
 for row,(command,s,kind) in zip(checks,expected):
  record=s['canvas'] if kind=='native-canvas' else next(e for e in s['exports'] if e['format']=='png')
  if any(row[k]!=v for k,v in dict(command=command,round=s['round'],kind=kind,sha256=record['sha256'],targetRegions=TARGETS).items()):raise ValueError('char_style_region_binding')
  if row['outsideChangedPixels']!=0 or type(row['outsideChangedPixels']) is not int:raise ValueError('char_style_non_target_pixels')
  if row['referenceSha256']!=next(c['stages'][0]['canvas']['sha256'] if kind=='native-canvas' else next(e['sha256'] for e in c['stages'][0]['exports'] if e['format']=='png') for c in cases if c['command']==command):raise ValueError('char_style_reference_binding')
def decode(root,record,size):
 from PIL import Image
 rel=Path(record['path']);p=root/rel
 if rel.is_absolute() or '..' in rel.parts or p.is_symlink() or not p.resolve().is_relative_to(root.resolve()) or hashlib.sha256(p.read_bytes()).hexdigest()!=record['sha256']:raise ValueError('char_style_pixel_identity')
 with Image.open(p) as im:
  im.load()
  if im.size!=size:raise ValueError('char_style_pixel_size')
  return im.convert('RGB')
def qualify(root):
 p=root/'proof.json';proof=json.loads(p.read_text());result=base().qualify(root,p);panels=[];regions=[]
 for c in proof['cases']:
  reference={}
  for s in c['stages']:
   record=s['window'];scale=record['pixelScale'];im=decode(root,record,(1440*scale,900*scale))
   for row in panel_rows(c['command'],s):
    x,y,w,h=row['roi'];pixels=[im.getpixel((i,j)) for i in range(x*scale,(x+w)*scale) for j in range(y*scale,(y+h)*scale)];count=sum(b>g+8 and g>r+8 and b<160 for r,g,b in pixels);panels.append({**row,'command':c['command'],'round':s['round'],'windowSha256':record['sha256'],'pixelScale':scale,'highlightPixels':count})
   for kind in ('native-canvas','png-export'):
    record=s['canvas'] if kind=='native-canvas' else next(e for e in s['exports'] if e['format']=='png');im=decode(root,record,(128,96))
    if s['round']==1:reference[kind]=(im.copy(),record['sha256'])
    first,digest=reference[kind];count=sum(im.getpixel((x,y))!=first.getpixel((x,y)) for y in range(96) for x in range(128) if not any(rx<=x<rx+w and ry<=y<ry+h for rx,ry,w,h in TARGETS));regions.append(dict(command=c['command'],round=s['round'],kind=kind,sha256=record['sha256'],referenceSha256=digest,targetRegions=TARGETS,outsideChangedPixels=count))
 validate_panels(proof['cases'],panels);validate_regions(proof['cases'],regions);result.update(schema='vectorcraft-command-char-style-render/v1',checkerSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),panelChecks=panels,regionChecks=regions,scope='24 actual canvas/PNG/window comparisons;independent style-derived fixed-layout selection highlights and protected pixels outside two owned text regions;not OCR,decorative-line rendering,all font/layout variants,creative/fullV1');return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);a=p.parse_args();result=qualify(a.root);(a.root/'render-changes.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'result':'PASS','comparisons':24,'panelChecks':len(result['panelChecks']),'regionChecks':len(result['regionChecks'])}))
