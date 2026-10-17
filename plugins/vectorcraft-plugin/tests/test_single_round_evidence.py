"""单轮真实模型证据不能通过刷新外层摘要掩盖语义缺失。"""
import importlib.util
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
REPORT='docs/evidence/vectorcraft-single-round64-20261009.json'
class SingleRoundEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.report=json.loads((ROOT/REPORT).read_text())
        index=json.loads((ROOT/'docs/evidence-index.json').read_text())
        dependencies=next(e['dependencies'] for e in index['entries'] if e['path']==REPORT)
        names=set(self.report['fingerprints'])|{REPORT,'openspec/changes/establish-v1-plugin/specs/quality-review/spec.md'}
        for name in names:
            target=self.root/name;target.parent.mkdir(parents=True,exist_ok=True)
            original=ROOT/name;digest=self.report['fingerprints'].get(name)
            if digest and (not original.is_file() or hashlib.sha256(original.read_bytes()).hexdigest()!=digest):
                aliases=[name]+(['scripts/harness/'+name.split('src/harness/',1)[1]] if name.startswith('src/harness/') else [])
                matches=[ROOT/p for p,h in dependencies.items() if h==digest and any(p.endswith('/'+a) or p==a for a in aliases)]
                if len(matches)!=1:raise AssertionError('missing original single-round execution bytes: '+name)
                original=matches[0]
            shutil.copyfile(original,target)
        spec=importlib.util.spec_from_file_location('single_round_verify',ROOT/'scripts/verify_single_round_evidence.py');self.module=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.module)
    def change(self,key,mutate):
        name=self.report[key];path=self.root/name;data=json.loads(path.read_text());mutate(data);path.write_text(json.dumps(data));self.report['fingerprints'][name]=self.module.sha(path);(self.root/REPORT).write_text(json.dumps(self.report))
    def test_complete_current_single_round_passes(self):
        self.assertEqual(self.module.verify(self.root)['taskClosed'],'9.21')
    def test_rehashed_missing_scenario_refused(self):
        self.change('matrix',lambda x:x['entries'].pop())
        with self.assertRaisesRegex(ValueError,'single_round_scenarios'):self.module.verify(self.root)
    def test_rehashed_fake_scores_refused(self):
        self.change('initialAssessment',lambda x:x.update(scores={k:4 for k in x['scores']}))
        with self.assertRaisesRegex(ValueError,'single_round_receipt_binding'):self.module.verify(self.root)
    def test_rehashed_independence_claim_refused(self):
        self.change('revisedAssessment',lambda x:x['reviewer'].update(independenceEvidence='self-claimed'))
        with self.assertRaisesRegex(ValueError,'single_round_model_binding'):self.module.verify(self.root)
    def test_rehashed_missing_small_preview_refused(self):
        self.change('flow',lambda x:x['revised']['observation']['previews'].pop())
        with self.assertRaisesRegex(ValueError,'single_round_previews'):self.module.verify(self.root)
    def test_rehashed_budget_restart_refused(self):
        self.change('guards',lambda x:x.update(sharedAttempts=0))
        with self.assertRaisesRegex(ValueError,'single_round_rejections'):self.module.verify(self.root)
    def test_rehashed_stagnation_bypass_refused(self):
        self.change('flow',lambda x:x['cycle'].update(state='active'))
        with self.assertRaisesRegex(ValueError,'single_round_stop'):self.module.verify(self.root)
    def test_rehashed_control_text_change_refused(self):
        self.change('afterModel',lambda x:x.update(tampered=True))
        with self.assertRaisesRegex(ValueError,'single_round_native_binding'):self.module.verify(self.root)
if __name__=='__main__':unittest.main()
