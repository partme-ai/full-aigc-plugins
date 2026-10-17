"""文档门禁拒绝过期矩阵、失配证据和未经验证的能力升级。"""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
class CurrentCapabilityTests(unittest.TestCase):
 def test_public_docs_gate_checks_current_matrix(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp)/'repo';shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','.codegraph','__pycache__'))
   def validate():return subprocess.run([sys.executable,'-I','-B',str(root/'scripts/validate_docs.py')],capture_output=True,text=True)
   r=validate();self.assertEqual(r.returncode,0,r.stdout+r.stderr)
   matrix=root/'docs/current-capabilities.json';proof=root/'docs/evidence/current-capability-evidence.json';report=root/json.loads(proof.read_text())['reportFile']
   cases=[(matrix,lambda v:v['web'].update(installation='PASS')),(matrix,lambda v:v['evidenceBinding'].update(sha256='0'*64)),(matrix,lambda v:v['platforms'][0].update(runtime='0.0.0')),(matrix,lambda v:v['platforms'][-1].update(nativeRepresentative='PASS')),(proof,lambda v:v.update(reportFile='docs/evidence/missing-capability-report.json')),(matrix,lambda v:v['platforms'][0].update(completePlatformAcceptance='PASS')),(matrix,lambda v:v['platforms'][0].update(runtimeMinimum={}))]
   for index,(path,change) in enumerate(cases):
    with self.subTest(index=index):
     original=path.read_bytes();v=json.loads(original);change(v);path.write_text(json.dumps(v));r=validate();self.assertEqual(r.returncode,1,r.stdout+r.stderr);self.assertIn('current capability',r.stdout);path.write_bytes(original)
   # 历史报告已不覆盖当前载荷时，篡改旧状态不能支持提升为当前通过。
   original_matrix=matrix.read_bytes();original_report=report.read_bytes()
   v=json.loads(original_matrix);v['evidenceBinding']['current']=True;matrix.write_text(json.dumps(v))
   v=json.loads(original_report);v['status']='FAIL';report.write_text(json.dumps(v))
   r=validate();self.assertEqual(r.returncode,1,r.stdout+r.stderr);self.assertIn('current capability',r.stdout)
   matrix.write_bytes(original_matrix);report.write_bytes(original_report)
