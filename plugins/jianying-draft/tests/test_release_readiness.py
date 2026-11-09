"""正式发布 readiness 报告测试。"""

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location(
    "release_readiness", ROOT / "scripts" / "release_readiness.py"
)
READINESS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(READINESS)


class ReleaseReadinessTests(unittest.TestCase):
    def test_current_checkout_readiness_matches_formal_host_acceptance_state(self) -> None:
        report = READINESS.build_report(ROOT)
        acceptance = json.loads(
            (ROOT / "runtime" / "host-acceptance.json").read_text(encoding="utf-8")
        )
        self.assertIn(acceptance["status"], {"pending", "passed"})
        blocked = set(report["blocked"])
        codex = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        cli = json.loads((ROOT / "runtime/jianying-cli.lock.json").read_text(encoding="utf-8"))
        skills = json.loads((ROOT / "skills.lock.json").read_text(encoding="utf-8"))
        expected_versions = (
            codex["version"].split("+")[0], cli["resolvedVersion"],
            skills["sources"][0]["releaseVersion"],
        )
        accepted_versions = (
            acceptance["pluginVersion"], acceptance["cliVersion"],
            acceptance["skillsVersion"],
        )
        host_check = next(
            check for check in report["checks"]
            if check["id"] == "hosts.release_acceptance"
        )
        if accepted_versions != expected_versions:
            self.assertFalse(report["ready"])
            self.assertFalse(report["production_ready"])
            self.assertEqual(blocked, {"hosts.release_acceptance"})
            self.assertEqual(host_check["status"], "blocked")
            self.assertEqual(host_check["evidence"]["acceptance_state"], "invalid")
        elif acceptance["status"] == "passed":
            self.assertTrue(report["ready"])
            self.assertTrue(report["production_ready"])
            self.assertEqual(blocked, set())
        else:
            self.assertTrue(report["ready"])
            self.assertFalse(report["production_ready"])
            self.assertEqual(blocked, set())
            self.assertEqual(host_check["status"], "ready")
            self.assertEqual(host_check["evidence"]["acceptance_state"], "pending")
        self.assertNotIn("cli.platform_artifacts", blocked)
        self.assertNotIn("cli.immutable_identity", blocked)
        self.assertNotIn("cli.artifact_integrity", blocked)
        self.assertNotIn("skills.immutable_release", blocked)
        self.assertNotIn("skills.content_digests", blocked)
        self.assertNotIn("runtime.legacy_engines_removed", blocked)
        self.assertNotIn("runtime.release_surface_rust_only", blocked)
        self.assertNotIn("distribution.legal_materials", blocked)
        self.assertNotIn("matrix.cli_skill_compatibility", blocked)

    def test_report_is_machine_serializable_and_contains_unique_checks(self) -> None:
        report = READINESS.build_report(ROOT)
        reparsed = json.loads(json.dumps(report))
        identifiers = [check["id"] for check in reparsed["checks"]]
        self.assertEqual(len(identifiers), len(set(identifiers)))
        self.assertEqual(reparsed["schema"], "jianying-plugin-release-readiness/v1")

    def test_complete_release_fixture_is_ready(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for directory in (
                "runtime", "skills/fixture-skill", ".codex-plugin", ".zcode-plugin",
                ".agents/plugins", "commands", "hooks", "scripts",
            ):
                (root / directory).mkdir(parents=True, exist_ok=True)
            (root / "skills/fixture-skill/SKILL.md").write_text(
                "---\nname: fixture-skill\ndescription: fixture\n---\n",
                encoding="utf-8",
            )
            skill_digest = READINESS.hash_skill_dir(root / "skills/fixture-skill")
            artifacts = {}
            for platform in sorted(READINESS.EXPECTED_PLATFORMS):
                archive = f"jianying-cli-1.6.0-{platform}.zip"
                artifacts[platform] = {
                    "url": (
                        "https://github.com/full-aigc-plugins/jianying-draft/"
                        f"releases/download/v1.6.0/{archive}"
                    ),
                    "archiveSha256": "1" * 64,
                    "binarySha256": "2" * 64,
                    "capabilityManifestSha256": "3" * 64,
                    "sbomSha256": "4" * 64,
                }
            (root / "runtime/jianying-cli.lock.json").write_text(json.dumps({
                "minimumVersion": "1.6.0",
                "resolvedVersion": "1.6.0",
                "releaseRef": "v1.6.0",
                "repository": "full-aigc-plugins/jianying-draft",
                "sourceCommit": "a" * 40,
                "requiredCapabilities": ["job.run"],
                "artifacts": artifacts,
            }), encoding="utf-8")
            (root / "skills.lock.json").write_text(json.dumps({
                "sources": [{
                    "package": "jianying-skills",
                    "repo": "https://github.com/full-aigc-skills/jianying-skills.git",
                    "releaseVersion": "2.0.3",
                    "ref": "v2.0.3",
                    "sha": "b" * 40,
                    "manifestSchema": "jianying-skills-manifest/v1",
                    "manifestSha256": "5" * 64,
                    "minimumCliVersion": "1.6.0",
                    "minimumCapabilities": ["job.run"],
                    "skills": ["fixture-skill"],
                    "sha256": {"fixture-skill": skill_digest},
                }],
            }), encoding="utf-8")
            manifests = {
                ".codex-plugin/plugin.json": {"version": "0.17.1+codex.20260919"},
                ".zcode-plugin/plugin.json": {"version": "0.17.1+codex.20260919"},
                "kimi.plugin.json": {"version": "0.17.1"},
                ".agents/plugins/marketplace.json": {"plugins": [{"version": "0.17.1"}]},
            }
            for relative, payload in manifests.items():
                (root / relative).write_text(json.dumps(payload), encoding="utf-8")
            for legal in READINESS.distribution.LEGAL:
                (root / legal).write_text("fixture\n", encoding="utf-8")

            evidence_entries = []
            (root / "runtime/host-evidence").mkdir()
            for host in ("codex", "zcode", "kimi"):
                job_input = {"schema": "jianying-job/v2", "operation": "create"}
                semantic_result = {"operation": "create", "verificationOk": True}
                check_evidence = {}
                for name in READINESS.host_acceptance.REQUIRED_CHECKS:
                    artifact = {"check": name, "host": host, "outcome": "passed"}
                    check_evidence[name] = {
                        "kind": "host_command",
                        "observedAt": "2026-09-20T12:00:00Z",
                        "artifact": artifact,
                        "artifactSha256": READINESS.host_acceptance.canonical_sha256(
                            artifact
                        ),
                    }
                evidence_path = root / f"runtime/host-evidence/{host}.json"
                evidence_path.write_text(json.dumps({
                    "schema": "jianying-host-run-evidence/v2",
                    "host": host,
                    "evidenceLevel": "real_host",
                    "pluginVersion": "0.17.1",
                    "cliVersion": "1.6.0",
                    "skillsVersion": "2.0.3",
                    "jobSchema": "jianying-job/v2",
                    "jobInput": job_input,
                    "semanticResult": semantic_result,
                    "jobInputSha256": READINESS.host_acceptance.canonical_sha256(job_input),
                    "resultSemanticSha256": READINESS.host_acceptance.canonical_sha256(
                        semantic_result
                    ),
                    "executedAt": "2026-09-20T12:00:00Z",
                    "checks": {
                        name: True
                        for name in READINESS.host_acceptance.REQUIRED_CHECKS
                    },
                    "checkEvidence": check_evidence,
                }), encoding="utf-8")
                evidence_entries.append({
                    "host": host,
                    "evidencePath": f"runtime/host-evidence/{host}.json",
                    "evidenceSha256": hashlib.sha256(evidence_path.read_bytes()).hexdigest(),
                })
            (root / "runtime/host-acceptance.json").write_text(json.dumps({
                "schema": "jianying-host-release-acceptance/v1",
                "status": "passed",
                "pluginVersion": "0.17.1",
                "cliVersion": "1.6.0",
                "skillsVersion": "2.0.3",
                "jobSchema": "jianying-job/v2",
                "hosts": evidence_entries,
            }), encoding="utf-8")

            report = READINESS.build_report(root)
            self.assertTrue(report["ready"], report["blocked"])
            self.assertTrue(report["production_ready"])
            self.assertEqual(report["blocked"], [])

            (root / "docs").mkdir()
            (root / "docs" / "runbook.md").write_text(
                "Run `python3 scripts/jydraft_run.py job.json`.\n",
                encoding="utf-8",
            )
            report = READINESS.build_report(root)
            self.assertIn("runtime.release_surface_rust_only", report["blocked"])
            surface = next(
                check for check in report["checks"]
                if check["id"] == "runtime.release_surface_rust_only"
            )
            self.assertTrue(any("docs/runbook.md" in item for item in surface["evidence"]))


if __name__ == "__main__":
    unittest.main()
