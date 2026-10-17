"""控制器仅路由只读协议检查；真实 Node 和原生验收另存。"""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest import mock
ROOT=Path(__file__).resolve().parents[1]
class CraftController(unittest.TestCase):
 def invoke(self,result):
  spec=importlib.util.spec_from_file_location('controller',ROOT/'scripts/controller.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);output=io.StringIO()
  with mock.patch.object(sys,'argv',['controller','craft-inspect','explicit-bundle.json']),mock.patch.object(m.subprocess,'run',return_value=result) as run,contextlib.redirect_stdout(output):code=m.main()
  self.assertEqual(run.call_count,1);self.assertEqual(run.call_args.args[0],['node',str(ROOT/'scripts/craft_exchange.ts'),'explicit-bundle.json'])
  return code,json.loads(output.getvalue())
 def test_result_never_authorizes_task_execution(self):
  code,result=self.invoke(subprocess.CompletedProcess([],0,json.dumps({'executionAllowed':False,'automaticReplay':False}),''));self.assertEqual(code,0);self.assertFalse(result['taskExecutionAllowed'])
 def test_failed_or_permission_promoting_results_reject(self):
  for result in [subprocess.CompletedProcess([],1,'{"error":"invalid"}',''),subprocess.CompletedProcess([],0,'{"executionAllowed":true,"automaticReplay":false}',''),subprocess.CompletedProcess([],0,'{"executionAllowed":false,"automaticReplay":true}','')]:
   with self.subTest(result=result.stdout):self.assertEqual(self.invoke(result)[0],1)
if __name__=='__main__':unittest.main()
