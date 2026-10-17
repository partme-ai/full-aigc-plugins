"""用临时本地 Git 来源验证发行检查入口；不联网、不发布或安装。"""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ReleaseValidationCli(unittest.TestCase):
    def fixture(self, directory):
        package = directory / 'plugin'
        shutil.copytree(ROOT, package, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        source = directory / 'source'; source.mkdir()
        shutil.copytree(package / 'skills', source / 'skills')
        suite = json.loads((package / 'source-suite.json').read_text())
        (source / 'skill-suite.json').write_text(json.dumps(suite))
        def git(*args):
            return subprocess.check_output(['git', '-C', str(source), *args], text=True).strip()
        git('init', '--quiet')
        git('add', '.')
        git('-c', 'user.name=Lightcraft test', '-c', 'user.email=test@example.invalid', 'commit', '--quiet', '--no-gpg-sign', '-m', 'fixture')
        commit = git('rev-parse', 'HEAD'); tag = 'v' + suite['version']; git('tag', tag)
        path = package / 'candidate-source.json'; lock = json.loads(path.read_text())
        lock.update(sourceStatus='published-immutable-release', repository='https://github.com/full-aigc-skills/lightcraft-skills', releaseTag=tag, commit=commit)
        path.write_text(json.dumps(lock))
        return package, source, tag

    def test_cli_accepts_explicit_source_git_and_checks_real_tag_blobs(self):
        with tempfile.TemporaryDirectory() as temporary:
            package, source, tag = self.fixture(Path(temporary))
            result = subprocess.run([sys.executable, '-I', '-B', str(package/'scripts/validate_package.py'), '--source-git', str(source)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['sourceRelease'], tag)

    def test_ci_environment_source_is_available_to_function_entry(self):
        with tempfile.TemporaryDirectory() as temporary:
            package, source, tag = self.fixture(Path(temporary))
            code = "import importlib.util; from pathlib import Path; p=Path('scripts/validate_package.py'); s=importlib.util.spec_from_file_location('v',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);print(m.validate()['sourceRelease'])"
            result = subprocess.run([sys.executable, '-I', '-B', '-c', code], cwd=package, env=dict(os.environ, LIGHTCRAFT_SOURCE_GIT=str(source)), capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), tag)

    def test_release_gate_forwards_source_git_without_bypassing_other_layers(self):
        with tempfile.TemporaryDirectory() as temporary:
            package, source, _ = self.fixture(Path(temporary))
            p = package/'scripts/verify_evidence.py'; spec=importlib.util.spec_from_file_location('e',p); e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
            report={'schemaVersion':1,'sourceFingerprint':e.fingerprint(package),'layers':{name:{'status':'NOT_RUN'} for name in ('structure','mock','native','host','visual','platform','remoteCI')}}
            path=package/'test-report.json';path.write_text(json.dumps(report))
            result=subprocess.run([sys.executable,'-I','-B',str(package/'scripts/release_preflight.py'),str(path),'--source-git',str(source)],capture_output=True,text=True)
            self.assertEqual(result.returncode,1)
            self.assertIn('host',json.loads(result.stdout)['missing'])


if __name__ == '__main__':
    unittest.main()
