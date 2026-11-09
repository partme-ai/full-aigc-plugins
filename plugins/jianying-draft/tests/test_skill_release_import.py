"""不可变技能发布清单导入门禁。"""

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "import_skill_release_manifest", ROOT / "scripts" / "import_skill_release_manifest.py"
)
IMPORTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(IMPORTER)
EVIDENCE_SPEC = importlib.util.spec_from_file_location(
    "verify_skill_dispatch_evidence",
    ROOT / "scripts" / "verify_skill_dispatch_evidence.py",
)
EVIDENCE = importlib.util.module_from_spec(EVIDENCE_SPEC)
EVIDENCE_SPEC.loader.exec_module(EVIDENCE)


class SkillReleaseImportTests(unittest.TestCase):
    def test_dispatch_evidence_accepts_exact_commit_and_manifest_digest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "manifest.json"
            manifest.write_text('{"schema":"fixture"}\n', encoding="utf-8")
            digest = hashlib.sha256(manifest.read_bytes()).hexdigest()
            commit = "a" * 40
            result = EVIDENCE.verify_dispatch_evidence(
                manifest,
                expected_source_commit=commit,
                expected_manifest_sha256=digest,
                observed_source_commit=commit,
            )
            self.assertEqual(result["source_commit"], commit)
            self.assertEqual(result["manifest_sha256"], digest)

    def test_dispatch_evidence_rejects_commit_or_manifest_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest = Path(directory) / "manifest.json"
            manifest.write_text("{}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "checkout commit differs"):
                EVIDENCE.verify_dispatch_evidence(
                    manifest,
                    expected_source_commit="a" * 40,
                    observed_source_commit="b" * 40,
                )
            with self.assertRaisesRegex(ValueError, "manifest digest differs"):
                EVIDENCE.verify_dispatch_evidence(
                    manifest,
                    expected_manifest_sha256="0" * 64,
                    observed_source_commit="a" * 40,
                )

    def fixture(self, root: Path, state: str = "released") -> tuple[Path, Path, Path, str]:
        source = root / "source"
        skill = source / "skills" / "fixture-skill"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: fixture-skill\ndescription: fixture\n---\n\nRust CLI only.\n",
            encoding="utf-8",
        )
        digest = IMPORTER.hash_skill_dir(skill)
        commit = "a" * 40
        entry = {
            "name": "fixture-skill",
            "sha256": digest,
            "minimum_cli_version": "1.6.0",
            "required_capabilities": ["job.run"],
        }
        manifest = {
            "schema": "jianying-skills-manifest/v1",
            "package": "jianying-skills",
            "repository": IMPORTER.CANONICAL_REPOSITORY,
            "version": "2.0.3",
            "source_commit": commit,
            "content_state": state,
            "release_ref": "v2.0.3" if state == "released" else None,
            "install_cli_capabilities": ["job.run"],
            "minimum_cli_capabilities": ["job.run", "render.native"],
            "skills": [entry],
            "content_sha256": IMPORTER.aggregate_digest([entry]),
        }
        manifest_path = root / "manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        plugin = root / "plugin"
        old_skill = plugin / "skills" / "old-skill"
        old_skill.mkdir(parents=True)
        (old_skill / "SKILL.md").write_text("old", encoding="utf-8")
        lock_path = plugin / "skills.lock.json"
        lock_path.write_text(json.dumps({
            "version": 1,
            "sources": [{
                "package": "jianying-skills",
                "repo": "https://github.com/full-aigc-skills/jianying-skills.git",
                "ref": "v1.2.0",
                "sha": "b" * 40,
                "skills": ["old-skill"],
                "dest": "skills/",
                "minimumCliVersion": "1.0.0",
                "minimumCapabilities": ["job.run"],
                "sha256": {"old-skill": "0" * 64},
            }],
        }), encoding="utf-8")
        acceptance = plugin / "runtime" / "host-acceptance.json"
        acceptance.parent.mkdir()
        acceptance.write_text(json.dumps({
            "schema": "jianying-host-release-acceptance/v1",
            "status": "passed",
            "pluginVersion": "0.17.2",
            "cliVersion": "1.6.0",
            "skillsVersion": "2.0.2",
            "jobSchema": "jianying-job/v2",
            "hosts": [{"host": "fixture"}],
        }), encoding="utf-8")
        return source, manifest_path, lock_path, commit

    def test_unreleased_manifest_is_rejected_without_mutating_plugin(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source, manifest, lock, commit = self.fixture(Path(directory), "working_tree_unreleased")
            original_lock = lock.read_bytes()
            with self.assertRaisesRegex(ValueError, "not an immutable released version"):
                IMPORTER.sync_release(
                    lock, manifest, source,
                    observed_commit=commit,
                    resolved_commit=commit,
                )
            self.assertEqual(lock.read_bytes(), original_lock)
            self.assertTrue((lock.parent / "skills" / "old-skill" / "SKILL.md").is_file())

    def test_released_manifest_atomically_replaces_skills_and_lock(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source, manifest, lock, commit = self.fixture(Path(directory))
            result = IMPORTER.sync_release(
                lock, manifest, source,
                observed_commit=commit,
                resolved_commit=commit,
            )
            updated = json.loads(lock.read_text(encoding="utf-8"))
            self.assertEqual(result["ref"], "v2.0.3")
            self.assertEqual(updated["sources"][0]["sha"], commit)
            self.assertEqual(updated["sources"][0]["releaseVersion"], "2.0.3")
            self.assertEqual(updated["sources"][0]["minimumCapabilities"], ["job.run"])
            self.assertTrue((lock.parent / "skills" / "fixture-skill" / "SKILL.md").is_file())
            self.assertFalse((lock.parent / "skills" / "old-skill").exists())
            acceptance = json.loads(
                (lock.parent / "runtime/host-acceptance.json").read_text(encoding="utf-8")
            )
            self.assertEqual(acceptance["status"], "pending")
            self.assertEqual(acceptance["skillsVersion"], "2.0.3")
            self.assertEqual(acceptance["hosts"], [])

    def test_release_before_contract_fix_is_rejected_before_swap(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source, manifest, lock, commit = self.fixture(Path(directory))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            payload["version"] = "2.0.2"
            payload["release_ref"] = "v2.0.2"
            manifest.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "predates required contract fix 2.0.3"):
                IMPORTER.sync_release(
                    lock, manifest, source,
                    observed_commit=commit,
                    resolved_commit=commit,
                )
            self.assertTrue((lock.parent / "skills" / "old-skill" / "SKILL.md").is_file())

    def test_tampered_skill_is_rejected_before_swap(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source, manifest, lock, commit = self.fixture(Path(directory))
            (source / "skills" / "fixture-skill" / "SKILL.md").write_text("tampered", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "differs from release manifest"):
                IMPORTER.sync_release(
                    lock, manifest, source,
                    observed_commit=commit,
                    resolved_commit=commit,
                )
            self.assertTrue((lock.parent / "skills" / "old-skill" / "SKILL.md").is_file())

    def test_symlinked_skill_content_is_rejected_before_swap(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, manifest, lock, commit = self.fixture(root)
            outside = root / "outside.md"
            outside.write_text("external content", encoding="utf-8")
            (source / "skills" / "fixture-skill" / "linked.md").symlink_to(outside)
            with self.assertRaisesRegex(ValueError, "symbolic links are forbidden"):
                IMPORTER.sync_release(
                    lock, manifest, source,
                    observed_commit=commit,
                    resolved_commit=commit,
                )
            self.assertTrue((lock.parent / "skills" / "old-skill" / "SKILL.md").is_file())

    def test_noncanonical_source_repository_is_rejected_before_swap(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source, manifest, lock, commit = self.fixture(Path(directory))
            payload = json.loads(lock.read_text(encoding="utf-8"))
            payload["sources"][0]["repo"] = "https://example.invalid/jianying-skills.git"
            lock.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "canonical jianying-skills repository"):
                IMPORTER.sync_release(
                    lock, manifest, source,
                    observed_commit=commit,
                    resolved_commit=commit,
                )
            self.assertTrue((lock.parent / "skills" / "old-skill" / "SKILL.md").is_file())

    def test_noncanonical_manifest_repository_is_rejected_before_swap(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source, manifest, lock, commit = self.fixture(Path(directory))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            payload["repository"] = "https://example.invalid/jianying-skills.git"
            manifest.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "manifest repository is not canonical"):
                IMPORTER.sync_release(
                    lock, manifest, source,
                    observed_commit=commit,
                    resolved_commit=commit,
                )
            self.assertTrue((lock.parent / "skills" / "old-skill" / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
