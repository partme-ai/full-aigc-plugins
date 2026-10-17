import unittest
from sound_more_core_smoke import verify_edges, verify_music_stems


class SoundMoreCoreTests(unittest.TestCase):
    def test_unchanged_edges_are_not_fades(self):
        wave = [[.1, -.1] * 96000] * 2
        with self.assertRaises(AssertionError):
            verify_edges(wave, wave)

    def test_music_stem_wrong_level_or_pan_is_rejected(self):
        ref = [[.1, -.1] * 100] * 2
        bed = [[.02, -.02] * 100] * 2
        for lead in [ref, [[x * 10 ** (-6 / 20) for x in c] for c in ref]]:
            with self.assertRaises(AssertionError):
                verify_music_stems(lead, bed, ref, bed)
