"""执行技能源中的文档排版步骤，核对真实DOCX结构和重开导出。"""
import hashlib
import json
import re
from pathlib import Path
import struct
import xml.etree.ElementTree as ET
import zipfile
import zlib

from craft_cli_windows import require, png_fixture
from office_playbook_smoke import verify_word
from word_core_smoke import native

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
WP = '{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}'
A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
SCENES = ['toc-handbook', 'illustrated-guide', 'landscape-appendix']
HEADINGS = ['安装准备', '安装步骤', '使用与排错', '排错路径']


def verify_toc(doc):
    """目录必须为真实域，且每个跳转目标均存在。"""
    toc = doc.find('.//' + W + 'sdtContent')
    require(toc is not None, 'Missing editable table of contents')
    fields = ''.join(x.text or '' for x in toc.iter(W + 'instrText'))
    require('TOC' in fields and '1-2' in fields, 'Missing two-level TOC field')
    links = toc.findall('.//' + W + 'hyperlink')
    require(len(links) == 4, 'TOC must contain exactly four actual headings')
    bookmarks = {x.get(W + 'name') for x in doc.iter(W + 'bookmarkStart')}
    for title, link in zip(HEADINGS, links):
        require(title in ''.join(link.itertext()), 'TOC heading mismatch')
        require(link.get(W + 'anchor') in bookmarks, 'TOC points to a missing bookmark')
    levels = [x.get(W + 'val') for x in toc.iter(W + 'pStyle')]
    require(levels.count('TOC1') == 2 and levels.count('TOC2') == 2, 'TOC hierarchy lost')


def verify_sections(doc):
    """只允许附录横向，正文保持A4纵向。"""
    sections = doc.findall('.//' + W + 'sectPr')
    require(len(sections) == 2, 'Expected real separate body/appendix sections')
    sizes = [s.find(W + 'pgSz') for s in sections]
    require(all(s is not None for s in sizes), 'Section page dimensions missing')
    dimensions = [(int(s.get(W + 'w')), int(s.get(W + 'h'))) for s in sizes]
    require(dimensions == [(11906, 16838), (16838, 11906)], 'Body or appendix A4 orientation wrong')
    # 分节必须位于附录标题之前，不能只在最后补一个无关的节。
    body = doc.find(W + 'body')
    section_index = next((i for i, p in enumerate(body) if p.find('.//' + W + 'sectPr') is not None), -1)
    appendix_index = next((i for i, p in enumerate(body) if '附录：对照矩阵' in ''.join(p.itertext())), -1)
    require(0 <= section_index < appendix_index, 'Section boundary must precede appendix')


def verify_pictures(z, source_bytes):
    """两幅图片应有正确尺寸、替代文本、关系及连续SEQ题注。"""
    doc = ET.fromstring(z.read('word/document.xml'))
    drawings = doc.findall('.//' + WP + 'inline')
    require(len(drawings) == 2, 'Expected two real embedded pictures')
    relationships = {x.get('Id'): x.get('Target') for x in ET.fromstring(z.read('word/_rels/document.xml.rels'))}
    for drawing, name, width, alt in zip(drawings, ['config.png', 'connect.png'], [240, 180], ['配置步骤截图', '连接检查截图']):
        extent = drawing.find(WP + 'extent')
        require(int(extent.get('cx')) == width * 12700 and int(extent.get('cy')) == width * 12700 * 3 // 4,
                'Picture dimensions/aspect ratio wrong')
        require(drawing.find(WP + 'docPr').get('descr') == alt, 'Picture alternative text lost')
        ref = drawing.find('.//' + A + 'blip').get(R + 'embed')
        target = relationships.get(ref)
        require(target is not None and target.startswith('media/'), 'Picture relationship missing or unsafe')
        require(z.read('word/' + target) == source_bytes[name], 'Embedded picture differs from actual input')
    paragraphs = list(doc.find(W + 'body'))
    captions = [p for p in paragraphs if any('SEQ Figure' in (x.text or '') for x in p.iter(W + 'instrText'))]
    require(len(captions) == 2, 'Caption numbers must be real SEQ fields')
    for index, (caption, label) in enumerate(zip(captions, ['配置位置示例', '连接检查示例']), 1):
        text = ''.join(caption.itertext())
        require(label in text, 'Caption text lost')
        require(str(index) in [x.text for x in caption.iter(W + 't')], 'Caption sequence number wrong')
        position = paragraphs.index(caption)
        require(position > 0 and paragraphs[position - 1].find('.//' + W + 'drawing') is not None,
                'Caption is not immediately after its picture')


