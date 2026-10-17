"""交换验收必须拒绝重新散列后的缺失原生保全、故障用例与场景。"""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]

def payload_source(name):
    """执行载荷收敛在 vectorcraft-harness：沙箱复制的 skills/<domain>/scripts/ 源按字节等价映射。"""
    if isinstance(name, str):
        prefix = 'skills/vectorcraft-'
        if name.startswith(prefix) and '/scripts/' in name and not (ROOT/name).is_file():
            candidate = 'skills/vectorcraft-harness/scripts/' + name.split('/scripts/', 1)[1]
            if (ROOT/candidate).is_file():
                return candidate
    return name

REPORT='docs/evidence/vectorcraft-exchange-qualified55-20261009.json'
class ExchangeEvidenceTests(unittest.TestCase):
    def setUp(self):
        spec=importlib.util.spec_from_file_location('exchange_verify_fixture',ROOT/'scripts/verify_exchange_evidence.py')
        self.module=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.module)
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.report=json.loads((ROOT/REPORT).read_text())
        index=json.loads((ROOT/'docs/evidence-index.json').read_text())
        dependencies=next(e['dependencies'] for e in index['entries'] if e['path']==REPORT)
        for name in set(self.report['fingerprints'])|set(dependencies)|{REPORT,'docs/evidence-index.json'}:
            target=self.root/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/payload_source(name),target)
        self.module.ROOT=self.root
    def write(self,name,data):
        p=self.root/name;p.write_text(json.dumps(data));self.report['fingerprints'][name]=self.module.sha(p)
        (self.root/REPORT).write_text(json.dumps(self.report))
    def run_verify(self):
        with contextlib.redirect_stdout(io.StringIO()):self.module.main()
    def test_current_evidence_passes(self):self.run_verify()
    def test_preservation_false_rejected_after_rehash(self):
        name=self.report['native'];data=json.loads((self.root/name).read_text());data['sourceAndPreviousExportsPreserved']=False;self.write(name,data)
        with self.assertRaisesRegex(ValueError,'native_preservation'):self.run_verify()
    def test_missing_scenario_rejected_after_rehash(self):
        name=self.report['scenarioMatrix'];data=json.loads((self.root/name).read_text());data['entries'].pop();self.write(name,data)
        with self.assertRaisesRegex(ValueError,'scenario_coverage'):self.run_verify()
    def test_missing_refusal_rejected_after_rehash(self):
        name=self.report['native'];data=json.loads((self.root/name).read_text());data['refusals'].pop();self.write(name,data)
        with self.assertRaisesRegex(ValueError,'missing_refusal'):self.run_verify()
    def test_unblocked_lossless_claim_rejected_after_rehash(self):
        name=self.report['native'];data=json.loads((self.root/name).read_text());row=next(x for x in data['lossReport']['outputs'] if x['format']=='svg');row['observations']['rasterizationScope']['losslessVectorClaimAllowed']=True;self.write(name,data)
        with self.assertRaisesRegex(ValueError,'raster_disclosure'):self.run_verify()
    def test_host_digest_rejected_after_rehash(self):
        name=self.report['host'];data=json.loads((self.root/name).read_text());data['skills'][0]['sha256']='0'*64;self.write(name,data)
        with self.assertRaisesRegex(ValueError,'host_identity'):self.run_verify()
