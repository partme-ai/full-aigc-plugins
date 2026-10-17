"""六个GridCraft核心场景：原生XLSX保存/重算/图表刷新及数据保护。"""
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

from craft_cli_windows import require

C = 'http://schemas.openxmlformats.org/drawingml/2006/chart'
CSV_ROWS = [['ID,Name,Amount,Region'], ['001,Alice,10,E'], ['002,Bob,20,W'],
            ['001,Alice,10,E'], ['1,Carol,30,N'], ['001,Alice,11,E']]


def native(r, steps, source=None, target=None):
    args = ['run'] + (['--in', source] if source else [])
    for command, params in steps:
        args += ['--cmd', command + '=' + json.dumps(params, ensure_ascii=False, separators=(',', ':'))]
    if target:
        args += ['--out', target]
    return [json.loads(line) for line in r.run(*args).splitlines() if line.strip()]


def read(r, file, area, formulas=False, sheet=None):
    params = {'range': area, 'formulas': formulas, 'formatted': False}
    if sheet:
        params['sheet'] = sheet
    return native(r, [('sheet.read', params)], file)[0]['result']['values']


def verify_clean_rows(rows):
    require(all(isinstance(row[0], str) for row in rows[1:]), 'Primary keys must remain text')
    expected = [['ID', 'Name', 'Amount', 'Region'], ['001', 'Alice', 10, 'E'],
                ['002', 'Bob', 20, 'W'], ['1', 'Carol', 30, 'N'], ['001', 'Alice', 11, 'E']]
    require(rows == expected, 'Cleaning lost leading zeros, stable order or a conflicting record')


def verify_audit(errors, precedents, evaluation):
    require(any(item['cell'] == 'H3' and item['error'] == '#DIV/0!' for item in errors['errors']),
            'Formula error checker missed the known error')
    require({item['range'] for item in precedents} == {'B2', 'C2'}, 'Formula precedents mismatch')
    require(evaluation['result'] == 20, 'Formula evaluator result mismatch')


def verify_chart(path, expected):
    with zipfile.ZipFile(path) as z:
        names = [name for name in z.namelist() if name.startswith('xl/charts/chart') and name.endswith('.xml')]
        require(len(names) == 1, 'Dashboard editable chart missing')
        xml = z.read(names[0]).decode('utf-8')
        doc = ET.fromstring(xml)
        values = [float(node.text) for node in doc.findall('.//{' + C + '}numCache/{' + C + '}pt/{' + C + '}v')]
        require(values == expected, 'Dashboard chart cached values did not refresh')
        require('G2:G3' in xml.replace('$', ''), 'Dashboard chart lost its live source range')


def fixture(r, name):
    steps = [('cell.set', {'cell': 'Z1', 'input': 'PRESERVE SENTINEL'})]
    if name == 'clean-table':
        steps.append(('range.setValues', {'range': 'A1', 'values': CSV_ROWS}))
    elif name == 'formula-audit':
        steps += [('range.setValues', {'range': 'B2', 'values': [[100, 0.2]]}),
                  ('cell.set', {'cell': 'H2', 'input': '=B2*C2'}), ('cell.set', {'cell': 'H3', 'input': '=1/0'})]
    elif name == 'reconcile-data':
        steps += [('range.setValues', {'range': 'A1', 'values': [['Key', 'Amount'], ['O1', 100], ['O2', 70], ['O3', 50], [None, 9]]}),
                  ('home.insertSheet', {'name': 'Sheet2'}),
                  ('range.setValues', {'range': 'A1', 'values': [['Key', 'Amount'], ['O1', 90], ['O1', 100], ['O2', 70]]}),
                  ('sheet.activate', {'sheet': 'Sheet1'})]
    elif name == 'sales-summary':
        steps += [('range.setValues', {'range': 'A1', 'values': [['Region', 'Order', 'Quantity', 'Amount'],
                   ['East', 'S1', 1, 100], ['West', 'S2', 1, 80], ['East', 'Return', 1, -20]]}),
                  ('range.setValues', {'range': 'F1', 'values': [['Region', 'Total'], ['East'], ['West']]})]
    native(r, steps, target='input.xlsx')


