"""只读 MCP 观察回执不允许升级为任务执行或交付成功。"""
import copy,hashlib,importlib.util,json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


class SessionFacts(unittest.TestCase):
    def fixture(self):
        scripts=ROOT/'skills/lightcraft-use/scripts';gateway=load('gw',scripts/'command_gateway.py')
        requests=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2025-06-18','capabilities':{},'clientInfo':{'name':'lightcraft-readonly-probe','version':'1'}}},
                  {'jsonrpc':'2.0','method':'notifications/initialized','params':{}},
                  {'jsonrpc':'2.0','id':2,'method':'tools/list','params':{}},
                  {'jsonrpc':'2.0','id':3,'method':'resources/read','params':{'uri':'lightcraft://library'}}]
        sha=hashlib.sha256(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in requests).encode()).hexdigest()
        binary=json.loads((scripts/'runtime.lock.json').read_text())['artifacts']['darwin-arm64']['binarySha256']
        return {'schemaVersion':1,'receiptKind':'mcp-readonly-probe','domain':'lightcraft','runId':'fixture-client-run','status':'NATIVE_EXIT_ZERO_REVIEW_REQUIRED',
                'planSha256':hashlib.sha256(json.dumps({'domain':'lightcraft','steps':[{'command':'mcp:'+r['method'],'params':r['params']} for r in requests if 'id' in r]},sort_keys=True,ensure_ascii=False).encode()).hexdigest(),'runtimeLockSha256':gateway.file_sha(scripts/'runtime.lock.json'),'skillResourceSha256':gateway.capture_resources(scripts),
                'inputSha256':{},'startedAt':'2026-10-08T00:00:00+00:00','requests':requests,'requestsSha256':sha,'readOnly':True,
                'automaticReplay':False,'completeAcceptance':False,'backendQuery':'PASS','backendSessionIdentity':'NOT_PROVIDED_BY_NATIVE_PROTOCOL',
                'requestedMode':{'mode':'Connect','connectAddress':'127.0.0.1:18991'},
                'runtimeIdentity':{'version':'0.2.1','binarySha256':binary,'mode':'Connect','transport':'stdio-mcp','connectAddress':'127.0.0.1:18991','readOnly':True},
                'process':{'status':'EXITED','exitCode':0,'logComplete':True,'stdinSha256':sha},
                'steps':[{'index':i,'command':'mcp:'+r['method'],'status':'SUCCEEDED'} for i,r in enumerate([r for r in requests if 'id' in r])]}

    def inspect(self,receipt):
        module=load('session_facts',ROOT/'scripts/session_facts.py')
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'receipt.json';path.write_text(json.dumps(receipt));return module.inspect_session(path)

    def test_valid_probe_is_readonly_and_cannot_deliver(self):
        receipt=self.fixture();receipt['steps']=[dict(s,index=i) for i,s in enumerate(receipt['steps'])]
        result=self.inspect(receipt)
        self.assertTrue(result['readOnly']);self.assertFalse(result['taskExecutionAllowed']);self.assertFalse(result['deliveryAllowed'])
        self.assertEqual(result['backendSessionIdentity'],'NOT_PROVIDED_BY_NATIVE_PROTOCOL')

    def test_mutation_and_inconsistent_success_rejected(self):
        base=self.fixture();base['steps']=[dict(s,index=i) for i,s in enumerate(base['steps'])]
        cases=[]
        r=copy.deepcopy(base);r['requests'][3]={'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'set_develop'}};cases.append(r)
        r=copy.deepcopy(base);r['process']['status']='UNKNOWN';cases.append(r)
        r=copy.deepcopy(base);r['runtimeIdentity']['mode']='Headless';cases.append(r)
        r=copy.deepcopy(base);r['runtimeIdentity']['binarySha256']='b'*64;cases.append(r)
        for receipt in cases:
            with self.subTest(case=cases.index(receipt)),self.assertRaises(ValueError):self.inspect(receipt)

    def test_newer_source_remains_readonly_until_snapshot_upgrade(self):
        receipt=self.fixture();receipt['steps']=[dict(s,index=i) for i,s in enumerate(receipt['steps'])]
        receipt['skillResourceSha256']['session_probe.py']='c'*64
        result=self.inspect(receipt)
        self.assertFalse(result['sourceSnapshotMatches']);self.assertFalse(result['taskExecutionAllowed'])

    def test_unknown_and_not_saved_stay_unconfirmed_without_replay(self):
        for status,step in [('UNKNOWN','UNKNOWN'),('PERSISTENCE_UNCONFIRMED','APPLIED_NOT_SAVED')]:
            receipt=self.fixture();receipt.update(status=status,backendQuery='NOT_CONFIRMED')
            receipt['steps'][2]['status']=step
            result=self.inspect(receipt)
            self.assertEqual(result['status'],status)
            self.assertFalse(result['automaticReplay']);self.assertFalse(result['deliveryAllowed'])

    def test_client_run_id_cannot_be_used_as_desktop_session_identity(self):
        receipt=self.fixture();receipt['backendSessionIdentity']=receipt['runId']
        with self.assertRaisesRegex(ValueError,'backend_identity_claim'):self.inspect(receipt)

    def test_controller_session_inspect_is_a_separate_readonly_action(self):
        receipt=self.fixture();receipt['steps']=[dict(s,index=i) for i,s in enumerate(receipt['steps'])]
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'receipt.json';path.write_text(json.dumps(receipt));before=path.read_bytes()
            process=subprocess.run([sys.executable,'-I','-B',str(ROOT/'scripts/controller.py'),'session-inspect',str(path)],capture_output=True,text=True)
            self.assertEqual(process.returncode,0,process.stdout+process.stderr);self.assertEqual(before,path.read_bytes())
            self.assertFalse(json.loads(process.stdout)['taskExecutionAllowed'])

if __name__=='__main__':unittest.main()
