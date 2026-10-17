import unittest
from deck_main_smoke import verify_reused_titles


class DeckMainTests(unittest.TestCase):
    def test_wrong_page_order_or_extra_brand_page_is_rejected(self):
        for after in [['DEST', 'BRAND C', 'BRAND A'], ['DEST', 'BRAND A', 'BRAND B', 'BRAND C']]:
            with self.assertRaises(AssertionError):
                verify_reused_titles(['DEST'], after, ['BRAND A', 'BRAND C'])
