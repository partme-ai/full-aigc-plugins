#!/usr/bin/env python3
"""校验 Codex、ZCode、Kimi 的真实发布验收证据。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

SUMMARY_SCHEMA = "jianying-host-release-acceptance/v1"
EVIDENCE_SCHEMA = "jianying-host-run-evidence/v2"
JOB_SCHEMA = "jianying-job/v2"
EXPECTED_HOSTS = {"codex", "zcode", "kimi"}
REQUIRED_CHECKS = {
    "freshInstall",
    "doctor",
    "skillDiscovery",
    "singleSkillInstall",
    "categoryDiscovery",
    "categoryRouting",
    "selectionExplanation",
    "approval",
    "simpleJob",
    "stop",
    "recovery",
    "evidenceDisplay",
    "nativeExportApproval",
}
CHECK_EVIDENCE_KINDS = {"host_command", "host_ui", "host_api", "artifact"}
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def load_json(path: Path) -> dict:
    """读取 JSON 对象，拒绝数组和标量顶层。"""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"host acceptance JSON must be an object: {path}")
    return value


def canonical_sha256(value: object) -> str:
    """按稳定 UTF-8 canonical JSON 计算语义摘要。"""
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_timestamp(value: object, host: str) -> None:
    """要求带时区的 RFC 3339 时间，避免无法审计的本地时间。"""
    if not isinstance(value, str):
        raise TypeError(f"{host}: executedAt must be RFC 3339")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"{host}: executedAt must be RFC 3339") from error
    if parsed.tzinfo is None:
        raise ValueError(f"{host}: executedAt must include a timezone")


def validate_check_evidence(value: object, host: str) -> None:
    """验证十三项检查均绑定可重算的宿主证据，而不是只有布尔声明。"""
    if not isinstance(value, dict) or set(value) != REQUIRED_CHECKS:
        raise ValueError(f"{host}: checkEvidence must cover every required check exactly once")
    for name in sorted(REQUIRED_CHECKS):
        record = value.get(name)
        if not isinstance(record, dict):
            raise TypeError(f"{host}: {name} check evidence must be an object")
        kind = record.get("kind")
        if kind not in CHECK_EVIDENCE_KINDS:
            raise ValueError(f"{host}: {name} check evidence kind is invalid")
        validate_timestamp(record.get("observedAt"), f"{host}:{name}")
        artifact = record.get("artifact")
        if not isinstance(artifact, dict):
            raise TypeError(f"{host}: {name} check evidence artifact must be an object")
        expected_digest = record.get("artifactSha256")
        if not isinstance(expected_digest, str) or not SHA256.fullmatch(expected_digest):
            raise ValueError(f"{host}: {name} check evidence digest is invalid")
        if canonical_sha256(artifact) != expected_digest:
            raise ValueError(f"{host}: {name} check evidence digest differs from artifact")


def resolve_evidence_path(root: Path, relative: object, host: str) -> Path:
    """将证据限制在 runtime/host-evidence，拒绝路径穿越。"""
    if not isinstance(relative, str) or not relative:
        raise ValueError(f"{host}: evidencePath is missing")
    expected_root = (root / "runtime" / "host-evidence").resolve()
    path = (root / relative).resolve()
    if expected_root not in path.parents:
        raise ValueError(f"{host}: evidencePath must stay under runtime/host-evidence")
    if not path.is_file():
        raise ValueError(f"{host}: evidence file is missing")
    return path


def validate_acceptance_document(
    root: Path,
    summary: dict,
    expected_plugin_version: str,
    expected_cli_version: str,
    expected_skills_version: str,
) -> dict:
    """验证汇总对象、三宿主原始证据、版本绑定和语义等价。"""
    root = root.resolve()
    if summary.get("schema") != SUMMARY_SCHEMA:
        raise ValueError("unsupported host release acceptance schema")
    if summary.get("status") != "passed":
        raise ValueError("host release acceptance is not passed")
    expected_identity = {
        "pluginVersion": expected_plugin_version,
        "cliVersion": expected_cli_version,
        "skillsVersion": expected_skills_version,
        "jobSchema": JOB_SCHEMA,
    }
    for key, expected in expected_identity.items():
        if not expected or summary.get(key) != expected:
            raise ValueError(f"host acceptance {key} does not match the release lock")

    entries = summary.get("hosts")
    if not isinstance(entries, list):
        raise TypeError("host acceptance hosts must be an array")
    host_names = [entry.get("host") for entry in entries if isinstance(entry, dict)]
    if len(entries) != len(EXPECTED_HOSTS) or set(host_names) != EXPECTED_HOSTS:
        raise ValueError("host acceptance must contain exactly Codex, ZCode, and Kimi")
    if len(host_names) != len(set(host_names)):
        raise ValueError("host acceptance contains duplicate hosts")

    job_inputs = set()
    semantic_results = set()
    for entry in entries:
        host = entry["host"]
        path = resolve_evidence_path(root, entry.get("evidencePath"), host)
        expected_digest = entry.get("evidenceSha256")
        actual_digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if not isinstance(expected_digest, str) or not SHA256.fullmatch(expected_digest):
            raise ValueError(f"{host}: evidence digest is invalid")
        if actual_digest != expected_digest:
            raise ValueError(f"{host}: evidence digest differs from the acceptance summary")

        evidence = load_json(path)
        if evidence.get("schema") != EVIDENCE_SCHEMA or evidence.get("host") != host:
            raise ValueError(f"{host}: evidence schema or host identity is invalid")
        if evidence.get("evidenceLevel") != "real_host":
            raise ValueError(f"{host}: evidenceLevel must be real_host")
        for key, expected in expected_identity.items():
            if evidence.get(key) != expected:
                raise ValueError(f"{host}: {key} does not match the release lock")
        validate_timestamp(evidence.get("executedAt"), host)
        checks = evidence.get("checks")
        if not isinstance(checks, dict) or any(checks.get(name) is not True for name in REQUIRED_CHECKS):
            raise ValueError(f"{host}: required real-host checks are incomplete")
        validate_check_evidence(evidence.get("checkEvidence"), host)
        job_input = evidence.get("jobInputSha256")
        semantic_result = evidence.get("resultSemanticSha256")
        job_input_value = evidence.get("jobInput")
        semantic_result_value = evidence.get("semanticResult")
        if not isinstance(job_input_value, dict):
            raise TypeError(f"{host}: jobInput must be an object")
        if not isinstance(semantic_result_value, dict):
            raise TypeError(f"{host}: semanticResult must be an object")
        if not isinstance(job_input, str) or not SHA256.fullmatch(job_input):
            raise ValueError(f"{host}: job input digest is invalid")
        if not isinstance(semantic_result, str) or not SHA256.fullmatch(semantic_result):
            raise ValueError(f"{host}: semantic result digest is invalid")
        if canonical_sha256(job_input_value) != job_input:
            raise ValueError(f"{host}: job input digest differs from the embedded object")
        if canonical_sha256(semantic_result_value) != semantic_result:
            raise ValueError(f"{host}: semantic result digest differs from the embedded object")
        job_inputs.add(job_input)
        semantic_results.add(semantic_result)

    if len(job_inputs) != 1:
        raise ValueError("real hosts did not execute the same Job input")
    if len(semantic_results) != 1:
        raise ValueError("real hosts did not produce one semantic result")
    return {
        "hosts": sorted(EXPECTED_HOSTS),
        "job_input_sha256": next(iter(job_inputs)),
        "result_semantic_sha256": next(iter(semantic_results)),
    }


def validate_acceptance(
    root: Path,
    expected_plugin_version: str,
    expected_cli_version: str,
    expected_skills_version: str,
) -> dict:
    """从固定汇总锁验证三宿主真实发布验收。"""
    root = root.resolve()
    summary_path = root / "runtime" / "host-acceptance.json"
    if not summary_path.is_file():
        raise ValueError("host release acceptance summary is missing")
    return validate_acceptance_document(
        root,
        load_json(summary_path),
        expected_plugin_version,
        expected_cli_version,
        expected_skills_version,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--plugin-version", required=True)
    parser.add_argument("--cli-version", required=True)
    parser.add_argument("--skills-version", required=True)
    arguments = parser.parse_args()
    try:
        result = validate_acceptance(
            arguments.root,
            arguments.plugin_version,
            arguments.cli_version,
            arguments.skills_version,
        )
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False))
        return 1
    print(json.dumps({"ok": True, "data": result}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
