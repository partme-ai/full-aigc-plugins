"""执行真实 CADCraft CLI 场景并解析保存后的DXF几何；不替代成图审阅。"""
import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET


def require(ok,message):
    if not ok:raise AssertionError(message)


def entities(text):
    lines=text.splitlines(); require(len(lines)%2==0,'Odd DXF group lines')
    pairs=[(int(lines[i].strip()),lines[i+1].strip()) for i in range(0,len(lines),2)]
    result=[]; section=None;current=None
    for i,(code,value) in enumerate(pairs):
        if code==0 and value=='SECTION':
            section=pairs[i+1][1];continue
        if code==0 and value=='ENDSEC':
            if section=='ENTITIES' and current:result.append(current)
            section=None;current=None;continue
        if section!='ENTITIES':continue
        if code==0:
            if current:result.append(current)
            current={'type':value,'groups':[]}
        elif current:current['groups'].append((code,value))
    return result


def number(e,code,default=None):
    return next((float(v) for c,v in e['groups'] if c==code),default)


def vertices(e):
    xs=[float(v) for c,v in e['groups'] if c==10];ys=[float(v) for c,v in e['groups'] if c==20]
    require(len(xs)==len(ys),'Unequal vertex coordinates')
    return list(map(list,zip(xs,ys)))


def near(a,b):
    return len(a)==len(b) and all(math.isclose(x,y,abs_tol=1e-7) for x,y in zip(a,b))


def verify_dxf(text,a):
    es=entities(text)
    circles=sorted([number(e,10),number(e,20),number(e,40)] for e in es if e['type']=='CIRCLE')
    if 'circles' in a:
        expected=sorted(a['circles']);require(len(circles)==len(expected),'Circle count changed')
        require(all(near(x,y) for x,y in zip(circles,expected)),'Circle center/radius changed')
    polys=[e for e in es if e['type']=='LWPOLYLINE']
    if 'polygon' in a:
        matches=[e for e in polys if vertices(e)==a['polygon']]
        require(len(matches)==1,'Polygon vertices changed')
        require(int(number(matches[0],70,0))&1,'Polygon is open')
        v=vertices(matches[0]);area=abs(sum(x*y1-x1*y for (x,y),(x1,y1) in zip(v,v[1:]+v[:1])))/2
        require(math.isclose(area,a['area'],abs_tol=1e-7),'Polygon area changed')
    if 'openPolyline' in a:
        matches=[e for e in polys if vertices(e)==a['openPolyline']]
        require(len(matches)==1 and not int(number(matches[0],70,0))&1,'Route missing or closed')
        v=vertices(matches[0]);length=sum(math.dist(p,q) for p,q in zip(v,v[1:]))
        require(math.isclose(length,a['length'],abs_tol=1e-7),'Route length changed')
    if 'closedPolylines' in a:
        require(sum(bool(int(number(e,70,0))&1) for e in polys)==a['closedPolylines'],'Border closure/count wrong')
    dims=[e for e in es if e['type']=='DIMENSION']
    if 'dimensions' in a:require(len(dims)==a['dimensions'],'Native dimension count changed')
    if 'dimensionValues' in a:
        values=[]
        for e in dims:
            require(not any(c==1 and v not in ('','<>') for c,v in e['groups']),'Dimension text override')
            kind=int(number(e,70,0))&7
            if kind==0:
                angle=math.radians(number(e,50,0))
                values.append(abs((number(e,14)-number(e,13))*math.cos(angle)+(number(e,24)-number(e,23))*math.sin(angle)))
            elif kind in (3,4):
                values.append(math.dist([number(e,10),number(e,20)],[number(e,15),number(e,25)]))
            else:raise AssertionError('Unexpected dimension type')
        require(near(sorted(values),sorted(a['dimensionValues'])),'Dimension measured values changed')
    lines=[e for e in es if e['type']=='LINE']
    if 'wallSegments' in a:
        actual=[[number(e,c) for c in (10,20,11,21)] for e in lines]
        for expected in a['wallSegments']+[a['doorLeaf']]:
            require(any(near(v,expected) or near(v,expected[2:]+expected[:2]) for v in actual),'Wall/door segment missing')
        require(len(actual)==len(a['wallSegments'])+1,'Unexpected wall/door lines')
    if 'doorGap' in a:
        lo,hi=a['doorGap']
        for e in lines:
            if number(e,20)==number(e,21)==0:
                x1,x2=sorted((number(e,10),number(e,11)))
                require(min(x2,hi)<=max(x1,lo),'Wall crosses doorway')
        arcs=[e for e in es if e['type']=='ARC']
        require(any(near([number(e,c) for c in (10,20,40,50,51)],a['arc']) for e in arcs),'Door swing arc changed')
    if 'gridCoordinates' in a:
        for v in a['gridCoordinates']:
            require(any(near([number(e,c) for c in (10,20,11,21)],[v,0,v,3000]) for e in lines),'Vertical grid line missing')
            require(any(near([number(e,c) for c in (10,20,11,21)],[0,v,3000,v]) for e in lines),'Horizontal grid line missing')
    # Units are a real header setting, not inferred from the coordinates or a text label.
    raw=text.splitlines();pairs=[(raw[i].strip(),raw[i+1].strip()) for i in range(0,len(raw),2)]
    require(any(code=='9' and value=='$INSUNITS' and pairs[i+1]==('70','4') for i,(code,value) in enumerate(pairs[:-1])),'Millimetre unit lost')
    if 'dimscale' in a:
        require(any(code=='9' and value=='$DIMSCALE' and math.isclose(float(pairs[i+1][1]),a['dimscale']) for i,(code,value) in enumerate(pairs[:-1])),'Dimension display scale lost')
    return es


