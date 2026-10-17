"""LightCraft六核心：明确照片ID、设置组、隐私导出及真实固定NEF样本。"""
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import quote
from craft_windows import download
from craft_cli_windows import png_fixture
from media_playbook_smoke import image_fixture
from photo_playbook_smoke import rgb_pixels
from light_core_fixtures import with_synthetic_gps, has_gps, jpeg_size


def resolve(value, bindings):
    if isinstance(value, str) and value.startswith('$'):
        assert value[1:] in bindings, 'Unbound photo/preset variable: ' + value
        return bindings[value[1:]]
    if isinstance(value, list):
        return [resolve(v, bindings) for v in value]
    if isinstance(value, dict):
        result = {k: resolve(v, bindings) for k, v in value.items()}
        if 'ids' in result:
            assert isinstance(result['ids'], list) and result['ids'] and all(type(x) is int for x in result['ids']), 'Photo IDs must be a nonempty flat integer array'
        return result
    return value


def verify_group(sample, before, after, guard_before, guard_after):
    assert after['light'] == sample['light'], 'Target did not receive full light settings group'
    assert {k: v for k, v in before.items() if k != 'light'} == {k: v for k, v in after.items() if k != 'light'}, 'Preset overwrote a non-light setting'
    assert guard_before == guard_after, 'Preset changed an unselected photo'


