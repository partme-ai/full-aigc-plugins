"""交换损失语义不能被重新签署文件摘要或通过解码掩盖。"""
import hashlib,importlib.util,json
from pathlib import Path
import tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
def module():
 spec=importlib.util.spec_from_file_location('exchange_delivery',ROOT/'src/evaluation/delivery_quality.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class ExchangeDeliveryTests(unittest.TestCase):
 def fixture(self,root):
  for name,data in {'project.vectorcraft':b'unit-native','native.json':b'{"layers":[]}','drawing.pdf':b'%PDF-unit-fixture'}.items():(root/name).write_bytes(data)
  sha=lambda name:hashlib.sha256((root/name).read_bytes()).hexdigest()
  report={'schema':'craft-exchange-loss/v1','pluginId':'vectorcraft','native':{'location':'project.vectorcraft','sha256':sha('project.vectorcraft')},'inspection':{'location':'native.json','sha256':sha('native.json')},'acceptance':'technical-observations-only','outputs':[{'location':'drawing.pdf','sha256':sha('drawing.pdf'),'format':'pdf','role':'derivative','nativeSubstitute':False,'changes':[{'code':c,'status':s,'reason':'unit fixture only'} for c,s in [('native-editing-model','lost'),('font-portability','unknown'),('effect-fidelity','unknown'),('vector-structure','unknown')]],'observations':{},'warnings':[]}]}
  manifest={'schema':'vectorcraft-delivery/v1','runtimeSha256':'a'*64,'files':{n:sha(n) for n in ['project.vectorcraft','native.json','drawing.pdf']},'outputs':[{'path':'drawing.pdf'}],'fontDependencies':[]}
  return manifest,report
 def save(self,root,m,r):
  (root/'exchange-loss.json').write_text(json.dumps(r));h=hashlib.sha256((root/'exchange-loss.json').read_bytes()).hexdigest();m['files']['exchange-loss.json']=h;m['lossReport']={'path':'exchange-loss.json','sha256':h};(root/'manifest.json').write_text(json.dumps(m))
 def check(self,root,m):return module().check_delivery(root,'a'*64,m['files']['project.vectorcraft'],decoder=lambda p:{'status':'PASS','scope':'unit decoder only'})
 def test_all_reported_outputs_are_checked_without_claiming_reopen_or_creative(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);m,r=self.fixture(root);self.save(root,m,r);q=self.check(root,m)
   self.assertEqual(q['exchangeStatus'],'PASS');self.assertEqual(q['technicalStatus'],'PASS');self.assertEqual(q['nativeReopenStatus'],'NOT_RUN');self.assertEqual(q['creativeStatus'],'NOT_RUN')
 def test_semantic_report_faults_refuse_before_decode(self):
  for fault in ['native-substitute','native-hash','inspection-hash','output-hash','missing-output','extra-output','false-font-fidelity','missing-effect-loss','wrong-plugin','false-approval','duplicate-code','invalid-state','wrong-format']:
   with self.subTest(fault=fault),tempfile.TemporaryDirectory() as d:
    root=Path(d);m,r=self.fixture(root);row=r['outputs'][0]
    if fault=='native-substitute':row['nativeSubstitute']=True
    elif fault=='native-hash':r['native']['sha256']='0'*64
    elif fault=='inspection-hash':r['inspection']['sha256']='0'*64
    elif fault=='output-hash':row['sha256']='0'*64
    elif fault=='missing-output':r['outputs']=[]
    elif fault=='extra-output':r['outputs'].append(dict(row))
    elif fault=='false-font-fidelity':row['changes'][1]['status']='observed'
    elif fault=='missing-effect-loss':row['changes']=[v for v in row['changes'] if v['code']!='effect-fidelity']
    elif fault=='wrong-plugin':r['pluginId']='other'
    elif fault=='false-approval':r['acceptance']='approved'
    elif fault=='duplicate-code':row['changes'].append(dict(row['changes'][0]))
    elif fault=='invalid-state':row['changes'][0]['status']='PASS'
    else:row['format']='png'
    self.save(root,m,r);q=self.check(root,m);self.assertEqual(q['technicalStatus'],'FAIL');self.assertEqual(q['outputs'],[])
 def test_svg_text_loss_matches_bound_native_mode(self):
  for fault in ['claimed-editable','changed-mode','missing-text-ids']:
   with self.subTest(fault=fault),tempfile.TemporaryDirectory() as d:
    root=Path(d);m,r=self.fixture(root)
    (root/'native.json').write_text(json.dumps({'layers':[{'id':3,'kind':{'type':'text'}}],'setup':{'exportText':'appearance'}}))
    (root/'drawing.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0L1 1"/></svg>')
    m['files'].pop('drawing.pdf');m['files']['drawing.svg']=hashlib.sha256((root/'drawing.svg').read_bytes()).hexdigest();m['files']['native.json']=hashlib.sha256((root/'native.json').read_bytes()).hexdigest();m['outputs']=[{'path':'drawing.svg'}]
    r=module().exchange_module().write_report(root,['drawing.svg'],{}, {'drawing.svg':'appearance'})
    if fault=='claimed-editable':next(v for v in r['outputs'][0]['changes'] if v['code']=='live-text-editability')['status']='observed'
    elif fault=='changed-mode':r['outputs'][0]['observations']['svgTextExportMode']='editable'
    else:r['outputs'][0]['observations']['nativeTextObjectIds']=[]
    self.save(root,m,r);self.assertEqual(self.check(root,m)['technicalStatus'],'FAIL')
 def test_missing_bound_report_and_invalid_report_json_refuse(self):
  for fault in ['missing-binding','missing-file','invalid-json','invalid-type']:
   with self.subTest(fault=fault),tempfile.TemporaryDirectory() as d:
    root=Path(d);m,r=self.fixture(root);self.save(root,m,r)
    if fault=='missing-binding':m.pop('lossReport')
    elif fault=='missing-file':(root/'exchange-loss.json').unlink()
    else:
     (root/'exchange-loss.json').write_text('{' if fault=='invalid-json' else '[]');h=hashlib.sha256((root/'exchange-loss.json').read_bytes()).hexdigest();m['files']['exchange-loss.json']=h;m['lossReport']['sha256']=h
    (root/'manifest.json').write_text(json.dumps(m));q=self.check(root,m);self.assertEqual(q['technicalStatus'],'FAIL')
if __name__=='__main__':unittest.main()
