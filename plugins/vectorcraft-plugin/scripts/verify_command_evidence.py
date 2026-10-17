#!/usr/bin/env python3
"""复核固定安装逐命令语义并生成完整目录矩阵，保留未执行状态。"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT='docs/evidence/vectorcraft-command-paint-fixed64-20261009.json'
MATRIX='docs/evidence/vectorcraft-command-matrix-fixed64-20261009.json'
CATALOG='skills/vectorcraft-use/references/command-coverage.json'

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def matrix_rows(catalog,passed):
    """按完整固定目录生成逐行状态；未知案例及重复目录拒绝。"""
    ids=[row['id'] for row in catalog['commands']]
    if len(ids)!=len(set(ids)):raise ValueError('command_catalog_duplicate')
    if not set(passed).issubset(ids):raise ValueError('command_case_unknown')
    return [{'id':row['id'],'ownerSkill':row['ownerSkill'],'paramsSha256':digest(row['params']),
             'executionAcceptance':'PASS' if row['id'] in passed else 'NOT_RUN'} for row in catalog['commands']]

def verify(root=ROOT):
    """核验实际快照、参数、重开、控制对象和固定发行身份；不验证创意质量。"""
    report=json.loads((root/REPORT).read_text());catalog=json.loads((root/CATALOG).read_text())
    identity=json.loads((root/'docs/current-identity.json').read_text())
    host=json.loads((root/'docs/evidence/vectorcraft-public-tag64-install-20261009.json').read_text())
    if report.get('schema')!='vectorcraft-command-family/v1' or report.get('result')!='PASS' or report.get('family')!='paint':raise ValueError('command_report_identity')
    for key in ('pluginVersion','pluginCommit','sourceRef','sourceCommit','hostVersion','platform'):
        if report[key]!=host[key]:raise ValueError('command_fixed_identity')
    if report['runtimeSha256']!=identity['runtime']['binarySha256'] or report['desktopBinarySha256']!=identity['desktop']['binarySha256']:raise ValueError('command_runtime_identity')
    if report['catalogSha256']!=sha(root/CATALOG) or report['driverSha256']!=sha(root/'scripts/qa/command_paint.py'):raise ValueError('command_execution_identity')
    if report['allOwnedProcessesStopped'] is not True or report['listenerOwnedByPID'] is not True:raise ValueError('command_session_ownership')
    spec=importlib.util.spec_from_file_location('paint_semantics',root/'scripts/qa/command_paint.py');driver=importlib.util.module_from_spec(spec);spec.loader.exec_module(driver)
    cases=report['cases'];passed=[x['command'] for x in cases]
    if len(passed)!=len(set(passed)) or set(passed)!=set(driver.PAINT_COMMANDS):raise ValueError('command_case_coverage')
    rows={r['id']:r for r in catalog['commands']}
    for case in cases:
        command=case['command']
        if case['result']!='PASS' or case['mode']!='owned-signed-desktop-bridge' or case['sourcePreserved'] is not True or case['previousDeliveryPreserved'] is not True:raise ValueError('command_case_context')
        if [s['round'] for s in case['stages']]!=[1,2]:raise ValueError('command_revision_round')
        for stage in case['stages']:
            context=stage['context']
            if context['id']!=command or context['enabled'] is not True or context['params']!=rows[command]['params']:raise ValueError('command_parameter_context')
            if stage['ui']['activeDocument'] is None:raise ValueError('command_gui_context')
            driver.validate_transition(command,stage)
            if command.startswith('paint.freeform.'):
                for model_key,proxy_key in (('before','freeformBefore'),('after','freeformAfter')):
                    native=driver.paint(stage[model_key]).get('freeform');proxy=stage[proxy_key]
                    if native is None:
                        if model_key=='after' and command not in ('paint.freeform.get','paint.freeform.selectPoint'):raise ValueError('command_freeform_native_missing')
                        # 未物化的自由渐变查询按形状临时生成点；查询不得擅自持久化。
                        continue
                    points=[{'at':[p['at']['x'],p['at']['y']],'color':list(driver.rgb(p['color'])),'opacity':p['opacity'],'spread':p['spread']} for p in native['points']]
                    if points!=proxy['points'] or native.get('lines',[])!=proxy['lines']:raise ValueError('command_freeform_native_binding')
            canvas=stage['canvas']
            if canvas['type']!='image' or canvas['mimeType']!='image/png' or (canvas['width'],canvas['height'])!=(128,96) or canvas['bytes']<=0:raise ValueError('command_canvas_decode')
            if [e['format'] for e in stage['exports']]!=['svg','png'] or any(e['decoded'] is not True for e in stage['exports']):raise ValueError('command_exports_decode')
            for h in [canvas['sha256'],stage['nativeProjectSha256'],*[e['sha256'] for e in stage['exports']]]:
                if len(h)!=64 or any(c not in '0123456789abcdef' for c in h):raise ValueError('command_artifact_digest')
    entries=matrix_rows(catalog,set(passed))
    if len(entries)!=585:raise ValueError('command_catalog_count')
    return {'schema':'vectorcraft-command-matrix/v1','result':'PASS','requirement':'VC-CM-001','tasksClosed':[],
            'pluginVersion':host['pluginVersion'],'pluginCommit':host['pluginCommit'],'sourceRef':host['sourceRef'],
            'report':REPORT,'reportSha256':sha(root/REPORT),'catalogSha256':sha(root/CATALOG),
            'coverage':{'catalogCommands':len(entries),'passed':len(passed),'notRun':len(entries)-len(passed),'stages':2*len(passed)},
            'scope':'Integrity and paint-family native semantics only; incomplete exhaustive command acceptance;native canvas images are not OS-window screenshots or creative review',
            'commands':entries}

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');args=parser.parse_args()
    matrix=verify()
    if args.write:(ROOT/MATRIX).write_text(json.dumps(matrix,ensure_ascii=False,indent=2)+'\n')
    elif json.loads((ROOT/MATRIX).read_text())!=matrix:raise SystemExit('command_matrix_drift')
    print(json.dumps({'result':'PASS',**matrix['coverage'],'tasksClosed':[]}))
