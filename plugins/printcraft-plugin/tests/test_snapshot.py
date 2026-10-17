"""本地插件快照合同。"""
import importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class SnapshotContract(unittest.TestCase):
    def test_self_contained_snapshot_and_unpublished_identity(self):
        p=ROOT/'scripts/validate_package.py';spec=importlib.util.spec_from_file_location('validator',p)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        self.assertEqual(module.validate()['upstreamSkills'],6)
if __name__=='__main__':unittest.main()
