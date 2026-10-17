#!/usr/bin/env python3
"""仅用标准库安装锁定的官方 CLI；技能单独复制后仍可运行。"""
import argparse
import importlib.util
import tarfile
import hashlib
import http.client
import ssl
import urllib.error
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import stat
import subprocess
import tempfile
import time
import urllib.request
import zipfile

MAX_BYTES = 1024 * 1024 * 1024
LOCK_WAIT_SECONDS = 120


def portable():
    spec = importlib.util.spec_from_file_location('craft_platform', Path(__file__).with_name('platform_support.py'))
    value = importlib.util.module_from_spec(spec); spec.loader.exec_module(value)
    return value


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def download(url, destination):
    """下载完成并核对摘要之前，永不运行内容。"""
    if not url.startswith('https://github.com/storytold/'):
        raise ValueError('untrusted_release_url')
    request = urllib.request.Request(url, headers={'User-Agent': 'craft-skill-bootstrap/0.1'})
    destination = Path(destination)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=60) as source, destination.open('wb') as out:
                if not source.url.startswith('https://'):
                    raise ValueError('insecure_redirect')
                total = 0
                while block := source.read(1024 * 1024):
                    total += len(block)
                    if total > MAX_BYTES:
                        raise ValueError('archive_too_large')
                    out.write(block)
                declared = source.headers.get('Content-Length')
                if declared is not None and declared.isdigit() and total != int(declared):
                    raise http.client.IncompleteRead(b'', int(declared) - total)
            return
        except (urllib.error.URLError, TimeoutError, ConnectionError, ssl.SSLEOFError, http.client.IncompleteRead) as error:
            # 只读制品下载可以恢复；半包不可复用，不重试原生编辑或完整性失败。
            if destination.exists():
                destination.unlink()
            if isinstance(error, urllib.error.HTTPError) and error.code not in (408, 429) and not 500 <= error.code <= 599:
                raise
            if isinstance(error, urllib.error.URLError) and isinstance(error.reason, ssl.SSLCertVerificationError):
                raise
            if attempt == 2:
                raise ValueError('artifact_download_failed: three read-only attempts exhausted') from error
            time.sleep(attempt + 1)


def extract(archive, destination):
    """先检查全部成员，再解压；拒绝链接、重复路径和越界。"""
    if tarfile.is_tarfile(archive):
        with tarfile.open(archive, 'r:*') as source:
            members = source.getmembers(); seen = set(); total = 0
            for item in members:
                path = PurePosixPath(item.name)
                if (path.is_absolute() or '..' in path.parts or '\\' in item.name
                        or ':' in item.name or not (item.isfile() or item.isdir())
                        or str(path) in seen):
                    raise ValueError('unsafe_archive: ' + item.name)
                seen.add(str(path)); total += item.size
                if total > MAX_BYTES:
                    raise ValueError('archive_too_large')
            source.extractall(destination, members=members, filter='data')
        return
    with zipfile.ZipFile(archive) as source:
        seen = set()
        total = 0
        for item in source.infolist():
            path = PurePosixPath(item.filename)
            mode = item.external_attr >> 16
            if (path.is_absolute() or '..' in path.parts or '\\' in item.filename
                    or ':' in item.filename or stat.S_ISLNK(mode)
                    or str(path) in seen or not path.parts
                    or (stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR))):
                raise ValueError('unsafe_archive: ' + item.filename)
            seen.add(str(path))
            total += item.file_size
            if total > MAX_BYTES:
                raise ValueError('archive_too_large')
        source.extractall(destination)


