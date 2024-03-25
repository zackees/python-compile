"""
Main entry point.
"""

import os
from dataclasses import dataclass
from pathlib import Path

from docker_run_cmd.api import docker_run

from python_compile.native_build import run_native_build

HERE = Path(__file__).parent
ASSETS = HERE / "assets"

DOCKER_FILE_MAP = {
    "debian": ASSETS / "debian-dockerfile",
    "windows": ASSETS
    / "windows-dockerfile",  # Work in progress - cross compilation through fedora
    "native": None,
}


@dataclass
class Args:
    app_py: Path
    requirements: Path | None = None
    pip_install_path: Path | None = None
    os: str | None = None


HERE = Path(__file__).parent
ASSETS = HERE / "assets"


def python_compile(args: Args) -> int:
    """Main entry point for the template_python_cmd package."""
    os_system = args.os
    app_py = args.app_py
    requirements_txt = args.requirements
    pip_install_path = args.pip_install_path
    if os_system == "windows":
        if os.name != "nt":
            # Work in progress, compile windows apps from docker.
            print("You must run this on a windows machine")
            return 1
        rtn = run_native_build(
            app_py=app_py,
            requirements_txt=requirements_txt,
            pip_install_path=pip_install_path,
        )
        return rtn
    if os_system is None or os_system == "native":
        rtn = run_native_build(
            app_py=app_py,
            requirements_txt=requirements_txt,
            pip_install_path=pip_install_path,
        )
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
