"""
Main entry point.
"""

import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path

from docker_run_cmd.api import docker_run

from python_compile.native_build import run_native_build


@dataclass
class Args:
    app_py: Path
    requirements: Path | None = None
    os: str | None = None


HERE = Path(__file__).parent
ASSETS = HERE / "assets"

DOCKER_FILE_MAP = {
    "debian": ASSETS / "debian-dockerfile",
    "windows": ASSETS
    / "windows-dockerfile",  # Work in progress - cross compilation through fedora
    "native": None,
}


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Replace with a description.")
    parser.add_argument(
        "--os",
        type=str,
        help="Which os to use",
        choices=DOCKER_FILE_MAP.keys(),
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
    return parser.parse_args()


def run(args: Args) -> int:
    """Main entry point for the template_python_cmd package."""
    os_system = args.os
    app_py = args.app_py
    requirements_txt = args.requirements
    if os_system == "windows":
        if os.name != "nt":
            # Work in progress, compile windows apps from docker.
            print("You must run this on a windows machine")
            return 1
        rtn = run_native_build(app_py=app_py, requirements_txt=requirements_txt)
        return rtn
    if os_system is None or os_system == "native":
        rtn = run_native_build(app_py=app_py, requirements_txt=requirements_txt)
        return rtn

    dockerpath: Path | None = DOCKER_FILE_MAP.get(os_system)
    if dockerpath is None:
        print(f"OS {os_system} is not supported")
        return 1
    assert dockerpath.exists(), f"dockerpath {dockerpath} does not exist"
    py_path = args.app_py
    assert Path(py_path).as_posix(), "You must provide a python path"

    extra_files: dict[Path, Path] = {}
    if args.requirements:
        extra_files[Path(args.requirements)] = Path("requirements.txt")

    docker_run(
        name=f"python-compile-{os_system}",
        dockerfile_or_url=dockerpath,
        cwd=os.getcwd(),
        cmd_list=[py_path],
        extra_files=extra_files,
    )
    return 0


def main() -> int:
    cli_args = parse_args()
    os_system = cli_args.os
    app_py = cli_args.input
    requirements_txt = cli_args.requirements
    args = Args(app_py=app_py, requirements=requirements_txt, os=os_system)
    return run(args)


if __name__ == "__main__":
    sys.argv.append("--os")
    sys.argv.append("debian")
    sys.argv.append("--py-path")
    sys.argv.append("src/python_compile/assets/demo_http_server.py")
    sys.exit(main())
