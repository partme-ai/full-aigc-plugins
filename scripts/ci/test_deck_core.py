import copy
import unittest
from deck_core_smoke import verify_notes, verify_redesign


def note(text):
    return {'notes': {'paragraphs': [{'runs': [{'text': text}]}]}}


class DeckCoreTests(unittest.TestCase):
    def test_note_on_only_one_slide_is_rejected(self):
        with self.assertRaises(AssertionError):
            verify_notes([note('目标练习回顾'), note(''), note('')], ['目标', '练习', '回顾'])

    def test_redesign_must_preserve_original_slides_and_use_new_ids(self):
        before = {'slides': [{'id': 1, 'shapes': [{'id': 10}]}, {'id': 2, 'shapes': []}]}
        for after in [ {'slides': [before['slides'][1], before['slides'][0], before['slides'][1]]},
                       {'slides': [before['slides'][0], copy.deepcopy(before['slides'][0]), before['slides'][1]]} ]:
            with self.assertRaises(AssertionError):
                verify_redesign(before, after)
