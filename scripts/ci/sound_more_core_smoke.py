"""SoundCraft另三核心：淡变、同源切口线性交叉淡化、带混音状态的分轨交付。"""
import hashlib
import json
import math
from pathlib import Path
from sound_core_smoke import pcm, close, fixture


def verify_edges(actual, baseline):
    def rms(a):
        return math.sqrt(sum(x * x for x in a) / len(a))
    assert len(actual) == len(baseline), 'Channel count changed'
    for a, b in zip(actual, baseline):
        assert len(a) == len(b) == 192000, 'Duration changed'
        assert rms(a[:480]) < rms(b[:480]) * .2 and rms(a[-480:]) < rms(b[-480:]) * .2, 'Short edge fades absent'
    close([c[48000:144000] for c in actual], [c[48000:144000] for c in baseline])


def verify_music_stems(lead, bed, lead_ref, bed_ref):
    close(bed, [[v * 10 ** (-12 / 20) for v in c] for c in bed_ref])
    def energy(a):
        return sum(x * x for c in a for x in c)
    ratio = math.sqrt(energy(lead) / energy(lead_ref))
    assert abs(ratio - 10 ** (-6 / 20)) < .002, 'Lead stem does not retain target fader gain'
    assert energy([lead[0]]) > energy([lead[1]]) * 1.1, 'Lead stem does not retain left pan'


def track_clips(session, name):
    tracks = [t for t in session['tracks'] if t['name'] == name]
    assert len(tracks) == 1, 'Ambiguous target track'
    track = tracks[0]
    return track, track['playlists'][track['active_playlist']]['clips']


