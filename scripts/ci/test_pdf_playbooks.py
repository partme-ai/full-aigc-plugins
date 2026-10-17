import unittest
from pdf_playbook_smoke import verify_form, verify_redacted, verify_page_order


class PdfResultTests(unittest.TestCase):
    def test_correct_field_value_with_broken_visible_text_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'appearance'):
            verify_form({'fields': [{'name': 'CustomerName', 'value': '真实姓名'}]}, '????', '真实姓名')

    def test_hidden_secret_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'stream'):
            verify_redacted('PUBLIC KEEP CONFIDENTIALITY', b'\nstream\nBT (CONFIDENTIAL) Tj ET\nendstream\n')

    def test_secret_visible_in_text_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'extract'):
            verify_redacted('PUBLIC KEEP CONFIDENTIAL', b'%PDF')

    def test_correct_pages_in_wrong_order_are_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'order'):
            verify_page_order('PAGE ONE\fPAGE TWO\fPAGE THREE', ['PAGE THREE', 'PAGE ONE', 'PAGE TWO'])
