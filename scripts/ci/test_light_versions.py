"""LightCraft编辑分支的内容与选择保护回归。"""
import unittest
from light_versions_smoke import verify_curve_only, named_version_index


class VersionChecks(unittest.TestCase):
    def test_curve_migration_preserves_target_exposure(self):
        source = {'curve': {'master': [[0, 0], [1, 1]]}, 'light': {'exposure': 0}}
        before = {'curve': {}, 'light': {'exposure': 1}}
        after = {'curve': source['curve'], 'light': {'exposure': 1}}
        verify_curve_only(source, before, after)
        with self.assertRaises(AssertionError):
            verify_curve_only(source, before, source)

    def test_curve_must_actually_be_copied(self):
        with self.assertRaises(AssertionError):
            verify_curve_only({'curve': {'master': [1]}}, {'curve': {}}, {'curve': {}})

    def test_version_index_comes_from_actual_name(self):
        value = {'versions': [{'name': 'Old'}, {'name': 'Review'}]}
        self.assertEqual(named_version_index(value, 'Review'), 1)
        with self.assertRaises(AssertionError):
            named_version_index(value, 'Absent')
        with self.assertRaises(AssertionError):
            named_version_index({'versions': [{'name': 'Review'}, {'name': 'Review'}]}, 'Review')
