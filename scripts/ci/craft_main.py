"""固定13仓main候选；只在隔离checkout构建，不改活动插件或稳定版锁。"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import re

LOCK = Path(__file__).with_name('craft_main_candidates.lock.json')


def build_matrix():
    return {'include': json.loads(LOCK.read_text())['candidates']}


def candidate(app):
    for row in build_matrix()['include']:
        if row['app'] == app:
            return row
    raise ValueError('Unknown Craft application: ' + app)


def run(*argv, cwd=None, env=None):
    subprocess.run(list(map(str, argv)), cwd=cwd, env=env, check=True)


def verify_checkout(source, expected):
    actual = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    if actual != expected:
        raise ValueError(f'Wrong checkout {source}: {actual} != {expected}')


def apply_candidate_patches(row, source, plugin):
    patches = row.get('candidatePatches', [])
    if patches:
        verify_checkout(plugin, row['pluginCommit'])
    for patch in patches:
        if Path(patch['file']).name != patch['file']:
            raise ValueError('Unsafe candidate patch filename')
        path = plugin / 'ui/runtime/patches' / patch['file']
        if hashlib.sha256(path.read_bytes()).hexdigest() != patch['sha256']:
            raise ValueError('Candidate patch checksum mismatch')
        run('git', 'apply', '--check', path, cwd=source)
        run('git', 'apply', path, cwd=source)


def prepare_web(row, source, plugin):
    """适配仅作用于CI副本，绝不更新仓库中的source/editor锁。"""
    verify_checkout(source, row['commit'])
    verify_checkout(plugin, row['pluginCommit'])
    apply_candidate_patches(row, source, plugin)
    if row['editorMode'] != 'source-overlay':
        return
    ui = plugin / 'ui'
    lock = json.loads((ui / 'source.lock.json').read_text())
    for patch in lock.get('patches', []):
        if Path(patch).name != patch:
            raise ValueError('Unsafe overlay filename')
        run('git', 'apply', ui / 'runtime/patches' / patch, cwd=source)
    run('python3', ui / 'runtime/prepare-automation.py', source, row['engine'])
    if (ui / 'runtime/prepare-fonts.py').is_file():
        run('python3', ui / 'runtime/prepare-fonts.py', source, row['engine'])


def build_web(row, source, plugin):
    verify_checkout(source, row['commit'])
    verify_checkout(plugin, row['pluginCommit'])
    ui = plugin / 'ui'
    run('npm', 'ci', cwd=ui)
    target = (source / 'target').resolve()
    env = {**os.environ, 'CARGO_INCREMENTAL': '0', 'CARGO_TARGET_DIR': str(target)}
    if row['editorMode'] == 'source-overlay':
        prepare_web(row, source, plugin)
        lock = json.loads((ui / 'source.lock.json').read_text())
        lock.update(repository='https://github.com/' + row['repository'], commit=row['commit'],
                    candidateStatus=row['status'])
        (ui / 'source.lock.json').write_text(json.dumps(lock, indent=2) + '\n')
        if (ui / 'fetch-fonts.py').is_file():
            fonts = plugin.parent / 'candidate-fonts'
            run('python3', ui / 'fetch-fonts.py', '--output', fonts)
            env.update(CRAFT_FONTS_DIR=str(fonts), CRAFT_FONTS_REQUIRED='1',
                       CRAFT_CJK_FONT=str(fonts / 'fonts/LXGWWenKai-Regular.ttf'), FIGCRAFT_EMBED_CJK='1')
        html = (source / 'apps' / (row['engine'] + '-web') / 'index.html').read_text()
        match = re.search('data-cargo-profile="([^"]+)"', html)
        profile = match[1] if match else 'release'
        run('cargo', 'build', '--target', 'wasm32-unknown-unknown', '--profile', profile,
            '-p', row['engine'] + '-web', '-j', '2', cwd=source, env=env)
        package = plugin.parent / 'candidate-web-package'
        run('python3', ui / 'finalize-source.py', '--source', source,
            '--target-dir', target, '--output', package, env=env)
        shutil.copytree(package / 'editor', ui / 'dist/editor')
    else:
        run('bash', 'packaging/web/package.sh', cwd=source, env=env)
        archives = list((source / 'dist/release').glob(row['engine'] + '-web-*.zip'))
        if len(archives) != 1:
            raise ValueError('Expected one official-format Web archive')
        # prepare.py按候选归档摘要检查与解包，修改仅位于隔离plugin checkout。
        archive = archives[0]
        lock = json.loads((ui / 'editor.lock.json').read_text())
        lock.update(sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
                    candidateStatus=row['status'], upstreamCommit=row['commit'])
        (ui / 'editor.lock.json').write_text(json.dumps(lock, indent=2) + '\n')
        run('python3', ui / 'prepare.py', archive)
    run('npm', 'run', 'build', cwd=ui)
    dest = Path('candidate-web').resolve()
    dest.mkdir(exist_ok=False)
    shutil.copytree(ui / 'dist', dest / 'ui/dist')
    hashes = {str(p.relative_to(dest)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in dest.rglob('*') if p.is_file()}
    (dest / 'provenance.json').write_text(json.dumps({**row, 'files': hashes,
        'browserAcceptance': 'PENDING', 'installedHostAcceptance': 'NOT_TESTED'}, indent=2) + '\n')
    (dest / 'overlay.diff').write_bytes(subprocess.check_output(['git', 'diff'], cwd=source))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('action', choices=['matrix', 'prepare-web', 'build-native', 'build-web'])
    p.add_argument('--app')
    p.add_argument('--apps', default='all')
    p.add_argument('--source', type=Path, default=Path('upstream'))
    p.add_argument('--plugin', type=Path, default=Path('candidate-plugin'))
    a = p.parse_args()
    if a.action == 'matrix':
        rows = build_matrix()
        if a.apps != 'all':
            names = a.apps.split(',')
            if len(set(names)) != len(names):
                p.error('Duplicate application')
            rows = {'include': [candidate(name) for name in names]}
        print(json.dumps(rows, separators=(',', ':')))
        return
    row = candidate(a.app)
    source = a.source.resolve()
    if a.action == 'prepare-web':
        prepare_web(row, source, a.plugin.resolve())
        return
    if a.action == 'build-web':
        build_web(row, source, a.plugin.resolve())
        return
    verify_checkout(source, row['commit'])
    apply_candidate_patches(row, source, a.plugin.resolve())
    env = {**os.environ, 'CARGO_INCREMENTAL': '0'}
    run('cargo', 'build', '--locked', '--release', '-p', row['engine'] + '-cli', cwd=source, env=env)
    exe = source / 'target/release' / (row['engine'] + '-cli' + ('.exe' if os.name == 'nt' else ''))
    dest = Path('candidate-native').resolve()
    dest.mkdir(exist_ok=False)
    shutil.copy2(exe, dest / exe.name)
    tests = 'NOT_RUN'
    if row['app'] == 'photocraft' and row.get('candidatePatches'):
        with (dest / 'upstream-export-presets-tests.log').open('wb') as log:
            subprocess.run(['cargo', 'test', '--release', '--locked', '-p', 'photocraft-engine',
                            'export_preset_cmds::tests', '--', '--nocapture'], cwd=source,
                           env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
        tests = 'PASS'
    (dest / 'provenance.json').write_text(json.dumps({**row, 'executable': exe.name,
        'exeSha256': hashlib.sha256(exe.read_bytes()).hexdigest(),
        'upstreamExportPresetTests': tests,
        'rustc': subprocess.check_output(['rustc', '--version'], text=True).strip()}, indent=2) + '\n')


if __name__ == '__main__':
    main()
