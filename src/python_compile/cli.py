"""
Main entry point.
"""
import argparse
import sys
import os
from pathlib import Path

from docker_run_cmd.api import docker_run

HERE = Path(__file__).parent
ASSETS = HERE / "assets"

DOCKER_FILE_MAP = {
    "debian": ASSETS / "debian-dockerfile",
    "windows": ASSETS / "windows-dockerfile",  # Work in progress - cross compilation through fedora
}

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Replace with a description.")
    parser.add_argument(
        "--os",
        type=str,
        help="Which os to use",
        choices=DOCKER_FILE_MAP.keys(),
    )
    parser.add_argument(
        "--py-path",
        type=str,
        help="Which python file to run",
    )
    parser.add_argument(
        "--requirements",
        type=str,
        help="Which requirements file to use",
        required=False,
    )
    return parser.parse_args()



def main() -> int:
    """Main entry point for the template_python_cmd package."""
    args = parse_args()
    print(args)
    os_system = args.os
    if not os_system:
        print("You must provide an os")
        return 1
    dockerpath: Path = DOCKER_FILE_MAP[os_system]
    assert dockerpath.exists(), f"dockerpath {dockerpath} does not exist"
    py_path = args.py_path or args.py_module_path
    py_path = Path(py_path).as_posix()

    assert py_path, "You must provide a python path"

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

if __name__ == "__main__":
    sys.argv.append("--os")
    sys.argv.append("debian")
    sys.argv.append("--py-path")
    sys.argv.append("src/python_compile/assets/demo_http_server.py")
    sys.exit(main())