"""控制器状态故障和上游回执集成；全部为 mock，不构成原生验收。"""
import importlib.util,json
from pathlib import Path
import subprocess,tempfile,unittest,shutil,sys
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]

def core():
    spec=importlib.util.spec_from_file_location('task_core',ROOT/'scripts/task_core.py')
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result

class ControllerIntegration(unittest.TestCase):
    def create(self,root):
        c=core();task=root/'task'
        c.create(task,{}, {'domain':'lightcraft','steps':[{'command':'library.info','params':{}}]},[])
        return c,task

    def test_cli_stdout_remains_one_json_document_when_child_reports(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);package=root/'plugin'
            shutil.copytree(ROOT,package,ignore=shutil.ignore_patterns('.git','__pycache__'))
            c,task=self.create(root)
            child=package/'skills/lightcraft-use/scripts/commands.py'
            child.write_text("print('{\"child\": true}')\n")
            result=subprocess.run([sys.executable,'-I','-B',str(package/'scripts/controller.py'),'run',str(task)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            state=json.loads(result.stdout)
            self.assertEqual(state['status'],'UNKNOWN')
            logs=list((task/'runs').glob('*.stdout.log'))
            self.assertEqual(len(logs),1)
            self.assertIn('child',logs[0].read_text())

    def test_unknown_and_not_saved_propagate_without_replay(self):
        for status in ['UNKNOWN','PERSISTENCE_UNCONFIRMED','FAILED_OR_PARTIAL']:
            with self.subTest(status=status),tempfile.TemporaryDirectory() as temporary:
                c,task=self.create(Path(temporary))
                def execute(argv,**kwargs):
                    state=c.inspect(task)
                    self.assertEqual(state['status'],'RUNNING')
                    path=Path(state['receiptPath']);path.parent.mkdir(parents=True)
                    resources=c.module('command_gateway').capture_resources(ROOT/'skills/lightcraft-use/scripts')
                    receipt={'schemaVersion':1,'domain':'lightcraft','runId':'mock-run','status':status,
                             'planSha256':state['planSha256'],'runtimeLockSha256':resources['runtime.lock.json'],'skillResourceSha256':resources,'inputSha256':{},
                             'startedAt':c.now(),'steps':[{'index':0,'command':'library.info','status':'UNKNOWN'}],'automaticReplay':False,'completeAcceptance':False}
                    path.write_text(json.dumps(receipt))
                    return subprocess.CompletedProcess(argv,1,'','')
                with patch.object(c.subprocess,'run',side_effect=execute) as execute_mock:
                    state=c.run(task)
                    self.assertIn(state['status'],['UNKNOWN','FAILED_OR_PARTIAL'])
                    self.assertEqual(state['acceptance']['execution'],status)
                    with self.assertRaisesRegex(ValueError,'no_replay'):c.run(task)
                    self.assertEqual(execute_mock.call_count,1)

    def test_missing_receipt_even_with_existing_output_is_unknown(self):
        with tempfile.TemporaryDirectory() as temporary:
            c,task=self.create(Path(temporary))
            def execute(argv,**kwargs):
                path=Path(c.inspect(task)['receiptPath']).parent;path.mkdir(parents=True);(path/'export.png').write_bytes(b'possibly exported')
                return subprocess.CompletedProcess(argv,0,'','')
            with patch.object(c.subprocess,'run',side_effect=execute):
                self.assertEqual(c.run(task)['status'],'UNKNOWN')

    def test_corrupt_execution_receipt_is_recorded_as_unknown(self):
        with tempfile.TemporaryDirectory() as temporary:
            c,task=self.create(Path(temporary))
            def execute(argv,**kwargs):
                path=Path(c.inspect(task)['receiptPath']);path.parent.mkdir(parents=True)
                path.write_text('{')
                return subprocess.CompletedProcess(argv,0,'','')
            with patch.object(c.subprocess,'run',side_effect=execute):
                state=c.run(task)
            self.assertEqual(state['status'],'UNKNOWN')
            self.assertEqual(c.inspect(task)['status'],'UNKNOWN')

    def test_atomic_write_failure_keeps_prior_state(self):
        with tempfile.TemporaryDirectory() as temporary:
            c,task=self.create(Path(temporary));before=(task/'state.json').read_bytes()
            with patch.object(c.os,'replace',side_effect=OSError('injected write interruption')):
                with self.assertRaises(OSError):c.save(task,c.inspect(task),'test')
            self.assertEqual((task/'state.json').read_bytes(),before)
            self.assertEqual(list(task.glob('.state-*')),[])

    def test_stop_can_be_requested_while_controller_holds_lock(self):
        with tempfile.TemporaryDirectory() as temporary:
            c,task=self.create(Path(temporary))
            with c.task_lock(task):
                result=c.stop(task)
                self.assertEqual(result['status'],'REQUESTED')
                self.assertEqual(json.loads((task/'stop-request.json').read_text())['nativeTermination'],'UNCONFIRMED')

    def test_remaining_is_bound_to_run_and_requires_explicit_new_session(self):
        with tempfile.TemporaryDirectory() as temporary:
            c,task=self.create(Path(temporary));state=c.inspect(task)
            resources=c.module('command_gateway').capture_resources(ROOT/'skills/lightcraft-use/scripts')
            receipt={'schemaVersion':1,'domain':'lightcraft','runId':'recorded-run','status':'FAILED_OR_PARTIAL',
                     'planSha256':state['planSha256'],'runtimeLockSha256':resources['runtime.lock.json'],
                     'skillResourceSha256':resources,'inputSha256':{},'startedAt':c.now(),
                     'steps':[{'index':0,'command':'library.info','status':'NOT_EXECUTED'}],
                     'protocolComplete':True,'automaticReplay':False,'completeAcceptance':False}
            path=task/'mock-receipt.json';path.write_text(json.dumps(receipt))
            state.update(status='FAILED_OR_PARTIAL',receiptPath=str(path),runId='recorded-run');c.save(task,state,'mock_failure')
            result=c.remaining(task)
            self.assertTrue(result['requiresSessionPreconditions'])
            self.assertTrue(result['requiresAuthorizationReview'])
            self.assertFalse(result['automaticReplay'])
            receipt['runId']='different-run';path.write_text(json.dumps(receipt))
            with self.assertRaisesRegex(ValueError,'remaining_identity'):c.remaining(task)

if __name__=='__main__':unittest.main()
