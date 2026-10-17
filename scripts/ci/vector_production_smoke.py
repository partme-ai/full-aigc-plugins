"""直接执行三个矢量技能配方，检查真实编辑结构、释放与展开结果。"""
from collections import OrderedDict
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from craft_cli_windows import require
from photo_playbook_smoke import rgb_pixels
from vector_core_smoke import native
from vector_playbook_smoke import inspect, nodes, near

SCENES = ['clipped-illustration', 'sticker-grid', 'sticker-offset-border']


def recipe_hashes(path):
    """文本步骤统一LF用于跨平台比对，同时保留原始文件摘要。"""
    return {'recipeSha256': hashlib.sha256(path.read_text(encoding='utf-8').encode('utf-8')).hexdigest(),
            'recipeFileSha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'recipeHashEncoding': 'UTF-8 with LF text newlines'}


def resolve(value, captures):
    """只解析手册引用，缺失真实返回值时失败，不能猜测对象编号。"""
    if isinstance(value, dict) and '$ref' in value:
        keys = value['$ref'].split('.')
        result = captures[keys[0]]
        for key in keys[1:]:
            result = result[int(key)] if isinstance(result, list) else result[key]
        return result
    if isinstance(value, dict): return {key: resolve(item, captures) for key, item in value.items()}
    if isinstance(value, list): return [resolve(item, captures) for item in value]
    return value


def bounds(node):
    return [node['bounds'][key] for key in ['x', 'y', 'width', 'height']]


def require_pixels(path, samples):
    width, height, pixels = rgb_pixels(path)
    require((width, height) == (320, 240), 'Vector preview dimensions changed')
    for x, y, expected in samples:
        require(list(pixels[(y * width + x) * 3:(y * width + x) * 3 + 3]) == expected,
                'Unexpected rendered pixel at ' + str((x, y)))


def verify_expanded_grid(info):
    """展开必须有十二个不同位置的真实图形，不能十二份重叠对象冒充。"""
    items = [n for n in nodes(info) if n['kind'] == 'Ellipse']
    require(len(items) == 12, 'Expanded grid must have twelve editable ellipses')
    actual = sorted(tuple(round(x, 6) for x in bounds(n)) for n in items)
    expected = sorted((20 + 50 * col, 20 + 50 * row, 30, 30) for row in range(3) for col in range(4))
    require(actual == expected, 'Expanded grid positions or dimensions wrong')


def verify_border(info, captures):
    ns = {n['id']: n for n in nodes(info)}
    art = ns[captures['art']['id']]
    require(near(bounds(art), [100, 80, 100, 60]) and art.get('fill') == '#2563eb', 'Original artwork changed')
    ids = captures['border']['ids']
    require(len(ids) == 1 and ids[0] != art['id'], 'Offset must be a separate editable path')
    border = ns[ids[0]]
    require(border['kind'] == 'Path' and border.get('closed') is True, 'Offset border is not a closed path')
    require(near(bounds(border), [92, 72, 116, 76]), 'Offset distance or geometry wrong')
    require(border.get('fill') == '#ffffff' and border.get('stroke') == 'None', 'White border paint wrong')


def run_playbooks(r, skills):
    original = r.work
    records = []
    try:
        for name in SCENES:
            path = Path(skills) / ('vectorcraft-' + name) / 'references/craft-steps.json'
            recipe = json.loads(path.read_text(encoding='utf-8'))
            require(recipe['id'] == name, 'Wrong vector scene')
            r.work = original / name
            r.work.mkdir()
            groups = OrderedDict()
            for step in recipe['steps']: groups.setdefault(step['batch'], []).append(step)
            captures = {}
            previous = None
            for index, group in enumerate(groups.values()):
                target = 'step-' + str(index) + '.vectorcraft'
                rows = native(r, [(s['command'], resolve(s['params'], captures)) for s in group], previous, target)
                commands = [row for row in rows if row.get('step') == 'cmd']
                require(len(commands) == len(group), 'Actual command results do not match recipe batch')
                for step, row in zip(group, commands):
                    require(step['command'] == row['command'], 'Wrong native command result')
                    if step.get('capture'): captures[step['capture']] = row['result']
                previous = target
            native(r, [], previous, 'master.vectorcraft')
            source_hash = hashlib.sha256((r.work / 'master.vectorcraft').read_bytes()).hexdigest()
            info = inspect(r, 'master.vectorcraft')
            r.run('convert', 'master.vectorcraft', 'review.png')
            r.run('convert', 'master.vectorcraft', 'review.svg')
            svg = ET.fromstring((r.work / 'review.svg').read_bytes())
            require(any(x.tag.endswith(('path', 'ellipse', 'rect', 'use')) for x in svg.iter()), 'No actual SVG vector geometry')
            require(not any(x.tag.endswith('}image') for x in svg.iter()), 'Vector scene unexpectedly flattened to raster')
            ns = {n['id']: n for n in nodes(info)}
            if name == 'clipped-illustration':
                group = ns[captures['clip']['id']]
                require(group['kind'] == 'Clip Group', 'Non-destructive clipping group missing')
                require(near(bounds(ns[captures['art']['id']]), [20, 40, 240, 160]), 'Clipping destroyed original artwork extent')
                require_pixels(r.work / 'review.png', [(30, 120, [255, 255, 255]), (90, 120, [37, 99, 235]),
                                                      (110, 120, [249, 115, 22]), (85, 65, [255, 255, 255])])
                native(r, [('object.clippingMask.release', {'ids': [group['id']]})], 'master.vectorcraft', 'released.vectorcraft')
                released = inspect(r, 'released.vectorcraft')
                require(not any(n['kind'] == 'Clip Group' for n in nodes(released)), 'Release kept a clipping group')
                released_nodes = {n['id']: n for n in nodes(released)}
                for key in ['art', 'stripe', 'mask']:
                    require(released_nodes[captures[key]['id']] == ns[captures[key]['id']], 'Release changed source geometry or paint')
                r.run('convert', 'released.vectorcraft', 'released.png')
                require_pixels(r.work / 'released.png', [(30, 120, [37, 99, 235]), (110, 50, [249, 115, 22])])
            elif name == 'sticker-grid':
                group = ns[captures['repeat']['id']]
                require(group['kind'] == 'Grid Repeat' and near(bounds(group), [20, 20, 180, 130]), 'Editable repeat or spacing wrong')
                require(len([n for n in nodes(info) if n['kind'] == 'Ellipse']) == 1, 'Live grid must retain one source ellipse')
                centers = [(35 + 50 * col, 35 + 50 * row) for row in range(3) for col in range(4)]
                require_pixels(r.work / 'review.png', [(x, y, [37, 99, 235]) for x, y in centers] + [(60, 35, [255, 255, 255])])
                native(r, [('paint.setFill', {'ids': [captures['art']['id']], 'color': '#f97316'})], 'master.vectorcraft', 'recolored.vectorcraft')
                r.run('convert', 'recolored.vectorcraft', 'recolored.png')
                require_pixels(r.work / 'recolored.png', [(x, y, [249, 115, 22]) for x, y in centers])
                select = ('select.set', {'ids': [group['id']]})
                native(r, [select, ('object.repeat.options', {'rows': 2, 'cols': 3})], 'master.vectorcraft', 'six-grid.vectorcraft')
                changed = next(n for n in nodes(inspect(r, 'six-grid.vectorcraft')) if n['id'] == group['id'])
                require(near(bounds(changed), [20, 20, 130, 80]), 'Saved grid row/column editing failed')
                native(r, [select, ('object.repeat.expand', {})], 'master.vectorcraft', 'expanded.vectorcraft')
                verify_expanded_grid(inspect(r, 'expanded.vectorcraft'))
                r.run('convert', 'expanded.vectorcraft', 'expanded.png')
                require(rgb_pixels(r.work / 'expanded.png') == rgb_pixels(r.work / 'review.png'), 'Expanding changed the artwork rendering')
            else:
                verify_border(info, captures)
                require_pixels(r.work / 'review.png', [(120, 100, [37, 99, 235]), (96, 100, [255, 255, 255]),
                                                      (80, 100, [100, 116, 139])])
            require(hashlib.sha256((r.work / 'master.vectorcraft').read_bytes()).hexdigest() == source_hash,
                    'Editing derivative output changed the saved original')
            (r.work / 'captures.json').write_text(json.dumps(captures, indent=2), encoding='utf-8')
            records.append({'id': name, **recipe_hashes(path),
                            'nativeSaveReopenEditing': 'PASS', 'renderedPixels': 'PASS', 'originalProjectUnchanged': 'PASS',
                            'hostEditorSync': 'NOT_TESTED', 'realDesignQuality': 'NOT_TESTED', 'scope': 'original small synthetic vector shapes'})
    finally:
        r.work = original
    return records
