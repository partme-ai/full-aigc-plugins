#!/usr/bin/env python3
"""验证三份真实宿主证据并原子生成 passed 汇总锁。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

import host_acceptance


def finalize_acceptance(
    root: Path,
    plugin_version: str,
    cli_version: str,
    skills_version: str,
) -> dict:
    """先完整校验证据集合，成功后才替换 host-acceptance.json。"""
    root = root.resolve()
    entries = []
    for host in sorted(host_acceptance.EXPECTED_HOSTS):
        relative = f"runtime/host-evidence/{host}.json"
        path = root / relative
        if not path.is_file():
            raise ValueError(f"{host}: evidence file is missing")
        entries.append({
            "host": host,
            "evidencePath": relative,
            "evidenceSha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    summary = {
        "schema": host_acceptance.SUMMARY_SCHEMA,
        "status": "passed",
        "pluginVersion": plugin_version,
        "cliVersion": cli_version,
        "skillsVersion": skills_version,
        "jobSchema": host_acceptance.JOB_SCHEMA,
        "hosts": entries,
    }
    host_acceptance.validate_acceptance_document(
        root,
        summary,
        plugin_version,
        cli_version,
        skills_version,
    )
    output = root / "runtime" / "host-acceptance.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(f".{output.name}.{os.getpid()}.tmp")
    temporary.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, output)
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--plugin-version", required=True)
    parser.add_argument("--cli-version", required=True)
    parser.add_argument("--skills-version", required=True)
    arguments = parser.parse_args()
    try:
        summary = finalize_acceptance(
            arguments.root,
            arguments.plugin_version,
            arguments.cli_version,
            arguments.skills_version,
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False))
        return 1
    print(json.dumps({
        "ok": True,
        "data": {"status": summary["status"], "hosts": len(summary["hosts"])},
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
