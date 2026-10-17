"""以固定技能创建包含真实链接 PNG 的自有合成工程，不修改既有输入。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import sys
import zlib


def png(color):
    """生成八像素方形测试素材；仅用于链接依赖故障验收。"""
    def chunk(kind, data):
        return struct.pack('!I', len(data))+kind+data+struct.pack('!I', zlib.crc32(kind+data)&0xffffffff)
    return (b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR', struct.pack('!2I5B', 8, 8, 8, 6, 0, 0, 0))
            +chunk(b'IDAT', zlib.compress((b'\0'+bytes(color)*8)*8))+chunk(b'IEND', b''))


def main():
    config=json.loads(Path(sys.argv[1]).read_text())
    root=Path(config['output']).resolve()
    root.mkdir(parents=True, exist_ok=False)
    skill=Path(config['skill']).resolve();runtime=Path(config['runtimeHome']).resolve()
    asset=root/'synthetic-link.png';asset.write_bytes(png([241,137,28,255]))
    (root/'changed-link.png').write_bytes(png([12,80,190,255]))
    plan=json.loads(Path(config['brandPlan']).read_text())
    plan['assets']={'referenceRaster':{'path':str(asset),'sha256':hashlib.sha256(asset.read_bytes()).hexdigest()}}
    plan['operations'].append({'command':'asset.place','params':{'asset':'referenceRaster','link':True,'rect':[8,8,16,16]},'as':'linkedRaster'})
    plan_path=root/'create-plan.json';plan_path.write_text(json.dumps(plan))
    with (root/'create.stdout').open('w') as out,(root/'create.stderr').open('w') as err:
        subprocess.run([sys.executable,'-I','-B',str(skill/'scripts/workflow.py'),str(plan_path),
                        '--output',str(root/'source'),'--runtime-home',str(runtime)],stdout=out,stderr=err,timeout=90,check=True)
    manifest=json.loads((root/'source/manifest.json').read_text())
    entry=manifest['assets']['referenceRaster']
    assert entry['linked'] is True and entry['ids']
    assert manifest['files'][entry['path']]==entry['sha256']==hashlib.sha256(asset.read_bytes()).hexdigest()
    spec=importlib.util.spec_from_file_location('session',skill/'scripts/mcp_session.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    project=root/'source/project.vectorcraft';original=hashlib.sha256(project.read_bytes()).hexdigest()
    with module.Session([str(runtime/'vectorcraft/0.2.0-craft.2/vectorcraft-cli'),'mcp','--headless']) as session:
        session.command('document.open',{'path':str(project)})
        links=session.command('links.check',{})
        assert links['missing']==links['modified']==0 and len(links['links'])==1
        assert links['links'][0]['status']=='ok'
    assert hashlib.sha256(project.read_bytes()).hexdigest()==original
    proof={'result':'PASS','skillDirectory':str(skill),'projectSha256':original,'assetSha256':entry['sha256'],
           'assetIds':entry['ids'],'nativeLinks':links,
           'brandPlanSha256':hashlib.sha256(Path(config['brandPlan']).read_bytes()).hexdigest(),
           'runtimeSha256':hashlib.sha256((runtime/'vectorcraft/0.2.0-craft.2/vectorcraft-cli').read_bytes()).hexdigest(),
           'fixtureScriptSha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'sourceReopenedUnchanged':True,
           'scope':'own synthetic PNG and brand plan created with pinned independent workflow; no creative acceptance'}
    (root/'proof.json').write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps({'result':'PASS','linkedAssets':len(links['links']),'sourceReopenedUnchanged':True}))


if __name__=='__main__':
    main()
