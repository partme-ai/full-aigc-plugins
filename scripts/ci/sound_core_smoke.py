"""SoundCraft核心配音、分段增益及母版交付；信号核查不替代真实人声试听。"""
import hashlib
import json
import math
from pathlib import Path
import struct
import wave


def pcm(path):
    with wave.open(str(path), 'rb') as f:
        width, channels, rate, n = f.getsampwidth(), f.getnchannels(), f.getframerate(), f.getnframes()
        assert width in (2, 3), 'Expected integer PCM, not float or compressed audio'
        raw = f.readframes(n)
    values = [int.from_bytes(raw[i:i + width], 'little', signed=True) / 2 ** (8 * width - 1) for i in range(0, len(raw), width)]
    return rate, width, [values[c::channels] for c in range(channels)]


def close(actual, expected):
    assert len(actual) == len(expected) and all(len(a) == len(b) for a, b in zip(actual, expected)), 'Audio geometry changed'
    assert max(sum(abs(x - y) for x, y in zip(a, b)) / len(a) for a, b in zip(actual, expected)) < .00008, 'Rendered samples differ from intended track/segment processing'


def verify_voice_mix(actual, voice, bed):
    close(actual, [[a + b * 10 ** (-18 / 20) for a, b in zip(v, m)] for v, m in zip(voice, bed)])


def verify_dialogue(actual, baseline):
    close(actual, [[v * 10 ** ((6 if i < len(c) // 2 else 0) / 20) * 10 ** (-3 / 20) for i, v in enumerate(c)] for c in baseline])


def fixture(path, frequency=440, segmented=False):
    with wave.open(str(path), 'wb') as f:
        f.setparams((1, 2, 48000, 192000, 'NONE', 'not compressed'))
        f.writeframes(b''.join(struct.pack('<h', round(32767 * (.12 if not segmented or i < 96000 else .24) * math.sin(2 * math.pi * frequency * i / 48000))) for i in range(192000)))


def run_core(r, skill_root):
    original = r.work
    records = []
    for name in ['voice-over-mix', 'dialogue-leveling', 'audio-delivery']:
        r.work = original / ('core-' + name)
        r.work.mkdir()
        (r.work / 'output').mkdir()
        fixture(r.work / 'voice.wav', 440, name == 'dialogue-leveling')
        fixture(r.work / 'bed.wav', 997)
        hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in r.work.glob('*.wav')}
        def run(steps, save=None, source=None):
            args = ['run'] + (['--in', source] if source else [])
            for command, params in steps:
                args += ['--cmd', command + '=' + json.dumps(params, ensure_ascii=False, separators=(',', ':'))]
            if save:
                args += ['--save', save]
            return r.run(*args)
        def bounce(path):
            return ('file.bounce_mix', {'path': path, 'format': 'wav', 'bit_depth': 24, 'start': {'seconds': 0}, 'end': {'seconds': 4}, 'normalize': False, 'dither': False})
        init = [('session.new', {'name': 'Core work copy', 'sample_rate': 48000, 'bit_depth': 24, 'template': 'blank'}),
                ('track.new', {'name': 'Voice', 'format': 'mono', 'kind': 'audio'}),
                ('file.import_audio', {'path': 'voice.wav', 'track': 'Voice', 'new_tracks': False, 'at': {'seconds': 0}})]
        if name == 'voice-over-mix':
            init += [('track.new', {'name': 'Bed', 'format': 'mono', 'kind': 'audio'}),
                     ('file.import_audio', {'path': 'bed.wav', 'track': 'Bed', 'new_tracks': False, 'at': {'seconds': 0}}),
                     ('mix.pan', {'tracks': ['Voice'], 'pan': .6}),
                     ('edit.select', {'tracks': ['Bed'], 'start': {'seconds': 0}, 'end': {'seconds': 4}})]
        run(init, 'input.scraft')
        input_sha = hashlib.sha256((r.work / 'input.scraft').read_bytes()).hexdigest()
        if name == 'voice-over-mix':
            run([('mix.volume', {'tracks': ['Bed'], 'db': -144}), ('mix.pan', {'tracks': ['Voice'], 'pan': 0}), bounce('voice-center.wav')], source='input.scraft')
            run([('mix.volume', {'tracks': ['Voice'], 'db': -144}), bounce('bed-only.wav')], source='input.scraft')
        else:
            run([bounce('baseline.wav')], source='input.scraft')
        path = Path(skill_root) / ('soundcraft-' + name) / 'references/craft-steps.json'
        recipe = json.loads(path.read_text(encoding='utf-8'))
        run([(s['command'], s['params']) for s in recipe['steps']], 'result.scraft', 'input.scraft')
        output = {'voice-over-mix': 'output/voice-mix.wav', 'dialogue-leveling': 'output/dialogue-review.wav', 'audio-delivery': 'output/master.wav'}[name]
        rate, width, actual = pcm(r.work / output)
        assert rate == 48000 and width == 3 and len(actual) == 2 and all(len(c) == 192000 for c in actual), 'Not actual 4s/48kHz/24-bit stereo PCM'
        assert max(abs(v) for c in actual for v in c) < .99, 'Output clips'
        if name == 'voice-over-mix':
            verify_voice_mix(actual, pcm(r.work / 'voice-center.wav')[2], pcm(r.work / 'bed-only.wav')[2])
        elif name == 'dialogue-leveling':
            verify_dialogue(actual, pcm(r.work / 'baseline.wav')[2])
        else:
            close(actual, pcm(r.work / 'baseline.wav')[2])
            text = (r.work / 'output/session.txt').read_text(encoding='utf-8')
            assert 'Voice' in text and len(text) > 30, 'Session delivery report missing real track'
        run([bounce('reopened.wav')], source='result.scraft')
        close(pcm(r.work / 'reopened.wav')[2], actual)
        assert hashlib.sha256((r.work / 'input.scraft').read_bytes()).hexdigest() == input_sha, 'Input editable session changed'
        assert all(hashlib.sha256((r.work / p).read_bytes()).hexdigest() == sha for p, sha in hashes.items()), 'Source audio changed'
        records.append({'id': name, 'technicalRoundtrip': 'PASS', 'trackOrSegmentSignalChecks': 'PASS', 'pcm48k24bitStereo': 'PASS', 'sourceProtected': 'PASS', 'auditoryAcceptance': 'NOT_TESTED', 'installedHostSync': 'NOT_TESTED'})
    r.work = original
    return records
