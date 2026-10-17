"""校验插件分发文档绑定；不实现安装、执行或平行公共协议。"""
import hashlib
import json
from pathlib import Path, PurePosixPath

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads(path.read_text(encoding='utf-8'))

def validate(root):
    """由插件锁定载荷独立验证已生成矩阵；失配不能冒充当前验收。"""
    root=Path(root)
    try:
        matrix=read(root/'docs/current-capabilities.json');base=root/'skills/effectcraft-harness'
        runtime=read(base/'scripts/runtime.lock.json');python=read(base/'scripts/python.lock.json')
        path=root/'docs/evidence/current-capability-evidence.json';proof=read(path)
        if matrix['schema']!='effectcraft-capability-matrix/v2' or proof['schema']!='effectcraft-capability-evidence/v1':raise ValueError('schema mismatch')
        files={}
        for p in sorted(base.rglob('*')):
            if '__pycache__' in p.relative_to(base).parts or p.suffix=='.pyc':continue
            if p.is_symlink():raise ValueError('payload symlink')
            if p.is_file():files[p.relative_to(base).as_posix()]=sha(p)
        if path.is_symlink() or base.is_symlink():raise ValueError('binding symlink')
        name=proof['reportFile'];relative=PurePosixPath(name)
        if relative.is_absolute() or '..' in relative.parts or '\\' in name or not name.startswith('docs/evidence/'):raise ValueError('report path invalid')
        report_path=root.joinpath(*relative.parts)
        if any(p.is_symlink() for p in [report_path,*report_path.parents] if p==root or root in p.parents):raise ValueError('report symlink')
        report=read(report_path);key=report['platform'];artifact=runtime['artifacts'][key];claim=proof['platforms'][key]
        inventory={name:{'sha256':digest,'mode':0o444} for name,digest in files.items()}
        inventory_sha=hashlib.sha256(json.dumps(inventory,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        cases=[row for row in report['cases'] if row['skill']=='effectcraft-use']
        current=(files==proof['baseSkillFiles'] and proof['runtimeVersion']==runtime['resolvedVersion']
            and proof['pythonVersion']==python['version'] and sha(report_path)==proof['reportSha256']
            and report['schema']=='effectcraft-independent-offline15/v1' and report['status']=='PASS'
            and claim['runtimeSha256']==artifact['binarySha256']
            and claim['pythonArchiveSha256']==python['artifacts'][key]['archiveSha256']==report['pythonArchiveSha256']
            and report['nativeArchiveSha256']==artifact['archiveSha256'] and len(cases)==1
            and all(cases[0].get(x)=='PASS' for x in ('status','engineering','technical'))
            and cases[0].get('installedFilesAndModesUnchanged') is True and cases[0].get('installedInventorySha256')==inventory_sha)
        binding=matrix['evidenceBinding']
        if (type(binding['current']) is not bool or binding['current']!=current
                or binding['file']!=path.relative_to(root).as_posix() or binding['sha256']!=sha(path)):
            raise ValueError('evidence binding differs from current payload/report')
        expected=[]
        for platform,value in runtime['artifacts'].items():
            expected.append({'platform':platform,'python':python['version'],'runtime':runtime['resolvedVersion'],
                'pythonMinimum':python['artifacts'][platform].get('minimumSystem',{}),'runtimeMinimum':value.get('minimumSystem',{}),
                'nativeRepresentative':'PASS' if current and platform==key and claim.get('nativeRepresentative')=='PASS' else 'NOT_RUN',
                'scope':'native technical sample only; not domain, cold-install, creative or host acceptance','completePlatformAcceptance':'NOT_RUN'})
        if matrix['platforms']!=expected:raise ValueError('platform claims/minimums differ from current locks and proof')
        if (matrix['web']!={'installation':'NOT_RUN','browserTask':'NOT_RUN'} or matrix['freebsd']!={'sourceBuild':'NOT_RUN'}
                or matrix['fullV1']!='NOT_RUN'):raise ValueError('unsupported acceptance promotion')
        return []
    except (OSError,ValueError,KeyError,TypeError,IndexError) as error:
        return ['current capability: '+str(error)]
