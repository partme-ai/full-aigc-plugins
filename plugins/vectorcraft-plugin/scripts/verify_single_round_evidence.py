#!/usr/bin/env python3
"""校验当前两场景的实际单轮评审证据；不将模型评分当成技术或发行资格。"""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPORT='docs/evidence/vectorcraft-single-round64-20261009.json'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify(root=ROOT):
    report=json.loads((root/REPORT).read_text())
    known={}
    index_path=root/'docs/evidence-index.json'
    if not index_path.is_file():index_path=ROOT/'docs/evidence-index.json'
    if index_path.is_file():
        known=next((e['dependencies'] for e in json.loads(index_path.read_text())['entries'] if e['path']==REPORT),{})
    def bound(name):
        path=root/name
        if Path(name).is_absolute() or '..' in Path(name).parts or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):raise ValueError('single_round_path')
        digest=report['fingerprints'][name]
        if path.is_file() and sha(path)==digest:return path
        archived=[root/p for p,h in known.items() if h==digest and p.endswith('/'+name)]
        if len(archived)!=1 or sha(archived[0])!=digest:raise ValueError('single_round_stale')
        return archived[0]
    for name in report['fingerprints']:bound(name)
    read=lambda name:json.loads(bound(name).read_text())
    if report['result']!='PASS' or report['tasksClosed']!=['9.21'] or report['marketplaceEligible'] is not False:raise ValueError('single_round_scope')
    lock=read('skills.lock.json')['sources'][0]
    if read('plugin.json')['version']!=report['pluginVersion'] or lock['ref']!=report['sourceRef'] or lock['sha']!=report['sourceCommit']:raise ValueError('single_round_identity')
    # 规格裁剪后 VC-QA-003 移出当前规格文件；历史证据按执行时归档规格核对。
    spec_name='openspec/changes/establish-v1-plugin/specs/quality-review/spec.md'
    spec_path=root/spec_name
    spec_text=spec_path.read_text() if spec_path.is_file() else ''
    if '### Requirement: VC-QA-003 ' not in spec_text:
        archived=[base/p for base in (root,ROOT) for p in known if p.endswith('/'+spec_name) and (base/p).is_file() and '### Requirement: VC-QA-003 ' in (base/p).read_text()]
        # 规格裁剪归档统一保存在收敛前执行身份目录；唯一字节版本才可作核对基准。
        for base in (root,ROOT):
            archived+=[p for p in sorted((base/'docs/evidence/pre-harness-convergence-identity').glob('*/'+spec_name)) if p.is_file() and '### Requirement: VC-QA-003 ' in p.read_text()]
        texts={p.read_text() for p in archived}
        if len(texts)!=1:raise ValueError('single_round_spec_archive')
        spec_text=next(iter(texts))
    spec=spec_text.split('### Requirement: VC-QA-003 ',1)[1].split('### Requirement:',1)[0]
    contracts={p.splitlines()[0].split()[0]:hashlib.sha256(p.strip().encode()).hexdigest() for p in spec.split('#### Scenario: ')[1:]}
    matrix=read(report['matrix'])
    if any(set(r['evidence'])!=({'flow.json','revision-phase.json','initial-assessment.json','revised-assessment.json','budget.json'} if r['scenario']=='VC-QA-003-P' else {'receipt-guards.json','malformed-green.log.txt'}) for r in matrix['entries']) or matrix['scenarioContracts']!=contracts or {r['scenario'] for r in matrix['entries']}!=set(contracts) or len(matrix['entries'])!=2 or any(r['result']!='PASS' or not r['evidence'] for r in matrix['entries']):raise ValueError('single_round_scenarios')
    flow=read(report['flow']);phase=read(report['revisionPhase']);initial=read(report['initialAssessment']);revised=read(report['revisedAssessment']);guards=read(report['guards']);budget=read(report['budget'])
    if any(x['result']!='PASS' for x in [flow,guards,budget]):raise ValueError('single_round_execution')
    for assessment,request,feedback,observation in [(initial,flow['initial']['request'],phase['feedback'],flow['initial']['observation']),(revised,flow['revised']['request'],flow['revised']['feedback'],flow['revised']['observation'])]:
        i=request['input'];technical=i['technicalEvidence'];receipt=feedback['receipt'];response=feedback['response']
        preview=str(Path(i['native']).parent/'artboard-1.png')
        if (assessment['kind']!='actual-current-conversation-model-review' or assessment['projectRevision']!=i['projectRevision'] or assessment['previewSha256']!=request['fingerprints'][preview]
                or assessment['reviewer']['kind']!='host-model' or assessment['reviewer']['independenceEvidence'] is not None or 'view_image' not in assessment['reviewer']['contextOrigin']):raise ValueError('single_round_model_binding')
        if receipt['requestId']!=request['id'] or receipt['bindingHash']!=request['bindingHash'] or receipt['scores']!=assessment['scores'] or receipt['issues']!=assessment['issues'] or receipt['reviewer']!=assessment['reviewer']:raise ValueError('single_round_receipt_binding')
        if response['independent'] is not False or response['state']!='revision_proposed' or response['acceptanceStatus']!='pending':raise ValueError('single_round_creative_claim')
        if (i['technicalEvidenceOrigin']!='checked-decoder' or technical['technicalStatus']!='PASS' or technical['artifactIntegrityStatus']!='PASS' or technical['projectRevision']!=i['projectRevision']
                or technical['runtimeIdentity']!=report['runtimeSha256'] or any(technical[k]!='NOT_RUN' for k in ['engineeringStatus','nativeReopenStatus','creativeStatus']) or len(technical['outputs'])!=3 or any(o['status']!='PASS' for o in technical['outputs'])):raise ValueError('single_round_technical_claim')
        if (observation['result']!='PASS' or observation['nativeReopen'] is not True or observation['sourceUnchanged'] is not True or observation['sourceProjectSha256']!=i['projectRevision']
                or observation['runtimeSha256']!=report['runtimeSha256'] or observation['driverSha256']!=sha(bound('scripts/qa/review_native_views.py')) or [p['width'] for p in observation['previews']]!=[128,64,32] or observation['previews']!=assessment['inspection']['actualImageViews']):raise ValueError('single_round_previews')
        if not all(assessment['inspection']['exchange'].get(k) for k in ['lost','observed','unknown']):raise ValueError('single_round_loss')
    for artifact in [guards,budget]:
        if artifact['pluginVersion']!=report['pluginVersion'] or artifact['sourceRef']!=report['sourceRef']:raise ValueError('single_round_identity')
    if flow['context']['pluginVersion']!=report['pluginVersion'] or flow['context']['sourceRef']!=report['sourceRef']:raise ValueError('single_round_identity')
    expected_change={'objectId':2,'field':'appearance.items.0.paint','value':{'type':'solid','color':{'model':'rgb','r':0,'g':1,'b':0}}}
    if phase['proposal']['changes']!=[expected_change] or phase['proposal']['authorization']['objects']!=[2] or phase['proposal']['authorization']['fields']!=['appearance.items.0.paint']:raise ValueError('single_round_authorization')
    cycle=flow['cycle'];a=sum(initial['scores'].values())/5;b=sum(revised['scores'].values())/5
    if (flow['sharedAttempts']!=5 or cycle['state']!='stopped' or cycle['reason']!='stagnation' or cycle['rounds']!=1 or not (0<b-a<cycle['policy']['minImprovement'])
            or flow['sourcePreserved'] is not True or flow['textAndGeometryPreserved'] is not True or flow['allGroupsStopped'] is not True or flow['oneExplicitRevision'] is not True):raise ValueError('single_round_stop')
    if budget['sharedAttempts']!=4 or budget['cycle']['reason']!='budget_exceeded' or budget['allGroupsStopped'] is not True:raise ValueError('single_round_budget')
    expected={'malformed-json','duplicate-json-key','schema-extra-field','binding-hash-mismatch','stale-source','stale-candidate','stale-target','stale-rubric','duplicate-receipt'}
    if (len(guards['records'])!=9 or {r['case'] for r in guards['records']}!=expected or any(r['result']!='PASS' or r['attemptsBefore']!=r['attemptsAfter'] or r['rejectionPersisted'] is not True for r in guards['records'])
            or guards['pendingRecovered'] is not True or guards['pendingRequestReused'] is not True or guards['restartCreatedNewReview'] is not False or guards['sharedAttempts']!=1 or guards['targetRoleSeparated'] is not True):raise ValueError('single_round_rejections')
    if len(guards['events'])!=9 or 'synthetic-malformed-secret' in json.dumps(guards['events']):raise ValueError('single_round_audit')
    for event in guards['events']:
        if event['reason']=='invalid_review_json':
            saved=json.loads(event['receipt'])
            if set(saved)!={'sha256','bytes','withheld'} or saved['withheld'] is not True:raise ValueError('single_round_audit')
    if sha(bound(report['beforeModel']))!=flow['initial']['request']['input']['technicalEvidence']['files']['native.json'] or sha(bound(report['afterModel']))!=flow['revised']['request']['input']['technicalEvidence']['files']['native.json']:raise ValueError('single_round_native_binding')
    before=read(report['beforeModel']);after=read(report['afterModel'])
    def object(model,identifier):
        if isinstance(model,dict):
            if model.get('id')==identifier:return model
            for value in model.values():
                found=object(value,identifier)
                if found is not None:return found
        if isinstance(model,list):
            for value in model:
                found=object(value,identifier)
                if found is not None:return found
    if object(before['layers'],3)!=object(after['layers'],3) or before['artboards']!=after['artboards'] or object(before['layers'],2)['kind']!=object(after['layers'],2)['kind'] or object(after['layers'],2)['appearance']['items'][0]['paint']!={'type':'solid','color':{'model':'rgb','r':0,'g':1,'b':0}}:raise ValueError('single_round_preservation')
    expected=json.loads(json.dumps(before))
    object(expected['layers'],2)['appearance']['items'][0]['paint']={'type':'solid','color':{'model':'rgb','r':0,'g':1,'b':0}}
    expected['metadata']['modified']=after['metadata']['modified']
    if expected!=after:raise ValueError('single_round_preservation')
    return {'result':'PASS','scenarios':2,'taskClosed':'9.21','actualCreativeAssessment':True,'creativeAcceptance':'pending; small label issue remains','scope':'current-conversation single round only; not independent,automatic loop or fixed-host distribution'}

if __name__=='__main__':
    print(json.dumps(verify(),ensure_ascii=False))
