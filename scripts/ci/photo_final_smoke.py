"""最后九条PhotoCraft配方：影调/细节和真正透明交付；只认证可控样例。"""
import hashlib
import json
from pathlib import Path
import struct
import zlib

from craft_cli_windows import require
from photo_playbook_smoke import rgb_pixels
from photo_more_smoke import edge_energy, yellow_bias

SCENES = {'yellow-paper-neutralize', 'moire-small-radius', 'bw-conversion-preserve',
          'gentle-color-noise', 'restore-final-sharpen', 'portrait-backlit',
          'product-edge-halo', 'product-dark-matte', 'product-background-mask'}


def fixture(path, name):
    alpha = name in {'product-edge-halo', 'product-dark-matte', 'product-background-mask'}
    width, height, channels = (64, 64, 4) if alpha else (256, 192, 3)
    rows = []
    for y in range(height):
        row = bytearray()
        for x in range(width):
            if name == 'product-background-mask':
                pixel = (40, 100, 180, 255) if 16 <= x < 48 and 16 <= y < 48 else (255, 255, 255, 255)
            elif alpha:
                if 20 <= x < 44 and 20 <= y < 44:
                    pixel = (40, 100, 180, 255)
                elif 16 <= x < 48 and 16 <= y < 48:
                    matte = 255 if name == 'product-edge-halo' else 0
                    pixel = tuple(round((value * 128 + matte * 127) / 255) for value in (40, 100, 180)) + (128,)
                else:
                    pixel = (0, 0, 0, 0)
            elif name == 'yellow-paper-neutralize':
                pixel = (180, 165, 120)
            elif name == 'moire-small-radius':
                tone = 150 if x < 128 else 190
                pixel = (70, 70, 70) if x % 4 == 0 and y % 4 == 0 else (tone, tone, tone)
            elif name == 'gentle-color-noise':
                sign = 1 if (x + y) % 2 else -1
                pixel = (48 + sign * 15, 48 - sign * 15, 48)
            elif name == 'restore-final-sharpen':
                value = 120 + ((x // 2 + y // 2) % 2) * 30
                pixel = (value, value, value)
            elif name == 'portrait-backlit':
                value = 40 if x < 128 else 220
                pixel = (value, value, value)
            else:
                pixel = (40 + x // 2, 100 + y // 3, 180)
            row.extend(pixel)
        rows.append(b'\0' + row)
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    path.write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 6 if channels == 4 else 2, 0, 0, 0))
                     + chunk(b'IDAT', zlib.compress(b''.join(rows))) + chunk(b'IEND', b''))


def verify_matte(before, after):
    width, height, original = before
    require(after[:2] == (width, height), 'Matte cleanup changed size')
    pixels = after[2]
    require(pixels[3::4] == original[3::4], 'Matte cleanup changed alpha contour')
    for i in range(0, len(pixels), 4):
        if original[i + 3] == 255:
            require(pixels[i:i + 3] == original[i:i + 3], 'Matte cleanup changed opaque interior')
        elif original[i + 3] == 128:
            require(max(abs(pixels[i + c] - value) for c, value in enumerate((40, 100, 180))) <= 2,
                    'Matte color was not removed from semitransparent edge')


def verify_background(image):
    width, height, pixels = image
    require((width, height) == (64, 64), 'Cutout dimensions changed')
    for y in range(height):
        for x in range(width):
            pixel = pixels[(y * width + x) * 4:(y * width + x) * 4 + 4]
            if x < 12 or x >= 52 or y < 12 or y >= 52:
                require(pixel[3] == 0, 'Original visible background survived cutout')
            if 20 <= x < 44 and 20 <= y < 44:
                require(pixel == bytes([40, 100, 180, 255]), 'Cutout removed or altered subject interior')


def resolve(value, original):
    if isinstance(value, dict):
        if set(value) == {'$ref'}:
            require(value['$ref'] == 'originalLayer', 'Unknown original layer reference')
            return original
        return {key: resolve(item, original) for key, item in value.items()}
    if isinstance(value, list):
        return [resolve(item, original) for item in value]
    return value


def chroma(pixels):
    return sum(max(pixels[i:i + 3]) - min(pixels[i:i + 3]) for i in range(0, len(pixels), 3))


