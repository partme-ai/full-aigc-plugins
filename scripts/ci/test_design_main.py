from pathlib import Path
import tempfile
import unittest
import zipfile
from design_main_smoke import verify_pptx


class DesignMainTests(unittest.TestCase):
    def test_raster_only_slide_is_not_editable_delivery(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'slide.pptx'
            with zipfile.ZipFile(p, 'w') as z:
                z.writestr('ppt/slides/slide1.xml', '<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:pic/></p:sld>')
            with self.assertRaises(AssertionError):
                verify_pptx(p)
