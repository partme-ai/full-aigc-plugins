"""文档交付场景必须随技能提供具体可执行配方。"""
import json
import os
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from word_publishing_smoke import verify_toc, verify_sections, W, HEADINGS

SKILLS = Path(os.environ.get('CRAFT_WORD_SKILLS_ROOT', Path(__file__).resolve().parents[3] / 'full-aigc-skills-repositories/wordcraft-skills/skills'))


class PublishingSkills(unittest.TestCase):
    def test_three_independent_scenes(self):
        for name in ['toc-handbook', 'illustrated-guide', 'landscape-appendix']:
            with self.subTest(name=name):
                root = SKILLS / ('wordcraft-' + name)
                self.assertTrue((root / 'SKILL.md').is_file(), name)
                recipe = json.loads((root / 'references/craft-steps.json').read_text())
                self.assertGreater(len(recipe['steps']), 8)
                self.assertEqual(recipe['id'], name)

    def toc(self):
        doc = ET.Element(W + 'document')
        body = ET.SubElement(doc, W + 'body')
        content = ET.SubElement(ET.SubElement(body, W + 'sdt'), W + 'sdtContent')
        ET.SubElement(content, W + 'instrText').text = ' TOC \\o "1-2" '
        for i, title in enumerate(HEADINGS):
            p = ET.SubElement(content, W + 'p')
            ET.SubElement(p, W + 'pStyle', {W + 'val': 'TOC' + str(i % 2 + 1)})
            link = ET.SubElement(p, W + 'hyperlink', {W + 'anchor': str(i)})
            ET.SubElement(link, W + 't').text = title
            heading = ET.SubElement(body, W + 'p')
            ET.SubElement(heading, W + 'bookmarkStart', {W + 'name': str(i)})
            ET.SubElement(heading, W + 't').text = title
        return doc

    def test_real_toc(self):
        verify_toc(self.toc())

    def test_reject_plain_text_toc(self):
        doc = self.toc()
        doc.find('.//' + W + 'instrText').text = '目录'
        with self.assertRaisesRegex(AssertionError, 'TOC field'):
            verify_toc(doc)

    def test_reject_dead_toc_link(self):
        doc = self.toc()
        doc.find('.//' + W + 'hyperlink').set(W + 'anchor', 'missing')
        with self.assertRaisesRegex(AssertionError, 'missing bookmark'):
            verify_toc(doc)

    def test_reject_link_to_wrong_existing_heading(self):
        doc = self.toc()
        doc.find('.//' + W + 'hyperlink').set(W + 'anchor', '2')
        with self.assertRaisesRegex(AssertionError, 'different heading'):
            verify_toc(doc)

    def test_reject_whole_document_landscape(self):
        doc = ET.fromstring('<document xmlns="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><body><sectPr/></body></document>')
        with self.assertRaisesRegex(AssertionError, 'separate body/appendix'):
            verify_sections(doc)

    def test_reject_two_landscape_sections(self):
        doc = ET.Element(W + 'document')
        body = ET.SubElement(doc, W + 'body')
        for _ in range(2):
            section = ET.SubElement(body, W + 'sectPr')
            ET.SubElement(section, W + 'pgSz', {W + 'w': '16838', W + 'h': '11906'})
        with self.assertRaisesRegex(AssertionError, 'orientation wrong'):
            verify_sections(doc)


if __name__ == '__main__':
    unittest.main()
