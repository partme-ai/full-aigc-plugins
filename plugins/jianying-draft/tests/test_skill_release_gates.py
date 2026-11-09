"""技能发布锁的负向门禁测试。"""

import copy
import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

validator_spec = importlib.util.spec_from_file_location(
    "validate_distribution", ROOT / "scripts" / "validate_distribution.py"
)
validator = importlib.util.module_from_spec(validator_spec)
validator_spec.loader.exec_module(validator)

vendor_spec = importlib.util.spec_from_file_location(
    "skill_vendor", ROOT / "scripts" / "vendor" / "skill_vendor.py"
)
skill_vendor = importlib.util.module_from_spec(vendor_spec)
vendor_spec.loader.exec_module(skill_vendor)


class SkillReleaseGateTests(unittest.TestCase):
    PANEL_SKILLS = {
        "jianying-draft-media",
        "jianying-draft-audio",
        "jianying-draft-text",
        "jianying-draft-stickers",
        "jianying-draft-effects",
        "jianying-draft-transitions",
        "jianying-draft-subtitles",
        "jianying-draft-smart-package",
        "jianying-draft-filters",
        "jianying-draft-adjustments",
        "jianying-draft-templates",
        "jianying-draft-digital-human",
        "jianying-draft-editing-console",
    }

    def setUp(self) -> None:
        self.skills_lock = json.loads((ROOT / "skills.lock.json").read_text(encoding="utf-8"))
        self.cli_lock = json.loads(
            (ROOT / "runtime" / "jianying-cli.lock.json").read_text(encoding="utf-8")
        )

    def test_cli_older_than_skill_contract_is_rejected(self) -> None:
        incompatible = copy.deepcopy(self.cli_lock)
        incompatible["minimumVersion"] = "1.5.0"
        with self.assertRaisesRegex(ValueError, "older than skill minimum"):
            validator.validate_skill_cli_compatibility(self.skills_lock, incompatible)

    def test_missing_cli_capability_is_rejected(self) -> None:
        incompatible = copy.deepcopy(self.skills_lock)
        incompatible["sources"][0]["minimumCapabilities"].remove("job.run")
        with self.assertRaisesRegex(ValueError, "skill lock misses CLI capabilities"):
            validator.validate_skill_cli_compatibility(incompatible, self.cli_lock)

    def test_missing_skill_and_digest_drift_fail_offline_vendor_check(self) -> None:
        source = copy.deepcopy(self.skills_lock["sources"][0])
        source["skills"] = ["fixture-skill"]
        source["sha256"] = {"fixture-skill": "0" * 64}
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "skills").mkdir()
            lock = root / "skills.lock.json"
            lock.write_text(json.dumps({"version": 1, "sources": [source]}), encoding="utf-8")
            self.assertEqual(skill_vendor.cmd_check(lock, offline=True, overrides={}), 1)

            skill = root / "skills" / "fixture-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: fixture-skill\n---\n", encoding="utf-8")
            self.assertEqual(skill_vendor.cmd_check(lock, offline=True, overrides={}), 1)

    def test_development_locks_cannot_pass_release_readiness(self) -> None:
        development_cli_lock = copy.deepcopy(self.cli_lock)
        development_cli_lock["artifacts"] = {}
        with self.assertRaisesRegex(ValueError, "three checksum-pinned CLI artifacts"):
            validator.validate_release_readiness(self.skills_lock, development_cli_lock)

    def test_release_readiness_requires_immutable_skill_manifest(self) -> None:
        artifacts = {}
        for platform in ("darwin-arm64", "darwin-x64", "win32-x64"):
            artifacts[platform] = {
                "url": (
                    "https://github.com/full-aigc-plugins/jianying-draft/"
                    f"releases/download/v1.6.0/{platform}.tar.gz"
                ),
                "archiveSha256": "1" * 64,
                "binarySha256": "2" * 64,
                "capabilityManifestSha256": "3" * 64,
                "sbomSha256": "4" * 64,
            }
        cli_lock = copy.deepcopy(self.cli_lock)
        cli_lock["artifacts"] = artifacts
        cli_lock["resolvedVersion"] = "1.6.0"
        cli_lock["releaseRef"] = "v1.6.0"
        cli_lock["repository"] = "full-aigc-plugins/jianying-draft"
        cli_lock["sourceCommit"] = "a" * 40
        skills_lock = copy.deepcopy(self.skills_lock)
        source = skills_lock["sources"][0]
        source.pop("releaseVersion", None)
        source.pop("manifestSchema", None)
        source.pop("manifestSha256", None)
        source["ref"] = "v1.2.0"
        with self.assertRaisesRegex(ValueError, "immutable jianying-skills manifest lock"):
            validator.validate_release_readiness(skills_lock, cli_lock)

    def test_locked_release_exposes_all_panel_skills(self) -> None:
        source = self.skills_lock["sources"][0]
        # 不钉死版本号：同步任务会把锁推到新的上游版本，
        # 这里只要求 ref 与 releaseVersion 一致且合法。
        self.assertRegex(source["releaseVersion"], r"^\d+\.\d+\.\d+$")
        self.assertEqual(source["ref"], f"v{source['releaseVersion']}")
        # 入口技能 jianying-draft-use 现在由插件自己拥有，不在上游包里
        local = set(self.skills_lock.get("localSkills", []))
        self.assertEqual(len(source["skills"]) + len(local), 24)
        self.assertEqual(local, {"jianying-draft-use"})
        self.assertTrue(self.PANEL_SKILLS.issubset(set(source["skills"])))

    def test_panel_workflows_define_semantic_routes_not_coordinates(self) -> None:
        operation_ids: set[str] = set()
        for skill_name in self.PANEL_SKILLS:
            workflow = ROOT / "skills" / skill_name / "references" / "workflow.md"
            self.assertTrue(workflow.is_file(), f"{skill_name} must define a workflow")
            text = workflow.read_text(encoding="utf-8")
            self.assertIn("| 语义动作 |", text, skill_name)
            self.assertIn("执行路由", text, skill_name)
            self.assertIn("验证", text, skill_name)
            self.assertIn("恢复", text, skill_name)
            self.assertNotRegex(text, r"\b(?:x|y)\s*[:=]\s*\d+", skill_name)
            ids = re.findall(r"\| `([a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*){2,})` \|", text)
            self.assertGreaterEqual(len(ids), 6, skill_name)
            for operation_id in ids:
                self.assertNotIn(operation_id, operation_ids, operation_id)
                operation_ids.add(operation_id)
        self.assertGreaterEqual(len(operation_ids), 100)


if __name__ == "__main__":
    unittest.main()