def alternate_png(path):
    """第二幅原创64×48合成图，不能与第一幅字节相同。"""
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    rows = b''.join(b'\0' + bytes((40, 100, 220)) * 64 for _ in range(48))
    path.write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 64, 48, 8, 2, 0, 0, 0))
                     + chunk(b'IDAT', zlib.compress(rows)) + chunk(b'IEND', b''))


def run_playbooks(r, skills):
    """直接运行各独立技能的原始步骤，不复制另一套业务配方。"""
    original_work = r.work
    records = []
    try:
        for name in SCENES:
            recipe = json.loads((Path(skills) / ('wordcraft-' + name) / 'references/craft-steps.json').read_text(encoding='utf-8'))
            require(recipe['id'] == name, 'Wrong Word scene recipe')
            r.work = original_work / name
            r.work.mkdir()
            sources = {}
            if name == 'illustrated-guide':
                (r.work / 'input').mkdir()
                png_fixture(r.work / 'input/config.png')
                alternate_png(r.work / 'input/connect.png')
                sources = {p.name: p.read_bytes() for p in (r.work / 'input').glob('*.png')}
            native(r, recipe['steps'], target='result.docx')
            with zipfile.ZipFile(r.work / 'result.docx') as z:
                doc = ET.fromstring(z.read('word/document.xml'))
                if name == 'toc-handbook':
                    verify_toc(doc)
                elif name == 'illustrated-guide':
                    verify_pictures(z, sources)
                else:
                    verify_sections(doc)
                    verify_word(z, {'tableCells': [['方案', '适用范围', '限制', '负责人'], ['方案甲', '示例范围', '待核实', '待确认']]})
                    require(doc.find('.//' + W + 'tblHeader') is not None, 'Repeating table header missing')
            text = r.run('text', 'result.docx')
            require(bool(text.strip()), 'Reopened document text missing')
            # 真正重开并保存，不能只读取ZIP里的XML。
            native(r, [{'command': 'document.inspect', 'params': {'text': True}}], source='result.docx', target='reopened.docx')
            with zipfile.ZipFile(r.work / 'reopened.docx') as z:
                if name == 'toc-handbook': verify_toc(ET.fromstring(z.read('word/document.xml')))
                elif name == 'illustrated-guide': verify_pictures(z, sources)
                else: verify_sections(ET.fromstring(z.read('word/document.xml')))
            r.run('convert', 'reopened.docx', 'review.pdf')
            pdf = (r.work / 'review.pdf').read_bytes()
            require(pdf.startswith(b'%PDF'), 'PDF export invalid')
            if name == 'landscape-appendix':
                boxes = [[float(x) for x in box.split()] for box in re.findall(rb'/MediaBox\s*\[([^\]]+)\]', pdf)]
                require(len(boxes) == 2, 'Expected two actual exported PDF pages')
                for box, expected in zip(boxes, [(595.3, 841.9), (841.9, 595.3)]):
                    require(len(box) == 4 and abs(box[2] - expected[0]) < .2 and abs(box[3] - expected[1]) < .2,
                            'Exported PDF page orientation/dimensions wrong')
            pages = 2 if name == 'landscape-appendix' else 1
            for page in range(1, pages + 1):
                r.run('render', 'reopened.docx', 'page-' + str(page) + '.png', '--page', str(page), '--scale', '1')
                data = (r.work / ('page-' + str(page) + '.png')).read_bytes()
                require(data.startswith(b'\x89PNG\r\n\x1a\n'), 'Native rendered page invalid')
                if name == 'landscape-appendix':
                    width, height = struct.unpack('>II', data[16:24])
                    require((width < height) if page == 1 else (width > height), 'Rendered page orientation wrong')
            for source, data in sources.items():
                require((r.work / 'input' / source).read_bytes() == data, 'Input picture changed')
            records.append({'id': name, 'recipeSha256': hashlib.sha256((Path(skills) / ('wordcraft-' + name) / 'references/craft-steps.json').read_bytes()).hexdigest(),
                            'nativeSaveReopenAndStructure': 'PASS', 'hostEditorSync': 'NOT_TESTED',
                            'realContentLayout': 'NOT_TESTED', 'scope': 'original short synthetic documents and two synthetic PNG inputs'})
    finally:
        r.work = original_work
    return records
