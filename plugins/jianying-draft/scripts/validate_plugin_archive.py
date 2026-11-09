#!/usr/bin/env python3
"""Validate the exact plugin source archive without extracting or executing it."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tarfile
import zipfile
from pathlib import Path, PurePosixPath

REQUIRED_FILES = {
    ".agents/plugins/marketplace.json",
    ".codex-plugin/plugin.json",
    ".zcode-plugin/plugin.json",
    "kimi.plugin.json",
    "skills.lock.json",
    "runtime/jianying-cli.lock.json",
    "runtime/harness_contract.json",
    "runtime/feature-flags.json",
    "hooks/hooks.json",
    "scripts/harness.mjs",
    "scripts/runtime_adapter.mjs",
    "scripts/quality_feature_gate.mjs",
    "LICENSE",
    "NOTICE",
    "PRIVACY.md",
    "TERMS.md",
    "THIRD_PARTY_NOTICES.md",
    "README.md",
    "README.zh-CN.md",
}
RETIRED_RUNTIME_PREFIXES = (
    "scripts/jydraft_run.py",
    "scripts/jydraft_check.py",
    "hooks/env_check.py",
    "scripts/vendor/pyJianYingDraft",
    "scripts/vendor/jianying-cli",
    "scripts/VENDOR.json",
    "scripts/vendor_engine.py",
    "scripts/jy_headless",
)
ACTIVE_SURFACE_PREFIXES = (
    "README.md",
    "README.zh-CN.md",
    "docs/",
    "scripts/",
    "commands/",
    "hooks/",
    ".github/workflows/",
)
AUDIT_EXCLUSIONS = {
    "scripts/validate_distribution.py",
    "scripts/validate_plugin_archive.py",
}
ACTIVE_LEGACY_PATTERNS = (
    re.compile(
        r"\bpython(?:3(?:\.\d+)?)?\s+(?:\./)?(?:scripts/)?"
        r"(?:jydraft_run|jydraft_check|vendor_engine|headless_draft)\.py\b"
    ),
    re.compile(
        r"\bpython(?:3(?:\.\d+)?)?\s+[^\n]*scripts/vendor/pyJianYingDraft(?:/|\b)"
    ),
    re.compile(r"\b(?:export\s+)?JIANYING_HEADLESS_ROOT\s*="),
    re.compile(
        r"(?:repository:\s*|\bgit\s+clone[^\n]*)"
        r"(?:https://github\.com/)?(?:partme-ai/)?jianying-headless(?:\.git)?\b"
    ),
    re.compile(r"\b(?:node|cargo\s+run)[^\n]*scripts/vendor/jianying-cli(?:/|\b)"),
)
MAX_MEMBERS = 10_000
MAX_FILE_BYTES = 16 * 1024 * 1024
MAX_TOTAL_BYTES = 256 * 1024 * 1024
COMMIT = re.compile(r"[0-9a-f]{40}")


class ArchiveValidationError(ValueError):
    """The candidate archive violates the plugin distribution contract."""


def _safe_parts(name: str) -> tuple[str, ...]:
    if not name or "\\" in name or name.startswith("/") or "//" in name:
        raise ArchiveValidationError(f"unsafe archive member path: {name!r}")
    path = PurePosixPath(name)
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ArchiveValidationError(f"unsafe archive member path: {name!r}")
    return path.parts


def _normalise_members(raw_members: list[tuple[str, bytes | None, str]]) -> dict[str, bytes]:
    if len(raw_members) > MAX_MEMBERS:
        raise ArchiveValidationError(
            f"archive contains too many members: {len(raw_members)} > {MAX_MEMBERS}"
        )
    roots: set[str] = set()
    files: dict[str, bytes] = {}
    total_bytes = 0
    for name, content, kind in raw_members:
        parts = _safe_parts(name.rstrip("/"))
        roots.add(parts[0])
        if kind == "directory":
            continue
        if kind != "file":
            raise ArchiveValidationError(
                f"archive member must be a regular file or directory: {name} ({kind})"
            )
        if len(parts) < 2:
            raise ArchiveValidationError("archive files must be contained by one root directory")
        relative = PurePosixPath(*parts[1:]).as_posix()
        if relative in files:
            raise ArchiveValidationError(f"duplicate archive member: {relative}")
        payload = content or b""
        if len(payload) > MAX_FILE_BYTES:
            raise ArchiveValidationError(
                f"archive member exceeds size limit: {relative}"
            )
        total_bytes += len(payload)
        if total_bytes > MAX_TOTAL_BYTES:
            raise ArchiveValidationError("archive exceeds total uncompressed size limit")
        files[relative] = payload
    if len(roots) != 1:
        raise ArchiveValidationError("archive must contain exactly one root directory")
    return files


def _read_tar(path: Path) -> dict[str, bytes]:
    members: list[tuple[str, bytes | None, str]] = []
    with tarfile.open(path, mode="r:*") as archive:
        archive_members = archive.getmembers()
        if len(archive_members) > MAX_MEMBERS:
            raise ArchiveValidationError(
                f"archive contains too many members: {len(archive_members)} > {MAX_MEMBERS}"
            )
        if sum(member.size for member in archive_members if member.isfile()) > MAX_TOTAL_BYTES:
            raise ArchiveValidationError("archive exceeds total uncompressed size limit")
        for member in archive_members:
            if member.isdir():
                members.append((member.name, None, "directory"))
            elif member.isfile():
                if member.size > MAX_FILE_BYTES:
                    raise ArchiveValidationError(
                        f"archive member exceeds size limit: {member.name}"
                    )
                source = archive.extractfile(member)
                if source is None:
                    raise ArchiveValidationError(f"cannot read archive member: {member.name}")
                members.append((member.name, source.read(), "file"))
            else:
                members.append((member.name, None, "link_or_special"))
    return _normalise_members(members)


def _read_zip(path: Path) -> dict[str, bytes]:
    members: list[tuple[str, bytes | None, str]] = []
    with zipfile.ZipFile(path) as archive:
        archive_members = archive.infolist()
        if len(archive_members) > MAX_MEMBERS:
            raise ArchiveValidationError(
                f"archive contains too many members: {len(archive_members)} > {MAX_MEMBERS}"
            )
        if sum(member.file_size for member in archive_members) > MAX_TOTAL_BYTES:
            raise ArchiveValidationError("archive exceeds total uncompressed size limit")
        for member in archive_members:
            unix_type = (member.external_attr >> 16) & 0o170000
            if member.is_dir():
                members.append((member.filename, None, "directory"))
            elif unix_type not in {0, 0o100000}:
                members.append((member.filename, None, "link_or_special"))
            else:
                if member.file_size > MAX_FILE_BYTES:
                    raise ArchiveValidationError(
                        f"archive member exceeds size limit: {member.filename}"
                    )
                members.append((member.filename, archive.read(member), "file"))
    return _normalise_members(members)


def _is_active_surface(relative: str) -> bool:
    return relative in ACTIVE_SURFACE_PREFIXES or any(
        prefix.endswith("/") and relative.startswith(prefix)
        for prefix in ACTIVE_SURFACE_PREFIXES
    )


def sha256(path: Path) -> str:
    """Return the SHA-256 digest of the exact archive bytes."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_archive(path: Path, source_commit: str) -> dict[str, object]:
    """Validate archive structure and the shipped Rust-only runtime surface."""
    if not path.is_file():
        raise ArchiveValidationError(f"archive does not exist: {path}")
    if COMMIT.fullmatch(source_commit) is None:
        raise ArchiveValidationError("plugin source commit must be a full Git SHA")
    try:
        files = _read_zip(path) if zipfile.is_zipfile(path) else _read_tar(path)
    except (tarfile.TarError, zipfile.BadZipFile, OSError) as exc:
        raise ArchiveValidationError(f"invalid plugin archive: {exc}") from exc

    missing = sorted(REQUIRED_FILES - files.keys())
    if missing:
        raise ArchiveValidationError(
            "archive misses required plugin files: " + ", ".join(missing)
        )

    retired = sorted(
        relative for relative in files
        if any(
            relative == prefix or relative.startswith(f"{prefix}/")
            for prefix in RETIRED_RUNTIME_PREFIXES
        )
    )
    if retired:
        raise ArchiveValidationError(
            "archive contains retired runtime artifacts: " + ", ".join(retired)
        )

    generated = sorted(
        relative for relative in files
        if "__pycache__" in PurePosixPath(relative).parts
        or relative.endswith((".pyc", ".pyo"))
    )
    if generated:
        raise ArchiveValidationError(
            "archive contains generated Python cache files: " + ", ".join(generated)
        )

    findings: list[str] = []
    for relative, payload in sorted(files.items()):
        if relative in AUDIT_EXCLUSIONS or not _is_active_surface(relative):
            continue
        text = payload.decode("utf-8", errors="ignore")
        for pattern in ACTIVE_LEGACY_PATTERNS:
            match = pattern.search(text)
            if match is not None:
                findings.append(f"{relative}: {match.group(0)}")
                break
    if findings:
        raise ArchiveValidationError(
            "archive contains active legacy runtime dependencies: " + "; ".join(findings)
        )

    skill_files = sorted(
        relative for relative in files
        if re.fullmatch(r"skills/[^/]+/SKILL\.md", relative)
    )
    try:
        skills_lock = json.loads(files["skills.lock.json"])
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ArchiveValidationError(f"archive skills lock is invalid: {exc}") from exc
    sources = skills_lock.get("sources")
    if not isinstance(sources, list) or len(sources) != 1:
        raise ArchiveValidationError("archive skills lock must contain exactly one source")
    # 归档里的技能 = 上游 vendored + 插件本地（入口技能）。
    locked_skills = list(sources[0].get("skills") or []) + list(skills_lock.get("localSkills") or [])
    if (not isinstance(locked_skills, list) or not locked_skills
            or any(not isinstance(name, str) or re.fullmatch(r"[a-z0-9-]+", name) is None for name in locked_skills)
            or len(set(locked_skills)) != len(locked_skills)):
        raise ArchiveValidationError("archive skills lock contains an invalid skill set")
    expected_skill_files = sorted(f"skills/{name}/SKILL.md" for name in locked_skills)
    if skill_files != expected_skill_files:
        raise ArchiveValidationError(
            "archive skill entrypoints must exactly match skills.lock.json: "
            f"expected {expected_skill_files}, found {skill_files}"
        )

    try:
        plugin_manifest = json.loads(files[".codex-plugin/plugin.json"])
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ArchiveValidationError(f"archive plugin manifest is invalid: {exc}") from exc
    plugin_version = plugin_manifest.get("version")
    if (plugin_manifest.get("name") != "jianying-draft"
            or not isinstance(plugin_version, str)
            or re.fullmatch(r"\d+\.\d+\.\d+(?:\+[0-9A-Za-z.-]+)?", plugin_version) is None):
        raise ArchiveValidationError("archive plugin identity is invalid")

    return {
        "schema": "jianying-plugin-archive-audit/v1",
        "status": "passed",
        "archive": path.name,
        "archiveSha256": sha256(path),
        "pluginVersion": plugin_version,
        "pluginSourceCommit": source_commit,
        "fileCount": len(files),
        "skillCount": len(skill_files),
        "rustOnlyRuntime": True,
        "externalHeadlessRuntime": False,
        "pythonDraftEngine": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = validate_archive(args.archive, args.source_commit)
    except ArchiveValidationError as exc:
        result = {
            "schema": "jianying-plugin-archive-audit/v1",
            "status": "failed",
            "archive": args.archive.name,
            "error": str(exc),
        }
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False), file=sys.stderr)
        return 1
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
