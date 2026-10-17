"""FigCraft主题变量、可换图标按钮和有符号柱图的实际CLI回归。"""
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import struct
import xml.etree.ElementTree as ET
import zipfile
from fig_playbook_smoke import read_nodes, near
from photo_playbook_smoke import rgb_pixels


def bar_geometry(values):
    if not values or any(type(v) not in (int, float) or not math.isfinite(v) for v in values):
        raise ValueError('Expected nonempty finite numeric values, not missing/boolean/string values')
    low, high = min(0, min(values)), max(0, max(values))
    if low == high:
        low, high = -1, 1
    y = lambda value: 200 + (high - value) / (high - low) * 600
    baseline = y(0)
    return baseline, [(min(baseline, y(v)), abs(baseline - y(v))) for v in values]


def verify_icon_instance(node, icon_id, label, shown):
    assert node['componentProperties'] == {'Icon': icon_id, 'Show Icon': shown, 'Label': label}
    icon = next(x for x in node['children'] if x['type'] == 'INSTANCE')
    assert icon['mainComponent'] == icon_id and icon.get('visible', True) == shown
    assert any(c.get('characters') == label for c in node['children'])


def verify_alias_export(tokens, semantic_id, palette_id):
    values = tokens['meta']['variables'][semantic_id]['valuesByMode']
    assert len(values) == 2 and all(value == {'type': 'VARIABLE_ALIAS', 'id': palette_id}
                                  for value in values.values()), 'Semantic alias was flattened or points elsewhere'


