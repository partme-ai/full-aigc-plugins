"""DeckCraft main：真实starter与指定品牌页面复用，不替代PowerPoint渲染验收。"""
import hashlib
import json
import xml.etree.ElementTree as ET
import zipfile


def verify_reused_titles(before, after, source):
    assert after == before[:1] + source + before[1:], 'Reuse changed page order or non-target slides'


def run_checks(r):
    original = r.work
    folder = original / 'main-slide-capabilities'
    folder.mkdir()
    r.work = folder
    try:
        def batch(steps, output, source=None):
            args = ['run'] + (['--in', source] if source else [])
            for command, params in steps:
                args += ['--cmd', command + '=' + json.dumps(params, separators=(',', ':'))]
            return r.run(*args, '--save', output)
        requests = [{'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2025-06-18', 'capabilities': {}, 'clientInfo': {'name': 'main-template-ci', 'version': '1'}}},
                    {'jsonrpc': '2.0', 'method': 'notifications/initialized'},
                    {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call', 'params': {'name': 'run_command', 'arguments': {'command': 'file.templates', 'params': {}}}}]
        rows = [json.loads(line) for line in r.run('mcp', stdin=''.join(json.dumps(x) + '\n' for x in requests)).splitlines() if line.strip()]
        result = next(x['result'] for x in rows if x.get('id') == 2)
        assert not result.get('isError'), 'Template listing failed'
        payload = json.loads(result['content'][0]['text'])
        # main帮助写成数组，实际引擎/MCP返回{templates:[...]}。
        templates = payload['templates'] if isinstance(payload, dict) else payload
        assert isinstance(templates, list) and templates and templates[0]['name'], 'No actual starter returned'
        chosen = templates[0]
        batch([('file.new', {'template': chosen['name']})], 'starter.deckcraft')
        info = json.loads(r.run('info', 'starter.deckcraft'))
        assert len(info['slides']) > 0, 'Chosen starter has no slides'
        if isinstance(chosen.get('slides'), int):
            assert len(info['slides']) == chosen['slides'], 'Starter slide count changed'
        batch([('file.new', {'blank': True})] + [('slide.new', {'layout': 'titleAndContent', 'title': name, 'body': 'Native editable brand page'}) for name in ['BRAND A', 'BRAND B', 'BRAND C']], 'brand.pptx')
        source = json.loads(r.run('info', 'brand.pptx'))
        titles = [x['title'] for x in source['slides']]
        indices = [titles.index('BRAND A'), titles.index('BRAND C')]
        source_sha = hashlib.sha256((folder / 'brand.pptx').read_bytes()).hexdigest()
        batch([('file.new', {'blank': True}), ('slide.new', {'layout': 'titleAndContent', 'title': 'DEST', 'body': 'Keep destination content'})], 'destination.deckcraft')
        before = [x['title'] for x in json.loads(r.run('info', 'destination.deckcraft'))['slides']]
        batch([('slide.reuse', {'path': 'brand.pptx', 'slides': indices, 'keepFormatting': True, 'at': 1})], 'reused.deckcraft', 'destination.deckcraft')
        after = [x['title'] for x in json.loads(r.run('info', 'reused.deckcraft'))['slides']]
        verify_reused_titles(before, after, ['BRAND A', 'BRAND C'])
        r.run('convert', 'reused.deckcraft', 'reused.pptx')
        with zipfile.ZipFile(folder / 'reused.pptx') as z:
            slides = sorted((n for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')), key=lambda n: int(n.rsplit('slide', 1)[1][:-4]))
            texts = [' '.join(n.text or '' for n in ET.fromstring(z.read(name)).iter('{http://schemas.openxmlformats.org/drawingml/2006/main}t')) for name in slides]
        assert len(texts) == len(after), 'PPTX page count differs'
        joined = '\n'.join(texts)
        assert 'BRAND B' not in joined and joined.index('BRAND A') < joined.index('BRAND C'), 'Native editable PPTX text missing or reordered'
        assert 'Keep destination content' in joined, 'Destination content lost'
        assert hashlib.sha256((folder / 'brand.pptx').read_bytes()).hexdigest() == source_sha, 'Brand source file changed'
        return {'actualStarterTemplate': 'PASS', 'selectedBrandPagesInOrder': 'PASS', 'destinationAndSourcePreserved': 'PASS',
                'editablePptxText': 'PASS', 'externalPowerPointRendering': 'NOT_TESTED', 'installedHostSync': 'NOT_TESTED'}
    finally:
        r.work = original
