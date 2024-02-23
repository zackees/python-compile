import subprocess
import tempfile
from pathlib import Path

from isolated_environment import IsolatedEnvironment, Requirements

HERE = Path(__file__).parent
VENV_PATH = HERE / "nuitka_venv"

REQUIREMENTS = [
    "nuitka==2.0.1",
    "zstandard==0.17.0",
    "chardet==5.2.0",
    "ordered-set==4.1.0",
    "python-dotenv==1.0.0",
    "tqdm==4.66.1",
]

REQS = Requirements(REQUIREMENTS)


def run_native_windows_build(app_py: Path, requirements_txt: Path) -> int:
    """Run the native windows build."""
    print("Running native windows build")
    with tempfile.TemporaryDirectory() as tmp_dir:
        print(f"Creating temporary directory: {tmp_dir}")
        env_path = Path(tmp_dir) / "nuitka_venv"
        iso_env = IsolatedEnvironment(env_path, REQS)
        subprocess.run(
            ["pip", "install", "-r", requirements_txt],
            env=iso_env.environment(),
            check=True,
        )
        # python -m nuitka --standalone --follow-imports --onefile --lto=yes --python-flag=-OO "$@"'
        subprocess.run(
            [
                "python",
                "-m",
                "nuitka",
                "--mingw",
                "--standalone",
                "--follow-imports",
                "--onefile",
                "--lto=yes",
                "--python-flag=-OO",
                app_py,
            ],
            env=iso_env.environment(),
            check=True,
        )
        return 0
