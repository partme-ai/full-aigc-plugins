"""工时、固定付款及月历模板：真实XLSX公式、规则、重算与原表保护。"""
import calendar
from datetime import date, timedelta
import hashlib
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile
from grid_core_smoke import native, read

N = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'


def number(actual, expected):
    assert isinstance(actual, (int, float)) and not isinstance(actual, bool), 'Expected an actual numeric result'
    assert math.isclose(actual, expected, rel_tol=1e-10, abs_tol=1e-8), 'Numeric result differs from independent calculation'


def verify_hours(rows):
    assert len(rows) == 6, 'Wrong hours result geometry'
    number(rows[0][0], 8)
    number(rows[1][0], 8)
    assert rows[0][1] == rows[1][1] == 'OK', 'Valid shift incorrectly rejected'
    assert rows[2] == ['', 'Missing input'] and rows[3] == ['', 'Review input'], 'Missing or invalid shift silently accepted'
    number(rows[5][0], 16)
    assert rows[5][1] == 'Incomplete rows excluded', 'Partial total must remain visibly incomplete'


def verify_payment(rows, principal, annual_rate, months):
    assert len(rows) == 3, 'Wrong payment result geometry'
    rate = annual_rate / 12
    monthly = principal / months if rate == 0 else principal * rate / (1 - (1 + rate) ** -months)
    for row, expected in zip(rows, [monthly, monthly * months, monthly * months - principal]):
        number(row[0], expected)


def verify_calendar(rows, year, month):
    assert len(rows) == 6 and all(len(row) == 7 for row in rows), 'Calendar must have six weeks of seven days'
    first = date(year, month, 1)
    start = first - timedelta(days=first.weekday())
    epoch = date(1899, 12, 30)
    for i, value in enumerate(v for row in rows for v in row):
        number(value, (start + timedelta(days=i) - epoch).days)
    days = [epoch + timedelta(days=int(value)) for row in rows for value in row]
    current = [d.day for d in days if d.year == year and d.month == month]
    assert current == list(range(1, calendar.monthrange(year, month)[1] + 1)), 'Calendar loses or repeats dates of the requested month'


def worksheet_xml(path, index):
    with zipfile.ZipFile(path) as archive:
        return ET.fromstring(archive.read(f'xl/worksheets/sheet{index}.xml'))


def preserve_original(before, after):
    # 新表被激活时原表的tabSelected会变化；其他XML必须保持。
    for root in [before, after]:
        for view in root.findall('.//' + N + 'sheetView'):
            view.attrib.pop('tabSelected', None)
    assert ET.tostring(before) == ET.tostring(after), 'Non-target worksheet content, formulas or formatting changed'


def formula_map(recipe):
    formulas = {}
    for step in recipe['steps']:
        command, params = step['command'], step['params']
        if command == 'cell.set' and params['input'].startswith('='):
            formulas[params['cell']] = params['input'][1:]
        if command == 'range.setValues':
            match = re.fullmatch(r'([A-Z]+)(\d+)', params['range'])
            # 本批模板的二维写入都从A列开始。
            assert match and match[1] == 'A'
            start = int(match[2])
            for r, row in enumerate(params['values']):
                for c, value in enumerate(row):
                    if isinstance(value, str) and value.startswith('='):
                        formulas[chr(65 + c) + str(start + r)] = value[1:]
    return formulas


def verify_xlsx(path, recipe):
    root = worksheet_xml(path, 2)
    formulas = {cell.attrib['r']: cell.find(N + 'f').text for cell in root.findall('.//' + N + 'c') if cell.find(N + 'f') is not None}
    assert formulas == formula_map(recipe), 'Live XLSX formulas flattened, changed or missing'
    validations = root.find(N + 'dataValidations')
    expected = {s['params']['range']: s['params'] for s in recipe['steps'] if s['command'] == 'data.validation'}
    actual = {v.attrib['sqref']: v for v in validations} if validations is not None else {}
    assert set(actual) == set(expected), 'XLSX input rules lost'
    for area, params in expected.items():
        node = actual[area]
        assert node.attrib['type'] == params['type'], 'Wrong validation type'
        assert node.find(N + 'formula1').text == params['formula1'] and node.find(N + 'formula2').text == params['formula2'], 'Input boundaries changed'
    with zipfile.ZipFile(path) as archive:
        styles = ET.fromstring(archive.read('xl/styles.xml'))
    formats = {0: 'General', 1: '0', 2: '0.00', 4: '#,##0.00', 10: '0.00%'}
    formats.update({int(node.attrib['numFmtId']): node.attrib['formatCode'] for node in styles.findall('.//' + N + 'numFmt')})
    xfs, fills = styles.find(N + 'cellXfs'), styles.find(N + 'fills')
    cells = {node.attrib['r']: node for node in root.findall('.//' + N + 'c')}
    def coordinates(area):
        match = re.fullmatch(r'([A-Z])(\d+)(?::([A-Z])(\d+))?', area)
        assert match, 'Unexpected template format range'
        left, top, right, bottom = match.groups()
        return [chr(c) + str(r) for r in range(int(top), int(bottom or top) + 1)
                for c in range(ord(left), ord(right or left) + 1)]
    for step in recipe['steps']:
        if step['command'] not in ['home.numberFormat', 'home.fillColor']:
            continue
        params = step['params']
        for address in coordinates(params['range']):
            assert address in cells, 'Formatted template cell missing'
            xf = xfs[int(cells[address].get('s', '0'))]
            if step['command'] == 'home.numberFormat':
                assert formats[int(xf.get('numFmtId', '0'))] == params['code'], 'Number/time/date format lost'
            else:
                color = fills[int(xf.get('fillId', '0'))].find('.//' + N + 'fgColor')
                assert color is not None and color.get('rgb', '')[-6:].upper() == params['color'].lstrip('#').upper(), 'Template input/weekend fill lost'


