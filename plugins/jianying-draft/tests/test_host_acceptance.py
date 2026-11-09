"""三宿主真实发布验收证据门禁测试。"""

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "host_acceptance", ROOT / "scripts" / "host_acceptance.py"
)
HOST_ACCEPTANCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HOST_ACCEPTANCE)


class HostAcceptanceTests(unittest.TestCase):
    def check_evidence(self, host: str) -> dict:
        result = {}
        for name in HOST_ACCEPTANCE.REQUIRED_CHECKS:
            artifact = {"check": name, "host": host, "outcome": "passed"}
            result[name] = {
                "kind": "host_command",
                "observedAt": "2026-09-20T12:00:00Z",
                "artifact": artifact,
                "artifactSha256": HOST_ACCEPTANCE.canonical_sha256(artifact),
            }
        return result

    def write_fixture(self, root: Path, *, split_semantics: bool = False) -> None:
        evidence_root = root / "runtime" / "host-evidence"
        evidence_root.mkdir(parents=True)
        entries = []
        for index, host in enumerate(("codex", "zcode", "kimi")):
            job_input = {"schema": "jianying-job/v2", "operation": "create", "name": "host-gate"}
            semantic_result = {
                "operation": "create",
                "verificationOk": not (split_semantics and index == 2),
                "evidenceLevel": "editable_draft",
            }
            payload = {
                "schema": "jianying-host-run-evidence/v2",
                "host": host,
                "evidenceLevel": "real_host",
                "pluginVersion": "0.17.2",
                "cliVersion": "1.6.0",
                "skillsVersion": "2.0.3",
                "jobSchema": "jianying-job/v2",
                "jobInput": job_input,
                "semanticResult": semantic_result,
                "jobInputSha256": HOST_ACCEPTANCE.canonical_sha256(job_input),
                "resultSemanticSha256": HOST_ACCEPTANCE.canonical_sha256(semantic_result),
                "executedAt": "2026-09-20T12:00:00Z",
                "checks": {name: True for name in HOST_ACCEPTANCE.REQUIRED_CHECKS},
                "checkEvidence": self.check_evidence(host),
            }
            path = evidence_root / f"{host}.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            entries.append({
                "host": host,
                "evidencePath": f"runtime/host-evidence/{host}.json",
                "evidenceSha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            })
        (root / "runtime" / "host-acceptance.json").write_text(json.dumps({
            "schema": "jianying-host-release-acceptance/v1",
            "status": "passed",
            "pluginVersion": "0.17.2",
            "cliVersion": "1.6.0",
            "skillsVersion": "2.0.3",
            "jobSchema": "jianying-job/v2",
            "hosts": entries,
        }), encoding="utf-8")

    def test_complete_real_host_evidence_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_fixture(root)
            result = HOST_ACCEPTANCE.validate_acceptance(
                root, "0.17.2", "1.6.0", "2.0.3"
            )
            self.assertEqual(result["hosts"], ["codex", "kimi", "zcode"])
            self.assertRegex(result["job_input_sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(result["result_semantic_sha256"], r"^[0-9a-f]{64}$")

    def test_tampered_evidence_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_fixture(root)
            path = root / "runtime/host-evidence/codex.json"
            path.write_text("{}", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "digest"):
                HOST_ACCEPTANCE.validate_acceptance(
                    root, "0.17.2", "1.6.0", "2.0.3"
                )

    def test_cross_host_semantic_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_fixture(root, split_semantics=True)
            with self.assertRaisesRegex(ValueError, "semantic result"):
                HOST_ACCEPTANCE.validate_acceptance(
                    root, "0.17.2", "1.6.0", "2.0.3"
                )

    def test_release_identity_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_fixture(root)
            summary_path = root / "runtime/host-acceptance.json"
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            summary["cliVersion"] = "1.7.0"
            summary_path.write_text(json.dumps(summary), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "cliVersion"):
                HOST_ACCEPTANCE.validate_acceptance(
                    root, "0.17.2", "1.6.0", "2.0.3"
                )

    def test_tampered_embedded_check_evidence_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_fixture(root)
            path = root / "runtime/host-evidence/codex.json"
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["checkEvidence"]["doctor"]["artifact"]["outcome"] = "failed"
            path.write_text(json.dumps(payload), encoding="utf-8")
            summary_path = root / "runtime/host-acceptance.json"
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            for entry in summary["hosts"]:
                if entry["host"] == "codex":
                    entry["evidenceSha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
            summary_path.write_text(json.dumps(summary), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "doctor.*digest"):
                HOST_ACCEPTANCE.validate_acceptance(
                    root, "0.17.2", "1.6.0", "2.0.3"
                )


if __name__ == "__main__":
    unittest.main()
