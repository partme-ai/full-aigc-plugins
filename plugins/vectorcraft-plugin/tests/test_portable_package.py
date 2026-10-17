"""The distributable Agent Plugin must not silently include development runtime code."""

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "scripts" / "verify_portable_package.py"


class PortablePackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.package = self.base / "vectorcraft"
        skill = self.package / "skills" / "vectorcraft-use"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: vectorcraft-use\ndescription: Test skill.\n---\n")
        (self.package / "plugin.json").write_text(json.dumps({
            "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
            "name": "vectorcraft",
        }))
        (self.package / "LICENSE").write_text("Apache-2.0")
        payload = (skill / "SKILL.md").read_bytes()
        digest = hashlib.sha256(("SKILL.md\0" + hashlib.sha256(payload).hexdigest() + "\n").encode()).hexdigest()
        self.lock = self.base / "skills.lock.json"
        self.lock.write_text(json.dumps({"sources": [{"skills": ["vectorcraft-use"], "sha256": {"vectorcraft-use": digest}}]}))

    def verify(self):
        return subprocess.run(
            [sys.executable, "-I", "-B", str(VERIFY), str(self.package), str(self.lock)],
            capture_output=True,
            text=True,
        )

    def test_minimal_locked_package_passes(self):
        result = self.verify()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["skills"], 1)

    def test_development_runtime_is_not_a_plugin_component(self):
        (self.package / "src").mkdir()
        (self.package / "src" / "harness.ts").write_text("export {}")
        self.assertIn("unsupported_root_entry", self.verify().stderr)

    def test_changed_skill_bytes_are_rejected(self):
        with (self.package / "skills" / "vectorcraft-use" / "SKILL.md").open("a") as handle:
            handle.write("changed")
        self.assertIn("skill_digest_mismatch", self.verify().stderr)

    def test_unlocked_skill_is_rejected(self):
        extra = self.package / "skills" / "extra"
        extra.mkdir()
        (extra / "SKILL.md").write_text("---\nname: extra\ndescription: Extra.\n---\n")
        self.assertIn("skill_set_mismatch", self.verify().stderr)

    def test_symlink_escape_is_rejected(self):
        (self.package / "skills" / "vectorcraft-use" / "outside").symlink_to(self.lock)
        self.assertIn("package_symlink", self.verify().stderr)


if __name__ == "__main__":
    unittest.main()
