"""候选构建不得串用源码、稳定版或覆盖活动编辑器。"""
import unittest
from craft_main import candidate, build_matrix


class MainCandidatesTest(unittest.TestCase):
    def test_exactly_thirteen_pinned_sources(self):
        rows = build_matrix()['include']
        self.assertEqual(len(rows), 13)
        self.assertEqual(len({r['app'] for r in rows}), 13)
        for row in rows:
            self.assertRegex(row['commit'], r'^[a-f0-9]{40}$')
            self.assertRegex(row['pluginCommit'], r'^[a-f0-9]{40}$')
            self.assertRegex(row['skillsCommit'], r'^[a-f0-9]{40}$')
            self.assertEqual(row['status'], 'development-candidate-not-accepted')

    def test_printcraft_uses_pdfcraft_engine(self):
        row = candidate('printcraft')
        self.assertEqual(row['engine'], 'pdfcraft')
        self.assertEqual(row['repository'], 'storytold/pdfcraft')

    def test_unknown_app_rejected(self):
        with self.assertRaises(ValueError):
            candidate('../cadcraft')


if __name__ == '__main__':
    unittest.main()
