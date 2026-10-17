#!/usr/bin/env python3
"""公开交付校验：真实原生交付包的血缘与同名替换拒绝。"""
import importlib.util,json,hashlib,shutil,sys
from pathlib import Path
c=json.loads(Path(sys.argv[1]).read_text());root=Path(c['output']);root.mkdir(parents=True,exist_ok=False)
quality=Path(c['quality']);spec=importlib.util.spec_from_file_location('lineage_public_quality',quality);q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)
source=Path(c['package']);native=json.loads((source/'proof.json').read_text())
assert native['result']=='PASS' and native['movedNativeReopened'] is True and native['sourceUnchanged'] is True
rows=[]
for name in ('moved package with spaces','revised'):
 p=source/name;m=json.loads((p/'manifest.json').read_text());checked=q.check_delivery(p,m['runtimeSha256'],m['files']['project.vectorcraft'])
 assert checked['artifactIntegrityStatus']=='PASS' and checked['technicalStatus']=='PASS' and checked['lineageStatus']=='PASS',checked
 rows.append({'case':name,'result':'PASS','quality':checked})
for row in native['refusals']:
 p=source/row['case'];m=json.loads((p/'manifest.json').read_text());checked=q.check_delivery(p,m['runtimeSha256'],m['files']['project.vectorcraft'])
 assert checked['artifactIntegrityStatus']=='FAIL' and checked['outputs']==[],checked
 rows.append({'case':row['case'],'result':'PASS','quality':checked})
proof={'schema':'vectorcraft-lineage-public-quality/v1','result':'PASS','driverSha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'qualitySha256':hashlib.sha256(quality.read_bytes()).hexdigest(),'nativeProofSha256':hashlib.sha256((source/'proof.json').read_bytes()).hexdigest(),'cases':rows,'scope':'actual native package public identity and decode; creative, engineering reopening and acceptance remain separate'}
(root/'proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'result':'PASS','cases':len(rows)}))
