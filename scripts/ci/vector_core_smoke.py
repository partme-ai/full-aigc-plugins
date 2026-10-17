"""六个VectorCraft核心场景：原生对象、实际描摹孔洞、数据重算与原稿保护。"""
import hashlib
import json
from pathlib import Path
import struct
import zlib

from craft_cli_windows import require
from vector_playbook_smoke import inspect, nodes, near
from photo_playbook_smoke import rgb_pixels


def native(r, commands, source=None, target=None):
    argv=['run']+(['--in',source] if source else [])
    for command,params in commands:
        argv+=['--cmd',command,'--params',json.dumps(params,ensure_ascii=False,separators=(',',':'))]
    if target:argv+=['--export',target]
    return [json.loads(line) for line in r.run(*argv).splitlines() if line.strip()]


def raster(path):
    def chunk(kind,data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
    rows=[]
    for y in range(64):
        row=bytearray([0])
        for x in range(64):
            black=8<=x<56 and 8<=y<56 and not(24<=x<40 and 24<=y<40)
            row.extend([0,0,0] if black else [255,255,255])
        rows.append(row)
    path.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',64,64,8,2,0,0,0))+
                     chunk(b'IDAT',zlib.compress(b''.join(rows)))+chunk(b'IEND',b''))


def verify_logo(info):
    ns=nodes(info);groups=[n for n in ns if n['kind']=='Group']
    require(len(groups)==1 and len(groups[0].get('children',[]))==2,'Logo group must contain both source and reflected parts')
    parts=groups[0]['children'];boxes=[n['bounds'] for n in parts]
    require(boxes[0]['x']+boxes[0]['width']<=boxes[1]['x'] or boxes[1]['x']+boxes[1]['width']<=boxes[0]['x'],
            'Mirrored logo parts must not overlap as duplicate art')


def verify_icon(info):
    icon=next(n for n in nodes(info) if n['kind']=='Ellipse')
    require(near([icon['bounds'][k] for k in ('x','y','width','height')],[16,16,16,16]),'Icon dimensions/alignment changed')
    require(icon.get('stroke')=='None' and icon.get('strokeWidth')==0,'Filled icon unexpectedly retained a stroke')
    require(icon.get('fill')=='#243042','Icon fill changed')


def verify_trace(path,info):
    require(not any(n['kind']=='Image' for n in nodes(info)),'Expanded trace still contains raster source')
    w,h,p=rgb_pixels(path,include_alpha=True)
    def color(x,y):return list(p[(y*w+x)*4:(y*w+x)*4+4])
    require(color(32,32)[3]==0,'Trace did not preserve a transparent hole')
    require(color(16,32)==[0,0,0,255],'Trace lost the black band')
    require(color(2,2)[3]==0,'Trace retained a white cover outside the mark')


