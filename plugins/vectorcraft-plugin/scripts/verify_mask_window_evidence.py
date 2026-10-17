#!/usr/bin/env python3
"""核对拥有的窗口蒙版验收身份及实际像素样本，不提升全部GUI资格。"""
import hashlib,importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT='docs/evidence/vectorcraft-mask-window-fixed64-20261009.json'
def era_identity(root,report):
    """收敛后 docs/current-identity.json 只描述当前世界；历史报告按执行时归档身份核对。"""
    def matches(identity):return identity['pluginVersion']==report['pluginVersion'] and identity['skillSource']['ref']==report['sourceRef'] and identity['skillSource']['sha']==report['sourceCommit']
    current=json.loads((root/'docs/current-identity.json').read_text())
    if matches(current):return current
    candidates={}
    for base in (root,ROOT):
        archived=base/'docs/evidence/pre-harness-convergence-identity'
        if not archived.is_dir():continue
        for path in sorted(archived.glob('*/docs/current-identity.json')):
            try:candidate=path.read_bytes()
            except OSError:continue
            if matches(json.loads(candidate)):candidates[hashlib.sha256(candidate).hexdigest()]=json.loads(candidate)
    if len(candidates)!=1:raise ValueError('mask_window_identity')
    return next(iter(candidates.values()))
def verify(root=ROOT):
    r=json.loads((root/REPORT).read_text());identity=era_identity(root,r);host=json.loads((root/'docs/evidence/vectorcraft-public-tag64-install-20261009.json').read_text())
    if r['schema']!='vectorcraft-mask-window/v1' or r['result']!='PASS' or r['command']!='transparency.viewOpacityMask' or r['tasksClosed']!=[]:raise ValueError('mask_window_report')
    for k in ('pluginVersion','pluginCommit','sourceRef','sourceCommit','hostVersion','platform'):
        if r[k]!=host[k]:raise ValueError('mask_window_fixed_identity')
    if r['installedSkillsBefore']!=identity['skills'] or r['installedSkillsAfter']!=identity['skills'] or r['runtimeSha256']!=identity['runtime']['binarySha256'] or r['desktopBinarySha256']!=identity['desktop']['binarySha256']:raise ValueError('mask_window_identity')
    if any(r[k] is not True for k in ('sourcePreserved','maskArtPreserved','listenerOwnedByPID','allOwnedProcessesStopped')):raise ValueError('mask_window_ownership')
    family=json.loads((root/'docs/evidence/vectorcraft-command-transparency-fixed64-20261009.json').read_text())
    source=next(c for c in family['cases'] if c['command']=='transparency.viewOpacityMask')['stages'][0]['nativeProjectSha256']
    if r['sourceProjectSha256']!=source:raise ValueError('mask_window_source_binding')
    path=root/'scripts/qa/command_mask_window.py';spec=importlib.util.spec_from_file_location('mask_window_samples',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    if r['driverSha256']!=hashlib.sha256(path.read_bytes()).hexdigest():raise ValueError('mask_window_driver')
    if [s['on'] for s in r['stages']]!=[True,False]:raise ValueError('mask_window_stages')
    for s in r['stages']:
        if (s['width'],s['height'])!=(1440,900) or s['sampleCoordinates']!=[[250,270],[310,340],[380,410]] or s['returned']!={'id':2,'on':s['on']} or s['info']['editingMask']!=2 or s['ui']['activeDocument'] is None:raise ValueError('mask_window_native_state')
        w=s['window'];digest=w['sha256']
        if w['mimeType']!='image/png' or w['bytes']<=0 or len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):raise ValueError('mask_window_image')
        m.sample_check(s['samples'],s['on'])
    if r['stages'][0]['window']['sha256']==r['stages'][1]['window']['sha256']:raise ValueError('mask_window_unchanged')
    # 收敛后按执行时归档核对依赖字节：当前文件 → 证据索引归档 → 收敛前执行身份归档。
    index_path=root/'docs/evidence-index.json'
    known=next((e['dependencies'] for e in json.loads(index_path.read_text())['entries'] if e['path']==REPORT),{}) if index_path.is_file() else {}
    def bound(name,digest):
        path=root/name
        if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==digest:return
        archived=[base/p for base in (root,ROOT) for p,h in known.items() if h==digest and p.endswith('/'+name) and (base/p).is_file()]
        archived+=[p for base in (root,ROOT) if (base/'docs/evidence/pre-harness-convergence-identity').is_dir() for p in sorted((base/'docs/evidence/pre-harness-convergence-identity').glob('*/'+name)) if p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==digest]
        if len({p.read_bytes() for p in archived})!=1:raise ValueError('mask_window_dependency')
    for name,digest in r['fingerprints'].items():bound(name,digest)
    return {'result':'PASS','windows':2,'tasksClosed':[],'scope':'viewOpacityMask owned desktop window only'}
if __name__=='__main__':print(json.dumps(verify()))