def run_playbooks(r,path):
    data=json.loads(Path(path).read_text(encoding='utf-8'));require(data['application']=='cadcraft','Wrong app')
    records=[]
    for recipe in data['recipes']:
        args=['run','--metric']
        for s in recipe['steps']:args+=['--cmd',s['command']+' '+json.dumps(s['params'],ensure_ascii=False,separators=(',',':'))]
        target=recipe['id']+'.dxf';r.run(*args,'--save',target)
        assertion=recipe['assertions'];verify_dxf((r.work/target).read_text(encoding='utf-8'),assertion)
        reopened=json.loads(r.run('info',target));require(reopened['entityCount']>0,'Empty reopened drawing')
        inspected=r.run('run',target,'--cmd','drawing.inspect {"entities":true,"limit":200}')
        info=json.loads(inspected.splitlines()[0]);require(len(info['entities'])>0,'No reopened entity geometry')
        if assertion.get('texts'):
            texts=r.run('run',target,'--cmd','texts {}')
            for text in assertion['texts']:require(text in texts,'Reopened label missing: '+text)
        svg=recipe['id']+'.svg';r.run('convert',target,svg)
        ET.fromstring((r.work/svg).read_bytes())
        records.append({'id':recipe['id'],'technicalRoundtrip':'PASS','geometryChecks':'PASS','drawingReview':'NOT_TESTED'})
    require(bool(records),'No CAD scenarios selected')
    records.append(run_core_floor_plan(r, path))
    records.append(run_core_part(r, path))
    records.append(run_core_layers(r, path))
    records.append(run_core_compare(r, path))
    records.append(run_core_sheet(r, path))
    records.append(run_core_trace(r, path))
    records.append(run_bolt_circle(r, path))
    return records


def run_core_floor_plan(r, path):
    """执行独立房间技能中的原始步骤，再验证实际DXF门洞与尺寸。"""
    skill = Path(path).parents[2] / 'cadcraft-floor-plan/references/craft-steps.json'
    recipe = json.loads(skill.read_text(encoding='utf-8'))
    original = r.work
    folder = original / 'core-floor-plan'
    folder.mkdir()
    r.work = folder
    try:
        args = ['run', '--metric']
        for step in recipe['steps']:
            args += ['--cmd', step['command'] + ' ' + json.dumps(step['params'], ensure_ascii=False, separators=(',', ':'))]
        r.run(*args, '--save', 'room.dxf')
        verify_dxf((folder / 'room.dxf').read_text(encoding='utf-8'), recipe['assertions'])
        assert json.loads(r.run('info', 'room.dxf'))['entityCount'] > 0
        reopened = json.loads(r.run('run', 'room.dxf', '--cmd', 'drawing.inspect {"entities":true,"limit":200}').splitlines()[0])
        assert len(reopened['entities']) > 0
        assert 'ROOM A' in r.run('run', 'room.dxf', '--cmd', 'texts {}')
        r.run('convert', 'room.dxf', 'room.svg')
        ET.fromstring((folder / 'room.svg').read_bytes())
        return {'id': 'floor-plan', 'technicalRoundtrip': 'PASS', 'geometryChecks': 'PASS',
                'doorOpeningAndNativeDimensions': 'PASS', 'drawingReview': 'NOT_TESTED', 'installedHostSync': 'NOT_TESTED'}
    finally:
        r.work = original


