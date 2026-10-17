"""WordCraft main：原生页眉页脚与筛选排序邮件合并的业务交付。"""
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def text(z, name):
    return ' '.join(x.text or '' for x in ET.fromstring(z.read(name)).iter(NS + 't'))


def verify_headers(path):
    with zipfile.ZipFile(path) as z:
        assert 'MAIN BODY' in text(z, 'word/document.xml'), 'Body content lost'
        for part, marker in [('header', 'MAIN HEADER'), ('footer', 'MAIN FOOTER')]:
            parts = [n for n in z.namelist() if n.startswith('word/' + part) and n.endswith('.xml')]
            assert any(marker in text(z, n) for n in parts), 'Native ' + part + ' missing'


def verify_mail(path):
    with zipfile.ZipFile(path) as z:
        result = text(z, 'word/document.xml')
    assert 'INACTIVE-BOB' not in result, 'Filtered-out recipient was merged'
    assert result.count('ACTIVE-CAROL') == result.count('ACTIVE-ALICE') == 1, 'Wrong merged recipient count'
    assert result.index('ACTIVE-CAROL') < result.index('ACTIVE-ALICE'), 'Recipient sort order ignored'


def batch(r, commands, output):
    args = ['run']
    for name, params in commands:
        args += ['--cmd', name + '=' + json.dumps(params, ensure_ascii=False, separators=(',', ':'))]
    return r.run(*args, '--save', output)


def run_checks(r):
    folder = r.work / 'main-capabilities'
    folder.mkdir()
    original = r.work
    r.work = folder
    try:
        batch(r, [('text.insert', {'text': 'MAIN BODY'}),
                  ('insert.createHeader', {'page': 0}), ('text.insert', {'text': 'MAIN HEADER'}),
                  ('insert.createFooter', {'page': 0}), ('text.insert', {'text': 'MAIN FOOTER'})], 'headers.docx')
        verify_headers(folder / 'headers.docx')
        batch(r, [('mailings.start', {'kind': 'letters'}),
                  ('mailings.recipients', {'rows': [
                      {'Name': 'ACTIVE-ALICE', 'Status': 'active', 'Rank': '2'},
                      {'Name': 'INACTIVE-BOB', 'Status': 'inactive', 'Rank': '3'},
                      {'Name': 'ACTIVE-CAROL', 'Status': 'active', 'Rank': '1'}]}),
                  ('mailings.insertField', {'field': 'Name'}),
                  ('mailings.filterRecipients', {'rules': [{'field': 'Status', 'op': 'equal', 'value': 'active'}]}),
                  ('mailings.sortRecipients', {'field': 'Rank', 'descending': False}),
                  ('mailings.finish', {'path': 'merged.docx'})], 'template.docx')
        verify_mail(folder / 'merged.docx')
        # 再用新进程读取实际交付文件；不以CLI日志字符串代替DOCX内容。
        assert 'MAIN BODY' in r.run('text', 'headers.docx')
        merged = r.run('text', 'merged.docx')
        assert 'INACTIVE-BOB' not in merged and merged.index('ACTIVE-CAROL') < merged.index('ACTIVE-ALICE')
        return {'nativeHeaderFooter': 'PASS', 'filteredSortedMerge': 'PASS',
                'savedNativePartsAndFreshProcessReadback': 'PASS', 'installedHostSync': 'NOT_TESTED'}
    finally:
        r.work = original
