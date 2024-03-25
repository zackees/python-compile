"""
Main entry point.
"""

import os
from dataclasses import dataclass
from pathlib import Path

from docker_run_cmd.api import docker_run

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


def docker_build(
    os_system: str, py_path: Path, requirements: Path | None, wheel: Path | None
) -> int:
    dockerpath = DOCKER_FILE_MAP.get(os_system)
    assert dockerpath is not None, f"Unknown os_system: {os_system}"
    extra_files: dict[Path, Path] = {}
    if requirements:
        extra_files[requirements] = Path("requirements.txt")
    if wheel:
        extra_files[wheel] = Path(".compile.whl")

    docker_run(
        name=f"python-compile-{os_system}",
        dockerfile_or_url=dockerpath,
        cwd=os.getcwd(),
        cmd_list=[str(py_path)],
        extra_files=extra_files,
    )
    return 0
