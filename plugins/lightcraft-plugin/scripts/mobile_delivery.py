"""准备及检查移动文件交付包；不连接设备、不运行原生任务或授予视觉通过。"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

CONTRACT=Path(__file__).with_name('craft_exchange.ts')
MANIFEST='delivery-manifest.json'
REPORT='evidence/native-exchange-report.json'
LIMIT=512*1024*1024

def sha(path):
    digest=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):digest.update(block)
    return digest.hexdigest()

def read(path):
    def pairs(values):
        result={}
        for key,value in values:
            if key in result:raise ValueError('duplicate_json_key')
            result[key]=value
        return result
    def constant(value):raise ValueError('nonfinite_json')
    path=Path(path)
    if path.is_symlink() or not path.is_file() or path.stat().st_size>16*1024*1024:raise ValueError('regular_bounded_json_required')
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=pairs,parse_constant=constant)

def allowed(root,location):
    if not isinstance(location,str) or not location or any(c in location for c in ('\\',':','\x00')) or any(p in ('','.','..') for p in location.split('/')):raise ValueError('relative_location_required')
    root=Path(root).resolve();path=root
    for part in location.split('/'):
        path=path/part
        if path.is_symlink():raise ValueError('delivery_symlink_rejected')
    if not path.resolve().is_relative_to(root) or not path.is_file():raise ValueError('delivery_member_missing_or_escape')
    return path

def protocol(artifacts,root):
    # 复用既有公共协议验证器，不建立第二套 craft-artifact 解释器。
    with tempfile.TemporaryDirectory(prefix='lightcraft-mobile-contract-') as tmp:
        payload=Path(tmp)/'input.json'
        for artifact in artifacts:
            payload.write_text(json.dumps({'operation':'artifact','artifact':artifact,'root':str(root)},ensure_ascii=False,allow_nan=False),encoding='utf-8')
            result=subprocess.run(['node',str(CONTRACT),str(payload)],capture_output=True,text=True,encoding='utf-8',timeout=30)
            if result.returncode:raise ValueError('artifact_identity_rejected: '+result.stdout.strip())

def source_locations(artifacts):
    locations={};identities={}
    for artifact in artifacts:
        for item in [artifact]+[a for a in [artifact.get('nativeProjectRef'),*artifact.get('renditions',[]),*artifact.get('evidenceRefs',[])] if a is not None]:
            key=(item['assetId'],item['version']);identity=item['sha256']
            if key in identities and identities[key]!=identity:raise ValueError('asset_version_conflict')
            identities[key]=identity;location=item['location']
            if location in (MANIFEST,REPORT) or location in locations and locations[location]!=identity:raise ValueError('delivery_location_conflict')
            locations[location]=identity
    known={a['assetId']:a for a in artifacts}
    if len(known)!=len(artifacts):raise ValueError('duplicate_asset_id')
    for a in artifacts:
        for ref in a['sourceRefs']:
            parent=known.get(ref['assetId'])
            if parent is None or any(parent[k]!=ref[k] for k in ('version','sha256')):raise ValueError('delivery_source_reference_missing')
    return locations

def inspect(output):
    """只读验证全部包成员及公共协议；设备/视觉/原生工程编辑始终另验。"""
    output=Path(output)
    if output.is_symlink() or not output.is_dir():raise ValueError('delivery_directory_required')
    manifest=read(output/MANIFEST)
    if type(manifest.get('schemaVersion')) is not int or manifest['schemaVersion']!=1 or manifest.get('kind')!='lightcraft-mobile-files/v1':raise ValueError('delivery_manifest_invalid')
    members=manifest.get('members');artifacts=manifest.get('artifacts')
    if not isinstance(members,list) or not 1<=len(members)<=256 or not isinstance(artifacts,list) or not artifacts:raise ValueError('delivery_members_invalid')
    expected={MANIFEST};total=0;by_location={}
    for item in members:
        if not isinstance(item,dict) or set(item)!={'location','bytes','sha256'} or type(item['bytes']) is not int or not 0<=item['bytes']<=LIMIT:raise ValueError('delivery_member_invalid')
        location=item['location']
        if location in expected:raise ValueError('delivery_inventory_duplicate')
        path=allowed(output,location);expected.add(location);total+=item['bytes'];by_location[location]=item
        if total>LIMIT or path.stat().st_size!=item['bytes'] or sha(path)!=item['sha256']:raise ValueError('delivery_member_identity_mismatch')
    actual={str(p.relative_to(output)) for p in output.rglob('*') if p.is_file()}
    if any(p.is_symlink() or not (p.is_file() or p.is_dir()) for p in output.rglob('*')) or actual!=expected:raise ValueError('delivery_inventory_mismatch')
    report=read(allowed(output,REPORT))
    if manifest.get('sourceReportSha256')!=by_location.get(REPORT,{}).get('sha256') or report.get('artifacts')!=artifacts:raise ValueError('delivery_source_report_identity_mismatch')
    locations=source_locations(artifacts)
    if set(locations)|{REPORT}!=set(by_location) or any(by_location[k]['sha256']!=v for k,v in locations.items()):raise ValueError('delivery_artifact_identity_mismatch')
    protocol(artifacts,output)
    return {'identity':'PASS','manifestSha256':sha(output/MANIFEST),'members':members,'artifacts':artifacts,'deviceAcceptance':'NOT_RUN','visual':'NOT_RUN','nativeProjectMobileReopen':'NOT_RUN','automaticReplay':False,'executionAllowed':False}

def prepare(output,report,report_sha256):
    """复制明确来源到全新目录；原件及已有目标不覆盖，失败不保留成功声明。"""
    output=Path(output);report=Path(report)
    if output.exists() or output.is_symlink():raise ValueError('new_output_required')
    value=read(report)
    if sha(report)!=report_sha256:raise ValueError('source_report_identity_mismatch')
    root=Path(value.get('root',''));artifacts=value.get('artifacts')
    if not root.is_dir() or root.is_symlink() or not isinstance(artifacts,list) or not 1<=len(artifacts)<=64:raise ValueError('source_artifacts_invalid')
    if output.resolve().is_relative_to(root.resolve()):raise ValueError('delivery_output_inside_source')
    locations=source_locations(artifacts);sources={k:allowed(root,k) for k in locations}
    for location,path in sources.items():
        if sha(path)!=locations[location]:raise ValueError('source_artifact_identity_mismatch')
    sources[REPORT]=report
    if len(sources)>256 or sum(p.stat().st_size for p in sources.values())>LIMIT:raise ValueError('delivery_size_limit')
    protocol(artifacts,root)
    output.mkdir(parents=True,exist_ok=False)
    try:
        members=[]
        for location,path in sorted(sources.items()):
            destination=output/location;destination.parent.mkdir(parents=True,exist_ok=True)
            with path.open('rb') as source,destination.open('xb') as target:shutil.copyfileobj(source,target)
            identity=report_sha256 if location==REPORT else locations[location]
            if sha(destination)!=identity or sha(path)!=identity:raise ValueError('source_changed_during_copy')
            members.append({'location':location,'bytes':destination.stat().st_size,'sha256':identity})
        manifest={'schemaVersion':1,'kind':'lightcraft-mobile-files/v1','sourceReportSha256':report_sha256,'artifacts':artifacts,'members':members}
        (output/MANIFEST).write_text(json.dumps(manifest,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
        return inspect(output)
    except BaseException:
        shutil.rmtree(output)
        raise
