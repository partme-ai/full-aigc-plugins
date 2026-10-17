import unittest
from effect_lower_third_smoke import verify_stages, verify_caption_bounds
class LowerThird(unittest.TestCase):
    def test_static_or_missing_exit_rejected(self):
        for values in [[10000]*5,[0,5000,10000,10000,10000],[0,10000,10000,10000,0]]:
            with self.subTest(values=values),self.assertRaises(AssertionError):verify_stages(values)
    def test_fade_hold_and_exit(self):
        verify_stages([0,5100,10000,10000,0])
    def test_caption_outside_plate_rejected(self):
        pixels=bytearray(960*540*4);i=(440*960+10)*4;pixels[i:i+4]=bytes([255]*4)
        with self.assertRaisesRegex(AssertionError,'safe'):verify_caption_bounds(960,540,pixels)
if __name__=='__main__':unittest.main()