def run_more_core(r, skill_root):
    original = r.work
    records = []
    try:
        for name in ['podcast-cleanup', 'audio-edit', 'music-demo']:
            r.work = original / ('core-' + name)
            r.work.mkdir()
            (r.work / 'output').mkdir()
            fixture(r.work / 'voice.wav', 440)
            fixture(r.work / 'bed.wav', 997)
            sources = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in r.work.glob('*.wav')}
            def run(steps, save=None, source=None):
                args = ['run'] + (['--in', source] if source else [])
                for command, params in steps:
                    args += ['--cmd', command + '=' + json.dumps(params, ensure_ascii=False, separators=(',', ':'))]
                if save:
                    args += ['--save', save]
                return r.run(*args)
            def bounce(path):
                return ('file.bounce_mix', {'path': path, 'format': 'wav', 'bit_depth': 24, 'start': {'seconds': 0}, 'end': {'seconds': 4}, 'normalize': False, 'dither': False})
            lead = 'Lead' if name == 'music-demo' else 'Voice'
            init = [('session.new', {'name': 'Core editable work copy', 'sample_rate': 48000, 'bit_depth': 24, 'template': 'blank'}),
                    ('track.new', {'name': lead, 'format': 'mono', 'kind': 'audio'}),
                    ('file.import_audio', {'path': 'voice.wav', 'track': lead, 'new_tracks': False, 'at': {'seconds': 0}})]
            if name == 'music-demo':
                init += [('track.new', {'name': 'Bed', 'format': 'mono', 'kind': 'audio'}),
                         ('file.import_audio', {'path': 'bed.wav', 'track': 'Bed', 'new_tracks': False, 'at': {'seconds': 0}}),
                         ('edit.select', {'tracks': ['Bed'], 'start': {'seconds': 0}, 'end': {'seconds': 4}})]
            run(init, 'input.scraft')
            input_hash = hashlib.sha256((r.work / 'input.scraft').read_bytes()).hexdigest()
            if name == 'music-demo':
                run([('mix.volume', {'tracks': ['Bed'], 'db': -144}), bounce('lead-reference.wav')], source='input.scraft')
                run([('mix.volume', {'tracks': ['Lead'], 'db': -144}), bounce('bed-reference.wav')], source='input.scraft')
            else:
                run([bounce('baseline.wav')], source='input.scraft')
            recipe = json.loads((Path(skill_root) / ('soundcraft-' + name) / 'references/craft-steps.json').read_text(encoding='utf-8'))
            run([(s['command'], s['params']) for s in recipe['steps']], 'result.scraft', 'input.scraft')
            output = {'podcast-cleanup': 'output/podcast-review.wav', 'audio-edit': 'output/edit-review.wav', 'music-demo': 'output/music-review.wav'}[name]
            rate, width, actual = pcm(r.work / output)
            assert rate == 48000 and width == 3 and len(actual) == 2 and all(len(c) == 192000 for c in actual), 'Output must be actual 4s 48kHz 24-bit stereo PCM'
            assert max(abs(v) for c in actual for v in c) < .99, 'Output clips'
            session = json.loads((r.work / 'result.scraft').read_text(encoding='utf-8'))
            track, clips = track_clips(session, lead)
            if name == 'podcast-cleanup':
                expected = [[v * 10 ** (-3 / 20) for v in c] for c in pcm(r.work / 'baseline.wav')[2]]
                verify_edges(actual, expected)
                assert len(clips) == 1 and clips[0]['gain_db'] == -3, 'Podcast gain changed wrong clip'
                assert clips[0]['fade_in']['len'] == clips[0]['fade_out']['len'] == 4800, 'Podcast fades not 100ms'
                assert clips[0]['start'] == 0 and clips[0]['length'] == 192000, 'Podcast content boundaries moved'
            elif name == 'audio-edit':
                close(actual, pcm(r.work / 'baseline.wav')[2])
                clips = sorted(clips, key=lambda c: c['start'])
                assert len(clips) == 2, 'Cut did not produce two editable clips'
                a, b = clips
                assert (a['start'], a['length'], b['start'], b['start'] + b['length']) == (0, 98400, 93600, 192000), 'Crossfade moved non-target content or changed total duration'
                assert a['fade_out']['len'] == b['fade_in']['len'] == 4800, 'Crossfade overlap is not 100ms'
                assert a['fade_out']['shape'] == b['fade_in']['shape'] == 'Linear', 'Correlated split must use linear complementary fades'
                assert a['content']['Audio']['source'] == b['content']['Audio']['source'], 'Split lost original source identity'
            else:
                assert track['mixer']['volume_db'] == -6 and track['mixer']['pan'] == [-.2], 'Lead mixer changed wrong track'
                bed_track, _ = track_clips(session, 'Bed')
                assert bed_track['mixer']['volume_db'] == -12 and bed_track['mixer']['pan'] == [0], 'Bed mixer changed wrong track'
                files = list((r.work / 'output/stems').glob('*.wav'))
                by_name = {p.stem.rsplit(' - ', 1)[-1]: p for p in files}
                assert set(by_name) == {'Lead', 'Bed'}, 'Stem export included wrong tracks'
                audio = {}
                for role, p in by_name.items():
                    sr, bits, ch = pcm(p)
                    assert sr == 48000 and bits == 3 and len(ch) == 2 and all(len(c) == 192000 for c in ch), 'Stem format or alignment differs'
                    audio[role] = ch
                verify_music_stems(audio['Lead'], audio['Bed'], pcm(r.work / 'lead-reference.wav')[2], pcm(r.work / 'bed-reference.wav')[2])
                close(actual, [[x + y for x, y in zip(a, b)] for a, b in zip(audio['Lead'], audio['Bed'])])
                run([('file.bounce_stems', {'dir': 'reopened-stems', 'format': 'wav', 'bit_depth': 24, 'start': {'seconds': 0}, 'end': {'seconds': 4}})], source='result.scraft')
                reopened_stems = {p.stem.rsplit(' - ', 1)[-1]: p for p in (r.work / 'reopened-stems').glob('*.wav')}
                assert set(reopened_stems) == set(by_name), 'Saved stem track set changed'
                for role in by_name:
                    close(pcm(reopened_stems[role])[2], audio[role])
            run([bounce('reopened.wav')], source='result.scraft')
            close(pcm(r.work / 'reopened.wav')[2], actual)
            assert hashlib.sha256((r.work / 'input.scraft').read_bytes()).hexdigest() == input_hash, 'Input editable session changed'
            assert all(hashlib.sha256((r.work / p).read_bytes()).hexdigest() == sha for p, sha in sources.items()), 'Source audio changed'
            records.append({'id': name, 'technicalRoundtrip': 'PASS', 'sampleAndNativeStructureChecks': 'PASS', 'pcm48k24bitStereo': 'PASS', 'sourceProtected': 'PASS', 'auditoryAcceptance': 'NOT_TESTED', 'installedHostSync': 'NOT_TESTED'})
        return records
    finally:
        r.work = original
