"""移动交付包必须保留完整资产身份并拒绝危险或不完整输入。"""
import hashlib,importlib.util,json,tempfile,unittest,subprocess,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def module():
 path=ROOT/'scripts/mobile_delivery.py';spec=importlib.util.spec_from_file_location('mobile_delivery',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class MobileDelivery(unittest.TestCase):
 def fixture(self,root):
  source=root/'source';source.mkdir();file=source/'photo.png';file.write_bytes(b'\x89PNG\r\n\x1a\nfixture');sha=hashlib.sha256(file.read_bytes()).hexdigest()
  artifact={'protocolVersion':'craft-artifact/v1','assetId':'photo','version':sha,'sha256':sha,'bytes':file.stat().st_size,'mediaType':'image/png','producerTaskId':'fixture','sourceRefs':[],'nativeProjectRef':None,'renditions':[],'dependencies':[],'technicalMetadata':{},'lossReportRef':None,'evidenceRefs':[],'location':'photo.png'}
  report=source/'report.json';report.write_text(json.dumps({'status':'PASS','root':str(source),'artifacts':[artifact]}));return source,report,hashlib.sha256(report.read_bytes()).hexdigest()
 def test_roundtrip_preserves_source_and_has_no_device_claim(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);source,report,sha=self.fixture(root);m=module();before={p.name:p.read_bytes() for p in source.iterdir()};result=m.prepare(root/'bundle',report,sha)
   self.assertEqual(m.inspect(root/'bundle')['identity'],'PASS');self.assertEqual(result['deviceAcceptance'],'NOT_RUN');self.assertEqual(before,{p.name:p.read_bytes() for p in source.iterdir()})
 def test_rejects_source_identity_drift_and_existing_target(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);_,report,sha=self.fixture(root);m=module()
   with self.assertRaisesRegex(ValueError,'source_report_identity'):m.prepare(root/'out',report,'0'*64)
   (root/'out').mkdir()
   with self.assertRaisesRegex(ValueError,'new_output_required'):m.prepare(root/'out',report,sha)
 def test_rejects_traversal_symlink_and_missing_project(self):
  for case in ('traversal','symlink','project'):
   with self.subTest(case=case),tempfile.TemporaryDirectory() as td:
    root=Path(td);source,report,sha=self.fixture(root);m=module();d=json.loads(report.read_text());a=d['artifacts'][0]
    if case=='traversal':a['location']='../photo.png'
    if case=='symlink':file=source/'photo.png';file.rename(source/'real.png');file.symlink_to(source/'real.png')
    if case=='project':a['nativeProjectRef']={'assetId':'project','version':'1','sha256':'0'*64,'location':'absent.designcraft'}
    report.write_text(json.dumps(d));sha=hashlib.sha256(report.read_bytes()).hexdigest()
    with self.assertRaises((ValueError,FileNotFoundError)):m.prepare(root/'out',report,sha)
    self.assertFalse((root/'out').exists())
 def test_changed_received_file_or_extra_file_rejected(self):
  for case in ('changed','extra'):
   with self.subTest(case=case),tempfile.TemporaryDirectory() as td:
    root=Path(td);_,report,sha=self.fixture(root);m=module();m.prepare(root/'out',report,sha)
    (root/'out'/('photo.png' if case=='changed' else 'unlisted.txt')).write_bytes(b'changed')
    with self.assertRaisesRegex(ValueError,'identity|inventory'):m.inspect(root/'out')

 def test_explicit_controller_prepare_and_inspect(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);_,report,sha=self.fixture(root);payload=root/'payload.json';payload.write_text(json.dumps({'report':str(report),'report_sha256':sha}));bundle=root/'bundle'
   result=subprocess.run([sys.executable,'-I','-B',str(ROOT/'scripts/controller.py'),'mobile-prepare',str(bundle),'--payload',str(payload)],capture_output=True,text=True)
   self.assertEqual(result.returncode,0,result.stdout+result.stderr)
   result=subprocess.run([sys.executable,'-I','-B',str(ROOT/'scripts/controller.py'),'mobile-inspect',str(bundle)],capture_output=True,text=True)
   self.assertEqual(result.returncode,0,result.stdout+result.stderr);self.assertEqual(json.loads(result.stdout)['deviceAcceptance'],'NOT_RUN')

 @unittest.skipUnless(hasattr(os,'mkfifo'),'POSIX FIFO required')
 def test_unlisted_special_file_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td);_,report,sha=self.fixture(root);m=module();m.prepare(root/'out',report,sha);os.mkfifo(root/'out/extra.pipe')
   with self.assertRaisesRegex(ValueError,'inventory'):m.inspect(root/'out')
