#!/usr/bin/env python3
"""将真实宿主 observation 记录为可验证的发布验收证据。"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

import host_acceptance

OBSERVATION_SCHEMA = "jianying-host-observation/v2"
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def record_observation(observation: dict, output_path: Path) -> dict:
    """校验真实运行 observation，计算 canonical 摘要并原子写入证据。"""
    if observation.get("schema") != OBSERVATION_SCHEMA:
        raise ValueError("unsupported host observation schema")
    host = observation.get("host")
    if host not in host_acceptance.EXPECTED_HOSTS:
        raise ValueError("host observation must identify Codex, ZCode, or Kimi")
    for key in ("pluginVersion", "cliVersion", "skillsVersion"):
        value = observation.get(key)
        if not isinstance(value, str) or not SEMVER.fullmatch(value):
            raise ValueError(f"host observation {key} must be semantic x.y.z")
    if observation.get("jobSchema") != host_acceptance.JOB_SCHEMA:
        raise ValueError("host observation must use jianying-job/v2")
    host_acceptance.validate_timestamp(observation.get("executedAt"), host)
    checks = observation.get("checks")
    if not isinstance(checks, dict) or any(
        checks.get(name) is not True for name in host_acceptance.REQUIRED_CHECKS
    ):
        raise ValueError("host observation checks are incomplete")
    check_evidence = observation.get("checkEvidence")
    host_acceptance.validate_check_evidence(check_evidence, host)
    job_input = observation.get("jobInput")
    semantic_result = observation.get("semanticResult")
    if not isinstance(job_input, dict) or not isinstance(semantic_result, dict):
        raise TypeError("host observation jobInput and semanticResult must be objects")

    evidence = {
        "schema": host_acceptance.EVIDENCE_SCHEMA,
        "host": host,
        "evidenceLevel": "real_host",
        "pluginVersion": observation["pluginVersion"],
        "cliVersion": observation["cliVersion"],
        "skillsVersion": observation["skillsVersion"],
        "jobSchema": observation["jobSchema"],
        "jobInput": job_input,
        "semanticResult": semantic_result,
        "jobInputSha256": host_acceptance.canonical_sha256(job_input),
        "resultSemanticSha256": host_acceptance.canonical_sha256(semantic_result),
        "executedAt": observation["executedAt"],
        "checks": checks,
        "checkEvidence": check_evidence,
    }
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = output_path.with_name(f".{output_path.name}.{os.getpid()}.tmp")
    temporary.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, output_path)
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--observation", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        observation = host_acceptance.load_json(arguments.observation)
        evidence = record_observation(observation, arguments.output)
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False))
        return 1
    print(json.dumps({
        "ok": True,
        "data": {
            "host": evidence["host"],
            "output": str(arguments.output.resolve()),
            "jobInputSha256": evidence["jobInputSha256"],
            "resultSemanticSha256": evidence["resultSemanticSha256"],
        },
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
