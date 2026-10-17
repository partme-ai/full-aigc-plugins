"""真实FilmCraft CLI剪辑回归；合成无声AVI不代替采访语义、音质或宿主验收。"""
import json
from pathlib import Path
import struct

from craft_cli_windows import require
from photo_playbook_smoke import rgb_pixels

TICKS = 254016000000


def avi_fixture(path, fps=25, warm=False):
    """纯stdlib生成4秒实际无压缩AVI，避免测试夹具依赖全局FFmpeg。"""
    def chunk(tag, data):
        return tag + struct.pack('<I', len(data)) + data + (b'\0' if len(data) % 2 else b'')
    def listing(tag, data):
        return chunk(b'LIST', tag + data)
    width, height, frames = 64, 48, fps * 4
    size = width * height * 3
    avih = struct.pack('<14I', round(1e6 / fps), size * fps, 0, 16, frames, 0, 1, size, width, height, 0, 0, 0, 0)
    strh = struct.pack('<4s4sIHHIIIIIIIIhhhh', b'vids', b'DIB ', 0, 0, 0, 0, 1, fps, 0, frames,
                       size, 0xffffffff, 0, 0, 0, width, height)
    strf = struct.pack('<IiiHHIIiiII', 40, width, height, 1, 24, 0, size, 0, 0, 0, 0)
    header = listing(b'hdrl', chunk(b'avih', avih) + listing(b'strl', chunk(b'strh', strh) + chunk(b'strf', strf)))
    image = b''.join(bytes((60 if warm else 100, 50 + y * 3, min(255, 50 + x * 2 + (40 if warm else 0))))
                     for y in reversed(range(height)) for x in range(width))
    body, index, offset = bytearray(), bytearray(), 4
    for _ in range(frames):
        encoded = chunk(b'00db', image)
        body.extend(encoded)
        index.extend(struct.pack('<4sIII', b'00db', 16, offset, len(image)))
        offset += len(encoded)
    data = b'AVI ' + header + listing(b'movi', bytes(body)) + chunk(b'idx1', bytes(index))
    path.write_bytes(b'RIFF' + struct.pack('<I', len(data)) + data)


def resolve(value, captures):
    if isinstance(value, dict):
        if set(value) == {'$ref'}:
            current = captures
            for part in value['$ref'].split('.'):
                current = current[int(part)] if isinstance(current, list) else current[part]
            return current
        return {key: resolve(item, captures) for key, item in value.items()}
    if isinstance(value, list):
        return [resolve(item, captures) for item in value]
    return value


def verify_trim(clips, target):
    require(len(clips) == 1 and clips[0]['clip'] == target, 'Trim edited the wrong clip')
    require((clips[0]['startFrame'], clips[0]['endFrame'], clips[0]['durationFrames']) == (0, 95, 95),
            'Five-frame out trim was not saved')


def verify_razor(clips):
    clips = sorted(clips, key=lambda clip: clip['startFrame'])
    require(len(clips) == 2, 'Razor did not create two clips')
    require([(clip['startFrame'], clip['endFrame']) for clip in clips] == [(0, 90), (90, 120)],
            'Razor clips are not contiguous at frame90 or do not preserve total duration')


def verify_subtitles(text):
    require('00:00:01,000 --> 00:00:04,000' in text, 'SRT timing changed')
    require(text.count('经过校对的实际台词') == 1, 'SRT caption text lost or duplicated')


def verify_match(before, after, reference):
    require(len(before) == len(after) == len(reference), 'Color match dimensions changed')
    old_error = sum(abs(a - b) for a, b in zip(before, reference))
    new_error = sum(abs(a - b) for a, b in zip(after, reference))
    require(old_error > 1000 and new_error < old_error * 0.5, 'Color match did not approach the reference')


