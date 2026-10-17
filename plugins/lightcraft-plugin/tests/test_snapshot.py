"""本地插件快照合同。"""
import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class SnapshotContract(unittest.TestCase):
    def test_self_contained_snapshot_and_unpublished_identity(self):
        p=ROOT/'scripts/validate_package.py';spec=importlib.util.spec_from_file_location('validator',p)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        result=module.validate()
        self.assertEqual(result['skills'],len([p for p in (ROOT/'skills').iterdir() if p.is_dir()]))
        self.assertEqual(len(json.loads((ROOT/'candidate-source.json').read_text())['managedSkills']),6)
if __name__=='__main__':unittest.main()
