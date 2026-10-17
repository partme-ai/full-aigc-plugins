#!/usr/bin/env python3
"""Check the current portable plugin payload against its locked skill source."""

import hashlib
import json
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
    if {path.name for path in package.iterdir()} != ROOT_ENTRIES:
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
    skills = package / "skills"
    if not skills.is_dir() or {path.name for path in skills.iterdir()} != set(names):
        raise ValueError("skill_set_mismatch")
    for name in names:
        directory = skills / name
        if not directory.is_dir() or not (directory / "SKILL.md").is_file():
            raise ValueError("skill_set_mismatch")
        if skill_digest(directory) != source["sha256"][name]:
            raise ValueError("skill_digest_mismatch")
    return {"schema": "vectorcraft-portable-package/v1", "skills": len(names), "rootEntries": sorted(ROOT_ENTRIES)}


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
