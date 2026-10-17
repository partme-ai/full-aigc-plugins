"""插件 RAW 观察器拒绝伪造完整解码、漂移身份与重复会话。"""
import hashlib
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
def api():
 spec=importlib.util.spec_from_file_location('raw_facts',ROOT/'scripts/raw_facts.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class RawFacts(unittest.TestCase):
 def test_legacy_report_is_readonly_and_cannot_execute(self):
  with tempfile.TemporaryDirectory() as temp:
   path=Path(temp)/'old.json';path.write_text('{"schemaVersion":1,"samples":[]}');before=path.read_bytes();result=api().inspect_raw(path)
   self.assertFalse(result['compatible']);self.assertFalse(result['deliveryAllowed']);self.assertEqual(before,path.read_bytes())
 def test_changed_manifest_or_missing_native_identity_rejected(self):
  for report in [{'schemaVersion':1,'reportKind':'raw-samples','manifest':{'schemaVersion':1,'samples':[]},'manifestSha256':'0'*64},
                 {'schemaVersion':1,'reportKind':'raw-samples','manifest':{'schemaVersion':1,'samples':[]},'manifestSha256':api().digest({'schemaVersion':1,'samples':[]})}]:
   with tempfile.TemporaryDirectory() as temp:
    path=Path(temp)/'report.json';path.write_text(json.dumps(report))
    with self.assertRaises(ValueError):api().inspect_raw(path)
 def test_decode_boolean_cannot_be_promoted_to_full_raw(self):
  m=api()
  for photo in [{'kind':'raw','previewOnly':False},{'kind':'image','previewOnly':None},{'kind':'raw'}]:self.assertEqual(m.decode_mode(photo),'UNKNOWN')
  self.assertEqual(m.decode_mode({'kind':'raw','previewOnly':'Canon sRAW/mRAW'}),'PREVIEW_FALLBACK')
 def test_camera_model_mismatch_is_not_same_brand_support(self):
  self.assertTrue(api().camera_matches({'make':'Nikon','model':'D2H'},'NIKON CORPORATION NIKON D2H'))
  self.assertFalse(api().camera_matches({'make':'Nikon','model':'D2H'},'NIKON D2X'))
 def test_controller_exposes_readonly_action(self):
  with tempfile.TemporaryDirectory() as temp:
   path=Path(temp)/'old.json';path.write_text('{"schemaVersion":1,"samples":[]}');before=path.read_bytes()
   result=subprocess.run([sys.executable,'-I','-B',str(ROOT/'scripts/controller.py'),'raw-inspect',str(path)],capture_output=True,text=True)
   self.assertEqual(result.returncode,0,result.stderr);self.assertFalse(json.loads(result.stdout)['deliveryAllowed']);self.assertEqual(before,path.read_bytes())


 def fixture(self,root,preview=False):
  root=root.resolve();m=api();gateway=m.module('command_gateway');resources=gateway.capture_resources(ROOT/'skills/lightcraft-use/scripts');lock=json.loads((ROOT/'skills/lightcraft-use/scripts/runtime.lock.json').read_text());source=root/'unit.nef';source.write_bytes(b'unit RAW fixture only');exports=root/'exports';exports.mkdir();candidate=exports/'unit.png';candidate.write_bytes(b'mock decoded PNG');settings={'light':{'exposure':.25}};photo={'id':1,'source':{'type':'file','path':str(source)},'develop':settings}
  sample={'sampleId':'unit-raw','make':'Nikon','model':'D2H','variant':'12bit compressed','license':'CC0-1.0','licenseUrl':'https://creativecommons.org/publicdomain/zero/1.0/','sourceUrl':'https://raw.pixls.us/unit.nef','catalogUrl':'https://raw.pixls.us/','path':str(source),'bytes':source.stat().st_size,'sha256':gateway.file_sha(source)}
  def step(command,**params):return {'command':command,'params':params}
  plans={'import':{'domain':'lightcraft','steps':[step('library.import',paths=[str(source)],mode='add'),step('catalog.query',limit=10)]},
   'edit-export':{'domain':'lightcraft','steps':[step('library.select',ids=[1],active=1),step('develop.set',control='light.exposure',value=.25),step('develop.get',id=1),step('app.export',path=str(candidate),format='png',width=256),step('catalog.query',limit=10),step('photo.inspect',id=1)]},
   'reopen':{'domain':'lightcraft','steps':[step('library.select',ids=[1],active=1),step('photo.inspect',id=1),step('develop.get',id=1),step('library.info')]}}
  values={'import':[{'imported':[1],'duplicates':[],'failed':[]},{}],'edit-export':[{}, {},settings,{}, {'photos':[{'id':1,'kind':'raw','previewOnly':'unsupported compression' if preview else None,'camera':'Nikon D2H'}]},photo], 'reopen':[{},photo,settings,{'persistent':True,'unsavedOps':0}]}
  native={'version':lock['resolvedVersion'],'binarySha256':next(iter(lock['artifacts'].values()))['binarySha256'],'mode':'Headless'};paths={}
  for name,plan in plans.items():
   receipt={'schemaVersion':1,'domain':'lightcraft','runId':'unit-'+name,'status':'NATIVE_EXIT_ZERO_REVIEW_REQUIRED','protocolComplete':True,'startedAt':'unit-fixture',
    'planSha256':m.digest(plan),'runtimeLockSha256':resources['runtime.lock.json'],'skillResourceSha256':resources,'skillResourceAfterSha256':resources,'inputSha256':{str(source):sample['sha256']},'inputAfterSha256':{str(source):sample['sha256']},'libraryPath':str(root/'library'),'outputRoot':str(exports),'runtimeIdentity':native,'process':{'status':'EXITED','exitCode':0,'logComplete':True},'automaticReplay':False,'completeAcceptance':False,
    'steps':[{'index':i,'command':step['command'],'status':'SUCCEEDED','native':{'result':value}} for i,(step,value) in enumerate(zip(plan['steps'],values[name]))]}
   path=root/(name+'.json');path.write_text(json.dumps(receipt));paths[name]=str(path)
  record=dict(sample,nativeAcceptance='PASS_WITH_PREVIEW_FALLBACK' if preview else 'PASS',decodeMode='PREVIEW_FALLBACK' if preview else 'FULL_RAW_REPORTED',fullRawAcceptance='NOT_PROVEN' if preview else 'REPORTED_BY_RUNTIME',cameraIdentity='MATCH',observedCamera='Nikon D2H',photoId=1,plans=plans,receipts=paths,artifact={'path':str(candidate),'sha256':gateway.file_sha(candidate),'technicalStatus':'PASS'})
  manifest={'schemaVersion':1,'samples':[sample]};report={'schemaVersion':1,'reportKind':'raw-samples','manifest':manifest,'manifestSha256':m.digest(manifest),'executionResourceSha256':resources,'runtimeIdentity':native,'samples':[record]};path=root/'report.json';path.write_text(json.dumps(report))
  original_module=m.module
  def modules(name):return SimpleNamespace(sha=gateway.file_sha,verify=lambda *a,**k:{'technicalStatus':'PASS'}) if name=='artifacts' else original_module(name)
  return m,path,report,modules

 def test_actual_receipt_shape_cannot_promote_preview_to_full(self):
  with tempfile.TemporaryDirectory() as temp:
   m,path,report,modules=self.fixture(Path(temp),preview=True)
   with patch.object(m,'module',side_effect=modules):
    result=m.inspect_raw(path);self.assertFalse(result['deliveryAllowed']);self.assertTrue(result['sourceSnapshotMatches'])
    report['samples'][0].update(nativeAcceptance='PASS',decodeMode='FULL_RAW_REPORTED',fullRawAcceptance='REPORTED_BY_RUNTIME');path.write_text(json.dumps(report))
    with self.assertRaisesRegex(ValueError,'decode_claim'):m.inspect_raw(path)

 def test_resource_and_reopen_settings_changes_refuse_support_claim(self):
  for fault in ['resource','reopen','session','artifact','process']:
   with self.subTest(fault=fault),tempfile.TemporaryDirectory() as temp:
    m,path,report,modules=self.fixture(Path(temp));record=report['samples'][0];receipt_path=Path(record['receipts']['reopen']);receipt=json.loads(receipt_path.read_text())
    if fault=='resource':receipt['skillResourceAfterSha256']={}
    elif fault=='reopen':receipt['steps'][2]['native']['result']={'light':{'exposure':0}}
    elif fault=='session':receipt['runId']='unit-import'
    elif fault=='artifact':Path(record['artifact']['path']).write_bytes(b'changed')
    elif fault=='process':receipt['process']['logComplete']=False
    receipt_path.write_text(json.dumps(receipt))
    with patch.object(m,'module',side_effect=modules),self.assertRaises(ValueError):m.inspect_raw(path)

 def test_wrong_photo_getter_cannot_be_verified_as_target_settings(self):
  with tempfile.TemporaryDirectory() as temp:
   m,path,report,modules=self.fixture(Path(temp));record=report['samples'][0];record['plans']['edit-export']['steps'][2]['params']['id']=2
   receipt_path=Path(record['receipts']['edit-export']);receipt=json.loads(receipt_path.read_text());receipt['planSha256']=m.digest(record['plans']['edit-export']);receipt_path.write_text(json.dumps(receipt));path.write_text(json.dumps(report))
   with patch.object(m,'module',side_effect=modules),self.assertRaisesRegex(ValueError,'plan_parameters'):m.inspect_raw(path)


 def test_camera_variant_cannot_change_even_if_manifest_hash_is_recomputed(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp).resolve();m,path,report,modules=self.fixture(root);sample=report['manifest']['samples'][0]
   data=[sample['make'],sample['model'],sample['variant'],0,'',sample['licenseUrl'],'',sample['sourceUrl']+' '+sample['sha256']]
   entry=root/'entry.json';entry.write_text(json.dumps(data));sample.update(catalogEntryPath=str(entry),catalogEntrySha256=m.digest(data));report['samples'][0].update(sample)
   sample['variant']='14bit lossless';report['samples'][0]['variant']=sample['variant'];report['manifestSha256']=m.digest(report['manifest']);path.write_text(json.dumps(report))
   with patch.object(m,'module',side_effect=modules),self.assertRaisesRegex(ValueError,'catalog_metadata'):m.inspect_raw(path)

if __name__=='__main__':unittest.main()
