"""业务结果判定回归；不能替代 Windows 原生执行。"""
import unittest
from pathlib import Path
import tempfile
from photo_playbook_smoke import fixture, rgb_pixels
from craft_cli_windows import verify_photo


class PhotoContractTests(unittest.TestCase):
    def info(self):
        return {'name':'图片.pcraft','width':64,'height':48,
                'layers':[{'name':'中文业务','kind':'Pixel','bounds':[-2,-2,46,36]}]}

    def test_saved_identity_uses_filename(self):
        verify_photo(self.info(), '图片.pcraft', '中文业务')

    def test_missing_layer_fails(self):
        value=self.info(); value['layers']=[]
        with self.assertRaisesRegex(AssertionError, 'layer name'):
            verify_photo(value, '图片.pcraft', '中文业务')

    def test_empty_paint_fails(self):
        value=self.info(); value['layers'][0]['bounds']=[0,0,0,0]
        with self.assertRaisesRegex(AssertionError, 'content bounds'):
            verify_photo(value, '图片.pcraft', '中文业务')

    def test_wrong_dimensions_fail(self):
        value=self.info(); value['width']=1
        with self.assertRaisesRegex(AssertionError, 'dimensions'):
            verify_photo(value, '图片.pcraft', '中文业务')

class PngInspectionTests(unittest.TestCase):
    def test_fixture_pixel_identity_is_decoded(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'input.png';fixture(p);w,h,pixels=rgb_pixels(p)
            self.assertEqual((w,h),(256,192))
            self.assertEqual(pixels[:3],bytes((50,50,100)))
            point=(30*w+40)*3
            self.assertEqual(pixels[point:point+3],b'\xff\xff\xff')

if __name__ == '__main__': unittest.main()
