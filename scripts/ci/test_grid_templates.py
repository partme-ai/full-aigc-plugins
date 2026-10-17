from datetime import date, timedelta
from pathlib import Path
import tempfile
import unittest
from grid_templates_smoke import verify_calendar, verify_payment, verify_hours
from grid_core_smoke import core_recipe_paths


class GridTemplateTests(unittest.TestCase):
    def test_new_template_does_not_change_six_core_recipe_selection(self):
        names = ['budget-tracker', 'clean-table', 'dashboard', 'formula-audit', 'reconcile-data', 'sales-summary']
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for name in names + ['month-calendar']:
                file = root / ('gridcraft-' + name) / 'references/craft-steps.json'
                file.parent.mkdir(parents=True)
                file.write_text('{}')
            selected = core_recipe_paths(root)
            self.assertEqual([file.parent.parent.name for file in selected], ['gridcraft-' + n for n in names])

    def test_calendar_rejects_missing_leap_day_or_repeated_cache(self):
        first = date(2028, 2, 1)
        first -= timedelta(days=first.weekday())
        serial = (first - date(1899, 12, 30)).days
        rows = [[serial + r * 7 + c for c in range(7)] for r in range(6)]
        verify_calendar(rows, 2028, 2)
        for bad in [rows[:5], [rows[0]] * 6, [[v + 1 for v in row] for row in rows]]:
            with self.assertRaises(AssertionError):
                verify_calendar(bad, 2028, 2)

    def test_payment_rejects_wrong_total_sign_or_numeric_string(self):
        verify_payment([[1000], [12000], [0]], 12000, 0, 12)
        for bad in [[[1000], [12000], [1]], [[-1000], [-12000], [0]], [['1000'], [12000], [0]]]:
            with self.assertRaises(AssertionError):
                verify_payment(bad, 12000, 0, 12)

    def test_hours_do_not_silently_accept_missing_or_invalid_rows(self):
        rows = [[8, 'OK'], [8, 'OK'], ['', 'Missing input'], ['', 'Review input'], [None, None], [16, 'Incomplete rows excluded']]
        verify_hours(rows)
        for bad in [rows[:5], [[-16, 'OK']] + rows[1:], rows[:3] + [[0, 'OK']] + rows[4:]]:
            with self.assertRaises(AssertionError):
                verify_hours(bad)
