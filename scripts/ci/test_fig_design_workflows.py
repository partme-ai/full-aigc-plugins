"""Fig柱图正负零基线、输入边界及组件属性检查。"""
import unittest
from fig_design_workflows_smoke import bar_geometry, verify_icon_instance, verify_alias_export


class FigDesignChecks(unittest.TestCase):
    def test_exported_alias_must_retain_both_mode_references(self):
        values = {'light': {'type': 'VARIABLE_ALIAS', 'id': 'palette'},
                  'dark': {'type': 'VARIABLE_ALIAS', 'id': 'palette'}}
        tokens = {'meta': {'variables': {'semantic': {'valuesByMode': values}}}}
        verify_alias_export(tokens, 'semantic', 'palette')
        values['dark'] = {'r': 0, 'g': 0, 'b': 0, 'a': 1}
        with self.assertRaises(AssertionError):
            verify_alias_export(tokens, 'semantic', 'palette')

    def test_signed_zero_baseline(self):
        baseline, bars = bar_geometry([-20, 0, 40, 80])
        self.assertEqual(baseline, 680)
        self.assertEqual(bars, [(680, 120), (680, 0), (440, 240), (200, 480)])

    def test_all_zero_has_finite_empty_bars(self):
        baseline, bars = bar_geometry([0, 0])
        self.assertEqual(baseline, 500)
        self.assertEqual(bars, [(500, 0), (500, 0)])

    def test_negative_only_baseline_at_top(self):
        baseline, bars = bar_geometry([-20, -10])
        self.assertEqual(baseline, 200)
        self.assertEqual(bars, [(200, 600), (200, 300)])

    def test_non_numeric_values_are_not_zero(self):
        for values in [[], [True], [None], ['2'], [float('nan')], [float('inf')]]:
            with self.assertRaises(ValueError):
                bar_geometry(values)

    def test_icon_and_label_require_actual_nested_instance(self):
        node = {'componentProperties': {'Icon': 9, 'Show Icon': True, 'Label': 'Save'},
                'children': [{'type': 'INSTANCE', 'mainComponent': 9}, {'characters': 'Save'}]}
        verify_icon_instance(node, 9, 'Save', True)
        node['children'][0]['mainComponent'] = 8
        with self.assertRaises(AssertionError):
            verify_icon_instance(node, 9, 'Save', True)
