import unittest
from pathlib import Path
import struct
import tempfile
import zlib
from effect_playbook_smoke import verify_mask, verify_fade, verify_loop, verify_texts
from photo_playbook_smoke import rgb_pixels


class MaskResultTests(unittest.TestCase):
    def tree(self):
        return {'children': [
            {'type': 'path', 'value': {'v': {'closed': True,
             'vertices': [[100, 100], [700, 100], [700, 450], [100, 450]]}}},
            {'path': 'transform/opacity', 'value': 90}]}

    def test_missing_mask_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'saved mask'):
            verify_mask({'children': []})

    def test_wrong_rectangle_is_rejected(self):
        tree = self.tree()
        tree['children'][0]['value']['v']['vertices'][1] = [600, 100]
        with self.assertRaisesRegex(AssertionError, 'coordinates'):
            verify_mask(tree)

    def test_wrong_opacity_is_rejected(self):
        tree = self.tree()
        tree['children'][1]['value'] = 100
        with self.assertRaisesRegex(AssertionError, 'opacity'):
            verify_mask(tree)

    def test_expected_saved_values_pass(self):
        verify_mask(self.tree())

    def test_png_alpha_is_preserved_for_animation_checks(self):
        def chunk(kind, data):
            return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data))
        png = (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 2, 1, 8, 6, 0, 0, 0))
               + chunk(b'IDAT', zlib.compress(bytes([0, 255, 0, 0, 0, 255, 0, 0, 229]))) + chunk(b'IEND', b''))
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / 'opacity.png'
            file.write_bytes(png)
            self.assertEqual(rgb_pixels(file, include_alpha=True), (2, 1, bytes([255, 0, 0, 0, 255, 0, 0, 229])))
            self.assertEqual(rgb_pixels(file), (2, 1, bytes([255, 0, 0, 255, 0, 0])))


class AnimationResultTests(unittest.TestCase):
    def test_fully_visible_first_frame_is_not_a_fade(self):
        with self.assertRaisesRegex(AssertionError, 'first frame'):
            verify_fade([10000, 10000, 10000, 10000])

    def test_missing_intermediate_opacity_is_not_a_fade(self):
        with self.assertRaisesRegex(AssertionError, 'halfway'):
            verify_fade([0, 0, 10000, 10000])

    def test_missing_late_text_is_not_a_hold(self):
        with self.assertRaisesRegex(AssertionError, 'hold'):
            verify_fade([0, 5000, 10000, 0])

    def test_static_dot_is_not_a_loop_motion(self):
        with self.assertRaisesRegex(AssertionError, 'midpoint'):
            verify_loop([(89, 240), (89, 240), (96, 240)])

    def test_blank_last_frame_is_not_a_loop(self):
        with self.assertRaisesRegex(AssertionError, 'empty'):
            verify_loop([(89, 240), (391, 240), None])

    def test_swapped_name_and_role_fail_even_when_all_text_is_present(self):
        wrong = {'Name': {'text': '真实职位', 'position': [180, 880, 0]},
                 'Role': {'text': '真实姓名', 'position': [180, 940, 0]}}
        with self.assertRaisesRegex(AssertionError, 'text'):
            verify_texts(wrong)