def run_core_part(r, path):
    """从独立技能执行真实零件与尺寸，保存后重新量测而非比对标签。"""
    recipe = json.loads((Path(path).parents[2] / 'cadcraft-dimension-part/references/craft-steps.json').read_text(encoding='utf-8'))
    original = r.work
    r.work = original / 'core-dimension-part'
    r.work.mkdir()
    try:
        args = ['run', '--metric']
        for step in recipe['steps']:
            args += ['--cmd', step['command'] + ' ' + json.dumps(step['params'], ensure_ascii=False, separators=(',', ':'))]
        r.run(*args, '--save', 'part.dxf')
        verify_dxf((r.work / 'part.dxf').read_text(encoding='utf-8'), recipe['assertions'])
        assert json.loads(r.run('info', 'part.dxf'))['entityCount'] == 7
        r.run('convert', 'part.dxf', 'part.svg')
        ET.fromstring((r.work / 'part.svg').read_bytes())
        return {'id': 'dimension-part', 'technicalRoundtrip': 'PASS', 'geometryChecks': 'PASS', 'nativeDimensionsAndRealHoles': 'PASS', 'drawingReview': 'NOT_TESTED', 'installedHostSync': 'NOT_TESTED'}
    finally:
        r.work = original


def layer_records(text):
    """读取DXF图层表，保留各字段用于检查属性和未指定层。"""
    lines=text.splitlines();pairs=[(int(lines[i].strip()),lines[i+1].strip()) for i in range(0,len(lines),2)]
    result={};current=None;active=False
    for code,value in pairs:
        if code==0:
            if current:
                result[next(v for c,v in current if c==2)]=current
                current=None
            if value=='LAYER':current=[];active=True
            elif value in ['ENDTAB','ENDSEC']:active=False
        elif active and current is not None:current.append((code,value))
    return result


def run_core_layers(r,path):
    """在有实体的既有图纸上整理图层，验证属性并保全原图。"""
    import hashlib
    recipe=json.loads((Path(path).parents[2]/'cadcraft-layer-cleanup/references/craft-steps.json').read_text(encoding='utf-8'))
    original=r.work;r.work=original/'core-layer-cleanup';r.work.mkdir()
    try:
        seed=[('layer.new',{'name':'REFERENCE','current':True}),('line',{'points':[[0,0],[100,60]]}),('layer.new',{'name':'WALL','current':True}),('circle',{'center':[20,20],'radius':5}),('layer.new',{'name':'KEEP','color':3,'current':True}),('line',{'points':[[100,100],[150,100]]})]
        args=['run','--metric']
        for command,params in seed:args+=['--cmd',command+' '+json.dumps(params)]
        r.run(*args,'--save','original.dxf')
        before=(r.work/'original.dxf').read_bytes();args=['run','original.dxf']
        for step in recipe['steps']:args+=['--cmd',step['command']+' '+json.dumps(step['params'])]
        r.run(*args,'--save','cleaned.dxf')
        after=(r.work/'cleaned.dxf').read_text(encoding='utf-8');before_text=before.decode('utf-8');a=layer_records(after);b=layer_records(before_text)
        reference=dict(a['REFERENCE']);assert int(reference[70])&4,'Reference layer not locked';assert reference[290]=='0','Reference layer still plots'
        assert dict(a['WALL'])[370]=='35','Wall lineweight is not 0.35mm'
        assert a['KEEP']==b['KEEP'],'Untargeted layer changed'
        assert entities(after)==entities(before_text),'Existing entity data changed'
        verify_dxf(after,{})
        assert (r.work/'original.dxf').read_bytes()==before,'Input overwritten'
        info=json.loads(r.run('info','cleaned.dxf'));assert info['entityCount']==3
        assert next(x for x in info['layers'] if x['name']=='REFERENCE')['locked'] is True
        return {'id':'layer-cleanup','technicalRoundtrip':'PASS','geometryChecks':'PASS','layerPropertiesAndInputPreserved':'PASS','drawingReview':'NOT_TESTED','installedHostSync':'NOT_TESTED'}
    finally:r.work=original


