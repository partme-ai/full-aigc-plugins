"""执行六个动效技能原始步骤，核对工程、时间采样及PNG序列；不代替宿主验收。"""
import json
from pathlib import Path

from craft_cli_windows import require
from photo_playbook_smoke import rgb_pixels


def properties(node):
    yield node
    for child in node.get('children', []):
        yield from properties(child)


def property_value(tree, path):
    return next(row['value'] for row in properties(tree) if row.get('path') == path)


def verify_fade(alpha_sums):
    first, middle, full, held = alpha_sums
    require(first == 0, 'Fade first frame should be transparent')
    require(full > 1000, 'Text did not render at full opacity')
    require(abs(middle / full - 0.5) < 0.04, 'Fade halfway opacity was not rendered')
    require(held == full, 'Text hold changed before composition end')


def verify_loop(centers):
    require(all(center is not None for center in centers), 'Loop rendered an empty frame')
    first, middle, last = centers
    require(abs(first[0] - 200 * 480 / 1080) < 2, 'Loop start position mismatch')
    require(abs(middle[0] - 880 * 480 / 1080) < 2, 'Loop midpoint did not move')
    require(0 < last[0] - first[0] < 10, 'Last valid frame did not approach start')
    require(all(abs(center[1] - 240) < 2 for center in centers), 'Loop vertical drift')


def verify_texts(layers):
    require(set(layers) == {'Name', 'Role'}, 'Lower thirds lost or added text layers')
    for name, text, y in [('Name', '真实姓名', 880), ('Role', '真实职位', 940)]:
        require(layers[name]['text'] == text, 'Lower thirds text assigned to wrong layer')
        require(layers[name]['position'] == [180, y, 0], 'Lower thirds position changed')


