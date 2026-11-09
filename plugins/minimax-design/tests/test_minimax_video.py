"""Unit tests for scripts/minimax_video.py v2 (offline: no network, no key)."""
import importlib.util
import os
import sys
import unittest
from pathlib import Path
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

spec = importlib.util.spec_from_file_location("minimax_video", ROOT / "scripts" / "minimax_video.py")
mm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mm)


class CheckTests(unittest.TestCase):
    def test_check_without_key_reports_actionable_guidance(self) -> None:
        import contextlib
        import io
        import os
        old = os.environ.pop("MINIMAX_API_KEY", None)
        try:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = mm.check()
            out = buf.getvalue()
            self.assertEqual(rc, 0, "check 永远 exit 0（advisory）")
            self.assertIn("未设置", out)
            self.assertIn("platform.minimax.cn", out, "必须给出可操作的申请地址")
            self.assertIn("export MINIMAX_API_KEY=", out, "必须给出可操作的配置命令")
            self.assertIn("mmx-cli", out, "必须提示 mmx 安装路径")
        finally:
            if old is not None:
                os.environ["MINIMAX_API_KEY"] = old

    def test_check_with_key_masks_secret(self) -> None:
        import contextlib
        import io
        import os
        os.environ["MINIMAX_API_KEY"] = "sk-test-abcdef1234"
        try:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                mm.check()
            out = buf.getvalue()
            self.assertIn("已设置", out)
            self.assertIn("1234", out, "只显示尾号")
            self.assertNotIn("sk-test-abcdef1234", out, "完整密钥禁止回显")
        finally:
            os.environ.pop("MINIMAX_API_KEY", None)


class ContentBuilderTests(unittest.TestCase):
    def test_t2v_content_is_text_only(self) -> None:
        c = mm.build_content("一个男孩在海边打篮球", None, None, [])
        self.assertEqual(len(c), 1)
        self.assertEqual(c[0]["type"], "text")

    def test_fl2v_roles_are_exact(self) -> None:
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"\x89PNG first")
            first = f.name
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"\x89PNG last")
            last = f.name
        c = mm.build_content("路径描述", first, last, [])
        self.assertEqual([x.get("role") for x in c if x["type"] == "image_url"],
                         ["first_frame", "last_frame"])
        for x in c:
            if x["type"] == "image_url":
                self.assertIn("url", x["image_url"])

    def test_local_frame_becomes_data_url(self) -> None:
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"\x89PNG fake")
            c = mm.build_content("p", f.name, None, [])
        url = c[1]["image_url"]["url"]
        self.assertTrue(url.startswith("data:image/png;base64,"))

    def test_reference_mode_mutually_exclusive_with_fl2v(self) -> None:
        with self.assertRaises(SystemExit):
            mm.build_content("p", "first.png", None, ["ref.png"])

    def test_url_frames_pass_through(self) -> None:
        c = mm.build_content("p", "https://example.com/a.png", None, [])
        self.assertEqual(c[1]["image_url"]["url"], "https://example.com/a.png")


class ApiGuardTests(unittest.TestCase):
    def test_api_without_key_exits_with_guidance(self) -> None:
        import os
        old = os.environ.pop("MINIMAX_API_KEY", None)
        try:
            with self.assertRaises(SystemExit) as ctx:
                mm.call("POST", "/v2/video_generation", {})
            self.assertIn("MINIMAX_API_KEY", str(ctx.exception))
        finally:
            if old is not None:
                os.environ["MINIMAX_API_KEY"] = old


if __name__ == "__main__":
    unittest.main()


class AuthAndResolutionTests(unittest.TestCase):
    """四级解析链（环境 > 项目 .env > 插件 .env > 用户配置）+ auth 子命令。"""

    def setUp(self) -> None:
        import tempfile
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.config_dir = Path(self.tmp.name) / "cfg"
        os.environ["MINIMAX_CONFIG_DIR"] = str(self.config_dir)
        self.addCleanup(os.environ.pop, "MINIMAX_CONFIG_DIR", None)
        self.old_key = os.environ.pop("MINIMAX_API_KEY", None)
        self.addCleanup(os.environ.__setitem__, "MINIMAX_API_KEY", self.old_key) if self.old_key else None

    def tearDown(self) -> None:
        os.environ.pop("MINIMAX_API_KEY", None)

    def test_auth_writes_and_resolution_finds_user_config(self) -> None:
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = mm.auth_setup(type("A", (), {"api_key": "sk-demo-9999", "clear": False})())
        self.assertEqual(rc, 0)
        self.assertIn("9999", buf.getvalue())
        self.assertNotIn("sk-demo-9999", buf.getvalue(), "完整密钥禁止回显")
        key, source = mm.get_key()
        self.assertEqual(key, "sk-demo-9999")
        self.assertIn("用户配置", source)
        mode = mm._config_file().stat().st_mode & 0o777
        self.assertEqual(mode, 0o600, "凭据文件必须 600")

    def test_auth_clear_removes_key(self) -> None:
        mm.auth_setup(type("A", (), {"api_key": "sk-demo-1", "clear": False})())
        mm.auth_setup(type("A", (), {"api_key": None, "clear": True})())
        key, _ = mm.get_key()
        self.assertIsNone(key)

    def test_project_env_beats_user_config(self) -> None:
        import os as o
        mm.auth_setup(type("A", (), {"api_key": "sk-from-config", "clear": False})())
        project = Path(self.tmp.name) / "proj"
        project.mkdir()
        (project / ".env").write_text('MINIMAX_API_KEY="sk-from-dotenv"\n', encoding="utf-8")
        old_cwd = o.getcwd()
        try:
            o.chdir(project)
            key, source = mm.get_key()
            self.assertEqual(key, "sk-from-dotenv")
            self.assertIn(".env", source)
        finally:
            o.chdir(old_cwd)

    def test_process_env_wins_over_everything(self) -> None:
        mm.auth_setup(type("A", (), {"api_key": "sk-from-config", "clear": False})())
        os.environ["MINIMAX_API_KEY"] = "sk-from-env"
        key, source = mm.get_key()
        self.assertEqual(key, "sk-from-env")
        self.assertEqual(source, "环境变量")

    def test_env_file_strips_quotes_and_comments(self) -> None:
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".env", delete=False, encoding="utf-8") as f:
            f.write("# comment\nMINIMAX_API_KEY=\"sk-quoted\"\n\n")
            path = f.name
        values = mm._parse_env_file(Path(path))
        self.assertEqual(values["MINIMAX_API_KEY"], "sk-quoted")

    def test_platform_hints_cover_all_systems(self) -> None:
        import contextlib
        import io
        win = "\n".join(mm.platform_setup_hint("windows"))
        mac = "\n".join(mm.platform_setup_hint("macos"))
        lin = "\n".join(mm.platform_setup_hint("linux"))
        self.assertIn("setx", win, "Windows 必须给 setx/PowerShell 指引")
        self.assertIn(".zshrc", mac, "macOS 必须给 zsh 指引")
        self.assertIn(".bashrc", lin, "Linux 必须给 bash 指引")
        # 未指定平台时自动探测且不抛异常
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = mm.check()
        self.assertEqual(rc, 0)
