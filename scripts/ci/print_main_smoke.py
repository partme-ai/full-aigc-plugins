"""PrintCraft main：可选页字数和定向未标记内容检查，保持源PDF不变。"""
import hashlib
import json
from pdf_playbook_smoke import write_pdf, script


def verify_count(report):
    assert report['total']['words'] == 3, 'Wrong Unicode word count'
    assert len(report['pages']) == 1, 'Repeated page was counted twice'


def run_checks(r):
    original = r.work
    r.work = original / 'main-pdf-statistics'
    r.work.mkdir()
    try:
        content = b'BT /F1 12 Tf 20 100 Td (alpha beta gamma) Tj ET\n'
        objects = [b'<< /Type /Catalog /Pages 2 0 R >>', b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
                   b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 150] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',
                   b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
                   f'<< /Length {len(content)} >>\nstream\n'.encode() + content + b'endstream']
        for name in ['input.pdf', 'decoy.pdf']:
            write_pdf(r.work / name, objects)
        source = r.work / 'input.pdf'
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        rows = script(r, 'main', [
            {'command': 'text_word_count', 'params': {'doc': 1, 'pages': [1, 1]}},
            {'command': 'accessibility_find_untagged', 'params': {'doc': 1, 'pages': [1]}},
        ])
        verify_count(rows[0])
        active = {x['rule']: x for x in rows[1]['results'] if x['status'] != 'skipped'}
        assert set(active) == {'tagged-content', 'tagged-annotations', 'tagged-form-fields'}, 'Focused audit changed scope'
        assert active['tagged-content']['status'] == 'failed', 'Untagged input incorrectly passed'
        assert hashlib.sha256(source.read_bytes()).hexdigest() == digest, 'Read-only tools changed input'
        (r.work / 'main-report.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
        return {'unicodeWordCountAndPageDedup': 'PASS', 'untaggedContentFound': 'PASS',
                'sourceUnchanged': 'PASS', 'fullAccessibilityCertification': 'NOT_TESTED', 'installedHostSync': 'NOT_TESTED'}
    finally:
        r.work = original
