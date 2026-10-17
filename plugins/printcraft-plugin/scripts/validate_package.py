"""作者端严格包校验；离线摘要完整性与远端发行证明分别报告。"""
from pathlib import Path
import runpy
import hashlib
import json
import re
ROOT=Path(__file__).resolve().parents[1]
UPSTREAM={'printcraft-use','printcraft-cli','printcraft-cli-setup','printcraft-cli-inspect','printcraft-cli-pages','printcraft-cli-automation'}
LOCAL={'printcraft-harness'}

def inventory(root):
    entries=sorted(root.rglob('*'))
    if root.is_symlink() or any(p.is_symlink() for p in entries):raise ValueError('snapshot_symlink')
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in entries if p.is_file() and p.name!='.DS_Store' and '__pycache__' not in p.parts}

def validate():
    manifest=json.loads((ROOT/'plugin.json').read_text())
    if set(manifest)-{'$schema','name','version','description','author','homepage','repository','license','keywords','extensions'}:raise ValueError('unknown_manifest_field')
    if manifest.get('$schema')!='https://agent-plugins.org/schemas/1.0.0/plugin.schema.json':raise ValueError('unsupported_plugin_schema')
    for key in ('name','version','description'):
        if not isinstance(manifest.get(key),str) or not manifest[key]:raise ValueError('invalid_manifest_'+key)
    if manifest['name']!='printcraft' or not re.fullmatch(r'\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?',manifest['version']):raise ValueError('manifest_identity_invalid')
    core=manifest['version'].split('+',1)[0];base,sep,pre=core.partition('-')
    if any(len(x)>1 and x.startswith('0') for x in base.split('.')) or sep and any(x.isdigit() and len(x)>1 and x.startswith('0') for x in pre.split('.')):raise ValueError('invalid_semver_leading_zero')
    for key in ('homepage','repository','license'):
        if key in manifest and not isinstance(manifest[key],str):raise ValueError('invalid_manifest_'+key)
    if 'keywords' in manifest and (not isinstance(manifest['keywords'],list) or any(not isinstance(x,str) for x in manifest['keywords'])):raise ValueError('invalid_keywords')
    if 'author' in manifest and (not isinstance(manifest['author'],dict) or set(manifest['author'])-{'name','email','url'} or any(not isinstance(x,str) for x in manifest['author'].values())):raise ValueError('invalid_author')
    if 'extensions' in manifest and not isinstance(manifest['extensions'],dict):raise ValueError('invalid_extensions')
    for relative in ('plugin.json','candidate-source.json','upstream/skill-suite.json','.codex-plugin/plugin.json'):
        if (ROOT/relative).is_symlink():raise ValueError('package_metadata_symlink')
    known=manifest.get('extensions',{}).get('com.openai',{})
    if not isinstance(known,dict) or 'interface' in known and not isinstance(known['interface'],dict):raise ValueError('invalid_openai_extension')
    interface=known.get('interface',{})
    for field,value in interface.items():
        if field in {'displayName','shortDescription','longDescription','developerName','category','websiteURL','privacyPolicyURL','termsOfServiceURL','brandColor','composerIcon','logo','logoDark'} and not isinstance(value,str):raise ValueError('invalid_interface_field')
        if field in {'capabilities','defaultPrompt','screenshots'} and not isinstance(value,list):raise ValueError('invalid_interface_field')
        if field in {'composerIcon','logo','logoDark'} and value.startswith('./'):
            resource=(ROOT/value).resolve()
            if ROOT.resolve() not in resource.parents or not resource.is_file() or (ROOT/value).is_symlink():raise ValueError('missing_or_unsafe_interface_resource')
    source=json.loads((ROOT/'upstream/skill-suite.json').read_text())
    provenance=json.loads((ROOT/'candidate-source.json').read_text())
    if provenance.get('sourceProject')!='printcraft-skills' or provenance.get('sourceVersion')!=source.get('version') or set(source.get('skills',[]))!=UPSTREAM:raise ValueError('source_identity_mismatch')
    status=provenance.get('sourceStatus')
    if status=='local-unpublished-candidate':
        if provenance.get('releaseTag') is not None or provenance.get('sourceCommit') is not None:raise ValueError('false_release_identity')
        release='UNPUBLISHED'
    elif status=='published-release':
        if provenance.get('releaseTag')!='v'+source['version'] or not re.fullmatch('[0-9a-f]{40}',provenance.get('sourceCommit','')):raise ValueError('release_identity_invalid')
        if provenance.get('sourceRepository')!='https://github.com/full-aigc-skills/printcraft-skills':raise ValueError('release_repository_invalid')
        lock_path=ROOT/'source-release.lock.json'
        if not lock_path.is_file() or lock_path.is_symlink():raise ValueError('release_lock_missing_or_unsafe')
        formal=json.loads(lock_path.read_text())
        if formal.get('protocol')!='printcraft.source-release/1' or formal.get('source')!=provenance or formal.get('pluginVersion')!=manifest['version']:raise ValueError('release_lock_identity_drift')
        release='OFFLINE_IDENTITY_ONLY_REMOTE_NOT_VERIFIED'
    else:raise ValueError('false_release_identity')
    files=inventory(ROOT/'skills')
    managed={p:d for p,d in files.items() if p.split('/')[0] in UPSTREAM}
    if managed!=provenance.get('skillFileSha256'):raise ValueError('snapshot_drift')
    if hashlib.sha256((ROOT/'upstream/skill-suite.json').read_bytes()).hexdigest()!=provenance.get('sourceSuiteSha256'):raise ValueError('source_suite_drift')
    names={p.name for p in (ROOT/'skills').iterdir() if p.is_dir() and p.name!='__pycache__'}
    scenes=runpy.run_path(str(ROOT/'scripts/validate_editor_scenes.py'))['candidate_names'](ROOT)
    if names!=UPSTREAM|LOCAL|scenes:raise ValueError('skill_set_mismatch')
    for name in names:
        text=(ROOT/'skills'/name/'SKILL.md').read_text()
        if f'name: {name}\n' not in text or len(text.splitlines())>=500:raise ValueError('skill_frontmatter_invalid')
    compat=ROOT/'.codex-plugin/plugin.json'
    if compat.exists():
        host=json.loads(compat.read_text())
        if host.get('name')!=manifest['name'] or host.get('version')!=manifest['version'] or host.get('skills')!='./skills/' or host.get('interface',{})!=interface:raise ValueError('host_manifest_drift')
    for relative in ('.claude-plugin/plugin.json','kimi.plugin.json'):
        path=ROOT/relative
        if not path.is_file() or path.is_symlink():raise ValueError('missing_or_unsafe_host_manifest')
        host=json.loads(path.read_text())
        if host.get('name')!=manifest['name'] or host.get('version')!=manifest['version'] or host.get('skills')!='./skills/':raise ValueError('host_manifest_drift')
    return {'plugin':manifest['name'],'upstreamSkills':len(UPSTREAM),'localSkills':len(LOCAL|scenes),'skills':len(names),'snapshot':'PASS','sourceRelease':release,'remoteSourceVerification':'NOT_RUN','hostAcceptance':'NOT_RUN'}
if __name__=='__main__':print(json.dumps(validate(),ensure_ascii=False))
