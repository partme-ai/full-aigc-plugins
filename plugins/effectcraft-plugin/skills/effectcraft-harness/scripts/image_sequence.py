"""逐帧核验原生 RGBA PNG 序列；所有依赖按包内路径和字节摘要绑定。"""
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import struct
import subprocess
import zlib


def rgba_facts(path):
    spec = importlib.util.spec_from_file_location('craft_sequence_png', Path(__file__).with_name('png_inspection.py'))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    facts = module.inspect_png(path)
    data = path.read_bytes()
    if data[24:29] != bytes([8, 6, 0, 0, 0]):
        raise ValueError('sequence_rgba8_required')
    compressed, at = [], 8
    while at < len(data):
        size = struct.unpack_from('>I', data, at)[0]
        if data[at+4:at+8] == b'IDAT':
            compressed.append(data[at+8:at+8+size])
        at += size+12
    # inspect_png 已约束解压尺寸及文件结构；这里还原滤波后像素以核验实际 alpha。
    decoder = zlib.decompressobj()
    scan = decoder.decompress(b''.join(compressed), (facts['width']*4+1)*facts['height']+1)
    pixels = hashlib.sha256(); minimum, maximum = 255, 0
    for row in module.rgba8_rows(scan, facts['width'], facts['height']):
        alpha=row[3::4]
        minimum=min(minimum,min(alpha));maximum=max(maximum,max(alpha))
        pixels.update(row)
    return dict(facts, alphaExtrema=[minimum, maximum], rgbaSha256=pixels.hexdigest())


def inspect_sequence(directory, composition, *, receipt=False):
    rate = Fraction(str(composition['frameRate'])); duration = Fraction(str(composition['duration']))
    count = math.ceil(rate*duration)
    if not 0 < count <= 10000 or count*composition['width']*composition['height']*4 > 512*1024*1024:
        raise ValueError('sequence_frame_budget_exceeded')
    expected = [f'frame_{index:05d}.png' for index in range(count)]
    if directory.is_symlink() or sorted(p.name for p in directory.iterdir() if not (receipt and p.name=='sequence.json')) != expected:
        raise ValueError('sequence_frame_set_mismatch')
    frames = []
    for index, name in enumerate(expected):
        path = directory/name
        if path.is_symlink() or not path.is_file():
            raise ValueError('sequence_frame_invalid')
        facts = rgba_facts(path)
        if (facts['width'], facts['height']) != (composition['width'], composition['height']):
            raise ValueError('sequence_dimensions_mismatch')
        if facts['alphaExtrema'][0] == 255:
            raise ValueError('sequence_transparency_missing')
        frames.append({'index': index, 'location': name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                       'bytes': path.stat().st_size, 'alphaExtrema': facts['alphaExtrema'], 'rgbaSha256': facts['rgbaSha256']})
    return {'schema': 'craft-image-sequence/v1', 'encoding': 'png', 'width': composition['width'], 'height': composition['height'],
            'bitDepth': 8, 'channels': 'rgba', 'alphaRepresentation': 'straight-png', 'colorSpace': 'unknown',
            'frameRate': {'num': rate.numerator, 'den': rate.denominator}, 'frameCount': count,
            'durationTicks': str(count), 'timeBase': {'num': rate.denominator, 'den': rate.numerator}, 'frames': frames}


def export_sequence(cli, project, composition, stage):
    # 输出长度有上限；即使原生支持更长序列也不允许一次请求无界耗用磁盘。
    count = math.ceil(Fraction(str(composition['frameRate']))*Fraction(str(composition['duration'])))
    if not 0 < count <= 10000 or count*composition['width']*composition['height']*4 > 512*1024*1024:
        raise ValueError('sequence_frame_budget_exceeded')
    directory = stage/'rgba-sequence'; directory.mkdir()
    args = [cli, '--project', str(project), 'render', '--comp', composition['name'], '--out', str(directory/'frame.png'),
            '--format', 'png', '--channels', 'rgba', '--start', '0', '--end', str(composition['duration']),
            '--fps', str(composition['frameRate']), '--audio', 'off']
    result = subprocess.run(args, capture_output=True, text=True, timeout=180)
    if result.returncode:
        raise ValueError('sequence_render_failed')
    manifest = inspect_sequence(directory, composition)
    (directory/'sequence.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8', newline='\n')
    return {'path': 'rgba-sequence/sequence.json', 'sha256': hashlib.sha256((directory/'sequence.json').read_bytes()).hexdigest(),
            'metadata': {k: v for k, v in manifest.items() if k != 'frames'}}
