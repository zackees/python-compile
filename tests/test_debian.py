"""
Unit test file.
"""

import os
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


class NativeTester(unittest.TestCase):
    """Main tester class."""

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
                expected_path_gz: Path = Path("demo_http_server.bin.gz")
                self.assertTrue(expected_path_gz.exists())
                expected_path = Path("demo_http_server.bin")
                self.assertTrue(expected_path.exists())
            finally:
                os.chdir(prev_dir)


if __name__ == "__main__":
    unittest.main()
