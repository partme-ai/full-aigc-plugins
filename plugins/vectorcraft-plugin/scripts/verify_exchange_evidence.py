#!/usr/bin/env python3
"""核对 VC-DM-005 当前场景和固定安装原生证据。"""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def payload_name(name):
    """执行载荷收敛在 vectorcraft-harness：历史证据绑定的 skills/<domain>/scripts/ 路径按字节等价映射到 harness。"""
    if isinstance(name, str):
        prefix = 'skills/vectorcraft-'
        if name.startswith(prefix) and '/scripts/' in name and not (ROOT/name).is_file():
            candidate = 'skills/vectorcraft-harness/scripts/' + name.split('/scripts/', 1)[1]
            if (ROOT/candidate).is_file():
                return candidate
    return name

REPORT='docs/evidence/vectorcraft-exchange-qualified55-20261009.json'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def local(name):
    name = payload_name(name)
    if not isinstance(name,str) or '\\' in name or any(x in ('','.','..') for x in name.split('/')) or Path(name).is_absolute():raise ValueError('invalid_evidence_path')
    p=ROOT/name
    if not p.resolve().is_relative_to(ROOT.resolve()) or any(x.is_symlink() for x in [p,*p.parents] if x.is_relative_to(ROOT)):raise ValueError('invalid_evidence_path')
    return p

