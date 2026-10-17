"""实际执行短表评审配方，核对原生表格与PPTX；不替代宿主同步验收。"""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

VALUES = [['Criterion', 'Option A', 'Option B'], ['Cost', '1200 USD/year', '1600 USD/year'],
          ['Delivery', '4 weeks', '3 weeks'], ['Risk', 'Vendor dependency', 'Training required']]
A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'


def verify_table(table):
    actual = [['\n'.join(''.join(run.get('text', '') for run in p.get('runs', []))
                        for p in cell['text']['paragraphs']) for cell in row['cells']]
              for row in table['rows']]
    assert actual == VALUES, 'Comparison cells missing, swapped, or changed'
    assert table['cols'] == [220, 310, 310], 'Column widths or total table width changed'


def native_table(path):
    with zipfile.ZipFile(path) as archive:
        presentation = json.loads(archive.read('presentation.json'))['presentation']
    assert len(presentation['slides']) == 1, 'Unexpected slide count'
    tables = [s for s in presentation['slides'][0]['shapes'] if s['kind']['type'] == 'table']
    assert len(tables) == 1, 'Expected one editable native table'
    return tables[0], presentation


def run_comparison(r, skill_root):
    original = r.work
    r.work = original / 'option-comparison'
    r.work.mkdir()
    try:
        def batch(steps, output, source=None):
            argv = ['run'] + (['--in', source] if source else [])
            for step in steps:
                params = dict(step['params'])
                if params.get('id') == '$table.id':
                    params['id'] = table_id
                argv += ['--cmd', step['command'] + '=' + json.dumps(params)]
            r.run(*argv, '--save', output)
        recipe = json.loads((Path(skill_root) / 'deckcraft-option-comparison/references/craft-steps.json').read_text())
        steps = recipe['steps']
        cut = next(i for i, step in enumerate(steps) if step.get('capture') == 'table.id') + 1
        batch(steps[:cut], 'input.deckcraft')
        source_hash = hashlib.sha256((r.work / 'input.deckcraft').read_bytes()).hexdigest()
        shape, _ = native_table(r.work / 'input.deckcraft')
        table_id = shape['id']
        batch(steps[cut:], 'comparison.deckcraft', 'input.deckcraft')
        shape, doc = native_table(r.work / 'comparison.deckcraft')
        verify_table(shape['kind'])
        assert shape['xfrm']['x'] == 60 and shape['xfrm']['w'] == 840, 'Table geometry changed'
        notes = doc['slides'][0]['notes']
        assert 'Illustrative data only.' in str(notes), 'Data assumptions missing from slide notes'
        r.run('convert', 'comparison.deckcraft', 'comparison.pptx')
        with zipfile.ZipFile(r.work / 'comparison.pptx') as archive:
            slide = ET.fromstring(archive.read('ppt/slides/slide1.xml'))
            tables = slide.findall('.//' + A + 'tbl')
            assert len(tables) == 1, 'PPTX table flattened or lost'
            actual = [[''.join(cell.itertext()) for cell in row.findall(A + 'tc')]
                      for row in tables[0].findall(A + 'tr')]
            assert actual == VALUES, 'PPTX editable cell contents changed'
        r.run('convert', 'comparison.pptx', 'reopened.deckcraft')
        table, _ = native_table(r.work / 'reopened.deckcraft')
        verify_table(table['kind'])
        batch([{'command': 'text.set', 'params': {'id': table['id'], 'cell': [1, 1], 'text': 'Revised 1250 USD/year'}}],
              'revised.deckcraft', 'reopened.deckcraft')
        revised, _ = native_table(r.work / 'revised.deckcraft')
        assert 'Revised 1250 USD/year' in str(revised['kind']['rows'][1]['cells'][1]['text']), 'Reopened cell cannot be edited'
        assert hashlib.sha256((r.work / 'input.deckcraft').read_bytes()).hexdigest() == source_hash, 'Input modified'
        r.run('render', 'comparison.deckcraft', '--slide', '0', 'comparison.png')
        return {'scenario': 'option-comparison', 'nativeTable': 'PASS', 'pptxRoundTripAndCellEdit': 'PASS',
                'inputPreserved': 'PASS', 'externalPowerPointRendering': 'NOT_TESTED', 'installedHostSync': 'NOT_TESTED'}
    finally:
        r.work = original
