import unittest
from photo_more_smoke import verify_mirror, verify_padding


class PhotoGeometryTests(unittest.TestCase):
    def test_unflipped_output_is_rejected(self):
        image = (2, 1, bytes([10, 20, 30, 255, 40, 50, 60, 255]))
        with self.assertRaisesRegex(AssertionError, 'mirror'):
            verify_mirror(image, image)

    def test_opaque_corners_do_not_count_as_transparent_padding(self):
        baseline = (1, 1, bytes([10, 20, 30, 255]))
        output = (3, 3, bytes([10, 20, 30, 255]) * 9)
        with self.assertRaisesRegex(AssertionError, 'extension'):
            verify_padding(output, baseline, 1, 1, False)

    def test_resized_center_does_not_count_as_canvas_padding(self):
        baseline = (1, 1, bytes([10, 20, 30, 255]))
        pixels = bytearray([0] * 36)
        pixels[16:20] = bytes([11, 20, 30, 255])
        with self.assertRaisesRegex(AssertionError, 'original pixels'):
            verify_padding((3, 3, bytes(pixels)), baseline, 1, 1, False)
