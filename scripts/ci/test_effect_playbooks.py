import unittest
from effect_playbook_smoke import verify_mask


class MaskResultTests(unittest.TestCase):
    def tree(self):
        return {'children': [
            {'type': 'path', 'value': {'v': {'closed': True,
             'vertices': [[100, 100], [700, 100], [700, 450], [100, 450]]}}},
            {'path': 'transform/opacity', 'value': 90}]}

    def test_missing_mask_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'saved mask'):
            verify_mask({'children': []})

    def test_wrong_rectangle_is_rejected(self):
        tree = self.tree()
        tree['children'][0]['value']['v']['vertices'][1] = [600, 100]
        with self.assertRaisesRegex(AssertionError, 'coordinates'):
            verify_mask(tree)

    def test_wrong_opacity_is_rejected(self):
        tree = self.tree()
        tree['children'][1]['value'] = 100
        with self.assertRaisesRegex(AssertionError, 'opacity'):
            verify_mask(tree)

    def test_expected_saved_values_pass(self):
        verify_mask(self.tree())
