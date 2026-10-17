#!/usr/bin/env python3
"""登记已执行的原生控制证据；日志、工程和独立技能身份均须仍可核对。"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil

P=Path(__file__).resolve().parents[2]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def archive(path):
    old=path.with_name(path.name.replace('-20261008','-before-execution-control-20261008'))
    if path.is_file() and not old.exists():shutil.copyfile(path,old)
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-repository',type=Path,required=True)
    parser.add_argument('--evidence-root',type=Path,required=True)
    args=parser.parse_args();S=args.source_repository.resolve();root=args.evidence_root.resolve()
    def load(path):return json.loads(path.read_text())
    spec=importlib.util.spec_from_file_location('source_evidence',S/'scripts/verify_optimization_evidence.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    skills={p.name:m.skill_digest(p) for p in sorted((S/'skills').iterdir()) if (p/'SKILL.md').is_file()}
    cold=load(root/'cold.json');assert cold['result']=='PASS' and len(cold['cases'])==13
    assert {c['skill']:c['skillSha256'] for c in cold['cases']}==skills
    cancellation=load(Path(load(root/'cancel-config.json')['output'])/'proof.json')
    review_root=Path(load(root/'review-config.json')['output']);revision=load(review_root/'proof.json')
    for report in [cancellation,revision]:
        assert report.get('fingerprints')
        for name,digest in report['fingerprints'].items():assert sha(P/name)==digest, 'stale execution fingerprint: '+name
    assert cancellation['result']=='PASS' and cancellation['settledState']=='cancelled' and cancellation['settledEpoch']==cancellation['epoch']+1
    assert cancellation['nativeGroupStopped'] and cancellation['lateReceiptQuarantined'] and cancellation['sourceUnchanged']
    assert revision['result']=='PASS' and revision['independent'] is False and revision['unrelatedBoardBytesPreserved']
    # 取消夹具默认同一专项技能，也允许使用完整use入口；必须绑定实际执行摘要。
    active_skill=Path(load(root/'cancel-config.json')['skill'])
    assert cancellation['skillSha256']==m.skill_digest(active_skill)
    for path,record in cancellation['recovery']['files'].items():
        assert sha(Path(path))==record['sha256'] and Path(path).stat().st_ino==record['inode']
    preserved=load(root/'preserved.json');assert len(preserved['cases'])==6 and all(c['result']=='PASS' for c in preserved['cases'])
    assert 'Ran 162 tests' in (root/'source.log').read_text() and 'OK (skipped=30)' in (root/'source.log').read_text()
    assert 'Ran 12 tests' in (root/'native-scenes.log').read_text() and '\nOK\n' in (root/'native-scenes.log').read_text()
    assert 'tests 15' in (root/'node.log').read_text() and 'fail 0' in (root/'node.log').read_text()
    def logs(repo,names):
        result={}
        for name in names:
            text=(root/name).read_text().replace(str(S),'<skills-repository>').replace(str(P),'<plugin-repository>')
            text=re.sub(r'/private/var/folders/[^\s"\']+','<temporary-path>',text)
            path=repo/'docs/evidence/optimization-logs'/('execution-control-'+name);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
            result[path.relative_to(repo).as_posix()]=sha(path)
        return result
    source_logs=logs(S,['source.log','source-baseline-red.log','cold.log','native-scenes.log','preserved.log'])
    source_paths=[S/'skill-suite.json',S/'.claude-plugin/plugin.json',S/'.github/workflows/implementation.yml',*sorted((S/'scripts').glob('*.py')),*sorted((S/'tests').rglob('*.py'))]
    source={'schema':'vectorcraft-optimization-candidate/v1','result':'PASS','level':'native-candidate','sourceCandidateVersion':'0.1.0-dev.34','uncommittedCandidate':True,
      'scope':'current source regression, 13 standalone cold runtime installations, 10 native scenes, 6 post-save faults, managed native revision/cancellation; not full V1, fixed release or host dispatch',
      'defaultRegression':{'ran':162,'passed':132,'skipped':30,'failures':0,'errors':0},'nativeSceneRegression':{'ran':12,'contractTests':2,'nativeSceneCases':10,'skipped':0},
      'native':{'standaloneCold':cold,'postSaveFaults':preserved,'managedCancellation':cancellation,'managedRevision':revision},
      'fingerprints':{**{p.relative_to(S).as_posix():sha(p) for p in source_paths},**source_logs},'skills':skills,
      'redLogBoundary':'original temporary logs were externally removed; retained red logs are explicitly labelled immutable HEAD baseline replays',
      'excluded':['fixed source/plugin release','fixed installation','actual host/model dispatch','independent reviewer','all585 native commands','full GUI','Art bundle','full task3/6 and V1 acceptance']}
    source_path=S/'docs/evidence/optimization-candidate-20261008.json';archive(source_path);write(source_path,source);assert m.verify(S,source)==[]
    plugin_logs=logs(P,['node.log','plugin-baseline-red.log','create.log','cancel.log','review.log'])
    python_log=root/'plugin-python.log';python_result={'status':'NOT_RUN'}
    if python_log.is_file():
        assert 'Ran 28 tests' in python_log.read_text() and '\nOK\n' in python_log.read_text()
        plugin_logs.update(logs(P,['plugin-python.log']));python_result={'ran':28,'passed':28,'skipped':0}
    copied=P/'docs/evidence/vectorcraft-optimization-source-candidate-20261008.json';archive(copied);write(copied,source)
    plugin_paths=[*sorted((P/'src').rglob('*.ts')),*sorted((P/'src').rglob('*.py')),*sorted((P/'tests').glob('*.ts')),*sorted((P/'tests').glob('*.py')),*sorted((P/'schemas').glob('*.json')),
      P/'package.json',P/'plugin.json',P/'skills.lock.json',P/'scripts/current_identity.py',P/'scripts/evidence_index.py',P/'scripts/acceptance/single_round.ts',P/'scripts/acceptance/managed_cancel.ts',P/'scripts/acceptance/execution_identity.ts',Path(__file__),P/'docs/vector-review-rubric.json',P/'.github/workflows/implementation.yml']
    fingerprints={**{p.relative_to(P).as_posix():sha(p) for p in plugin_paths},**plugin_logs}
    native_path=P/'docs/evidence/vectorcraft-optimization-single-round-native-20261008.json';archive(native_path);write(native_path,{**revision,'fingerprints':fingerprints})
    receipt_path=P/'docs/evidence/vectorcraft-optimization-review-receipt-20261008.json';archive(receipt_path);write(receipt_path,load(review_root/'receipt.json'))
    control={'schema':'vectorcraft-execution-control-evidence/v1','result':'PASS','level':'native-candidate','scope':'current local controller/process/recovery tests plus actual controlled native checkpoint cancellation and restart verification; minimum implementation only',
      'completedTasks':['3.1','3.2','3.4','3.5','3.7','3.8'],'openFullAcceptance':['3.3','3.6','3.9','6.x','9.21'],
      'nodeTests':{'ran':15,'passed':15,'skipped':0},'pythonRegression':python_result,'nativeCancellation':cancellation,'nativeRevision':revision,'fingerprints':fingerprints,
      'sourceEvidence':{'path':copied.relative_to(P).as_posix(),'sha256':sha(copied)},'baselineReplay':'original logs lost to external temporary-directory cleanup; HEAD replay explicitly labelled',
      'fixedPluginVersion':'0.1.0-dev.37','fixedSkillSource':'v0.1.0-dev.33','newSourceCandidate':'0.1.0-dev.34','fixedInstallation':'NOT_RUN','actualGitHubCI':'NOT_RUN','fullV1':'incomplete'}
    write(P/'docs/evidence/vectorcraft-execution-control-20261008.json',control)
    local_path=P/'docs/evidence/vectorcraft-optimization-local-20261008.json';archive(local_path)
    write(local_path,{**control,'schema':'vectorcraft-optimization-local/v1','level':'local-tests','scope':'current local tests and bounded source/native candidate; original wider optimization proof retained as historical report','fingerprints':fingerprints})
    print(json.dumps({'result':'PASS','sourceTests':162,'nodeTests':15,'pythonRegression':python_result,'standaloneSkills':13,'nativeScenes':10,'openTasks':46}))
if __name__=='__main__':main()
