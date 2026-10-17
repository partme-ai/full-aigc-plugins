"""原生PDF场景：页面/字段/删除/压缩/OCR；不等同印刷认证或中文表单支持。"""
import hashlib
import json
import os
from pathlib import Path
import re
import zlib

from craft_cli_windows import require
from craft_windows import download
from photo_playbook_smoke import rgb_pixels


def write_pdf(path, objects):
    data, offsets = b'%PDF-1.7\n', [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(data))
        data += f'{i} 0 obj\n'.encode() + obj + b'\nendobj\n'
    start = len(data)
    data += f'xref\n0 {len(objects)+1}\n0000000000 65535 f \n'.encode()
    data += b''.join(f'{offset:010d} 00000 n \n'.encode() for offset in offsets[1:])
    data += f'trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{start}\n%%EOF\n'.encode()
    path.write_bytes(data)


def fixture(path):
    objects = [b'<< /Type /Catalog /Pages 2 0 R /AcroForm 12 0 R >>',
               b'<< /Type /Pages /Kids [3 0 R 5 0 R 7 0 R] /Count 3 >>']
    for i, name in enumerate(['PAGE ONE', 'PAGE TWO', 'PAGE THREE']):
        page = 3 + i * 2
        objects.append(f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 200] /Resources << /Font << /F1 10 0 R >> >> /Contents {page+1} 0 R'.encode()
                       + (b' /Annots [11 0 R]' if i == 0 else b'') + b' >>')
        secret = b'CONFIDENTIAL' if i == 0 else b'CONFIDENTIALITY' if i == 1 else b'PUBLIC THREE'
        lines = f'BT /F1 12 Tf 20 170 Td ({name}) Tj 0 -30 Td (PUBLIC KEEP) Tj 0 -30 Td ('.encode()
        lines += secret + b') Tj ET\n' + b'% redundant fixture comment\n' * 250
        objects.append(f'<< /Length {len(lines)} >>\nstream\n'.encode() + lines + b'endstream')
    objects.extend([b'<< /Unused true >>', b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
                    b'<< /Type /Annot /Subtype /Widget /FT /Tx /T (CustomerName) /V (Initial) /Rect [20 35 260 65] /P 3 0 R /DA (/Helv 12 Tf 0 g) >>',
                    b'<< /Fields [11 0 R] /DR << /Font << /Helv 10 0 R >> >> /DA (/Helv 12 Tf 0 g) >>'])
    write_pdf(path, objects)


def scan_fixture(path, image):
    width, height, pixels = rgb_pixels(image)
    compressed = zlib.compress(pixels)
    content = b'q 300 0 0 200 0 0 cm /Im0 Do Q\n'
    write_pdf(path, [b'<< /Type /Catalog /Pages 2 0 R >>', b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
                    b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 200] /Resources << /XObject << /Im0 5 0 R >> >> /Contents 4 0 R >>',
                    f'<< /Length {len(content)} >>\nstream\n'.encode() + content + b'endstream',
                    f'<< /Type /XObject /Subtype /Image /Width {width} /Height {height} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /FlateDecode /Length {len(compressed)} >>\nstream\n'.encode()
                    + compressed + b'\nendstream'])


def json_values(text):
    decoder, values = json.JSONDecoder(), []
    while text.strip():
        text = text.lstrip()
        value, end = decoder.raw_decode(text)
        values.append(value)
        text = text[end:]
    return values


def script(r, name, steps, source='input.pdf'):
    # 官方CLI全新脚本分配递增ID；增加独立诱饵文件，检查映射不依赖目标doc=1。
    native = [{'tool': 'doc_open', 'args': {'path': 'decoy.pdf'}},
              {'tool': 'doc_open', 'args': {'path': source}}]
    for step in steps:
        params = dict(step['params'])
        if 'doc' in params:
            params['doc'] += 1
        native.append({'tool': step['command'], 'args': params})
    file = r.work / (name + '.json')
    file.write_text(json.dumps(native, ensure_ascii=False), encoding='utf-8')
    rows = json_values(r.run('run', '--script', str(file), '--root', str(r.work)))
    require(rows[0]['doc'] == 1 and rows[1]['doc'] == 2, 'Native fresh-script document IDs changed')
    require(len(rows) == len(native), 'PDF tool output count mismatch')
    return rows[2:]


def verify_page_order(text, expected):
    pages = [page for page in text.split('\f') if page.strip()]
    require(len(pages) == len(expected) and all(label in page for label, page in zip(expected, pages)),
            'PDF page order or count changed')


def verify_form(fields, visible, expected):
    require(next(field['value'] for field in fields['fields'] if field['name'] == 'CustomerName') == expected,
            'Stored field value changed')
    require(expected in visible and '????' not in visible, 'Field appearance does not display the stored value')


def verify_redacted(text, data):
    require(not re.search(r'\bCONFIDENTIAL\b', text), 'Secret survived text extraction')
    require('PUBLIC KEEP' in text and 'CONFIDENTIALITY' in text, 'Redaction removed protected public text')
    # 独立检查原始/Flate内容流，不能用黑框遮住仍存在的文字来通过。
    for stream in re.findall(rb'stream\r?\n(.*?)\r?\nendstream', data, re.S):
        try:
            stream = zlib.decompress(stream)
        except zlib.error:
            pass
        require(not re.search(rb'\bCONFIDENTIAL\b', stream), 'Secret survived in a PDF content stream')