def run_core_compare(r,path):
    """比较两个真实DXF版本并检查无差异分支，不把叠加当修改。"""
    recipe=json.loads((Path(path).parents[2]/'cadcraft-compare-revisions/references/craft-steps.json').read_text(encoding='utf-8'))
    original=r.work;r.work=original/'core-compare';r.work.mkdir();(r.work/'input').mkdir()
    try:
        r.run('run','--metric','--cmd','circle {"center":[20,20],"radius":5}','--save','revision-a.dxf')
        r.run('run','revision-a.dxf','--cmd','circle {"center":[50,20],"radius":3}','--save','input/revision-b.dxf')
        before=(r.work/'revision-a.dxf').read_bytes();other=(r.work/'input/revision-b.dxf').read_bytes()
        args=['run','revision-a.dxf']
        for step in recipe['steps']:args+=['--cmd',step['command']+' '+json.dumps(step['params'])]
        rows=[json.loads(line) for line in r.run(*args,'--save','review.dxf').splitlines() if line.strip()]
        compared=rows[0];assert compared['counts']=={'added':0,'removed':1,'changed':0,'common':1},compared
        assert compared['regions'],'Expected one actual change region'
        missing=compared['removed'];assert len(missing)==1 and missing[0]['type']=='Circle'
        actual=[e for e in entities(other.decode('utf-8')) if dict(e['groups']).get(5)==missing[0]['handle']]
        assert len(actual)==1 and actual[0]['type']=='CIRCLE' and near([number(actual[0],10),number(actual[0],20),number(actual[0],40)],[50,20,3]),'Difference handle does not identify B-only circle'
        reverse=json.loads(r.run('run','input/revision-b.dxf','--cmd','compare {"path":"revision-a.dxf"}').splitlines()[0])
        assert reverse['counts']=={'added':1,'removed':0,'changed':0,'common':1},reverse
        assert entities((r.work/'review.dxf').read_text(encoding='utf-8'))==entities(before.decode('utf-8')),'Comparison changed entities'
        same=json.loads(r.run('run','revision-a.dxf','--cmd','compare {"path":"revision-a.dxf"}').splitlines()[0])
        assert same['counts']['added']==same['counts']['removed']==same['counts']['changed']==0
        assert not same['regions'],'Identical versions contain change regions'
        assert (r.work/'revision-a.dxf').read_bytes()==before and (r.work/'input/revision-b.dxf').read_bytes()==other,'Comparison overwrote source'
        return {'id':'compare-revisions','technicalRoundtrip':'PASS','geometryChecks':'PASS','realAddedEntityAndIdenticalVersions':'PASS','inputPreserved':'PASS','drawingReview':'NOT_TESTED','installedHostSync':'NOT_TESTED'}
    finally:r.work=original


