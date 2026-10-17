import unittest
from sound_core_smoke import verify_voice_mix, verify_dialogue


class SoundCoreTests(unittest.TestCase):
    def test_wrong_track_level_or_pan_is_rejected(self):
        voice = [[.1, -.1] * 100] * 2
        bed = [[.05, -.05] * 100] * 2
        for output in [voice, [[.1, -.1] * 100, [.02, -.02] * 100]]:
            with self.assertRaises(AssertionError):
                verify_voice_mix(output, voice, bed)

    def test_boosting_both_speaker_segments_is_rejected(self):
        baseline = [[.05] * 100 + [.1] * 100] * 2
        wrong = [[v * 10 ** (3 / 20) for v in c] for c in baseline]
        with self.assertRaises(AssertionError):
            verify_dialogue(wrong, baseline)
