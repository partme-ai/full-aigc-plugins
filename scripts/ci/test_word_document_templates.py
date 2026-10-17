import io
import unittest
import zipfile
from office_playbook_smoke import verify_word

W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
class DocumentTableChecks(unittest.TestCase):
    def check(self,xml,assertion):
        data=io.BytesIO()
        with zipfile.ZipFile(data,'w') as z:
            z.writestr('word/document.xml',xml)
            z.writestr('word/styles.xml',f'<w:styles xmlns:w="{W}"><w:style w:styleId="H2"><w:name w:val="Heading 2"/></w:style></w:styles>')
        with zipfile.ZipFile(data) as z:verify_word(z,assertion)
    def test_same_text_in_wrong_cells_does_not_pass(self):
        xml=f'<w:document xmlns:w="{W}"><w:body><w:tbl><w:tr><w:tc><w:p><w:r><w:t>姓名任务</w:t></w:r></w:p></w:tc></w:tr></w:tbl></w:body></w:document>'
        with self.assertRaisesRegex(AssertionError,'cell'):self.check(xml,{'tableCells':[['姓名','任务']]})
    def test_visual_heading_text_without_style_is_rejected(self):
        xml=f'<w:document xmlns:w="{W}"><w:body><w:p><w:r><w:t>验收条件</w:t></w:r></w:p></w:body></w:document>'
        with self.assertRaisesRegex(AssertionError,'heading'):self.check(xml,{'heading2Minimum':1})
