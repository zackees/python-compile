"""
Unit test file.
"""

import os
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

HERE = Path(__file__).parent
PROJECT_ROOT = HERE.parent
DEMO_PY = PROJECT_ROOT / "src/python_compile/assets/demo_http_server.py"


class CliNativetester(unittest.TestCase):
    """Main tester class."""

    def test_cli(self) -> None:
        """Test command line interface (CLI)."""
        with TemporaryDirectory() as tmp_dir:
            os.chdir(tmp_dir)
            try:
                cmd_list = [
                    "python-compile",
                    "--input",
                    str(DEMO_PY),
                ]
                cmd_str = subprocess.list2cmdline(cmd_list)
                print(f"Running: {cmd_str}")
                rtn = os.system(" ".join(cmd_list))
                self.assertEqual(0, rtn)
                expected_path_gz: Path = Path("demo_http_server.bin.gz")
                self.assertTrue(expected_path_gz.exists())
                if sys.platform == "win32":
                    expected_path = Path("demo_http_server.exe")
                else:
                    expected_path = Path("demo_http_server.bin")
                self.assertTrue(expected_path.exists())
            finally:
                os.chdir(PROJECT_ROOT)


if __name__ == "__main__":
    unittest.main()