def run_playbooks(r, path):
    original = r.work
    root = original / 'photo-final-scenes'
    root.mkdir()
    records = []
    try:
        for recipe in json.loads(Path(path).read_text(encoding='utf-8'))['recipes']:
            name = recipe['id']
            if name not in SCENES:
                continue
            r.work = root / name
            r.work.mkdir()
            fixture(r.work / 'input.png', name)
            source_hash = hashlib.sha256((r.work / 'input.png').read_bytes()).hexdigest()
            original_info = json.loads(r.run('info', 'input.png'))
            original_id = original_info['activeLayer']
            r.run('convert', 'input.png', 'baseline.png')
            before = rgb_pixels(r.work / 'baseline.png', True)
            before_rgb = rgb_pixels(r.work / 'baseline.png')[2]
            args = ['run', 'input.png']
            for step in recipe['steps']:
                args += ['--cmd', step['command'], '--params', json.dumps(resolve(step['params'], original_id), ensure_ascii=False)]
            r.run(*args, '--out', 'result.pcraft')
            info = json.loads(r.run('info', 'result.pcraft'))
            r.run('convert', 'result.pcraft', 'result.png')
            after = rgb_pixels(r.work / 'result.png', True)
            pixels = rgb_pixels(r.work / 'result.png')[2]
            require(before[:2] == after[:2] == (info['width'], info['height']), 'Saved image dimensions changed')
            metrics = {}
            if name in {'product-edge-halo', 'product-dark-matte'}:
                verify_matte(before, after)
            elif name == 'product-background-mask':
                verify_background(after)
                require(any(row['hasMask'] for row in info['layers'] if row['id'] != original_id), 'Editable subject mask lost')
            elif name == 'yellow-paper-neutralize':
                old, new = yellow_bias(before_rgb, 256, (0, 0, 256, 192)), yellow_bias(pixels, 256, (0, 0, 256, 192))
                require(new < old * 0.98, 'Yellow paper cast did not decrease')
                metrics = {'yellowBiasBefore': old, 'yellowBiasAfter': new}
            elif name == 'moire-small-radius':
                expected = bytes(value for _ in range(192) for x in range(256)
                                 for value in [150 if x < 128 else 190] * 3)
                old = sum(abs(a - b) for a, b in zip(before_rgb, expected))
                new = sum(abs(a - b) for a, b in zip(pixels, expected))
                require(new < old * 0.2, 'Median did not remove the controlled fine-dot pattern')
                require(pixels[(80 * 256 + 64) * 3] == 150 and pixels[(80 * 256 + 192) * 3] == 190,
                        'Median removed the coarse tonal structure')
                metrics = {'dotPatternErrorBefore': old, 'dotPatternErrorAfter': new}
            elif name == 'gentle-color-noise':
                old, new = chroma(before_rgb), chroma(pixels)
                require(new < old * 0.98, 'Synthetic color noise was not reduced')
                require(abs(sum(pixels) / len(pixels) - 48) < 2, 'Noise reduction shifted shadow brightness')
                metrics = {'chromaBefore': old, 'chromaAfter': new}
            elif name == 'restore-final-sharpen':
                old, new = edge_energy(before_rgb, 256, (16, 16, 240, 176)), edge_energy(pixels, 256, (16, 16, 240, 176))
                require(new > old, 'Final sharpening did not increase edge contrast')
                require(max(abs(a - b) for a, b in zip(before_rgb, pixels)) < 10,
                        'Final sharpening overcorrected the controlled sample')
                metrics = {'edgeBefore': old, 'edgeAfter': new}
            elif name == 'portrait-backlit':
                dark = [pixels[(y * 256 + x) * 3] for y in range(16, 176) for x in range(16, 112)]
                bright = [pixels[(y * 256 + x) * 3] for y in range(16, 176) for x in range(144, 240)]
                require(min(dark) > 40 and max(bright) < 220, 'Shadow/highlight regions did not move as intended')
                metrics = {'shadowRange': [min(dark), max(dark)], 'highlightRange': [min(bright), max(bright)]}
            else:
                require(max(max(pixels[i:i + 3]) - min(pixels[i:i + 3]) for i in range(0, len(pixels), 3)) <= 1,
                        'Black/white output retains chroma')
            # 隐藏工作/调整层并恢复原件可见性，在检查副本中证明输入未破坏。
            restore = ['run', 'result.pcraft']
            for layer in info['layers']:
                restore += ['--cmd', 'layer.setProps', '--params', json.dumps({'layer': layer['id'], 'visible': layer['id'] == original_id})]
            r.run(*restore, '--out', 'original-only.pcraft')
            r.run('convert', 'original-only.pcraft', 'original-only.png')
            require(rgb_pixels(r.work / 'original-only.png', True) == before, 'Original layer not recoverable')
            require(hashlib.sha256((r.work / 'input.png').read_bytes()).hexdigest() == source_hash, 'Input file changed')
            records.append({'id': name, 'technicalSample': 'PASS', 'metrics': metrics,
                            'originalLayerRestored': 'PASS', 'creativeAcceptance': 'NOT_TESTED', 'hostEditorSync': 'NOT_TESTED'})
        require({row['id'] for row in records} == SCENES, 'Missing final PhotoCraft recipe')
    finally:
        r.work = original
    return records
