"""LightCraft虚拟副本、命名版本与选择性曲线迁移的真实CLI回归。"""
import hashlib
import json
from pathlib import Path
from media_playbook_smoke import image_fixture
from craft_cli_windows import png_fixture
from photo_playbook_smoke import rgb_pixels
from light_core_smoke import resolve


def named_version_index(history, name):
    matches = [i for i, row in enumerate(history['versions']) if row['name'] == name]
    assert len(matches) == 1, 'Version name is missing or ambiguous; do not guess index'
    return matches[0]


def verify_curve_only(source, before, after):
    assert after['curve'] == source['curve'], 'Tone curve group was not copied'
    assert {k: v for k, v in before.items() if k != 'curve'} == {
        k: v for k, v in after.items() if k != 'curve'}, 'Copy changed a non-curve setting'


def run_versions(r, skill_root):
    original = r.work
    records = []
    try:
        for scene in ['virtual-copy-review', 'named-version-restore', 'tone-curve-transfer']:
            r.work = original / scene
            r.work.mkdir()
            image_fixture(r.work / 'sample.png')
            image_fixture(r.work / 'target.png', True)
            png_fixture(r.work / 'guard.png')
            hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in r.work.glob('*.png')}

            def run(steps, imports=()):
                args = ['run', '--library', 'library']
                for path in imports:
                    args += ['--import', path]
                rows = [json.loads(line) for line in r.run(*args, '--script', '-', stdin=''.join(
                    json.dumps({'command': c, 'params': p}) + '\n' for c, p in steps)).splitlines() if line.strip()]
                assert len(rows) == len(steps) and all(row.get('ok') is True and 'result' in row for row in rows)
                return [row['result'] for row in rows]

            photos = run([('catalog.query', {'filter': {}})], hashes)[0]['photos']
            ids = {p['fileName']: p['id'] for p in photos}
            sample, target, guard = (ids[n + '.png'] for n in ['sample', 'target', 'guard'])
            # 不同设置使误选照片或误复制全组能被真实状态比较发现。
            run([('develop.set', {'ids': [sample], 'values': {'light.exposure': .1, 'color.saturation': 8}}),
                 ('develop.set', {'ids': [target], 'values': {'light.exposure': -.3, 'color.saturation': 25, 'crop.angle': 1}}),
                 ('develop.set', {'ids': [guard], 'control': 'light.exposure', 'value': -.6}),
                 ('library.select', {'ids': [sample], 'active': sample, 'mode': 'replace'})])
            if scene == 'tone-curve-transfer':
                run([('develop.curve', {'channel': 'master', 'points': [[0, 0], [.25, .15], [.75, .85], [1, 1]]})])
            before = dict(zip(ids.values(), run([('develop.get', {'id': p}) for p in ids.values()])))
            render = lambda p, path: ('app.export', {'ids': [p], 'path': path, 'format': 'png', 'longEdge': 0, 'bitDepth': 8, 'colorSpace': 'srgb', 'metadata': 'none'})
            run([render(target if scene == 'tone-curve-transfer' else sample, 'before.png')])
            bindings = {'sample.id': sample, 'target.id': target, 'targets.photoIds': [target]}
            recipe = json.loads((Path(skill_root) / ('lightcraft-' + scene) / 'references/craft-steps.json').read_text(encoding='utf-8'))
            pending = []

            def flush():
                if not pending:
                    return
                values = run([(s['command'], resolve(s['params'], bindings)) for s in pending])
                for step, value in zip(pending, values):
                    if step.get('capture') == 'copy':
                        assert len(value['ids']) == 1
                        bindings['copy.id'] = value['ids'][0]
                    elif step.get('capture') == 'baselineVersion':
                        bindings['version.index'] = named_version_index(value, 'Review baseline')
                pending.clear()

            for step in recipe['steps']:
                pending.append(step)
                if step.get('capture'):
                    flush()
            flush()
            after = dict(zip(ids.values(), run([('develop.get', {'id': p}) for p in ids.values()])))
            assert before[guard] == after[guard], 'Non-target guard changed'
            if scene == 'virtual-copy-review':
                assert before == after, 'Virtual copy changed an existing photo'
                copy = bindings['copy.id']
                copy_state = run([('develop.get', {'id': copy})])[0]
                assert abs(copy_state['light']['exposure'] - .7) < 1e-6
                catalog = run([('catalog.query', {'filter': {}})])[0]['photos']
                row = next(x for x in catalog if x['id'] == copy)
                assert row['copyOf'] == sample and row['copyName'] == 'Review alternate' and len(catalog) == 4
                assert rgb_pixels(r.work / 'original.png') == rgb_pixels(r.work / 'before.png')
                assert rgb_pixels(r.work / 'alternate.png') != rgb_pixels(r.work / 'original.png')
                run([render(copy, 'reopened.png')])
                assert rgb_pixels(r.work / 'reopened.png') == rgb_pixels(r.work / 'alternate.png')
            elif scene == 'named-version-restore':
                assert before == after, 'Named restore did not restore exact settings'
                assert rgb_pixels(r.work / 'restored.png') == rgb_pixels(r.work / 'before.png')
                assert rgb_pixels(r.work / 'alternate.png') != rgb_pixels(r.work / 'restored.png')
                named_version_index(run([('history.list', {'id': sample})])[0], 'Review baseline')
                run([render(sample, 'reopened.png')])
                assert rgb_pixels(r.work / 'reopened.png') == rgb_pixels(r.work / 'restored.png')
            else:
                verify_curve_only(before[sample], before[target], after[target])
                assert before[sample] == after[sample], 'Source changed during transfer'
                assert rgb_pixels(r.work / 'curve-proof.png') != rgb_pixels(r.work / 'before.png')
                run([render(target, 'reopened.png')])
                assert rgb_pixels(r.work / 'reopened.png') == rgb_pixels(r.work / 'curve-proof.png')
            assert all(hashlib.sha256((r.work / p).read_bytes()).hexdigest() == value for p, value in hashes.items())
            records.append({'id': scene, 'nativeRoundtrip': 'PASS', 'settingsAndRenderedPixels': 'PASS',
                            'freshProcessReopen': 'PASS', 'originalFilesAndGuardProtected': 'PASS',
                            'realPhotoQuality': 'NOT_TESTED', 'installedHostSync': 'NOT_TESTED'})
        return records
    finally:
        r.work = original
