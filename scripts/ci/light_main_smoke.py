"""LightCraft main：联系印样模板重用与实际PDF交付。"""
import hashlib
import json
import re
from media_playbook_smoke import image_fixture


def verify_print_settings(value):
    settings = value['settings']
    assert settings['layout']['style'] == 'contactSheet', 'Wrong print layout'
    assert settings['layout']['grid']['columns'] == settings['layout']['grid']['rows'] == 3, 'Print template grid lost'
    assert settings['job']['ppi'] == 150, 'Print template resolution lost'


def run_checks(r):
    original = r.work
    folder = original / 'main-print-capabilities'
    folder.mkdir()
    r.work = folder
    try:
        image_fixture(folder / 'first.png')
        image_fixture(folder / 'second.png', True)
        hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.glob('*.png')}
        def run(steps, imports=()):
            args = ['run', '--library', 'main-print-library']
            for path in imports:
                args += ['--import', path]
            rows = [json.loads(line) for line in r.run(*args, '--script', '-', stdin=''.join(
                json.dumps({'command': name, 'params': params}) + '\n' for name, params in steps)).splitlines() if line.strip()]
            assert len(rows) == len(steps) and all('result' in x and not x.get('error') for x in rows), 'Print command failed'
            return [x['result'] for x in rows]
        name = 'MAIN CI Contact 3x3 150ppi'
        settings = {'layout': {'style': 'contactSheet', 'grid': {'columns': 3, 'rows': 3, 'spacingX': .12, 'spacingY': .12}},
                    'image': {'zoomToFill': False, 'rotateToFit': True}, 'job': {'ppi': 150}}
        # 这是仅含本测试两张图片的新建专用库；共享库必须传明确ID。
        rows = run([('library.selectAll', {}), ('print.set', settings), ('print.template.save', {'name': name}),
                    ('print.set', {'layout': {'grid': {'columns': 1, 'rows': 1}}, 'job': {'ppi': 300}}),
                    ('print.template.apply', {'name': name}), ('print.get', {}),
                    ('print.exportPdf', {'path': 'contact-proof.pdf'})], ['first.png', 'second.png'])
        verify_print_settings(rows[5])
        assert any(x['name'] == name for x in rows[2]['templates']), 'Saved print template absent'
        exported = rows[6]
        assert exported['photos'] == 2 and exported['pages'] == 1, 'Wrong selected photo or page count'
        pdf = (folder / 'contact-proof.pdf').read_bytes()
        assert pdf.startswith(b'%PDF') and len(re.findall(rb'/Type\s*/Page\b', pdf)) == 1, 'Not an actual one-page PDF'
        assert all(hashlib.sha256((folder / n).read_bytes()).hexdigest() == sha for n, sha in hashes.items()), 'Original photo changed'
        return {'templateSaveApply': 'PASS', 'restoredGridAndResolution': 'PASS', 'twoPhotosOnePagePdf': 'PASS',
                'originalPhotosUnchanged': 'PASS', 'thumbnailVisualReview': 'NOT_TESTED', 'installedHostSync': 'NOT_TESTED'}
    finally:
        r.work = original
