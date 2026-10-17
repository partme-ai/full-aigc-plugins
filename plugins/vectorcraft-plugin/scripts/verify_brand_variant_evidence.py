#!/usr/bin/env python3
"""核对 VC-DM-006 当前六场景的固定安装、真实依赖边与异常保全证据。"""
import ast
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

REPORT='docs/evidence/vectorcraft-brand-variants-fixed56-20261009.json'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def local(name):
    name = payload_name(name)
    if not isinstance(name,str) or '\\' in name or Path(name).is_absolute() or any(x in ('','.','..') for x in name.split('/')):raise ValueError('invalid_evidence_path')
    p=ROOT/name
    if not p.resolve().is_relative_to(ROOT.resolve()) or any(x.is_symlink() for x in [p,*p.parents] if x.is_relative_to(ROOT)):raise ValueError('invalid_evidence_path')
    return p

def main():
    report=json.loads(local(REPORT).read_text())
    index=json.loads(local('docs/evidence-index.json').read_text())
    known=next((x['dependencies'] for x in index['entries'] if x['path']==REPORT),{})
    def bound(name):
        digest=report['fingerprints'][name]
        if sha(local(name))==digest:return local(name)
        archived=[p for p,h in known.items() if h==digest and p.endswith('/'+name)]
        if len(archived)!=1 or sha(local(archived[0]))!=digest:raise ValueError('stale_brand_variants')
        return local(archived[0])
    def read(name):
        if name not in report['fingerprints']:raise ValueError('unbound_brand_evidence')
        return json.loads(bound(name).read_text())
    def digest(files):return hashlib.sha256(''.join(n+'\0'+h+'\n' for n,h in sorted(files.items())).encode()).hexdigest()
    for name in report['fingerprints']:bound(name)
    if report['result']!='PASS' or report['tasksClosed']!=['4.18']:raise ValueError('incomplete_brand_variants')
    spec=local('openspec/changes/establish-v1-plugin/specs/domain-workflow/spec.md').read_text()
    block=spec.split('### Requirement: VC-DM-006 ',1)[1].split('### Requirement:',1)[0]
    contracts={part.splitlines()[0].split()[0]:hashlib.sha256(part.strip().encode()).hexdigest() for part in block.split('#### Scenario: ')[1:]}
    matrix=read(report['scenarioMatrix'])
    if matrix['scenarioContracts']!=contracts or len(matrix['entries'])!=len(contracts) or {r['scenario'] for r in matrix['entries']}!=set(contracts):raise ValueError('scenario_coverage')
    host=read(report['host']);integrity=read(report['installedIntegrity']);lock=read('skills.lock.json')['sources'][0]
    expected={r['name']:r['sha256'] for r in host['skills']}
    if len(host['skills'])!=13 or expected!=lock['sha256'] or integrity['digests']!=expected or integrity['skillsUnchanged']!=13 or host['skillsUnchangedAfterQa']!=13:raise ValueError('installed_identity')
    if host['pluginCommit']!=report['pluginCommit'] or host['pluginVersion']!=report['pluginVersion'] or host['skillSourceCommit']!=report['sourceCommit'] or host['skillSourceRef']!=report['sourceRef'] or host['platform']!=report['platform'] or lock['sha']!=report['sourceCommit'] or lock['ref']!=report['sourceRef']:raise ValueError('installed_identity')
    if read('plugin.json')['version']!=report['pluginVersion'] or read('docs/current-identity.json')['runtime']['binarySha256']!=report['runtimeSha256']:raise ValueError('runtime_identity')
    native={key:read(name) for key,name in report['native'].items()}
    a,g,b,u=(native[k] for k in ['assets','gateway','guard','unknown'])
    for key,row in native.items():
        if row.get('runtimeSha256',row.get('nativeRuntimeSha256'))!=report['runtimeSha256']:raise ValueError('runtime_identity')
        if key!='gateway' and row['driverSha256']!=sha(bound(report['drivers'][key])):raise ValueError('driver_identity')
    if digest(a['originFiles'])!=expected['vectorcraft-cli-assets'] or a['originFiles']!=a['copiedFiles'] or digest(g['skillFiles'])!=expected['vectorcraft-cli-export'] or digest(u['skillFiles'])!=expected['vectorcraft-cli-export']:raise ValueError('native_skill_identity')
    # 故障只注入隔离副本；将实际改动的会话脚本与未修改发布字节逐项核对。
    for key,files,original,append in [('assets',a['instrumentedFiles'],a['originFiles'],a['qaInstrumentation'])]:
        name='skills/vectorcraft-cli-assets/scripts/mcp_session.py'
        expected_files={**original,'scripts/mcp_session.py':hashlib.sha256(bound(name).read_bytes()+append.encode()).hexdigest()}
        if files!=expected_files:raise ValueError('qa_instrumentation_identity')
    driver=ast.parse(bound(report['drivers']['guard']).read_text())
    proxy=next(ast.literal_eval(n.value) for n in driver.body if isinstance(n,ast.Assign) and any(isinstance(k,ast.Name) and k.id=='PROXY' for k in n.targets))
    original_session=bound('skills/vectorcraft-cli-appearance/scripts/mcp_session.py').read_bytes()
    instrumented=b['instrumentedSkillFiles']
    if instrumented['scripts/mcp_session.py']!=hashlib.sha256(original_session+('\nimport os\n'+proxy).encode()).hexdigest() or digest({**instrumented,'scripts/mcp_session.py':hashlib.sha256(original_session).hexdigest()})!=expected['vectorcraft-cli-appearance']:raise ValueError('qa_instrumentation_identity')
    if a['result']!='PASS' or a['level']!='fixed-install' or a['sourceAndInstalledSkillPreserved'] is not True or a['explicitEmptyExportsPreserved'] is not True:raise ValueError('asset_dependency')
    if len(a['checks'])!=2 or {x['asset'] for x in a['checks']}!={'logo','mark'}:raise ValueError('asset_dependency')
    for check in a['checks']:
        if check['status']!='passed' or len(check['consumerIds'])!=2 or check['affectedObjectIds'] or check['boundsMismatchObjectIds'] or check['unexpectedDependencies'] or check['artboardsChanged'] or check['checkpointRetained'] is not False:raise ValueError('asset_dependency')
        if {int(k) for k in check['replacementMapping']}!=set(check['consumerIds']) or sorted(i for ids in check['replacementMapping'].values() for i in ids)!=check['replacementIds']:raise ValueError('asset_dependency')
    mf=a['manifest']
    if mf['sourceProjectSha256']!=a['sourceFiles']['project.vectorcraft'] or any(a['updatedFiles'][k]!=v for k,v in mf['files'].items()):raise ValueError('asset_file_binding')
    body=json.dumps({'schema':'vectorcraft-brand-dependencies/v1','checks':a['checks']},ensure_ascii=False,indent=2)+'\n'
    if hashlib.sha256(body.encode()).hexdigest()!=mf['brandDependencyReport']['sha256'] or mf['brandDependencyReport']['sha256']!=a['updatedFiles']['brand-dependencies.json']:raise ValueError('asset_file_binding')
    wanted={'artboard-'+str(i)+'.'+fmt for i in range(1,4) for fmt in ['svg','pdf','png']}
    if len(a['decoded'])!=9 or {x['path'] for x in a['decoded']}!=wanted:raise ValueError('unrelated_exports')
    for row in a['decoded']:
        same=a['sourceFiles'][row['path']]==a['updatedFiles'][row['path']]
        if row['result']!='PASS' or row['sha256']!=a['updatedFiles'][row['path']] or row['unrelatedUnchanged'] is not same or same is not row['path'].startswith('artboard-3.'):raise ValueError('unrelated_exports')
    fault=a['fault'];check=fault['check']
    if fault['result']!='PASS' or fault['explicitQaNativeMutation'] is not True or fault['injection'].get('isError',False) or check['status']!='failed' or not check['affectedObjectIds'] or not check['unexpectedDependencies'] or check['checkpointRetained'] is not True or fault['checkpointIndependentlyReopened'] is not True or fault['retainedFilesVerified'] is not True or fault['failure']['replayAllowed'] is not False:raise ValueError('asset_refusal')
    if {x['fault'] for x in a['preflight']}!={'tampered-plan','linked-plan','unknown-asset'} or any(x['result']!='PASS' or x['beforeRuntimeAndOutput'] is not True for x in a['preflight']):raise ValueError('asset_refusal')
    if g['result']!='PASS' or len(g['cases'])!=2 or {x['mode'] for x in g['cases']}!={'direct','native-gateway'} or not all(g[k] is True for k in ['explicitEmptyExportsRespected','tamperedPlanRefusedBeforeInstallation','skillFilesUnchanged']):raise ValueError('gateway_coverage')
    for row in g['cases']:
        if row['inheritedOutputs']!=9 or not all(row[k] is True for k in ['boundPreviewChanged','unrelatedSVGPNGPDFFilesUnchanged','sourcePreserved','guardPassed']):raise ValueError('gateway_coverage')
    modes={route+'-'+kind for route in ['direct','native-gateway'] for kind in ['nonconsumer','consumer-geometry','consumer-text','consumer-stroke']}
    if b['status']!='passed' or b['fixedInstalled'] is not True or len(b['failures'])!=8 or {x['mode'] for x in b['failures']}!=modes:raise ValueError('guard_coverage')
    for row in b['failures']:
        if row['injectionCount']!=1 or row['retainedFileHashesVerified'] is not True or row['checkpointIndependentlyReopened'] is not True or row['report']['status']!='failed' or row['report']['checkpointRetained'] is not True or not row['report']['unexpectedDependencies']:raise ValueError('guard_coverage')
    if b['healthyReport']['checks'][0]['status']!='passed' or b['healthyReport']['checks'][0]['checkpointRetained'] is not False:raise ValueError('guard_coverage')
    if u['result']!='PASS' or u['level']!='fixed-install' or not all(u[k] is True for k in ['unknownSwatchRefused','noSuccessManifest','checkpointIndependentlyReopened','sourceAndSkillPreserved']) or u['replayAllowed'] is not False or 'outcome_unknown' in u['reason']:raise ValueError('unknown_refusal')
    if {x['mode'] for x in u['linkedPlanRefusals']}!={'direct','native-gateway'} or len(u['linkedPlanRefusals'])!=2 or any(x['result']!='PASS' or x['beforeRuntimeAndOutput'] is not True for x in u['linkedPlanRefusals']):raise ValueError('unknown_refusal')
    checks=0
    for row in matrix['entries']:
        if not row['checks'] or any(x['level']!='native-fixed-install' for x in row['checks']):raise ValueError('scenario_coverage')
        for check in row['checks']:
            value=read(check['report'])
            try:
                for part in check['pointer'].split('/')[1:]:value=value[int(part)] if isinstance(value,list) else value[part]
            except (KeyError,IndexError,TypeError) as error:raise ValueError('missing_scenario_receipt') from error
            if value!=check['expected']:raise ValueError('failed_scenario_receipt')
            checks+=1
    print(json.dumps({'result':'PASS','scope':'all six current VC-DM-006 scenarios on fixed56/source42 macOS arm64 only','scenarios':len(contracts),'checks':checks,'taskClosed':'4.18'}))
if __name__=='__main__':main()
