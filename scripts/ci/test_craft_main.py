"""候选构建不得串用源码、稳定版或覆盖活动编辑器。"""
import unittest
from unittest.mock import patch
from pathlib import Path
import tempfile
from craft_main import candidate, build_matrix, prepare_web, apply_candidate_patches


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

    def test_apps_without_separate_font_overlay(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'ui').mkdir()
            (root / 'ui/source.lock.json').write_text('{"patches": []}')
            with patch('craft_main.verify_checkout'), patch('craft_main.apply_candidate_patches'), patch('craft_main.run') as run:
                prepare_web(candidate('photocraft'), root / 'source', root)
                self.assertEqual(run.call_count, 1)
                self.assertIn('prepare-automation.py', str(run.call_args.args[1]))

    def test_changed_patch_is_rejected_before_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / 'ui/runtime/patches'
            folder.mkdir(parents=True)
            (folder / 'fix.patch').write_text('changed')
            row = {'pluginCommit': 'a' * 40, 'candidatePatches': [{'file': 'fix.patch', 'sha256': '0' * 64}]}
            with patch('craft_main.verify_checkout'), patch('craft_main.run') as run:
                with self.assertRaisesRegex(ValueError, 'checksum'):
                    apply_candidate_patches(row, root / 'source', root)
                run.assert_not_called()


if __name__ == '__main__':
    unittest.main()
