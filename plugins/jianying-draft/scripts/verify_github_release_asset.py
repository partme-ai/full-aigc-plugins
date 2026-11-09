#!/usr/bin/env python3
"""将下载文件的实际字节绑定到 GitHub 不可变 Release 资产元数据。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

EVIDENCE_SCHEMA = "jianying-github-release-asset-verification/v1"
REPOSITORY_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
RELEASE_REF_PATTERN = re.compile(r"^v[0-9]+\.[0-9]+\.[0-9]+$")
SHA256_PATTERN = re.compile(r"^sha256:([0-9a-f]{64})$")


def sha256_file(path: Path) -> str:
    """流式计算下载资产的 SHA-256。"""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_release_asset(
    metadata_path: Path,
    asset_path: Path,
    *,
    repository: str,
    release_ref: str,
    assets_metadata_path: Path | None = None,
) -> dict:
    """验证稳定不可变 Release 元数据与本地下载文件完全一致。"""
    if REPOSITORY_PATTERN.fullmatch(repository) is None:
        raise ValueError("repository must be an owner/name pair")
    if RELEASE_REF_PATTERN.fullmatch(release_ref) is None:
        raise ValueError("release ref must be an immutable v<semver> tag")
    if not metadata_path.is_file():
        raise ValueError("release metadata file is missing")
    if not asset_path.is_file():
        raise ValueError("downloaded release asset is missing")

    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"release metadata is not valid JSON: {error}") from error
    if not isinstance(metadata, dict):
        raise TypeError("release metadata must be an object")
    tag_name = metadata.get("tagName", metadata.get("tag_name"))
    is_draft = metadata.get("isDraft", metadata.get("draft"))
    is_prerelease = metadata.get("isPrerelease", metadata.get("prerelease"))
    is_immutable = metadata.get("isImmutable", metadata.get("immutable"))
    published_at = metadata.get("publishedAt", metadata.get("published_at"))
    if tag_name != release_ref:
        raise ValueError("release tag differs from the requested ref")
    if (is_draft is not False
            or is_prerelease is not False
            or is_immutable is not True):
        raise ValueError("release must be a stable immutable publication")
    if not isinstance(published_at, str) or not published_at:
        raise ValueError("release metadata has no published timestamp")

    if assets_metadata_path is not None:
        if not assets_metadata_path.is_file():
            raise ValueError("release assets metadata file is missing")
        try:
            assets = json.loads(assets_metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError(f"release assets metadata is not valid JSON: {error}") from error
    else:
        assets = metadata.get("assets")
    matching = [] if not isinstance(assets, list) else [
        item for item in assets
        if isinstance(item, dict) and item.get("name") == asset_path.name
    ]
    if len(matching) != 1:
        raise ValueError("release metadata must contain exactly one matching asset")
    asset = matching[0]
    if asset.get("state") != "uploaded":
        raise ValueError("release asset is not uploaded")
    expected_size = asset.get("size")
    if not isinstance(expected_size, int) or isinstance(expected_size, bool) or expected_size <= 0:
        raise ValueError("release asset must declare a positive size")
    digest_match = SHA256_PATTERN.fullmatch(str(asset.get("digest", "")))
    if digest_match is None:
        raise ValueError("release asset must declare a valid sha256 digest")
    expected_url = (
        f"https://github.com/{repository}/releases/download/"
        f"{release_ref}/{asset_path.name}"
    )
    if asset.get("browser_download_url", asset.get("url")) != expected_url:
        raise ValueError("release asset URL is not the canonical release URL")

    actual_size = asset_path.stat().st_size
    if actual_size != expected_size:
        raise ValueError("downloaded release asset size differs from GitHub metadata")
    actual_sha256 = sha256_file(asset_path)
    if actual_sha256 != digest_match.group(1):
        raise ValueError("downloaded release asset digest differs from GitHub metadata")

    return {
        "schema": EVIDENCE_SCHEMA,
        "verified": True,
        "repository": repository,
        "releaseRef": release_ref,
        "publishedAt": published_at,
        "asset": asset_path.name,
        "size": actual_size,
        "sha256": actual_sha256,
        "githubDigest": asset["digest"],
        "url": expected_url,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--assets-metadata", type=Path)
    parser.add_argument("--asset", type=Path, required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--release-ref", required=True)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    try:
        evidence = verify_release_asset(
            arguments.metadata,
            arguments.asset,
            repository=arguments.repository,
            release_ref=arguments.release_ref,
            assets_metadata_path=arguments.assets_metadata,
        )
    except ValueError as error:
        print(f"release asset verification failed: {error}", file=sys.stderr)
        return 1
    rendered = json.dumps(evidence, ensure_ascii=False, indent=2) + "\n"
    if arguments.output:
        arguments.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
