"""远端发布只读预检测试。"""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "remote_release_preflight", ROOT / "scripts/remote_release_preflight.py"
)
PREFLIGHT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREFLIGHT)


class RemoteReleasePreflightTests(unittest.TestCase):
    @staticmethod
    def write_equivalent_policy(root: Path) -> None:
        workflow = root / ".github/workflows/release-gate.yml"
        workflow.parent.mkdir(parents=True)
        workflow.write_text(
            """enabled=\"$(gh api repos/${GITHUB_REPOSITORY}/immutable-releases)\"\n
python3 scripts/release_publication_plan.py --remote origin --expected-commit \"$(git rev-parse HEAD)\"\n
gh release create \"$GITHUB_REF_NAME\" --draft\n
python3 scripts/release_publication_plan.py --remote origin --expected-commit \"$(git rev-parse HEAD)\"\n
gh release edit \"$GITHUB_REF_NAME\" --draft=false\n
python3 scripts/release_publication_plan.py --remote origin --expected-commit \"$(git rev-parse HEAD)\"\n
test \"$(jq -r .action \"$release_plan\")\" = \"verify_existing\"\n
""",
            encoding="utf-8",
        )
        (root / "runtime/release-protection-policy.json").write_text(
            json.dumps({
                "schema": "jianying-release-protection-policy/v1",
                "repository": PREFLIGHT.PLUGIN_REPOSITORY,
                "mode": "immutable_release_with_tag_commit_rechecks",
                "approvedAt": "2026-09-22T00:00:00+08:00",
                "approvedBy": "project-owner",
                "requiredChecks": {
                    "immutableReleasesEnabled": True,
                    "beforeDraftTagCommit": True,
                    "beforePublishTagCommit": True,
                    "afterPublishTagCommit": True,
                    "publishedReleaseImmutable": True,
                },
            }),
            encoding="utf-8",
        )

    def fixture(self) -> tuple[Path, tempfile.TemporaryDirectory]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / ".codex-plugin").mkdir()
        (root / "runtime").mkdir()
        (root / ".codex-plugin/plugin.json").write_text(json.dumps({
            "version": "0.17.2+codex.20260920",
        }), encoding="utf-8")
        (root / "runtime/jianying-cli.lock.json").write_text(json.dumps({
            "minimumVersion": "1.6.0",
            "resolvedVersion": None,
        }), encoding="utf-8")
        (root / "skills.lock.json").write_text(json.dumps({
            "sources": [{"releaseVersion": "2.2.2"}],
        }), encoding="utf-8")
        self.write_equivalent_policy(root)
        return root, temporary

    @staticmethod
    def ready_query(arguments: list[str]) -> object:
        endpoint = arguments[1]
        if "rulesets" in endpoint:
            return PREFLIGHT.release_tag_ruleset_fixture()
        if "/releases/tags/" in endpoint:
            repository, release_ref = endpoint.removeprefix("repos/").split("/releases/tags/")
            release_id = {
                PREFLIGHT.CLI_REPOSITORY: 1,
                PREFLIGHT.SKILLS_REPOSITORY: 2,
                PREFLIGHT.PLUGIN_REPOSITORY: 3,
            }[repository]
            return {
                "id": release_id,
                "tag_name": release_ref,
                "draft": False,
                "prerelease": False,
                "immutable": True,
                "published_at": "2026-09-20T00:00:00Z",
                "assets": [],
            }
        if "/releases/" in endpoint and "/assets?" in endpoint:
            repository, suffix = endpoint.removeprefix("repos/").split("/releases/")
            release_id = int(suffix.split("/")[0])
            name, release_ref = {
                1: ("cli", "v1.6.0"),
                2: ("skills", "v2.2.2"),
                3: ("plugin", "v0.17.2"),
            }[release_id]
            assets = PREFLIGHT.expected_release_assets(name, release_ref.removeprefix("v"))
            return [{
                "name": asset,
                "digest": f"sha256:{'a' * 64}",
                "size": 1024,
                "state": "uploaded",
                "browser_download_url": (
                    f"https://github.com/{repository}/releases/download/"
                    f"{release_ref}/{asset}"
                ),
            } for asset in assets]
        return {"enabled": True}

    def test_all_prerequisites_and_plugin_release_are_distinguished(self) -> None:
        root, temporary = self.fixture()
        try:
            report = PREFLIGHT.build_report(root, self.ready_query)
            self.assertEqual(report["schema"], "jianying-remote-release-preflight/v2")
            self.assertTrue(report["prerequisitesReady"])
            self.assertTrue(report["releaseComplete"])
            self.assertEqual(report["blocked"], [])
            self.assertEqual(report["blockedPrerequisites"], [])
            self.assertEqual(report["expected"]["cli"]["ref"], "v1.6.0")
            self.assertEqual(report["expected"]["skills"]["ref"], "v2.2.2")
        finally:
            temporary.cleanup()

    def test_rest_asset_listing_prevents_empty_embedded_release_assets(self) -> None:
        root, temporary = self.fixture()
        try:
            def query(arguments: list[str]) -> object:
                if arguments[0] != "api":
                    raise PREFLIGHT.RemoteQueryError("GraphQL release assets are empty")
                endpoint = arguments[1]
                if "/releases/tags/" in endpoint:
                    release_ref = endpoint.rsplit("/", 1)[-1]
                    return {
                        "id": {"v1.6.0": 1, "v2.2.2": 2, "v0.17.2": 3}[release_ref],
                        "tag_name": release_ref,
                        "draft": False,
                        "prerelease": False,
                        "immutable": True,
                        "published_at": "2026-09-20T00:00:00Z",
                        "assets": [],
                    }
                if "/releases/" in endpoint and "/assets?" in endpoint:
                    repository = endpoint.split("/releases/")[0].removeprefix("repos/")
                    release_id = int(endpoint.split("/releases/")[1].split("/")[0])
                    name = {1: "cli", 2: "skills", 3: "plugin"}[release_id]
                    release_ref = {1: "v1.6.0", 2: "v2.2.2", 3: "v0.17.2"}[release_id]
                    return [{
                        "name": asset,
                        "digest": f"sha256:{'a' * 64}",
                        "size": 1024,
                        "state": "uploaded",
                        "browser_download_url": f"https://github.com/{repository}/releases/download/{release_ref}/{asset}",
                    } for asset in PREFLIGHT.expected_release_assets(name, release_ref.removeprefix("v"))]
                if "rulesets" in endpoint:
                    return PREFLIGHT.release_tag_ruleset_fixture()
                return {"enabled": True}

            report = PREFLIGHT.build_report(root, query)
            self.assertTrue(report["prerequisitesReady"])
            self.assertTrue(report["releaseComplete"])
        finally:
            temporary.cleanup()

    def test_missing_plugin_release_does_not_hide_ready_prerequisites(self) -> None:
        root, temporary = self.fixture()
        try:
            def query(arguments: list[str]) -> dict:
                if "/jianying-draft-plugin/releases/tags/v0.17.2" in arguments[1]:
                    raise PREFLIGHT.RemoteQueryError("release not found")
                return self.ready_query(arguments)

            report = PREFLIGHT.build_report(root, query)
            self.assertTrue(report["prerequisitesReady"])
            self.assertFalse(report["releaseComplete"])
            self.assertEqual(report["blocked"], ["release.plugin.expected"])
            self.assertEqual(report["blockedPrerequisites"], [])
        finally:
            temporary.cleanup()

    def test_rest_404_reports_missing_release_instead_of_generic_query_failure(self) -> None:
        evidence = PREFLIGHT.remote_error_evidence(
            PREFLIGHT.RemoteQueryError("gh: Not Found (HTTP 404)")
        )
        self.assertEqual(evidence["errorCode"], "release_not_found")

    def test_missing_cli_release_and_disabled_plugin_immutable_setting_block_preflight(self) -> None:
        root, temporary = self.fixture()
        try:
            def query(arguments: list[str]) -> dict:
                rendered = " ".join(arguments)
                if "jianying-draft/releases/tags/" in rendered:
                    raise PREFLIGHT.RemoteQueryError("release not found")
                if "jianying-draft-plugin/immutable-releases" in rendered:
                    return {"enabled": False}
                return self.ready_query(arguments)

            report = PREFLIGHT.build_report(root, query)
            self.assertFalse(report["prerequisitesReady"])
            self.assertFalse(report["releaseComplete"])
            self.assertIn("release.cli.expected", report["blocked"])
            self.assertIn("repository.plugin.immutable_releases", report["blocked"])
            self.assertEqual(report["blockedPrerequisites"], [
                "release.cli.expected",
                "repository.plugin.immutable_releases",
            ])
        finally:
            temporary.cleanup()

    def test_missing_tag_protection_blocks_each_repository(self) -> None:
        root, temporary = self.fixture()
        try:
            def query(arguments: list[str]) -> dict:
                if arguments[0] == "api" and "rulesets" in arguments[1]:
                    if PREFLIGHT.PLUGIN_REPOSITORY in arguments[1]:
                        return []
                    return PREFLIGHT.release_tag_ruleset_fixture()
                return self.ready_query(arguments)

            report = PREFLIGHT.build_report(root, query)
            self.assertFalse(report["prerequisitesReady"])
            self.assertIn(
                "repository.plugin.release_protection",
                report["blockedPrerequisites"],
            )
        finally:
            temporary.cleanup()

    def test_private_plan_unavailable_tag_ruleset_is_structured(self) -> None:
        root, temporary = self.fixture()
        try:
            def query(arguments: list[str]) -> dict:
                if arguments[0] == "api" and "rulesets" in arguments[1]:
                    raise PREFLIGHT.RemoteQueryError(
                        "gh: Upgrade to GitHub Pro or make this repository public "
                        "to enable this feature. (HTTP 403)"
                    )
                return self.ready_query(arguments)

            report = PREFLIGHT.build_report(root, query)
            item = next(
                check for check in report["checks"]
                if check["id"] == "repository.plugin.release_protection"
            )
            self.assertEqual(item["status"], "ready")
            self.assertEqual(
                item["evidence"]["strategy"],
                "immutable_release_with_tag_commit_rechecks",
            )
            self.assertEqual(
                item["evidence"]["rulesetQuery"]["errorCode"],
                "feature_unavailable_for_plan",
            )
            self.assertTrue(report["prerequisitesReady"])
        finally:
            temporary.cleanup()

    def test_private_plan_without_complete_equivalent_policy_stays_blocked(self) -> None:
        root, temporary = self.fixture()
        try:
            policy_path = root / "runtime/release-protection-policy.json"
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            policy["requiredChecks"]["afterPublishTagCommit"] = False
            policy_path.write_text(json.dumps(policy), encoding="utf-8")

            def query(arguments: list[str]) -> dict:
                if arguments[0] == "api" and "rulesets" in arguments[1]:
                    raise PREFLIGHT.RemoteQueryError(
                        "gh: Upgrade to GitHub Pro or make this repository public "
                        "to enable this feature. (HTTP 403)"
                    )
                return self.ready_query(arguments)

            report = PREFLIGHT.build_report(root, query)
            item = next(
                check for check in report["checks"]
                if check["id"] == "repository.plugin.release_protection"
            )
            self.assertEqual(item["status"], "blocked")
            self.assertEqual(
                item["evidence"]["errorCode"], "equivalent_policy_invalid"
            )
            self.assertFalse(report["prerequisitesReady"])
        finally:
            temporary.cleanup()

    def test_equivalent_policy_requires_final_post_publish_recheck(self) -> None:
        root, temporary = self.fixture()
        try:
            workflow = root / ".github/workflows/release-gate.yml"
            text = workflow.read_text(encoding="utf-8")
            last_plan = text.rfind("python3 scripts/release_publication_plan.py")
            workflow.write_text(text[:last_plan], encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "three tag commit rechecks"):
                PREFLIGHT.load_equivalent_release_policy(root)
        finally:
            temporary.cleanup()

    def test_inherited_ruleset_is_loaded_from_canonical_self_link(self) -> None:
        self_link = (
            "https://api.github.com/orgs/full-aigc-plugins/rulesets/42"
        )

        def query(arguments: list[str]) -> object:
            if arguments[1] == self_link:
                return PREFLIGHT.release_tag_ruleset_fixture()[0]
            return [{"id": 42, "_links": {"self": {"href": self_link}}}]

        details = PREFLIGHT.load_release_tag_rulesets(
            query, PREFLIGHT.PLUGIN_REPOSITORY
        )
        self.assertTrue(PREFLIGHT.release_tags_are_protected(details))


    def test_immutable_release_missing_one_required_asset_is_blocked(self) -> None:
        root, temporary = self.fixture()
        try:
            def query(arguments: list[str]) -> dict:
                evidence = self.ready_query(arguments)
                if "/releases/3/assets?" in arguments[1]:
                    evidence = evidence[:-1]
                return evidence

            report = PREFLIGHT.build_report(root, query)
            self.assertTrue(report["prerequisitesReady"])
            self.assertFalse(report["releaseComplete"])
            self.assertEqual(report["blocked"], ["release.plugin.expected"])
            self.assertIn(
                "jianying-draft-plugin-source.tar.gz",
                report["expected"]["plugin"]["assets"],
            )
        finally:
            temporary.cleanup()

    def test_release_asset_digest_or_canonical_url_drift_is_blocked(self) -> None:
        for mutate in (
            lambda asset: asset.update({"digest": None}),
            lambda asset: asset.update({"digest": "sha256:1234"}),
            lambda asset: asset.update({"size": 0}),
            lambda asset: asset.update({"state": "new"}),
            lambda asset: asset.update({"browser_download_url": "https://example.com/asset"}),
        ):
            root, temporary = self.fixture()
            try:
                def query(arguments: list[str], mutate=mutate) -> dict:
                    evidence = self.ready_query(arguments)
                    if "/releases/2/assets?" in arguments[1]:
                        mutate(evidence[0])
                    return evidence

                report = PREFLIGHT.build_report(root, query)
                self.assertFalse(report["prerequisitesReady"])
                self.assertIn("release.skills.expected", report["blocked"])
            finally:
                temporary.cleanup()


if __name__ == "__main__":
    unittest.main()
