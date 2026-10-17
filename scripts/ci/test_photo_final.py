import unittest
from photo_final_smoke import verify_matte, verify_background


class AlphaResultTests(unittest.TestCase):
    def test_duplicate_alpha_is_not_preserved_transparency(self):
        original = (1, 1, bytes([147, 177, 217, 128]))
        output = (1, 1, bytes([76, 126, 192, 192]))
        with self.assertRaisesRegex(AssertionError, 'alpha'):
            verify_matte(original, output)

    def test_opaque_background_is_not_a_cutout(self):
        output = (64, 64, bytes([255] * 64 * 64 * 4))
        with self.assertRaisesRegex(AssertionError, 'background'):
            verify_background(output)

    def test_fully_empty_image_is_not_a_cutout(self):
        output = (64, 64, bytes([0] * 64 * 64 * 4))
        with self.assertRaisesRegex(AssertionError, 'subject'):
            verify_background(output)
