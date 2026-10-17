import unittest
from print_main_smoke import verify_count


class PrintMainTest(unittest.TestCase):
    def test_repeated_pages_and_partial_counts_do_not_pass(self):
        for value in [{'total': {'words': 6}, 'pages': [1, 1]}, {'total': {'words': 2}, 'pages': [1]}]:
            with self.assertRaises(AssertionError):
                verify_count(value)
