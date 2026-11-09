"""GitHub 不可变 Release 下载资产的本地字节绑定测试。"""

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "verify_github_release_asset",
    ROOT / "scripts" / "verify_github_release_asset.py",
)
VERIFIER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFIER)


class GitHubReleaseAssetTests(unittest.TestCase):
    def fixture(self) -> tuple[tempfile.TemporaryDirectory, Path, Path, dict]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        asset = root / "jianying-skills.manifest.json"
        asset.write_bytes(b'{"schema":"fixture"}\n')
        digest = hashlib.sha256(asset.read_bytes()).hexdigest()
        metadata = {
            "tagName": "v2.0.3",
            "isDraft": False,
            "isPrerelease": False,
            "isImmutable": True,
            "publishedAt": "2026-09-21T00:00:00Z",
            "assets": [{
                "name": asset.name,
                "digest": f"sha256:{digest}",
                "size": asset.stat().st_size,
                "state": "uploaded",
                "url": (
                    "https://github.com/full-aigc-skills/jianying-skills/"
                    f"releases/download/v2.0.3/{asset.name}"
                ),
            }],
        }
        metadata_path = root / "release.json"
        metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
        return temporary, asset, metadata_path, metadata

    def test_binds_downloaded_bytes_to_exact_release_asset_metadata(self) -> None:
        temporary, asset, metadata_path, _ = self.fixture()
        try:
            evidence = VERIFIER.verify_release_asset(
                metadata_path,
                asset,
                repository="full-aigc-skills/jianying-skills",
                release_ref="v2.0.3",
            )
            self.assertEqual(
                evidence["schema"],
                "jianying-github-release-asset-verification/v1",
            )
            self.assertEqual(evidence["asset"], asset.name)
            self.assertEqual(evidence["sha256"], hashlib.sha256(asset.read_bytes()).hexdigest())
            self.assertEqual(evidence["size"], asset.stat().st_size)
            self.assertTrue(evidence["verified"])
        finally:
            temporary.cleanup()

    def test_binds_rest_release_and_separately_listed_assets(self) -> None:
        temporary, asset, metadata_path, metadata = self.fixture()
        try:
            rest_metadata = {
                "id": 394465333,
                "tag_name": metadata["tagName"],
                "draft": False,
                "prerelease": False,
                "immutable": True,
                "published_at": metadata["publishedAt"],
                "assets": [],
            }
            metadata_path.write_text(json.dumps(rest_metadata), encoding="utf-8")
            rest_asset = dict(metadata["assets"][0])
            rest_asset["browser_download_url"] = rest_asset.pop("url")
            rest_asset["url"] = "https://api.github.com/repos/full-aigc-skills/jianying-skills/releases/assets/1"
            assets_path = asset.parent / "assets.json"
            assets_path.write_text(json.dumps([rest_asset]), encoding="utf-8")
            evidence = VERIFIER.verify_release_asset(
                metadata_path,
                asset,
                repository="full-aigc-skills/jianying-skills",
                release_ref="v2.0.3",
                assets_metadata_path=assets_path,
            )
            self.assertTrue(evidence["verified"])
            self.assertEqual(evidence["sha256"], hashlib.sha256(asset.read_bytes()).hexdigest())
        finally:
            temporary.cleanup()

    def test_rejects_downloaded_content_or_size_drift(self) -> None:
        temporary, asset, metadata_path, _ = self.fixture()
        try:
            asset.write_bytes(b"tampered")
            with self.assertRaisesRegex(ValueError, "size differs|digest differs"):
                VERIFIER.verify_release_asset(
                    metadata_path,
                    asset,
                    repository="full-aigc-skills/jianying-skills",
                    release_ref="v2.0.3",
                )
        finally:
            temporary.cleanup()

    def test_rejects_ambiguous_or_missing_asset_identity(self) -> None:
        for assets in ([], None):
            with self.subTest(assets=assets):
                temporary, asset, metadata_path, metadata = self.fixture()
                try:
                    metadata["assets"] = assets
                    metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, "exactly one matching asset"):
                        VERIFIER.verify_release_asset(
                            metadata_path,
                            asset,
                            repository="full-aigc-skills/jianying-skills",
                            release_ref="v2.0.3",
                        )
                finally:
                    temporary.cleanup()

        temporary, asset, metadata_path, metadata = self.fixture()
        try:
            metadata["assets"].append(dict(metadata["assets"][0]))
            metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "exactly one matching asset"):
                VERIFIER.verify_release_asset(
                    metadata_path,
                    asset,
                    repository="full-aigc-skills/jianying-skills",
                    release_ref="v2.0.3",
                )
        finally:
            temporary.cleanup()

    def test_rejects_unstable_release_or_asset_metadata_drift(self) -> None:
        mutations = (
            ("release tag", lambda metadata: metadata.update({"tagName": "v2.0.4"})),
            ("stable immutable", lambda metadata: metadata.update({"isImmutable": False})),
            ("published timestamp", lambda metadata: metadata.update({"publishedAt": None})),
            ("uploaded", lambda metadata: metadata["assets"][0].update({"state": "new"})),
            ("positive size", lambda metadata: metadata["assets"][0].update({"size": 0})),
            ("valid sha256 digest", lambda metadata: metadata["assets"][0].update({"digest": "sha256:1234"})),
            ("canonical release URL", lambda metadata: metadata["assets"][0].update({"url": "https://example.invalid/asset"})),
        )
        for expected, mutate in mutations:
            with self.subTest(expected=expected):
                temporary, asset, metadata_path, metadata = self.fixture()
                try:
                    mutate(metadata)
                    metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, expected):
                        VERIFIER.verify_release_asset(
                            metadata_path,
                            asset,
                            repository="full-aigc-skills/jianying-skills",
                            release_ref="v2.0.3",
                        )
                finally:
                    temporary.cleanup()


if __name__ == "__main__":
    unittest.main()
