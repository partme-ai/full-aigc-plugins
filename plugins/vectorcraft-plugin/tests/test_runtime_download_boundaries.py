"""用当前固定安装器逐项验证RT-002下载失败分类；故障注入不冒充真实网络故障。"""
import errno,hashlib,importlib.util,json,os,ssl,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError,URLError
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'skills/vectorcraft-harness/scripts/bootstrap.py'
class Response:
 url='https://objects.githubusercontent.com/release'
 def __init__(self,error=None,body=b'complete',length=None):self.error=error;self.body=body;self.reads=0;self.headers={} if length is None else {'Content-Length':str(length)}
 def __enter__(self):return self
 def __exit__(self,*args):return False
 def read(self,_):
  self.reads+=1
  if self.error and self.reads==2:raise self.error
  if self.reads==1:return b'partial' if self.error else self.body
  return b''
class RuntimeDownloadBoundaryTests(unittest.TestCase):
 def setUp(self):
  source=Path(os.environ.get('VECTORCRAFT_INSTALLED_BOOTSTRAP',SOURCE))
  self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),hashlib.sha256(SOURCE.read_bytes()).hexdigest())
  spec=importlib.util.spec_from_file_location('fixed_runtime_download',source);self.module=importlib.util.module_from_spec(spec)
  with patch.object(sys,'dont_write_bytecode',True):spec.loader.exec_module(self.module)
  self.lock=json.loads(SOURCE.with_name('runtime.lock.json').read_text());self.url=self.lock['artifacts']['darwin-arm64']['url'];self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup);self.root=Path(self.temp.name);self.target=self.root/'download.zip'
 def transient(self):
  return [ssl.SSLEOFError('EOF'),TimeoutError('timeout'),ConnectionResetError('reset'),URLError(ConnectionAbortedError('aborted'))]+[HTTPError(self.url,c,'transient',{},None) for c in [408,429,500,502,503,504,599]]
 def test_every_declared_transient_discards_partial_and_recovers(self):
  for error in self.transient():
   with self.subTest(error=str(error)),patch.object(self.module.urllib.request,'urlopen',side_effect=[Response(error),Response()]) as fetch,patch.object(self.module.time,'sleep'):
    self.module.download(self.url,self.target);self.assertEqual(fetch.call_count,2);self.assertEqual(self.target.read_bytes(),b'complete')
  with patch.object(self.module.urllib.request,'urlopen',side_effect=[Response(body=b'short',length=9),Response()]) as fetch,patch.object(self.module.time,'sleep'):
   self.module.download(self.url,self.target);self.assertEqual(fetch.call_count,2);self.assertEqual(self.target.read_bytes(),b'complete')
 def test_every_declared_transient_stops_at_three_attempts(self):
  for error in self.transient():
   with self.subTest(error=str(error)),patch.object(self.module.urllib.request,'urlopen',side_effect=error) as fetch,patch.object(self.module.time,'sleep'),patch.object(self.module.subprocess,'run',side_effect=AssertionError('native editing started')):
    self.target.write_bytes(b'stale-partial')
    with self.assertRaisesRegex(ValueError,'three read-only attempts exhausted'):self.module.download(self.url,self.target)
    self.assertEqual(fetch.call_count,3);self.assertFalse(self.target.exists())
 def test_certificate_permission_and_nontransient_http_have_one_attempt(self):
  for error in [URLError(ssl.SSLCertVerificationError('certificate')),PermissionError('permission')]+[HTTPError(self.url,c,'denied',{},None) for c in [400,401,403,404,409]]:
   with self.subTest(error=str(error)),patch.object(self.module.urllib.request,'urlopen',side_effect=error) as fetch,patch.object(self.module.time,'sleep',side_effect=AssertionError('retried')):
    with self.assertRaises(type(error)):self.module.download(self.url,self.target)
    self.assertEqual(fetch.call_count,1)
 def test_disk_and_size_failures_have_one_attempt(self):
  with patch.object(self.module.urllib.request,'urlopen',return_value=Response()) as fetch,patch.object(Path,'open',side_effect=OSError(errno.ENOSPC,'disk full')),patch.object(self.module.time,'sleep',side_effect=AssertionError('retried')):
   with self.assertRaises(OSError) as error:self.module.download(self.url,self.target)
   self.assertEqual(error.exception.errno,errno.ENOSPC);self.assertEqual(fetch.call_count,1)
  with patch.object(self.module.urllib.request,'urlopen',return_value=Response()) as fetch,patch.object(self.module,'MAX_BYTES',2),patch.object(self.module.time,'sleep',side_effect=AssertionError('retried')):
   with self.assertRaisesRegex(ValueError,'archive_too_large'):self.module.download(self.url,self.target)
   self.assertEqual(fetch.call_count,1)
 def test_checksum_refusal_never_executes_and_unsupported_platform_never_downloads(self):
  with patch.object(self.module.urllib.request,'urlopen',return_value=Response(body=b'corrupt')) as fetch,patch.object(self.module.subprocess,'run',side_effect=AssertionError('unverified executable')):
   with self.assertRaisesRegex(ValueError,'archive_checksum'):self.module.install(self.lock,self.root/'runtime',platform_key='darwin-arm64')
   self.assertEqual(fetch.call_count,1);self.assertFalse((self.root/'runtime/vectorcraft'/self.lock['resolvedVersion']).exists())
  with patch.object(self.module.urllib.request,'urlopen',side_effect=AssertionError('network')):
   with self.assertRaisesRegex(ValueError,'unsupported_platform'):self.module.install(self.lock,self.root/'unsupported',platform_key='linux-x86_64')
   self.assertFalse((self.root/'unsupported').exists())
