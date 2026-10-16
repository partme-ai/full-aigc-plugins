"""检查完整分发包，通过真实 Codex 安装器和 app-server 验证；不使用 MCP SDK。"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import queue
import re
import shutil
import stat
import subprocess
import sys
import threading
import time
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen
import zipfile

NAMES = 'cadcraft designcraft effectcraft photocraft figcraft filmcraft lightcraft printcraft vectorcraft deckcraft soundcraft gridcraft wordcraft'.split()
RESERVED = {'CON', 'PRN', 'AUX', 'NUL', *('COM' + str(i) for i in range(1, 10)), *('LPT' + str(i) for i in range(1, 10))}


def safe_name(name):
    path = PurePosixPath(name)
    if not name or path.is_absolute() or '\\' in name or any(
        part in {'', '.', '..'} or part.endswith((' ', '.')) or re.search(r'[<>:"|?*\x00-\x1f]', part)
        or part.split('.')[0].upper() in RESERVED for part in name.rstrip('/').split('/')
    ):
        raise ValueError('Windows unsafe archive path: ' + name)
    return path


def extract_package(archive, destination, name):
    """在任意平台检查 Windows 路径语义，缺资源或摘要不符立即失败。"""
    if destination.exists():
        raise ValueError('Destination already exists')
    seen = set()
    with zipfile.ZipFile(archive) as z:
        if sum(i.file_size for i in z.infolist()) > 2 * 1024**3:
            raise ValueError('Archive exceeds 2 GiB expanded size')
        for item in z.infolist():
            path = safe_name(item.filename)
            if path.parts[0] != name + '-plugin' or stat.S_ISLNK(item.external_attr >> 16):
                raise ValueError('Unexpected package root or symlink')
            key = str(path).casefold()
            if key in seen:
                raise ValueError('Windows case collision: ' + item.filename)
            seen.add(key)
        z.extractall(destination)
    root = destination / (name + '-plugin')
    for file in ['plugin.json', 'mcp.json', '.codex-plugin/plugin.json', '.codex-plugin/mcp.json',
                 'ui/dist/adapter.mjs', 'ui/editor.lock.json']:
        if not (root / file).is_file():
            raise ValueError('Incomplete install package, missing ' + file)
    identity = json.loads((root / 'plugin.json').read_text(encoding='utf-8'))
    host = json.loads((root / '.codex-plugin/plugin.json').read_text(encoding='utf-8'))
    if identity['name'] != name or any(identity[k] != host[k] for k in ['name', 'version']):
        raise ValueError('Plugin identity/version mismatch')
    lock = json.loads((root / 'ui/editor.lock.json').read_text(encoding='utf-8'))
    if lock.get('mode') == 'web-api':
        # 官方 Web 包锁定的是 ZIP 摘要，不是增强包的逐文件锁。
        for file in ['config.json', 'web-panel.js', 'web-connect.js', 'editor/index.html',
                     f'editor/{name}_web.js', f'editor/{name}_web_bg.wasm']:
            if not (root / 'ui/dist' / file).is_file():
                raise ValueError('Missing Web runtime resource: ' + file)
        if (root / f'ui/dist/editor/{name}_web_bg.wasm').read_bytes()[:4] != b'\x00asm':
            raise ValueError('Invalid WASM resource')
        if not re.fullmatch(r'[0-9a-f]{64}', lock.get('sha256', '')):
            raise ValueError('Missing upstream archive digest')
        return root
    if not lock.get('files'):
        raise ValueError('Missing editor resource hashes')
    for file, digest in lock['files'].items():
        safe_name(file)
        target = root / 'ui/dist/editor' / file
        if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != digest:
            raise ValueError('Missing/corrupt locked resource: ' + file)
    return root


def download(url, target, digest):
    if urlparse(url).scheme != 'https' or not re.fullmatch(r'[0-9a-f]{64}', digest):
        raise ValueError('HTTPS URL and SHA-256 required')
    with urlopen(url, timeout=90) as response, target.open('wb') as output:
        shutil.copyfileobj(response, output)
    if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
        raise ValueError('Download checksum mismatch: ' + target.name)


class NativeHost:
    def __init__(self, cli, env, output):
        self.responses = queue.Queue()
        self.seq = 0
        self.trace = []
        self.output = output
        self.stderr = (output / 'app-server.stderr.log').open('w', encoding='utf-8')
        self.process = subprocess.Popen(cli + ['app-server'], env=env, stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=self.stderr, text=True,
                                        encoding='utf-8', bufsize=1)
        def read():
            for line in self.process.stdout:
                try:
                    self.responses.put(json.loads(line))
                except json.JSONDecodeError:
                    self.responses.put({'invalidOutput': line})
        threading.Thread(target=read, daemon=True).start()

    def call(self, method, params):
        self.seq += 1
        self.process.stdin.write(json.dumps({'id': self.seq, 'method': method, 'params': params}) + '\n')
        self.process.stdin.flush()
        end = time.monotonic() + 120
        while True:
            remaining = end - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(method)
            try:
                response = self.responses.get(timeout=remaining)
            except queue.Empty:
                raise TimeoutError('app-server response timeout: ' + method) from None
            if 'invalidOutput' in response:
                raise RuntimeError('Non-JSON app-server stdout')
            if response.get('id') != self.seq:
                continue
            self.trace.append({'method': method, 'params': params, 'response': response})
            (self.output / 'native-rpc.json').write_text(json.dumps(self.trace, indent=2), encoding='utf-8')
            if 'error' in response:
                raise RuntimeError(str(response['error']))
            return response['result']

    def close(self):
        self.process.terminate()
        try:
            self.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=10)
        self.stderr.close()


def native_smoke(root, name, cli, output):
    market = output / '中文 插件市场'
    manifest = market / '.agents/plugins/marketplace.json'
    manifest.parent.mkdir(parents=True)
    # 包已经搬到同一个市场下，安装来源保持相对路径。
    relative = './' + os.path.relpath(root, market).replace(os.sep, '/')
    manifest.write_text(json.dumps({'name': 'craft-windows-ci', 'plugins': [{
        'name': name, 'source': {'source': 'local', 'path': relative},
        'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}, 'category': 'Creativity'
    }]}), encoding='utf-8')
    env = {**os.environ, 'CODEX_HOME': str(output / '独立 Codex Home'),
           'CRAFT_EDITOR_UPDATE': 'off', 'CRAFT_EDITOR_CACHE_DIR': str(output / '编辑器 Cache')}
    Path(env['CODEX_HOME']).mkdir()
    for args, log in [(['--version'], 'codex-version.log'),
                      (['plugin', 'marketplace', 'add', str(market)], 'marketplace-install.log'),
                      (['plugin', 'add', name + '@craft-windows-ci', '--json'], 'plugin-install.json')]:
        result = subprocess.run(cli + args, env=env, capture_output=True, text=True, encoding='utf-8', timeout=120)
        (output / log).write_text(result.stdout + result.stderr, encoding='utf-8')
        if result.returncode:
            raise RuntimeError('Native installer failed: ' + log)
    workspace = output / '中文 工作区 with spaces'
    workspace.mkdir()
    host = NativeHost(cli, env, output)
    try:
        host.call('initialize', {'clientInfo': {'name': 'craft-windows-ci', 'version': '1'},
                                'capabilities': {'experimentalApi': True}})
        host.process.stdin.write('{"method":"initialized"}\n')
        host.process.stdin.flush()
        thread = host.call('thread/start', {'cwd': str(workspace), 'approvalPolicy': 'never', 'sandbox': 'workspace-write'})['thread']['id']
        status = host.call('mcpServerStatus/list', {'threadId': thread})
        server = next((s for s in status['data'] if s['name'] == name + '-editor'), None)
        if not server or server.get('runtimeStatus') != 'connected' or 'open_browser_editor' not in server.get('tools', {}):
            raise RuntimeError('Native MCP not connected or tools missing')
        def tool(name_, arguments):
            value = host.call('mcpServer/tool/call', {'threadId': thread, 'server': name + '-editor',
                                                   'tool': name_, 'arguments': arguments})
            if value.get('isError'):
                raise RuntimeError(json.dumps(value))
            return value
        tool('editor_status', {})
        opened = tool('open_browser_editor', {'workspace': str(workspace)})['structuredContent']
        if Path(opened['workspace']).resolve() != workspace.resolve():
            raise RuntimeError('Workspace incorrectly resolved')
        url = opened['editorUrl']
        if urlparse(url).hostname != '127.0.0.1':
            raise RuntimeError('Editor is not loopback-bound')
        with urlopen(url, timeout=30) as response:
            if response.status != 200 or 'html' not in response.headers.get('Content-Type', ''):
                raise RuntimeError('Editor HTML unavailable')
        tool('editor_status', {})
        return {'nativeInstall': 'PASS', 'nativeMcpCalls': 'PASS', 'editorHtml': 'PASS',
                'embeddedUi': 'NOT_TESTED', 'editingSync': 'NOT_TESTED'}
    finally:
        host.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--plugin', choices=NAMES, required=True)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--index-url')
    source.add_argument('--archive', type=Path)
    parser.add_argument('--sha256', required=True, help='index or archive SHA-256')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--codex-js', type=Path, help='npm Codex JS entry, avoiding Windows .cmd shell quoting')
    parser.add_argument('--require-windows', action='store_true')
    parser.add_argument('--preflight-only', action='store_true')
    args = parser.parse_args()
    args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=False)
    report = {'plugin': args.plugin, 'platform': sys.platform, 'status': 'FAIL',
              'nativeInstall': 'NOT_TESTED', 'nativeMcpCalls': 'NOT_TESTED',
              'embeddedUi': 'NOT_TESTED', 'editingSync': 'NOT_TESTED'}
    try:
        if args.require_windows and sys.platform != 'win32':
            raise RuntimeError('This acceptance requires an actual Windows runner')
        archive = args.archive
        if args.index_url:
            index = args.output / 'index.json'
            download(args.index_url, index, args.sha256)
            entries = [e for e in json.loads(index.read_text(encoding='utf-8')) if e['plugin'] == args.plugin]
            if len(entries) != 1:
                raise ValueError('Expected exactly one package in index')
            entry = entries[0]
            if PurePosixPath(entry['file']).name != entry['file']:
                raise ValueError('Archive index file must be a basename')
            archive = args.output / entry['file']
            download(urljoin(args.index_url, entry['file']), archive, entry['sha256'])
        elif hashlib.sha256(archive.read_bytes()).hexdigest() != args.sha256:
            raise ValueError('Archive checksum mismatch')
        root = extract_package(archive, args.output / '中文 插件市场/plugins', args.plugin)
        report['package'] = 'PASS'
        if not args.preflight_only:
            cli = [shutil.which('node'), str(args.codex_js.resolve())] if args.codex_js else [shutil.which('codex')]
            if not cli[0]:
                raise RuntimeError('Codex/Node executable unavailable')
            report.update(native_smoke(root, args.plugin, cli, args.output))
        report['status'] = 'PASS'
    except Exception as exc:
        report['error'] = str(exc)
        raise
    finally:
        (args.output / 'result.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        print(json.dumps(report))


if __name__ == '__main__':
    main()