def alpha_metrics(image):
    width, height, pixels = rgb_pixels(image, include_alpha=True)
    total = xsum = ysum = 0
    for i, alpha in enumerate(pixels[3::4]):
        total += alpha
        xsum += (i % width) * alpha
        ysum += (i // width) * alpha
    return total, (xsum / total, ysum / total) if total else None


def verify_mask(tree):
    rows = list(properties(tree))
    masks = [row for row in rows if row.get('type') == 'path']
    require(len(masks) == 1, 'Expected one saved mask path')
    path = masks[0]['value']['v']
    require(path['closed'] is True, 'Mask path is not closed')
    require(path['vertices'] == [[100, 100], [700, 100], [700, 450], [100, 450]],
            'Mask coordinates changed after reopen')
    require(next(row['value'] for row in rows if row.get('path') == 'transform/opacity') == 90,
            'Layer opacity was not saved')


def verify_pixels(image):
    width, height, pixels = rgb_pixels(image)
    require((width, height) == (480, 270), 'Preview dimensions changed')
    def pixel(x, y):
        return tuple(pixels[(y * width + x) * 3:(y * width + x) * 3 + 3])
    require(pixel(50, 50)[1] > 200, 'Mask interior did not render')
    require(pixel(5, 5) == (0, 0, 0) and pixel(200, 150) == (0, 0, 0),
            'Mask leaked into protected exterior')
    _, _, rgba = rgb_pixels(image, include_alpha=True)
    require(228 <= rgba[(50 * width + 50) * 4 + 3] <= 230, 'Rendered mask opacity mismatch')
    require(rgba[(5 * width + 5) * 4 + 3] == 0, 'Mask exterior is not transparent')


def run_recipe(r, recipe):
    name = recipe['id']
    # 仅合成/导出夹具需要已有工程；其他四项直接执行技能中的新工程步骤。
    fixture = [
        {'command': 'comp.new', 'params': {'name': 'Main', 'width': 1920, 'height': 1080,
                                         'duration': 4, 'frameRate': 25}},
        {'command': 'layer.newSolid', 'params': {'name': 'Screen', 'color': '#00ff00'}},
    ] if name in {'screen-composite', 'motion-export'} else []
    steps = fixture + recipe['steps']
    (r.work / 'output').mkdir()
    args = ['run', '--empty']
    for step in steps:
        args += [step['command'], json.dumps(step['params'], ensure_ascii=False)]
    r.run(*args, '--save-as', 'scene.ecproj')
    info = json.loads(r.run('info', '--project', 'scene.ecproj', '--json'))['activeComp']
    initial = next(step['params'] for step in steps if step['command'] == 'comp.new')
    for field in ['name', 'width', 'height', 'duration', 'frameRate']:
        require(info[field] == initial[field], 'Saved composition changed ' + field)
    def props(layer):
        return json.loads(r.run('props', info['name'], layer, '--project', 'scene.ecproj', '--json'))['properties']
    def render(time):
        file = f'frame-{time}.png'
        r.run('render-frame', '--project', 'scene.ecproj', '--comp', info['name'], '--time', str(time),
              '--max-side', '480', '--out', file, '--transparent')
        return r.work / file
    if name == 'screen-composite':
        verify_mask(props('Screen'))
        verify_pixels(render(0))
    elif name in {'kinetic-type', 'logo-reveal'}:
        layer, end = ('Phrase', 0.5) if name == 'kinetic-type' else ('LogoTitle', 1)
        expected_text = '准确的短文案' if name == 'kinetic-type' else '品牌名称'
        require(property_value(props(layer), 'text/sourceText') == expected_text, 'Saved text changed')
        for time, expected in [(0, 0), (end / 2, 50), (end, 100)]:
            value = json.loads(r.run('get', info['name'], layer, 'transform/opacity', '--time', str(time),
                                     '--project', 'scene.ecproj', '--json'))['value']
            require(abs(value - expected) < 0.001, 'Saved opacity keyframes did not interpolate')
        verify_fade([alpha_metrics(render(t))[0] for t in [0, end / 2, end, info['duration'] - 0.5]])
    elif name == 'lower-thirds':
        layers = {row['name']: {'text': property_value(props(row['name']), 'text/sourceText'),
                               'position': property_value(props(row['name']), 'transform/position')}
                  for row in info['layers']}
        verify_texts(layers)
        image = render(0)
        width, height, rgba = rgb_pixels(image, include_alpha=True)
        # 姓名和职位应落在两个独立的纵向带内；存在所有文本仍不能替代正确分配。
        for top, bottom in [(218, 231), (234, 246)]:
            require(sum(rgba[(top * width) * 4 + 3:(bottom * width) * 4:4]) > 1000,
                    'Lower thirds rendered text missing from intended vertical band')
    elif name == 'social-loop':
        for time, expected in [(0, [200, 540, 0]), (1.5, [880, 540, 0]), (3, [200, 540, 0])]:
            value = json.loads(r.run('get', 'Loop', 'Dot', 'transform/position', '--time', str(time),
                                     '--project', 'scene.ecproj', '--json'))['value']
            require(value == expected, 'Loop saved keyframe position changed')
        verify_loop([alpha_metrics(render(t))[1] for t in [0, 1.5, 3 - 1 / 30]])
    elif name == 'motion-export':
        copy = r.work / 'output/motion.ecproj'
        saved = json.loads(r.run('info', '--project', str(copy), '--json'))['activeComp']
        require(saved['workArea'] == [0, 3] and saved['frameRate'] == 25, 'Saved export timing changed')
        for step in recipe['cliExport']:
            r.run(*step['argv'])
        frames = sorted((r.work / 'output').glob('motion-frames_*.png'))
        require(len(frames) == 75, 'Export frame count should equal 3 seconds at 25 fps')
        for frame in frames:
            width, height, rgba = rgb_pixels(frame, include_alpha=True)
            require((width, height) == (480, 270), 'Export resolution mismatch')
            require(all(value == 255 for value in rgba[3::4]), 'Solid export alpha lost')
            require(all(rgba[i:i + 3] == b'\0\xff\0' for i in range(0, len(rgba), 4)),
                    'Exported frame content changed')
    else:
        raise ValueError('Unsupported EffectCraft scenario ' + name)
    return {'id': name, 'technicalRoundtripAndRender': 'PASS', 'hostEditorSync': 'NOT_TESTED',
            'scope': 'synthetic scene; real footage, brand artwork and playback quality not inferred'}


def run_playbooks(r, path):
    path = Path(path)
    files = sorted(path.glob('effectcraft-*/references/craft-steps.json')) if path.is_dir() else [path]
    if path.is_dir():
        require({json.loads(file.read_text(encoding='utf-8'))['id'] for file in files} == {
            'screen-composite', 'kinetic-type', 'logo-reveal', 'lower-thirds', 'social-loop', 'motion-export'},
            'Expected all six EffectCraft skill recipes')
    original_work = r.work
    records = []
    try:
        for file in files:
            recipe = json.loads(file.read_text(encoding='utf-8'))
            r.work = original_work / recipe['id']
            r.work.mkdir()
            records.append(run_recipe(r, recipe))
    finally:
        r.work = original_work
    return records
