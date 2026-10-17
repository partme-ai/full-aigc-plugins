#!/usr/bin/env python3
"""效果两轮图像核验：改变、保全与只测量契约，原生探针另行断言。"""
import argparse,base64,hashlib,importlib.util,io,json,math
from pathlib import Path
import xml.etree.ElementTree as ET
COMMANDS=['effect.'+n for n in ('apply','list','remove','setParams','expandAppearance','duplicate','move')]
CHANGED=set(COMMANDS)-{'effect.list'}
MEASURED=set()
def base():
 s=importlib.util.spec_from_file_location('effect_render_base',Path(__file__).with_name('command_layer_render.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.COMMANDS=COMMANDS;m.CHANGED=CHANGED;m.MEASURED=MEASURED;return m
def expectation(command,kind):return base().expectation(command,kind)
def validate_count(count,total,relation):return base().validate_count(count,total,relation)
def driver():
 s=importlib.util.spec_from_file_location('effect_pixel_contract',Path(__file__).with_name('command_effect.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def image_contract(stage,kind):
 """按固定RasterFx外扩与2pt安全边距计算原生72ppi图像区域。"""
 m=driver();f=stage['fixture'];source=m.shape.find(stage['before'],f[kind]);after=m.shape.find(stage['after'],f[kind]);image=after['kind']['children'][0] if kind=='shadow' else after;params=source['appearance']['effects'][0]['params'];x,y,w,h=m.bounds(source)
 if stage['before']['raster_effects_ppi']!=72:raise ValueError('effect_image_fixture_resolution')
 reach=2+1.5*(params['blur'] if kind=='shadow' else params['radius'])+(max(abs(params['x']),abs(params['y'])) if kind=='shadow' else 0)
 expected={'width':math.ceil(w+2*reach),'height':math.ceil(h+2*reach),'xf':[1,0,0,1,x-reach,y-reach]}
 m.shape.near({k:image['kind'][k] for k in expected},expected,'effect_image_region')
 rgba=[0,0,0,0] if kind=='shadow' else [round(source['appearance']['items'][0]['paint']['color'][k]*255) for k in ('r','g','b')]+[255]
 return {'kind':kind,'modelImageKey':image['kind']['key'],'sourceObjectID':source['id'],'sourceBounds':[x,y,w,h],**expected,'centerRGBA':rgba,'cornerAlpha':0}
def validate_expanded_images(cases,measurements):
 stage=next(c['stages'][1] for c in cases if c['command']=='effect.expandAppearance')
 if [m['kind'] for m in measurements]!=['shadow','blur']:raise ValueError('effect_image_checks_coverage')
 for row in measurements:
  expected=image_contract(stage,row['kind'])
  driver().shape.near({k:row[k] for k in expected},expected,'effect_image_pixel_contract')
  if row['svgSha256']!=stage['observed']['embeddedSvgSha256'] or row['decoded'] is not True or row['unexpectedColorPixels']!=0 or row['nonzeroInteriorPixels']!=0:raise ValueError('effect_image_pixel_binding')
  source=next((m for m in stage['observed']['embeddedImages'] if m['sha256']==row['sha256']),None)
  if source is None or (row['width'],row['height'],row['nontransparentPixels'],row['translucentPixels'])!=(source['width'],source['height'],source['nontransparentPixels'],source['translucentPixels']):raise ValueError('effect_image_pixel_binding')
def embedded_path(stage):return Path(stage['exports'][0]['path']).parent/'expanded-images.svg'
def qualify_images(root,proof):
 from PIL import Image
 report=json.loads(Path(proof).read_text());stage=next(c['stages'][1] for c in report['cases'] if c['command']=='effect.expandAppearance');relative=embedded_path(stage);path=root/relative
 if relative.is_absolute() or '..' in relative.parts or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):raise ValueError('effect_image_source_path')
 digest=hashlib.sha256(path.read_bytes()).hexdigest()
 if digest!=stage['observed']['embeddedSvgSha256']:raise ValueError('effect_image_svg_changed')
 decoded=[]
 for element in ET.fromstring(path.read_bytes()).iter():
  if element.tag.split('}')[-1]!='image':continue
  href=element.get('href',element.get('{http://www.w3.org/1999/xlink}href',''))
  if not href.startswith('data:image/png;base64,'):raise ValueError('effect_image_encoding')
  data=base64.b64decode(href.split(',',1)[1],validate=True)
  with Image.open(io.BytesIO(data)) as im:im.load();decoded.append((hashlib.sha256(data).hexdigest(),im.convert('RGBA').copy()))
 rows=[]
 for kind in ('shadow','blur'):
  expected=image_contract(stage,kind);matches=[(sha,im) for sha,im in decoded if im.size==(expected['width'],expected['height'])]
  if len(matches)!=1:raise ValueError('effect_image_pixel_binding')
  sha,im=matches[0];pixels=list(im.getdata());alpha=[p[3] for p in pixels];center=im.getpixel((im.width//2,im.height//2));bad=interior=tinted=0
  if kind=='shadow':
   x,y,w,h=expected['sourceBounds'];ox,oy=expected['xf'][4:]
   for j in range(im.height):
    for i in range(im.width):
     px=im.getpixel((i,j));dx,dy=ox+i+.5,oy+j+.5
     # 源码按覆盖扣除原艺术，半像素边界保留抗锯齿源色；外侧阴影必须黑，内部必须空。
     outside=dx<x-.5 or dx>x+w+.5 or dy<y-.5 or dy>y+h+.5
     inside=x+.5<dx<x+w-.5 and y+.5<dy<y+h-.5
     colored=px[3]>0 and px[:3]!=(0,0,0)
     bad+=outside and colored;interior+=inside and px[3]>0;tinted+=colored and not outside

  rows.append({**expected,'centerRGBA':list(center),'cornerAlpha':im.getpixel((0,0))[3],'sha256':sha,'svgSha256':digest,'decoded':True,'unexpectedColorPixels':bad,'nonzeroInteriorPixels':interior,'antialiasEdgeTintPixels':tinted,'nontransparentPixels':sum(a>0 for a in alpha),'translucentPixels':sum(0<a<255 for a in alpha)})
 validate_expanded_images(report['cases'],rows);return rows
def qualify(root,proof):
 result=base().qualify(root,proof);result['expandedImageChecks']=qualify_images(root,proof);result['schema']='vectorcraft-command-effect-render/v1';result['checkerSha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();result['scope']='Actual21 canvas/PNG/window comparisons for7 effect commands;explicit preservation/change/measurement contracts;geometry/raster/type/container expansion independently checked;not all effect variants,creative or full V1';return result
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('root',type=Path);args=parser.parse_args();result=qualify(args.root,args.root/'proof.json');(args.root/'render-changes.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'result':'PASS','commands':len(result['cases']),'comparisons':21}))
