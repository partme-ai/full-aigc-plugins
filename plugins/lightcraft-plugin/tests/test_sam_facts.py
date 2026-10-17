"""SAM 只读观察器不接受伪造成功、身份漂移或缺少事实的报告。"""
import importlib.util
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
def module(name):
 spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class SamFacts(unittest.TestCase):
 def report(self):
  lock=json.loads((ROOT/'skills/lightcraft-use/scripts/runtime.lock.json').read_text());identity={'status':'READY','version':lock['resolvedVersion'],'binarySha256':lock['artifacts']['darwin-arm64']['binarySha256']}
  snapshot={'domain':'lightcraft','mode':'Headless','executionAllowed':True,'executableIdentity':identity,'commands':[]}
  return module('sam_contract').assess(snapshot)
 def inspect(self,data):
  with tempfile.TemporaryDirectory() as temp:
   path=Path(temp)/'report.json';path.write_text(json.dumps(data));return module('sam_facts').inspect_sam(path)
 def test_valid_missing_status_is_unknown_and_readonly(self):
  r=self.inspect(self.report());self.assertEqual(r['compileFeature'],'UNKNOWN');self.assertFalse(r['taskExecutionAllowed']);self.assertFalse(r['downloadAllowed']);self.assertFalse(r['deliveryAllowed'])
 def test_unknown_legacy_is_readonly_incompatible(self):
  r=self.inspect({'schemaVersion':0});self.assertFalse(r['compatible']);self.assertFalse(r['taskExecutionAllowed'])
 def test_promoted_feature_and_authorization_rejected(self):
  for key,value in [('compileFeature','REPORTED_ENABLED'),('authorization',{'download':'GRANTED','execution':'GRANTED'}),('executionAllowed',True),('modelIdentityVerified',True),('blockers',[])]:
   with self.subTest(key=key),self.assertRaises(ValueError):self.inspect(dict(self.report(),**{key:value}))
 def test_manifest_rehash_does_not_allow_replacement(self):
  r=self.report();r['modelManifest']['files'][0]['sha256']='0'*64;r['modelManifestSha256']=module('sam_contract').digest(r['modelManifest'])
  with self.assertRaises(ValueError):self.inspect(r)
 def test_controller_action_is_readonly(self):
  with tempfile.TemporaryDirectory() as temp:
   path=Path(temp)/'report.json';path.write_text(json.dumps(self.report()))
   result=subprocess.run([sys.executable,'-I','-B',str(ROOT/'scripts/controller.py'),'sam-inspect',str(path)],capture_output=True,text=True)
   self.assertEqual(result.returncode,0,result.stdout);self.assertFalse(json.loads(result.stdout)['taskExecutionAllowed'])
 def test_changed_file_facts_are_rejected(self):
  with tempfile.TemporaryDirectory() as temp:
   api=module('sam_contract');data=api.assess(self.report()['snapshot'],model_dir=Path(temp))
   (Path(temp)/'vocab.json').write_bytes(b'not a tokenizer')
   with self.assertRaises(ValueError):self.inspect(data)
 def test_snapshot_identity_and_digest_rejected(self):
  for mutate in ('digest','version','missing'):
   r=self.report()
   if mutate=='digest':r['snapshotSha256']='0'*64
   elif mutate=='version':r['snapshot']['executableIdentity']['version']='0.2.2';r['snapshotSha256']=module('sam_contract').digest(r['snapshot'])
   else:r.pop('snapshot')
   with self.subTest(mutate=mutate),self.assertRaises(ValueError):self.inspect(r)
if __name__=='__main__':unittest.main()
