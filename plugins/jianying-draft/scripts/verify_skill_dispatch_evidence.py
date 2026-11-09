#!/usr/bin/env python3
"""核对技能发布 dispatch 与实际 checkout/manifest 的身份。"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

COMMIT = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def git_head(source_root: Path) -> str:
    """读取技能发布 checkout 的实际提交。"""
    return subprocess.run(
        ["git", "-C", str(source_root), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def verify_dispatch_evidence(
    manifest_path: Path,
    *,
    expected_source_commit: str = "",
    expected_manifest_sha256: str = "",
    observed_source_commit: str,
) -> dict:
    """仅在 dispatch 提供证据时要求其与实际下载内容完全一致。"""
    if expected_source_commit:
        if COMMIT.fullmatch(expected_source_commit) is None:
            raise ValueError("dispatch source commit is invalid")
        if observed_source_commit != expected_source_commit:
            raise ValueError("skill checkout commit differs from dispatch evidence")
    if expected_manifest_sha256:
        if SHA256.fullmatch(expected_manifest_sha256) is None:
            raise ValueError("dispatch manifest SHA-256 is invalid")
        actual_digest = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        if actual_digest != expected_manifest_sha256:
            raise ValueError("skill manifest digest differs from dispatch evidence")
    return {
        "source_commit": observed_source_commit,
        "manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--expected-source-commit", default="")
    parser.add_argument("--expected-manifest-sha256", default="")
    arguments = parser.parse_args()
    try:
        result = verify_dispatch_evidence(
            arguments.manifest,
            expected_source_commit=arguments.expected_source_commit,
            expected_manifest_sha256=arguments.expected_manifest_sha256,
            observed_source_commit=git_head(arguments.source_root),
        )
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"ERROR: {error}")
        return 1
    print(
        "verified skill dispatch evidence: "
        f"commit={result['source_commit']} manifest={result['manifest_sha256']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
