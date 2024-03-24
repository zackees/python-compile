"""
Unit test file.
"""

import os
import sys
import unittest
from pathlib import Path
from pprint import pprint
from tempfile import TemporaryDirectory

from python_compile.cli import Args, run

HERE = Path(__file__).parent
PROJECT_ROOT = HERE.parent
DEMO_PY = PROJECT_ROOT / "src/python_compile/assets/demo_http_server.py"


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_run_main(self) -> None:
        """Test command line interface (CLI)."""
        with TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            prev_dir = os.getcwd()
            os.chdir(tmp_dir)
            if sys.platform == "win32":
                expected_path = "demo_http_server.exe"
            else:
                expected_path = "demo_http_server.bin"
            try:
                args = Args(app_py=DEMO_PY)
                rtn = run(args)
                self.assertEqual(0, rtn)
                files = os.listdir(tmp_dir)
                pprint(files)
                self.assertTrue(
                    expected_path in files, f"{expected_path} not found in {files}"
                )
            finally:
                os.chdir(prev_dir)


if __name__ == "__main__":
    unittest.main()
