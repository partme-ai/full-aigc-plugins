"""Hook contract tests: advisory exit 0, no stderr spam, no secret leakage."""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys_path = ROOT / "scripts"
import sys  # noqa: E402

sys.path.insert(0, str(sys_path))


def run_hook(path: Path, stdin_payload: str = "{}", env_extra: dict | None = None):
    env = {**os.environ, **(env_extra or {})}
    return subprocess.run(
        [sys.executable, str(path)], input=stdin_payload,
        capture_output=True, text=True, env=env, timeout=30,
    )


class EnvCheckHookTests(unittest.TestCase):
    """env_check：插件自完整性检查——完好时静默，缺件时一行告警，永远 exit 0。"""

    def test_intact_tree_is_silent_with_and_without_key(self) -> None:
        hook = ROOT / "hooks" / "env_check.py"
        for env in ({}, {"MINIMAX_API_KEY": "sk-secret-9999"}):
            r = run_hook(hook, env_extra=env)
            self.assertEqual(r.returncode, 0)
            self.assertEqual("", r.stdout)

    def test_missing_client_script_warns_once(self) -> None:
        import shutil, tempfile
        hook = ROOT / "hooks" / "env_check.py"
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory) / "hooks" / "env_check.py"
            copied.parent.mkdir(parents=True)
            shutil.copy2(hook, copied)
            r = run_hook(copied, "{}")
        self.assertEqual(r.returncode, 0)
        self.assertIn("生成客户端脚本缺失", r.stdout)


class IntentHookTests(unittest.TestCase):
    def test_minimax_prompt_gets_hint(self) -> None:
        hook = ROOT / "hooks" / "check_minimax_intent.py"
        r = run_hook(hook, json.dumps({"prompt": "帮我用 minimax 生成一段海螺视频"}))
        self.assertEqual(r.returncode, 0)
        self.assertIn("minimax-design-use", r.stdout)

    def test_unrelated_prompt_is_silent(self) -> None:
        hook = ROOT / "hooks" / "check_minimax_intent.py"
        r = run_hook(hook, json.dumps({"prompt": "帮我修这个 java 空指针"}))
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.strip(), "")

    def test_slash_commands_are_ignored(self) -> None:
        hook = ROOT / "hooks" / "check_minimax_intent.py"
        r = run_hook(hook, json.dumps({"prompt": "/minimax-video something"}))
        self.assertEqual(r.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
