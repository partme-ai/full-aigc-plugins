"""执行屏幕遮罩技能原始步骤，重开核验路径和实际渲染；不代表透视追踪验收。"""
import json
from pathlib import Path

from craft_cli_windows import require
from photo_playbook_smoke import rgb_pixels


def properties(node):
    yield node
    for child in node.get('children', []):
        yield from properties(child)


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


def run_playbooks(r, path):
    recipe = json.loads(Path(path).read_text(encoding='utf-8'))
    require(recipe['id'] == 'screen-composite', 'Unsupported EffectCraft scenario')
    # 仅测试夹具创建合成与屏幕层；实际任务应使用已导入图层和当前会话。
    steps = [
        {'command': 'comp.new', 'params': {'name': 'Main', 'width': 1920, 'height': 1080,
                                         'duration': 4, 'frameRate': 25}},
        {'command': 'layer.newSolid', 'params': {'name': 'Screen', 'color': '#00ff00'}},
    ] + recipe['steps']
    args = ['run', '--empty']
    for step in steps:
        args += [step['command'], json.dumps(step['params'], ensure_ascii=False)]
    r.run(*args, '--save-as', 'screen.ecproj')
    tree = json.loads(r.run('props', 'Main', 'Screen', '--project', 'screen.ecproj', '--json'))
    verify_mask(tree['properties'])
    r.run('render-frame', '--project', 'screen.ecproj', '--comp', 'Main', '--time', '0',
          '--max-side', '480', '--out', 'screen.png')
    verify_pixels(r.work / 'screen.png')
    return [{'id': recipe['id'], 'savedMaskAndOpacity': 'PASS', 'renderedMaskLocality': 'PASS',
             'perspectiveTracking': 'NOT_TESTED', 'hostEditorSync': 'NOT_TESTED'}]