def pdf_control_lengths(data):
    """只解析本测试的未压缩直线控制PDF，拒绝复杂PDF，不当作通用PDF解释器。"""
    import re
    text=data.decode('latin-1')
    assert '/FlateDecode' not in text,'Control PDF unexpectedly compressed'
    boxes=re.findall(r'/MediaBox\s*\[([^]]+)\]',text)
    assert len(boxes)==1,'Control PDF must have one page'
    box=[float(x) for x in boxes[0].split()]
    assert len(box)==4 and near(box[:2],[0,0])
    assert abs(box[2]*25.4/72-210)<0.02 and abs(box[3]*25.4/72-297)<0.02,'Wrong A4 portrait MediaBox'
    streams=re.findall(r'stream\r?\n(.*?)\r?\nendstream',text,re.S)
    assert streams,'No PDF content stream'
    segments=[];start=None;all_points=[];clips=[]
    for stream in streams:
        clips.extend(re.findall(r'([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+re W n',stream))
        assert not re.search(r'(?m)\s+cm\s*$',stream),'Unexpected PDF transform needs a full PDF interpreter'
        for line in stream.splitlines():
            m=re.fullmatch(r'\s*([-+0-9.eE]+)\s+([-+0-9.eE]+)\s+([ml])\s*',line)
            if not m:continue
            point=[float(m[1]),float(m[2])];all_points.append(point)
            if m[3]=='m':start=point
            elif start is not None:segments.append(math.dist(start,point)*25.4/72);start=point
    assert len(segments)==2,'Control PDF must contain exactly two line segments'
    assert len(clips)==1,'Expected one printable clip rectangle'
    x,y,w,h=map(float,clips[0]);assert w>0 and h>0
    assert all(x-0.02<=px<=x+w+0.02 and y-0.02<=py<=y+h+0.02 for px,py in all_points),'Control geometry is clipped'
    return sorted(segments)


def run_core_sheet(r,path):
    """从真实模型导出PDF并量测纸面控制线，保全源图。"""
    recipe=json.loads((Path(path).parents[2]/'cadcraft-sheet-export/references/craft-steps.json').read_text(encoding='utf-8'))
    original=r.work;r.work=original/'core-sheet-export';r.work.mkdir();(r.work/'output').mkdir()
    try:
        r.run('run','--metric','--cmd','line {"points":[[0,0],[5000,0]]}','--cmd','line {"points":[[0,0],[0,4000]]}','--save','control.dxf')
        before=(r.work/'control.dxf').read_bytes();args=['run','control.dxf']
        for step in recipe['steps']:args+=['--cmd',step['command']+' '+json.dumps(step['params'])]
        r.run(*args)
        lengths=pdf_control_lengths((r.work/'output/sheet.pdf').read_bytes())
        assert all(abs(a-b)<0.02 for a,b in zip(lengths,[80,100])),('Wrong fixed plot scale',lengths)
        opts=dict(next(s['params'] for s in recipe['steps'] if s['command']=='plot'));opts.update({'path':'output/fit-control.pdf','fit':True})
        r.run('run','control.dxf','--cmd','plot '+json.dumps(opts))
        fitted=pdf_control_lengths((r.work/'output/fit-control.pdf').read_bytes())
        assert abs(fitted[-1]-100)>1,'Fit control failed to change output length'
        assert (r.work/'control.dxf').read_bytes()==before,'Plot changed original DXF'
        info=json.loads(r.run('info','control.dxf'));assert info['entityCount']==2
        return {'id':'sheet-export','technicalRoundtrip':'PASS','geometryChecks':'PASS','actualA4And100By80mmControl':'PASS','fitPositiveControl':'PASS','drawingReview':'NOT_TESTED','physicalPrinting':'NOT_TESTED','installedHostSync':'NOT_TESTED'}
    finally:r.work=original


def calibrated_outline(calibration):
    """独立核对确认点到模型的比例、方向及第二尺寸；不执行图像自动识别。"""
    origin=calibration['originPx'];reference=calibration['xReferencePx'];distance=math.dist(origin,reference)
    assert distance>0 and calibration['xLengthMm']>0,'Invalid calibration baseline'
    ux=(reference[0]-origin[0])/distance;uy=(reference[1]-origin[1])/distance;factor=calibration['xLengthMm']/distance
    def mapped(point):
        dx=point[0]-origin[0];dy=point[1]-origin[1]
        return [(dx*ux+dy*uy)*factor,(dx*uy-dy*ux)*factor]
    vertical=mapped(calibration['verticalCheckPx'])
    assert abs(vertical[0])<1e-7 and abs(vertical[1]-calibration['verticalLengthMm'])<1e-7,'Independent vertical reference disagrees with scale or Y direction'
    return [mapped(point) for point in calibration['outlinePx']]


