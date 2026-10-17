import unittest
from light_main_smoke import verify_print_settings


class LightMainTests(unittest.TestCase):
    def test_wrong_grid_or_resolution_is_rejected(self):
        for cols, ppi in [(1, 150), (3, 300)]:
            with self.assertRaises(AssertionError):
                verify_print_settings({'settings': {'layout': {'style': 'contactSheet', 'grid': {'columns': cols, 'rows': 3}}, 'job': {'ppi': ppi}}})
