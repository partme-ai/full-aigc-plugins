"""比较实际运行目录的调用契约；enabled等会话状态不算新增能力。"""
import argparse
import hashlib
import json
from pathlib import Path


def index(rows):
    if not isinstance(rows, list):
        raise ValueError('Expected observed catalog array')
    result = {}
    for row in rows:
        key = row.get('id') or row.get('name')
        if not isinstance(key, str) or not key or key in result:
            raise ValueError('Missing/duplicate catalog identifier')
        result[key] = {field: row[field] for field in
                       ['params', 'inputSchema', 'outputSchema', 'input_schema', 'output_schema',
                        'command', 'description', 'mutates', 'read_only', 'interactive', 'aliases']
                       if field in row}
    return result


def compare(before, after):
    a, b = index(before), index(after)
    return {'baselineCount': len(a), 'mainCount': len(b), 'added': sorted(b.keys() - a.keys()),
            'removed': sorted(a.keys() - b.keys()),
            'contractsChanged': [{'id': key, 'baseline': a[key], 'main': b[key]}
                                 for key in sorted(a.keys() & b.keys()) if a[key] != b[key]]}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--baseline', type=Path, required=True)
    p.add_argument('--candidate', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    result = compare(json.loads(a.baseline.read_bytes()), json.loads(a.candidate.read_bytes()))
    result.update(baselineSha256=hashlib.sha256(a.baseline.read_bytes()).hexdigest(),
                  candidateSha256=hashlib.sha256(a.candidate.read_bytes()).hexdigest(),
                  scope='observed-command-contracts-not-full-semantic-audit')
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