def run_design_workflows(r, skill_root, scenes=None):
    original = r.work
    records = []
    try:
        for scene in scenes or ['light-dark-token-card', 'swappable-icon-button', 'signed-bar-chart']:
            r.work = original / scene
            r.work.mkdir()
            folder = Path(skill_root) / ('figcraft-' + scene)
            spec = importlib.util.spec_from_file_location('fig_design_recipe', folder / 'scripts/run_recipe.py')
            helper = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(helper)
            recipe = json.loads((folder / 'references/craft-steps.json').read_text(encoding='utf-8'))
            fixture = {'steps': [
                {'command': 'file.new', 'params': {'name': 'Existing user design'}},
                {'command': 'node.create', 'params': {'type': 'frame', 'name': 'Protected note', 'x': -256, 'y': 0,
                    'width': 200, 'height': 120, 'props': {'fill': '#fedf89'}}, 'capture': 'guard'},
                {'command': 'node.create', 'params': {'type': 'text', 'name': 'User text', 'text': 'KEEP USER TEXT',
                    'width': 180, 'height': 24, 'parent': {'$ref': 'guard.id'}, 'props': {'fontSize': 16}}, 'capture': 'note'}]}
            source = r.work / 'input.figcraft'
            initial = helper.execute_recipe(fixture, r.run, r.work, source)
            initial_nodes = read_nodes(r, source, initial['bindings'])
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            target = r.work / 'result.figcraft'
            receipt = helper.execute_recipe(recipe, r.run, r.work, target, source)
            (r.work / 'receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
            assert not any(row['command'] == 'file.new' for row in receipt['steps']), 'Existing file was initialized'
            assert read_nodes(r, target, initial['bindings']) == initial_nodes
            bindings = receipt['bindings']
            selected = {k: bindings[k] for k in recipe['nodeBindings']}
            nodes = read_nodes(r, target, selected)
            assert [nodes['root']['width'], nodes['root']['height']] == [1280, 1024]
            modified = []

            def query(steps, output=None, input_file=target):
                script = r.work / 'query.json'
                script.write_text(json.dumps(steps, ensure_ascii=False), encoding='utf-8')
                args = ['run', script, '--in', input_file] + (['--out', output] if output else [])
                rows = [json.loads(line) for line in r.run(*args).splitlines() if line.strip()]
                assert len(rows) == len(steps) and all(x.get('ok') is True for x in rows)
                if output:
                    modified.append(output)
                return [x['result'] for x in rows]

            def export(file, name):
                r.run('export', file, '--node', str(bindings['root']['id']), '-o', name + '.png', '--format', 'png')
                assert struct.unpack('>II', (r.work / (name + '.png')).read_bytes()[16:24]) == (1280, 1024)
                r.run('export', file, '--node', str(bindings['root']['id']), '-o', name + '.svg', '--format', 'svg')
                ET.parse(r.work / (name + '.svg'))

            export(target, 'proof')
            if scene == 'light-dark-token-card':
                for key, color in [('light', '#FFFFFF'), ('dark', '#101828'),
                                   ('lightTitle', '#101828'), ('darkTitle', '#FFFFFF')]:
                    assert nodes[key]['fills'][0]['color'] == color, 'Inherited theme color wrong: ' + key
                assert nodes['dark']['boundVariables']['fill'] == bindings['semanticSurface']['id']
                tokens = bindings['tokens']['text']
                token_data = json.loads(tokens)
                verify_alias_export(token_data, bindings['semanticSurface']['id'], bindings['surface']['id'])
                verify_alias_export(token_data, bindings['semanticText']['id'], bindings['foreground']['id'])
                css = bindings['css']['text']
                assert ':root' in css and '[data-review-theme="Dark"]' in css
                (r.work / 'tokens.json').write_text(tokens, encoding='utf-8')
                (r.work / 'tokens.css').write_text(css, encoding='utf-8')
                changed = r.work / 'changed-dark.figcraft'
                query([{'command': 'variable.set', 'params': {'variable': bindings['surface']['id'],
                        'mode': 'Dark', 'value': '#1d2939'}}], changed)
                after = read_nodes(r, changed, selected)
                assert after['dark']['fills'][0]['color'] == '#1D2939'
                assert after['light'] == nodes['light'] and after['lightTitle'] == nodes['lightTitle']
                assert read_nodes(r, changed, initial['bindings']) == initial_nodes
                export(changed, 'changed-dark')
            elif scene == 'swappable-icon-button':
                for key, expected in [('iconProperty', 'Icon'), ('labelProperty', 'Label'), ('showProperty', 'Show Icon')]:
                    assert bindings[key]['name'] == expected, 'Property name differed; literal keys no longer valid'
                assert not bindings['properties']['conflicts']
                verify_icon_instance(nodes['first'], bindings['iconB']['id'], 'Save', True)
                verify_icon_instance(nodes['second'], bindings['iconA']['id'], 'Back', False)
                visible_label = next(c for c in nodes['first']['children'] if c.get('characters') == 'Save')
                hidden_label = next(c for c in nodes['second']['children'] if c.get('characters') == 'Back')
                assert near(visible_label['x'], 36) and near(hidden_label['x'], 12), 'Hidden icon left a false gap'
                assert nodes['label']['characters'] == 'Continue', 'Instance text changed main component'
                changed = r.work / 'changed-main.figcraft'
                query([{'command': 'node.set', 'params': {'id': bindings['main']['id'], 'props': {'fill': '#c7d7fe'}}}], changed)
                after = read_nodes(r, changed, selected)
                verify_icon_instance(after['first'], bindings['iconB']['id'], 'Save', True)
                verify_icon_instance(after['second'], bindings['iconA']['id'], 'Back', False)
                assert all(after[k]['fills'][0]['color'] == '#C7D7FE' for k in ['first', 'second'])
                export(changed, 'changed-main')
            else:
                values = recipe['exampleData']['values']
                baseline, geometry = bar_geometry(values)
                assert near(nodes['baseline']['y'], baseline)
                for i, (y, height) in enumerate(geometry):
                    assert near(nodes['bar' + str(i)]['y'], y) and near(nodes['bar' + str(i)]['height'], height)
                    assert nodes['value' + str(i)]['characters'] == str(values[i])
                width, _, pixels = rgb_pixels(r.work / 'proof.png')
                def pixel(x, y):
                    return tuple(pixels[(y * width + x) * 3:(y * width + x) * 3 + 3])
                assert pixel(264, 740) == (217, 45, 32), 'Negative bar not rendered below baseline'
                assert pixel(984, 300) == (21, 112, 239), 'Positive bar not rendered above baseline'
                assert pixel(504, 740) == (255, 255, 255), 'Zero value rendered a false column'
                for name, values in [('all-zero', [0, 0, 0, 0]), ('negative-only', [-80, -40, -20, -10])]:
                    baseline, geometry = bar_geometry(values)
                    steps = [{'command': 'node.set', 'params': {'id': bindings['baseline']['id'], 'props': {'y': baseline}}}]
                    for i, (y, height) in enumerate(geometry):
                        steps += [
                            {'command': 'node.set', 'params': {'id': bindings['bar' + str(i)]['id'],
                                'props': {'y': y, 'height': height, 'fill': '#d92d20' if values[i] < 0 else '#1570ef',
                                    'pluginData': {'scene': 'signed-bar-chart',
                                        'category': recipe['exampleData']['categories'][i], 'value': str(values[i])}}}},
                            {'command': 'node.set', 'params': {'id': bindings['value' + str(i)]['id'],
                                'props': {'characters': str(values[i]), 'y': y + height + 8 if values[i] < 0 else y - 42}}}]
                    changed = r.work / (name + '.figcraft')
                    query(steps, changed)
                    after = read_nodes(r, changed, selected)
                    for i, (y, height) in enumerate(geometry):
                        assert near(after['bar' + str(i)]['y'], y) and near(after['bar' + str(i)]['height'], height)
                        assert after['value' + str(i)]['characters'] == str(values[i])
                    with zipfile.ZipFile(changed) as archive:
                        document = json.loads(archive.read('document.json'))
                    for i, value in enumerate(values):
                        assert document['nodes'][str(bindings['bar' + str(i)]['id'])]['plugin_data']['value'] == str(value)
                    export(changed, name)
            assert hashlib.sha256(source.read_bytes()).hexdigest() == digest
            assert read_nodes(r, target, initial['bindings']) == initial_nodes
            for changed in modified:
                assert read_nodes(r, changed, initial['bindings']) == initial_nodes, 'Modified result changed protected user nodes'
            # 每个场景也验证独立新文件分支；不只检查已有文件跳过初始化的路径。
            fresh = r.work / 'fresh.figcraft'
            new = helper.execute_recipe(recipe, r.run, r.work, fresh)
            fresh_nodes = read_nodes(r, fresh, {k: new['bindings'][k] for k in recipe['nodeBindings']})
            assert [fresh_nodes['root']['width'], fresh_nodes['root']['height']] == [1280, 1024]
            records.append({'id': scene, 'nativeRoundtrip': 'PASS', 'existingNodesAndInputProtected': 'PASS',
                            'freshAndExistingDocumentPaths': 'PASS', 'modifiedResultReopened': 'PASS',
                            'actualPngAndSvgExport': 'PASS', 'designQuality': 'NOT_TESTED', 'installedHostSync': 'NOT_TESTED'})
        return records
    finally:
        r.work = original
