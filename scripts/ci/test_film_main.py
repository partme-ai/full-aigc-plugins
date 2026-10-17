import unittest
from film_main_smoke import verify_removed


def sequence(video, audio):
    return {'video': [{'id': 1, 'items': video}], 'audio': [{'id': 2, 'items': audio}]}


class FilmMainTests(unittest.TestCase):
    def test_losing_partner_or_moving_other_clip_is_rejected(self):
        before = sequence([{'clip': 10, 'start': 0}], [{'clip': 11, 'start': 0}, {'clip': 12, 'start': 48}])
        for after in [sequence([], [{'clip': 12, 'start': 48}]),
                      sequence([], [{'clip': 11, 'start': 0}, {'clip': 12, 'start': 0}])]:
            with self.assertRaises(AssertionError):
                verify_removed(before, after, 10)

    def test_only_target_is_removed(self):
        before = sequence([{'clip': 10}], [{'clip': 11}])
        verify_removed(before, sequence([], [{'clip': 11}]), 10)
