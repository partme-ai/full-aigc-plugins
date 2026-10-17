"""历史几何驱动必须绑定原字节，不能要求旧运行匹配后续QA实现。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
REPORT='docs/evidence/vectorcraft-geometry-fixed51-20261009.json'
DRIVER='scripts/qa/geometry_fixed.ts'
VERIFIER=ROOT/'scripts/verify_geometry_evidence.py'
class GeometryDriverEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name).resolve()
        self.report=json.loads((ROOT/REPORT).read_text());index=json.loads((ROOT/'docs/evidence-index.json').read_text())
        self.dependencies=next(e['dependencies'] for e in index['entries'] if e['path']==REPORT)
        names=set(self.report['fingerprints'])|{REPORT,'docs/evidence-index.json','openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md'}
        for name in names:
            original=ROOT/name;expected=self.report['fingerprints'].get(name)
            if expected and (not original.is_file() or hashlib.sha256(original.read_bytes()).hexdigest()!=expected):
                # harness 归位/收敛归档：依赖键可能是字节等价映射后的路径。
                aliases=[name]+(['scripts/harness/'+name.split('src/harness/',1)[1]] if name.startswith('src/harness/') else [])
                original=ROOT/next(p for p,h in self.dependencies.items() if h==expected and any(p.endswith('/'+a) or p==a for a in aliases))
            target=self.root/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original,target)
        archived=next(p for p,h in self.dependencies.items() if h==self.report['fingerprints'][DRIVER] and p.endswith('/'+DRIVER))
        target=self.root/archived;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/archived,target)
        shutil.copyfile(ROOT/DRIVER,self.root/DRIVER)
        spec=importlib.util.spec_from_file_location('geometry_driver_verify',VERIFIER);self.module=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.module);self.module.ROOT=self.root
    def test_original_driver_remains_valid_after_candidate_driver_changes(self):
        self.module.main()
    def test_rehashed_native_report_cannot_forge_the_driver_identity(self):
        name='docs/evidence/vc-dm-001/native.json';path=self.root/name;value=json.loads(path.read_text());value['driverSha256']='0'*64;path.write_text(json.dumps(value));self.report['fingerprints'][name]=hashlib.sha256(path.read_bytes()).hexdigest();(self.root/REPORT).write_text(json.dumps(self.report))
        with self.assertRaisesRegex(ValueError,'qa_driver_drift'):self.module.main()
if __name__=='__main__':unittest.main()