def run_core(r, skill_root):
    original = r.work
    records = []
    try:
        for name in ['photo-culling', 'batch-photo-style', 'portrait-develop', 'landscape-develop', 'photo-export', 'raw-develop']:
            r.work = original / ('core-' + name)
            r.work.mkdir()
            (r.work / 'output').mkdir()
            image_fixture(r.work / 'sample.png')
            image_fixture(r.work / 'target.png', True)
            png_fixture(r.work / 'guard.png')
            def run(steps, imports=(), library='library'):
                args = ['run', '--library', library]
                for p in imports:
                    args += ['--import', p]
                text = ''.join(json.dumps({'command': command, 'params': params}, ensure_ascii=False) + '\n' for command, params in steps)
                rows = [json.loads(line) for line in r.run(*args, '--script', '-', stdin=text).splitlines() if line.strip()]
                assert len(rows) == len(steps) and all('result' in x and not x.get('error') for x in rows), 'Native core command failed'
                return [x['result'] for x in rows]
            def render(id, path, size=0):
                return ('app.export', {'ids': [id], 'path': path, 'format': 'png', 'bitDepth': 8, 'longEdge': size, 'dontEnlarge': True, 'colorSpace': 'srgb', 'metadata': 'none'})
            sample_name = 'sample.png'
            imports = ['sample.png', 'target.png', 'guard.png']
            if name == 'photo-export':
                run([('app.export', {'path': 'plain.jpg', 'format': 'jpeg', 'metadata': 'none', 'longEdge': 0})], ['sample.png'], 'fixture-library')
                (r.work / 'sample-gps.jpg').write_bytes(with_synthetic_gps((r.work / 'plain.jpg').read_bytes()))
                assert has_gps((r.work / 'sample-gps.jpg').read_bytes()), 'Fixture lacks actual EXIF GPS'
                sample_name = 'sample-gps.jpg'
                imports = [sample_name, 'target.png', 'guard.png']
            elif name == 'raw-develop':
                lock = json.loads(Path(__file__).with_name('light_raw_fixture.lock.json').read_text(encoding='utf-8'))
                target = r.work / 'camera.nef'
                download(quote(lock['sourceUrl'], safe=':/?=&'), target, lock['sha256'])
                assert target.stat().st_size == lock['bytes'], 'Wrong fixed RAW fixture size'
                sample_name = 'camera.nef'
                imports = [sample_name, 'guard.png']
            sources = {p: hashlib.sha256((r.work / p).read_bytes()).hexdigest() for p in imports}
            photos = run([('catalog.query', {'filter': {}})], imports)[0]['photos']
            by_name = {p['fileName']: p for p in photos}
            sample_id = by_name[sample_name]['id']
            guard_id = by_name['guard.png']['id']
            group = [sample_id, by_name['target.png']['id']] if name in ('photo-culling', 'batch-photo-style') else [sample_id]
            bindings = {'sample.id': sample_id, 'target.id': sample_id, 'targets.photoIds': group, 'group.photoIds': group}
            seed = [('develop.set', {'control': 'light.exposure', 'value': -.7, 'ids': [guard_id]}),
                    ('photo.rate', {'rating': 2, 'ids': [guard_id]}), ('photo.flag', {'flag': 'reject', 'ids': [guard_id]})]
            if name == 'batch-photo-style':
                other = group[1]
                seed += [('develop.set', {'control': 'light.contrast', 'value': .15, 'ids': [sample_id]}),
                         ('develop.set', {'control': 'light.exposure', 'value': .8, 'ids': [other]}),
                         ('develop.set', {'control': 'color.saturation', 'value': 35, 'ids': [other]}),
                         ('develop.set', {'control': 'crop.angle', 'value': .5, 'ids': [other]})]
            seed += [('library.select', {'ids': [guard_id], 'active': guard_id, 'mode': 'replace'})]
            run(seed)
            all_ids = [p['id'] for p in photos]
            before = dict(zip(all_ids, run([('develop.get', {'id': id}) for id in all_ids])))
            guard_meta = next(p for p in run([('catalog.query', {'filter': {}})])[0]['photos'] if p['id'] == guard_id)
            if name in ('portrait-develop', 'landscape-develop', 'raw-develop', 'batch-photo-style'):
                probe_id = group[1] if name == 'batch-photo-style' else sample_id
                run([render(probe_id, 'before.png', 1600 if name == 'raw-develop' else 0)])
            if name == 'photo-export':
                run([('app.export', {'ids': [sample_id], 'path': 'keep-gps.jpg', 'format': 'jpeg', 'longEdge': 0, 'metadata': 'all', 'removeLocation': False})])
                assert has_gps((r.work / 'keep-gps.jpg').read_bytes()), 'Positive GPS-retention control failed; removal not proven'
                (r.work / 'output/web').mkdir()
                # 先由实际命名规则产生交付名，再设置同名哨兵，确保真的形成冲突。
                run([('app.export', {'ids': [sample_id], 'dir': 'output/web', 'format': 'jpeg', 'longEdge': 2000, 'dontEnlarge': True, 'metadata': 'all', 'removeLocation': False, 'conflict': 'unique'})])
                existing = list((r.work / 'output/web').iterdir())
                assert len(existing) == 1, 'Fixture export did not produce one actual delivery name'
                sentinel = existing[0]
                sentinel.write_bytes(b'KEEP EXISTING DELIVERY')
            recipe = json.loads((Path(skill_root) / ('lightcraft-' + name) / 'references/craft-steps.json').read_text(encoding='utf-8'))
            pending = []
            results = []
            def flush():
                if not pending:
                    return
                rows = run([(s['command'], resolve(s['params'], bindings)) for s in pending])
                results.extend(zip(pending[:], rows))
                for s, value in zip(pending, rows):
                    if s.get('capture') == 'preset':
                        bindings['preset.id'] = value['id']
                pending.clear()
            for step in recipe['steps']:
                if '$photo.id' in json.dumps(step['params']):
                    flush()
                    for id in group:
                        bindings['photo.id'] = id
                        results.append((step, run([(step['command'], resolve(step['params'], bindings))])[0]))
                else:
                    pending.append(step)
                    if step.get('capture'):
                        flush()
            flush()
            after = dict(zip(all_ids, run([('develop.get', {'id': id}) for id in all_ids])))
            catalog_after = {p['id']: p for p in run([('catalog.query', {'filter': {}})])[0]['photos']}
            assert before[guard_id] == after[guard_id] and guard_meta == catalog_after[guard_id], 'Unselected photo state changed'
            detail = {}
            if name == 'photo-culling':
                assert all(catalog_after[id]['rating'] == 4 and str(catalog_after[id]['flag']).lower() == 'pick' for id in group), 'Ratings/flags applied to wrong photos'
                sheet = next(v for s, v in results if s['command'] == 'export.contactSheet')
                assert sheet['photos'] == 2 and sheet['pages'] == 1, 'Contact sheet includes wrong photos'
                pdf = (r.work / 'output/selects.pdf').read_bytes()
                assert pdf.startswith(b'%PDF') and len(re.findall(rb'/Type\s*/Page\b', pdf)) == 1, 'Not a one-page contact sheet'
                detail['selectedTwoPhotosAndProtectedReject'] = 'PASS'
            elif name == 'batch-photo-style':
                verify_group(after[sample_id], before[group[1]], after[group[1]], before[guard_id], after[guard_id])
                assert abs(after[sample_id]['light']['exposure'] - .25) < 1e-6, 'Sample exposure not applied'
                run([render(group[1], 'after.png')])
                a, b = rgb_pixels(r.work / 'before.png'), rgb_pixels(r.work / 'after.png')
                assert a[:2] == b[:2] and sum(abs(x - y) for x, y in zip(a[2], b[2])) / len(a[2]) > .5, 'Target rendered image did not change'
                exported = list((r.work / 'output/batch').glob('*.jpg'))
                assert len(exported) == 2 and all(0 < jpeg_size(p.read_bytes())[0] <= 64 for p in exported), 'Batch delivery omitted or included wrong photos'
                sheet = next(v for s, v in results if s['command'] == 'export.contactSheet')
                assert sheet['photos'] == 2 and sheet['pages'] == 1 and (r.work / 'output/group-proof.pdf').read_bytes().startswith(b'%PDF'), 'Batch contact proof missing or wrong selection'
                detail['fullLightGroupOnly'] = 'PASS'
                detail['targetColorAndCropPreserved'] = 'PASS'
            elif name in ('portrait-develop', 'landscape-develop', 'raw-develop'):
                expected = {'portrait-develop': .15, 'landscape-develop': .2, 'raw-develop': .25}[name]
                assert abs(after[sample_id]['light']['exposure'] - expected) < 1e-6, 'Edited wrong photo'
                if name == 'landscape-develop':
                    assert abs(after[sample_id]['crop']['angle'] - 1) < 1e-6, 'Straightening not saved'
                run([render(sample_id, 'after.png', 1600 if name == 'raw-develop' else 0)])
                a, b = rgb_pixels(r.work / 'before.png'), rgb_pixels(r.work / 'after.png')
                assert sum(b[2]) / len(b[2]) > sum(a[2]) / len(a[2]) + .1, 'Positive exposure did not brighten rendered image'
                output = {'portrait-develop': 'portrait-proof.jpg', 'landscape-develop': 'landscape-proof.jpg', 'raw-develop': 'raw-proof.jpg'}[name]
                width, height = jpeg_size((r.work / 'output' / output).read_bytes())
                assert 0 < width <= by_name[sample_name]['width'] and 0 < height <= by_name[sample_name]['height'], 'Proof image enlarged or malformed'
                if name == 'raw-develop':
                    raw = catalog_after[sample_id]
                    assert 'D2H' in str(raw['camera']) and raw['previewOnly'] is None and raw['width'] > 2000, 'RAW identity or full-decode report not proven'
                    detail.update({'rawClassification': 'FULL_RAW_REPORTED_NIKON_D2H_ONLY', 'independentDecoderParity': 'NOT_TESTED'})
                detail['targetSettingAndRenderedExposure'] = 'PASS'
                # 以上回读来自关闭后新进程；再次导出比对持久化渲染。
                run([render(sample_id, 'reopened.png', 1600 if name == 'raw-develop' else 0)])
                assert rgb_pixels(r.work / 'reopened.png') == b, 'Library reopen changed rendered result'
            else:
                assert sentinel.read_bytes() == b'KEEP EXISTING DELIVERY', 'Unique conflict policy overwrote existing output'
                outputs = [p for p in (r.work / 'output/web').iterdir() if p != sentinel]
                assert len(outputs) == 1 and jpeg_size(outputs[0].read_bytes()) == (64, 48), 'Wrong selected count or no-enlarge geometry'
                assert not has_gps(outputs[0].read_bytes()), 'GPS coordinates survived removal'
                detail.update({'positiveGpsControlAndActualRemoval': 'PASS', 'uniqueOutputAndNoEnlarge': 'PASS'})
            assert all(hashlib.sha256((r.work / p).read_bytes()).hexdigest() == sha for p, sha in sources.items()), 'Original source file changed'
            records.append({'id': name, 'technicalRoundtrip': 'PASS', 'unselectedPhotoAndSourcesProtected': 'PASS', **detail, 'creativeVisualAcceptance': 'NOT_TESTED', 'installedHostSync': 'NOT_TESTED'})
        return records
    finally:
        r.work = original
