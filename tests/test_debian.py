"""
Unit test file.
"""

import os
import shutil
import subprocess
import unittest
from pathlib import Path
from pprint import pprint
from tempfile import TemporaryDirectory

from python_compile.cli import Args
from python_compile.compile import python_compile

HERE = Path(__file__).parent
PROJECT_ROOT = HERE.parent
DEMO_PY = PROJECT_ROOT / "src/python_compile/assets/demo_http_server.py"


class NativeTester(unittest.TestCase):
    """Main tester class."""

    @unittest.skip("Skip test_compile")
    def test_compile(self) -> None:
        """Test command line interface (CLI)."""
        with TemporaryDirectory() as tmp_dir:
            prev_dir = os.getcwd()
            os.chdir(tmp_dir)
            try:
                cmd_list = [
                    "python-compile",
                    "--input",
                    "src/python_compile/assets/demo_http_server.py",
                    "--os",
                    "debian",
                ]
                cmd_str = subprocess.list2cmdline(cmd_list)
                print(f"Running: {cmd_str}")
                rtn = os.system(" ".join(cmd_list))
                self.assertEqual(0, rtn)
                files = os.listdir(tmp_dir)
                pprint(files)
                expected_path_gz: Path = Path("demo_http_server.bin.gz")
                self.assertTrue(expected_path_gz.exists())
                expected_path = Path("demo_http_server.bin")
                self.assertTrue(expected_path.exists())
            finally:
                os.chdir(prev_dir)

    def test_compile_main(self) -> None:
        """Test command line interface (CLI)."""
        with TemporaryDirectory() as tmp_dir:
            prev_dir = os.getcwd()
            os.chdir(tmp_dir)
            try:
                shutil.copy(DEMO_PY, DEMO_PY.name)
                args = Args(app_py=Path(DEMO_PY.name), os="debian")
                rtn = python_compile(args)
                self.assertEqual(0, rtn)
                files = os.listdir(tmp_dir)
                pprint(files)
                expected_path_gz: Path = Path("demo_http_server.bin.gz")
                self.assertTrue(expected_path_gz.exists())
                expected_path = Path("demo_http_server.bin.gz")
                self.assertTrue(expected_path.exists())
            finally:
                os.chdir(prev_dir)


if __name__ == "__main__":
    unittest.main()
