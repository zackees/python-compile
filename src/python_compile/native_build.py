import subprocess
import sys
import tempfile
from pathlib import Path

from isolated_environment import IsolatedEnvironment, Requirements

# import run_native_windows_build

HERE = Path(__file__).parent
VENV_PATH = HERE / "nuitka_venv"

REQUIREMENTS = [
    "nuitka==2.0.3",
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


def run_native_build(app_py: Path, requirements_txt: Path) -> int:
    """Run the native windows build."""

    print("Running native build")
    with tempfile.TemporaryDirectory() as tmp_dir:
        print(f"Creating temporary directory: {tmp_dir}")
        env_path = Path(tmp_dir) / "nuitka_venv"
        iso_env = IsolatedEnvironment(env_path, REQS)
        subprocess.run(
            ["pip", "install", "-r", requirements_txt],
            env=iso_env.environment(),
            check=True,
        )
        cmd_list: list[str] = generate_cmd_list(app_py)
        subprocess.run(
            cmd_list,
            env=iso_env.environment(),
            check=True,
        )
        return 0
