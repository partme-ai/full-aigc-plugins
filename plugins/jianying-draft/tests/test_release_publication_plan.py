"""插件不可变 Release 的 Draft 恢复契约。"""

import hashlib
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "release_publication_plan", ROOT / "scripts" / "release_publication_plan.py"
)
PLAN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PLAN)
ATTESTATION_SPEC = importlib.util.spec_from_file_location(
    "verify_release_attestation", ROOT / "scripts" / "verify_release_attestation.py"
)
ATTESTATION = importlib.util.module_from_spec(ATTESTATION_SPEC)
ATTESTATION_SPEC.loader.exec_module(ATTESTATION)


class ReleasePublicationPlanTests(unittest.TestCase):
    def test_release_attestation_binds_commit_and_exact_assets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            asset = Path(temporary) / "plugin.tar.gz"
            asset.write_bytes(b"plugin")
            commit = "a" * 40
            evidence = {"verificationResult": {"statement": {
                "predicate": {"repository": "full-aigc-plugins/jianying-draft-plugin", "tag": "v0.17.2"},
                "subject": [
                    {"uri": "pkg:github/full-aigc-plugins/jianying-draft-plugin@v0.17.2", "digest": {"sha1": commit}},
                    {"name": asset.name, "digest": {"sha256": hashlib.sha256(b"plugin").hexdigest()}},
                ],
            }}}
            ATTESTATION.verify(evidence, "full-aigc-plugins/jianying-draft-plugin", "v0.17.2", commit, [asset])
            evidence["verificationResult"]["statement"]["subject"].append(
                {"name": "unexpected.json", "digest": {"sha256": "0" * 64}}
            )
            with self.assertRaisesRegex(ValueError, "asset set or digest differs"):
                ATTESTATION.verify(evidence, "full-aigc-plugins/jianying-draft-plugin", "v0.17.2", commit, [asset])

    def test_release_query_treats_only_explicit_http_404_as_absent(self) -> None:
        def missing(arguments, **_kwargs):
            if "--slurp" in arguments:
                return subprocess.CompletedProcess([], 0, "[]\n", "")
            return subprocess.CompletedProcess(
                [], 1, '{"message":"Not Found","status":"404"}\n',
                "gh: Not Found (HTTP 404)\n",
            )

        self.assertIsNone(PLAN.query_release_metadata(
            "full-aigc-plugins/jianying-draft-plugin", "v0.17.2", missing,
        ))

        def throttled(*_args, **_kwargs):
            return subprocess.CompletedProcess(
                [], 1, '{"message":"rate limit","status":"429"}\n',
                "gh: rate limit (HTTP 429)\n",
            )

        with self.assertRaisesRegex(ValueError, "cannot query GitHub release"):
            PLAN.query_release_metadata(
                "full-aigc-plugins/jianying-draft-plugin", "v0.17.2", throttled,
            )

    def test_release_query_recovers_tagged_draft_from_release_list(self) -> None:
        def draft(arguments, **_kwargs):
            if "--slurp" in arguments:
                return subprocess.CompletedProcess([], 0, '''[[{
                  "tag_name":"v0.17.2","draft":true,"prerelease":false,
                  "immutable":false,"assets":[]
                }]]''', "")
            return subprocess.CompletedProcess(
                [], 1, '{"message":"Not Found","status":"404"}\n', "",
            )

        metadata = PLAN.query_release_metadata(
            "full-aigc-plugins/jianying-draft-plugin", "v0.17.2", draft,
        )
        self.assertTrue(metadata["isDraft"])
        self.assertEqual(metadata["assets"], [])

    def test_lightweight_remote_tag_must_equal_expected_commit(self) -> None:
        release_ref = "v0.17.2"
        commit = "a" * 40
        output = f"{commit}\trefs/tags/{release_ref}\n"
        self.assertEqual(
            PLAN.verify_remote_tag_output(output, release_ref, commit), commit
        )
        with self.assertRaisesRegex(ValueError, "remote tag commit differs"):
            PLAN.verify_remote_tag_output(output, release_ref, "c" * 40)

    def test_partial_draft_only_uploads_missing_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "plugin.tar.gz"
            report = root / "report.json"
            archive.write_bytes(b"archive")
            report.write_bytes(b"report")
            metadata = {
                "tagName": "v0.17.2",
                "isDraft": True,
                "isPrerelease": False,
                "isImmutable": False,
                "assets": [PLAN.describe_expected(archive)],
            }
            plan = PLAN.plan_publication(
                metadata, [archive, report], "v0.17.2"
            )
            self.assertEqual(plan["action"], "resume_draft")
            self.assertEqual(plan["missing"], [str(report)])

    def test_extra_draft_evidence_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "plugin.tar.gz"
            archive.write_bytes(b"archive")
            extra = PLAN.describe_expected(archive)
            extra["name"] = "stale.json"
            with self.assertRaisesRegex(ValueError, "unexpected asset"):
                PLAN.plan_publication(
                    {
                        "tagName": "v0.17.2",
                        "isDraft": True,
                        "isPrerelease": False,
                        "isImmutable": False,
                        "assets": [extra],
                    },
                    [archive],
                    "v0.17.2",
                )


if __name__ == "__main__":
    unittest.main()
