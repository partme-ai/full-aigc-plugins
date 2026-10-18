"""检查实际 tar 头，防止 PAX 扩展重新进入分发包。"""
import gzip,importlib.util,tempfile,unittest,subprocess,json,tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('pack_runtime',ROOT/'ui/package-runtime.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class RuntimeArchiveContract(unittest.TestCase):
    def test_raw_headers_are_only_regular_and_directory_and_repeatable(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);runtime=root/'runtime';(runtime/'editor').mkdir(parents=True);(runtime/'editor/中文.json').write_text('{}',encoding='utf-8');(runtime/'adapter.mjs').write_text('export {}')
            a=root/'one.tgz';b=root/'two.tgz';self.assertEqual(module.package(runtime,a),module.package(runtime,b));raw=gzip.decompress(a.read_bytes());offset=0
            while any(raw[offset:offset+512]):
                header=raw[offset:offset+512];self.assertIn(header[156:157],[b'0',b'5']);size=int(header[124:136].strip(b'\x00 '),8);offset+=512+((size+511)//512)*512
            before=a.read_bytes()
            with self.assertRaises(FileExistsError):module.package(runtime,a)
            self.assertEqual(a.read_bytes(),before)
    def test_actual_bootstrap_accepts_ustar_and_rejects_pax(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);runtime=root/'runtime';runtime.mkdir();(runtime/'adapter.mjs').write_text('export {}')
            good=root/'good.tgz';bad=root/'bad.tgz';module.package(runtime,good)
            with tarfile.open(bad,'w:gz',format=tarfile.PAX_FORMAT) as archive:
                info=archive.gettarinfo(str(runtime/'adapter.mjs'),arcname='adapter.mjs');info.mtime=1.25
                with (runtime/'adapter.mjs').open('rb') as stream:archive.addfile(info,stream)
            for archive,expected in [(good,0),(bad,1)]:
                dest=root/archive.stem
                code='import {extractRuntime} from '+json.dumps((ROOT/'ui/bootstrap.mjs').as_uri())+'; import {readFile} from "node:fs/promises"; await extractRuntime(await readFile('+json.dumps(str(archive))+'),'+json.dumps(str(dest))+');'
                result=subprocess.run(['node','--input-type=module','-e',code],capture_output=True,text=True)
                self.assertEqual(result.returncode,expected,result.stderr)
                if expected:self.assertIn('Unsupported tar entry type: x',result.stderr)
                else:self.assertEqual((dest/'adapter.mjs').read_text(),'export {}')
    def test_symlink_refused_before_archive_creation(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t);runtime=root/'runtime';runtime.mkdir();(root/'file').write_text('outside')
            try:(runtime/'link').symlink_to(root/'file')
            except OSError:self.skipTest('Windows symlink privilege unavailable')
            with self.assertRaises(ValueError):module.package(runtime,root/'out.tgz')
            self.assertFalse((root/'out.tgz').exists())
if __name__=='__main__':unittest.main()
