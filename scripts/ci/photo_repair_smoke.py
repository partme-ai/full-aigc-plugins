"""已知干净底图加可控损伤，检查修复误差和保护区域；不代替真实照片修复质量。"""
import hashlib
import json
from pathlib import Path
import struct
import zlib

from craft_cli_windows import require
from photo_playbook_smoke import rgb_pixels

CASES = {
    'scan-dust-specks': ([(40, 30), (44, 32)], (32, 22, 52, 40), 255, 0.25),
    'torn-corner-texture': ([(80, 40), (84, 42)], (72, 32, 92, 50), 20, 0.25),
    'silver-mirror-local': ([(80, 40), (84, 42)], (72, 32, 92, 50), 235, 0.25),
    'small-stain-sampled': ([(80, 40), (84, 42)], (72, 32, 92, 50), 30, 0.25),
    'portrait-eye-shadow': ([(100, 72), (104, 72)], (94, 66, 110, 78), 40, 0.02),
    'product-surface-dust': ([(40, 30), (44, 32), (80, 40), (84, 42)], (32, 22, 92, 50), 245, 0.25),
    'scratch-edge-protection': ([(40, y) for y in range(40, 61)], (27, 28, 54, 72), 245, 0.25),
    'large-stain-patch': ([(x, y) for y in range(72, 92) for x in range(96, 120)], (88, 64, 128, 100), 30, 0.25),
    'skin-shine-burn': ([(112, 60), (116, 64)], (102, 50, 126, 74), 225, 0.01),
    'hair-stray-cleanup': ([(168, 40), (169, 41), (170, 42), (171, 43), (172, 44)], (162, 34, 178, 50), 20, 0.25),
    'product-reflection-spot': ([(156, 88)], (148, 80, 164, 96), 225, 0.02),
}


def clean_pixels():
    return bytes(value for _ in range(192) for x in range(256)
                 for value in (140 + (x % 4) * 2, 115 + (x % 4) * 2, 90 + (x % 4) * 2))


def write_png(path, pixels):
    def chunk(kind, data):
        return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
    rows = b''.join(b'\0' + pixels[y * 768:(y + 1) * 768] for y in range(192))
    path.write_bytes(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 256, 192, 8, 2, 0, 0, 0))
                     + chunk(b'IDAT', zlib.compress(rows)) + chunk(b'IEND', b''))


def verify_repair(before, after, clean, width, damaged, bounds, minimum_gain):
    require(len(before) == len(after) == len(clean), 'Repair changed dimensions')
    def error(pixels):
        return sum(abs(pixels[(y * width + x) * 3 + channel] - clean[(y * width + x) * 3 + channel])
                   for x, y in damaged for channel in range(3))
    old, new = error(before), error(after)
    require(old > 100, 'Repair fixture does not contain damage')
    require(new < old * (1 - minimum_gain), 'Known damage did not improve sufficiently')
    x0, y0, x1, y1 = bounds
    for i in range(len(before) // 3):
        x, y = i % width, i // width
        if not (x0 <= x < x1 and y0 <= y < y1):
            require(before[i * 3:i * 3 + 3] == after[i * 3:i * 3 + 3], 'Repair changed protected pixels')
    return {'beforeError': old, 'afterError': new, 'minimumGain': minimum_gain,
            'measuredGain': 1 - new / old, 'protectedOutside': list(bounds)}


def run_playbooks(r, path):
    recipes = json.loads(Path(path).read_text(encoding='utf-8'))['recipes']
    original = r.work
    root = original / 'photo-repair-scenes'
    root.mkdir()
    r.work = root
    records = []
    try:
        pristine = clean_pixels()
        write_png(root / 'clean.png', pristine)
        r.run('run', 'clean.png', '--cmd', 'layer.duplicate', '--params', '{}', '--out', 'clean.pcraft')
        r.run('convert', 'clean.pcraft', 'clean-reference.png')
        clean = rgb_pixels(root / 'clean-reference.png')[2]
        for recipe in recipes:
            name = recipe['id']
            if name not in CASES:
                continue
            damaged, bounds, intensity, minimum_gain = CASES[name]
            r.work = root / name
            r.work.mkdir()
            pixels = bytearray(pristine)
            for x, y in damaged:
                pixels[(y * 256 + x) * 3:(y * 256 + x) * 3 + 3] = bytes([intensity] * 3)
            write_png(r.work / 'input.png', bytes(pixels))
            digest = hashlib.sha256((r.work / 'input.png').read_bytes()).hexdigest()
            args = ['run', 'input.png']
            for step in recipe['steps']:
                args += ['--cmd', step['command'], '--params', json.dumps(step['params'], ensure_ascii=False)]
            r.run(*args, '--out', 'repaired.pcraft')
            info = json.loads(r.run('info', 'repaired.pcraft'))
            require((info['width'], info['height']) == (256, 192) and len(info['layers']) >= 2,
                    'Repair layers or dimensions not saved')
            r.run('convert', 'repaired.pcraft', 'repaired.png')
            metrics = verify_repair(bytes(pixels), rgb_pixels(r.work / 'repaired.png')[2], clean,
                                    256, damaged, bounds, minimum_gain)
            if name == 'large-stain-patch':
                after = rgb_pixels(r.work / 'repaired.png')[2]
                ring = [(x, y) for x, y in damaged if x in (96, 119) or y in (72, 91)]
                seam = max(abs(after[(y * 256 + x) * 3 + c] - clean[(y * 256 + x) * 3 + c])
                           for x, y in ring for c in range(3))
                require(seam <= 2, 'Patch seam remains darker than the clean surrounding texture')
                metrics['seamMaxChannelError'] = seam
            layer = next(row['id'] for row in info['layers'] if row['name'] == recipe['steps'][0]['params']['name'])
            r.run('run', 'repaired.pcraft', '--cmd', 'layer.setProps',
                  '--params', json.dumps({'layer': layer, 'visible': False}), '--out', 'original.pcraft')
            r.run('convert', 'original.pcraft', 'original.png')
            require(rgb_pixels(r.work / 'original.png')[2] == bytes(pixels),
                    'Repair did not preserve original damaged layer')
            require(hashlib.sha256((r.work / 'input.png').read_bytes()).hexdigest() == digest, 'Original file changed')
            records.append({'id': name, 'syntheticRepair': 'PASS', 'metrics': metrics,
                            'creativeAcceptance': 'NOT_TESTED', 'hostEditorSync': 'NOT_TESTED'})
        require({row['id'] for row in records} == set(CASES), 'Missing repair scenario')
    finally:
        r.work = original
    return records
