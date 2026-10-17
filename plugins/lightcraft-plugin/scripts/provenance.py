"""候选/发行来源验证；上游技能与本地扩展分别登记。"""
import runpy
import hashlib
import json
from pathlib import Path
import re
import subprocess

EXPECTED_SKILLS = ['lightcraft-cli', 'lightcraft-cli-develop', 'lightcraft-cli-export',
                   'lightcraft-cli-library', 'lightcraft-cli-setup', 'lightcraft-use']


def inventory(root):
    paths = sorted(Path(root).rglob('*'))
    if Path(root).is_symlink() or any(p.is_symlink() for p in paths):
        raise ValueError('snapshot_symlink')
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths if p.is_file() and '__pycache__' not in p.parts}


def validate(root, source_git=None):
    root = Path(root)
    manifest = json.loads((root / 'plugin.json').read_text())
    if manifest.get('name') != 'lightcraft':
        raise ValueError('plugin_identity_mismatch')
    if manifest.get('$schema') != 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json':
        raise ValueError('unsupported_plugin_schema')
    suite = json.loads((root / 'source-suite.json').read_text())
    lock = json.loads((root / 'candidate-source.json').read_text())
    if (suite.get('domain') != 'lightcraft' or suite.get('skills') != EXPECTED_SKILLS
            or lock.get('sourceProject') != 'lightcraft-skills'
            or lock.get('sourceVersion') != suite.get('version')
            or lock.get('managedSkills') != EXPECTED_SKILLS):
        raise ValueError('source_identity_mismatch')
    names = sorted(p.name for p in (root / 'skills').iterdir() if p.is_dir())
    local = json.loads((root / 'local-components.json').read_text())
    scenes = runpy.run_path(str(root/'scripts/validate_editor_scenes.py'))['candidate_names'](root)
    if local.get('skills') != [] or set(names) != set(EXPECTED_SKILLS) | scenes:
        raise ValueError('skill_set_mismatch')
    managed = {p:d for p,d in inventory(root/'skills').items() if p.split('/')[0] in EXPECTED_SKILLS}
    if managed != lock.get('skillFileSha256'):
        raise ValueError('snapshot_drift')
    if lock.get('sourceStatus') == 'local-unpublished-candidate':
        if lock.get('releaseTag') is not None or lock.get('commit') is not None:
            raise ValueError('false_release_identity')
        return {'sourceRelease': 'UNPUBLISHED', 'sourceVersion': suite['version'], 'snapshot': 'PASS'}
    if lock.get('sourceStatus') != 'published-immutable-release':
        raise ValueError('unsupported_source_status')
    if not source_git:
        raise ValueError('release_tag_commit_verification_required')
    if lock.get('repository') != 'https://github.com/full-aigc-skills/lightcraft-skills':
        raise ValueError('source_repository_mismatch')
    tag = lock.get('releaseTag', '')
    if tag != 'v' + suite['version'] or not re.fullmatch(r'[0-9a-f]{40}', lock.get('commit', '')):
        raise ValueError('release_identity_invalid')
    result = subprocess.run(['git', '-C', str(source_git), 'rev-parse', '--verify', 'refs/tags/' + tag + '^{commit}'],
                            capture_output=True, text=True, check=True)
    if result.stdout.strip() != lock['commit']:
        raise ValueError('release_tag_commit_mismatch')
    for path, expected in lock['skillFileSha256'].items():
        blob = subprocess.run(['git', '-C', str(source_git), 'show', lock['commit'] + ':skills/' + path], capture_output=True, check=True)
        if hashlib.sha256(blob.stdout).hexdigest() != expected:
            raise ValueError('release_content_mismatch: ' + path)
    return {'sourceRelease': tag, 'commit': lock['commit'], 'snapshot': 'PASS', 'remotePublication': 'NOT_VERIFIED'}
