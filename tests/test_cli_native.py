"""
Unit test file.
"""

import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from pprint import pprint
from tempfile import TemporaryDirectory

HERE = Path(__file__).parent.absolute()
PROJECT_ROOT = HERE.parent
DEMO_PY = PROJECT_ROOT / "src/python_compile/assets/demo_http_server.py"


class CliNativetester(unittest.TestCase):
    """Main tester class."""

    def test_cli(self) -> None:
        """Test command line interface (CLI)."""
        with TemporaryDirectory() as tmp_dir:
            os.chdir(tmp_dir)
            basename = DEMO_PY.name
            shutil.copy(DEMO_PY, basename)
            try:
                cmd_list = [
                    "python-compile",
                    "--input",
                    str(basename),
                ]
                cmd_str = subprocess.list2cmdline(cmd_list)
                print(f"Running: {cmd_str}")
                rtn = os.system(" ".join(cmd_list))
                self.assertEqual(0, rtn)

                files = os.listdir()

                pprint(files)
                if sys.platform == "win32":
                    self.assertTrue("demo_http_server.exe" in files)
                else:
                    self.assertTrue("demo_http_server.bin.gz" in files)
            finally:
                os.chdir(PROJECT_ROOT)


if __name__ == "__main__":
    unittest.main()