def run_recipe(r, recipe):
    name = recipe['id']
    fixture(r, name)
    digest = hashlib.sha256((r.work / 'input.xlsx').read_bytes()).hexdigest()
    rows = native(r, [(step['command'], step['params']) for step in recipe['steps']], 'input.xlsx', 'result.xlsx')
    def mutation(changes, target):
        native(r, changes, 'result.xlsx', target)
        require(read(r, target, 'Z1')[0][0] == 'PRESERVE SENTINEL', 'Unrelated cell changed during mutation')
    if name == 'budget-tracker':
        require(read(r, 'result.xlsx', 'D2')[0][0] == 20, 'Initial budget difference mismatch')
        for label, changes, expected in [
            ('missing-budget', [('cell.set', {'cell': 'B2', 'input': ''})], '待确认预算'),
            ('zero-budget', [('cell.set', {'cell': 'B2', 'input': '0'})], -80),
            ('missing-actual', [('cell.set', {'cell': 'C2', 'input': ''})], '待确认实际'),
            ('zero-actual', [('cell.set', {'cell': 'C2', 'input': '0'})], 100),
        ]:
            target = label + '.xlsx'
            mutation(changes, target)
            require(read(r, target, 'D2')[0][0] == expected, 'Budget blank/zero distinction failed: ' + label)
    elif name == 'clean-table':
        verify_clean_rows(read(r, 'result.xlsx', 'F1:I5'))
        require(read(r, 'result.xlsx', 'A1:A6') == CSV_ROWS, 'Cleaning overwrote original CSV input')
    elif name == 'formula-audit':
        results = {row['command']: row['result'] for row in rows}
        verify_audit(results['formulas.errorChecking'], results['formulas.tracePrecedents'], results['formulas.evaluateFormula'])
        mutation([('cell.set', {'cell': 'B2', 'input': '125'})], 'recalculated.xlsx')
        require(read(r, 'recalculated.xlsx', 'H2')[0][0] == 25, 'Saved formula did not recalculate after input change')
    elif name == 'reconcile-data':
        expected = [['重复键', ''], [70, 0], ['未匹配', ''], ['缺少主键', '']]
        require(read(r, 'result.xlsx', 'E2:F5') == expected, 'Reconciliation lost missing/duplicate/amount status')
        require('COUNTIF' in read(r, 'result.xlsx', 'E2', True)[0][0], 'Reconciliation guard formula lost')
        mutation([('sheet.activate', {'sheet': 'Sheet2'}), ('cell.set', {'cell': 'A3', 'input': 'O9'}),
                  ('sheet.activate', {'sheet': 'Sheet1'})], 'unique-key.xlsx')
        require(read(r, 'unique-key.xlsx', 'E2:F2') == [[90, 10]], 'Cross-sheet lookup and difference did not recalculate')
        require(read(r, 'result.xlsx', 'A2:B5') == [['O1', 100], ['O2', 70], ['O3', 50], [None, 9]],
                'Reconciliation deleted original unmatched records')
    elif name == 'dashboard':
        verify_chart(r.work / 'result.xlsx', [21, 42])
        mutation([('cell.set', {'cell': 'G3', 'input': '84'})], 'refreshed-chart.xlsx')
        require(read(r, 'refreshed-chart.xlsx', 'G3')[0][0] == 84, 'Dashboard data update not saved')
        verify_chart(r.work / 'refreshed-chart.xlsx', [21, 84])
    elif name == 'sales-summary':
        require(read(r, 'result.xlsx', 'G2')[0][0] == 80, 'Sales summary did not include the return')
        mutation([('cell.set', {'cell': 'D2', 'input': '120'})], 'updated-sales.xlsx')
        require(read(r, 'updated-sales.xlsx', 'G2')[0][0] == 100, 'Sales summary did not update after data change')
        with zipfile.ZipFile(r.work / 'result.xlsx') as z:
            require('xl/tables/table1.xml' in z.namelist(), 'Editable sales table missing')
    else:
        raise ValueError('Unsupported GridCraft core scene ' + name)
    require(read(r, 'result.xlsx', 'Z1')[0][0] == 'PRESERVE SENTINEL', 'Scenario overwrote unrelated cell')
    require(hashlib.sha256((r.work / 'input.xlsx').read_bytes()).hexdigest() == digest, 'Input workbook modified')
    return {'id': name, 'nativeWorkbookAndBusinessChecks': 'PASS', 'hostEditorSync': 'NOT_TESTED',
            'scope': 'synthetic business rows and XLSX/engine checks; no real financial reconciliation acceptance'}


def run_playbooks(r, skills):
    original = r.work
    root = original / 'grid-core-scenes'
    root.mkdir()
    records = []
    try:
        files = sorted(Path(skills).glob('gridcraft-*/references/craft-steps.json'))
        require(len(files) == 6, 'Expected six GridCraft core skill recipes')
        for file in files:
            recipe = json.loads(file.read_text(encoding='utf-8'))
            r.work = root / recipe['id']
            r.work.mkdir()
            records.append(run_recipe(r, recipe))
    finally:
        r.work = original
    return records
