import tempfile
from pathlib import Path
import unittest
import zipfile
from word_main_smoke import verify_mail, verify_headers


class WordMainTests(unittest.TestCase):
    def doc(self, folder, parts):
        p = Path(folder) / 'test.docx'
        with zipfile.ZipFile(p, 'w') as z:
            for name, text in parts.items():
                z.writestr(name, '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:t>' + text + '</w:t></w:document>')
        return p

    def test_names_only_in_body_do_not_count_as_headers(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self.doc(tmp, {'word/document.xml': 'MAIN BODY MAIN HEADER MAIN FOOTER'})
            with self.assertRaises(AssertionError):
                verify_headers(p)

    def test_unfiltered_or_unsorted_merge_fails(self):
        for text in ['ACTIVE-ALICE ACTIVE-CAROL', 'ACTIVE-CAROL INACTIVE-BOB ACTIVE-ALICE']:
            with tempfile.TemporaryDirectory() as tmp:
                p = self.doc(tmp, {'word/document.xml': text})
                with self.assertRaises(AssertionError):
                    verify_mail(p)
