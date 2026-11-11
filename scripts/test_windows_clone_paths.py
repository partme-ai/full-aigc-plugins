"""检查 Codex Windows 临时检出目录中的文件路径预算。"""

import pathlib
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
MAX_RELATIVE_PATH = 150


class WindowsClonePathsTest(unittest.TestCase):
    def test_tracked_paths_fit_codex_staging_directory(self):
        paths = subprocess.check_output(
            ["git", "-C", str(ROOT), "ls-files", "-z"]
        ).decode("utf-8").split("\0")
        too_long = sorted(
            (path for path in paths if (ROOT / path).is_file() and len(path) > MAX_RELATIVE_PATH),
            key=len,
            reverse=True,
        )
        self.assertEqual([], too_long, f"tracked paths exceed {MAX_RELATIVE_PATH} characters")


if __name__ == "__main__":
    unittest.main()
