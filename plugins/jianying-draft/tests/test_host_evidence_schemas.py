"""三宿主验收 JSON Schema 与运行时代码常量一致性测试。"""

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location(
    "host_acceptance", ROOT / "scripts" / "host_acceptance.py"
)
HOST_ACCEPTANCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HOST_ACCEPTANCE)


class HostEvidenceSchemaTests(unittest.TestCase):
    REQUIRED_PRODUCTION_CHECKS = {
        "freshInstall",
        "doctor",
        "skillDiscovery",
        "singleSkillInstall",
        "categoryDiscovery",
        "categoryRouting",
        "selectionExplanation",
        "approval",
        "simpleJob",
        "stop",
        "recovery",
        "evidenceDisplay",
        "nativeExportApproval",
    }

    def load(self, name: str) -> dict:
        return json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))

    def test_observation_and_evidence_schemas_match_runtime_contract(self) -> None:
        observation = self.load("host-observation-v2.schema.json")
        evidence = self.load("host-run-evidence-v2.schema.json")
        self.assertEqual(observation["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(
            observation["properties"]["schema"]["const"],
            "jianying-host-observation/v2",
        )
        self.assertEqual(
            evidence["properties"]["schema"]["const"], HOST_ACCEPTANCE.EVIDENCE_SCHEMA
        )
        self.assertEqual(
            set(observation["properties"]["host"]["enum"]),
            HOST_ACCEPTANCE.EXPECTED_HOSTS,
        )
        self.assertEqual(
            set(observation["properties"]["checks"]["required"]),
            HOST_ACCEPTANCE.REQUIRED_CHECKS,
        )
        self.assertEqual(
            HOST_ACCEPTANCE.REQUIRED_CHECKS,
            self.REQUIRED_PRODUCTION_CHECKS,
        )
        for name in HOST_ACCEPTANCE.REQUIRED_CHECKS:
            self.assertEqual(
                observation["properties"]["checks"]["properties"][name], {"const": True}
            )
        self.assertIn("jobInputSha256", evidence["required"])
        self.assertIn("resultSemanticSha256", evidence["required"])
        self.assertIn("checkEvidence", observation["required"])
        self.assertIn("checkEvidence", evidence["required"])
        self.assertEqual(
            set(observation["properties"]["checkEvidence"]["required"]),
            HOST_ACCEPTANCE.REQUIRED_CHECKS,
        )
        self.assertEqual(
            set(evidence["properties"]["checkEvidence"]["required"]),
            HOST_ACCEPTANCE.REQUIRED_CHECKS,
        )

    def test_published_v1_schemas_remain_unchanged_and_are_not_current(self) -> None:
        observation = self.load("host-observation-v1.schema.json")
        evidence = self.load("host-run-evidence-v1.schema.json")
        self.assertEqual(
            observation["properties"]["schema"]["const"],
            "jianying-host-observation/v1",
        )
        self.assertEqual(
            evidence["properties"]["schema"]["const"],
            "jianying-host-run-evidence/v1",
        )
        self.assertNotIn("checkEvidence", observation["required"])
        self.assertNotIn("checkEvidence", evidence["required"])

    def test_summary_schema_covers_current_pending_or_exact_three_host_evidence(self) -> None:
        summary = self.load("host-release-acceptance-v1.schema.json")
        self.assertEqual(
            summary["properties"]["schema"]["const"], HOST_ACCEPTANCE.SUMMARY_SCHEMA
        )
        rendered = json.loads(
            (ROOT / "runtime" / "host-acceptance.json").read_text(encoding="utf-8")
        )
        self.assertEqual(rendered["schema"], HOST_ACCEPTANCE.SUMMARY_SCHEMA)
        self.assertIn(rendered["status"], {"pending", "passed"})
        pending_rule = next(
            rule["then"] for rule in summary["allOf"]
            if rule["if"]["properties"]["status"].get("const") == "pending"
        )
        passed_rule = next(
            rule["then"] for rule in summary["allOf"]
            if rule["if"]["properties"]["status"].get("const") == "passed"
        )
        self.assertEqual(pending_rule["properties"]["hosts"]["maxItems"], 0)
        self.assertEqual(passed_rule["properties"]["hosts"]["minItems"], 3)
        self.assertEqual(passed_rule["properties"]["hosts"]["maxItems"], 3)
        if rendered["status"] == "pending":
            self.assertEqual(rendered["hosts"], [])
        else:
            self.assertEqual(
                {entry["host"] for entry in rendered["hosts"]},
                HOST_ACCEPTANCE.EXPECTED_HOSTS,
            )
            HOST_ACCEPTANCE.validate_acceptance(
                ROOT,
                rendered["pluginVersion"],
                rendered["cliVersion"],
                rendered["skillsVersion"],
            )


if __name__ == "__main__":
    unittest.main()
