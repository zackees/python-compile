"""
Main entry point.
"""

import os
from dataclasses import dataclass
from pathlib import Path

from python_compile.docker_build import docker_build
from python_compile.native_build import run_native_build


@dataclass
class Args:
    app_py: Path
    requirements: Path | None = None
    wheel: Path | None = None
    os: str | None = None


def python_compile(args: Args) -> int:
    """Main entry point for the template_python_cmd package."""
    os_system = args.os
    app_py = args.app_py
    requirements_txt = args.requirements
    wheel = args.wheel
    if os_system == "windows":
        if os.name != "nt":
            # Work in progress, compile windows apps from docker.
            print("You must run this on a windows machine")
            return 1
        rtn = run_native_build(
            app_py=app_py,
            requirements_txt=requirements_txt,
            wheel=wheel,
        )
        return rtn
    if os_system is None or os_system == "native":
        rtn = run_native_build(
            app_py=app_py,
            requirements_txt=requirements_txt,
            wheel=wheel,
        )
        return rtn
    docker_build(
        os_system=os_system,
        py_path=app_py,
        requirements=requirements_txt,
        wheel=wheel,
    )
    return 0
