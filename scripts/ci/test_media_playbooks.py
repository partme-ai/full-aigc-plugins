"""信号检查负例：不以文件存在或反转标签代替样本效果。"""
from pathlib import Path
import tempfile
import unittest
from media_playbook_smoke import verify_audio,image_fixture
from photo_playbook_smoke import rgb_pixels


class MediaResultTests(unittest.TestCase):
    def test_unprocessed_samples_fail_polarity_check(self):
        wave=(48000,[[0.1]*192000])
        with self.assertRaisesRegex(AssertionError,'sample content'):
            verify_audio(wave,wave,wave,{'seconds':4,'check':'invert'})

    def test_unfaded_samples_fail_edge_check(self):
        wave=(48000,[[0.1]*192000])
        with self.assertRaisesRegex(AssertionError,'Head fade'):
            verify_audio(wave,wave,wave,{'seconds':4,'check':'fades'})

    def test_missing_frames_fail_excerpt_check(self):
        base=(48000,[[0.1]*192000]);short=(48000,[[0.1]*48000])
        with self.assertRaisesRegex(AssertionError,'duration/frame count'):
            verify_audio(short,base,base,{'seconds':2,'check':'excerpt','offset':1})

    def test_neutral_reference_fixture_is_actually_color_cast(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'input.png';image_fixture(p);w,h,pixels=rgb_pixels(p)
            self.assertEqual((w,h),(64,48));idx=(24*w+16)*3
            self.assertEqual(tuple(pixels[idx:idx+3]),(180,145,110))

if __name__=='__main__':unittest.main()
