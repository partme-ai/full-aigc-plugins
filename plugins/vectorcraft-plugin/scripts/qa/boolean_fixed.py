#!/usr/bin/env python3
"""公开固定技能的外部原生布尔QA；沿用独立源验收流程，已知／未知故障在真实成功操作后显式注入。"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(sys.argv[3]).resolve()


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def module(skill, name):
    spec = importlib.util.spec_from_file_location('boolean_accept_'+name, skill/'scripts'/(name+'.py'))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def run(destination, runtime):
    dependencies = ['skills/vectorcraft-use/scripts/'+name+'.py' for name in
                    ['boolean_transactions','workflow','native_workflow','commands','mcp_session','preserved_stage','execution_control']]
    dependencies += ['skills.lock.json','plugin.json']
    fingerprints = {p:digest(ROOT/p) for p in dependencies}
    def skill_digest(folder):
        files = sorted((p for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'),
                       key=lambda p:p.relative_to(folder).as_posix())
        return hashlib.sha256(''.join(p.relative_to(folder).as_posix()+'\0'+digest(p)+'\n' for p in files).encode()).hexdigest()
    skills = {folder.name:skill_digest(folder) for folder in (ROOT/'skills').iterdir() if folder.is_dir()}
    destination.mkdir()
    skill = ROOT/'skills/vectorcraft-cli-boolean'
    skill_files = {str(p.relative_to(skill)):digest(p) for p in skill.rglob('*') if p.is_file()}
    workflow = module(skill,'workflow')
    source = destination/'source'
    operations = [{'command':'shape.rectangle','params':{'x':x,'y':y,'width':w,'height':h},'as':name}
                  for name,x,y,w,h in [('outer',10,10,70,70),('inner',30,30,30,30),('sentinel',90,10,8,8)]]
    exports = [{'format':fmt,'artboard':0} for fmt in ['svg','png','pdf']]
    first = workflow.execute({'document':{'width':128,'height':100,'units':'Pixels'},'operations':operations,
                              'exports':exports},source,runtime_home=runtime)
    source_hashes = {str(p.relative_to(source)):digest(p) for p in source.rglob('*') if p.is_file()}
    ids = [first['bindings'][name]['id'] for name in ['outer','inner']]
    cases = []
    guard = module(skill,'boolean_transactions')
    cli = json.loads((skill/'scripts/runtime.lock.json').read_text())
    runtime_binary = runtime/'vectorcraft'/cli['resolvedVersion']/'vectorcraft-cli'
    assert digest(runtime_binary) == cli['artifacts']['darwin-arm64']['binarySha256']
    Session = module(skill,'mcp_session').Session
    def reopened(path):
        with Session([str(runtime_binary),'mcp','--headless']) as session:
            session.command('document.open',{'path':str(path)})
            return session.command('document.json',{})
    for route in ['direct','gateway']:
        for command in ['object.pathfinder.unite','object.pathfinder.minusFront',
                        'object.pathfinder.intersect','object.pathfinder.exclude','object.group']:
            name = route+'-'+command.rsplit('.',1)[1]
            output = destination/name
            operation = ({'command':'native.command','params':{'command':command,'params':{}},'as':'result'}
                         if route == 'gateway' else {'command':command,'as':'result'})
            plan = {'expectedProjectSha256':first['files']['project.vectorcraft'],
                    'operations':[{'command':'select.set','params':{'ids':ids}},operation], 'exports':exports}
            result = workflow.execute(plan,output,runtime_home=runtime,source=source)
            report = json.loads((output/'boolean-transactions.json').read_text())
            record = report['operations'][0]
            assert record['status'] == 'verified' and record['participantIds'] == ids
            assert digest(output/record['checkpoint']) == record['checkpointSha256']
            before = reopened(output/record['checkpoint']); after = reopened(output/'project.vectorcraft')
            assert all(i in guard.nodes(before) for i in ids)
            assert all(i in guard.nodes(after) for i in record['resultIds'])
            assert guard.pruned(before,set(ids)) == guard.pruned(after,set(record['resultIds']))
            assert result['files']['boolean-transactions.json'] == digest(output/'boolean-transactions.json')
            cases.append({'name':name,'participantIds':ids,'resultIds':record['resultIds'],
                          'checkpointReopened':True,'projectReopened':True,
                          'checkpointSha256':record['checkpointSha256'],
                          'projectSha256':result['files']['project.vectorcraft']})
    # 链接素材触发工作流收集后的根目录变化；检查点也必须独立收集并随交付迁移。
    from PIL import Image
    image = destination/'linked.png'; Image.new('RGB',(4,4),(220,30,10)).save(image)
    asset_source = destination/'asset-source'
    with_asset = workflow.execute({'document':{'width':128,'height':100,'units':'Pixels'},
        'assets':{'photo':{'path':str(image),'sha256':digest(image)}},
        'operations':operations+[{'command':'asset.place','params':{'asset':'photo','rect':[90,40,8,8],'link':True}}]},
        asset_source,runtime_home=runtime)
    asset_ids = [with_asset['bindings'][name]['id'] for name in ['outer','inner']]
    output = destination/'asset-revision'
    revised = workflow.execute({'expectedProjectSha256':with_asset['files']['project.vectorcraft'],
        'operations':[{'command':'select.set','params':{'ids':asset_ids}},
                      {'command':'object.pathfinder.unite','as':'result'}]},output,runtime_home=runtime,source=asset_source)
    report = json.loads((output/'boolean-transactions.json').read_text())
    record = report['operations'][0]
    assert record['checkpointCollection'].startswith('native-package')
    moved = destination/'moved-asset-revision'; shutil.copytree(output,moved)
    with Session([str(runtime_binary),'mcp','--headless']) as session:
        session.command('document.open',{'path':str(moved/record['checkpoint'])})
        checked = session.command('links.check',{})
        assert not checked['missing'] and not checked['modified']
        assert all(i in guard.nodes(session.command('document.json',{})) for i in asset_ids)
    assert digest(moved/record['checkpoint'])==record['checkpointSha256']
    cases.append({'name':'linked-asset-checkpoint-relocation','checkpointReopened':True,
                  'movedLinksValid':True,'participantIds':asset_ids})
    commands = module(skill,'commands')
    output = destination/'complete-command'
    receipt = commands.execute({'schema':'craft-command-plan/v1','operations':[
        {'command':'document.open','params':{'path':{'$ref':'project.path'}}},
        {'command':'select.set','params':{'ids':ids}},
        {'command':'object.group','params':{},'as':'group'},
        {'command':'select.set','params':{'ids':[{'$ref':'group.id'}]}},
        {'command':'object.ungroup','params':{}}]}, output, runtime_home=runtime,
        inputs={'project':source/'project.vectorcraft'})
    assert receipt['result']=='PASS',receipt
    report = json.loads((output/'boolean-transactions.json').read_text())
    assert len(report['operations'])==2 and all(r['status']=='verified' for r in report['operations'])
    cases.append({'name':'complete-command-group-ungroup','transactions':2,'result':'PASS'})
    # 明确标记为故障注入：实际原生命令已完成，测试随后制造语义失败或丢失可信回复。
    for fault in ['known','unknown']:
        stage = destination/('fault-'+fault);stage.mkdir()
        with Session([str(runtime_binary),'mcp','--headless']) as session:
            session.command('document.open',{'path':str(source/'project.vectorcraft')})
            session.command('select.set',{'ids':ids})
            before = session.command('document.json',{})
            count = [0]
            def invoke():
                count[0] += 1
                session.command('object.pathfinder.unite',{})
                raise RuntimeError('semantic_error: injected after successful native mutation' if fault=='known'
                                   else 'outcome_unknown: injected lost reply after native mutation')
            try:
                guard.execute(session,'object.pathfinder.unite',{},invoke,stage)
            except RuntimeError as error:
                assert ('non_atomic_operation_defect' if fault=='known' else 'outcome_unknown') in str(error)
            else:
                raise AssertionError('fault accepted')
            after = session.command('document.json',{})
            assert (guard.normalized(before)==guard.normalized(after)) == (fault=='known')
            record = json.loads((stage/'boolean-transactions.json').read_text())['operations'][0]
            assert record['status'] == ('restored_after_failure' if fault=='known' else 'unknown')
            assert count[0] == 1 and not record['replayAllowed']
            assert all(i in guard.nodes(reopened(stage/record['checkpoint'])) for i in ids)
            cases.append({'name':'real-native-injected-'+fault,'status':record['status'],
                          'invocations':count[0],'checkpointReopened':True,'replayAllowed':False})
    assert source_hashes == {str(p.relative_to(source)):digest(p) for p in source.rglob('*') if p.is_file()}
    assert skill_files == {str(p.relative_to(skill)):digest(p) for p in skill.rglob('*') if p.is_file()}
    assert fingerprints == {p:digest(ROOT/p) for p in dependencies}
    assert skills == {folder.name:skill_digest(folder) for folder in (ROOT/'skills').iterdir() if folder.is_dir()}
    proof = {'schema':'vectorcraft-boolean-fixed-qa/v1','result':'PASS','level':'external-qa-against-fixed-install',
             'platform':sys.platform,'runtimeIdentity':digest(runtime_binary),'cases':cases,'fingerprints':fingerprints,
             'installedFilesSha256':hashlib.sha256(json.dumps(skill_files,sort_keys=True).encode()).hexdigest(),
             'sourcePreserved':True,'isolatedSkillPreserved':True,'skills':skills,
             'pluginVersion':json.loads((ROOT/'plugin.json').read_text())['version'],
             'sourceRef':json.loads((ROOT/'skills.lock.json').read_text())['sources'][0]['ref'],
             'sourceCommit':json.loads((ROOT/'skills.lock.json').read_text())['sources'][0]['sha'],
             'driverSha256':digest(Path(__file__)),
             'fixedInstalledSkill':True,
             'scope':'14 real native cases: direct/gateway operations, complete group/ungroup and explicit post-success fault injection; actual public fixed installed skill; not all Pathfinder contexts, GUI or creative acceptance'}
    (destination/'proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'result':'PASS','cases':len(cases),'scope':proof['scope']}))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination',type=Path);parser.add_argument('runtime',type=Path);parser.add_argument('implementation',type=Path)
    args=parser.parse_args();run(args.destination.resolve(),args.runtime.resolve())
