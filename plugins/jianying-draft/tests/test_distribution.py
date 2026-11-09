"""Distribution contract tests for partme-jianying-plugin."""
import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

spec = importlib.util.spec_from_file_location("validate_distribution", ROOT / "scripts" / "validate_distribution.py")
vd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vd)


class DistributionTests(unittest.TestCase):
    def test_validator_accepts_distribution(self) -> None:
        self.assertEqual(vd.main(), 0)

    def test_skill_release_evidence_verifier_is_a_required_distribution_file(self) -> None:
        validator = (ROOT / "scripts" / "validate_distribution.py").read_text(
            encoding="utf-8"
        )
        self.assertIn('"scripts/verify_skill_dispatch_evidence.py"', validator)
        self.assertIn('"scripts/verify_github_release_asset.py"', validator)
        self.assertIn('".github/workflows/skills-sync.yml"', validator)
        self.assertIn('"scripts/remote_release_preflight.py"', validator)
        self.assertIn('"scripts/quality_feature_gate.mjs"', validator)
        self.assertIn('"runtime/feature-flags.json"', validator)

    def test_release_rejects_skill_version_before_job_contract_fix(self) -> None:
        artifacts = {
            platform: {
                "url": (
                    "https://github.com/full-aigc-plugins/jianying-draft/"
                    f"releases/download/v1.6.0/jianying-cli-1.6.0-{platform}.zip"
                ),
                "archiveSha256": "1" * 64,
                "binarySha256": "2" * 64,
                "capabilityManifestSha256": "3" * 64,
                "sbomSha256": "4" * 64,
            }
            for platform in ("darwin-arm64", "darwin-x64", "win32-x64")
        }
        cli_lock = {
            "resolvedVersion": "1.6.0",
            "releaseRef": "v1.6.0",
            "repository": "full-aigc-plugins/jianying-draft",
            "sourceCommit": "a" * 40,
            "artifacts": artifacts,
        }
        skills_lock = {"sources": [{
            "package": "jianying-skills",
            "repo": "https://github.com/full-aigc-skills/jianying-skills.git",
            "releaseVersion": "2.0.2",
            "ref": "v2.0.2",
            "sha": "b" * 40,
            "manifestSchema": "jianying-skills-manifest/v1",
            "manifestSha256": "5" * 64,
        }]}
        with self.assertRaisesRegex(ValueError, "requires jianying-skills 2.0.3"):
            vd.validate_release_readiness(skills_lock, cli_lock)

    def test_manifest_identity(self) -> None:
        repository = "https://github.com/full-aigc-plugins/jianying-draft-plugin"
        for path in (
            ".codex-plugin/plugin.json", ".zcode-plugin/plugin.json",
            "kimi.plugin.json", "plugin.json",
        ):
            manifest = json.loads((ROOT / path).read_text(encoding="utf-8"))
            self.assertEqual(manifest["name"], "jianying-draft", path)
            self.assertEqual(manifest["homepage"], repository, path)
        root_manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(root_manifest["repository"], repository)

    def test_readme_versions_match_the_codex_manifest(self) -> None:
        version = json.loads(
            (ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )["version"]
        for name in ("README.md", "README.en.md"):
            self.assertIn(
                version,
                (ROOT / name).read_text(encoding="utf-8"),
                f"{name} must declare the packaged plugin version",
            )

    def test_active_legacy_dependency_audit_keeps_history_but_rejects_execution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "docs").mkdir()
            (root / ".github" / "workflows").mkdir(parents=True)
            (root / "scripts").mkdir()
            (root / "docs" / "history.md").write_text(
                "pyJianYingDraft and jianying-headless were removed.\n",
                encoding="utf-8",
            )
            self.assertEqual(vd.find_active_legacy_dependencies(root), [])

            (root / "docs" / "runbook.md").write_text(
                "Run `python3 scripts/jydraft_run.py job.json`.\n",
                encoding="utf-8",
            )
            (root / ".github" / "workflows" / "legacy.yml").write_text(
                "repository: partme-ai/jianying-headless\n",
                encoding="utf-8",
            )
            (root / "scripts" / "legacy.sh").write_text(
                "export JIANYING_HEADLESS_ROOT=/tmp/headless\n",
                encoding="utf-8",
            )
            findings = vd.find_active_legacy_dependencies(root)
            self.assertEqual(len(findings), 3)
            self.assertTrue(any("jydraft_run.py" in finding for finding in findings))
            self.assertTrue(any("jianying-headless" in finding for finding in findings))
            self.assertTrue(any("JIANYING_HEADLESS_ROOT" in finding for finding in findings))

    def test_commands_and_hooks_use_only_the_rust_runtime_adapter(self) -> None:
        for rel in (
            "scripts/jydraft_run.py",
            "scripts/jydraft_check.py",
            "hooks/env_check.py",
            "tests/fixtures/host_contract_baseline.json",
            "scripts/vendor/pyJianYingDraft",
            "scripts/vendor/jianying-cli",
            "scripts/VENDOR.json",
            "scripts/vendor_engine.py",
            "scripts/jy_headless",
        ):
            self.assertFalse((ROOT / rel).exists(), f"parallel engine must stay removed: {rel}")
        forbidden = ("python3", "pyJianYingDraft", "jydraft_", "JIANYING_HEADLESS_ROOT", "headless_draft.py")
        for path in [*(ROOT / "commands").glob("*.md"), ROOT / "hooks/hooks.json"]:
            text = path.read_text(encoding="utf-8")
            for value in forbidden:
                self.assertNotIn(value, text, f"{path.relative_to(ROOT)} retains {value}")
        hook = json.loads((ROOT / "hooks/hooks.json").read_text(encoding="utf-8"))
        command = hook["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        self.assertIn("scripts/harness.mjs", command)

    def test_host_manifests_describe_one_rust_runtime(self) -> None:
        paths = [
            ROOT / ".codex-plugin/plugin.json",
            ROOT / ".zcode-plugin/plugin.json",
            ROOT / "kimi.plugin.json",
            ROOT / ".agents/plugins/marketplace.json",
        ]
        for path in paths:
            text = path.read_text(encoding="utf-8")
            self.assertIn("Rust", text, path.name)
            for value in ("pyJianYingDraft", "jycut", "fork pro-tier"):
                self.assertNotIn(value, text, f"{path.relative_to(ROOT)} retains {value}")

    def test_zcode_userconfig_is_record(self) -> None:
        d = json.loads((ROOT / ".zcode-plugin/plugin.json").read_text())
        self.assertIsInstance(d.get("userConfig"), dict)
        self.assertNotIn(
            "hooks",
            d,
            "ZCode auto-discovers hooks/hooks.json; declaring it again creates a duplicate hook",
        )

    def test_kimi_session_start_preloads_router(self) -> None:
        d = json.loads((ROOT / "kimi.plugin.json").read_text())
        self.assertEqual(d.get("sessionStart"), {"skill": "jianying-draft-use"})
        self.assertEqual(d["hooks"][0]["command"], "node ./scripts/harness.mjs session-check")

    def test_skill_sync_uses_only_immutable_release_importer(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "skills-sync.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("scripts/import_skill_release_manifest.py", workflow)
        self.assertIn("isImmutable", workflow)
        self.assertIn("isPrerelease", workflow)
        self.assertIn("gh release verify-asset", workflow)
        self.assertIn("full-aigc-skills/jianying-skills", workflow)
        self.assertIn("client_payload.sha", workflow)
        self.assertIn("client_payload.manifest_sha256", workflow)
        self.assertIn("scripts/verify_skill_dispatch_evidence.py", workflow)
        self.assertIn("scripts/verify_github_release_asset.py", workflow)
        self.assertIn("tagName,isDraft,isPrerelease,isImmutable,publishedAt,assets", workflow)
        self.assertLess(workflow.index("isImmutable"), workflow.index("gh release download"))
        self.assertLess(
            workflow.index("scripts/verify_github_release_asset.py"),
            workflow.index("gh release verify-asset"),
        )
        self.assertLess(
            workflow.index("gh release verify-asset"),
            workflow.index("scripts/import_skill_release_manifest.py"),
        )
        self.assertNotIn("skill_vendor.py update", workflow)

    def test_cli_sync_uses_only_the_canonical_release_index_importer(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "cli-sync.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("repository_dispatch:", workflow)
        self.assertIn("types: [cli-released]", workflow)
        self.assertIn("full-aigc-plugins/jianying-draft", workflow)
        self.assertIn("scripts/import_cli_release_index.mjs", workflow)
        self.assertIn("client_payload.index_sha256", workflow)
        self.assertIn("jq -r .immutable", workflow)
        self.assertIn("--exclude-pre-releases", workflow)
        self.assertIn("gh release verify-asset", workflow)
        self.assertIn("scripts/verify_github_release_asset.py", workflow)
        self.assertIn("releases/tags/$release_ref", workflow)
        self.assertIn("releases/$release_id/assets?per_page=100", workflow)
        self.assertIn("--assets-metadata", workflow)
        self.assertLess(workflow.index("jq -r .immutable"), workflow.index("curl --fail"))
        self.assertLess(
            workflow.index("scripts/verify_github_release_asset.py"),
            workflow.index("gh release verify-asset"),
        )
        self.assertLess(
            workflow.index("gh release verify-asset"),
            workflow.index("scripts/import_cli_release_index.mjs"),
        )
        # 导入器会原子失效宿主验收；同步 PR 必须同时提交锁与失效记录。
        self.assertIn(
            "git diff --quiet -- runtime/jianying-cli.lock.json runtime/host-acceptance.json",
            workflow,
        )
        self.assertIn(
            "git add runtime/jianying-cli.lock.json runtime/host-acceptance.json",
            workflow,
        )
        self.assertNotIn("--clobber", workflow)

    def test_github_actions_use_immutable_commits(self) -> None:
        action_reference = re.compile(r"^\s*-\s+uses:\s+([^\s#]+)", re.MULTILINE)
        immutable_action = re.compile(r"^[^/\s]+/[^@\s]+@[0-9a-f]{40}$")
        for workflow in sorted((ROOT / ".github" / "workflows").glob("*.yml")):
            for reference in action_reference.findall(workflow.read_text(encoding="utf-8")):
                self.assertRegex(
                    reference,
                    immutable_action,
                    f"{workflow.name} uses a mutable action reference: {reference}",
                )

    def test_release_gate_covers_all_supported_platforms_and_real_install(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "release-gate.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("concurrency:\n  group: ${{ github.workflow }}-${{ github.ref }}", workflow)
        self.assertIn("cancel-in-progress: false", workflow)
        for runner, platform in (
            ("macos-15", "darwin-arm64"),
            ("macos-15-intel", "darwin-x64"),
            ("windows-2025", "win32-x64"),
        ):
            self.assertIn(f"runner: {runner}", workflow)
            self.assertIn(f"platform: {platform}", workflow)
        self.assertIn("scripts/release_readiness.py", workflow)
        self.assertIn("scripts/remote_release_preflight.py", workflow)
        self.assertIn("--output remote-release-preflight.json", workflow)
        self.assertIn("name: jianying-plugin-remote-preflight", workflow)
        self.assertIn("path: remote-release-preflight.json", workflow)
        self.assertIn('if [[ "$GITHUB_REF" == refs/tags/v* ]]', workflow)
        self.assertIn('exit "$preflight_status"', workflow)
        self.assertLess(
            workflow.index("scripts/remote_release_preflight.py"),
            workflow.index("scripts/release_readiness.py"),
            "remote prerequisites must fail a tag before expensive contract work",
        )
        self.assertIn("if: always()", workflow)
        self.assertIn("scripts/release_install_canary.mjs", workflow)
        self.assertIn("node --test tests/*.test.mjs", workflow)
        self.assertNotIn("tests/runtime_adapter.test.mjs \\", workflow)
        self.assertIn("scripts/validate_distribution.py --release", workflow)
        self.assertIn('exit "$readiness_status"', workflow)
        self.assertGreaterEqual(workflow.count('if [[ "$GITHUB_REF" == refs/tags/v* ]]'), 3)
        self.assertIn("scripts/validate_plugin_archive.py", workflow)
        self.assertIn('--source-commit "$GITHUB_SHA"', workflow)
        self.assertIn("name: jianying-plugin-release-archive-audit", workflow)
        self.assertIn("plugin-archive-audit.json", workflow)
        self.assertIn("jianying-draft-plugin-source.tar.gz", workflow)
        self.assertIn("-name '*.tar.gz'", workflow)
        self.assertIn("immutable-releases", workflow)
        self.assertIn(
            "- name: Require native immutable releases for the plugin repository\n"
            "        if: startsWith(github.ref, 'refs/tags/v')",
            workflow,
        )
        self.assertIn("needs: [contract, fresh-install]", workflow)
        self.assertIn("\n  evidence:\n", workflow)
        self.assertIn("\n  evidence:\n    if: always()\n", workflow)
        self.assertIn("Create the evidence directory even after upstream failure", workflow)
        self.assertIn("continue-on-error: true", workflow)
        self.assertIn(
            "--output release-evidence/release-evidence-verification.json",
            workflow,
        )
        self.assertIn("needs: [contract, fresh-install, evidence]", workflow)
        self.assertIn("name: jianying-plugin-release-verification", workflow)
        self.assertIn("Preserve platform canary evidence even when it fails", workflow)
        self.assertIn("Preserve aggregate verification evidence even when it fails", workflow)
        self.assertGreaterEqual(workflow.count("if: always()"), 3)
        self.assertIn("merge-multiple: true", workflow)
        self.assertIn("scripts/verify_release_evidence.mjs", workflow)
        self.assertIn("gh release create", workflow)
        self.assertIn("--draft", workflow)
        self.assertIn("gh release verify-asset", workflow)
        self.assertIn("existing immutable release matches this build", workflow)
        self.assertIn("scripts/release_publication_plan.py", workflow)
        self.assertIn(
            "secrets.RELEASE_RULESET_READ_TOKEN || github.token", workflow
        )
        self.assertIn(
            'GH_TOKEN="$RELEASE_RULESET_READ_TOKEN" gh release verify ', workflow
        )
        self.assertIn(
            'GH_TOKEN="$RELEASE_RULESET_READ_TOKEN" gh release verify-asset ', workflow
        )
        self.assertEqual(workflow.count("--remote origin"), 3)
        self.assertEqual(workflow.count('--expected-commit "$(git rev-parse HEAD)"'), 3)
        policy = json.loads(
            (ROOT / "runtime/release-protection-policy.json").read_text(encoding="utf-8")
        )
        self.assertEqual(policy["schema"], "jianying-release-protection-policy/v1")
        self.assertEqual(
            policy["mode"], "immutable_release_with_tag_commit_rechecks"
        )
        self.assertTrue(all(policy["requiredChecks"].values()))
        self.assertIn("resuming a byte-identical partial draft release", workflow)
        self.assertGreaterEqual(
            workflow.count('--repository "$GITHUB_REPOSITORY"'), 3,
        )
        self.assertNotIn('gh release view "$GITHUB_REF_NAME"', workflow)
        self.assertIn("scripts/verify_release_attestation.py", workflow)
        self.assertIn("--expected-tag-object", workflow)
        self.assertIn('if [ "$publication_action" != "verify_existing" ]; then', workflow)
        self.assertIn("published release asset set or digest differs", workflow)
        self.assertIn("asset attestation not visible yet", workflow)
        self.assertIn("for attempt in $(seq 1 30)", workflow)
        self.assertNotIn("release already exists; refusing to replace immutable evidence", workflow)
        self.assertNotIn("--clobber", workflow)

    def test_automation_branches_use_serialized_explicit_leases(self) -> None:
        for name, branch, unavailable_label in (
            ("skills-sync.yml", "chore/skills-sync", "skills-sync"),
            ("cli-sync.yml", "chore/cli-sync", "cli-sync"),
            ("rust-cutover.yml", "chore/rust-only-cutover", "rust-cutover"),
        ):
            workflow_path = ROOT / ".github" / "workflows" / name
            if name == "rust-cutover.yml" and not workflow_path.exists():
                continue
            workflow = workflow_path.read_text(encoding="utf-8")
            with self.subTest(workflow=name):
                self.assertIn("concurrency:", workflow)
                self.assertIn("cancel-in-progress: false", workflow)
                self.assertIn(
                    f"git ls-remote --heads origin refs/heads/{branch}", workflow
                )
                self.assertIn(
                    f"--force-with-lease=refs/heads/{branch}:${{remote_sha}}", workflow
                )
                self.assertNotIn(f"git push --force-with-lease origin {branch}", workflow)
                self.assertNotIn(
                    f"--label {unavailable_label}",
                    workflow,
                    "automation must not require an undeclared repository label",
                )

    def test_rust_cutover_waits_for_all_other_release_gates(self) -> None:
        workflow_path = ROOT / ".github" / "workflows" / "rust-cutover.yml"
        if not workflow_path.exists():
            harness = (ROOT / "scripts" / "harness.mjs").read_text(encoding="utf-8")
            self.assertNotIn("legacyRuntimeDiagnostics", harness)
            self.assertNotIn("JIANYING_HEADLESS_ROOT", harness)
            self.assertFalse((ROOT / "tests" / "legacy_migration.test.mjs").exists())
            return
        workflow = workflow_path.read_text(encoding="utf-8")
        for runner, platform in (
            ("macos-15", "darwin-arm64"),
            ("macos-15-intel", "darwin-x64"),
            ("windows-2025", "win32-x64"),
        ):
            self.assertIn(f"runner: {runner}", workflow)
            self.assertIn(f"platform: {platform}", workflow)
        self.assertIn("scripts/release_install_canary.mjs", workflow)
        self.assertIn("--allow-cutover-pending", workflow)
        self.assertIn("needs: [prerequisites, fresh-install]", workflow)
        self.assertIn("jianying-plugin-cutover-readiness", workflow)
        self.assertIn("jianying-plugin-cutover-canary-${{ matrix.platform }}", workflow)
        self.assertIn("jianying-plugin-cutover-archive-audit", workflow)
        self.assertIn("scripts/validate_plugin_archive.py", workflow)
        self.assertIn("jianying-draft-plugin-source.tar.gz", workflow)
        self.assertIn('--plugin-source-commit "$GITHUB_SHA"', workflow)
        self.assertIn("blocked == allowed", workflow)
        self.assertNotIn("'runtime.legacy_engines_removed'", workflow)
        self.assertIn("'runtime.release_surface_rust_only'", workflow)
        self.assertIn("tests/legacy_migration.test.mjs", workflow)
        self.assertIn(".github/workflows/rust-cutover.yml", workflow)
        for removed_python_path in (
            "scripts/jydraft_run.py",
            "scripts/jydraft_check.py",
            "hooks/env_check.py",
        ):
            self.assertNotIn(removed_python_path, workflow)
        self.assertIn("scripts/release_readiness.py", workflow)
        self.assertIn("scripts/validate_distribution.py --release", workflow)
        self.assertNotIn("git rm -r", workflow)

    def test_version_bump_invalidates_real_host_acceptance(self) -> None:
        script = (ROOT / "scripts" / "bump-plugin.mjs").read_text(encoding="utf-8")
        self.assertIn('runtime/host-acceptance.json', script)
        self.assertIn('"README.md", "README.en.md"', script)
        self.assertIn("bumpReadme", script)
        self.assertIn('timeZone: "Asia/Shanghai"', script)
        self.assertIn('acceptance.status = "pending"', script)
        self.assertIn("acceptance.pluginVersion = newVersion", script)
        self.assertIn("acceptance.hosts = []", script)
        self.assertIn("发版候选已生成（尚未提交、推送、打 tag 或发布）", script)
        self.assertIn("不可变 Release、制品校验和真实市场安装验证", script)
        self.assertNotIn("发版完成。剩余步骤", script)


if __name__ == "__main__":
    unittest.main()