def run_playbooks(r,skills):
    original=r.work;root=original/'vector-core-scenes';root.mkdir();records=[]
    try:
        files=sorted(Path(skills).glob('vectorcraft-*/references/craft-steps.json'))
        require(len(files)==6,'Expected six VectorCraft core recipes')
        for file in files:
            recipe=json.loads(file.read_text(encoding='utf-8'));name=recipe['id'];r.work=root/name;r.work.mkdir()
            size=(48,48) if name=='icon-set' else (520,320)
            if name=='trace-artwork':size=(64,64);raster(r.work/'scan.png')
            scan_hash=hashlib.sha256((r.work/'scan.png').read_bytes()).hexdigest() if name=='trace-artwork' else None
            fixture=[('file.new',{'width':size[0],'height':size[1],'units':'Pixels','backgroundContents':'transparent' if name=='trace-artwork' else 'white'}),
                     ('text.create',{'x':440,'y':290,'text':'KEEP CORE','font':'Arial','size':14,'color':'#d97706'})]
            if name=='trace-artwork':fixture+=[('file.place',{'path':'scan.png','link':False,'rect':[0,0,64,64]})]
            svg_hash=None
            if name=='svg-cleanup':
                # 精确矩形上的共线冗余点；保护无关文字，不把一般曲线保真推断成零误差。
                points=[[20,20],[40,20],[60,20],[80,20],[100,20],[100,40],[100,60],[100,80],[100,100],
                        [80,100],[60,100],[40,100],[20,100],[20,80],[20,60],[20,40]]
                path='M '+' L '.join(f'{x} {y}' for x,y in points)+' Z'
                svg=('<svg xmlns="http://www.w3.org/2000/svg" width="520" height="320" viewBox="0 0 520 320">'
                     '<text x="440" y="290" font-family="Arial" font-size="14" fill="#d97706">KEEP CORE</text>'
                     '<path d="'+path+'" fill="#2563eb"/></svg>')
                (r.work/'input.svg').write_text(svg,encoding='utf-8')
                svg_hash=hashlib.sha256((r.work/'input.svg').read_bytes()).hexdigest()
                r.run('convert','input.svg','input.vectorcraft')
            else:native(r,fixture,target='input.vectorcraft')
            source_hash=hashlib.sha256((r.work/'input.vectorcraft').read_bytes()).hexdigest()
            before=inspect(r,'input.vectorcraft');keep=next(n for n in nodes(before) if n.get('text')=='KEEP CORE')
            prefix=[]
            if name=='trace-artwork':
                image=next(n for n in nodes(before) if n['kind']=='Image')
                prefix=[('select.set',{'ids':[image['id']]})]
            steps=prefix+[(s['command'],s['params']) for s in recipe['steps']]
            results=native(r,steps,'input.vectorcraft','result.vectorcraft');info=inspect(r,'result.vectorcraft')
            ns=nodes(info)
            if name=='logo-system':verify_logo(info)
            elif name=='icon-set':verify_icon(info)
            elif name in ('editable-chart','infographic'):
                graph_id=next(x['result']['id'] for x in results if x.get('command')=='graph.create')
                def graph_command(source,params,target=None):
                    rows=native(r,[('select.set',{'ids':[graph_id]}),('graph.setData',{'id':graph_id,**params})],source,target)
                    return next(x['result'] for x in rows if x.get('command')=='graph.setData')
                state=graph_command('result.vectorcraft',{})
                require(state['rows']==[[21],[42]] and state['categories']==['A','B'],'Graph data/category order lost')
                graph_command('result.vectorcraft',{'rows':[[42],[84]]},'data-changed.vectorcraft')
                changed=graph_command('data-changed.vectorcraft',{})
                require(changed['rows']==[[42],[84]],'Saved graph lost editable data')
                require(next(n for n in nodes(inspect(r,'data-changed.vectorcraft')) if n['id']==keep['id'])==keep,
                        'Graph data edit changed unrelated artwork')
                r.run('convert','data-changed.vectorcraft','data-changed.png')
                if name=='infographic':
                    require(any(n.get('text')=='示例数量' for n in ns),'Infographic must identify placeholder data')
            elif name=='svg-cleanup':
                summary=next(x['result'] for x in results if x.get('command')=='object.path.simplify')
                require(summary['after']<summary['before'],'SVG cleanup did not reduce redundant anchors')
                native(r,[],'input.vectorcraft','before.svg');native(r,[],'result.vectorcraft','after.svg')
                r.run('convert','input.vectorcraft','before.png');r.run('convert','result.vectorcraft','after.png')
                require(rgb_pixels(r.work/'before.png',include_alpha=True)==rgb_pixels(r.work/'after.png',include_alpha=True),'Collinear cleanup changed rendered artwork')
            native(r,[],'result.vectorcraft','result.svg');r.run('convert','result.vectorcraft','result.png')
            if name in ('editable-chart','infographic'):
                require(rgb_pixels(r.work/'data-changed.png')!=rgb_pixels(r.work/'result.png'),'Graph rendering stayed stale after data change')
            if name=='svg-cleanup':
                reopened=inspect(r,'result.svg')
                require(near([reopened['artboards'][0][k] for k in ('width','height')],size),'Reopened SVG artboard changed')
                require(any(n.get('text')=='KEEP CORE' for n in nodes(reopened)),'SVG lost protected live text')
                r.run('convert','result.svg','svg-reopened.png')
                require(rgb_pixels(r.work/'svg-reopened.png',include_alpha=True)==rgb_pixels(r.work/'result.png',include_alpha=True),'SVG roundtrip changed the cleanup rendering')
                require(hashlib.sha256((r.work/'input.svg').read_bytes()).hexdigest()==svg_hash,'Original SVG source changed')
            if name=='trace-artwork':
                presets=next(x['result']['presets'] for x in results if x.get('command')=='imageTrace.presets')
                preset=next(x for x in presets if x['name']=='Black and White Logo')
                require(preset['params']['ignoreWhite'] is True,'Trace preset no longer ignores the white background')
                verify_trace(r.work/'result.png',info)
            if name!='logo-system':
                require(next(n for n in ns if n['id']==keep['id'])==keep,'Scene changed unrelated original artwork')
            require(hashlib.sha256((r.work/'input.vectorcraft').read_bytes()).hexdigest()==source_hash,'Scene modified input master')
            if name=='trace-artwork':
                require(hashlib.sha256((r.work/'scan.png').read_bytes()).hexdigest()==scan_hash,'Trace raster source modified')
            records.append({'id':name,'nativeBusinessChecks':'PASS','originalMasterPreserved':'PASS',
                            'hostEditorSync':'NOT_TESTED','designAcceptance':'NOT_TESTED',
                            'scope':'synthetic geometry/data and raster-ring technical fixtures'})
    finally:r.work=original
    return records
