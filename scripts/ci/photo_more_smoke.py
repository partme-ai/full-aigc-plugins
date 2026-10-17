"""PhotoCraft补画布/镜像/黑白及八个局部处理的像素回归；不代替真实照片效果验收。"""
import hashlib
import json
from pathlib import Path
import struct
import zlib

from craft_cli_windows import require
from photo_playbook_smoke import local_effect, rgb_pixels

SCENES = {'social-canvas-padding', 'photo-mirror-layout', 'transparent-canvas-padding',
          'black-white-selective-channel', 'background-soft-blur', 'garment-color-local',
          'white-product-local-neutral', 'sky-gradient-balance', 'corner-vignette-mask',
          'portrait-teeth-local', 'product-label-edge-sharpen', 'product-color-proof-area'}


def fixture(path):
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    rows = []
    for y in range(192):
        row = bytearray()
        for x in range(256):
            row.extend((190 + ((x // 2 + y // 2) % 2) * 20, 140 + (x % 5) * 4, 50 + (y % 7) * 3))
        rows.append(b'\0' + row)
    path.write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 256, 192, 8, 2, 0, 0, 0))
                     + chunk(b'IDAT', zlib.compress(b''.join(rows))) + chunk(b'IEND', b''))


def verify_mirror(image, baseline):
    width, height, pixels = image
    bw, bh, before = baseline
    require((width, height) == (bw, bh), 'Layer mirror changed dimensions')
    expected = b''.join(before[(y * bw + x) * 4:(y * bw + x) * 4 + 4]
                        for y in range(bh) for x in reversed(range(bw)))
    require(pixels == expected, 'Output pixels do not match a horizontal mirror')


def verify_padding(image, baseline, dx, dy, white):
    width, height, pixels = image
    bw, bh, before = baseline
    require((width, height) == (bw + dx * 2, bh + dy * 2), 'Canvas dimensions mismatch')
    for y in range(height):
        for x in range(width):
            pixel = pixels[(y * width + x) * 4:(y * width + x) * 4 + 4]
            if dx <= x < dx + bw and dy <= y < dy + bh:
                original = before[((y - dy) * bw + x - dx) * 4:((y - dy) * bw + x - dx) * 4 + 4]
                require(pixel == original, 'Canvas resize resampled or shifted original pixels')
            else:
                require(pixel == b'\xff\xff\xff\xff' if white else pixel[3] == 0,
                        'Canvas extension color or alpha mismatch')


def edge_energy(pixels, width, rect):
    x0, y0, x1, y1 = rect
    return sum(abs(pixels[(y * width + x) * 3 + c] - pixels[(y * width + x + 1) * 3 + c])
               for y in range(y0, y1) for x in range(x0, x1 - 1) for c in range(3))


def yellow_bias(pixels, width, rect):
    x0, y0, x1, y1 = rect
    return sum((pixels[(y * width + x) * 3] + pixels[(y * width + x) * 3 + 1]) / 2
               - pixels[(y * width + x) * 3 + 2] for y in range(y0, y1) for x in range(x0, x1))


def run_playbooks(r, path):
    recipes = json.loads(Path(path).read_text(encoding='utf-8'))['recipes']
    original = r.work
    work = original / 'more-photo-scenes'
    work.mkdir()
    r.work = work
    records = []
    regions = {
        'background-soft-blur': ((8, 8, 32, 32), (96, 72, 160, 120)),
        'garment-color-local': ((90, 120, 130, 150), (0, 0, 32, 32)),
        'white-product-local-neutral': ((96, 76, 144, 108), (0, 0, 32, 32)),
        'sky-gradient-balance': ((32, 8, 224, 32), (32, 128, 224, 192)),
        'corner-vignette-mask': ((0, 0, 20, 20), (112, 80, 144, 112)),
        'portrait-teeth-local': ((106, 105, 122, 110), (80, 80, 96, 96)),
        'product-label-edge-sharpen': ((90, 76, 160, 108), (0, 0, 32, 32)),
        'product-color-proof-area': ((80, 80, 144, 128), (0, 0, 32, 32)),
    }
    try:
        fixture(work / 'input.png')
        source_hash = hashlib.sha256((work / 'input.png').read_bytes()).hexdigest()
        r.run('run', 'input.png', '--cmd', 'layer.duplicate', '--params', '{}', '--out', 'baseline.pcraft')
        r.run('convert', 'baseline.pcraft', 'baseline.png')
        base_rgba = rgb_pixels(work / 'baseline.png', include_alpha=True)
        base_rgb = rgb_pixels(work / 'baseline.png')[2]
        for recipe in recipes:
            name = recipe['id']
            if name not in SCENES:
                continue
            project, png = name + '.pcraft', name + '.png'
            args = ['run', 'input.png']
            for step in recipe['steps']:
                args += ['--cmd', step['command'], '--params', json.dumps(step['params'], ensure_ascii=False)]
            r.run(*args, '--out', project)
            info = json.loads(r.run('info', project))
            r.run('convert', project, png)
            rgba = rgb_pixels(work / png, include_alpha=True)
            pixels = rgb_pixels(work / png)[2]
            require((info['width'], info['height']) == rgba[:2], 'Saved project and export dimensions differ')
            check = []
            if name == 'photo-mirror-layout':
                verify_mirror(rgba, base_rgba)
                layer = next(layer['id'] for layer in info['layers'] if layer['name'] == 'Restoration working copy')
                r.run('run', project, '--cmd', 'layer.setProps', '--params', json.dumps({'layer': layer, 'visible': False}),
                      '--out', 'mirror-hidden.pcraft')
                r.run('convert', 'mirror-hidden.pcraft', 'mirror-original.png')
                require(rgb_pixels(work / 'mirror-original.png', True) == base_rgba, 'Layer mirror also changed original layer')
                check += ['exact horizontal pixel reversal', 'hidden copy reveals unchanged original']
            elif name in {'social-canvas-padding', 'transparent-canvas-padding'}:
                white = name == 'social-canvas-padding'
                verify_padding(rgba, base_rgba, 32 if white else 16, 24 if white else 16, white)
                check += ['all original pixels centered unchanged', 'white RGBA' if white else 'transparent alpha throughout extension']
            elif name == 'black-white-selective-channel':
                require(len(info['layers']) >= 3, 'Editable black/white adjustment lost')
                require(max(max(pixels[i:i + 3]) - min(pixels[i:i + 3]) for i in range(0, len(pixels), 3)) <= 1,
                        'Black/white output has chromatic pixels')
                require(max(pixels) - min(pixels) > 10, 'Black/white output lost tonal variation')
                r.run('run', project, '--cmd', 'layer.setProps', '--params', json.dumps({'layer': info['activeLayer'], 'visible': False}),
                      '--out', 'bw-hidden.pcraft')
                r.run('convert', 'bw-hidden.pcraft', 'bw-original.png')
                require(rgb_pixels(work / 'bw-original.png', True) == base_rgba, 'Black/white adjustment destroyed original color')
                check += ['RGB channels neutral', 'adjustment off restores original color']
            else:
                target, protected = regions[name]
                require(rgba[:2] == base_rgba[:2], 'Local edit changed dimensions')
                local_effect(pixels, base_rgb, 256, target, protected)
                if name == 'background-soft-blur':
                    require(edge_energy(pixels, 256, target) < edge_energy(base_rgb, 256, target) * 0.7,
                            'Background blur did not reduce high-frequency detail')
                if name == 'product-label-edge-sharpen':
                    require(edge_energy(pixels, 256, target) > edge_energy(base_rgb, 256, target),
                            'Label sharpening did not increase local edge contrast')
                if name in {'white-product-local-neutral', 'portrait-teeth-local'}:
                    require(yellow_bias(pixels, 256, target) < yellow_bias(base_rgb, 256, target) * 0.95,
                            'Selected yellow cast was not reduced')
                check += ['target changed', 'protected region exactly unchanged']
            records.append({'id': name, 'technicalRoundtripAndPixels': 'PASS', 'checks': check,
                            'creativeAcceptance': 'NOT_TESTED', 'hostEditorSync': 'NOT_TESTED'})
        require({row['id'] for row in records} == SCENES, 'Missing extended PhotoCraft recipe')
        require(hashlib.sha256((work / 'input.png').read_bytes()).hexdigest() == source_hash, 'Source image changed')
    finally:
        r.work = original
    return records
