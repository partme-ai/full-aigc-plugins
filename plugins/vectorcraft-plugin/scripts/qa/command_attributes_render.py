#!/usr/bin/env python3
"""属性交付检查：艺术像素保全、真实面板状态与实际SVG链接绑定。"""
import argparse,hashlib,importlib.util,json,re
from pathlib import Path
import xml.etree.ElementTree as ET
COMMANDS=['attributes.info','attributes.set'];CHANGED=set();MEASURED=set()
def load(name):
 s=importlib.util.spec_from_file_location('attribute_render_'+name,Path(__file__).with_name(name+'.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def base():
 m=load('command_layer_render');m.COMMANDS=COMMANDS;m.CHANGED=CHANGED;m.MEASURED=MEASURED;return m
def expectation(command,kind):return base().expectation(command,kind)
def validate_count(count,total,relation):return base().validate_count(count,total,relation)
def validate_links(cases,checks):
 expected=[(c['command'],s) for c in cases for s in c['stages']]
 if len(checks)!=len(expected):raise ValueError('attributes_svg_coverage')
 for row,(command,stage) in zip(checks,expected):
  observed=stage['observed'];expected_path=str(Path(stage['exports'][0]['path']).parent/'attribute-links.svg')
  if stage['ui']['ui']['open_panel']!='attributes' or stage['ui']['ui']['dock'] is not True:raise ValueError('attributes_panel_state')
  if row['command']!=command or row['round']!=stage['round'] or row['sha256']!=observed['svgSha256'] or row['links']!=observed['svgLinks'] or row['path']!=expected_path or row['decoded'] is not True or observed['svgDecoded'] is not True or observed['svgPath']!='attribute-links.svg' or not re.fullmatch('[0-9a-f]{64}',row['sha256']):raise ValueError('attributes_svg_binding')
def checkbox_rows(stage):
 m=load('command_attributes');e,urls,_=m.expected('attributes.set' if 'overprintFill' in stage['params'] else 'attributes.info',stage['before'],stage['params'],stage['fixture']);values=m.info(e,{},stage['fixture'],urls)
 return [{'field':key,'value':values[key],'roi':[x,159,13,13],'dashRoi':[x+3,163,7,4]} for key,x in (('overprintFill',851),('overprintStroke',951))]
def validate_checkboxes(cases,rows):
 expected=[(c['command'],s,row) for c in cases for s in c['stages'] for row in checkbox_rows(s)]
 if len(rows)!=len(expected):raise ValueError('attributes_checkbox_coverage')
 for measured,(command,stage,row) in zip(rows,expected):
  scale=stage['window']['pixelScale']
  if {k:measured[k] for k in row}!=row or measured['command']!=command or measured['round']!=stage['round'] or measured['windowSha256']!=stage['window']['sha256'] or measured['pixelScale']!=scale:raise ValueError('attributes_checkbox_binding')
  blue,dash=measured['bluePixels'],measured['dashPixels']
  if type(blue) is not int or type(dash) is not int or not 0<=blue<=169*scale*scale or not 0<=dash<=28*scale*scale:raise ValueError('attributes_checkbox_samples')
  if row['value'] is True:
   if blue<16*scale*scale:raise ValueError('attributes_checkbox_state')
  elif blue!=0 or (row['value'] is None and dash<3*scale*scale) or (row['value'] is False and dash!=0):raise ValueError('attributes_checkbox_state')
def qualify_checkboxes(root,proof):
 from PIL import Image
 rows=[]
 for case in proof['cases']:
  for stage in case['stages']:
   record=stage['window'];relative=Path(record['path']);path=root/relative;scale=record['pixelScale']
   if relative.is_absolute() or '..' in relative.parts or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()) or hashlib.sha256(path.read_bytes()).hexdigest()!=record['sha256']:raise ValueError('attributes_checkbox_identity')
   with Image.open(path) as raw:
    raw.load()
    if raw.size!=(1440*scale,900*scale):raise ValueError('attributes_checkbox_size')
    im=raw.convert('RGB')
    for row in checkbox_rows(stage):
     def pixels(box):
      x,y,w,h=box
      return [im.getpixel((i,j)) for i in range(x*scale,(x+w)*scale) for j in range(y*scale,(y+h)*scale)]
     blue=sum(b>150 and b>r+30 and g>r+5 for r,g,b in pixels(row['roi']));dash=sum(min(r,g,b)>140 and max(r,g,b)-min(r,g,b)<10 for r,g,b in pixels(row['dashRoi']));rows.append({**row,'command':case['command'],'round':stage['round'],'windowSha256':record['sha256'],'pixelScale':scale,'bluePixels':blue,'dashPixels':dash})
 validate_checkboxes(proof['cases'],rows);return rows

def qualify(root):
 p=root/'proof.json';proof=json.loads(p.read_text());result=base().qualify(root,p);checks=[]
 for case in proof['cases']:
  for stage in case['stages']:
   relative=Path(stage['exports'][0]['path']).parent/'attribute-links.svg';path=root/relative
   if relative.is_absolute() or '..' in relative.parts or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):raise ValueError('attributes_svg_path')
   data=path.read_bytes();links=sorted(e.get('href',e.get('{http://www.w3.org/1999/xlink}href')) for e in ET.fromstring(data).iter() if e.tag.split('}')[-1]=='a');checks.append({'command':case['command'],'round':stage['round'],'path':str(relative),'sha256':hashlib.sha256(data).hexdigest(),'decoded':True,'links':links})
 validate_links(proof['cases'],checks);result['svgLinkChecks']=checks;result['checkboxChecks']=qualify_checkboxes(root,proof);result['schema']='vectorcraft-command-attributes-render/v1';result['checkerSha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();result['scope']='6 canvas/PNG/window comparisons preserve artwork;4 actual Attributes-panel windows and8 model-derived checked/mixed/unchecked checkbox pixel checks,4 independently decoded SVG hyperlink checks;normal rendering only,no overprint print simulation or creative/fullV1';return result
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);a=p.parse_args();result=qualify(a.root);(a.root/'render-changes.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'result':'PASS','comparisons':6,'svgLinkChecks':len(result['svgLinkChecks'])}))
