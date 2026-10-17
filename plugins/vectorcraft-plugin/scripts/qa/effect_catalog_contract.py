#!/usr/bin/env python3
"""从固定上游源码提取独立效果目录；只读源码，不读取原生查询结果。"""
import argparse,hashlib,json,re
from pathlib import Path

COMMIT='90e022b0c05f12171a4e9bebe0894fa62f7bc95c'

def split_args(text):
 """忽略字符串内分隔符，按顶层逗号拆分Rust静态表达式。"""
 out=[];start=0;depth=0;quoted=False;escape=False
 for i,c in enumerate(text):
  if quoted:
   if escape:escape=False
   elif c=='\\':escape=True
   elif c=='"':quoted=False
  elif c=='"':quoted=True
  elif c in '([{':depth+=1
  elif c in ')]}':depth-=1
  elif c==',' and depth==0:out.append(text[start:i].strip());start=i+1
 if text[start:].strip():out.append(text[start:].strip())
 if quoted or depth:raise ValueError('effect_contract_syntax')
 return out

def lengths(id):
 always={
 'convertToShape.rectangle':['extraW','extraH','width','height'],
 'convertToShape.ellipse':['extraW','extraH','width','height'],
 'convertToShape.roundedRectangle':['extraW','extraH','width','height','radius'],
 'distort.transform':['moveH','moveV'],'path.offsetPath':['offset'],'path.outlineStroke':['width'],
 'stylize.roundCorners':['radius'],'stylize.feather':['radius'],'blur.gaussian':['radius'],
 'stylize.scribble':['overlap','strokeWidth','spacing','variation'],'stylize.dropShadow':['x','y','blur'],
 'stylize.innerGlow':['blur'],'stylize.outerGlow':['blur']}
 return {'always':always.get(id,[]),'absolute':['size'] if id in ('distort.roughen','distort.zigZag') else ['h','v'] if id=='distort.tweak' else []}

def extract(lib,group,marks):
 """返回与EffectInfo字段对应的完整目录；拒绝未识别静态表达式。"""
 aliases={name:json.loads(value) for name,value in re.findall(r'const (\w+): &\[&str\] = &(\[[^;]+\]);',lib)}
 aliases['WARP_DOC']=json.loads(re.search(r'const WARP_DOC: &str\s*=\s*("(?:\\.|[^"\\])*");',lib).group(1))
 aliases['CROP_MARKS']=json.loads(re.search(r'pub const CROP_MARKS: &str = ("[^"]+");',marks).group(1))
 def value(v):
  if v in aliases:return aliases[v]
  if v.startswith('&['):v=v[1:]
  if v.startswith('json!(') and v.endswith(')'):v=v[6:-1]
  return json.loads(v)
 def row(expr):
  kind=expr[0];args=split_args(expr[2:-1]);id,label,menu,params,defaults=map(value,args)
  return {'id':id,'label':label,'menu':menu,'params':params,'defaults':defaults,'raster':kind=='r','lengths':lengths(id)}
 block=lib.split('let mut v = vec![',1)[1].split('\n    ];',1)[0]
 catalog=[row(expr) for expr in split_args(block)]
 warp_block=lib.split('pub const WARP_STYLES:',1)[1].split('= [',1)[1].split('];',1)[0]
 for suffix,label in re.findall(r'\("([^"]+)", "([^"]+)"\)',warp_block):
  id='warp.'+suffix;catalog.append({'id':id,'label':label,'menu':aliases['WARP'],'params':aliases['WARP_DOC'],'defaults':{'bend':50.0,'horizontal':0.0,'vertical':0.0,'orientation':'horizontal'},'raster':False,'lengths':lengths(id)})
 pathfinder=group.split('pub const PATHFINDER_EFFECTS:',1)[1].split('= [',1)[1].split('];',1)[0]
 for id,label in re.findall(r'\("([^"]+)", "([^"]+)"',pathfinder):
  catalog.append({'id':id,'label':label,'menu':aliases['PATHFINDER'],'params':'{} (groups and layers: live Pathfinder over the members)','defaults':{},'raster':False,'lengths':lengths(id)})
 crop=lib.split('v.push(g(\n        CROP_MARKS,',1)[1].split('\n    ));',1)[0]
 catalog.append(row('g(CROP_MARKS,'+crop+')'))
 if len(catalog)!=len({r['id'] for r in catalog}) or len(catalog)<40:raise ValueError('effect_contract_coverage')
 return catalog

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('lib',type=Path);p.add_argument('group',type=Path);p.add_argument('marks',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
 sources={name:hashlib.sha256(path.read_bytes()).hexdigest() for name,path in [('crates/effects/src/lib.rs',a.lib),('crates/effects/src/group.rs',a.group),('crates/effects/src/marks.rs',a.marks)]}
 result={'schema':'vectorcraft-effect-catalog-contract/v1','repository':'https://github.com/storytold/vectorcraft','sourceCommit':COMMIT,'sourceSha256':sources,'catalog':extract(a.lib.read_text(),a.group.read_text(),a.marks.read_text())}
 a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'catalogEntries':len(result['catalog'])}))
