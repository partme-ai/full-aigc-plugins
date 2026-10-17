"""静音间隙和有限循环的实际音频回归；不替代真实素材试听。"""
import hashlib
import json
import math
from pathlib import Path
import struct
import wave
from sound_core_smoke import pcm, close


def verify_gaps(clips):
    clips = sorted(clips, key=lambda c: c['start'])
    assert len(clips) == 2, 'Expected two retained bursts'
    for clip, start, end in zip(clips, [23521, 119521], [72960, 168960]):
        assert abs(clip['start'] - start) <= 2 and abs(clip['start'] + clip['length'] - end) <= 2, 'Silence edit moved speech or dropped boundary padding'
        assert clip['content']['Audio']['offset'] == clip['start'], 'Retained audio is no longer aligned with its original samples'


def verify_loop(clips):
    clips = sorted(clips, key=lambda c: c['start'])
    assert len(clips) == 3, 'count=3 must mean three total copies'
    assert len({c['content']['Audio']['source'] for c in clips}) == 1, 'Loop source identity changed'
    assert [(c['start'], c['length'], c['content']['Audio']['offset']) for c in clips] == [(i * 48000, 48000, 0) for i in range(3)], 'Loop has gaps, overlaps, or wrong source offsets'


def fixture(path, stereo=False, bursts=False, seconds=4):
    with wave.open(str(path), 'wb') as f:
        f.setparams((2 if stereo else 1, 2, 48000, 0, 'NONE', 'not compressed'))
        samples = []
        for i in range(48000 * seconds):
            amplitude = .2 if not bursts or 24000 <= i < 72000 or 120000 <= i < 168000 else 0
            for channel in range(2 if stereo else 1):
                samples.append(struct.pack('<h', round(32767 * amplitude * math.sin(2 * math.pi * (440 if channel == 0 else 880) * i / 48000))))
        f.writeframes(b''.join(samples))


def track_clips(session, name):
    tracks = [t for t in session['tracks'] if t['name'] == name]
    assert len(tracks) == 1, 'Ambiguous fixture track'
    track = tracks[0]
    return track, track['playlists'][track['active_playlist']]['clips']


def run_production(r, skill_root):
    original = r.work
    records = []
    try:
        for name in ['voice-silence-gaps', 'finite-audio-loop']:
            r.work = original / name
            r.work.mkdir()
            seconds = 1 if name == 'finite-audio-loop' else 4
            fixture(r.work / 'source.wav', stereo=False, bursts=name == 'voice-silence-gaps', seconds=seconds)
            source_hash = hashlib.sha256((r.work / 'source.wav').read_bytes()).hexdigest()
            def batch(steps, output=None, source=None):
                args = ['run'] + (['--in', source] if source else [])
                for command, params in steps:
                    args += ['--cmd', command + '=' + json.dumps(params, separators=(',', ':'))]
                if output:
                    args += ['--save', output]
                return r.run(*args)
            def load(path):
                return json.loads((r.work / path).read_text(encoding='utf-8'))
            def bounce(path, duration):
                return ('file.bounce_mix', {'path': path, 'format': 'wav', 'bit_depth': 24, 'start': {'seconds': 0}, 'end': {'seconds': duration}, 'normalize': False, 'dither': False})
            batch([('session.new', {'name': 'Production fixture', 'sample_rate': 48000, 'bit_depth': 24, 'template': 'blank'}),
                   ('track.new', {'name': 'Source', 'format': 'mono', 'kind': 'audio'}),
                   ('file.import_audio', {'path': 'source.wav', 'track': 'Source', 'new_tracks': False, 'at': {'seconds': 0}}),
                   ('track.new', {'name': 'Untouched', 'format': 'mono', 'kind': 'audio'}),
                   ('file.import_audio', {'path': 'source.wav', 'track': 'Untouched', 'new_tracks': False, 'at': {'seconds': 0}}),
                   ('mix.mute', {'tracks': ['Untouched'], 'value': True})], 'input.scraft')
            before = load('input.scraft')
            track, clips = track_clips(before, 'Source')
            bindings = {'source.track': track['id'], 'source.clip': clips[0]['id']}
            def resolve(value):
                if isinstance(value, str) and value.startswith('$'):
                    assert value[1:] in bindings, 'Unbound recipe ID ' + value
                    return bindings[value[1:]]
                if isinstance(value, list):
                    return [resolve(item) for item in value]
                if isinstance(value, dict):
                    return {key: resolve(item) for key, item in value.items()}
                return value
            input_hash = hashlib.sha256((r.work / 'input.scraft').read_bytes()).hexdigest()
            batch([bounce('baseline.wav', seconds)], source='input.scraft')
            recipe = json.loads((Path(skill_root) / ('soundcraft-' + name) / 'references/craft-steps.json').read_text(encoding='utf-8'))
            pending, current = [], 'input.scraft'
            for step in recipe['steps']:
                pending.append((step['command'], resolve(step['params'])))
            batch(pending, 'result.scraft', current)
            after = load('result.scraft')
            track, clips = track_clips(after, 'Source')
            assert track_clips(after, 'Untouched')[0] == track_clips(before, 'Untouched')[0], 'Non-target track changed'
            if name == 'voice-silence-gaps':
                verify_gaps(clips)
                close(pcm(r.work / 'gaps-review.wav')[2], pcm(r.work / 'baseline.wav')[2])
            else:
                verify_loop(clips)
                baseline = pcm(r.work / 'baseline.wav')[2]
                actual = pcm(r.work / 'loop-review.wav')[2]
                close(actual, [channel * 3 for channel in baseline])
                batch([('clip.unloop', {'clips': [clips[0]['id']], 'mode': 'flatten'})], 'flattened.scraft', 'result.scraft')
                _, flat = track_clips(load('flattened.scraft'), 'Source')
                verify_loop(flat)
                assert all(c['loop_id'] is None for c in flat), 'Flatten left grouped loop clips'
                batch([bounce('flattened.wav', 3)], source='flattened.scraft')
                close(pcm(r.work / 'flattened.wav')[2], actual)
                batch([('clip.unloop', {'clips': [clips[0]['id']], 'mode': 'remove'})], 'removed.scraft', 'result.scraft')
                _, removed = track_clips(load('removed.scraft'), 'Source')
                assert len(removed) == 1 and removed[0]['start'] == 0 and removed[0]['length'] == 48000, 'Remove changed the original clip'
            review = 'loop-review.wav' if name == 'finite-audio-loop' else 'gaps-review.wav'
            duration = 3 if name == 'finite-audio-loop' else 4
            batch([bounce('reopened.wav', duration)], source='result.scraft')
            close(pcm(r.work / 'reopened.wav')[2], pcm(r.work / review)[2])
            assert hashlib.sha256((r.work / 'source.wav').read_bytes()).hexdigest() == source_hash, 'Original audio changed'
            assert hashlib.sha256((r.work / 'input.scraft').read_bytes()).hexdigest() == input_hash, 'Input session changed'
            records.append({'id': name, 'nativeStructureAndSamples': 'PASS', 'sourceProtected': 'PASS', 'auditoryAcceptance': 'NOT_TESTED', 'installedHostSync': 'NOT_TESTED'})
        return records
    finally:
        r.work = original
