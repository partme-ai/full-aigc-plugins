"""公开交付校验必须验证血缘语义，历史清单不能被提升为血缘通过。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
def load(path):
 spec=importlib.util.spec_from_file_location('lineage_quality',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class LineageQualityTests(unittest.TestCase):
 def fixture(self,root):
  for name,data in {'project.vectorcraft':b'native','plan.json':b'{}','preview.png':b'unit decode fixture'}.items():(root/name).write_bytes(data)
  files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in root.iterdir()}
  version=hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
  logical='vectorcraft:00000000-0000-4000-8000-000000000001'
  parent={'status':'creation','projectSha256':None}
  r={'schema':'vectorcraft-artifact-lineage/v1','logicalId':logical,'version':version,'sourceTask':{'id':'test-task','scope':'workflow-execution','planSha256':files['plan.json']},'files':files.copy(),'native':{'path':'project.vectorcraft','sha256':files['project.vectorcraft']},'assets':{},'outputs':[{'path':'preview.png','sha256':files['preview.png']}],'parent':parent}
  (root/'lineage.json').write_text(json.dumps(r));files['lineage.json']=hashlib.sha256((root/'lineage.json').read_bytes()).hexdigest()
  m={'schema':'vectorcraft-delivery/v1','runtimeSha256':'a'*64,'files':files,'outputs':[{'path':'preview.png'}],'assets':{},'sourceProjectSha256':None,'executionId':'test-task','lineage':{'path':'lineage.json','sha256':files['lineage.json'],'logicalId':logical,'version':version,'parent':parent}}
  return m,r
 def check(self,root,m):
  (root/'manifest.json').write_text(json.dumps(m));return load(ROOT/'src/evaluation/delivery_quality.py').check_delivery(root,'a'*64,m['files']['project.vectorcraft'],decoder=lambda p:{'status':'PASS','scope':'unit fixture only'})
 def test_readonly_check_does_not_write_skill_cache(self):
  module=load(ROOT/'src/evaluation/delivery_quality.py')
  import sys
  original=sys.dont_write_bytecode
  try:
   sys.dont_write_bytecode=False
   before={p.relative_to(ROOT/'skills').as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'skills').rglob('*') if p.is_file()}
   with tempfile.TemporaryDirectory() as d:
    root=Path(d);manifest,record=self.fixture(root);self.check(root,manifest)
   after={p.relative_to(ROOT/'skills').as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'skills').rglob('*') if p.is_file()}
   self.assertEqual(before,after)
  finally:sys.dont_write_bytecode=original
 def test_current_lineage_is_verified(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);m,r=self.fixture(root);self.assertEqual(self.check(root,m)['lineageStatus'],'PASS')
 def test_legacy_package_is_not_lineage_pass(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);m,r=self.fixture(root);m.pop('lineage');m['files'].pop('lineage.json');(root/'lineage.json').unlink()
   self.assertEqual(self.check(root,m)['lineageStatus'],'NOT_RUN')
 def test_rehashed_semantic_faults_block_before_decoding(self):
  for fault in ['task','native','outputs','version','dependencies']:
   with self.subTest(fault=fault),tempfile.TemporaryDirectory() as d:
    root=Path(d);m,r=self.fixture(root)
    if fault=='task':r['sourceTask']['id']='forged'
    elif fault=='native':r['native']['sha256']='0'*64
    elif fault=='outputs':r['outputs']=[]
    elif fault=='version':r['version']='0'*64
    else:r['assets']={'missing':{'path':'assets/missing.svg','sha256':'0'*64}}
    (root/'lineage.json').write_text(json.dumps(r));m['files']['lineage.json']=hashlib.sha256((root/'lineage.json').read_bytes()).hexdigest();m['lineage']['sha256']=m['files']['lineage.json']
    result=self.check(root,m);self.assertEqual(result['artifactIntegrityStatus'],'FAIL');self.assertEqual(result['outputs'],[])
if __name__=='__main__':unittest.main()
