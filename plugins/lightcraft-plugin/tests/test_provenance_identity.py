"""来源身份不能仅由文件摘要代替。"""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import subprocess

ROOT = Path(__file__).resolve().parents[1]


class ProvenanceIdentity(unittest.TestCase):
    def provenance(self):
        spec=importlib.util.spec_from_file_location('provenance',ROOT/'scripts/provenance.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        return module

    def test_published_tag_must_resolve_to_expected_commit(self):
        with tempfile.TemporaryDirectory() as temporary:
            target=Path(temporary)/'plugin';shutil.copytree(ROOT,target)
            path=target/'candidate-source.json';lock=json.loads(path.read_text())
            version=lock['sourceVersion']
            lock.update(sourceStatus='published-immutable-release',releaseTag='v'+version,commit='a'*40,repository='https://github.com/full-aigc-skills/lightcraft-skills')
            path.write_text(json.dumps(lock));module=self.provenance()
            with patch.object(module.subprocess,'run',return_value=subprocess.CompletedProcess([],0,'b'*40+'\n','')):
                with self.assertRaisesRegex(ValueError,'tag_commit_mismatch'):module.validate(target,Path(temporary)/'source')

    def test_extra_skill_and_file_are_refused(self):
        for extra in ['lightcraft-other/SKILL.md','lightcraft-use/extra.txt']:
            with self.subTest(extra=extra),tempfile.TemporaryDirectory() as temporary:
                target=Path(temporary)/'plugin';shutil.copytree(ROOT,target)
                path=target/'skills'/extra;path.parent.mkdir(exist_ok=True);path.write_text('unexpected')
                with self.assertRaises(ValueError):self.provenance().validate(target)

    def test_candidate_identity_mismatch_is_refused(self):
        for field, value in [('releaseTag', 'v0.1.0'), ('sourceProject', 'foreign-skills'), ('sourceVersion', '99.0.0')]:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary:
                target = Path(temporary) / 'plugin'
                shutil.copytree(ROOT, target)
                path = target / 'candidate-source.json'
                lock = json.loads(path.read_text())
                lock[field] = value
                path.write_text(json.dumps(lock))
                spec = importlib.util.spec_from_file_location('validator', target / 'scripts/validate_package.py')
                validator = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(validator)
                with self.assertRaises(ValueError):
                    validator.validate()


if __name__ == '__main__':
    unittest.main()
