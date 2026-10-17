from pathlib import Path
import tempfile
import unittest
from vector_core_smoke import verify_logo, verify_icon, verify_trace, raster


def document(children):
    return {'layers':[{'kind':'Layer','children':children}]}


class VectorCoreTests(unittest.TestCase):
    def test_grouping_only_the_reflected_copy_is_not_a_paired_logo(self):
        with self.assertRaisesRegex(AssertionError,'both source'):
            verify_logo(document([{'kind':'Group','children':[{'kind':'Path'}]}]))

    def test_filled_icon_must_not_keep_an_inherited_outline(self):
        icon={'kind':'Ellipse','bounds':{'x':16,'y':16,'width':16,'height':16},
              'stroke':'#000000','strokeWidth':1,'fill':'#243042'}
        with self.assertRaisesRegex(AssertionError,'stroke'):
            verify_icon(document([icon]))

    def test_white_cover_is_not_a_transparent_trace_hole(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'ring.png';raster(path)
            with self.assertRaisesRegex(AssertionError,'transparent hole'):
                verify_trace(path,document([]))
