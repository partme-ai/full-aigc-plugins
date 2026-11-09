#!/usr/bin/env python3
"""只读检查剪映三仓正式发布链的 GitHub 前置条件。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI_REPOSITORY = "full-aigc-plugins/jianying-draft"
SKILLS_REPOSITORY = "full-aigc-skills/jianying-skills"
PLUGIN_REPOSITORY = "full-aigc-plugins/jianying-draft-plugin"
SHA256_DIGEST = re.compile(r"sha256:[0-9a-f]{64}")
EQUIVALENT_POLICY_SCHEMA = "jianying-release-protection-policy/v1"
EQUIVALENT_POLICY_MODE = "immutable_release_with_tag_commit_rechecks"
REPORT_SCHEMA = "jianying-remote-release-preflight/v2"
EQUIVALENT_REQUIRED_CHECKS = {
    "immutableReleasesEnabled",
    "beforeDraftTagCommit",
    "beforePublishTagCommit",
    "afterPublishTagCommit",
    "publishedReleaseImmutable",
}


class RemoteQueryError(RuntimeError):
    """远端只读查询失败。"""


def expected_release_assets(name: str, version: str) -> list[str]:
    """返回三个正典 Release 必须精确携带的资产名称。"""
    if name == "cli":
        archives = [
            f"jianying-cli-{version}-darwin-arm64.tar.gz",
            f"jianying-cli-{version}-darwin-x64.tar.gz",
            f"jianying-cli-{version}-win32-x64.zip",
        ]
        return sorted([
            "jianying-cli-release-index.json",
            *archives,
            *(f"{archive}.sha256" for archive in archives),
            *(f"jianying-cli-{version}-{platform}.release-entry.json" for platform in (
                "darwin-arm64", "darwin-x64", "win32-x64",
            )),
        ])
    if name == "skills":
        return ["jianying-skills.manifest.json"]
    if name == "plugin":
        return sorted([
            "jianying-draft-plugin-source.tar.gz",
            "plugin-archive-audit.json",
            "release-evidence-verification.json",
            "release-install-canary-darwin-arm64.json",
            "release-install-canary-darwin-x64.json",
            "release-install-canary-win32-x64.json",
            "release-readiness.json",
        ])
    raise ValueError(f"unknown release name: {name}")


def released_asset_names(evidence: dict) -> list[str]:
    """规范化 gh release view 返回的资产集合。"""
    assets = evidence.get("assets")
    if not isinstance(assets, list):
        return []
    names = [asset.get("name") for asset in assets if isinstance(asset, dict)]
    if any(not isinstance(name, str) or not name for name in names):
        return []
    return sorted(names)


def release_assets_valid(
    evidence: dict,
    repository: str,
    release_ref: str,
    required_assets: list[str],
) -> bool:
    """验证精确资产集合、GitHub 摘要、状态、大小和正典下载身份。"""
    assets = evidence.get("assets")
    if not isinstance(assets, list) or len(assets) != len(required_assets):
        return False
    if released_asset_names(evidence) != required_assets:
        return False
    by_name = {
        asset.get("name"): asset
        for asset in assets
        if isinstance(asset, dict) and isinstance(asset.get("name"), str)
    }
    if len(by_name) != len(required_assets):
        return False
    prefix = f"https://github.com/{repository}/releases/download/{release_ref}/"
    for name in required_assets:
        asset = by_name.get(name)
        if (not isinstance(asset, dict)
                or asset.get("state") != "uploaded"
                or not isinstance(asset.get("size"), int)
                or asset["size"] <= 0
                or SHA256_DIGEST.fullmatch(str(asset.get("digest", ""))) is None
                or asset.get("url") != f"{prefix}{name}"):
            return False
    return True


def load_release_with_assets(
    query: Callable[[list[str]], object],
    repository: str,
    release_ref: str,
) -> dict:
    """用 REST 精确列出资产，避免 Release GraphQL 嵌入列表暂时为空。"""
    release = query(["api", f"repos/{repository}/releases/tags/{release_ref}"])
    if not isinstance(release, dict):
        raise RemoteQueryError("GitHub release metadata is malformed")
    release_id = release.get("id")
    if not isinstance(release_id, int) or isinstance(release_id, bool) or release_id <= 0:
        raise RemoteQueryError("GitHub release ID is missing")
    assets = query(["api", f"repos/{repository}/releases/{release_id}/assets?per_page=100"])
    if not isinstance(assets, list):
        raise RemoteQueryError("GitHub release assets are malformed")
    return {
        "tagName": release.get("tag_name"),
        "isDraft": release.get("draft"),
        "isPrerelease": release.get("prerelease"),
        "isImmutable": release.get("immutable"),
        "publishedAt": release.get("published_at"),
        "assets": [
            {**asset, "url": asset.get("browser_download_url")}
            if isinstance(asset, dict) else asset
            for asset in assets
        ],
    }


def release_tag_ruleset_fixture() -> list[dict]:
    """返回测试与文档共用的最小安全 tag ruleset 形状。"""
    return [{
        "target": "tag",
        "enforcement": "active",
        "bypass_actors": [],
        "conditions": {
            "ref_name": {"include": ["refs/tags/v*"], "exclude": []},
        },
        "rules": [{"type": "deletion"}, {"type": "non_fast_forward"}],
    }]


def release_tags_are_protected(evidence: object) -> bool:
    """确认 v* tag 由无 bypass 的 active ruleset 禁止删除与移动。"""
    if not isinstance(evidence, list):
        return False
    for ruleset in evidence:
        if not isinstance(ruleset, dict):
            continue
        conditions = ruleset.get("conditions")
        ref_name = conditions.get("ref_name") if isinstance(conditions, dict) else None
        include = ref_name.get("include") if isinstance(ref_name, dict) else None
        exclude = ref_name.get("exclude") if isinstance(ref_name, dict) else None
        rules = ruleset.get("rules")
        rule_types = {
            rule.get("type") for rule in rules or [] if isinstance(rule, dict)
        }
        if (
            ruleset.get("target") == "tag"
            and ruleset.get("enforcement") == "active"
            and ruleset.get("bypass_actors") == []
            and isinstance(include, list)
            and any(pattern in {"~ALL", "refs/tags/v*"} for pattern in include)
            and isinstance(exclude, list)
            and not exclude
            and {"deletion", "non_fast_forward"}.issubset(rule_types)
        ):
            return True
    return False


def load_release_tag_rulesets(
    query: Callable[[list[str]], object],
    repository: str,
) -> list[dict]:
    """列举适用 ruleset，并沿 GitHub 正典 self link 读取完整详情。"""
    summaries = query([
        "api", f"repos/{repository}/rulesets?includes_parents=true",
    ])
    if not isinstance(summaries, list):
        raise RemoteQueryError("GitHub ruleset list is not an array")
    details: list[dict] = []
    trusted_url = re.compile(
        r"https://api\.github\.com/(?:repos/[^/]+/[^/]+|orgs/[^/]+|"
        r"enterprises/[^/]+)/rulesets/\d+"
    )
    for summary in summaries:
        if not isinstance(summary, dict):
            raise RemoteQueryError("GitHub ruleset summary is malformed")
        if all(key in summary for key in ("conditions", "rules", "bypass_actors")):
            details.append(summary)
            continue
        links = summary.get("_links")
        self_link = links.get("self") if isinstance(links, dict) else None
        href = self_link.get("href") if isinstance(self_link, dict) else None
        if not isinstance(href, str) or trusted_url.fullmatch(href) is None:
            raise RemoteQueryError("GitHub ruleset summary omitted a trusted detail URL")
        detail = query(["api", href])
        if not isinstance(detail, dict):
            raise RemoteQueryError("GitHub ruleset detail is malformed")
        details.append(detail)
    return details


def load_equivalent_release_policy(root: Path) -> dict:
    """验证获批的 Immutable Release 与三阶段 tag commit 等价门禁。"""
    policy_path = root / "runtime/release-protection-policy.json"
    if not policy_path.is_file():
        raise ValueError("equivalent release protection policy is missing")
    try:
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError("equivalent release protection policy is invalid JSON") from error
    if not isinstance(policy, dict):
        raise TypeError("equivalent release protection policy must be an object")
    if policy.get("schema") != EQUIVALENT_POLICY_SCHEMA:
        raise ValueError("equivalent release protection policy schema is invalid")
    if policy.get("repository") != PLUGIN_REPOSITORY:
        raise ValueError("equivalent release protection policy repository is invalid")
    if policy.get("mode") != EQUIVALENT_POLICY_MODE:
        raise ValueError("equivalent release protection policy mode is invalid")
    if policy.get("approvedBy") != "project-owner":
        raise ValueError("equivalent release protection policy lacks owner approval")
    approved_at = policy.get("approvedAt")
    if not isinstance(approved_at, str):
        raise TypeError("equivalent release protection approval time is missing")
    try:
        parsed = datetime.fromisoformat(approved_at.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("equivalent release protection approval time is invalid") from error
    if parsed.tzinfo is None:
        raise ValueError("equivalent release protection approval time needs timezone")
    required = policy.get("requiredChecks")
    if (
        not isinstance(required, dict)
        or set(required) != EQUIVALENT_REQUIRED_CHECKS
        or any(required.get(name) is not True for name in EQUIVALENT_REQUIRED_CHECKS)
    ):
        raise ValueError("equivalent release protection required checks are incomplete")

    workflow_path = root / ".github/workflows/release-gate.yml"
    if not workflow_path.is_file():
        raise ValueError("release workflow is missing")
    workflow = workflow_path.read_text(encoding="utf-8")
    plan_marker = "python3 scripts/release_publication_plan.py"
    plan_positions = [match.start() for match in re.finditer(plan_marker, workflow)]
    if len(plan_positions) != 3:
        raise ValueError("equivalent policy requires exactly three tag commit rechecks")
    remote_marker = "--remote origin"
    commit_marker = '--expected-commit "$(git rev-parse HEAD)"'
    if workflow.count(remote_marker) != 3 or workflow.count(commit_marker) != 3:
        raise ValueError("equivalent policy requires three tag commit rechecks")
    create_position = workflow.find("gh release create")
    publish_position = workflow.find('gh release edit "$GITHUB_REF_NAME" --draft=false')
    final_verify_position = workflow.rfind('test "$(jq -r .action "$release_plan")" = "verify_existing"')
    immutable_position = workflow.find("immutable-releases")
    if not (
        0 <= immutable_position < plan_positions[0] < create_position
        < plan_positions[1] < publish_position < plan_positions[2]
        < final_verify_position
    ):
        raise ValueError("equivalent policy tag commit recheck order is invalid")
    workflow_sha256 = hashlib.sha256(workflow.encode("utf-8")).hexdigest()
    return {
        "schema": policy["schema"],
        "repository": policy["repository"],
        "mode": policy["mode"],
        "approvedAt": approved_at,
        "approvedBy": policy["approvedBy"],
        "requiredChecks": required,
        "workflow": str(workflow_path.relative_to(root)),
        "workflowSha256": workflow_sha256,
        "tagCommitRecheckCount": len(plan_positions),
    }


def gh_json(arguments: list[str]) -> object:
    """执行 gh 只读查询并解析 JSON。"""
    result = subprocess.run(
        ["gh", *arguments],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RemoteQueryError(result.stderr.strip() or result.stdout.strip())
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise RemoteQueryError(f"gh returned invalid JSON: {error}") from error


def remote_error_evidence(error: RemoteQueryError) -> dict:
    """把 GitHub 查询失败归一为可执行、稳定的阻塞原因。"""
    message = str(error)
    if (
        "Upgrade to GitHub Pro or make this repository public" in message
        and "HTTP 403" in message
    ):
        return {
            "error": message,
            "errorCode": "feature_unavailable_for_plan",
            "remediationOptions": [
                "upgrade_github_plan",
                "make_repository_public",
                "approve_equivalent_immutable_release_policy",
            ],
        }
    if "release not found" in message.lower() or "Not Found (HTTP 404)" in message:
        return {
            "error": message,
            "errorCode": "release_not_found",
            "remediationOptions": ["publish_expected_immutable_release"],
        }
    return {
        "error": message,
        "errorCode": "remote_query_failed",
        "remediationOptions": ["retry_read_only_preflight"],
    }


def release_protection_check(
    root: Path,
    query: Callable[[list[str]], object],
    repository: str,
) -> dict:
    """优先验证 tag ruleset；套餐不支持时验证显式批准的等价策略。"""
    identifier = "repository.plugin.release_protection"
    try:
        rulesets = load_release_tag_rulesets(query, repository)
    except RemoteQueryError as error:
        query_error = remote_error_evidence(error)
        if query_error.get("errorCode") != "feature_unavailable_for_plan":
            return {"id": identifier, "status": "blocked", "evidence": query_error}
        try:
            policy = load_equivalent_release_policy(root)
        except (OSError, TypeError, ValueError) as policy_error:
            return {
                "id": identifier,
                "status": "blocked",
                "evidence": {
                    "error": str(policy_error),
                    "errorCode": "equivalent_policy_invalid",
                    "rulesetQuery": query_error,
                },
            }
        return {
            "id": identifier,
            "status": "ready",
            "evidence": {
                "strategy": EQUIVALENT_POLICY_MODE,
                "rulesetQuery": query_error,
                "policy": policy,
            },
        }
    if release_tags_are_protected(rulesets):
        return {
            "id": identifier,
            "status": "ready",
            "evidence": {"strategy": "tag_ruleset", "rulesets": rulesets},
        }
    return {
        "id": identifier,
        "status": "blocked",
        "evidence": {
            "error": "active tag protection ruleset is missing or incomplete",
            "errorCode": "tag_ruleset_missing",
            "rulesets": rulesets,
        },
    }


def check(identifier: str, query: Callable[[], dict], predicate: Callable[[dict], bool]) -> dict:
    """执行单个只读检查并返回稳定状态。"""
    try:
        evidence = query()
        ready = predicate(evidence)
        return {
            "id": identifier,
            "status": "ready" if ready else "blocked",
            "evidence": evidence,
        }
    except RemoteQueryError as error:
        return {
            "id": identifier,
            "status": "blocked",
            "evidence": remote_error_evidence(error),
        }


def build_report(
    root: Path = ROOT,
    query: Callable[[list[str]], dict] = gh_json,
) -> dict:
    """构造远端发布前置条件与完整发布状态报告。"""
    plugin = json.loads((root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    cli_lock = json.loads((root / "runtime/jianying-cli.lock.json").read_text(encoding="utf-8"))
    skills_lock = json.loads((root / "skills.lock.json").read_text(encoding="utf-8"))
    sources = skills_lock.get("sources")
    if not isinstance(sources, list) or len(sources) != 1:
        raise ValueError("skills.lock.json must contain exactly one source")
    skills_version = sources[0].get("releaseVersion")
    if not isinstance(skills_version, str) or re.fullmatch(r"\d+\.\d+\.\d+", skills_version) is None:
        raise ValueError("skills.lock.json releaseVersion is invalid")
    plugin_version = plugin["version"].split("+")[0]
    cli_version = cli_lock.get("resolvedVersion") or cli_lock["minimumVersion"]
    expected = {
        "cli": {
            "repository": CLI_REPOSITORY,
            "ref": f"v{cli_version}",
            "assets": expected_release_assets("cli", cli_version),
        },
        "skills": {
            "repository": SKILLS_REPOSITORY,
            "ref": f"v{skills_version}",
            "assets": expected_release_assets("skills", skills_version),
        },
        "plugin": {
            "repository": PLUGIN_REPOSITORY,
            "ref": f"v{plugin_version}",
            "assets": expected_release_assets("plugin", plugin_version),
        },
    }
    checks = []
    for name, release in expected.items():
        repository = release["repository"]
        release_ref = release["ref"]
        required_assets = release["assets"]
        checks.append(check(
            f"repository.{name}.immutable_releases",
            lambda repository=repository: query([
                "api", f"repos/{repository}/immutable-releases",
            ]),
            lambda evidence: evidence.get("enabled") is True,
        ))
        if name == "plugin":
            checks.append(release_protection_check(root, query, repository))
        checks.append(check(
            f"release.{name}.expected",
            lambda repository=repository, release_ref=release_ref: load_release_with_assets(
                query, repository, release_ref,
            ),
            lambda evidence, repository=repository, release_ref=release_ref,
            required_assets=required_assets: (
                evidence.get("tagName") == release_ref
                and evidence.get("isDraft") is False
                and evidence.get("isPrerelease") is False
                and evidence.get("isImmutable") is True
                and isinstance(evidence.get("publishedAt"), str)
                and bool(evidence["publishedAt"])
                and release_assets_valid(
                    evidence, repository, release_ref, required_assets,
                )
            ),
        ))

    by_id = {item["id"]: item for item in checks}
    prerequisite_ids = {
        "repository.cli.immutable_releases",
        "release.cli.expected",
        "repository.skills.immutable_releases",
        "release.skills.expected",
        "repository.plugin.immutable_releases",
        "repository.plugin.release_protection",
    }
    prerequisites_ready = all(by_id[name]["status"] == "ready" for name in prerequisite_ids)
    release_complete = prerequisites_ready and by_id["release.plugin.expected"]["status"] == "ready"
    blocked_prerequisites = [
        item["id"]
        for item in checks
        if item["id"] in prerequisite_ids and item["status"] == "blocked"
    ]
    return {
        "schema": REPORT_SCHEMA,
        "prerequisitesReady": prerequisites_ready,
        "releaseComplete": release_complete,
        "expected": expected,
        "checks": checks,
        "blockedPrerequisites": blocked_prerequisites,
        "blocked": [item["id"] for item in checks if item["status"] == "blocked"],
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
    return 0 if report["prerequisitesReady"] else 1


if __name__ == "__main__":
    sys.exit(main())
