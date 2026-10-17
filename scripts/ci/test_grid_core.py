import unittest
from grid_core_smoke import verify_clean_rows, verify_audit


class GridCoreTests(unittest.TestCase):
    def test_numeric_key_does_not_preserve_leading_zeros(self):
        with self.assertRaisesRegex(AssertionError, 'text'):
            verify_clean_rows([['ID', 'Name', 'Amount', 'Region'], [1, 'Alice', 10, 'E']])

    def test_key_conflict_must_not_be_silently_removed(self):
        with self.assertRaisesRegex(AssertionError, 'conflict'):
            verify_clean_rows([['ID', 'Name', 'Amount', 'Region'], ['001', 'Alice', 10, 'E'],
                               ['002', 'Bob', 20, 'W'], ['1', 'Carol', 30, 'N']])

    def test_empty_error_list_does_not_validate_known_bad_formula(self):
        with self.assertRaisesRegex(AssertionError, 'error'):
            verify_audit({'errors': []}, [{'range': 'B2'}, {'range': 'C2'}], {'result': 20})

    def test_wrong_precedents_do_not_validate_the_formula(self):
        with self.assertRaisesRegex(AssertionError, 'precedents'):
            verify_audit({'errors': [{'cell': 'H3', 'error': '#DIV/0!'}]},
                         [{'range': 'B2'}, {'range': 'D2'}], {'result': 20})
