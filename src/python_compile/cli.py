"""
Main entry point.
"""

import argparse
import sys
from pathlib import Path

from python_compile.compile import DOCKER_FILE_MAP, Args, python_compile

CHOICES = list(DOCKER_FILE_MAP.keys())


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Replace with a description.")
    parser.add_argument(
        "--os",
        type=str,
        help="Which os to use",
        choices=CHOICES,
        required=False,
    )
    parser.add_argument(
        "--platform",
        type=str,
        help="If specified, then the docker platform will be used, like linux/amd64",
        required=False,
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Which python file to run",
    )
    parser.add_argument(
        "--requirements",
        type=Path,
        help="Which requirements file to use",
        required=False,
    )
    parser.add_argument(
        "--wheel",
        type=Path,
        help="Optional wheel file to install",
        required=False,
    )
    return parser.parse_args()


def main() -> int:
    cli_args = parse_args()
    os_system = cli_args.os
    app_py = cli_args.input
    requirements_txt = cli_args.requirements
    wheel = cli_args.wheel
    args = Args(
        app_py=app_py,
        requirements=requirements_txt,
        wheel=wheel,
        os=os_system,
    )
    return python_compile(args)


if __name__ == "__main__":
    sys.argv.append("--os")
    sys.argv.append("debian")
    sys.argv.append("--input")
    sys.argv.append("src/python_compile/assets/demo_http_server.py")
    sys.exit(main())
