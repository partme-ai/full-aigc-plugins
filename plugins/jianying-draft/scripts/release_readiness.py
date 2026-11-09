#!/usr/bin/env python3
"""输出剪映插件正式发布门禁的完整结构化报告。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import host_acceptance
import validate_distribution as distribution

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PLATFORMS = {"darwin-arm64", "darwin-x64", "win32-x64"}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
MINIMUM_SKILL_RELEASE_VERSION = (2, 0, 3)


def result(identifier: str, ready: bool, evidence: object) -> dict:
    """构造稳定的单项门禁结果。"""
    return {"id": identifier, "status": "ready" if ready else "blocked", "evidence": evidence}


def hash_skill_dir(skill_dir: Path) -> str:
    """计算与技能发布清单一致的目录摘要。"""
    digest = hashlib.sha256()
    entries = []
    for path in skill_dir.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"symbolic links are forbidden in skill content: {path}")
        if path.is_dir():
            continue
        entries.append((path.relative_to(skill_dir).as_posix(), path))
    for relative, path in sorted(entries, key=lambda item: item[0]):
        data = path.read_bytes().replace(b"\r\n", b"\n")
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(data).hexdigest().encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def build_report(root: Path = ROOT) -> dict:
    """一次性检查版本、制品、技能、许可证和旧运行路径。"""
    cli_lock = json.loads((root / "runtime/jianying-cli.lock.json").read_text(encoding="utf-8"))
    skills_lock = json.loads((root / "skills.lock.json").read_text(encoding="utf-8"))
    codex = json.loads((root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    zcode = json.loads((root / ".zcode-plugin/plugin.json").read_text(encoding="utf-8"))
    kimi = json.loads((root / "kimi.plugin.json").read_text(encoding="utf-8"))
    market = json.loads((root / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    checks = []

    plugin_version = codex.get("version", "")
    base_version = plugin_version.split("+")[0]
    observed_versions = {
        "codex": plugin_version,
        "zcode": zcode.get("version"),
        "kimi": kimi.get("version"),
        "marketplace": market.get("plugins", [{}])[0].get("version"),
    }
    versions_ready = SEMVER.fullmatch(base_version) is not None and all(
        value in {plugin_version, base_version} for value in observed_versions.values()
    )
    checks.append(result("plugin.version_matrix", versions_ready, observed_versions))

    artifacts = cli_lock.get("artifacts", {})
    checks.append(result(
        "cli.platform_artifacts",
        set(artifacts) == EXPECTED_PLATFORMS,
        {"expected": sorted(EXPECTED_PLATFORMS), "observed": sorted(artifacts)},
    ))
    resolved = cli_lock.get("resolvedVersion")
    release_ref = cli_lock.get("releaseRef")
    cli_identity_ready = (
        isinstance(resolved, str)
        and SEMVER.fullmatch(resolved) is not None
        and release_ref == f"v{resolved}"
        and cli_lock.get("repository") == "full-aigc-plugins/jianying-draft"
        and COMMIT.fullmatch(cli_lock.get("sourceCommit") or "") is not None
    )
    checks.append(result("cli.immutable_identity", cli_identity_ready, {
        "version": resolved,
        "release_ref": release_ref,
        "repository": cli_lock.get("repository"),
        "source_commit": cli_lock.get("sourceCommit"),
    }))

    artifact_errors = []
    if set(artifacts) == EXPECTED_PLATFORMS and cli_identity_ready:
        prefix = (
            "https://github.com/full-aigc-plugins/jianying-draft/releases/download/"
            f"{release_ref}/"
        )
        for platform, artifact in sorted(artifacts.items()):
            url = artifact.get("url", "")
            suffix = url.removeprefix(prefix) if isinstance(url, str) else ""
            if not suffix or "/" in suffix or "\\" in suffix or not url.startswith(prefix):
                artifact_errors.append(f"{platform}: noncanonical URL")
            for key in (
                "archiveSha256", "binarySha256", "capabilityManifestSha256", "sbomSha256"
            ):
                if SHA256.fullmatch(artifact.get(key, "")) is None:
                    artifact_errors.append(f"{platform}: invalid {key}")
    else:
        artifact_errors.append("platform artifacts or immutable CLI identity are incomplete")
    checks.append(result("cli.artifact_integrity", not artifact_errors, artifact_errors))

    sources = skills_lock.get("sources", [])
    source = sources[0] if len(sources) == 1 else {}
    skill_version = source.get("releaseVersion")
    skill_version_tuple = (
        tuple(int(part) for part in skill_version.split("."))
        if isinstance(skill_version, str) and SEMVER.fullmatch(skill_version)
        else None
    )
    skill_release_ready = (
        len(sources) == 1
        and source.get("package") == "jianying-skills"
        and source.get("repo") == "https://github.com/full-aigc-skills/jianying-skills.git"
        and isinstance(skill_version, str)
        and SEMVER.fullmatch(skill_version) is not None
        and skill_version_tuple >= MINIMUM_SKILL_RELEASE_VERSION
        and source.get("ref") == f"v{skill_version}"
        and COMMIT.fullmatch(source.get("sha") or "") is not None
        and source.get("manifestSchema") == "jianying-skills-manifest/v1"
        and SHA256.fullmatch(source.get("manifestSha256") or "") is not None
    )
    checks.append(result("skills.immutable_release", skill_release_ready, {
        "version": skill_version,
        "ref": source.get("ref"),
        "commit": source.get("sha"),
        "manifest_sha256": source.get("manifestSha256"),
        "minimum_version": ".".join(map(str, MINIMUM_SKILL_RELEASE_VERSION)),
    }))

    skill_errors = []
    names = source.get("skills", [])
    digests = source.get("sha256", {})
    for name in names:
        directory = root / "skills" / name
        if not (directory / "SKILL.md").is_file():
            skill_errors.append(f"{name}: missing")
        elif hash_skill_dir(directory) != digests.get(name):
            skill_errors.append(f"{name}: digest mismatch")
    actual_names = sorted(
        path.name for path in (root / "skills").iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )
    # 插件本地技能（入口技能）不受上游包摘要约束，但必须被显式声明。
    local_names = sorted(skills_lock.get("localSkills", []))
    if sorted(names + local_names) != actual_names:
        skill_errors.append("skill set differs from lock")
    checks.append(result("skills.content_digests", not skill_errors, skill_errors))

    host_evidence: object
    host_acceptance_ready = False
    host_release_policy_ready = False
    try:
        host_evidence = host_acceptance.validate_acceptance(
            root,
            base_version,
            resolved if isinstance(resolved, str) else "",
            skill_version if isinstance(skill_version, str) else "",
        )
        host_acceptance_ready = True
        host_release_policy_ready = True
    except (OSError, ValueError, json.JSONDecodeError) as error:
        acceptance_path = root / "runtime/host-acceptance.json"
        try:
            pending = json.loads(acceptance_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            pending = None
        host_release_policy_ready = (
            isinstance(pending, dict)
            and pending.get("schema") == "jianying-host-release-acceptance/v1"
            and pending.get("status") == "pending"
            and pending.get("pluginVersion") == base_version
            and pending.get("cliVersion") == resolved
            and pending.get("skillsVersion") == skill_version
            and pending.get("jobSchema") == "jianying-job/v2"
            and pending.get("hosts") == []
        )
        host_evidence = {
            "acceptance_state": "pending" if host_release_policy_ready else "invalid",
            "production_ready": False,
            "reason": str(error),
        }
    checks.append(result(
        "hosts.release_acceptance",
        host_release_policy_ready,
        host_evidence,
    ))

    compatibility_error = None
    try:
        distribution.validate_skill_cli_compatibility(skills_lock, cli_lock)
    except ValueError as error:
        compatibility_error = str(error)
    checks.append(result(
        "matrix.cli_skill_compatibility",
        compatibility_error is None,
        compatibility_error or {
            "cli_minimum": cli_lock.get("minimumVersion"),
            "skill_minimum": source.get("minimumCliVersion"),
            "required_capabilities": cli_lock.get("requiredCapabilities", []),
        },
    ))

    missing_legal = [name for name in distribution.LEGAL if not (root / name).is_file()]
    checks.append(result("distribution.legal_materials", not missing_legal, missing_legal))

    retired = [
        path for path in (
            "scripts/jydraft_run.py", "scripts/jydraft_check.py", "hooks/env_check.py",
            "scripts/vendor/pyJianYingDraft", "scripts/vendor/jianying-cli", "scripts/jy_headless",
        ) if (root / path).exists()
    ]
    checks.append(result("runtime.legacy_engines_removed", not retired, retired))

    legacy_surfaces = distribution.find_active_legacy_dependencies(root)
    checks.append(result(
        "runtime.release_surface_rust_only",
        not legacy_surfaces,
        sorted(set(legacy_surfaces)),
    ))

    blocked = [check["id"] for check in checks if check["status"] == "blocked"]
    return {
        "schema": "jianying-plugin-release-readiness/v1",
        "ready": not blocked,
        "production_ready": not blocked and host_acceptance_ready,
        "plugin_version": plugin_version,
        "checks": checks,
        "blocked": blocked,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    report = build_report()
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if arguments.output:
        arguments.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if report["ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
