"""DeckCraft六核心原生可编辑结构、备注与PPTX回读；不替代投影/外部PowerPoint验收。"""
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile
from office_playbook_smoke import verify_deck, A, C, P


def native(path):
    with zipfile.ZipFile(path) as z:
        return json.loads(z.read('presentation.json'))['presentation']


def body_text(body):
    return '\n'.join(''.join(run.get('text', '') for run in p.get('runs', [])) for p in (body or {}).get('paragraphs', []))


def shape_text(shape):
    return body_text(shape.get('text'))


def verify_notes(slides, tokens):
    assert len(slides) == len(tokens), 'Wrong page count for speaker notes'
    for slide, token in zip(slides, tokens):
        assert token in body_text(slide.get('notes')), 'Missing intended note on its own page: ' + token


def find_shape(slide, text):
    items = [s for s in slide['shapes'] if shape_text(s) == text]
    assert len(items) == 1, 'Target shape text is missing or ambiguous: ' + text
    return items[0]


def verify_redesign(before, after):
    assert len(after['slides']) == 3 and after['slides'][0] == before['slides'][0] and after['slides'][2] == before['slides'][1], 'Redesign changed original or unrelated slide'
    copied = after['slides'][1]
    assert not {s['id'] for s in copied['shapes']} & {s['id'] for s in before['slides'][0]['shapes']}, 'Duplicate incorrectly reused original shape IDs'
    assert sorted(shape_text(s) for s in copied['shapes']) == sorted(shape_text(s) for s in before['slides'][0]['shapes']), 'Redesign changed content'
    for text, box in [('SOURCE TITLE KEEP', (48, 36, 864, 80)), ('SOURCE DETAIL KEEP', (48, 150, 540, 300)), ('METRIC KEEP 42', (630, 150, 280, 120))]:
        rect = find_shape(copied, text)['xfrm']
        assert tuple(rect[k] for k in ['x', 'y', 'w', 'h']) == box, 'Target layout not applied to copied object'


