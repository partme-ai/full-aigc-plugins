import unittest
from photo_repair_smoke import verify_repair


class RepairResultTests(unittest.TestCase):
    def test_unchanged_damage_is_not_a_repair(self):
        before = bytes([240, 240, 240, 100, 100, 100])
        clean = bytes([100] * 6)
        with self.assertRaisesRegex(AssertionError, 'damage'):
            verify_repair(before, before, clean, 2, [(0, 0)], (0, 0, 1, 1), 0.1)

    def test_repair_that_changes_protected_pixels_is_rejected(self):
        before = bytes([240, 240, 240, 100, 100, 100])
        clean = bytes([100] * 6)
        after = bytes([100, 100, 100, 110, 100, 100])
        with self.assertRaisesRegex(AssertionError, 'protected'):
            verify_repair(before, after, clean, 2, [(0, 0)], (0, 0, 1, 1), 0.1)

    def test_damaged_ground_truth_is_rejected(self):
        image = bytes([100] * 6)
        with self.assertRaisesRegex(AssertionError, 'fixture'):
            verify_repair(image, image, image, 2, [(0, 0)], (0, 0, 1, 1), 0.1)
