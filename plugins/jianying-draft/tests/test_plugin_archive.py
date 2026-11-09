"""Tests for the exact plugin archive Rust-only distribution gate."""
from __future__ import annotations

import importlib.util
import io
import json
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = "a" * 40
SPEC = importlib.util.spec_from_file_location(
    "validate_plugin_archive", ROOT / "scripts" / "validate_plugin_archive.py"
)
ARCHIVE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ARCHIVE)


def required_payload() -> dict[str, bytes]:
    files = {name: b"safe\n" for name in ARCHIVE.REQUIRED_FILES}
    files[".codex-plugin/plugin.json"] = (
        b'{"name":"jianying-draft","version":"0.17.2+codex.20260920"}\n'
    )
    skills = [f"skill-{index}" for index in range(14)]
    files["skills.lock.json"] = json.dumps({"sources": [{"skills": skills}]}).encode()
    for name in skills:
        files[f"skills/{name}/SKILL.md"] = b"---\nname: safe\n---\n"
    return files


def write_tar(path: Path, files: dict[str, bytes], *, unsafe_link: bool = False) -> None:
    with tarfile.open(path, mode="w:gz") as archive:
        for relative, payload in files.items():
            info = tarfile.TarInfo(f"plugin/{relative}")
            info.size = len(payload)
            archive.addfile(info, io.BytesIO(payload))
        if unsafe_link:
            info = tarfile.TarInfo("plugin/scripts/link")
            info.type = tarfile.SYMTYPE
            info.linkname = "../../outside"
            archive.addfile(info)


class PluginArchiveTests(unittest.TestCase):
    def test_accepts_complete_rust_only_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "plugin.tar.gz"
            write_tar(path, required_payload())
            result = ARCHIVE.validate_archive(path, SOURCE_COMMIT)
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["skillCount"], 14)
        self.assertTrue(result["rustOnlyRuntime"])
        self.assertRegex(result["archiveSha256"], r"^[0-9a-f]{64}$")
        self.assertEqual(result["pluginSourceCommit"], SOURCE_COMMIT)

    def test_rejects_retired_python_engine_member(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "plugin.tar.gz"
            files = required_payload()
            files["scripts/jydraft_run.py"] = b"print('legacy')\n"
            write_tar(path, files)
            with self.assertRaisesRegex(
                ARCHIVE.ArchiveValidationError, "retired runtime artifacts"
            ):
                ARCHIVE.validate_archive(path, SOURCE_COMMIT)

    def test_rejects_missing_packaged_quality_feature_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "plugin.tar.gz"
            files = required_payload()
            del files["runtime/feature-flags.json"]
            write_tar(path, files)
            with self.assertRaisesRegex(
                ARCHIVE.ArchiveValidationError, "runtime/feature-flags.json"
            ):
                ARCHIVE.validate_archive(path, SOURCE_COMMIT)

    def test_rejects_external_headless_checkout_instruction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "plugin.tar.gz"
            files = required_payload()
            files["docs/runbook.md"] = (
                b"git clone https://github.com/partme-ai/jianying-headless.git\n"
            )
            write_tar(path, files)
            with self.assertRaisesRegex(
                ARCHIVE.ArchiveValidationError, "active legacy runtime dependencies"
            ):
                ARCHIVE.validate_archive(path, SOURCE_COMMIT)

    def test_rejects_generated_python_cache(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "plugin.tar.gz"
            files = required_payload()
            files["scripts/__pycache__/tool.cpython-312.pyc"] = b"compiled"
            write_tar(path, files)
            with self.assertRaisesRegex(
                ARCHIVE.ArchiveValidationError, "generated Python cache files"
            ):
                ARCHIVE.validate_archive(path, SOURCE_COMMIT)

    def test_rejects_member_exceeding_uncompressed_size_limit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "plugin.tar.gz"
            files = required_payload()
            files["docs/oversized.md"] = b"x" * 33
            write_tar(path, files)
            original = ARCHIVE.MAX_FILE_BYTES
            ARCHIVE.MAX_FILE_BYTES = 32
            try:
                with self.assertRaisesRegex(
                    ARCHIVE.ArchiveValidationError, "exceeds size limit"
                ):
                    ARCHIVE.validate_archive(path, SOURCE_COMMIT)
            finally:
                ARCHIVE.MAX_FILE_BYTES = original

    def test_rejects_links_before_extraction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "plugin.tar.gz"
            write_tar(path, required_payload(), unsafe_link=True)
            with self.assertRaisesRegex(
                ARCHIVE.ArchiveValidationError, "regular file or directory"
            ):
                ARCHIVE.validate_archive(path, SOURCE_COMMIT)

    def test_rejects_missing_skill_entrypoint(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "plugin.tar.gz"
            files = required_payload()
            del files["skills/skill-13/SKILL.md"]
            write_tar(path, files)
            with self.assertRaisesRegex(
                ARCHIVE.ArchiveValidationError, "exactly match skills.lock.json"
            ):
                ARCHIVE.validate_archive(path, SOURCE_COMMIT)


if __name__ == "__main__":
    unittest.main()
