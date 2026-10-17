#!/usr/bin/env python3
"""外部原生验收：画板隔离、完整依赖与 PDF 日期参数；不修改安装技能。"""
import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time
import xml.etree.ElementTree as ET

config = json.loads(Path(sys.argv[1]).read_text())
root = Path(config['output']).resolve()
root.mkdir(exist_ok=False)
skill = Path(config['skill']).resolve()
binary = Path(config['binary']).resolve()
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def tree(path):
    return {p.relative_to(path).as_posix(): sha(p) for p in sorted(path.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
before_skill = tree(skill)
spec = importlib.util.spec_from_file_location('isolation_session', skill/'scripts/mcp_session.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
cases = []
with module.Session([str(binary), 'mcp', '--headless']) as session:
    def call(identifier, **params):
        return session.command(identifier, params)
    def scene():
        call('file.new', name='Isolation qualification', width=80, height=64, units='Pixels', created=946684800)
    def rect(x, y, color):
        made = call('shape.rectangle', x=x, y=y, width=20, height=20)
        call('paint.setFill', color=color)
        call('paint.setStroke', none=True)
        return made['id']
    def state():
        return {'model': call('document.json'), 'inspect': call('document.inspect')}
    def export(name, params=None, error=False):
        before = state()
        try:
            value = call('document.serialize', **({'format':'svg','artboard':0,'artboardContentOnly':True} if params is None else params))
        except RuntimeError as exc:
            if not error:
                raise
            value = {'rejected': True, 'error': str(exc)}
        else:
            assert not error, name+' accepted invalid options'
        assert state() == before, name+' changed model or selection/history'
        path = root/(name+'.json')
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')
        state_path = root/(name+'-state.json')
        state_path.write_text(json.dumps(before, ensure_ascii=False, indent=2)+'\n')
        cases.append({'name':name,'result':'PASS','sourceSelectionHistoryPreserved':True,'receipt':path.name,'sha256':sha(path),'state':state_path.name,'stateSha256':sha(state_path)})
        if 'text' in value:
            ET.fromstring(value['text'])
        return value

    scene()
    inside = rect(20, 16, '#22aa66')
    call('object.lock')
    remote = rect(200, 20, '#2366e8')
    svg = export('locked-visible')['text']
    assert '#22aa66' in svg and '#2366e8' not in svg
    call('paint.setFill', ids=[remote], color='#175cce')
    assert export('remote-change')['text'] == svg

    scene()
    rect(-25,16,'#2366e8')
    call('paint.setStroke', color='#e96340')
    call('stroke.set', weight=16)
    assert '#e96340' in export('stroke-reaching-board')['text']

    scene()
    rect(-50,16,'#2366e8')
    call('effect.apply', effect='stylize.dropShadow', params={'x':45,'y':0,'blur':2,'opacity':100})
    assert '#2366e8' in export('shadow-reaching-board')['text']

    scene()
    a = rect(10,10,'#22aa66')
    b = rect(200,20,'#2366e8')
    call('select.set', ids=[a,b])
    group = call('object.group')
    group_dependency = {'id':group['id'],'members':[a,b],'scope':'whole indivisible cross-artboard group; remote child is a dependency'}
    svg = export('indivisible-cross-board-group')['text']
    assert '#22aa66' in svg and '#2366e8' in svg

    scene()
    b = rect(200,20,'#2366e8')
    a = rect(10,10,'#22aa66')
    call('select.set', ids=[a,b])
    call('object.clippingMask.make')
    svg = export('complete-clipping-group')['text']
    assert 'clipPath' in svg and '#2366e8' in svg

    scene()
    rect(200,20,'#2366e8')
    svg = export('empty-board')['text']
    assert not ET.fromstring(svg).findall('.//{http://www.w3.org/2000/svg}path')
    assert list(map(float,ET.fromstring(svg).attrib['viewBox'].split())) == [0,0,80,64]
    legacy = export('legacy-default', {'format':'svg','artboard':0})['text']
    assert '#2366e8' in legacy
    assert export('isolation-off', {'format':'svg','artboard':0,'artboardContentOnly':False})['text'] == legacy
    invalid = [{'artboard':9},{'artboard':-1},{'selectedOnly':True},{'artboardContentOnly':'true'},
               {'artboards':[0,1]},{'range':'all'},{'useArtboards':False},{'svg':{'artboard':0}},
               {'format':'png'},{'svg':{'useArtboards':False}}]
    for i, extra in enumerate(invalid):
        export('invalid-isolation-'+str(i), {'format':'svg','artboard':0,'artboardContentOnly':True,**extra}, error=True)

    # 原生空子图层的绘制范围为 None（渲染器 children.fold(None, ...)）。
    # 保守策略必须保留有未知后代的整个父图层，不能只删除远处兄弟对象。
    scene()
    rect(200,20,'#2366e8')
    model = call('document.json')
    layer_id = model['layers'][0]['id']
    call('layer.newSublayer', parent=layer_id, name='Unknown empty native paint bounds')
    model = call('document.json')
    empty = next(n for n in model['layers'][0]['kind']['children'] if n.get('name')=='Unknown empty native paint bounds')
    assert empty['kind']['type'] == 'layer' and empty['kind']['children'] == []
    (root/'unknown-bounds-model.json').write_text(json.dumps(model, ensure_ascii=False, indent=2)+'\n')
    assert '#2366e8' in export('unknown-descendant-conservative-parent')['text']

    scene()
    rect(20,16,'#22aa66')
    params = {'format':'pdf','artboard':0,'created':946684800}
    first = export('pdf-fixed-date', params)
    time.sleep(2.1)
    second = export('pdf-fixed-date-later', params)
    assert base64.b64decode(first['dataBase64']) == base64.b64decode(second['dataBase64'])
    import fitz
    with fitz.open(stream=base64.b64decode(first['dataBase64']), filetype='pdf') as pdf:
        assert pdf.metadata['creationDate'] == 'D:20000101000000Z'
    for i, created in enumerate([True,'2026-10-06',1.5,{},[],2**63]):
        export('invalid-pdf-date-'+str(i), {**params,'created':created}, error=True)
    default = export('pdf-default-now', {'format':'pdf','artboard':0})
    time.sleep(2.1)
    later = export('pdf-default-later', {'format':'pdf','artboard':0})
    dates = []
    for value in [default,later]:
        with fitz.open(stream=base64.b64decode(value['dataBase64']), filetype='pdf') as pdf:
            dates.append(pdf.metadata['creationDate'])
    assert dates[0] != dates[1]
    null_default = export('pdf-null-default', {'format':'pdf','artboard':0,'created':None})
    with fitz.open(stream=base64.b64decode(null_default['dataBase64']), filetype='pdf') as pdf:
        from datetime import datetime, timezone
        observed = datetime.strptime(pdf.metadata['creationDate'],'D:%Y%m%d%H%M%SZ').replace(tzinfo=timezone.utc).timestamp()
        assert abs(time.time()-observed) < 5
assert tree(skill) == before_skill
proof = {'schema':'vectorcraft-artboard-isolation-native/v1','result':'PASS','cases':cases,
         'runtimeSha256':sha(binary),'driverSha256':sha(__file__),'skillFiles':before_skill,
         'crossArtboardDependency':group_dependency,
         'installedSkillPreserved':True,'pdfLegacyDefaultDates':dates,
         'scope':'actual fixed native SVG locked/stroke/effect/group/clipping/empty/invalid/legacy/empty-sublayer conservative parent and PDF fixed/default/invalid dates; empty sublayer None bounds also requires pinned renderer source evidence'}
(root/'proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2)+'\n')
print(json.dumps({'result':'PASS','cases':len(cases),'scope':proof['scope']}))
