"""独立分段生产候选；每段复用 v1 像素验收，检查点不冒充下游交付合同。"""
import argparse
from contextlib import contextmanager
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
CHUNK_BYTES = 512 * 1024 * 1024
TOTAL_DECODED_BYTES = 64 * 1024 * 1024 * 1024
TOTAL_ENCODED_BYTES = 2 * 1024 * 1024 * 1024


def module(name):
    spec = importlib.util.spec_from_file_location('craft_segment_' + name, Path(__file__).with_name(name + '.py'))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def rational(value):
    return {'num': value.numerator, 'den': value.denominator}


def plan_segments(composition, chunk_bytes=CHUNK_BYTES):
    """按帧索引切分；最终半开区间以总帧数决定，不累加浮点秒数。"""
    width, height = composition['width'], composition['height']
    if any(type(v) is not int or not 1 <= v <= 16384 for v in (width, height)):
        raise ValueError('segment_dimensions_invalid')
    if type(chunk_bytes) is not int or not 0 < chunk_bytes <= CHUNK_BYTES:
        raise ValueError('segment_budget_invalid')
    frame_bytes = width * height * 4
    if frame_bytes > chunk_bytes:
        raise ValueError('segment_single_frame_budget')
    rate, duration = Fraction(str(composition['frameRate'])), Fraction(str(composition['duration']))
    if not 1 <= rate <= 240 or duration <= 0 or rate.numerator > 2**31-1 or rate.denominator > 2**31-1:
        raise ValueError('segment_timing_invalid')
    count = math.ceil(rate * duration)
    if count > 10000 or count * frame_bytes > TOTAL_DECODED_BYTES:
        raise ValueError('segment_total_budget')
    size = chunk_bytes // frame_bytes
    return [{'firstFrame': first, 'frameCount': min(size, count-first),
             'start': rational(Fraction(first, 1)/rate),
             'end': rational(Fraction(min(first+size, count), 1)/rate)}
            for first in range(0, count, size)]


def regular_path(path):
    for item in [path, *path.parents]:
        if item.is_symlink():
            raise ValueError('segment_symlink')


def atomic_json(path, value):
    regular_path(path)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.segment-', delete=False) as stream:
        temporary = Path(stream.name)
        stream.write((json.dumps(value, sort_keys=True, indent=2)+'\n').encode())
        stream.flush()
        os.fsync(stream.fileno())
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


@contextmanager
def output_lock(root):
    # 内核锁在进程退出时释放；不通过删除锁文件抢占仍在运行的生产器。
    platform_adapter = module('platform_support')
    path = root/'render.lock'
    regular_path(path)
    with path.open('a+b') as stream:
        try:
            platform_adapter.lock_stream(stream)
        except BlockingIOError as error:
            raise ValueError('segment_render_busy') from error
        try:
            yield
        finally:
            platform_adapter.unlock_stream(stream)


def render_segment(cli, project, composition, directory, part):
    """固定 CLI 使用合成全局编号；核验完整集合后改为段内编号。"""
    seconds = lambda value: format(float(Fraction(value['num'], value['den'])), '.17g')
    rate = Fraction(str(composition['frameRate']))
    args = [str(cli), '--project', str(project), 'render', '--comp', composition['name'],
            '--out', str(directory/'frame.png'), '--format', 'png', '--channels', 'rgba',
            '--start', seconds(part['start']), '--end', seconds(part['end']),
            '--fps', format(float(rate), '.17g'), '--audio', 'off']
    result = subprocess.run(args, capture_output=True, timeout=180)
    if result.returncode:
        raise ValueError('sequence_render_failed')
    names = [f"frame_{i:05d}.png" for i in range(part['firstFrame'], part['firstFrame']+part['frameCount'])]
    if sorted(p.name for p in directory.iterdir()) != names:
        raise ValueError('segment_native_frame_range')
    for index, name in enumerate(names):
        source = directory/name
        regular_path(source)
        source.rename(directory/f'frame_{index:05d}.png')


