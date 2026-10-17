"""执行六份WordCraft核心技能，检查原生段落、表格、修订和选择保护。"""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

from craft_cli_windows import require
from office_playbook_smoke import verify_word

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
ACTION_ROWS = [['行动项', '责任人', '截止时间', '状态'],
               ['待确认事项', '待确认', '待确认', '未确认'],
               ['待补充事项', '待确认', '待确认', '未确认']]


def paragraph_text(p):
    return ''.join(x.text or '' for x in p.iter(W + 't'))


def verify_core(z, name):
    doc = ET.fromstring(z.read('word/document.xml'))
    paragraphs = doc.findall('./' + W + 'body/' + W + 'p')
    texts = [paragraph_text(p) for p in paragraphs]
    if name == 'meeting-minutes':
        verify_word(z, {'tableCells': ACTION_ROWS})
        require(any('非已决议' in text for text in texts), 'Discussion must not become an agreed decision')
        require(len(paragraphs) >= 4, 'Meeting metadata must use real paragraphs')
    elif name == 'business-proposal':
        verify_word(z, {'headingRequired': True, 'heading2Minimum': 4})
        require(all(title in texts for title in ['目标', '方案与边界', '成本依据', '验收方式']),
                'Proposal sections must be real separate paragraphs')
        require(any('待核实' in text for text in texts), 'Proposal must not invent facts')
    elif name == 'research-report':
        verify_word(z, {'headingRequired': True, 'heading2Minimum': 4})
        require(all(title in texts for title in ['问题与范围', '来源与证据', '分析与推断', '结论与未验证项']),
                'Research report structure missing')
    elif name == 'resume-layout':
        verify_word(z, {'heading2Minimum': 3})
        require(all(title in texts for title in ['工作经历', '教育经历', '技能与项目']),
                'Resume must use separate structural paragraphs')
        margins = doc.find('.//' + W + 'pgMar')
        require(margins is not None and all(margins.get(W + key) == str(value * 20)
                for key, value in {'top': 36, 'bottom': 36, 'left': 42, 'right': 42}.items()),
                'Resume page margins changed')
    elif name == 'document-style':
        require(texts == ['保留一级标题', '正文待统一', '保留强调内容'], 'Style edit changed document text')
        verify_word(z, {'headingRequired': True})
        target = paragraphs[1].find('./' + W + 'pPr/' + W + 'pStyle')
        require(target is None or target.get(W + 'val') in ('Normal', 'normal'), 'Selected body style not normalized')
        emphasis = paragraphs[2].find('.//' + W + 'b')
        require(emphasis is not None and emphasis.get(W + 'val', 'true') not in ('0', 'false'),
                'Style edit removed unrelated emphasis')
    elif name == 'document-comparison':
        deleted = ''.join(x.text or '' for x in doc.findall('.//' + W + 'del//' + W + 'delText'))
        inserted = ''.join(x.text or '' for x in doc.findall('.//' + W + 'ins//' + W + 't'))
        require('100' in deleted and '20' in deleted, 'Comparison lost original amount/date revisions')
        require('120' in inserted and '25' in inserted, 'Comparison lost revised amount/date revisions')
    else:
        raise ValueError(name)


def native(r, steps, source=None, target=None):
    argv = ['run'] + (['--file', source] if source else [])
    for step in steps:
        argv += ['--cmd', step['command'] + '=' + json.dumps(step['params'], ensure_ascii=False, separators=(',', ':'))]
    if target:
        argv += ['--save', target]
    return r.run(*argv)


def step(command, **params):
    return {'command': command, 'params': params}


def run_playbooks(r, skills):
    original = r.work
    root = original / 'word-core-scenes'
    root.mkdir()
    records = []
    try:
        files = sorted(Path(skills).glob('wordcraft-*/references/craft-steps.json'))
        require(len(files) == 6, 'Expected six WordCraft core recipes')
        for file in files:
            recipe = json.loads(file.read_text(encoding='utf-8'))
            name = recipe['id']
            r.work = root / name
            r.work.mkdir()
            source = None
            protected = {}
            if name == 'document-style':
                native(r, [step('para.heading1'), step('text.insert', text='保留一级标题'), step('text.newParagraph'),
                           step('para.heading2'), step('text.insert', text='正文待统一'), step('text.newParagraph'),
                           step('para.normal'), step('text.insert', text='保留强调内容'),
                           step('select.text', text='保留强调内容'), step('format.bold', value=True)], target='input.docx')
                source = 'input.docx'
            elif name == 'document-comparison':
                (r.work / 'input').mkdir()
                for label, text in [('original', '金额100，截止2026-10-20。'), ('revised', '金额120，截止2026-10-25。')]:
                    path = 'input/' + label + '.docx'
                    native(r, [step('text.insert', text=text)], target=path)
                    protected[path] = hashlib.sha256((r.work / path).read_bytes()).hexdigest()
                source = 'input/original.docx'
            if source:
                protected[source] = hashlib.sha256((r.work / source).read_bytes()).hexdigest()
            native(r, recipe['steps'], source, 'result.docx')
            with zipfile.ZipFile(r.work / 'result.docx') as z:
                verify_core(z, name)
            # 另一个原生进程重新读取；只读XML不能替代此往返。
            text = r.run('text', 'result.docx')
            require(bool(text.strip()), 'Reopened document has no text')
            r.run('convert', 'result.docx', 'result.pdf')
            require((r.work / 'result.pdf').read_bytes().startswith(b'%PDF'), 'PDF conversion failed')
            r.run('render', 'result.docx', 'first-page.png', '--page', '1', '--scale', '1')
            require((r.work / 'first-page.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n'), 'Document rendering failed')
            for path, digest in protected.items():
                require(hashlib.sha256((r.work / path).read_bytes()).hexdigest() == digest, 'Original input changed')
            records.append({'id': name, 'nativeDocumentChecks': 'PASS', 'hostEditorSync': 'NOT_TESTED',
                            'visualLayoutAcceptance': 'NOT_TESTED', 'scope': 'synthetic document structure and native save/reopen'})
    finally:
        r.work = original
    return records
