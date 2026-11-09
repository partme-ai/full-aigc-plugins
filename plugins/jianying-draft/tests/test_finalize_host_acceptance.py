"""三宿主证据汇总锁原子生成测试。"""

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RECORDER = load_module("record_host_acceptance")
FINALIZER = load_module("finalize_host_acceptance")
VALIDATOR = load_module("host_acceptance")


class FinalizeHostAcceptanceTests(unittest.TestCase):
    def check_evidence(self, host: str) -> dict:
        result = {}
        for name in VALIDATOR.REQUIRED_CHECKS:
            artifact = {"check": name, "host": host, "outcome": "passed"}
            result[name] = {
                "kind": "host_command",
                "observedAt": "2026-09-20T12:00:00Z",
                "artifact": artifact,
                "artifactSha256": VALIDATOR.canonical_sha256(artifact),
            }
        return result

    def write_evidence(self, root: Path, *, split_semantics: bool = False) -> None:
        for host in ("codex", "zcode", "kimi"):
            observation = {
                "schema": "jianying-host-observation/v2",
                "host": host,
                "pluginVersion": "0.17.2",
                "cliVersion": "1.6.0",
                "skillsVersion": "2.0.3",
                "jobSchema": "jianying-job/v2",
                "executedAt": "2026-09-20T12:00:00Z",
                "checks": {name: True for name in VALIDATOR.REQUIRED_CHECKS},
                "checkEvidence": self.check_evidence(host),
                "jobInput": {"schema": "jianying-job/v2", "name": "same-job"},
                "semanticResult": {
                    "operation": "create",
                    "verificationOk": not (split_semantics and host == "kimi"),
                },
            }
            RECORDER.record_observation(
                observation, root / f"runtime/host-evidence/{host}.json"
            )

    def test_finalize_validates_then_atomically_writes_passed_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_evidence(root)
            summary = FINALIZER.finalize_acceptance(root, "0.17.2", "1.6.0", "2.0.3")
            self.assertEqual(summary["status"], "passed")
            self.assertEqual(len(summary["hosts"]), 3)
            self.assertEqual(
                summary,
                json.loads((root / "runtime/host-acceptance.json").read_text(encoding="utf-8")),
            )
            result = VALIDATOR.validate_acceptance(root, "0.17.2", "1.6.0", "2.0.3")
            self.assertEqual(result["hosts"], ["codex", "kimi", "zcode"])

    def test_semantic_drift_does_not_replace_pending_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.write_evidence(root, split_semantics=True)
            summary_path = root / "runtime/host-acceptance.json"
            pending = {"schema": VALIDATOR.SUMMARY_SCHEMA, "status": "pending"}
            summary_path.write_text(json.dumps(pending), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "semantic result"):
                FINALIZER.finalize_acceptance(root, "0.17.2", "1.6.0", "2.0.3")
            self.assertEqual(pending, json.loads(summary_path.read_text(encoding="utf-8")))


if __name__ == "__main__":
    unittest.main()
