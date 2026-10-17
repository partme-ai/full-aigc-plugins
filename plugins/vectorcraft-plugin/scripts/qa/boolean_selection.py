#!/usr/bin/env python3
"""固定技能的实际选择与子树授权QA；显式制造计划选择和实际选择不一致。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time
root=Path(sys.argv[1]).resolve();installed=Path(sys.argv[2]).resolve();runtime=Path(sys.argv[3]).resolve();source_root=Path(sys.argv[4]).resolve();group_root=Path(sys.argv[5]).resolve()
root.mkdir();skill=installed/'skills/vectorcraft-use'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def module(name):
 spec=importlib.util.spec_from_file_location('fixed_selection_'+name,skill/'scripts'/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
Session=module('mcp_session').Session;Control=module('execution_control').ExecutionControl;guard=module('boolean_transactions')
lock=json.loads((skill/'scripts/runtime.lock.json').read_text());binary=runtime/'vectorcraft'/lock['resolvedVersion']/'vectorcraft-cli';assert sha(binary)==lock['artifacts']['darwin-arm64']['binarySha256']
records=[]
for name,source in [('selection-mismatch',source_root),('missing-descendants',group_root)]:
 work=root/name;work.mkdir();project=source/'project.vectorcraft';manifest=json.loads((source/'manifest.json').read_text());original=sha(project);plan=work/'plan.json';plan.write_text('{"operations":[]}');state=work/'state.json';state.write_text(json.dumps({'task':name,'epoch':1,'state':'running'}));events=work/'events.jsonl';events.touch();st=events.stat()
 ids=[manifest['bindings'][n]['id'] for n in ['outer','inner']];group=manifest['bindings'].get('result',{}).get('id')
 auth_ids=ids if name=='selection-mismatch' else [group]
 profile={'schema':'vectorcraft-execution-control/v1','task':name,'epoch':1,'stateFile':str(state),'eventFile':str(events),'eventDevice':st.st_dev,'eventInode':st.st_ino,'deadline':int(time.time()*1000)+60000,'maxBytes':10000000,'runtimeIdentity':sha(binary),'source':{'path':str(project),'sha256':original},'planFile':str(plan),'planHash':sha(plan),'authorization':{'objects':auth_ids,'fields':['structure']}}
 path=work/'control.json';path.write_text(json.dumps(profile));control=Control(path)
 with Session([str(binary),'mcp','--headless'],control=control) as session:
  session.command('document.open',{'path':str(project)});before=session.command('document.json',{})
  if name=='selection-mismatch':
   control.authorize_operation('select.set',{'ids':ids},before)
   session.command('select.set',{'ids':[ids[0]]});actual=session.command('document.inspect',{})['selection'];after=session.command('document.json',{});assert actual==[ids[0]] and guard.normalized(before)==guard.normalized(after)
   try:control.verify_revision(before,after,'select.set',{'ids':ids},after_selection=actual)
   except RuntimeError as error:assert 'revision_selection_identity_mismatch' in str(error);reason='revision_selection_identity_mismatch'
   else:raise AssertionError('wrong selection accepted')
  else:
   session.command('select.set',{'ids':[group]});actual=session.command('document.inspect',{})['selection'];assert actual==[group]
   try:control.authorize_operation('object.ungroup',{},before,selection=actual)
   except RuntimeError as error:assert 'revision_outside_authorization' in str(error);reason='revision_outside_authorization'
   else:raise AssertionError('ungranted descendants accepted')
  assert sha(project)==original
 assert session.process.returncode is not None
 event_rows=[json.loads(x) for x in events.read_text().splitlines()];commands=[x.get('params',{}).get('arguments',{}).get('command') for x in event_rows if x['event']=='submitted'];assert not any(x in guard.COMMANDS for x in commands)
 records.append({'name':name,'result':'PASS','expectedFailure':reason,'explicitSelectionMismatchInjection':name=='selection-mismatch','sourceSha256':original,'sourceUnchanged':sha(project)==original,'actualSelection':actual,'authorizedObjectIds':auth_ids,'planObjectIds':ids,'nativeMutationNotSubmitted':True,'sessionExited':True,'beforeModelSha256':hashlib.sha256(json.dumps(guard.normalized(before),sort_keys=True).encode()).hexdigest(),'eventSha256':sha(events)})
proof={'schema':'vectorcraft-boolean-selection-fixed/v1','result':'PASS','scope':'real pinned SDK control with actual reopened native document/selection; explicit selection mismatch and missing descendant authorization; not an engine defect or complete Harness case','runtimeIdentity':sha(binary),'driverSha256':sha(__file__),'cases':records,'fingerprints':{str(p.relative_to(installed)):sha(p) for p in sorted(skill.rglob('*')) if p.is_file()}}
(root/'proof.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps({'result':'PASS','cases':len(records)}))
