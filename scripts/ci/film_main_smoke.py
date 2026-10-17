"""FilmCraft main：单侧关联删除、伙伴保护与撤销；内置演示仅验证工程模型。"""
import json

TICKS = 254016000000


def clips(sequence):
    return [(kind, track['id'], item) for kind in ['video', 'audio'] for track in sequence[kind] for item in track['items']]


def verify_removed(before, after, target):
    original = clips(before)
    assert any(item['clip'] == target for _, _, item in original), 'Target absent before edit'
    expected = [(kind, track, item) for kind, track, item in original if item['clip'] != target]
    assert clips(after) == expected, 'Deletion changed linked partner or other clips'


def run_checks(r):
    original = r.work
    folder = original / 'main-linked-selection'
    folder.mkdir()
    r.work = folder
    try:
        def run(steps, source=None, output='working.fcproj', demo=False):
            args = (['--demo'] if demo else []) + (['--project', source] if source else [])
            rows = [json.loads(line) for line in r.run(*args, '--save-as', output, 'run', '-', stdin=''.join(
                json.dumps({'id': command, 'params': params}) + '\n' for command, params in steps)).splitlines() if line.strip()]
            assert len(rows) == len(steps) and all(x.get('ok') for x in rows), 'Linked-selection CLI command failed'
            return [x['result'] for x in rows]
        project = json.loads(r.run('--demo', 'inspect', 'project'))
        def movies(node):
            if node.get('type') == 'Movie':
                yield node['item']
            for child in node.get('children', []):
                yield from movies(child)
        item = next(movies(project['root']))
        run([('file.newSequence', {'name': 'Main paired test', 'video': 1, 'audio': 1, 'fps': 24}),
             ('timeline.place', {'item': item, 'frame': 0, 'duration': 2 * TICKS}),
             ('timeline.place', {'item': item, 'frame': 48, 'duration': 2 * TICKS})], output='paired.fcproj', demo=True)
        baseline = json.loads(r.run('--project', 'paired.fcproj', 'inspect', 'sequence'))
        video = baseline['video'][0]['items']
        audio = baseline['audio'][0]['items']
        assert len(video) == len(audio) == 2, 'Demo did not create two actual linked AV pairs'
        outcomes = {}
        for kind, target in [('video', video[0]['clip']), ('audio', audio[0]['clip'])]:
            partner = audio[0]['clip'] if kind == 'video' else video[0]['clip']
            selected = {'clips': [target], 'add': False, 'toggle': False}
            # 先执行旧指导的显式目标形式，证明它确实会展开关联伙伴，再撤回。
            rows = run([('timeline.select', dict(selected, linked=False)), ('sequence.inspect', {}),
                        ('edit.clear', {'clips': [target]}), ('sequence.inspect', {}),
                        ('edit.undo', {}), ('sequence.inspect', {}),
                        ('timeline.select', selected), ('sequence.inspect', {}),
                        ('timeline.select', dict(selected, linked=False)), ('sequence.inspect', {}),
                        ('edit.clear', {}), ('sequence.inspect', {}),
                        ('edit.undo', {}), ('sequence.inspect', {})], source='paired.fcproj', output=kind + '-restored.fcproj')
            assert rows[1]['selection'] == [target], 'linked:false did not isolate the target'
            legacy_ids = {item['clip'] for _, _, item in clips(rows[3])}
            assert target not in legacy_ids and partner not in legacy_ids, 'Legacy explicit-target contract differs; inspect before using this guide'
            assert clips(rows[5]) == clips(baseline), 'Undo did not restore legacy deletion'
            assert set(rows[7]['selection']) == {target, partner}, 'Local isolation changed global linked selection'
            assert rows[9]['selection'] == [target], 'Final delete selection is not precise'
            verify_removed(baseline, rows[11], target)
            assert clips(rows[13]) == clips(baseline), 'Undo failed to restore both tracks'
            run([('timeline.select', dict(selected, linked=False)), ('edit.clear', {})],
                source='paired.fcproj', output=kind + '-deleted.fcproj')
            reopened = json.loads(r.run('--project', kind + '-deleted.fcproj', 'inspect', 'sequence'))
            verify_removed(baseline, reopened, target)
            restored = json.loads(r.run('--project', kind + '-restored.fcproj', 'inspect', 'sequence'))
            assert clips(restored) == clips(baseline), 'Restored native project changed on reopen'
            outcomes[kind + 'OnlyDeletion'] = 'PASS'
        return {**outcomes, 'explicitTargetExpandsPartnerReproduced': 'PASS', 'localSelectionKeepsGlobalLinking': 'PASS',
                'partnerAndOtherClipsUnchanged': 'PASS', 'undoAndNativeReopen': 'PASS',
                'scope': 'Built-in demo project model; no real media playback or J/L-cut quality certification',
                'installedHostSync': 'NOT_TESTED'}
    finally:
        r.work = original