def mcp_themes(r):
    requests = [{'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2025-06-18', 'capabilities': {}, 'clientInfo': {'name': 'core-theme-query', 'version': '1'}}},
                {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
                {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call', 'params': {'name': 'run_command', 'arguments': {'command': 'design.themes', 'params': {}}}}]
    rows = [json.loads(line) for line in r.run('mcp', stdin=''.join(json.dumps(q) + '\n' for q in requests)).splitlines() if line.strip()]
    result = next(x['result'] for x in rows if x.get('id') == 2)
    assert not result.get('isError'), 'Native theme query failed'
    return json.loads(result['content'][0]['text'])['themes']


def resolve(value, bindings):
    if isinstance(value, str) and value.startswith('$'):
        assert value[1:] in bindings, 'Unbound scene value ' + value
        return bindings[value[1:]]
    if isinstance(value, list):
        return [resolve(x, bindings) for x in value]
    if isinstance(value, dict):
        return {k: resolve(v, bindings) for k, v in value.items()}
    return value


def verify_chart(path, categories, values):
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if re.fullmatch(r'ppt/charts/chart\d+\.xml', n)]
        assert len(names) == 1, 'Not one editable native chart'
        root = ET.fromstring(z.read(names[0]))
        series = root.findall('.//{' + C + '}ser')
        assert len(series) == 1, 'Unexpected chart series count'
        def points(parent, kind):
            cache = parent.find('.//{' + C + '}' + kind)
            assert cache is not None, 'Chart data cache missing'
            return [p.find('{' + C + '}v').text for p in sorted(cache.findall('{' + C + '}pt'), key=lambda p: int(p.attrib['idx']))]
        cat = series[0].find('{' + C + '}cat')
        val = series[0].find('{' + C + '}val')
        assert points(cat, 'strCache') == categories, 'Chart categories reordered or detached'
        assert [float(v) for v in points(val, 'numCache')] == values, 'Chart values reordered or wrong'


def run_core(r, skill_root):
    original = r.work
    records = []
    try:
        for name in ['training-slides', 'slide-redesign', 'brand-template', 'weekly-report', 'pitch-deck', 'data-story']:
            r.work = original / ('core-' + name)
            r.work.mkdir()
            def run(steps, output, source=None):
                args = ['run'] + (['--in', source] if source else [])
                for command, params in steps:
                    args += ['--cmd', command + '=' + json.dumps(params, ensure_ascii=False, separators=(',', ':'))]
                r.run(*args, '--save', output)
            setup = [('file.new', {'size': [960, 540], 'blank': True})]
            if name == 'slide-redesign':
                setup += [('slide.new', {'layout': 'titleAndContent', 'title': 'SOURCE TITLE KEEP', 'body': 'SOURCE DETAIL KEEP'}),
                          ('shape.insert', {'preset': 'roundRect', 'rect': [700, 420, 180, 80], 'text': 'METRIC KEEP 42'}),
                          ('slide.new', {'layout': 'titleAndContent', 'title': 'UNRELATED KEEP', 'body': 'Do not edit this slide'})]
            run(setup, 'input.deckcraft')
            source_hash = hashlib.sha256((r.work / 'input.deckcraft').read_bytes()).hexdigest()
            before = native(r.work / 'input.deckcraft')
            bindings = {'source.index': 0}
            if name == 'brand-template':
                themes = mcp_themes(r)
                assert themes and themes[0]['name'], 'No actual theme available'
                bindings['theme.name'] = themes[0]['name']
            recipe = json.loads((Path(skill_root) / ('deckcraft-' + name) / 'references/craft-steps.json').read_text(encoding='utf-8'))
            pending, current, stage = [], 'input.deckcraft', 0
            def flush(final=False):
                nonlocal current, stage
                if not pending:
                    return
                output = 'result.deckcraft' if final else 'stage-' + str(stage) + '.deckcraft'
                run([(s['command'], resolve(s['params'], bindings)) for s in pending], output, current)
                if any(s.get('capture') == 'copy' for s in pending):
                    doc = native(r.work / output)
                    old_ids = {s['id'] for s in before['slides']}
                    added = [(i, s) for i, s in enumerate(doc['slides']) if s['id'] not in old_ids]
                    assert len(added) == 1, 'Duplicate did not produce one intended slide'
                    index, slide = added[0]
                    bindings.update({'copy.index': index, 'copy.titleId': find_shape(slide, 'SOURCE TITLE KEEP')['id'],
                                     'copy.bodyId': find_shape(slide, 'SOURCE DETAIL KEEP')['id'], 'copy.metricId': find_shape(slide, 'METRIC KEEP 42')['id']})
                current = output
                stage += 1
                pending.clear()
            for step in recipe['steps']:
                pending.append(step)
                if step.get('capture'):
                    flush()
            flush(True)
            assert current == 'result.deckcraft', 'No final editable output'
            after = native(r.work / current)
            if name == 'training-slides':
                verify_notes(after['slides'], ['课程目标：', '练习：', '回顾：'])
                expected = {'slides': 3, 'textContains': ['课程目标', '完成标准', '练习', '操作步骤', '回顾', '常见错误'], 'notesContains': ['课程目标：', '练习：', '回顾：']}
            elif name == 'slide-redesign':
                verify_redesign(before, after)
                expected = {'slides': 3, 'textContains': ['SOURCE TITLE KEEP', 'SOURCE DETAIL KEEP', 'METRIC KEEP 42', 'UNRELATED KEEP']}
            elif name == 'brand-template':
                assert len(after['slides']) == 2, 'Brand template page count wrong'
                for master in after['masters']:
                    theme = master['theme']
                    assert theme['colors']['colors'][4] == {'r': 26, 'g': 115, 'b': 232, 'a': 255}, 'Actual brand accent not applied'
                    assert theme['fonts']['major']['latin'] == theme['fonts']['minor']['latin'] == 'Inter', 'Brand theme fonts not applied'
                expected = {'slides': 2, 'textContains': ['品牌标题', '正文规范', '最长标题测试'], 'notesContains': ['品牌规范：']}
            elif name == 'weekly-report':
                verify_notes(after['slides'], ['本周结论：', '趋势：', '行动：'])
                expected = {'slides': 3, 'textContains': ['本周结论', '完成量趋势', '行动与风险'], 'tableCount': 1, 'chartCount': 1, 'chartValues': [21, 42]}
            elif name == 'pitch-deck':
                verify_notes(after['slides'], ['问题证据：', '方案约束：', '验证计划：', '里程碑：', '资源请求：'])
                expected = {'slides': 5, 'textContains': ['用户问题', '解决方案', '验证计划', '交付路径', '资源与风险', '待确认']}
            else:
                verify_notes(after['slides'], ['数据依据：', '解释边界：'])
                expected = {'slides': 2, 'textContains': ['结论与数据依据', '解释边界与下一步'], 'chartCount': 1, 'chartValues': [21, 42]}
            r.run('info', current)
            r.run('convert', current, 'result.pptx')
            with zipfile.ZipFile(r.work / 'result.pptx') as z:
                verify_deck(z, expected)
                if name == 'brand-template':
                    theme = ET.fromstring(z.read('ppt/theme/theme1.xml'))
                    accent = theme.find('.//{' + A + '}accent1/{' + A + '}srgbClr')
                    assert accent is not None and accent.attrib['val'].upper() == '1A73E8', 'Brand accent absent in PPTX theme'
            r.run('convert', 'result.pptx', 'reopened.deckcraft')
            reopened = native(r.work / 'reopened.deckcraft')
            assert len(reopened['slides']) == len(after['slides']), 'PPTX import lost pages'
            # 使用各页的活文字核对，而不是重新生成的对象ID或默认样式字节。
            for old, new in zip(after['slides'], reopened['slides']):
                assert [shape_text(s) for s in old['shapes'] if s.get('text')] == [shape_text(s) for s in new['shapes'] if s.get('text')], 'PPTX import changed editable text/order'
                assert body_text(old.get('notes')) == body_text(new.get('notes')), 'PPTX import changed notes'
            if name in ('weekly-report', 'data-story'):
                categories = ['上周', '本周'] if name == 'weekly-report' else ['A', 'B']
                verify_chart(r.work / 'result.pptx', categories, [21, 42])
                charts = [s for sl in reopened['slides'] for s in sl['shapes'] if s['kind'].get('type') == 'chart']
                assert len(charts) == 1, 'PPTX chart became an image'
                # Native command acts on the chart's owning page, not whichever page reopen selects.
                slide_index = next(i for i, sl in enumerate(reopened['slides']) if any(s['id'] == charts[0]['id'] for s in sl['shapes']))
                run([('slide.go', {'index': slide_index}), ('chart.data', {'id': charts[0]['id'], 'categories': categories, 'series': [{'name': '指标', 'values': [21, 48]}]})], 'revision.deckcraft', 'reopened.deckcraft')
                r.run('convert', 'revision.deckcraft', 'revision.pptx')
                verify_chart(r.work / 'revision.pptx', categories, [21, 48])
            assert hashlib.sha256((r.work / 'input.deckcraft').read_bytes()).hexdigest() == source_hash, 'Input presentation overwritten'
            records.append({'id': name, 'technicalRoundtrip': 'PASS', 'editableNativeAndPptxChecks': 'PASS', 'inputProtected': 'PASS',
                            'chartRevision': 'PASS' if name in ('weekly-report', 'data-story') else 'NOT_APPLICABLE',
                            'layoutVisualAcceptance': 'NOT_TESTED', 'externalPowerPointRendering': 'NOT_TESTED', 'installedHostSync': 'NOT_TESTED'})
        return records
    finally:
        r.work = original