def run_templates(r, skill_root):
    original = r.work
    records = []
    try:
        for name in ['shift-timesheet', 'fixed-payment', 'month-calendar']:
            r.work = original / name
            r.work.mkdir()
            native(r, [('cell.set', {'cell': 'Z1', 'input': 'KEEP ORIGINAL'}), ('cell.set', {'cell': 'Z2', 'input': '=40+2'})], target='input.xlsx')
            input_hash = hashlib.sha256((r.work / 'input.xlsx').read_bytes()).hexdigest()
            before_xml = worksheet_xml(r.work / 'input.xlsx', 1)
            recipe = json.loads((Path(skill_root) / ('gridcraft-' + name) / 'references/craft-steps.json').read_text(encoding='utf-8'))
            sheet = recipe['sheetNameExample']
            def resolve(value):
                if isinstance(value, str) and value == '$sheet.name':
                    return sheet
                if isinstance(value, list):
                    return [resolve(v) for v in value]
                if isinstance(value, dict):
                    return {k: resolve(v) for k, v in value.items()}
                return value
            output = native(r, [(s['command'], resolve(s['params'])) for s in recipe['steps']], 'input.xlsx', 'result.xlsx')
            assert not any('error' in value for value in output), 'Template command error'
            verify_xlsx(r.work / 'result.xlsx', recipe)
            preserve_original(before_xml, worksheet_xml(r.work / 'result.xlsx', 1))
            def readback(file, area):
                return read(r, file, area, sheet=sheet)
            def mutate(label, cells):
                target = label + '.xlsx'
                native(r, [('sheet.activate', {'sheet': sheet})] + [('cell.set', {'cell': cell, 'input': value}) for cell, value in cells], 'result.xlsx', target)
                verify_xlsx(r.work / target, recipe)
                preserve_original(worksheet_xml(r.work / 'input.xlsx', 1), worksheet_xml(r.work / target, 1))
                return target
            if name == 'shift-timesheet':
                verify_hours(readback('result.xlsx', 'E2:F7'))
                for label, cells, expected, note in [
                    ('midnight', [('B2', '0'), ('C2', '0.25'), ('D2', '0')], 6, 'OK'),
                    ('same-time', [('B2', '0.25'), ('C2', '0.25')], '', 'Review input'),
                    ('negative-break', [('D2', '-0.5')], '', 'Review input'),
                    ('missing-break', [('D2', '')], '', 'Missing input'),
                    ('text-time', [('B2', 'tomorrow')], '', 'Review input')]:
                    target = mutate(label, cells)
                    rows = readback(target, 'E2:F2')
                    if expected == '':
                        assert rows == [['', note]], 'Invalid shift accepted'
                    else:
                        number(rows[0][0], expected)
                        assert rows[0][1] == note
            elif name == 'fixed-payment':
                verify_payment(readback('result.xlsx', 'B6:B8'), 12000, .06, 12)
                verify_payment(readback(mutate('zero-rate', [('B3', '0')]), 'B6:B8'), 12000, 0, 12)
                verify_payment(readback(mutate('changed-principal', [('B2', '24000')]), 'B6:B8'), 24000, .06, 12)
                for label, cells, expected in [('missing-rate', [('B3', '')], 'Missing input'),
                                                ('fractional-months', [('B4', '12.5')], 'Invalid input'),
                                                ('negative-rate', [('B3', '-0.01')], 'Invalid input'),
                                                ('zero-months', [('B4', '0')], 'Invalid input')]:
                    target = mutate(label, cells)
                    assert readback(target, 'B6:B8') == [[expected], [''], ['']], 'Invalid payment input became a normal amount'
            else:
                verify_calendar(readback('result.xlsx', 'A5:G10'), 2028, 2)
                for label, year, month in [('common-february', 2027, 2), ('december', 2026, 12), ('sunday-start', 2026, 11)]:
                    target = mutate(label, [('B1', str(year)), ('B2', str(month))])
                    verify_calendar(readback(target, 'A5:G10'), year, month)
                for label, cells in [('invalid-month', [('B2', '13')]), ('missing-year', [('B1', '')]), ('text-month', [('B2', 'Feb')])]:
                    target = mutate(label, cells)
                    assert all(value == '' for row in readback(target, 'A5:G10') for value in row), 'Invalid month/year generated misleading dates'
            assert hashlib.sha256((r.work / 'input.xlsx').read_bytes()).hexdigest() == input_hash, 'Input workbook overwritten'
            records.append({'id': name, 'nativeRecalculationAndXlsxFormulas': 'PASS', 'inputRulesAndOriginalWorksheet': 'PASS',
                            'externalExcelRendering': 'NOT_TESTED', 'installedHostSync': 'NOT_TESTED'})
        return records
    finally:
        r.work = original
