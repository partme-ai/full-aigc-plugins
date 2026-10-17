"""DesignCraft main：SVG原生图形进入版式，再交付可编辑PPTX。"""
import json
import xml.etree.ElementTree as ET
import zipfile
from design_playbook_smoke import run_script

P = '{http://schemas.openxmlformats.org/presentationml/2006/main}'
A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'


def verify_pptx(path):
    with zipfile.ZipFile(path) as z:
        slides = [n for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')]
        assert len(slides) == 1, 'Page/slide count mismatch'
        root = ET.fromstring(z.read(slides[0]))
        assert len(list(root.iter(P + 'sp'))) >= 3, 'SVG shapes or text were flattened'
        assert not list(root.iter(P + 'pic')), 'Simple vector artwork became a bitmap'
        assert 'MAIN EDITABLE TITLE' in ''.join(x.text or '' for x in root.iter(A + 't')), 'Live text lost'
        colors = {x.attrib.get('val', '').lower() for x in root.iter(A + 'srgbClr')}
        assert {'2563eb', '16a34a'} <= colors, 'SVG fill colors lost'


def run_checks(r):
    original = r.work
    r.work = original / 'main-svg-pptx'
    r.work.mkdir()
    try:
        svg = '<svg xmlns="http://www.w3.org/2000/svg" width="120" height="60"><rect x="0" y="0" width="50" height="60" fill="#2563eb"/><ellipse cx="90" cy="30" rx="25" ry="25" fill="#16a34a"/></svg>'
        results = run_script(r, [
            {'command': 'file.new', 'params': {'width': 360, 'height': 240, 'facingPages': False}},
            {'command': 'edit.pasteSvg', 'params': {'svg': svg, 'at': [180, 100]}},
            {'command': 'frame.create', 'params': {'rect': [24, 180, 336, 220], 'content': 'text', 'text': 'MAIN EDITABLE TITLE'}},
            {'command': 'file.exportPptx', 'params': {'path': 'editable.pptx', 'rasterize': False, 'embedFonts': False}},
        ], save='layout.designcraft')
        assert results[1]['ids'], 'SVG import created no native items'
        assert results[3]['slides'] == 1, 'PPTX export did not include one page'
        verify_pptx(r.work / 'editable.pptx')
        story = run_script(r, [{'command': 'story.get', 'params': {'frame': results[2]['id']}}], source='layout.designcraft')[0]
        assert story['text'] == 'MAIN EDITABLE TITLE', 'Saved native story changed'
        r.run('run', '--in', 'layout.designcraft', '--export', 'layout.pdf')
        assert (r.work / 'layout.pdf').read_bytes().startswith(b'%PDF'), 'Native layout did not render'
        return {'svgNativeImport': 'PASS', 'editablePptxGeometryAndText': 'PASS',
                'nativeReopen': 'PASS', 'externalPowerPointRendering': 'NOT_TESTED', 'installedHostSync': 'NOT_TESTED'}
    finally:
        r.work = original
