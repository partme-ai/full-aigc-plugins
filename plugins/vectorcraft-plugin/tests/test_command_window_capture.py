"""窗口读取故障可有限重取，任何重试都不能成为编辑请求重放。"""
import hashlib,importlib.util,json,sys,tempfile,types,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
class WindowCaptureTests(unittest.TestCase):
 def setUp(self):
  spec=importlib.util.spec_from_file_location('window_capture',ROOT/'scripts/qa/command_family_window.py');self.m=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.m);self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
 def test_read_errors_stop_after_three_attempts(self):
  seen=[]
  owned=types.SimpleNamespace(request=lambda *args:seen.append(args) or {})
  def parse(*args):raise RuntimeError('native-read-error')
  with patch.dict(sys.modules,{'PIL':types.SimpleNamespace(Image=None)}):
   with self.assertRaises(RuntimeError):self.m.capture_window(owned,types.SimpleNamespace(parse_reply=parse),self.root/'window',1,self.root)
  self.assertEqual(len(seen),3);self.assertTrue(all(x[1]['name']=='screenshot' for x in seen));self.assertEqual(len(json.loads((self.root/'window/attempts.json').read_text())),3)
 def test_second_read_can_recover_without_replaying_any_command(self):
  seen=[]
  def request(*args):seen.append(args);return {}
  def parse(reply,directory,number):
   if len(seen)==1:raise RuntimeError('native-read-error')
   p=directory/'fake.png';p.write_bytes(b'test payload');return {'content':[{'type':'image','path':'fake.png','sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':12,'mimeType':'image/png'},{'type':'text','value':{'window':True}}]}
  class Img:
   size=(1440,900)
   def __enter__(self):return self
   def __exit__(self,*args):pass
   def load(self):pass
  with patch.dict(sys.modules,{'PIL':types.SimpleNamespace(Image=types.SimpleNamespace(open=lambda p:Img()))}):r=self.m.capture_window(types.SimpleNamespace(request=request),types.SimpleNamespace(parse_reply=parse),self.root/'window',1,self.root)
  self.assertEqual([a['status'] for a in r['readAttempts']],['native-read-error','PASS']);self.assertTrue(all(x[1]['name']=='screenshot' for x in seen))
