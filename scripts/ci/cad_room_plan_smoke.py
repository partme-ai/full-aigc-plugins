"""实际CADCraft CLI执行房间计划，重开核对门洞、墙线和原生尺寸。"""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
from craft_cli_windows import Runner,require


def verify(drawing,data):
    width,depth,start,door=[data[k] for k in ('width','depth','door_start','door_width')]
    expected=[]
    if start>0:expected.append((0,0,start,0))
    if start+door<width:expected.append((start+door,0,width,0))
    expected += [(width,0,width,depth),(width,depth,0,depth),(0,depth,0,0)]
    walls=[e for e in drawing['entities'] if e['layer']=='WALLS'];require(all(e['type']=='Line' for e in walls),'Non-line wall entity')
    actual=[tuple(e['geometry'][point][axis] for point,axis in [('a','x'),('a','y'),('b','x'),('b','y')]) for e in walls]
    require(sorted(actual)==sorted(expected),'Walls close the door gap or dimensions changed')
    leaves=[e['geometry'] for e in drawing['entities'] if e['layer']=='DOOR' and e['type']=='Line']
    require(len(leaves)==1 and leaves[0]['a']['x']==start and leaves[0]['a']['y']==0 and leaves[0]['b']['x']==start and leaves[0]['b']['y']==door,'Door leaf geometry changed')
    arcs=[e['geometry'] for e in drawing['entities'] if e['type']=='Arc'];require(len(arcs)==1,'Expected one door swing')
    arc=arcs[0];require(arc['center']['x']==start and arc['center']['y']==0 and arc['radius']==door and arc['start']==0 and math.isclose(arc['end'],math.pi/2),'Door swing geometry changed')
    dims=[e['geometry'] for e in drawing['entities'] if e['type']=='Dimension'];require(len(dims)==2 and sorted(d['measurement'] for d in dims)==sorted([width,depth]),'Dimensions do not match room')
    require(all(not d['text'] for d in dims),'Dimension text override hides true measurement')
    labels=[e['geometry']['value'] for e in drawing['entities'] if e['type']=='Text'];require(labels==[data['label']],'Room label changed')


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    g=p.add_mutually_exclusive_group(required=True);g.add_argument('--cli',type=Path);g.add_argument('--runtime-root',type=Path);a=p.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False);exe=a.cli.resolve() if a.cli else None
    if a.runtime_root:
        matches=list(a.runtime_root.resolve().rglob('cadcraft-cli.exe'));require(len(matches)==1,'Expected one verified runtime');exe=matches[0]
        previous=json.loads((a.runtime_root/'result.json').read_text(encoding='utf-8'));require(hashlib.sha256(exe.read_bytes()).hexdigest()==previous['exeSha256'],'Runtime changed')
    source=a.source.resolve()/'skills/cadcraft-floor-plan';s=importlib.util.spec_from_file_location('room_plan',source/'scripts/room_plan.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    sample=json.loads((source/'assets/example-input.json').read_text(encoding='utf-8'));left={**sample,'width':4200,'depth':3000,'door_start':0,'door_width':800};right={**sample,'width':8000,'depth':5000,'door_start':6800,'door_width':1200};work=out/'房间 中文 workspace';work.mkdir();r=Runner(exe,work,out);results=[]
    for name,data in [('sample',sample),('left-edge',left),('right-edge',right)]:
        root=work/name;root.mkdir();inp=root/'input.json';inp.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8');before=inp.read_bytes();plan=m.build_plan(data);(root/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8');args=['run','--metric']
        for c in plan['steps']:args+=['--cmd',c['command']+' '+json.dumps(c['params'],ensure_ascii=True,separators=(',',':'))]
        dxf=root/'room.dxf';r.run(*args,'--save',dxf);text=r.run('run',dxf,'--cmd','drawing.inspect {"entities":true,"limit":2000}');drawing=next(json.loads(line) for line in text.splitlines() if line.startswith('{') and '"entities"' in line);verify(drawing,data)
        (root/'reopened.json').write_text(json.dumps(drawing,ensure_ascii=False,indent=2),encoding='utf-8');r.run('convert',dxf,root/'room.png');r.run('convert',dxf,root/'room.svg');require(inp.read_bytes()==before,'Input changed')
        results.append({'name':name,'wallsDoorAndNativeDimensions':'PASS','labelPreserved':'PASS','inputPreserved':'PASS','visualAcceptance':'NOT_TESTED'})
    result={'status':'PASS','platform':sys.platform,'nativeProcesses':len(r.calls),'variants':results,'installedHostSync':'NOT_TESTED'};(out/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