def main():
    report=json.loads(local(REPORT).read_text())
    index=json.loads(local('docs/evidence-index.json').read_text())
    known=next(e['dependencies'] for e in index['entries'] if e['path']==REPORT)
    def bound(name):
        digest=report['fingerprints'][name]
        if sha(local(name))==digest:return local(name)
        archived=[p for p,saved in known.items() if saved==digest and p.endswith('/'+name)]
        if len(archived)!=1 or sha(local(archived[0]))!=digest:raise ValueError('stale_exchange_evidence')
        return local(archived[0])
    for name in report['fingerprints']:bound(name)
    def read(name):
        if name not in report['fingerprints']:raise ValueError('unbound_exchange_evidence')
        return json.loads(bound(name).read_text())
    if report['result']!='PASS' or report['tasksClosed']!=['4.15']:raise ValueError('incomplete_exchange')
    spec='openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md'
    block=local(spec).read_text().split('### Requirement: VC-DM-005 ',1)[1].split('### Requirement:',1)[0]
    contracts={part.splitlines()[0].split()[0]:hashlib.sha256(part.strip().encode()).hexdigest() for part in block.split('#### Scenario: ')[1:]}
    matrix=read(report['scenarioMatrix'])
    if matrix['scenarioContracts']!=contracts or {x['scenario'] for x in matrix['entries']}!=set(contracts) or len(matrix['entries'])!=2:raise ValueError('scenario_coverage')
    for row in matrix['entries']:
        if row['level']!='native-fixed-install' or row['report']!=report['native'] or not row['checks']:raise ValueError('scenario_coverage')
    host=read(report['host']);lock=read('skills.lock.json')['sources'][0]
    if host['pluginCommit']!=report['pluginCommit'] or host['skillSourceCommit']!=report['sourceCommit'] or host['skillSourceRef']!=report['sourceRef'] or host['pluginVersion']!=report['pluginVersion'] or host['platform']!=report['platform']:raise ValueError('host_identity')
    if len(host['skills'])!=13 or {x['name']:x['sha256'] for x in host['skills']}!=lock['sha256'] or host['skillsUnchangedAfterQa']!=13 or host['installedQualitySha256']!=sha(bound('src/evaluation/delivery_quality.py')):raise ValueError('host_identity')
    native=read(report['native'])
    if native['driverSha256']!=sha(local(report['driver'])) or native['runtimeSha256']!=report['runtimeSha256'] or native['platform']!=report['platform'] or native['level']!='fixed-install' or native['result']!='PASS':raise ValueError('native_identity')
    skill_digest=hashlib.sha256(''.join(name+'\0'+digest+'\n' for name,digest in sorted(native['skillFiles'].items())).encode()).hexdigest()
    if skill_digest!=lock['sha256']['vectorcraft-cli-export']:raise ValueError('native_skill_identity')
    if any(native[key] is not True for key in ['sourceAndPreviousExportsPreserved','nativeGradientEditableAfterIndependentReopen','automaticRasterizationWithoutExpand']):raise ValueError('native_preservation')
    before=native['sourceNativeModel'];after=native['exportedNativeModel']
    if before['layers']!=after['layers'] or before['artboards']!=after['artboards'] or before['metadata']['created']!=after['metadata']['created']:raise ValueError('native_preservation')
    points=native['originalPoints']['points'];edited=native['editedPoints']['points']
    if len(points)<2 or len(points)!=len(edited) or points[0]['color']==edited[0]['color'] or points[1:]!=edited[1:] or {k:v for k,v in points[0].items() if k!='color'}!={k:v for k,v in edited[0].items() if k!='color'}:raise ValueError('native_preservation')
    if native['exportPlan']['operations'] or any(x.get('params',{}).get('command')=='effect.expandAppearance' or x['command']=='effect.expandAppearance' for x in native['plan']['operations']):raise ValueError('not_automatic_fallback')
    mf=native['manifest'];files=native['exportedFiles'];loss=native['lossReport']
    if mf['runtimeSha256']!=report['runtimeSha256']:raise ValueError('native_identity')
    if mf['sourceProjectSha256']!=native['originalFiles']['project.vectorcraft'] or loss['native']['sha256']!=files['project.vectorcraft'] or any(files[k]!=v for k,v in mf['files'].items()):raise ValueError('native_file_binding')
    if {x['format'] for x in native['decoded']}!={'svg','pdf','png'} or len(native['decoded'])!=3 or any(x['result']!='PASS' or x['size']!=[96,80] for x in native['decoded']):raise ValueError('missing_export_decode')
    for row in loss['outputs']:
        name=row.get('location',row.get('path'))
        if row['sha256']!=files[name]:raise ValueError('output_binding')
    svg=next(x for x in loss['outputs'] if x['format']=='svg');scope=svg['observations']['rasterizationScope']
    if scope['vectorOnly'] is not False or scope['losslessVectorClaimAllowed'] is not False or len(scope['elements'])!=1 or scope['elements'][0]['geometry']!={'x':'12','y':'16','width':'60','height':'40'} or scope['elements'][0]['payloadSha256']!=native['rasterPayloadSha256'] or not any(x['code']=='lossless-vector-claim' and x.get('status')=='blocked' for x in svg['changes']):raise ValueError('raster_disclosure')
    required={'undisclosed-raster','wrong-scope','unblocked-claim','corrupt-embedded-png','corrupt-pdf','corrupt-png','corrupt-native'}
    if {x['fault'] for x in native['refusals']}!=required or len(native['refusals'])!=7:raise ValueError('missing_refusal')
    for row in native['refusals']:
        if row['result']!='PASS' or row['explicitQaMutation'] is not True:raise ValueError('failed_refusal')
        if row['fault']=='corrupt-native':
            if not row['knownNativeRefusal'] or 'outcome_unknown' in row['knownNativeRefusal']:raise ValueError('failed_refusal')
        elif row['freshMatchingManifestHashes'] is not True or row['quality']['artifactIntegrityStatus']!='PASS' or row['quality']['technicalStatus']!='FAIL' or row['quality']['acceptanceStatus']!='blocked':raise ValueError('failed_refusal')
    if native['quality']['technicalStatus']!='PASS' or native['quality']['creativeStatus']!='NOT_RUN':raise ValueError('technical_scope')
    print(json.dumps({'result':'PASS','scope':'both current VC-DM-005 scenarios on fixed55/source41 macOS arm64 only','scenarios':2,'decodedExports':3,'refusals':7,'taskClosed':'4.15'}))
if __name__=='__main__':main()
