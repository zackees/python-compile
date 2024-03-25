"""
Unit test file.
"""

import os
import shutil
import sys
import unittest
from pathlib import Path
from pprint import pprint
from tempfile import TemporaryDirectory

from python_compile.cli import Args
from python_compile.compile import python_compile

HERE = Path(__file__).parent.absolute()
PROJECT_ROOT = HERE.parent
DEMO_PY = PROJECT_ROOT / "src/python_compile/assets/demo_http_server.py"


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_run_main(self) -> None:
        """Test command line interface (CLI)."""
        with TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
            prev_dir = os.getcwd()
            os.chdir(tmp_dir)
            basename = DEMO_PY.name
            shutil.copy(DEMO_PY, basename)
            if sys.platform == "win32":
                expected_path = "demo_http_server.exe"
            else:
                expected_path = "demo_http_server.bin.gz"
            try:
                args = Args(app_py=Path(basename))
                rtn = python_compile(args)
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
