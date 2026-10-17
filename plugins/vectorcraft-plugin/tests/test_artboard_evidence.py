"""证明画板验收校验器不会接受重新散列后的缺失场景或原生用例。"""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

def payload_source(name):
    """执行载荷收敛在 vectorcraft-harness：沙箱复制的 skills/<domain>/scripts/ 源按字节等价映射。"""
    if isinstance(name, str):
        prefix = 'skills/vectorcraft-'
        if name.startswith(prefix) and '/scripts/' in name and not (ROOT/name).is_file():
            candidate = 'skills/vectorcraft-harness/scripts/' + name.split('/scripts/', 1)[1]
            if (ROOT/candidate).is_file():
                return candidate
    return name

REPORT = 'docs/evidence/vectorcraft-artboards-fixed54-20261009.json'

class ArtboardEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.report = json.loads((ROOT/REPORT).read_text())
        index=json.loads((ROOT/'docs/evidence-index.json').read_text())
        dependencies=next(e['dependencies'] for e in index['entries'] if e['path']==REPORT)
        names = set(self.report['fingerprints']) | set(dependencies) | {REPORT,'docs/evidence-index.json','openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md'}
        for name in names:
            target = self.root/name
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/payload_source(name),target)
        spec = importlib.util.spec_from_file_location('artboard_verify_fixture',ROOT/'scripts/verify_artboard_evidence.py')
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.module.ROOT = self.root
    def write(self,name,value):
        path = self.root/name
        path.write_text(json.dumps(value))
        self.report['fingerprints'][name] = self.module.sha(path)
        (self.root/REPORT).write_text(json.dumps(self.report))
    def test_current_complete_evidence_passes(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.module.main()
    def test_missing_native_case_refused_even_with_fresh_fingerprint(self):
        name = self.report['native']
        native = json.loads((self.root/name).read_text())
        native['cases'].pop()
        self.write(name,native)
        with self.assertRaises(ValueError):
            self.module.main()
    def test_missing_scenario_refused_even_with_fresh_fingerprint(self):
        name = self.report['scenarioMatrix']
        matrix = json.loads((self.root/name).read_text())
        matrix['entries'].pop()
        self.write(name,matrix)
        with self.assertRaisesRegex(ValueError,'scenario_coverage_mismatch'):
            self.module.main()
    def test_changed_native_receipt_refused_even_with_outer_fingerprint(self):
        native = json.loads((self.root/self.report['native']).read_text())
        name = 'docs/evidence/vc-dm-004/'+native['cases'][0]['receipt']
        self.write(name,{'text':'unrelated replacement'})
        with self.assertRaisesRegex(ValueError,'unbound_native_receipt'):
            self.module.main()
    def test_installation_digest_mismatch_refused(self):
        name = self.report['installedIntegrity']
        integrity = json.loads((self.root/name).read_text())
        integrity['digests']['vectorcraft-cli-export'] = '0'*64
        self.write(name,integrity)
        with self.assertRaisesRegex(ValueError,'installed_identity_mismatch'):
            self.module.main()

if __name__ == '__main__':
    unittest.main()