def run_core_trace(r,path):
    """真实参考位图与已确认点为输入，核对原生矢量输出；不代替AI读点验收。"""
    import struct,zlib
    recipe=json.loads((Path(path).parents[2]/'cadcraft-trace-reference/references/craft-steps.json').read_text(encoding='utf-8'))
    expected=calibrated_outline(recipe['calibration']);poly=next(s['params']['vertices'] for s in recipe['steps'] if s['command']=='pline')
    assert all(near(a,b) for a,b in zip(expected,poly)) and len(expected)==len(poly),'Recipe vertices do not follow confirmed reference points'
    original=r.work;r.work=original/'core-reference-trace';r.work.mkdir()
    try:
        def chunk(kind,data):return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))
        rows=[]
        for y in range(160):
            pixels=b''.join(bytes([0,0,0] if ((x in [20,220] and 20<=y<=140) or (y in [20,140] and 20<=x<=220)) else [255,255,255]) for x in range(240));rows.append(b'\0'+pixels)
        image=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',240,160,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(b''.join(rows)))+chunk(b'IEND',b'')
        (r.work/'reference.png').write_bytes(image)
        args=['run','--metric']
        for step in recipe['steps']:args+=['--cmd',step['command']+' '+json.dumps(step['params'])]
        r.run(*args,'--save','traced.dxf')
        verify_dxf((r.work/'traced.dxf').read_text(encoding='utf-8'),recipe['assertions'])
        info=json.loads(r.run('info','traced.dxf'));assert info['entityCount']==1 and info['extents']==[[0,0],[100,60]]
        assert (r.work/'reference.png').read_bytes()==image,'Source reference changed'
        r.run('convert','traced.dxf','traced.svg');ET.fromstring((r.work/'traced.svg').read_bytes())
        return {'id':'trace-reference','technicalRoundtrip':'PASS','geometryChecks':'PASS','confirmedPointScaleAndTwoAxes':'PASS','inputPreserved':'PASS','automaticPointDetection':'NOT_TESTED','rasterUnderlayViaCli':'UNAVAILABLE','drawingReview':'NOT_TESTED','installedHostSync':'NOT_TESTED'}
    finally:r.work=original


def run_bolt_circle(r, path):
    """实际执行独立技能入口，Windows中文路径/ASCII输出及DXF独立回读。"""
    import os
    import subprocess
    import sys
    entry=Path(path).resolve().parents[2]/'cadcraft-bolt-circle/scripts/draw_bolt_circle.py'
    records=[]
    for name,count,start,center in [('six',6,0,[0,0]),('offset-seven',7,30,[100,50])]:
        target=r.work/'中文 孔位'/f'{name}.dxf'
        process=subprocess.run([sys.executable,str(entry),'--cli',str(Path(r.exe).resolve()),'--output',str(target.resolve()),'--count',str(count),'--start-angle',str(start),'--center',*map(str,center)],env={**os.environ,'PYTHONIOENCODING':'ascii'},capture_output=True,timeout=120)
        require(process.returncode==0,process.stderr.decode('utf-8',errors='replace'))
        receipt=json.loads(process.stdout.decode('ascii'))
        require(Path(receipt['output']).resolve()==target.resolve(),'Unicode output path corrupted')
        (r.output/f'bolt-{name}-receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
        expected=[[center[0]+40*math.cos(math.radians(start+360*i/count)),center[1]+40*math.sin(math.radians(start+360*i/count)),3] for i in range(count)]
        verify_dxf(target.read_text(encoding='utf-8'),{'circles':[[*center,55],[*center,15],[*center,40]]+expected,'dimensions':1,'dimensionValues':[3],'dimscale':0.5})
        # Re-execution must refuse all output, leaving original bytes untouched.
        before=target.read_bytes()
        rejected=subprocess.run([sys.executable,str(entry),'--cli',str(Path(r.exe).resolve()),'--output',str(target.resolve())],capture_output=True,timeout=120)
        require(rejected.returncode!=0 and target.read_bytes()==before,'Existing output overwritten')
        require(target.with_suffix('.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n'),'PNG missing')
        ET.fromstring(target.with_suffix('.svg').read_bytes())
        records.append({'id':'bolt-circle-'+name,'standaloneEntry':'PASS','reopenedGeometry':'PASS','nativeProcessesInChild':receipt['nativeProcesses'],'scope':'child CLI calls logged in receipt, excluded from direct Runner process count; host sync NOT_TESTED'})
    return {'id':'bolt-circle','variants':records,'technicalRoundtrip':'PASS','drawingReview':'NOT_TESTED by CI'}
