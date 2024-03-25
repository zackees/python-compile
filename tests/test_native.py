"""
Unit test file.
"""

import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

HERE = Path(__file__).parent.absolute()
PROJECT_ROOT = HERE.parent
DEMO_PY = PROJECT_ROOT / "src/python_compile/assets/demo_http_server.py"


class NativeTester(unittest.TestCase):
    """Main tester class."""

    def test_compile(self) -> None:
        """Test command line interface (CLI)."""
        with TemporaryDirectory() as tmp_dir:
            prev_dir = os.getcwd()
            os.chdir(tmp_dir)
            basename = DEMO_PY.name
            shutil.copy(DEMO_PY, basename)
            try:
                cmd_list = [
                    "python-compile",
                    "--input",
                    basename,
                ]
                cmd_str = subprocess.list2cmdline(cmd_list)
                print(f"Running: {cmd_str}")
                rtn = os.system(" ".join(cmd_list))
                self.assertEqual(0, rtn)
                if sys.platform == "win32":
                    self.assertTrue("demo_http_server.exe" in os.listdir())
                else:
                    self.assertTrue("demo_http_server.bin.gz" in os.listdir())
            finally:
                os.chdir(prev_dir)


if __name__ == "__main__":
    unittest.main()
