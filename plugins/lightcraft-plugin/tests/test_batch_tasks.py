"""结构化批量任务不能扩大照片或字段范围。"""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]

def core():
 spec=importlib.util.spec_from_file_location('batch_core',ROOT/'scripts/task_core.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

class BatchTasks(unittest.TestCase):
 def setUp(self):
  self.scope={'targetIds':[1,2],'observedIds':[1,2,3],'allowedFields':['light.exposure']}
 def plan(self,ids=None,values=None):return {'domain':'lightcraft','steps':[{'command':'develop.set','params':{'ids':[1,2] if ids is None else ids,'values':{'light.exposure':.5} if values is None else values}}]}
 def test_batch_contract_is_saved_and_run_revalidates(self):
  api=core()
  with tempfile.TemporaryDirectory() as temp:
   task=Path(temp)/'task';state=api.create(task,{},self.plan(),[],batch_scope=self.scope)
   self.assertEqual(state['batchScope'],self.scope)
   state['batchScope']['targetIds'].append(3);(task/'state.json').write_text(json.dumps(state))
   with self.assertRaisesRegex(ValueError,'batch_scope_identity'):api.run(task)
 def test_invalid_initial_scope_has_no_task_directory(self):
  api=core()
  for plan in [self.plan([3]),self.plan([True]),self.plan(values={'light.contrast':1}),{'domain':'lightcraft','steps':[{'command':'develop.reset','params':{}}]},{'domain':'lightcraft','steps':[{'command':'develop.set','params':{'control':'light.exposure','value':1}}]}]:
   with tempfile.TemporaryDirectory() as temp:
    task=Path(temp)/'task'
    with self.assertRaises(ValueError):api.create(task,{},plan,[],batch_scope=self.scope)
    self.assertFalse(task.exists())
 def test_selective_revision_and_outside_scope_are_atomic(self):
  api=core()
  with tempfile.TemporaryDirectory() as temp:
   task=Path(temp)/'task';state=api.create(task,{},self.plan(),[],batch_scope=self.scope)
   state.update(status='AWAITING_REVIEW',reviewReceipt={'verdict':'FAIL'},reviewRequest={'id':'fixture-only'})
   (task/'state.json').write_text(json.dumps(state));before=(task/'state.json').read_bytes()
   for scope in ['exposure only',{'targetIds':[3],'allowedFields':['light.exposure']},{'targetIds':[2],'allowedFields':['light.contrast']}]:
    with self.assertRaises(ValueError):api.revise(task,self.plan([2]),'fixture failed review',scope)
    self.assertEqual((task/'state.json').read_bytes(),before)
   state=api.revise(task,self.plan([2],{'light.exposure':.25}),'fixture failed review',{'targetIds':[2],'allowedFields':['light.exposure']})
   self.assertEqual(state['revision'],1);self.assertEqual(state['batchScope'],self.scope)
   self.assertEqual(state['revisionScope']['targetIds'],[2])
 def test_revision_plan_must_match_declared_subset(self):
  api=core()
  with tempfile.TemporaryDirectory() as temp:
   task=Path(temp)/'task';state=api.create(task,{},self.plan(),[],batch_scope=self.scope)
   state.update(status='AWAITING_REVIEW',reviewReceipt={'verdict':'FAIL'},reviewRequest={});(task/'state.json').write_text(json.dumps(state))
   with self.assertRaisesRegex(ValueError,'outside_scope'):api.revise(task,self.plan([1]),'fixture',{'targetIds':[2],'allowedFields':['light.exposure']})


 def test_real_step_shape_requires_all_observations_and_no_collateral_change(self):
  import copy
  api=core();source='/synthetic/original.png';base={'light':{'exposure':0,'contrast':0},'enhance':{'raw_details':False}};plan={'domain':'lightcraft','steps':[]};rows=[]
  def photo(identifier,settings):
   plan['steps'].append({'command':'photo.inspect','params':{'id':identifier}})
   rows.append({'index':len(rows),'command':'photo.inspect','status':'SUCCEEDED','native':{'result':{'id':identifier,'source':{'type':'file','path':source},'develop':copy.deepcopy(settings)}}})
  for i in [1,2,3]:photo(i,base)
  plan['steps']+=self.plan([2],{'light.exposure':.25})['steps'];rows.append({'index':3,'command':'develop.set','status':'SUCCEEDED'})
  for i in [1,2,3]:
   setting=copy.deepcopy(base)
   if i==2:setting['light']['exposure']=.25
   photo(i,setting)
  state={'plan':plan,'batchScope':self.scope,'originals':{source:'0'*64}}
  self.assertEqual(api.verify_batch_execution(state,{'steps':rows})['status'],'PASS')
  changed=copy.deepcopy(rows);changed[-1]['native']['result']['develop']['enhance']['raw_details']=0
  with self.assertRaisesRegex(ValueError,'outside_scope'):api.verify_batch_execution(state,{'steps':changed})
  rows[-1]['native']['result']['develop']['light']['contrast']=1
  with self.assertRaisesRegex(ValueError,'outside_scope'):api.verify_batch_execution(state,{'steps':rows})
  with self.assertRaisesRegex(ValueError,'incomplete'):api.verify_batch_execution(state,{'steps':rows[:-1]})

if __name__=='__main__':unittest.main()
