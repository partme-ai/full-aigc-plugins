"""Distribution contract tests for partme-minimax-design."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys_path = ROOT / "scripts"
import sys  # noqa: E402

sys.path.insert(0, str(sys_path))

import validate_distribution  # noqa: E402


class DistributionTests(unittest.TestCase):
    def test_validator_accepts_distribution(self) -> None:
        self.assertEqual(validate_distribution.main(), 0)

    def test_manifest_identity(self) -> None:
        import json
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        self.assertEqual(manifest["name"], "minimax-design")
        self.assertEqual(manifest["repository"],
                         "https://github.com/full-aigc-plugins/minimax-design-plugin")

    def test_zcode_and_kimi_versions_match(self) -> None:
        import json
        codex = json.loads((ROOT / ".codex-plugin/plugin.json").read_text())
        base_version = codex["version"].split("+", 1)[0]
        for rel in (".zcode-plugin/plugin.json", "kimi.plugin.json"):
            m = json.loads((ROOT / rel).read_text())
            self.assertEqual(m["name"], codex["name"], rel)
            self.assertEqual(m["version"], base_version, rel)

    def test_vendored_skills_match_lock(self) -> None:
        import json
        lock = json.loads((ROOT / "skills.lock.json").read_text())
        for source in lock["sources"]:
            for name, digest in source["sha256"].items():
                self.assertTrue((ROOT / "skills" / name / "SKILL.md").is_file(),
                                f"missing vendored skill {name}")


class CapabilitySurfaceTests(unittest.TestCase):
    def test_commands_have_frontmatter_and_description(self) -> None:
        import json
        d = json.loads((ROOT / "kimi.plugin.json").read_text())
        self.assertEqual(d.get("commands"), "./commands/")
        self.assertEqual(d.get("sessionStart"), {"skill": "minimax-design-use"})

    def test_agent_has_required_frontmatter(self) -> None:
        text = (ROOT / "agents" / "minimax-prompt-writer.md").read_text()
        self.assertIn("name: minimax-prompt-writer", text)
        self.assertIn("description:", text)
        self.assertIn("tools: [Read, Grep, Glob]", text)

    def test_zcode_userconfig_declares_sensitive_key(self) -> None:
        import json
        d = json.loads((ROOT / ".zcode-plugin/plugin.json").read_text())
        raw = d.get("userConfig", {})
        uc = raw if isinstance(raw, dict) else {item["key"]: item for item in raw}
        self.assertTrue(uc["MINIMAX_API_KEY"].get("sensitive"))
        self.assertIn(d.get("commands"), ("./commands", "./commands/"))
        self.assertIn(d.get("agents"), ("./agents", "./agents/"))
        self.assertNotIn(
            "hooks",
            d,
            "ZCode auto-discovers hooks/hooks.json; an explicit pointer loads hooks twice",
        )

    def test_managed_and_plugin_local_skill_counts(self) -> None:
        import json
        lock = json.loads((ROOT / "skills.lock.json").read_text())
        local = json.loads((ROOT / "plugin-local-skills.json").read_text())
        managed = {name for source in lock["sources"] for name in source["skills"]}
        plugin_local = set(local["skills"])
        actual = {
            path.name
            for path in (ROOT / "skills").iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        }
        self.assertEqual(12, len(managed))
        self.assertEqual(
            {"minimax-design-use", "minimax-video-generation"},
            plugin_local,
        )
        self.assertEqual(managed | plugin_local, actual)


if __name__ == "__main__":
    unittest.main()
