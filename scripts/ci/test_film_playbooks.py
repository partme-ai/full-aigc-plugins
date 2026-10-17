import unittest
from film_playbook_smoke import resolve, verify_trim, verify_razor, verify_subtitles, verify_match


class FilmResultTests(unittest.TestCase):
    def test_id_reference_preserves_integer(self):
        self.assertEqual(resolve({'clip': {'$ref': 'insert.clips.0'}}, {'insert': {'clips': [29]}}), {'clip': 29})

    def test_missing_id_is_not_guessed(self):
        with self.assertRaises((KeyError, IndexError)):
            resolve({'$ref': 'insert.clips.0'}, {'insert': {'clips': []}})

    def test_untrimmed_clip_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'trim'):
            verify_trim([{'clip': 29, 'startFrame': 0, 'endFrame': 100, 'durationFrames': 100}], 29)

    def test_razor_gap_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'contiguous'):
            verify_razor([{'startFrame': 0, 'endFrame': 90}, {'startFrame': 91, 'endFrame': 120}])

    def test_wrong_srt_timing_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'timing'):
            verify_subtitles('1\n00:00:00,000 --> 00:00:03,000\n经过校对的实际台词\n')

    def test_changed_but_worse_color_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'reference'):
            verify_match(bytes([100] * 100), bytes([200] * 100), bytes([0] * 100))
