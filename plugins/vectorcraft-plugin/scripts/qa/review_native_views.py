"""独立QA观察：在明确文件根内重开当前工程并生成多尺寸原生预览。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys

config=json.loads(Path(sys.argv[1]).read_text());source=Path(config['source']);output=Path(config['output']);output.mkdir(parents=True,exist_ok=False)
skill=Path(config['skill']);binary=Path(config['binary'])
spec=importlib.util.spec_from_file_location('review_native_session',skill/'scripts/mcp_session.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before={str(p.relative_to(source)):sha(p) for p in source.rglob('*') if p.is_file()}
with module.Session([str(binary),'mcp','--headless'],filesystem={'readRoots':[str(source)],'writeRoots':[str(output)]}) as session:
    session.command('document.open',{'path':str(source/'project.vectorcraft')})
    model=session.command('document.json',{})
    assert model==json.loads((source/'native.json').read_text())
    previews=[]
    for width,scale in [(128,1),(64,.5),(32,.25)]:
        target=output/f'preview-{width}.png'
        session.request('tools/call',{'name':'export','arguments':{'path':str(target),'format':'png','artboard':0,'scale':scale}})
        data=target.read_bytes();assert data[:8]==b'\x89PNG\r\n\x1a\n'
        size=struct.unpack('>II',data[16:24]);assert size==(width,width*3//4)
        previews.append({'path':target.name,'sha256':sha(target),'width':size[0],'height':size[1],'scale':scale})
assert before=={str(p.relative_to(source)):sha(p) for p in source.rglob('*') if p.is_file()}
proof={'schema':'vectorcraft-single-review-native-observer/v1','result':'PASS','sourceProjectSha256':before['project.vectorcraft'],'runtimeSha256':sha(binary),'driverSha256':sha(Path(__file__)),'nativeReopen':True,'sourceUnchanged':True,'previews':previews,'scope':'explicit QA instrumentation before or after the bounded review; outside workflow budget,not a model-dispatch or automatic workflow call'}
(output/'proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'result':'PASS','previews':len(previews)}))
