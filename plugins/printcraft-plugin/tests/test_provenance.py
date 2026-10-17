"""候选来源与清单反向回归；全部修改位于临时包。"""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
class Provenance(unittest.TestCase):
    def test_reject_false_identity_and_invalid_manifest(self):
        cases=[('candidate-source.json','releaseTag','v1.0.0'),('candidate-source.json','sourceProject','other-skills'),('candidate-source.json','sourceVersion','9.9.9'),('plugin.json','version',1),('plugin.json','unknownField',True)]
        for filename,key,value in cases:
            with self.subTest(key=key),tempfile.TemporaryDirectory() as t:
                target=Path(t)/'plugin';shutil.copytree(ROOT,target,ignore=shutil.ignore_patterns('__pycache__','.DS_Store'))
                p=target/filename;data=json.loads(p.read_text());data[key]=value;p.write_text(json.dumps(data))
                spec=importlib.util.spec_from_file_location('validator',target/'scripts/validate_package.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
                with self.assertRaises(ValueError):m.validate()
if __name__=='__main__':unittest.main()

class FormalOfflineIdentity(unittest.TestCase):
    def test_formal_lock_format_never_claims_remote_verification(self):
        with tempfile.TemporaryDirectory() as t:
            target=Path(t)/'plugin';shutil.copytree(ROOT,target,ignore=shutil.ignore_patterns('__pycache__','.DS_Store'))
            path=target/'candidate-source.json';data=json.loads(path.read_text());data.update(sourceStatus='published-release',releaseTag='v'+data['sourceVersion'],sourceCommit='a'*40,sourceRepository='https://github.com/full-aigc-skills/printcraft-skills');path.write_text(json.dumps(data));(target/'source-release.lock.json').write_text(json.dumps({'protocol':'printcraft.source-release/1','source':data,'pluginVersion':json.loads((target/'plugin.json').read_text())['version']}))
            spec=importlib.util.spec_from_file_location('formal_validator',target/'scripts/validate_package.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
            result=m.validate();self.assertEqual(result['sourceRelease'],'OFFLINE_IDENTITY_ONLY_REMOTE_NOT_VERIFIED');self.assertEqual(result['remoteSourceVerification'],'NOT_RUN')
            data['sourceCommit']='not-commit';path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError,'release_identity'):m.validate()

class PublishedSourceLock(unittest.TestCase):
    def test_formal_source_needs_independent_repository_bound_release_lock(self):
        with tempfile.TemporaryDirectory() as t:
            target=Path(t)/'plugin';shutil.copytree(ROOT,target,ignore=shutil.ignore_patterns('__pycache__','.DS_Store','.git'))
            path=target/'candidate-source.json';data=json.loads(path.read_text());data.update(sourceStatus='published-release',releaseTag='v'+data['sourceVersion'],sourceCommit='a'*40,sourceRepository='https://github.com/full-aigc-skills/printcraft-skills');path.write_text(json.dumps(data))
            (target/'source-release.lock.json').unlink(missing_ok=True)
            spec=importlib.util.spec_from_file_location('published_validator',target/'scripts/validate_package.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
            with self.assertRaisesRegex(ValueError,'release_lock_missing'):m.validate()
