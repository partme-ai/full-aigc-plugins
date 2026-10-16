"""Windows 分发检查的离线回归，不冒充 Windows 宿主实测。"""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from craft_windows import extract_package


class PackageTests(unittest.TestCase):
    def make_archive(self, root, extra=None, missing=None):
        files = {
            'plugin.json': json.dumps({'name': 'photocraft', 'version': '1.0.0'}),
            '.codex-plugin/plugin.json': json.dumps({'name': 'photocraft', 'version': '1.0.0'}),
            '.codex-plugin/mcp.json': '{}',
            'mcp.json': '{}',
            'ui/dist/adapter.mjs': 'export {};',
            'ui/dist/editor/panel.html': '<html></html>',
        }
        locked = {'panel.html': hashlib.sha256(files['ui/dist/editor/panel.html'].encode()).hexdigest()}
        files['ui/editor.lock.json'] = json.dumps({'files': locked})
        if missing:
            del files[missing]
        archive = root / 'candidate.zip'
        with zipfile.ZipFile(archive, 'w') as z:
            for name, value in files.items():
                z.writestr('photocraft-plugin/' + name, value)
            for name, value in (extra or {}).items():
                z.writestr(name, value)
        return archive

    def test_unicode_and_space_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            package = extract_package(self.make_archive(root), root / '中文 插件', 'photocraft')
            self.assertTrue((package / 'ui/dist/adapter.mjs').is_file())

    def test_missing_runtime_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaisesRegex(ValueError, 'adapter'):
                extract_package(self.make_archive(root, missing='ui/dist/adapter.mjs'), root / 'out', 'photocraft')

    def test_corrupt_locked_resource_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            archive = self.make_archive(root, missing='ui/dist/editor/panel.html')
            with self.assertRaisesRegex(ValueError, 'locked resource'):
                extract_package(archive, root / 'out', 'photocraft')

    def test_windows_unsafe_names_fail(self):
        for name in ['../outside', 'photocraft-plugin/..\\outside', 'photocraft-plugin/CON.txt',
                     'photocraft-plugin/asset:stream', 'photocraft-plugin/trailing.']:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                with self.assertRaises(ValueError):
                    extract_package(self.make_archive(root, {name: 'bad'}), root / 'out', 'photocraft')

    def test_case_collisions_fail_on_every_platform(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaisesRegex(ValueError, 'collision'):
                extract_package(self.make_archive(root, {'photocraft-plugin/PLUGIN.json': '{}'}), root / 'out', 'photocraft')


if __name__ == '__main__':
    unittest.main()
