"""
Unit test file.
"""

import os
import unittest


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_imports(self) -> None:
        """Test command line interface (CLI)."""
        cmd_list = [
            "python-compile",
            "--os",
            "debian",
            "--input",
            "src/python_compile/assets/demo_http_server.py",
        ]
        rtn = os.system(" ".join(cmd_list))
        self.assertEqual(0, rtn)


if __name__ == "__main__":
    unittest.main()
