"""只读核对逐 RAW 样本回执；不启动 Lightcraft、不下载、不交付或重放。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]


def module(name):
 spec=importlib.util.spec_from_file_location('raw_observer_'+name,ROOT/'skills/lightcraft-use/scripts'/(name+'.py'))
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def digest(value):
 return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,allow_nan=False).encode()).hexdigest()


def decode_mode(photo):
 """观察原生标记，不把缺字段或布尔值提升为解码证明。"""
 if not isinstance(photo,dict) or photo.get('kind')!='raw' or 'previewOnly' not in photo:return 'UNKNOWN'
 if photo['previewOnly'] is None:return 'FULL_RAW_REPORTED'
 if isinstance(photo['previewOnly'],str) and photo['previewOnly'].strip():return 'PREVIEW_FALLBACK'
 return 'UNKNOWN'


def camera_matches(sample,observed):
 if not isinstance(observed,str):return False
 norm=lambda value:re.sub(r'\s+',' ',value.strip().casefold())
 make=norm(sample['make']);model=norm(sample['model']);value=norm(observed)
 aliases={'nikon':['nikon corporation','nikon'],'canon':['canon'],'blackmagic':['blackmagic design','blackmagic']}.get(make,[make])
 def strip(text):
  found=False
  while True:
   prefix=next((a+' ' for a in aliases if text.startswith(a+' ')),None)
   if prefix is None:return text,found
   text=text[len(prefix):];found=True
 model,_=strip(model);value,found=strip(value);return found and model==value


def inspect_raw(path):
 """核对报告与实际原片/回执/产物；旧记录只读，不授权执行。"""
 gateway=module('command_gateway');report=gateway.strict_json(Path(path).read_text())
 base={'readOnly':True,'taskExecutionAllowed':False,'deliveryAllowed':False,'automaticReplay':False}
 if not isinstance(report,dict):raise ValueError('raw_report_invalid')
 if type(report.get('schemaVersion')) is not int or report.get('schemaVersion')!=1 or report.get('reportKind')!='raw-samples':return dict(base,compatible=False,scope='legacy RAW report; no current capability proof')
 manifest=report.get('manifest')
 if not isinstance(manifest,dict) or digest(manifest)!=report.get('manifestSha256'):raise ValueError('raw_manifest_identity_mismatch')
 samples=manifest.get('samples');records=report.get('samples')
 if type(manifest.get('schemaVersion')) is not int or manifest.get('schemaVersion')!=1 or not isinstance(samples,list) or not 1<=len(samples)<=64 or not isinstance(records,list) or len(records)!=len(samples):raise ValueError('raw_samples_invalid')
 resources=report.get('executionResourceSha256');native=report.get('runtimeIdentity',{});snapshot=ROOT/'skills/lightcraft-use/scripts';lock=gateway.strict_json((snapshot/'runtime.lock.json').read_text())
 if not isinstance(resources,dict) or resources.get('runtime.lock.json')!=gateway.file_sha(snapshot/'runtime.lock.json'):raise ValueError('raw_runtime_lock_mismatch')
 if not isinstance(native,dict):raise ValueError('raw_native_identity_mismatch')
 if native.get('version')!=lock['resolvedVersion'] or native.get('binarySha256') not in {a['binarySha256'] for a in lock['artifacts'].values()}:raise ValueError('raw_native_identity_mismatch')
 seen=set();runs=set();source_hashes=set();results=[]
 for sample,record in zip(samples,records):
  required={'sampleId','make','model','variant','license','licenseUrl','sourceUrl','catalogUrl','path','bytes','sha256'}
  if not isinstance(sample,dict) or not required<=set(sample) or any(not isinstance(sample.get(k),str) or not sample[k].strip() for k in required-{'bytes'}):raise ValueError('raw_sample_metadata_invalid')
  for key in ('licenseUrl','sourceUrl','catalogUrl'):
   url=urlsplit(sample[key])
   if url.scheme!='https' or not url.hostname or url.username or url.password or url.fragment:raise ValueError('raw_source_url_invalid')
  if sample['sampleId'] in seen or type(sample['bytes']) is not int or sample['bytes']<=0 or not re.fullmatch('[0-9a-f]{64}',sample['sha256']):raise ValueError('raw_sample_identity_invalid')
  if sample['sha256'] in source_hashes:raise ValueError('raw_duplicate_source')
  source_hashes.add(sample['sha256']);seen.add(sample['sampleId'])
  if not isinstance(record,dict) or any(record.get(k)!=v for k,v in sample.items()):raise ValueError('raw_sample_report_mismatch')
  source=Path(sample['path'])
  if source.is_symlink() or not source.is_file() or source.stat().st_size!=sample['bytes'] or gateway.file_sha(source)!=sample['sha256']:raise ValueError('raw_original_changed_or_missing')
  if 'catalogEntryPath' in sample or 'catalogEntrySha256' in sample:
   if not {'catalogEntryPath','catalogEntrySha256'}<=set(sample):raise ValueError('raw_catalog_identity_missing')
   entry_path=Path(sample['catalogEntryPath'])
   if entry_path.is_symlink() or not entry_path.is_file() or entry_path.stat().st_size>65536:raise ValueError('raw_catalog_entry_invalid')
   entry=gateway.strict_json(entry_path.read_text())
   if (digest(entry)!=sample['catalogEntrySha256'] or not isinstance(entry,list) or len(entry)<8 or entry[:3]!=[sample['make'],sample['model'],sample['variant']]
       or not isinstance(entry[5],str) or sample['licenseUrl'] not in entry[5] or not isinstance(entry[7],str) or sample['sha256'] not in entry[7] or sample['sourceUrl'] not in entry[7]):raise ValueError('raw_catalog_metadata_mismatch')
  paths=record.get('receipts');plans=record.get('plans');read={}
  if not isinstance(paths,dict) or not isinstance(plans,dict) or not paths or set(paths)!=set(plans) or set(paths)-{'import','edit-export','reopen'}:raise ValueError('raw_receipts_invalid')
  for name,receipt_path in paths.items():
   value=gateway.read_receipt(receipt_path)
   if not value['compatible']:raise ValueError('raw_current_receipt_required')
   receipt=value['receipt'];plan=plans[name];gateway.validate_shape('lightcraft',plan)
   expected={str(source.resolve()):sample['sha256']}
   if (receipt['planSha256']!=digest(plan) or receipt.get('skillResourceSha256')!=resources or receipt.get('skillResourceAfterSha256')!=resources
       or receipt.get('runtimeLockSha256')!=resources['runtime.lock.json'] or receipt.get('inputSha256')!=expected or receipt.get('inputAfterSha256')!=expected):raise ValueError('raw_receipt_identity_mismatch')
   identity=receipt.get('runtimeIdentity',{})
   if identity.get('version')!=native['version'] or identity.get('binarySha256')!=native['binarySha256'] or identity.get('mode')!='Headless':raise ValueError('raw_receipt_runtime_mismatch')
   if receipt['runId'] in runs:raise ValueError('raw_reused_session')
   runs.add(receipt['runId']);read[name]=receipt
  imported=read.get('import');status=record.get('nativeAcceptance')
  if imported is None:raise ValueError('raw_import_receipt_required')
  if plans['import']['steps']!=[{'command':'library.import','params':{'paths':[str(source.resolve())],'mode':'add'}},{'command':'catalog.query','params':{'limit':10}}]:raise ValueError('raw_import_plan_mismatch')
  if status=='UNSUPPORTED':
   process=imported.get('process',{})
   if process.get('status')!='EXITED' or process.get('exitCode')!=0 or process.get('logComplete') is not True:raise ValueError('raw_process_unconfirmed')
   row=imported['steps'][0];result=row.get('native',{}).get('result',{});failed=result.get('failed');reason=None
   if (imported.get('status')=='FAILED_OR_PARTIAL' and imported.get('protocolComplete') is True and row.get('command')=='library.import' and row.get('status')=='PARTIAL'
       and row.get('native',{}).get('ok') is True and not result.get('imported') and not result.get('duplicates') and isinstance(failed,list) and len(failed)==1 and isinstance(failed[0],list) and len(failed[0])==2 and failed[0][0]==str(source.resolve())):reason=failed[0][1]
   if not isinstance(reason,str) or not (reason.startswith('unsupported raw (') or reason=='RawOther files are not supported yet') or record.get('decodeMode')!='UNKNOWN' or record.get('fullRawAcceptance')!='NOT_PROVEN' or set(read)!={'import'}:raise ValueError('raw_unsupported_claim_inconsistent')
  elif status in ('PASS','PASS_WITH_PREVIEW_FALLBACK'):
   if set(read)!={'import','edit-export','reopen'}:raise ValueError('raw_success_receipts_incomplete')
   for name,receipt in read.items():
    rows=receipt['steps'];steps=plans[name]['steps']
    if (receipt['status']!='NATIVE_EXIT_ZERO_REVIEW_REQUIRED' or receipt.get('protocolComplete') is not True or len(rows)!=len(steps)
        or any(row.get('index')!=i or row.get('command')!=steps[i]['command'] or row.get('status')!='SUCCEEDED' for i,row in enumerate(rows))):raise ValueError('raw_success_inconsistent')
   for receipt in read.values():
    process=receipt.get('process',{})
    if process.get('status')!='EXITED' or process.get('exitCode')!=0 or process.get('logComplete') is not True:raise ValueError('raw_process_unconfirmed')
   report_import=imported['steps'][0]['native']['result'];identifier=record.get('photoId')
   if type(identifier) is not int or identifier<=0 or report_import.get('imported')!=[identifier] or report_import.get('failed') or report_import.get('duplicates'):raise ValueError('raw_import_photo_mismatch')
   def step(command,**params):return {'command':command,'params':params}
   export_path=record.get('artifact',{}).get('path')
   expected_edit=[step('library.select',ids=[identifier],active=identifier),step('develop.set',control='light.exposure',value=.25),step('develop.get',id=identifier),step('app.export',path=export_path,format='png',width=256),step('catalog.query',limit=10),step('photo.inspect',id=identifier)]
   expected_reopen=[step('library.select',ids=[identifier],active=identifier),step('photo.inspect',id=identifier),step('develop.get',id=identifier),step('library.info')]
   if plans['edit-export']['steps']!=expected_edit or plans['reopen']['steps']!=expected_reopen:raise ValueError('raw_plan_parameters_mismatch')
   edit=read['edit-export'];reopen=read['reopen'];commands=lambda name:[s['command'] for s in plans[name]['steps']]
   if commands('edit-export')!=['library.select','develop.set','develop.get','app.export','catalog.query','photo.inspect'] or commands('reopen')!=['library.select','photo.inspect','develop.get','library.info']:raise ValueError('raw_plan_sequence_mismatch')
   catalog=edit['steps'][4]['native']['result'].get('photos',[]);photos=[photo for photo in catalog if photo.get('id')==identifier]
   if len(photos)!=1:raise ValueError('raw_catalog_photo_mismatch')
   photo=photos[0];mode=decode_mode(photo)
   if not camera_matches(sample,photo.get('camera')) or photo.get('camera')!=record.get('observedCamera') or record.get('cameraIdentity')!='MATCH':raise ValueError('raw_camera_mismatch')
   if mode!=record.get('decodeMode') or (status=='PASS')!=(mode=='FULL_RAW_REPORTED') or mode=='UNKNOWN':raise ValueError('raw_decode_claim_inconsistent')
   if record.get('fullRawAcceptance')!=('REPORTED_BY_RUNTIME' if mode=='FULL_RAW_REPORTED' else 'NOT_PROVEN'):raise ValueError('raw_full_acceptance_inconsistent')
   before=edit['steps'][5]['native']['result'];after=reopen['steps'][1]['native']['result'];settings=edit['steps'][2]['native']['result'];info=reopen['steps'][3]['native']['result']
   if before.get('id')!=identifier or after.get('id')!=identifier or before.get('source')!=after.get('source') or before.get('source')!={'type':'file','path':str(source.resolve())}:raise ValueError('raw_reopen_photo_mismatch')
   if not gateway.json_equal(before.get('develop'),settings) or not gateway.json_equal(after.get('develop'),settings):raise ValueError('raw_photo_settings_mismatch')
   if edit.get('libraryPath')!=reopen.get('libraryPath') or not gateway.json_equal(settings,reopen['steps'][2]['native']['result']) or info.get('persistent') is not True or info.get('unsavedOps')!=0:raise ValueError('raw_reopen_unconfirmed')
   artifact=record.get('artifact',{});target=Path(artifact.get('path',''))
   if target.is_symlink() or not target.is_file() or not target.resolve().is_relative_to(Path(edit['outputRoot']).resolve()) or module('artifacts').sha(target)!=artifact.get('sha256') or artifact.get('technicalStatus')!='PASS':raise ValueError('raw_export_identity_mismatch')
   fresh=module('artifacts').verify(target,Path(edit['outputRoot']),{'format':'png','width':256})
   if fresh.get('technicalStatus')!='PASS':raise ValueError('raw_export_decode_unconfirmed')
  elif status not in ('FAILED','UNCONFIRMED'):raise ValueError('raw_acceptance_status_invalid')
  elif record.get('fullRawAcceptance')!='NOT_PROVEN':raise ValueError('raw_failed_cannot_claim_full_acceptance')
  results.append({k:record.get(k) for k in ('sampleId','make','model','variant','sha256','nativeAcceptance','decodeMode','fullRawAcceptance','cameraIdentity','observedCamera','previewOnlyReason','error')})
 return dict(base,compatible=True,sourceSnapshotMatches=gateway.capture_resources(snapshot)==resources,runtimeIdentity=native,samples=results,scope='sample-bound runtime reports only; no all-camera support or visual acceptance')
