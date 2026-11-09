"""真实宿主 observation 到验收证据的标准记录器测试。"""

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location(
    "record_host_acceptance", ROOT / "scripts" / "record_host_acceptance.py"
)
RECORDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RECORDER)


class RecordHostAcceptanceTests(unittest.TestCase):
    def check_evidence(self) -> dict:
        evidence = {}
        for name in RECORDER.host_acceptance.REQUIRED_CHECKS:
            artifact = {"check": name, "host": "codex", "outcome": "passed"}
            evidence[name] = {
                "kind": "host_command",
                "observedAt": "2026-09-20T12:00:00Z",
                "artifact": artifact,
                "artifactSha256": RECORDER.host_acceptance.canonical_sha256(artifact),
            }
        return evidence

    def observation(self) -> dict:
        return {
            "schema": "jianying-host-observation/v2",
            "host": "codex",
            "pluginVersion": "0.17.2",
            "cliVersion": "1.6.0",
            "skillsVersion": "2.0.3",
            "jobSchema": "jianying-job/v2",
            "executedAt": "2026-09-20T12:00:00Z",
            "checks": {
                name: True for name in RECORDER.host_acceptance.REQUIRED_CHECKS
            },
            "checkEvidence": self.check_evidence(),
            "jobInput": {"schema": "jianying-job/v2", "name": "same-job"},
            "semanticResult": {"operation": "create", "verificationOk": True},
        }

    def test_record_computes_canonical_digests(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "codex.json"
            evidence = RECORDER.record_observation(self.observation(), output)
            self.assertEqual(evidence, json.loads(output.read_text(encoding="utf-8")))
            self.assertEqual(evidence["evidenceLevel"], "real_host")
            self.assertEqual(
                evidence["jobInputSha256"],
                RECORDER.host_acceptance.canonical_sha256(evidence["jobInput"]),
            )
            self.assertEqual(
                evidence["resultSemanticSha256"],
                RECORDER.host_acceptance.canonical_sha256(evidence["semanticResult"]),
            )

    def test_record_rejects_incomplete_checks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            observation = self.observation()
            observation["checks"]["recovery"] = False
            with self.assertRaisesRegex(ValueError, "checks"):
                RECORDER.record_observation(observation, Path(temporary) / "codex.json")

    def test_record_rejects_boolean_only_checks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            observation = self.observation()
            del observation["checkEvidence"]
            with self.assertRaisesRegex(ValueError, "checkEvidence"):
                RECORDER.record_observation(observation, Path(temporary) / "codex.json")

    def test_record_rejects_tampered_check_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            observation = self.observation()
            observation["checkEvidence"]["doctor"]["artifact"]["outcome"] = "failed"
            with self.assertRaisesRegex(ValueError, "doctor.*digest"):
                RECORDER.record_observation(observation, Path(temporary) / "codex.json")


if __name__ == "__main__":
    unittest.main()
