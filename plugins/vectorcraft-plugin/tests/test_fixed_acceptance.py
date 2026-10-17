"""重新计算摘要不能掩盖固定安装矩阵缺项或实际技能身份不符。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
REPORT='docs/evidence/vectorcraft-fixed38-optimization-20261008.json'
spec=importlib.util.spec_from_file_location('verify_fixed',ROOT/'scripts/acceptance/verify_fixed.py')
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)


class FixedAcceptanceTests(unittest.TestCase):
    def fixture(self,root):
        report=json.loads((ROOT/REPORT).read_text())
        for name in {REPORT,*report['fingerprints']}:
            destination=root/name;destination.parent.mkdir(parents=True,exist_ok=True);historical=ROOT/'docs/evidence/fixed38-identity'/name
            shutil.copyfile(historical if historical.is_file() else ROOT/name,destination)
        self.assertEqual(gate.verify(root)['result'],'PASS')
        return report

    def rehash(self,root,report,key,data):
        entry=report['reports'][key];path=root/entry['path'];path.write_text(json.dumps(data))
        digest=hashlib.sha256(path.read_bytes()).hexdigest();entry['sha256']=digest;report['fingerprints'][entry['path']]=digest
        (root/REPORT).write_text(json.dumps(report))

    def test_rehashed_protocol_report_still_requires_all_faults(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);report=self.fixture(root);data=json.loads((root/report['reports']['protocol']['path']).read_text());data['cases'].pop();self.rehash(root,report,'protocol',data)
            with self.assertRaisesRegex(ValueError,'fixed_protocol_incomplete'):gate.verify(root)

    def test_rehashed_skill_identity_drift_cannot_pass(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);report=self.fixture(root);data=json.loads((root/report['reports']['native']['path']).read_text());data['cases'][0]['sha256']='0'*64;self.rehash(root,report,'native',data)
            with self.assertRaisesRegex(ValueError,'fixed_skill_digest_mismatch'):gate.verify(root)

    def test_fixed_release_identity_change_is_not_current_acceptance(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);self.fixture(root);path=root/'plugin.json';manifest=json.loads(path.read_text());manifest['version']='0.1.0-dev.999';path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError,'fixed_identity_mismatch'):gate.verify(root)
