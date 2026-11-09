#!/usr/bin/env python3
"""从不可变 jianying-skills 发布清单原子更新插件技能锁和 vendored 技能。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

MANIFEST_SCHEMA = "jianying-skills-manifest/v1"
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
CANONICAL_REPOSITORY = "https://github.com/full-aigc-skills/jianying-skills.git"
MINIMUM_RELEASE_VERSION = (2, 0, 3)


def hash_skill_dir(skill_dir: Path) -> str:
    """使用与技能仓 canonical manifest 相同的目录摘要算法。"""
    if skill_dir.is_symlink() or not skill_dir.is_dir():
        raise ValueError(f"skill directory is invalid or symbolic: {skill_dir}")
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


def aggregate_digest(entries: list[dict]) -> str:
    """计算清单声明的有序技能集合摘要。"""
    digest = hashlib.sha256()
    for entry in entries:
        digest.update(entry["name"].encode("utf-8"))
        digest.update(b"\0")
        digest.update(entry["sha256"].encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def git_head(source_root: Path) -> str:
    """读取待同步 checkout 的实际提交。"""
    return subprocess.run(
        ["git", "-C", str(source_root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def resolve_remote_ref(repo: str, release_ref: str) -> str:
    """解析远端不可变 tag；annotated tag 优先使用 peeled commit。"""
    output = subprocess.run(
        ["git", "ls-remote", "--tags", repo,
         f"refs/tags/{release_ref}", f"refs/tags/{release_ref}^{{}}"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    resolved = None
    for line in output.splitlines():
        commit, _, name = line.partition("\t")
        if name == f"refs/tags/{release_ref}^{{}}" or name == f"refs/tags/{release_ref}" and resolved is None:
            resolved = commit
    if resolved is None:
        raise ValueError(f"release ref is missing from remote: {release_ref}")
    return resolved


def validate_release_manifest(
    manifest: dict,
    source_root: Path,
    observed_commit: str,
    resolved_commit: str,
) -> dict:
    """校验发布状态、tag/commit、完整技能集合和逐目录摘要。"""
    if manifest.get("schema") != MANIFEST_SCHEMA:
        raise ValueError("unsupported skill manifest schema")
    if manifest.get("package") != "jianying-skills":
        raise ValueError("skill manifest package must be jianying-skills")
    if manifest.get("repository") != CANONICAL_REPOSITORY:
        raise ValueError("skill manifest repository is not canonical")
    version = manifest.get("version", "")
    if not VERSION_PATTERN.fullmatch(version):
        raise ValueError("skill manifest version must be semver")
    if tuple(int(part) for part in version.split(".")) < MINIMUM_RELEASE_VERSION:
        minimum = ".".join(map(str, MINIMUM_RELEASE_VERSION))
        raise ValueError(f"skill release {version} predates required contract fix {minimum}")
    release_ref = manifest.get("release_ref")
    if manifest.get("content_state") != "released" or release_ref != f"v{version}":
        raise ValueError("skill manifest is not an immutable released version")
    source_commit = manifest.get("source_commit", "")
    if not COMMIT_PATTERN.fullmatch(source_commit):
        raise ValueError("skill manifest source_commit is invalid")
    if observed_commit != source_commit or resolved_commit != source_commit:
        raise ValueError("skill checkout, remote release ref, and manifest commit differ")

    entries = manifest.get("skills")
    if not isinstance(entries, list) or not entries:
        raise ValueError("skill manifest has no skills")
    names = [entry.get("name") for entry in entries]
    if len(names) != len(set(names)) or any(not isinstance(name, str) for name in names):
        raise ValueError("skill manifest contains invalid or duplicate skill names")
    actual_names = sorted(
        path.name for path in (source_root / "skills").iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )
    if sorted(names) != actual_names:
        raise ValueError("skill manifest does not cover the complete source skill set")

    minimum_versions = []
    global_capabilities = set(manifest.get("minimum_cli_capabilities", []))
    if not global_capabilities:
        raise ValueError("skill manifest has no minimum CLI capabilities")
    install_capabilities = set(
        manifest.get("install_cli_capabilities", manifest.get("minimum_cli_capabilities", []))
    )
    if not install_capabilities or not install_capabilities.issubset(global_capabilities):
        raise ValueError("skill manifest install capabilities must be a non-empty aggregate subset")
    for entry in entries:
        name = entry["name"]
        digest = entry.get("sha256", "")
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"{name}: invalid skill digest")
        if hash_skill_dir(source_root / "skills" / name) != digest:
            raise ValueError(f"{name}: source content differs from release manifest")
        minimum = entry.get("minimum_cli_version", "")
        if not VERSION_PATTERN.fullmatch(minimum):
            raise ValueError(f"{name}: minimum CLI version is invalid")
        minimum_versions.append(tuple(int(part) for part in minimum.split(".")))
        if not set(entry.get("required_capabilities", [])).issubset(global_capabilities):
            raise ValueError(f"{name}: required capabilities exceed the manifest aggregate")
    if aggregate_digest(entries) != manifest.get("content_sha256"):
        raise ValueError("skill manifest aggregate digest differs from its entries")
    return {
        "version": version,
        "release_ref": release_ref,
        "source_commit": source_commit,
        "skill_names": names,
        "skill_digests": {entry["name"]: entry["sha256"] for entry in entries},
        "minimum_cli_version": ".".join(map(str, max(minimum_versions))),
        "minimum_capabilities": sorted(install_capabilities),
    }


def sync_release(
    lock_path: Path,
    manifest_path: Path,
    source_root: Path,
    *,
    observed_commit: str | None = None,
    resolved_commit: str | None = None,
) -> dict:
    """验证发布清单后原子替换技能目录和锁文件。"""
    lock_path = lock_path.resolve()
    plugin_root = lock_path.parent
    source_root = source_root.resolve()
    manifest_path = manifest_path.resolve()
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    if lock.get("version") != 1 or len(lock.get("sources", [])) != 1:
        raise ValueError("unsupported skills.lock.json shape")
    source = lock["sources"][0]
    if (source.get("package") != "jianying-skills"
            or source.get("repo") != CANONICAL_REPOSITORY):
        raise ValueError("skill lock must use the canonical jianying-skills repository")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    observed_commit = observed_commit or git_head(source_root)
    resolved_commit = resolved_commit or resolve_remote_ref(source["repo"], manifest.get("release_ref", ""))
    release = validate_release_manifest(
        manifest, source_root, observed_commit, resolved_commit
    )

    acceptance_path = plugin_root / "runtime" / "host-acceptance.json"
    if not acceptance_path.is_file():
        raise ValueError("skill release import requires runtime/host-acceptance.json")
    acceptance = json.loads(acceptance_path.read_text(encoding="utf-8"))
    if acceptance.get("schema") != "jianying-host-release-acceptance/v1":
        raise ValueError("unsupported host acceptance schema")
    reset_acceptance = {
        **acceptance,
        "status": "pending",
        "skillsVersion": release["version"],
        "hosts": [],
    }

    updated_source = {
        **source,
        "ref": release["release_ref"],
        "sha": release["source_commit"],
        "releaseVersion": release["version"],
        "manifestSchema": manifest["schema"],
        "manifestSha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        "skills": release["skill_names"],
        "sha256": release["skill_digests"],
        "minimumCliVersion": release["minimum_cli_version"],
        "minimumCapabilities": release["minimum_capabilities"],
    }
    updated_lock = {**lock, "sources": [updated_source]}

    with tempfile.TemporaryDirectory(prefix="jianying-skill-import-", dir=plugin_root) as temporary:
        temporary_root = Path(temporary)
        staged_skills = temporary_root / "skills"
        staged_skills.mkdir()
        for name in release["skill_names"]:
            shutil.copytree(source_root / "skills" / name, staged_skills / name)
        # 插件本地技能（入口技能）不在上游包里，
        # 交换目录时必须一并带过去，否则导入会把它删掉。
        local_skills = list(lock.get("localSkills", []))
        for name in local_skills:
            origin = plugin_root / "skills" / name
            if not (origin / "SKILL.md").is_file():
                raise ValueError(f"declared local skill is missing: skills/{name}")
            shutil.copytree(origin, staged_skills / name)
        staged_lock = temporary_root / "skills.lock.json"
        staged_lock.write_text(
            json.dumps(updated_lock, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        staged_acceptance = temporary_root / "host-acceptance.json"
        staged_acceptance.write_text(
            json.dumps(reset_acceptance, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        destination = plugin_root / source.get("dest", "skills/")
        destination = destination.resolve()
        if destination != (plugin_root / "skills").resolve():
            raise ValueError("skill destination must be the plugin skills directory")
        backup = plugin_root / f".skills-backup-{os.getpid()}"
        if backup.exists():
            raise ValueError(f"skill backup already exists: {backup}")
        destination.rename(backup)
        try:
            staged_skills.rename(destination)
            # 先失效宿主证据，再激活新技能锁；中断时最多保持 fail-closed 的 pending 状态。
            os.replace(staged_acceptance, acceptance_path)
            os.replace(staged_lock, lock_path)
        except Exception:
            if destination.exists():
                shutil.rmtree(destination)
            backup.rename(destination)
            raise
        shutil.rmtree(backup)
    return {
        "version": release["version"],
        "ref": release["release_ref"],
        "commit": release["source_commit"],
        "skills": len(release["skill_names"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lock", type=Path, default=Path("skills.lock.json"))
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        result = sync_release(arguments.lock, arguments.manifest, arguments.source_root)
    except (OSError, ValueError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}")
        return 1
    print(json.dumps({"ok": True, "data": result}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
