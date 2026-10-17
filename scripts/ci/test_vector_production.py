"""矢量场景必须有独立技能与实际操作配方。"""
import json
import os
from pathlib import Path
import unittest
import tempfile

from vector_production_smoke import resolve, verify_expanded_grid, verify_border, recipe_hashes

SKILLS = Path(os.environ.get('CRAFT_VECTOR_SKILLS_ROOT', Path(__file__).resolve().parents[3] / 'full-aigc-skills-repositories/vectorcraft-skills/skills'))


class ProductionSkills(unittest.TestCase):
    def test_three_independent_scenes(self):
        for name in ['clipped-illustration', 'sticker-grid', 'sticker-offset-border']:
            with self.subTest(name=name):
                root = SKILLS / ('vectorcraft-' + name)
                self.assertTrue((root / 'SKILL.md').is_file(), name)
                recipe = json.loads((root / 'references/craft-steps.json').read_text())
                self.assertGreater(len(recipe['steps']), 4)
                self.assertEqual(recipe['id'], name)

    def test_bind_actual_returned_ids_without_nested_array(self):
        self.assertEqual(resolve({'ids': {'$ref': 'border.ids'}}, {'border': {'ids': [93, 94]}}), {'ids': [93, 94]})
        self.assertEqual(resolve([{'$ref': 'art.id'}], {'art': {'id': 72}}), [72])

    def test_missing_capture_cannot_guess_id(self):
        with self.assertRaises(KeyError):
            resolve({'$ref': 'art.id'}, {})

    def test_windows_text_newlines_keep_separate_raw_digest(self):
        with tempfile.TemporaryDirectory() as directory:
            lf, crlf = Path(directory) / 'lf.json', Path(directory) / 'crlf.json'
            lf.write_bytes(b'{"id":"sticker-grid"}\n')
            crlf.write_bytes(b'{"id":"sticker-grid"}\r\n')
            a, b = recipe_hashes(lf), recipe_hashes(crlf)
            self.assertEqual(a['recipeSha256'], b['recipeSha256'])
            self.assertNotEqual(a['recipeFileSha256'], b['recipeFileSha256'])

    def test_reject_twelve_overlapping_copies(self):
        info = {'layers': [{'kind': 'Ellipse', 'bounds': {'x': 20, 'y': 20, 'width': 30, 'height': 30}} for _ in range(12)]}
        with self.assertRaisesRegex(AssertionError, 'positions or dimensions'):
            verify_expanded_grid(info)

    def test_reject_unexpanded_repeat(self):
        with self.assertRaisesRegex(AssertionError, 'twelve editable'):
            verify_expanded_grid({'layers': [{'kind': 'Grid Repeat'}]})

    def border(self):
        art = {'id': 3, 'kind': 'Rectangle', 'fill': '#2563eb', 'bounds': {'x': 100, 'y': 80, 'width': 100, 'height': 60}}
        border = {'id': 4, 'kind': 'Path', 'fill': '#ffffff', 'closed': True, 'stroke': 'None',
                  'bounds': {'x': 92, 'y': 72, 'width': 116, 'height': 76}}
        return {'layers': [art, border]}, {'art': {'id': 3}, 'border': {'ids': [4]}}

    def test_reject_original_resized_as_offset(self):
        info, captures = self.border()
        info['layers'][0]['bounds']['width'] = 116
        with self.assertRaisesRegex(AssertionError, 'Original artwork changed'):
            verify_border(info, captures)

    def test_reject_wrong_offset_distance(self):
        info, captures = self.border()
        info['layers'][1]['bounds']['width'] = 108
        with self.assertRaisesRegex(AssertionError, 'distance or geometry'):
            verify_border(info, captures)

    def test_reject_open_border(self):
        info, captures = self.border()
        info['layers'][1]['closed'] = False
        with self.assertRaisesRegex(AssertionError, 'closed path'):
            verify_border(info, captures)


if __name__ == '__main__':
    unittest.main()