def render_segments(cli, project, composition, output, chunk_bytes=CHUNK_BYTES, before_segment=None,before_native=None,after_native=None):
    """只有与当前输入绑定且重新通过像素核验的段允许复用。"""
    parts = plan_segments(composition, chunk_bytes)
    cli, project, output = Path(cli).absolute(), Path(project).absolute(), Path(output).absolute()
    for path in (cli, project, output):
        regular_path(path)
    binding = {'projectSha256': sha(project), 'runtimeSha256': sha(cli),
               'composition': composition, 'chunkBytes': chunk_bytes, 'parts': parts}
    if output.exists() and not (output/'checkpoint.json').is_file():
        raise ValueError('segment_output_unowned')
    output.mkdir(parents=True, exist_ok=True)
    sequence = module('image_sequence')
    with output_lock(output):
        checkpoint = output/'checkpoint.json'
        regular_path(checkpoint)
        if checkpoint.exists():
            if checkpoint.stat().st_size > 2*1024*1024 or json.loads(checkpoint.read_text(encoding='utf-8')) != binding:
                raise ValueError('segment_binding_conflict')
        else:
            atomic_json(checkpoint, binding)
        allowed = {'checkpoint.json', 'verified.json', 'render.lock', 'segments.json'} | {f'segment_{i:05d}' for i in range(len(parts))}
        if any(p.name not in allowed for p in output.iterdir()):
            raise ValueError('segment_output_unowned')
        ledger_path = output/'verified.json'
        regular_path(ledger_path)
        if ledger_path.exists() and ledger_path.stat().st_size > 2*1024*1024:
            raise ValueError('segment_checkpoint_invalid')
        ledger = json.loads(ledger_path.read_text(encoding='utf-8')) if ledger_path.exists() else {}
        if not isinstance(ledger, dict) or any(k not in {str(i) for i in range(len(parts))} or not isinstance(v, str) or len(v) != 64 for k, v in ledger.items()):
            raise ValueError('segment_checkpoint_invalid')
        completion = output/'segments.json'
        regular_path(completion)
        completion.unlink(missing_ok=True)
        records, total = [], 0
        for index, part in enumerate(parts):
            if before_segment:before_segment()
            if sha(project) != binding['projectSha256'] or sha(cli) != binding['runtimeSha256']:
                raise ValueError('segment_input_changed')
            directory = output/f'segment_{index:05d}'
            regular_path(directory)
            comp = dict(composition, duration=str(Fraction(part['frameCount'], 1)/Fraction(str(composition['frameRate']))))
            manifest = None
            if directory.exists():
                names = {'sequence.json'} | {f'frame_{i:05d}.png' for i in range(part['frameCount'])}
                if any(path.name not in names for path in directory.iterdir()):
                    raise ValueError('segment_output_unowned')
                for path in directory.rglob('*'):
                    regular_path(path)
                    if not path.is_file():
                        raise ValueError('segment_output_unowned')
                try:
                    regular_path(directory/'sequence.json')
                    if sha(directory/'sequence.json') != ledger.get(str(index)):
                        raise ValueError('segment_receipt_changed')
                    saved = json.loads((directory/'sequence.json').read_text(encoding='utf-8'))
                    # 检查器要求只有帧；验证副本不修改已完成的段。
                    with tempfile.TemporaryDirectory(prefix='effect-segment-check-') as temp:
                        copy = Path(temp)
                        for path in directory.glob('frame_*.png'):
                            shutil.copyfile(path, copy/path.name)
                        facts = sequence.inspect_sequence(copy, comp)
                    if saved == facts and sorted(p.name for p in directory.iterdir()) == sorted(['sequence.json', *[f['location'] for f in facts['frames']]]):
                        manifest = facts
                except (ValueError, OSError, KeyError):
                    pass
            if manifest is None:
                with tempfile.TemporaryDirectory(dir=output.parent, prefix='.effect-segment-') as temp:
                    stage = Path(temp)
                    if before_native:before_native(stage,directory,part,composition)
                    try:
                        render_segment(cli, project, composition, stage, part)
                        manifest = sequence.inspect_sequence(stage, comp)
                        atomic_json(stage/'sequence.json', manifest)
                        if directory.exists():
                            shutil.rmtree(directory)
                        stage.rename(directory)
                    finally:
                        if after_native:after_native(stage)
                ledger[str(index)] = sha(directory/'sequence.json')
                atomic_json(ledger_path, ledger)
            total += sum(frame['bytes'] for frame in manifest['frames'])
            if total > TOTAL_ENCODED_BYTES:
                raise ValueError('segment_encoded_budget')
            records.append(dict(part, location=f'{directory.name}/sequence.json', sha256=sha(directory/'sequence.json')))
        if sha(project) != binding['projectSha256'] or sha(cli) != binding['runtimeSha256']:
            raise ValueError('segment_input_changed')
        result = {'schema': 'craft-segmented-render-checkpoint/v1', 'state': 'verified',
                  'binding': binding, 'frameCount': sum(p['frameCount'] for p in parts),
                  'frameRate': rational(Fraction(str(composition['frameRate']))), 'segments': records}
        atomic_json(output/'segments.json', result)
        return result


def main():
    # 固定重定向输出编码，Windows默认代码页也能返回中文帮助和回执。
    import sys
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,"reconfigure"):stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--composition', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--chunk-frames', type=int, help='可缩小每段帧数；不能提高固定资源上限')
    parser.add_argument('--runtime-home', default=os.environ.get('CRAFT_RUNTIME_HOME', str(Path.home()/'.local/share/craft-runtimes')))
    args = parser.parse_args()
    try:
        composition = json.loads(args.composition.read_text(encoding='utf-8'))
        plan_segments(composition)
        chunk_bytes = CHUNK_BYTES
        if args.chunk_frames is not None:
            if not 1 <= args.chunk_frames <= 10000:
                raise ValueError('segment_budget_invalid')
            chunk_bytes = min(CHUNK_BYTES, args.chunk_frames*composition['width']*composition['height']*4)
        installed = module('bootstrap').install(json.loads(Path(__file__).with_name('runtime.lock.json').read_text(encoding='utf-8')), args.runtime_home)
        result = render_segments(installed['executable'], args.project, composition, args.output, chunk_bytes)
        print(json.dumps({'state': result['state'], 'frameCount': result['frameCount'], 'segments': len(result['segments'])}))
        return 0
    except (ValueError, OSError, KeyError, subprocess.SubprocessError) as error:
        print(json.dumps({'error': str(error), 'state': 'failed'}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
