"""已发布来源升级预检与事务记录；默认只读，不伪造 tag/commit。"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import uuid

ROOT=Path(__file__).resolve().parents[1]


def git(source,*argv,binary=False):
    result=subprocess.run(['git','-C',str(source),*argv],capture_output=True,check=True)
    return result.stdout if binary else result.stdout.decode().strip()


def prepare(source,tag,commit):
    source=Path(source)
    spec=importlib.util.spec_from_file_location('provenance',ROOT/'scripts/provenance.py')
    p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
    old=json.loads((ROOT/'candidate-source.json').read_text())
    if p.inventory(ROOT/'skills')!=old.get('skillFileSha256'):raise ValueError('preserve_modified_plugin_snapshot')
    actual=git(source,'rev-parse','--verify','refs/tags/'+tag+'^{commit}')
    if actual!=commit:raise ValueError('release_tag_commit_mismatch')
    remote=git(source,'remote','get-url','origin')
    if remote not in ('https://github.com/full-aigc-skills/lightcraft-skills.git','git@github.com:full-aigc-skills/lightcraft-skills.git'):
        raise ValueError('source_remote_mismatch')
    suite=json.loads(git(source,'show',commit+':skill-suite.json'))
    if suite['skills']!=p.EXPECTED_SKILLS or tag!='v'+suite['version']:raise ValueError('source_version_or_skill_set_mismatch')
    paths=git(source,'ls-tree','-r','--name-only',commit,'--','skills').splitlines()
    files={}
    for path in paths:
        relative=str(Path(path).relative_to('skills'))
        files[relative]=hashlib.sha256(git(source,'show',commit+':'+path,binary=True)).hexdigest()
    if not files or set(old['skillFileSha256'])-set(files):raise ValueError('source_removal_requires_review')
    lock={'schemaVersion':1,'sourceProject':'lightcraft-skills','sourceVersion':suite['version'],
          'sourceStatus':'published-immutable-release','repository':'https://github.com/full-aigc-skills/lightcraft-skills',
          'releaseTag':tag,'commit':commit,'managedSkills':suite['skills'],'skillFileSha256':files}
    changes=[path for path,value in files.items() if old['skillFileSha256'].get(path)!=value]
    return {'schemaVersion':1,'migrationId':str(uuid.uuid4()),'oldSource':old,'newSource':lock,'suite':suite,
            'changed':changes,'hostUpdate':'NOT_RUN','remotePublication':'NOT_VERIFIED'}


def apply(source,migration):
    """只按通过预检的内容应用，留下迁移记录；不修改人工漂移或发版。"""
    current=json.loads((ROOT/'candidate-source.json').read_text())
    if current!=migration['oldSource']:raise ValueError('source_lock_changed_since_preflight')
    spec=importlib.util.spec_from_file_location('provenance',ROOT/'scripts/provenance.py')
    p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
    if p.inventory(ROOT/'skills')!=current['skillFileSha256']:raise ValueError('preserve_modified_plugin_snapshot')
    # 在临时目录先验证完整发行内容，再做普通文件更新；异常时保留迁移日志，不声称完成。
    history=ROOT/'source-migrations';history.mkdir(exist_ok=True)
    journal=history/(migration['migrationId']+'.json')
    journal.write_text(json.dumps(dict(migration,status='STARTED'),ensure_ascii=False,indent=2)+'\n')
    with tempfile.TemporaryDirectory(prefix='lightcraft-upgrade-') as temporary:
        stage=Path(temporary)
        for path,expected in migration['newSource']['skillFileSha256'].items():
            target=stage/path;target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(git(source,'show',migration['newSource']['commit']+':skills/'+path,binary=True))
            if hashlib.sha256(target.read_bytes()).hexdigest()!=expected:raise ValueError('release_content_changed')
        for path in migration['changed']:
            target=ROOT/'skills'/path
            if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()!=current['skillFileSha256'].get(path):raise ValueError('concurrent_snapshot_change')
            target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(stage/path,target)
    for name,data in [('source-suite.json',migration['suite']),('candidate-source.json',migration['newSource'])]:
        with tempfile.NamedTemporaryFile(mode='w',dir=ROOT,delete=False) as stream:
            tmp=Path(stream.name);json.dump(data,stream,indent=2);stream.write('\n');stream.flush();os.fsync(stream.fileno())
        os.replace(tmp,ROOT/name)
    p.validate(ROOT,source)
    journal.write_text(json.dumps(dict(migration,status='APPLIED_HOST_NOT_VERIFIED'),ensure_ascii=False,indent=2)+'\n')
    return {'migrationId':migration['migrationId'],'snapshot':'PASS','hostUpdate':'NOT_RUN','published':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--source-root',type=Path,required=True);parser.add_argument('--tag',required=True);parser.add_argument('--commit',required=True);parser.add_argument('--apply',action='store_true')
    args=parser.parse_args()
    result=prepare(args.source_root,args.tag,args.commit)
    if args.apply:result=apply(args.source_root,result)
    print(json.dumps(result,ensure_ascii=False,indent=2))