def native_batch(r, steps, project=None):
    args = (['--project', project] if project else []) + ['--save-as', 'scene.fcproj', 'run', '-']
    output = r.run(*args, stdin=''.join(json.dumps({'id': step['command'], 'params': step['params']},
                                               ensure_ascii=False) + '\n' for step in steps))
    rows = [json.loads(line) for line in output.splitlines() if line.strip()]
    require(len(rows) == len(steps) and all(row.get('ok') for row in rows), 'CLI batch result count or status mismatch')
    return rows


def run_recipe(r, recipe):
    name = recipe['id']
    (r.work / 'input').mkdir()
    (r.work / 'output').mkdir()
    fps = 30 if name == 'short-video' else 25
    avi_fixture(r.work / 'input/product.avi', fps)
    probe = json.loads(r.run('probe', 'input/product.avi'))
    require(probe['kind'] == 'Movie' and probe['duration'] == 4 * TICKS, 'AVI fixture is not a four-second movie')
    captures, project = {}, None
    if name not in {'short-video', 'product-video'}:
        # 后四项要求已存在的真实时间线；夹具只搭建该前置，不替代技能操作。
        imported = native_batch(r, [{'command': 'file.import', 'params': {'paths': ['input/product.avi']}}])
        item = imported[0]['result']['items'][0]
        initial = [
            {'command': 'file.newSequence', 'params': {'name': 'Main', 'width': 320, 'height': 180, 'fps': 25}},
            {'command': 'source.open', 'params': {'item': item}},
            {'command': 'markers.markIn', 'params': {'target': 'source', 'frame': 0}},
            {'command': 'markers.markOut', 'params': {'target': 'source', 'frame': 99}},
            {'command': 'source.insert', 'params': {}},
        ]
        rows = native_batch(r, initial, 'scene.fcproj')
        captures['clip'] = rows[-1]['result']['clips'][0]
        project = 'scene.fcproj'
        if name == 'color-match':
            avi_fixture(r.work / 'input/warm.avi', warm=True)
            rows = native_batch(r, [{'command': 'file.import', 'params': {'paths': ['input/warm.avi']}}], project)
            second = rows[0]['result']['items'][0]
            rows = native_batch(r, [
                {'command': 'source.open', 'params': {'item': second}},
                {'command': 'markers.markIn', 'params': {'target': 'source', 'frame': 0}},
                {'command': 'markers.markOut', 'params': {'target': 'source', 'frame': 99}},
                {'command': 'source.insert', 'params': {}},
            ], project)
            captures['clip'] = rows[-1]['result']['clips'][0]
            r.run('--project', project, 'render', '--seconds', '5', '--out', 'before.png')
    # 按显式batch读取真实返回值，再生成下一批原生JSONL，不把引用记号发给引擎。
    groups = []
    for step in recipe['steps']:
        batch = step.get('batch', 'main')
        if not groups or groups[-1][0] != batch:
            groups.append((batch, []))
        groups[-1][1].append(step)
    for _, group in groups:
        steps = [{'command': step['command'], 'params': resolve(step['params'], captures)} for step in group]
        for step in steps:
            if step['command'] == 'file.import':
                step['params']['paths'] = ['input/product.avi']
        rows = native_batch(r, steps, project)
        for template, row in zip(group, rows):
            if template.get('capture'):
                captures[template['capture']] = row['result']
        project = 'scene.fcproj'
    sequence = json.loads(r.run('--project', project, 'inspect', 'sequence'))
    clips = [clip for track in sequence['video'] for clip in track['items']]
    if name == 'interview-edit':
        verify_trim(clips, captures['clip'])
        require(any(marker['name'] == '议题起点' for marker in sequence['markers']), 'Interview marker was not saved')
    elif name == 'short-video':
        verify_razor(clips)
    elif name == 'product-video':
        require(len(clips) == 1 and clips[0]['durationFrames'] == 100, 'Product source range or insertion changed')
        require(sequence['settings']['width'] == 1920 and sequence['settings']['height'] == 1080, 'Product dimensions changed')
    elif name == 'subtitle-delivery':
        verify_subtitles((r.work / 'output/captions.srt').read_text(encoding='utf-8-sig'))
        track = json.loads(r.run('--project', project, 'exec', 'captions.list'))['tracks'][0]
        require(track['captions'][0]['start'] == TICKS and track['captions'][0]['end'] == 4 * TICKS,
                'Reopened subtitle timing changed')
    elif name == 'video-export':
        output = json.loads(r.run('probe', 'output/review.mp4'))
        require(output['kind'] == 'Movie' and output['duration'] == 4 * TICKS, 'Exported video duration mismatch')
        require((output['video']['width'], output['video']['height']) == (320, 180), 'Encoded dimensions mismatch')
        require(output['video']['frame_rate'] == {'num': 25, 'den': 1} and 'H.264' in output['video']['codec'],
                'Encoded frame rate or video codec mismatch')
        rows = json.loads(r.run('--project', project, 'exec', 'export.queue.list'))['items']
        # 队列是否持久化不作为视频成功依据；实际编码文件另由probe与解码检查。
        captures['queueItemsAfterReopen'] = len(rows)
        imported = native_batch(r, [{'command': 'file.import', 'params': {'paths': ['output/review.mp4']}}])
        item = imported[0]['result']['items'][0]
        native_batch(r, [
            {'command': 'file.newSequence', 'params': {'name': 'Decoded', 'width': 320, 'height': 180, 'fps': 25}},
            {'command': 'source.open', 'params': {'item': item}},
            {'command': 'source.insert', 'params': {}},
        ], 'scene.fcproj')
        project = 'scene.fcproj'
        for time in [0.04, 2, 3.96]:
            file = f'decoded-{time}.png'
            r.run('--project', project, 'render', '--seconds', str(time), '--out', file)
            require(sum(rgb_pixels(r.work / file)[2]) > 1000, 'Encoded start/middle/end frame did not decode')
    elif name == 'color-match':
        color = sequence['settings']['color']
        require(color['working'] == 'Rec709' and color['auto_tone_map'] is False, 'Sequence color settings not saved')
        r.run('--project', project, 'render', '--seconds', '5', '--out', 'after.png')
        r.run('--project', project, 'render', '--seconds', '1', '--out', 'reference.png')
        before = rgb_pixels(r.work / 'before.png')[2]
        after = rgb_pixels(r.work / 'after.png')[2]
        verify_match(before, after, rgb_pixels(r.work / 'reference.png')[2])
    else:
        raise ValueError('Unsupported FilmCraft scenario ' + name)
    if name != 'color-match':
        r.run('--project', project, 'render', '--seconds', '1', '--scale', '0.25' if name in {'product-video', 'short-video'} else '1',
              '--out', 'preview.png')
        pixels = rgb_pixels(r.work / 'preview.png')[2]
        require(sum(pixels) > 1000, 'Rendered preview is blank or offline placeholder')
        if name in {'short-video', 'product-video'}:
            width, height, pixels = rgb_pixels(r.work / 'preview.png')
            occupied = [(i // 3) % width for i in range(0, len(pixels), 3) if any(pixels[i:i + 3])]
            expected = width if name == 'short-video' else height * 4 / 3
            require(abs(max(occupied) - min(occupied) + 1 - expected) <= 2, 'Fit-to-frame did not resize the source')
    return {'id': name, 'savedStructureAndMedia': 'PASS', 'hostEditorSync': 'NOT_TESTED',
            'scope': 'synthetic silent AVI; no interview semantics, audio sync or real footage grade acceptance'}


def run_playbooks(r, path):
    files = sorted(Path(path).glob('filmcraft-*/references/craft-steps.json'))
    require(len(files) == 6, 'Expected six FilmCraft skill recipes')
    records, original = [], r.work
    try:
        for file in files:
            recipe = json.loads(file.read_text(encoding='utf-8'))
            r.work = original / recipe['id']
            r.work.mkdir()
            records.append(run_recipe(r, recipe))
    finally:
        r.work = original
    return records
