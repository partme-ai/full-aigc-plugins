#!/usr/bin/env python3
"""Vendor skills from source skill packages into this repository.

The source of truth for skill bodies is the upstream skill package repository
(for example full-aigc-skills/processon-skills). This repository carries a
vendored snapshot plus skills.lock.json so that the main branch is always
complete and installable without network access.

Commands:
  check   Verify the in-tree managed skills match the lockfile digests and,
          unless --offline, that each source ref still resolves to the locked
          commit. Exits 1 on any mismatch.

Released content is imported only through import_skill_release_manifest.py.
This checker intentionally has no update command, so a mutable checkout or
branch cannot bypass the immutable release-manifest gate.

Lockfile schema (version 1):
  {
    "version": 1,
    "sources": [
      {
        "package": "processon-skills",
        "repo": "https://github.com/full-aigc-skills/processon-skills.git",
        "ref": "v1.0.0",
        "sha": "<resolved commit>",
        "skills": ["processon-use", "..."],
        "dest": "skills/",
        "sha256": {"processon-use": "<digest>", "...": "..."}
      }
    ]
  }
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def fail(message: str) -> None:
    print(f"ERROR: {message}")


def hash_skill_dir(skill_dir: Path) -> str:
    """Deterministic digest over every file in a skill directory."""
    digest = hashlib.sha256()
    # 与技能仓 canonical manifest 保持同一口径：
    # 先统一换行（CRLF -> LF），再按相对路径字符串排序，
    # 否则 Windows 检出会得到与 Linux 不同的摘要。
    entries = []
    for path in skill_dir.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"symbolic links are forbidden in skill content: {path}")
        if path.is_dir():
            continue
        if not path.is_file():
            raise ValueError(f"special files are forbidden in skill content: {path}")
        entries.append((path.relative_to(skill_dir).as_posix(), path))
    for relative, path in sorted(entries, key=lambda item: item[0]):
        data = path.read_bytes().replace(b"\r\n", b"\n")
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(data).hexdigest().encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def resolve_ref(repo: str, ref: str) -> str:
    out = subprocess.run(
        # the explicit peel pattern makes annotated tags also list their
        # refs/tags/<ref>^{} line, whose commit sha is what we lock on
        ["git", "ls-remote", repo, ref, f"{ref}^{{}}"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    if not out:
        raise RuntimeError(f"{repo}: ref '{ref}' not found")
    # annotated tags produce two lines (refs/tags/<ref> and its peeled
    # refs/tags/<ref>^{}); the peeled commit sha wins
    sha = None
    for line in out.splitlines():
        candidate, _, name = line.partition("\t")
        short = name.removeprefix("refs/tags/").removeprefix("refs/heads/")
        if short == f"{ref}^{{}}" or short == ref and sha is None:
            sha = candidate
    if sha is None:
        raise RuntimeError(f"{repo}: could not resolve ref '{ref}'")
    return sha


def fetch_checkout(repo: str, ref: str, workdir: Path) -> Path:
    checkout = workdir / "checkout"
    subprocess.run(["git", "init", "--quiet", str(checkout)], check=True)
    subprocess.run(["git", "-C", str(checkout), "remote", "add", "origin", repo], check=True)
    subprocess.run(
        ["git", "-C", str(checkout), "fetch", "--quiet", "--depth", "1", "origin", ref],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(checkout), "checkout", "--quiet", "--detach", "FETCH_HEAD"],
        check=True,
    )
    head = subprocess.run(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    print(f"fetched {repo}@{ref} -> {head}")
    return checkout


def load_lock(path: Path) -> dict:
    lock = json.loads(path.read_text())
    if lock.get("version") != 1:
        raise RuntimeError(f"unsupported lockfile version: {lock.get('version')}")
    return lock


def validate_source(source: dict, root: Path) -> Path:
    for key in ("package", "repo", "ref", "skills", "dest", "sha", "sha256",
                "minimumCliVersion", "minimumCapabilities"):
        if key not in source:
            raise RuntimeError(f"source {source.get('package', '?')}: missing key '{key}'")
    for name in source["skills"]:
        if not SKILL_NAME_RE.match(name):
            raise RuntimeError(f"{source['package']}: illegal skill name '{name}'")
    dest = (root / source["dest"]).resolve()
    if root not in dest.parents and dest != root:
        raise RuntimeError(f"{source['package']}: dest escapes repository root")
    if dest != (root / "skills").resolve():
        raise RuntimeError(f"{source['package']}: managed skills must target skills/")
    if not source["minimumCapabilities"]:
        raise RuntimeError(f"{source['package']}: minimumCapabilities must not be empty")
    if not re.fullmatch(r"\d+\.\d+\.\d+", source["minimumCliVersion"]):
        raise RuntimeError(f"{source['package']}: minimumCliVersion must be semver")
    return dest


def source_checkout(source: dict, overrides: dict, workdir: Path) -> tuple[Path, str]:
    """Return (checkout_path, resolved_sha) for one source."""
    package = source["package"]
    if package in overrides:
        local = Path(overrides[package]).resolve()
        if not local.is_dir():
            raise RuntimeError(f"{package}: --source-path '{local}' is not a directory")
        sha = subprocess.run(
            ["git", "-C", str(local), "rev-parse", "HEAD"],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        print(f"using local override for {package}: {local} @ {sha}")
        return local, sha
    sha = resolve_ref(source["repo"], source["ref"])
    return fetch_checkout(source["repo"], source["ref"], workdir / package), sha


def cmd_check(lock_path: Path, offline: bool, overrides: dict) -> int:
    root = lock_path.parent.resolve()
    lock_path = lock_path.resolve()
    lock = load_lock(lock_path)
    errors = 0
    local_skills = {name for name in lock.get("localSkills", [])}
    upstream_skills = {
        name for source in lock["sources"] for name in source.get("skills", [])
    }
    # 插件本地技能（如入口技能）不来自上游包，
    # 但同名技能不能两边都声明，否则 vendor 与本地会互相覆盖。
    for name in sorted(local_skills & upstream_skills):
        fail(f"skill {name} is declared both locally and by a source package")
        errors += 1
    expected_skills = upstream_skills | local_skills
    actual_skills = {
        path.name for path in (root / "skills").iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    for extra in sorted(actual_skills - expected_skills):
        fail(f"unmanaged skill directory: skills/{extra}")
        errors += 1
    with tempfile.TemporaryDirectory(prefix="skill-vendor-") as tmp:
        for source in lock["sources"]:
            package = source["package"]
            dest = validate_source(source, root)
            locked = source.get("sha256", {})
            for name in source["skills"]:
                target = dest / name
                if not (target / "SKILL.md").is_file():
                    fail(f"{package}: managed skill skills/{name} is missing from the tree")
                    errors += 1
                    continue
                actual = hash_skill_dir(target)
                if actual != locked.get(name):
                    fail(f"{package}: skills/{name} content differs from the lockfile digest")
                    errors += 1
            if offline:
                continue
            try:
                checkout, sha = source_checkout(source, overrides, Path(tmp))
            except (RuntimeError, subprocess.CalledProcessError) as exc:
                fail(f"{package}: {exc}")
                errors += 1
                continue
            if sha != source.get("sha"):
                fail(f"{package}: {source['ref']} moved to {sha[:12]} "
                     f"(locked at {str(source.get('sha'))[:12]}); run update")
                errors += 1
                continue
            for name in source["skills"]:
                src = checkout / "skills" / name
                if not (src / "SKILL.md").is_file():
                    fail(f"{package}: skills/{name} missing upstream")
                    errors += 1
                    continue
                if hash_skill_dir(src) != locked.get(name):
                    fail(f"{package}: skills/{name} upstream content differs from the lockfile")
                    errors += 1
    if errors:
        return 1
    print("skill vendor check: all managed skills match the lockfile" +
          (" (offline)" if offline else ""))
    return 0


def parse_overrides(pairs: list[str]) -> dict:
    overrides = {}
    for pair in pairs or []:
        package, sep, path = pair.partition("=")
        if not sep:
            raise SystemExit(f"--source-path expects PKG=PATH, got '{pair}'")
        overrides[package] = path
    return overrides


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("check",))
    parser.add_argument("--lock", default="skills.lock.json",
                        help="path to the lockfile (default: skills.lock.json)")
    parser.add_argument("--offline", action="store_true",
                        help="check only the in-tree snapshot, skip upstream resolution")
    parser.add_argument("--source-path", action="append", default=[],
                        metavar="PKG=PATH", help="use a local checkout for a source package")
    args = parser.parse_args()
    lock_path = Path(args.lock).resolve()
    if not lock_path.is_file():
        fail(f"lockfile not found: {lock_path}")
        return 1
    overrides = parse_overrides(args.source_path)
    try:
        return cmd_check(lock_path, args.offline, overrides)
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        fail(str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