def inspect_install(destination, artifact, expected, version=None, platform_key=None):
    binary = destination / expected.get('binaryPath', artifact)
    if destination.is_symlink() or binary.is_symlink() or not binary.is_file():
        raise ValueError('invalid_installed_path')
    if digest(binary) != expected['binarySha256']:
        raise ValueError('installed_checksum_mismatch; preserve directory for inspection')
    if expected.get('integrityFile'):
        manifest=Path(__file__).parent/expected['integrityFile']
        if digest(manifest)!=expected['integritySha256']:raise ValueError('runtime_integrity_manifest_changed')
        files=json.loads(manifest.read_text(encoding='utf-8'))
        actual={str(p.relative_to(destination)).replace(os.sep,'/'):digest(p) for p in destination.rglob('*') if p.is_file() and p.name!='installation.json'}
        if any(p.is_symlink() for p in destination.rglob('*')) or actual!=files:
            raise ValueError('runtime_payload_changed; preserve directory for inspection')
    receipt = destination / 'installation.json'
    if receipt.is_symlink() or not receipt.is_file():
        raise ValueError('installation_receipt_missing')
    def unique_fields(pairs):
        result={}
        for key,value in pairs:
            if key in result:raise ValueError('duplicate installation field')
            result[key]=value
        return result
    identity={field:expected[field] for field in ('url','archiveSha256','binarySha256','binaryPath','payloadRoot','integrityFile','integritySha256','provenanceSha256') if field in expected}
    identity.update(name=artifact.removesuffix('-cli'),source='official-github-release')
    if version is not None:
        identity.update(version=version,versionOutput=expected.get('versionOutput',f'{artifact} {version}'))
    elif 'versionOutput' in expected:identity['versionOutput']=expected['versionOutput']
    if platform_key is not None:identity['platform']=platform_key
    try:
        record=json.loads(receipt.read_text(encoding='utf-8'),object_pairs_hook=unique_fields,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite receipt')))
        if not isinstance(record,dict) or any(record.get(k)!=v for k,v in identity.items()):
            raise ValueError('receipt identity mismatch')
    except (ValueError,OSError):
        raise ValueError('installation_receipt_invalid; preserve directory for inspection') from None
    return {'executable': str(binary), 'reused': True, 'binarySha256': expected['binarySha256']}


def install(lock, runtime_home, archive=None, platform_key=None):
    """每个版本只安装一次；失败不覆盖旧版，也不改变 PATH 或用户配置。"""
    key = platform_key or portable().platform_key()
    # 锁结构先验证：损坏的独立安装材料不能触发目录写入或下载。
    if (not isinstance(lock, dict) or not isinstance(lock.get('artifacts'), dict)
            or not isinstance(lock.get('artifact'), str)
            or not isinstance(lock.get('resolvedVersion'), str)):
        raise ValueError('runtime_lock_invalid')
    if key not in lock['artifacts']:
        raise ValueError('unsupported_platform: ' + key)
    expected = lock['artifacts'][key]
    if (not isinstance(expected, dict)
            or not isinstance(expected.get('url'), str) or not expected['url']
            or any(not isinstance(expected.get(field), str)
                   or not re.fullmatch(r'[a-f0-9]{64}', expected[field])
                   for field in ('archiveSha256', 'binarySha256'))
            or ('versionOutput' in expected and not isinstance(expected['versionOutput'], str))
            or ('provenanceSha256' in expected and
                (not isinstance(expected['provenanceSha256'], str)
                 or not re.fullmatch(r'[a-f0-9]{64}', expected['provenanceSha256'])))):
        raise ValueError('runtime_lock_invalid')
    artifact, version = lock['artifact'], lock['resolvedVersion']
    if not re.fullmatch(r'[a-z]+craft-cli', artifact) or not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('invalid_runtime_identity')
    portable().check_minimum(expected.get('minimumSystem',{}))
    parent = Path(runtime_home).expanduser().absolute() / artifact.removesuffix('-cli')
    parent.mkdir(parents=True, exist_ok=True)
    if parent.is_symlink():
        raise ValueError('invalid_runtime_directory')
    destination = parent / version
    guard = portable()
    with guard.exclusive_lock(parent / '.install.lock', LOCK_WAIT_SECONDS):
        if destination.exists() or destination.is_symlink():
            return inspect_install(destination, artifact, expected, version, key)
        # 单技能受管理调用无需额外安装步骤；显式参数优先，离线失败不回落下载。
        if archive is None:
            archive = os.environ.get('CRAFT_RUNTIME_ARCHIVE') or None
        with tempfile.TemporaryDirectory(prefix='.install-', dir=parent) as temporary:
            stage = Path(temporary)
            package = Path(archive) if archive else stage / 'release.zip'
            if archive is None:
                download(expected['url'], package)
            if digest(package) != expected['archiveSha256']:
                raise ValueError('archive_checksum_mismatch')
            unpacked = stage / 'unpacked'
            extract(package, unpacked)
            binary_name = Path(expected.get('binaryPath', artifact)).name
            binaries = [p for p in unpacked.rglob(binary_name) if p.is_file()]
            if len(binaries) != 1 or digest(binaries[0]) != expected['binarySha256']:
                raise ValueError('binary_checksum_mismatch')
            payload = stage / 'payload'
            if 'binaryPath' in expected:
                relative = PurePosixPath(expected['binaryPath'])
                payload_root = PurePosixPath(expected.get('payloadRoot', '.'))
                if relative.is_absolute() or '..' in relative.parts or payload_root.is_absolute() or '..' in payload_root.parts:
                    raise ValueError('unsafe_payload_path')
                shutil.copytree(unpacked / payload_root, payload)
                binary = payload / relative
                if not binary.is_file() or digest(binary) != expected['binarySha256']:
                    raise ValueError('binary_checksum_mismatch')
            else:
                payload.mkdir()
                binary = payload / artifact
                shutil.copyfile(binaries[0], binary)
            binary.chmod(0o755)
            licenses = [p for p in unpacked.rglob('*') if p.is_file() and p.name.lower().startswith(('license', 'copying'))]
            if not licenses:
                raise ValueError('license_missing')
            for index, path in enumerate(licenses):
                target = payload / path.name
                if target.exists():
                    continue
                shutil.copyfile(path, target)
            result = subprocess.run([str(binary), '--version'], capture_output=True, text=True, timeout=20, check=True)
            if result.stdout.strip() != expected.get('versionOutput', f'{artifact} {version}'):
                raise ValueError('runtime_version_mismatch')
            receipt = dict(expected, name=artifact.removesuffix('-cli'), version=version,
                           platform=key, versionOutput=result.stdout.strip(), source='official-github-release')
            (payload / 'installation.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8', newline='\n')
            inspect_install(payload,artifact,expected,version,key)
            # 同文件系统原子发布。没有任何自动升级/替换已有版本的分支。
            payload.rename(destination)
            return dict(inspect_install(destination, artifact, expected, version, key), reused=False)


def setup_failure(runtime_home):
    """定位当前独立技能的安装入口；仅提供诊断，不触发重试。"""
    return {'skill': 'effectcraft-cli-setup',
            'bootstrapScript': str(Path(__file__).resolve()),
            'runtimeHome': str(Path(runtime_home).expanduser().absolute()),
            'automaticRetry': False}


def main():
    # 固定重定向输出编码，Windows默认代码页也能返回中文帮助和回执。
    import sys
    for stream in (sys.stdout,sys.stderr):
        if hasattr(stream,"reconfigure"):stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime-home', default=os.environ.get('CRAFT_RUNTIME_HOME', str(Path.home() / '.local/share/craft-runtimes')))
    parser.add_argument('--archive', type=Path, help='已下载的官方 ZIP；仍强制校验锁定摘要')
    args = parser.parse_args()
    try:
        lock = json.loads(Path(__file__).with_name('runtime.lock.json').read_text(encoding='utf-8'))
        print(json.dumps(install(lock, args.runtime_home, args.archive), ensure_ascii=False))
    except (ValueError, OSError, subprocess.SubprocessError, zipfile.BadZipFile) as error:
        print(json.dumps({'error': str(error), 'installed': False, 'dependencySetup': setup_failure(args.runtime_home)}, ensure_ascii=False))
        raise SystemExit(1)


if __name__ == '__main__':
    main()
