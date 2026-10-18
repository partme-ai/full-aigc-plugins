"""编辑器源码变动必须使当前证据过期；不重绑定历史宿主证据。"""
from pathlib import Path
import runpy
import tempfile
import unittest


class EditorEvidenceTests(unittest.TestCase):
    def test_client_change_invalidates_current_evidence(self):
        functions = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'scripts/evidence.py'))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            client = root / 'ui/runtime/client.mjs'
            client.parent.mkdir(parents=True)
            client.write_text('original client')
            index = {'sourceSha256': functions['fingerprint'](root), 'evidenceSha256': {}}
            self.assertTrue(functions['current'](index, root))
            client.write_text('changed client')
            self.assertFalse(functions['current'](index, root))
