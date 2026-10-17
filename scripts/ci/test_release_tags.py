"""公开ZIP正确不能替代Git发行标签与期望提交一致。"""
import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location('release_zip_verifier',Path(__file__).resolve().parents[1]/'verify-craft-release-zip.py')
verifier=importlib.util.module_from_spec(spec);spec.loader.exec_module(verifier)
class ReleaseTagTests(unittest.TestCase):
    def test_lightweight_tag(self):
        sha='a'*40
        self.assertEqual(verifier.checked_tag_commit(sha+'\trefs/tags/v1.2.3\n','1.2.3',sha),sha)
    def test_annotated_tag_uses_peeled_commit(self):
        sha='a'*40
        data='b'*40+'\trefs/tags/v1.2.3\r\n'+sha+'\trefs/tags/v1.2.3^{}\r\n'
        self.assertEqual(verifier.checked_tag_commit(data,'1.2.3',sha),sha)
    def test_existing_wrong_tag_rejected(self):
        with self.assertRaisesRegex(ValueError,'commit differs'):
            verifier.checked_tag_commit('b'*40+'\trefs/tags/v1.2.3\n','1.2.3','a'*40)
    def test_missing_tag_rejected(self):
        with self.assertRaisesRegex(ValueError,'absent'):
            verifier.checked_tag_commit('','1.2.3','a'*40)
if __name__=='__main__':unittest.main()
