#!/usr/bin/env python3
"""Run all documentation generator scripts in a fixed order."""

from pathlib import Path
import shutil
import subprocess
import sys


SCRIPTS = [
    "generators/generate_events.py",
    "generators/generate_training_catalogue_aliases.py",
    "generators/generate_scientific_domains.py",
    "generators/generate_learning_paths.py",
    "generators/generate_bundles.py",
    "generators/generate_tags.py",
]


def main() -> int:
    scripts_dir = Path(__file__).resolve().parent

    for script_name in SCRIPTS:
        script_path = scripts_dir / script_name
        if not script_path.exists():
            print(f"Error: missing script {script_path}")
            return 1

        print(f"Running {script_name}...")
        result = subprocess.run([sys.executable, str(script_path)], check=False)
        if result.returncode != 0:
            print(f"Error: {script_name} failed with exit code {result.returncode}")
            return result.returncode

    zensical_exe = Path(sys.executable).resolve().parent / "zensical"
    zensical_cmd = str(zensical_exe) if zensical_exe.exists() else shutil.which("zensical")
    if not zensical_cmd:
        print(
            "Error: missing zensical executable in interpreter bin and PATH"
        )
        return 1

    print("Running zensical build...")
    build_result = subprocess.run([zensical_cmd, "build"], check=False)
    if build_result.returncode != 0:
        print(f"Error: zensical build failed with exit code {build_result.returncode}")
        return build_result.returncode

    print("All generators and build completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())