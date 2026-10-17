import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from deck_comparison_smoke import verify_table


def table():
    return {'cols': [220, 310, 310], 'rows': [
        {'cells': [{'text': {'paragraphs': [{'runs': [{'text': value}]}]}} for value in row]}
        for row in [['Criterion', 'Option A', 'Option B'], ['Cost', '1200 USD/year', '1600 USD/year'],
                    ['Delivery', '4 weeks', '3 weeks'], ['Risk', 'Vendor dependency', 'Training required']]]}


class ComparisonTests(unittest.TestCase):
    def test_deepened_skill_does_not_inflate_scene_count(self):
        spec = importlib.util.spec_from_file_location('playbook_validator', Path(__file__).resolve().parents[1] / 'validate-craft-playbooks.py')
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            skill = root / 'deepened'
            refs = skill / 'references'
            refs.mkdir(parents=True)
            (skill / 'SKILL.md').write_text('---\nname: deepened\ndescription: test\n---\n')
            records = {'craft-steps.json': {'id': 'deeper', 'extendsScene': 'original', 'check': 'readback',
                       'boundary': 'test only', 'steps': [{'command': 'file.new', 'params': {}}]},
                       'craft-command-evidence.json': {'observedCommands': {'file.new': {'params': '{}'}}},
                       'workflow-sources.json': {'sources': [{'commit': 'a' * 40, 'readFiles': [{'path': 'README'}]}]}}
            for name, record in records.items():
                (refs / name).write_text(json.dumps(record))
            errors, count = validator.validate_skill(skill)
            self.assertTrue(any('unknown original scene' in error for error in errors))
            base = root / 'base/references'
            base.mkdir(parents=True)
            (base / 'recipes.json').write_text(json.dumps({'recipes': [{'id': 'original'}]}))
            errors, count = validator.validate_skill(skill)
            self.assertEqual(errors, [])
            self.assertEqual(count, 0)

    def test_original_values_and_dimensions(self):
        verify_table(table())

    def test_swapped_or_missing_values_are_rejected(self):
        for mutation in ['swap', 'missing']:
            item = copy.deepcopy(table())
            if mutation == 'swap':
                item['rows'][1]['cells'][1:3] = reversed(item['rows'][1]['cells'][1:3])
            else:
                item['rows'].pop()
            with self.assertRaises(AssertionError):
                verify_table(item)

    def test_width_drift_is_rejected(self):
        item = table()
        item['cols'] = [220, 280, 280]
        with self.assertRaises(AssertionError):
            verify_table(item)
