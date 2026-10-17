import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
def load():
    spec=importlib.util.spec_from_file_location('harness',ROOT/'skills/printcraft-harness/scripts/harness.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
class Harness(unittest.TestCase):
    def test_unknown_protocol_and_missing_run_id_fail(self):
        for data in ({},{'protocol':'printcraft.execution/9'},{'protocol':'printcraft.execution/1','status':'UNKNOWN'}):
            with self.assertRaises(ValueError):load().consume(data)
    def test_unknown_partial_and_zero_exit_never_trigger_replay(self):
        for status in ('UNKNOWN','FAILED_OR_PARTIAL','NATIVE_EXIT_ZERO_REVIEW_REQUIRED'):
            data=load().consume({'protocol':'printcraft.execution/1','runId':'same-run','status':status})
            self.assertFalse(data['automaticReplay']);self.assertFalse(data['completeAcceptance']);self.assertEqual(data['runId'],'same-run')
    def test_explicit_route_and_authority_reuse(self):
        h=load();self.assertEqual(h.route('general','printcraft-cli-pages'),'printcraft-cli-pages')
        self.assertEqual(h.new_scope(['read','save-as'],['save-as']),[])
        self.assertEqual(h.new_scope(['read','save-as'],['overwrite-original','print']),['overwrite-original','print'])
    def test_public_delegate_works_from_space_chinese_path(self):
        import shutil
        with tempfile.TemporaryDirectory(prefix='打印 插件 ') as t:
            root=Path(t)/'包';shutil.copytree(ROOT/'skills',root/'skills')
            catalog=Path(t)/'catalog.json';catalog.write_text('[{"name":"doc_info","input_schema":{"type":"object","properties":{}}}]')
            r=subprocess.run([sys.executable,'-I',str(root/'skills/printcraft-harness/scripts/harness.py'),'delegate','list','--catalog',str(catalog)],capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stdout+r.stderr);self.assertEqual(json.loads(r.stdout)['count'],1)
if __name__=='__main__':unittest.main()

class ExplicitCLI(unittest.TestCase):
    def test_explicit_skill_is_honored_by_cli(self):
        r=subprocess.run([sys.executable,str(ROOT/'skills/printcraft-harness/scripts/harness.py'),'route','general','--explicit','printcraft-cli-pages'],capture_output=True,text=True)
        self.assertEqual(json.loads(r.stdout)['skill'],'printcraft-cli-pages')

class ExternalOcrHarness(unittest.TestCase):
    def test_ocr_route_and_receipt_never_complete(self):
        h=load();self.assertEqual(h.route('ocr'),'printcraft-use')
        for status in ('UNKNOWN','FAILED_OR_PARTIAL','DETERMINISTIC_PASS_REVIEW_REQUIRED','PRESERVATION_UNKNOWN_REVIEW_REQUIRED','INPUT_OR_BACKEND_OR_SKILL_CHANGED_REVIEW_REQUIRED'):
            data=h.consume({'protocol':'printcraft.ocr/1','runId':'ocr-run','status':status,'completeAcceptance':True,'backendIdentity':{'backend':'tesseract'}})
            self.assertFalse(data['completeAcceptance']);self.assertFalse(data['automaticReplay']);self.assertEqual(data['backendIdentity']['backend'],'tesseract')
            if status=='UNKNOWN':self.assertEqual(data['nextAction'],'READ_ONLY_OCR_RECEIPT_AND_ARTIFACTS')
        for data in ({'protocol':'printcraft.ocr/1','status':'UNKNOWN'},{'protocol':'printcraft.ocr/1','runId':'x','status':'VERIFIED'}):
            with self.assertRaises(ValueError):h.consume(data)

    def test_public_ocr_delegates_to_owned_entry_with_explicit_backend(self):
        from unittest.mock import patch
        h=load()
        with patch.object(sys,'argv',['harness.py','ocr','diagnose','--backend','tesseract','--language','chi_sim']),patch.object(h.subprocess,'run',return_value=subprocess.CompletedProcess([],0)) as run:
            self.assertEqual(h.main(),0)
        argv=run.call_args.args[0]
        self.assertEqual(argv[3],str(ROOT/'skills/printcraft-use/scripts/ocr.py'))
        self.assertEqual(argv[4:],['diagnose','--backend','tesseract','--language','chi_sim'])
