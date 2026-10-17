import unittest
from sound_production_smoke import verify_gaps, verify_loop


def clip(start, length, offset=0):
    return {'start': start, 'length': length, 'content': {'Audio': {'source': 2, 'offset': offset}}}


class SoundProductionTests(unittest.TestCase):
    def test_gaps_preserve_source_offsets_and_time(self):
        parts = [clip(23521, 49439, 23521), clip(119521, 49439, 119521)]
        verify_gaps(parts)
        for broken in [parts[:1], [clip(0, 49439, 23521), parts[1]], [parts[0], clip(119521, 49439, 0)]]:
            with self.assertRaises(AssertionError):
                verify_gaps(broken)

    def test_loop_count_includes_original_and_cannot_overlap(self):
        parts = [clip(i * 48000, 48000) for i in range(3)]
        verify_loop(parts)
        for broken in [parts + [clip(144000, 48000)], [parts[0]] * 3, parts[:2]]:
            with self.assertRaises(AssertionError):
                verify_loop(broken)
