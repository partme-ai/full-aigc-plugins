#!/usr/bin/env python3
"""Distribution validator for partme-jianying-plugin."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import host_acceptance

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ID = "jianying-draft"
REPOSITORY = "https://github.com/full-aigc-plugins/jianying-draft-plugin"
LEGAL = ("LICENSE", "NOTICE", "PRIVACY.md", "README.md", "README.en.md",
         "TERMS.md", "THIRD_PARTY_NOTICES.md")
MINIMUM_SKILL_RELEASE_VERSION = (2, 0, 3)
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


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def load_json(rel: str) -> dict:
    try:
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{rel}: invalid JSON ({exc})")
        raise


def find_active_legacy_dependencies(root: Path) -> list[str]:
    """扫描活动文档、脚本和 CI，允许历史说明但拒绝可执行旧依赖。"""
    candidates: list[Path] = []
    for readme_name in ("README.md", "README.en.md"):
        readme = root / readme_name
        if readme.is_file():
            candidates.append(readme)
    for base_name in ("docs", "scripts", "commands", "hooks", ".github/workflows"):
        base = root / base_name
        if not base.is_dir():
            continue
        candidates.extend(path for path in base.rglob("*") if path.is_file())

    findings = []
    ignored = {
        root / "scripts" / "validate_distribution.py",
        root / "scripts" / "validate_plugin_archive.py",
        root / "runtime" / "release-protection-policy.json",
    }
    for path in sorted(set(candidates)):
        if path in ignored or "__pycache__" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in ACTIVE_LEGACY_PATTERNS:
            match = pattern.search(text)
            if match is not None:
                findings.append(
                    f"{path.relative_to(root).as_posix()}: {match.group(0)}"
                )
                break
    return findings


def version_tuple(value: str) -> tuple[int, int, int]:
    if not re.fullmatch(r"\d+\.\d+\.\d+", value):
        raise ValueError(f"invalid semantic version: {value}")
    return tuple(int(part) for part in value.split("."))


def validate_skill_cli_compatibility(skills_lock: dict, cli_lock: dict) -> None:
    """验证技能锁声明不会超过插件锁定的 CLI 基础契约。"""
    cli_minimum = version_tuple(cli_lock.get("minimumVersion", ""))
    required = set(cli_lock.get("requiredCapabilities", []))
    for source in skills_lock.get("sources", []):
        package = source.get("package", "unknown")
        skill_minimum = version_tuple(source.get("minimumCliVersion", ""))
        if cli_minimum < skill_minimum:
            raise ValueError(
                f"{package}: CLI minimum {cli_lock.get('minimumVersion')} is older than "
                f"skill minimum {source.get('minimumCliVersion')}"
            )
        declared = set(source.get("minimumCapabilities", []))
        missing = sorted(required - declared)
        if missing:
            raise ValueError(f"{package}: skill lock misses CLI capabilities: {', '.join(missing)}")


def validate_release_readiness(skills_lock: dict, cli_lock: dict) -> None:
    """验证正式发布所需的三平台 CLI 与不可变技能版本锁。"""
    expected_platforms = {"darwin-arm64", "darwin-x64", "win32-x64"}
    artifacts = cli_lock.get("artifacts", {})
    if set(artifacts) != expected_platforms:
        raise ValueError("release requires exactly three checksum-pinned CLI artifacts")
    if not re.fullmatch(r"[0-9a-f]{40}", cli_lock.get("sourceCommit", "")):
        raise ValueError("release requires the immutable CLI source commit")
    resolved_version = cli_lock.get("resolvedVersion", "")
    release_ref = cli_lock.get("releaseRef", "")
    repository = cli_lock.get("repository", "")
    if (not re.fullmatch(r"\d+\.\d+\.\d+", resolved_version)
            or release_ref != f"v{resolved_version}"
            or repository != "full-aigc-plugins/jianying-draft"):
        raise ValueError("release requires the canonical CLI repository and immutable version ref")
    release_prefix = (
        f"https://github.com/{repository}/releases/download/{release_ref}/"
    )
    for platform, artifact in artifacts.items():
        for key in (
            "url", "archiveSha256", "binarySha256",
            "capabilityManifestSha256", "sbomSha256",
        ):
            value = artifact.get(key, "")
            if key == "url":
                suffix = value.removeprefix(release_prefix) if isinstance(value, str) else ""
                if (not suffix or "/" in suffix or "\\" in suffix
                        or not value.startswith(release_prefix)):
                    raise ValueError(
                        f"{platform}: release artifact URL must belong to canonical repository/ref"
                    )
            elif not re.fullmatch(r"[0-9a-f]{64}", value):
                raise ValueError(f"{platform}: {key} must be a SHA-256 digest")

    sources = skills_lock.get("sources", [])
    if len(sources) != 1:
        raise ValueError("release requires exactly one canonical skill source")
    source = sources[0]
    version = source.get("releaseVersion", "")
    if (source.get("package") != "jianying-skills"
            or source.get("repo") != "https://github.com/full-aigc-skills/jianying-skills.git"
            or not re.fullmatch(r"\d+\.\d+\.\d+", version)
            or source.get("ref") != f"v{version}"
            or source.get("manifestSchema") != "jianying-skills-manifest/v1"
            or not re.fullmatch(r"[0-9a-f]{64}", source.get("manifestSha256", ""))):
        raise ValueError("release requires an immutable jianying-skills manifest lock")
    if version_tuple(version) < MINIMUM_SKILL_RELEASE_VERSION:
        minimum = ".".join(map(str, MINIMUM_SKILL_RELEASE_VERSION))
        raise ValueError(
            f"release requires jianying-skills {minimum} or newer for the Rust Job contract"
        )

    for retired in ("scripts/jydraft_run.py", "scripts/jydraft_check.py", "hooks/env_check.py"):
        if (ROOT / retired).exists():
            raise ValueError(f"release still contains a migration-only Python shim: {retired}")

    active_legacy = find_active_legacy_dependencies(ROOT)
    if active_legacy:
        raise ValueError(
            "release runtime surface retains active legacy dependencies: "
            + "; ".join(active_legacy)
        )


def validate_host_release_policy(
    root: Path,
    plugin_version: str,
    cli_version: str,
    skills_version: str,
) -> None:
    """允许已通过验收，或允许尚未发布版本的精确 pending 占位。"""
    try:
        host_acceptance.validate_acceptance(
            root, plugin_version, cli_version, skills_version,
        )
        return
    except (OSError, ValueError, json.JSONDecodeError):
        pass
    pending = json.loads(
        (root / "runtime/host-acceptance.json").read_text(encoding="utf-8")
    )
    expected = {
        "schema": "jianying-host-release-acceptance/v1",
        "status": "pending",
        "pluginVersion": plugin_version,
        "cliVersion": cli_version,
        "skillsVersion": skills_version,
        "jobSchema": "jianying-job/v2",
        "hosts": [],
    }
    if pending != expected:
        raise ValueError(
            "release requires exact pending host acceptance or a passed host acceptance"
        )


def main(*, release: bool = False) -> int:
    codex = load_json(".codex-plugin/plugin.json")
    zcode = load_json(".zcode-plugin/plugin.json")
    kimi = load_json("kimi.plugin.json")
    root_manifest = load_json("plugin.json")
    market = load_json(".agents/plugins/marketplace.json")

    if codex.get("name") != PLUGIN_ID or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", PLUGIN_ID):
        fail(f"codex manifest name must be '{PLUGIN_ID}'")
    version = codex.get("version", "")
    if not re.match(r"\d+\.\d+\.\d+", version):
        fail(f"version not semver: {version}")
    if codex.get("repository") != REPOSITORY:
        fail("codex manifest repository mismatch")
    base = version.split("+")[0]
    for label, m in (("zcode", zcode), ("kimi", kimi), ("root", root_manifest)):
        if m.get("name") != PLUGIN_ID or m.get("version") not in {version, base}:
            fail(f"{label} manifest name/version must match")
        if m.get("homepage") != REPOSITORY:
            fail(f"{label} manifest homepage must match the plugin repository")
    if root_manifest.get("repository") != REPOSITORY:
        fail("root manifest repository mismatch")
    entry = market["plugins"][0]
    if entry.get("name") != PLUGIN_ID or entry.get("version") not in {version, base}:
        fail("marketplace entry name/version must match")
    if entry.get("source", {}).get("url") != f"{REPOSITORY}.git":
        fail("marketplace source must match the plugin repository")
    for readme_name in ("README.md", "README.en.md"):
        if version not in (ROOT / readme_name).read_text(encoding="utf-8"):
            fail(f"{readme_name} must declare the packaged plugin version {version}")

    for legal in LEGAL:
        if not (ROOT / legal).is_file():
            fail(f"missing legal file: {legal}")

    for runtime_file in (
        "scripts/install_cli_bundle.mjs",
        "scripts/fetch_cli_artifact.mjs",
        "scripts/import_cli_release_index.mjs",
        "scripts/import_skill_release_manifest.py",
        "scripts/verify_skill_dispatch_evidence.py",
        "scripts/verify_github_release_asset.py",
        "scripts/release_readiness.py",
        "scripts/remote_release_preflight.py",
        "scripts/release_publication_plan.py",
        "scripts/validate_plugin_archive.py",
        "scripts/host_acceptance.py",
        "scripts/record_host_acceptance.py",
        "scripts/finalize_host_acceptance.py",
        "scripts/release_install_canary.mjs",
        "scripts/verify_release_evidence.mjs",
        "scripts/harness.mjs",
        "scripts/runtime_adapter.mjs",
        "scripts/quality_feature_gate.mjs",
        "runtime/jianying-cli.lock.json",
        "runtime/feature-flags.json",
        "runtime/host-acceptance.json",
        "schemas/host-observation-v1.schema.json",
        "schemas/host-run-evidence-v1.schema.json",
        "schemas/host-observation-v2.schema.json",
        "schemas/host-run-evidence-v2.schema.json",
        "schemas/host-release-acceptance-v1.schema.json",
        "runtime/harness_contract.json",
        "tests/runtime_adapter.test.mjs",
        "tests/real_cli_archive_fetch.test.mjs",
        "tests/fetch_cli_artifact.test.mjs",
        "tests/test_release_readiness.py",
        "tests/release_evidence.test.mjs",
        ".github/workflows/release-gate.yml",
        ".github/workflows/cli-sync.yml",
        ".github/workflows/skills-sync.yml",
    ):
        if not (ROOT / runtime_file).is_file():
            fail(f"missing Rust runtime adapter artifact: {runtime_file}")

    cli_lock = load_json("runtime/jianying-cli.lock.json")
    if cli_lock.get("jobSchema") != "jianying-job/v2":
        fail("CLI lock must require jianying-job/v2")
    required = set(cli_lock.get("requiredCapabilities", []))
    if not {"capabilities", "schema.job_v2", "job.run"}.issubset(required):
        fail("CLI lock is missing the runtime adapter handshake capabilities")

    harness = load_json("runtime/harness_contract.json")
    if harness.get("schema") != "jianying-plugin-harness/v1":
        fail("shared Harness contract schema is invalid")
    if set(harness.get("riskLevels", {})) != {
            "read_only", "reversible_write", "high_risk_write", "native_external"}:
        fail("shared Harness risk policy is incomplete")
    if harness.get("resultContract", {}).get("stdout") != "single_json_document":
        fail("shared Harness result contract must require one JSON document")

    skills_lock = load_json("skills.lock.json")
    try:
        validate_skill_cli_compatibility(skills_lock, cli_lock)
        if release:
            validate_release_readiness(skills_lock, cli_lock)
            source = skills_lock["sources"][0]
            validate_host_release_policy(
                ROOT,
                base,
                cli_lock["resolvedVersion"],
                source["releaseVersion"],
            )
    except ValueError as exc:
        fail(str(exc))

    for skill_dir in sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir()):
        md = skill_dir / "SKILL.md"
        if not md.is_file():
            fail(f"skills/{skill_dir.name}: directory without SKILL.md")
        text = md.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.+?)\n---\n", text, re.DOTALL)
        if not m:
            fail(f"skills/{skill_dir.name}: missing frontmatter")
        block = m.group(1)
        if re.findall(r"^name: (\S+)$", block, re.MULTILINE) != [skill_dir.name]:
            fail(f"skills/{skill_dir.name}: frontmatter name must equal directory name")
        if len(re.findall(r"^description: ", block, re.MULTILINE)) != 1:
            fail(f"skills/{skill_dir.name}: exactly one description key required")

    # 已切换的宿主入口不得再调用迁移期 Python/fork 路径。
    forbidden_runtime = (
        "python3", "pyJianYingDraft", "jydraft_", "JIANYING_HEADLESS_ROOT", "headless_draft.py",
    )
    for path in [*(ROOT / "commands").glob("*.md"), ROOT / "hooks/hooks.json"]:
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden_runtime:
            if pattern in text:
                fail(f"{path.relative_to(ROOT)} retains legacy runtime entry {pattern}")
    hook_command = load_json("hooks/hooks.json")["hooks"]["SessionStart"][0]["hooks"][0]["command"]
    if "scripts/harness.mjs" not in hook_command or not hook_command.startswith("node "):
        fail("SessionStart must call the shared Node Harness")

    for rel in (".codex-plugin/plugin.json", ".zcode-plugin/plugin.json",
                "kimi.plugin.json", "plugin.json", ".agents/plugins/marketplace.json"):
        text = (ROOT / rel).read_text(encoding="utf-8")
        if "Rust" not in text:
            fail(f"{rel} must describe the Rust Runtime Adapter")
        for pattern in ("pyJianYingDraft", "jycut", "fork pro-tier"):
            if pattern in text:
                fail(f"{rel} retains legacy runtime description {pattern}")

    # 旧制品在迁移删除前若仍存在，继续校验其内容未漂移；它们不再是入口或就绪条件。
    stale = []
    skip_dirs = {".git", "node_modules", ".venv", "__pycache__", "jy_headless", "target"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or skip_dirs.intersection(path.parts):
            continue
        if path.name in {
                "validate_distribution.py", "release_readiness.py",
                "validate_plugin_archive.py",
                "test_distribution.py", "test_release_readiness.py", "AGENTS.md"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pattern in ("scripts/jy_headless", "scripts/VENDOR.json", "vendor_engine"):
            if pattern in text:
                stale.append(f"{path.relative_to(ROOT)}: {pattern}")
                break
    if stale:
        fail("stale vendored-engine references: " + "; ".join(sorted(set(stale))))

    active_legacy_dependencies = find_active_legacy_dependencies(ROOT)
    if active_legacy_dependencies:
        fail(
            "active legacy runtime dependencies: "
            + "; ".join(active_legacy_dependencies)
        )

    # 分发包不得重新引入任何可执行的旧引擎或源码快照。来源与许可证证据保留在
    # THIRD_PARTY_NOTICES 和 OpenSpec 基线中，不通过携带失活代码来保存历史。
    retired_runtime_paths = (
        "scripts/vendor/pyJianYingDraft",
        "scripts/vendor/jianying-cli",
        "scripts/VENDOR.json",
        "scripts/vendor_engine.py",
        "scripts/jy_headless",
    )
    for rel in retired_runtime_paths:
        if (ROOT / rel).exists():
            fail(f"retired runtime artifact must not ship: {rel}")

    if "SessionStart" not in load_json("hooks/hooks.json").get("hooks", {}):
        fail("hooks.json missing SessionStart")

    skill_count = len([path for path in (ROOT / "skills").iterdir() if path.is_dir()])
    print(f"validated {PLUGIN_ID} {version}: "
          f"{skill_count} skills, Rust Runtime Adapter entries wired")
    return 0


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        "--release", action="store_true",
        help="also require immutable skills and all three CLI release artifacts",
    )
    sys.exit(main(release=argument_parser.parse_args().release))
