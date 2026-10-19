#!/usr/bin/env python3
"""Check the current portable plugin payload against its locked skill source."""

import hashlib
import json
import re
import sys
from pathlib import Path


SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
ROOT_ENTRIES = {"plugin.json", "skills", "LICENSE"}


def skill_digest(directory: Path) -> str:
    rows = []
    for path in sorted(directory.rglob("*")):
        if path.is_file():
            rows.append(
                path.relative_to(directory).as_posix()
                + "\0"
                + hashlib.sha256(path.read_bytes()).hexdigest()
                + "\n"
            )
    return hashlib.sha256("".join(rows).encode()).hexdigest()


def verify(package: Path, lock_path: Path) -> dict:
    if package.is_symlink() or not package.is_dir():
        raise ValueError("invalid_package_root")
    entries = {path.name for path in package.iterdir()}
    if entries not in (ROOT_ENTRIES, ROOT_ENTRIES | {'scenario-candidates.json'}):
        raise ValueError("unsupported_root_entry")
    if any(path.is_symlink() for path in package.rglob("*")):
        raise ValueError("package_symlink")
    if not (package / "plugin.json").is_file() or not (package / "LICENSE").is_file():
        raise ValueError("missing_package_metadata")
    manifest = json.loads((package / "plugin.json").read_text())
    if manifest.get("$schema") != SCHEMA or manifest.get("name") != "vectorcraft":
        raise ValueError("invalid_plugin_manifest")
    lock = json.loads(lock_path.read_text())
    sources = lock.get("sources")
    if not isinstance(sources, list) or len(sources) != 1:
        raise ValueError("invalid_skill_lock")
    source = sources[0]
    names = source["skills"]
    if set(names) != set(source["sha256"]) or len(names) != len(set(names)):
        raise ValueError("invalid_skill_lock")
    candidates = set()
    if 'scenario-candidates.json' in entries:
        declaration = json.loads((package / 'scenario-candidates.json').read_text())
        authorities = {'vectorcraft-skills', 'full-aigc-skills/vectorcraft-skills'}
        if source.get('package') not in authorities or declaration.get('status') != 'local-unreleased' or declaration.get('sourcePackage') not in authorities:
            raise ValueError('invalid_candidate_authority')
        if not isinstance(declaration.get('skills'), list):
            raise ValueError('invalid_candidate_inventory')
        for entry in declaration['skills']:
            name = entry.get('name', '')
            if not re.fullmatch(r'vectorcraft-[a-z0-9]+(?:-[a-z0-9]+)*', name) or name in names or name in candidates:
                raise ValueError('invalid_candidate_inventory')
            directory = package / 'skills' / name
            path = directory / 'SKILL.md'
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != entry.get('sha256'):
                raise ValueError('candidate_digest_mismatch')
            if not path.read_text().startswith('---\nname: ' + name + '\n'):
                raise ValueError('invalid_candidate_skill')
            files = {p.relative_to(directory).as_posix(): p for p in directory.rglob('*') if p.is_file()}
            references = set(files) - {'SKILL.md', 'agents/openai.yaml'}
            if any(not rel.startswith('references/') or Path(rel).suffix not in {'.md', '.json'} for rel in references):
                raise ValueError('unsupported_candidate_payload')
            if references or 'files' in entry:
                if not isinstance(entry.get('files'), dict) or set(entry['files']) != set(files):
                    raise ValueError('candidate_file_inventory_mismatch')
                if any(hashlib.sha256(path.read_bytes()).hexdigest() != entry['files'][rel] for rel, path in files.items()):
                    raise ValueError('candidate_digest_mismatch')
            candidates.add(name)
    skills = package / "skills"
    if not skills.is_dir() or {path.name for path in skills.iterdir()} != set(names) | candidates:
        raise ValueError("skill_set_mismatch")
    for name in names:
        directory = skills / name
        if not directory.is_dir() or not (directory / "SKILL.md").is_file():
            raise ValueError("skill_set_mismatch")
        if skill_digest(directory) != source["sha256"][name]:
            raise ValueError("skill_digest_mismatch")
    return {"schema": "vectorcraft-portable-package/v1", "skills": len(names), "localCandidateSkills": len(candidates), "rootEntries": sorted(entries)}


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: verify_portable_package.py PACKAGE_ROOT SKILLS_LOCK", file=sys.stderr)
        return 2
    try:
        print(json.dumps(verify(Path(sys.argv[1]), Path(sys.argv[2]))))
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"portable_package_error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