def run_recipe(r, recipe):
    name = recipe['id']
    (r.work / 'output').mkdir()
    fixture(r.work / 'input.pdf')
    fixture(r.work / 'decoy.pdf')
    original = hashlib.sha256((r.work / 'input.pdf').read_bytes()).hexdigest()
    baseline = r.run('text', 'input.pdf')
    source = 'input.pdf'
    if name == 'ocr-scans':
        r.run('render', source, '--page', '1', '--dpi', '144', '--out', 'raster.png')
        scan_fixture(r.work / 'scan.pdf', r.work / 'raster.png')
        require(not r.run('text', 'scan.pdf').strip(), 'OCR fixture already contains selectable text')
        source = 'scan.pdf'
    rows = script(r, 'steps', recipe['steps'], source)
    result = {'id': name, 'technicalSample': 'PASS', 'hostEditorSync': 'NOT_TESTED'}
    if name == 'organize-pdf':
        verify_page_order(r.run('text', 'output/organized.pdf'), ['PAGE THREE', 'PAGE ONE', 'PAGE TWO'])
        verify_page_order(r.run('text', 'output/selected.pdf'), ['PAGE THREE', 'PAGE ONE'])
    elif name == 'compress-pdf':
        require(r.run('text', 'output/optimized.pdf') == baseline, 'Optimized PDF changed extracted content')
        require((r.work / 'output/optimized.pdf').stat().st_size < (r.work / source).stat().st_size,
                'Compression fixture did not get smaller')
        r.run('render', source, '--page', '1', '--dpi', '144', '--out', 'before.png')
        r.run('render', 'output/optimized.pdf', '--page', '1', '--dpi', '144', '--out', 'after.png')
        require(rgb_pixels(r.work / 'before.png') == rgb_pixels(r.work / 'after.png'), 'Optimization changed rendered sample')
    elif name == 'fill-pdf-forms':
        fields = script(r, 'reopen', [{'command': 'form_fields', 'params': {'doc': 1}}], 'output/filled.pdf')[0]
        verify_form(fields, r.run('text', 'output/filled.pdf'), 'Sample Customer')
        r.run('render', 'output/filled.pdf', '--page', '1', '--dpi', '144', '--out', 'filled.png')
        # 单独保留真实的中文外观失败，不把ASCII样例当作中文验收。
        script(r, 'cjk', [
            {'command': 'form_fill', 'params': {'doc': 1, 'values': {'CustomerName': '真实姓名'}}},
            {'command': 'doc_save', 'params': {'doc': 1, 'path': 'output/cjk.pdf', 'full': True}},
        ])
        cjk = script(r, 'cjk-reopen', [{'command': 'form_fields', 'params': {'doc': 1}}], 'output/cjk.pdf')[0]
        visible = r.run('text', 'output/cjk.pdf')
        require(cjk['fields'][0]['value'] == '真实姓名', 'CJK field storage changed')
        result['cjkAppearance'] = 'PASS' if '真实姓名' in visible else 'FAIL_KNOWN_FONT_LIMITATION'
    elif name == 'redact-pdf':
        verify_redacted(r.run('text', 'output/redacted.pdf'), (r.work / 'output/redacted.pdf').read_bytes())
        audit = json.loads(r.run('audit', 'output/redacted.pdf'))
        result['audit'] = audit
        r.run('render', 'output/redacted.pdf', '--page', '1', '--dpi', '144', '--out', 'redacted.png')
    elif name == 'ocr-scans':
        text = r.run('text', 'output/searchable.pdf')
        require('PAGE ONE' in text and 'PUBLIC KEEP' in text and 'CONFIDENTIAL' in text, 'OCR searchable layer lost expected words')
        r.run('render', 'output/searchable.pdf', '--page', '1', '--dpi', '144', '--out', 'ocr.png')
        require(rgb_pixels(r.work / 'raster.png') == rgb_pixels(r.work / 'ocr.png'), 'OCR changed scanned image appearance')
        result['language'] = 'en'
    elif name == 'pdf-preflight':
        require(len(rows[0]['pages']) == 3 and rows[-1]['count'] == 1, 'Preflight page or form inventory mismatch')
        r.run('render', source, '--page', '1', '--dpi', '144', '--out', 'preflight.png')
    else:
        raise ValueError('Unsupported PDF scenario ' + name)
    require(hashlib.sha256((r.work / 'input.pdf').read_bytes()).hexdigest() == original, 'Source PDF modified')
    return result


def run_playbooks(r, path):
    original, previous = r.work, os.environ.get('PDFCRAFT_MODELS')
    records = []
    try:
        model_dir = original / 'ocr-models'
        model_dir.mkdir()
        for model in json.loads(Path(__file__).with_name('pdf_ocr_models.lock.json').read_text(encoding='utf-8')):
            download(model['url'], model_dir / model['file'], model['sha256'])
        os.environ['PDFCRAFT_MODELS'] = str(model_dir)
        require(json.loads(r.run('run', 'ocr_status'))['available'], 'Official OCR models not available')
        files = {json.loads(file.read_text(encoding='utf-8'))['id']:file for file in Path(path).glob('printcraft-*/references/craft-steps.json')}
        core = {'organize-pdf','compress-pdf','fill-pdf-forms','ocr-scans','pdf-preflight','redact-pdf'}
        from pdf_delivery_smoke import SCENES,run_delivery
        require(set(files) == core | set(SCENES), 'PDF scenario missing a known native driver')
        for name in sorted(core):
            recipe = json.loads(files[name].read_text(encoding='utf-8'))
            r.work = original / recipe['id']
            r.work.mkdir()
            records.append(run_recipe(r, recipe))
        r.work = original
        records.extend(run_delivery(r,Path(path)))
    finally:
        r.work = original
        if previous is None:
            os.environ.pop('PDFCRAFT_MODELS', None)
        else:
            os.environ['PDFCRAFT_MODELS'] = previous
    return records
