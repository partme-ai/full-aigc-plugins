"""产物、视觉回执和重启修订；mock 状态明确不构成原生验收。"""
import importlib.util
import json
from pathlib import Path
import struct
import tempfile
import unittest
import uuid
import zlib

ROOT=Path(__file__).resolve().parents[1]


def core():
    spec=importlib.util.spec_from_file_location('task_core',ROOT/'scripts/task_core.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def png(path):
    def chunk(name,data):return struct.pack('>I',len(data))+name+data+struct.pack('>I',zlib.crc32(name+data))
    path.write_bytes(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',3,2,8,2,0,0,0))+chunk(b'IDAT',zlib.compress((b'\x00'+bytes([110,120,130])*3)*2))+chunk(b'IEND',b''))


class ReviewContract(unittest.TestCase):
    def setup_task(self,root):
        c=core();task=root/'task';exports=root/'exports';exports.mkdir()
        photo=exports/'image.png';png(photo)
        plan={'domain':'lightcraft','steps':[{'command':'develop.get','params':{}},{'command':'photo.inspect','params':{}}]}
        state=c.create(task,{'request':'exposure only'},plan,[],library=root/'library',output_root=exports,max_revisions=1)
        path=task/'mock-execution.json'
        resources=c.module('command_gateway').capture_resources(ROOT/'skills/lightcraft-use/scripts')
        receipt={'schemaVersion':1,'domain':'lightcraft','runId':str(uuid.uuid4()),'status':'NATIVE_EXIT_ZERO_REVIEW_REQUIRED',
                 'planSha256':state['planSha256'],'runtimeLockSha256':resources['runtime.lock.json'],'skillResourceSha256':resources,
                 'inputSha256':{},'startedAt':c.now(),'automaticReplay':False,'completeAcceptance':False,
                 'steps':[{'index':0,'command':'develop.get','status':'SUCCEEDED','native':{'result':{'light':{'exposure':.5}}}},
                          {'index':1,'command':'photo.inspect','status':'SUCCEEDED','native':{'result':{'id':1,'source':{'path':'mock-original.png'}}}}]}
        path.write_text(json.dumps(receipt));state.update(status='VERIFYING',receiptPath=str(path),runId=receipt['runId'])
        c.save(task,state,'mock_execution')
        request=c.review_request(task,[{'path':str(photo),'expected':{'width':3}}],{'light':{'exposure':.5}},'photo-v1')
        return c,task,photo,request

    def review_receipt(self,request,verdict='PASS'):
        return {'schemaVersion':1,'requestId':request['requestId'],'bindingSha256':request['bindingSha256'],
                'source':'human','reviewer':'test-fixture','verdict':verdict,'observations':['mock observation']}

    def test_changed_candidate_expires_visual_pass(self):
        with tempfile.TemporaryDirectory() as temporary:
            c,task,photo,request=self.setup_task(Path(temporary))
            photo.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'candidate_changed'):
                c.review(task,self.review_receipt(request))

    def test_duplicate_review_is_refused_and_no_reopen_no_delivery(self):
        with tempfile.TemporaryDirectory() as temporary:
            c,task,photo,request=self.setup_task(Path(temporary))
            receipt=self.review_receipt(request)
            c.review(task,receipt)
            with self.assertRaisesRegex(ValueError,'duplicate'):c.review(task,receipt)
            with self.assertRaisesRegex(ValueError,'reopen'):c.deliver(task)

    def test_revision_limit_survives_reload(self):
        with tempfile.TemporaryDirectory() as temporary:
            c,task,photo,request=self.setup_task(Path(temporary))
            c.review(task,self.review_receipt(request,'FAIL'))
            c.revise(task,{'domain':'lightcraft','steps':[{'command':'develop.get','params':{}}]},'too bright',['light.exposure'])
            reloaded=core().inspect(task)
            self.assertEqual(reloaded['revision'],1)
            self.assertEqual(reloaded['maxRevisions'],1)
            self.assertEqual(reloaded['revisions'][0]['scope'],['light.exposure'])
            reloaded.update(status='AWAITING_REVIEW',reviewRequest=request,reviewReceipt=self.review_receipt(request,'FAIL'))
            c.save(task,reloaded,'mock_second_review')
            with self.assertRaisesRegex(ValueError,'revision_limit_reached'):
                core().revise(task,reloaded['plan'],'still bright',['light.exposure'])

    def test_delivery_requires_explicit_persistence_and_separates_layers(self):
        for persistent in (False,True):
            with self.subTest(persistent=persistent),tempfile.TemporaryDirectory() as temporary:
                c,task,photo,request=self.setup_task(Path(temporary))
                c.review(task,self.review_receipt(request))
                state=c.inspect(task)
                execution=json.loads(Path(state['receiptPath']).read_text())
                library=Path(state['library']);library.mkdir()
                evidence=dict(execution,runId=str(uuid.uuid4()),libraryPath=state['library'],
                              libraryAfterSha256=c.module('command_gateway').capture_inputs([library]))
                evidence['steps']=execution['steps']+[{'index':2,'command':'library.info','status':'SUCCEEDED','native':{'result':{'persistent':persistent,'unsavedOps':0}}}]
                reopen=task/'mock-reopen.json';reopen.write_text(json.dumps(evidence))
                state['reopenEvidence']={'receiptPath':str(reopen)};c.save(task,state,'mock_reopen')
                if not persistent:
                    with self.assertRaisesRegex(ValueError,'persistence_unconfirmed'):c.deliver(task)
                else:
                    result=c.deliver(task)
                    self.assertEqual(result['status'],'COMPLETED')
                    self.assertEqual(result['acceptance']['reopen'],'PASS')
                    self.assertEqual(result['acceptance']['execution'],'NATIVE_EXIT_ZERO_REVIEW_REQUIRED')
                    self.assertTrue((task/'delivery.json').is_file())

    def test_invalid_review_shape_does_not_mutate_state(self):
        with tempfile.TemporaryDirectory() as temporary:
            c,task,photo,request=self.setup_task(Path(temporary))
            before=(task/'state.json').read_bytes()
            receipt=self.review_receipt(request);receipt['observations']='not an array'
            with self.assertRaises(ValueError):c.review(task,receipt)
            self.assertEqual(before,(task/'state.json').read_bytes())

    def test_old_receipt_is_immutable_read_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            c=core();path=Path(temporary)/'legacy.json';path.write_text('{"status":"done"}')
            before=path.read_bytes()
            result=c.module('command_gateway').read_receipt(path)
            self.assertFalse(result['compatible'])
            self.assertTrue(result['readOnly'])
            self.assertEqual(before,path.read_bytes())

    def test_unknown_schema_is_never_compatible(self):
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'receipt.json';path.write_text('{"schemaVersion":1,"status":"success"}')
            with self.assertRaises(ValueError):core().module('command_gateway').read_receipt(path)



    def setup_batch(self,root):
        c,task,photo,old_request=self.setup_task(root);state=c.inspect(task)
        state['plan']={'domain':'lightcraft','steps':[{'command':'develop.get','params':{'id':1}},{'command':'photo.inspect','params':{'id':1}}]}
        state.update(batchScope={'targetIds':[1],'observedIds':[1],'allowedFields':['light.exposure']},batchObservation={'status':'PASS'},status='VERIFYING')
        state['batchScopeSha256']=c.digest(state['batchScope']);state['planSha256']=c.digest(state['plan'])
        receipt=json.loads(Path(state['receiptPath']).read_text());receipt['planSha256']=state['planSha256'];receipt['steps'][1]['native']['result']['develop']={'light':{'exposure':.5}}
        Path(state['receiptPath']).write_text(json.dumps(receipt));state.pop('reviewRequest',None);c.save(task,state,'mock_batch_execution')
        return c,task,photo

    def test_batch_review_requires_settings_bound_to_each_photo(self):
        with tempfile.TemporaryDirectory() as temporary:
            c,task,photo=self.setup_batch(Path(temporary));before=(task/'state.json').read_bytes()
            for settings in [{'light':{'exposure':.5}},{'1':{'light':{'exposure':0}}}]:
                with self.assertRaisesRegex(ValueError,'batch_review_settings'):c.review_request(task,[{'path':str(photo)}],settings,'batch-v1')
                self.assertEqual(before,(task/'state.json').read_bytes())
            request=c.review_request(task,[{'path':str(photo)}],{'1':{'light':{'exposure':.5}}},'batch-v1')
            self.assertEqual(request['binding']['settings']['1']['light']['exposure'],.5)

    def test_batch_reopen_wrong_photo_settings_cannot_deliver(self):
        with tempfile.TemporaryDirectory() as temporary:
            c,task,photo=self.setup_batch(Path(temporary));request=c.review_request(task,[{'path':str(photo)}],{'1':{'light':{'exposure':.5}}},'batch-v1');c.review(task,self.review_receipt(request))
            state=c.inspect(task);evidence=json.loads(Path(state['receiptPath']).read_text());library=Path(state['library']);library.mkdir()
            evidence.update(runId=str(uuid.uuid4()),libraryPath=state['library'],libraryAfterSha256=c.module('command_gateway').capture_inputs([library]))
            evidence['steps'][1]['native']['result']['develop']['light']['exposure']=0
            path=task/'mock-batch-reopen.json';path.write_text(json.dumps(evidence));state['reopenEvidence']={'receiptPath':str(path)};c.save(task,state,'mock_batch_reopen')
            with self.assertRaisesRegex(ValueError,'batch_delivery_settings'):c.deliver(task)
            self.assertFalse((task/'delivery.json').exists())

if __name__=='__main__':unittest.main()
