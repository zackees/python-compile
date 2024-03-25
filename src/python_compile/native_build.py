import os
import shutil
import sys
import tempfile
import warnings
from atexit import register
from pathlib import Path

from isolated_environment import IsolatedEnvironment, Requirements

# import run_native_windows_build

HERE = Path(__file__).parent
VENV_PATH = HERE / "nuitka_venv"

REQUIREMENTS = [
    "wheel",
    "nuitka==2.1.3",
    "zstandard==0.17.0",
    "chardet==5.2.0",
    "ordered-set==4.1.0",
    "python-dotenv==1.0.0",
    "tqdm==4.66.1",
]

REQS = Requirements(REQUIREMENTS)

USE_GENERIC_FOR_WINDOWS = True
IS_WINDOWS = sys.platform == "win32"


def generate_cmd_list(app_py: Path) -> list[str]:
    """Generate the command list."""
    head_cmd_list = ["python", "-m", "nuitka"]
    body_cmd_list = [
        "--standalone",
        "--follow-imports",
        "--onefile",
        "--lto=yes",
        "--python-flag=-OO",
    ]
    if IS_WINDOWS:
        body_cmd_list.append("--mingw")

    cmd_list = head_cmd_list + body_cmd_list + [str(app_py)]
    return cmd_list


def clean_dir(path: str) -> None:
    """Clean the directory."""
    try:
        shutil.rmtree(path, ignore_errors=True)
    except Exception as e:  # pylint: disable=broad-except
        warnings.warn(f"Failed to clean directory: {path} with error: {e}")


def full_path(path: Path | str) -> str:
    """Get the full path."""
    return str(Path(path).absolute())


def run_native_build(
    app_py: Path, requirements_txt: Path | None, wheel: Path | None
) -> int:
    """Run the native windows build."""
    print("Running native build")
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
        print(f"Creating temporary directory: {full_path(tmp_dir)}")
        full_tmp_path = os.path.abspath(tmp_dir)
        register(clean_dir, full_tmp_path)
        env_path = Path(tmp_dir) / "nuitka_venv"
        iso_env = IsolatedEnvironment(env_path, REQS, full_isolation=True)
        if requirements_txt:
            print(f"Installing requirements from {full_path(requirements_txt)}")
            iso_env.run(["pip", "install", "-r", requirements_txt])
        if wheel:
            print(f"Installing {full_path(wheel)}")
            iso_env.run(["pip", "install", wheel])
        cmd_list: list[str] = generate_cmd_list(app_py)
        iso_env.run(cmd_list)
        basename = app_py.stem
        outexe = f"{basename}.exe" if IS_WINDOWS else f"{basename}.bin.gz"
        print(f"Generated executable: {full_path(outexe)}")
        return 0
