"""Office 检查必须识别真实结构和计算结果，不能只匹配可见文字。"""
import io
import unittest
import zipfile
from office_playbook_smoke import verify_deck, verify_word, verify_grid


def archive(files):
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w') as z:
        for name,data in files.items():z.writestr(name,data)
    return zipfile.ZipFile(io.BytesIO(buf.getvalue()))


class OfficeResultTests(unittest.TestCase):
    def test_visible_table_title_does_not_prove_editable_table(self):
        with archive({'ppt/slides/slide1.xml':'<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:t>方案比较表</a:t></p:sld>'}) as z:
            with self.assertRaisesRegex(AssertionError,'editable table'):
                verify_deck(z,{'slides':1,'textContains':['方案比较表'],'tableCount':1})

    def test_heading_text_without_applied_style_fails(self):
        with archive({'word/document.xml':'<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>项目启动说明</w:t></w:r></w:p></w:body></w:document>',
                      'word/styles.xml':'<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:style w:styleId="Heading1"><w:name w:val="heading 1"/></w:style></w:styles>'}) as z:
            with self.assertRaisesRegex(AssertionError,'applied first-level heading'):
                verify_word(z,{'textContains':['项目启动说明'],'headingRequired':True})

    def test_formula_text_does_not_substitute_computed_value(self):
        class Runner:
            def run(self,*args):return '21'
        with self.assertRaisesRegex(AssertionError,'Computed value mismatch'):
            verify_grid(Runner(),'test.xlsx',{'cells':{'B2':42}})

    def test_speaker_note_must_be_notes_content(self):
        with archive({'ppt/slides/slide1.xml':'<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:t>备注：转场</a:t></p:sld>'}) as z:
            with self.assertRaisesRegex(AssertionError,'Speaker note lost'):
                verify_deck(z,{'slides':1,'notesContains':['转场']})


if __name__=='__main__':unittest.main()
