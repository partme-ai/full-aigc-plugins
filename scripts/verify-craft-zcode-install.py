#!/usr/bin/env python3
"""隔离调用真实宿主安装器，核对完整包资源；不声称MCP或UI验收通过。"""
from pathlib import Path
import argparse, hashlib, json, os, subprocess
ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cli-js', type=Path, required=True)
    parser.add_argument('--marketplace', type=Path, default=ROOT / 'candidate-marketplace')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    env = {**os.environ, 'ZCODE_STORAGE_DIR': str(out / 'storage'),
           'ZCODE_DATA_BASE_DIR': str(out / 'data'), 'ZCODE_MODEL_TELEMETRY_ENABLED': '0'}
    base = ['node', str(args.cli_js.resolve())]
    def call(arguments, log):
        result = subprocess.run(base + arguments, env=env, capture_output=True, text=True, timeout=180)
        (out / log).write_text(result.stdout + result.stderr, encoding='utf-8')
        if result.returncode:
            raise RuntimeError((result.stdout + result.stderr)[-1800:])
        return json.loads(result.stdout)
    call(['plugins', 'marketplace', 'add', str(args.marketplace.resolve()), '--scope', 'user', '--json'], 'market-add.log')
    listings = json.loads((args.marketplace / 'marketplace.json').read_text())
    reports = []
    for row in json.loads((ROOT / 'docs/craft-marketplace-candidate-releases.json').read_text()):
        name = row['plugin']
        listing = next(entry for entry in listings['plugins'] if entry['name'] == name)
        receipt = call(['plugins', 'install', name + '@' + listings['name'], '--scope', 'user', '--json'], name + '-install.log')
        installed = Path(receipt['installed'][0]['installPath'])
        assert receipt['installed'][0]['version'] == row['version']
        bundled = listing['source'].get('type') == 'zip'
        if bundled:
            lock = json.loads((installed / 'ui/runtime.lock.json').read_text())
            for file, digest in lock['files'].items():
                assert hashlib.sha256((installed / 'ui/dist' / file).read_bytes()).hexdigest() == digest, file
        report = {'plugin': name, 'version': row['version'], 'installation': 'PASS',
                  'source': 'complete-zip' if bundled else 'git-host-size-limit-fallback',
                  'installedBundledDigests': 'PASS' if bundled else 'NOT_APPLICABLE',
                  'mcpCall': 'NOT_TESTED', 'embeddedUI': 'NOT_TESTED'}
        reports.append(report)
        (out / 'results.json').write_text(json.dumps(reports, indent=2) + '\n')
        print(json.dumps(report), flush=True)

if __name__ == '__main__':
    main()
