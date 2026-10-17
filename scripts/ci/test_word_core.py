import io
import unittest
import zipfile
from word_core_smoke import verify_core


class WordCoreTests(unittest.TestCase):
    def document(self, body):
        data = io.BytesIO()
        with zipfile.ZipFile(data, 'w') as z:
            z.writestr('word/document.xml', '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>' + body + '</w:body></w:document>')
        return zipfile.ZipFile(data)

    def test_blank_action_table_is_not_meeting_minutes(self):
        with self.document('<w:tbl/>') as z, self.assertRaisesRegex(AssertionError, 'table cell'):
            verify_core(z, 'meeting-minutes')

    def test_plain_revised_text_is_not_tracked_comparison(self):
        with self.document('<w:p><w:r><w:t>金额120，截止2026-10-25。</w:t></w:r></w:p>') as z:
            with self.assertRaisesRegex(AssertionError, 'original'):
                verify_core(z, 'document-comparison')

    def test_style_cleanup_must_preserve_text(self):
        with self.document('<w:p/>') as z, self.assertRaisesRegex(AssertionError, 'text'):
            verify_core(z, 'document-style')
