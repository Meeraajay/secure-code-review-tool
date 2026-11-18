
import json
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def run_bandit(repository_path: str, python_files: list[str]) -> str:
    repository = Path(repository_path).resolve()

    output_directory = PROJECT_ROOT / "scan_results" / repository.name
    output_directory.mkdir(parents=True, exist_ok=True)

    output_file = output_directory / "bandit_results.json"
    output_file.unlink(missing_ok=True)

    files = [str(Path(file).resolve()) for file in python_files]

    command = [
        sys.executable,
        "-m",
        "bandit",
        "-f",
        "json",
        "-o",
        str(output_file),
        *files
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300
    )

    if not output_file.exists():
        raise RuntimeError(f"Bandit failed: {result.stderr}")

    with output_file.open("r", encoding="utf-8") as file:
        json.load(file)

    return str(output_file)


def run_semgrep(repository_path: str, python_files: list[str]) -> str:
    repository = Path(repository_path).resolve()

    output_directory = PROJECT_ROOT / "scan_results" / repository.name
    output_directory.mkdir(parents=True, exist_ok=True)

    output_file = output_directory / "semgrep_results.json"
    output_file.unlink(missing_ok=True)

    semgrep_executable = (
        PROJECT_ROOT / ".venv-semgrep" / "Scripts" / "semgrep.exe"
    )

    if not semgrep_executable.exists():
        raise FileNotFoundError("Semgrep executable not found")

    files = [str(Path(file).resolve()) for file in python_files]

    command = [
        str(semgrep_executable),
        "scan",
        "--config",
        "auto",
        "--json",
        "--output",
        str(output_file),
        *files
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=300
    )

    if not output_file.exists():
        raise RuntimeError(
            f"Semgrep failed: {result.stderr or result.stdout}"
        )

    with output_file.open("r", encoding="utf-8") as file:
        json.load(file)

    return str(output_file)


def run_all_scanners(repository_path: str, python_files: list[str]) -> dict:

    if not python_files:
        raise ValueError("No Python files available for scanning")

    results = {}

    results["bandit"] = run_bandit(repository_path, python_files)
    results["semgrep"] = run_semgrep(repository_path, python_files)

    return {
        "message": "All security scans completed successfully",
        "repository": repository_path,
        "python_file_count": len(python_files),
        "reports": results
    }
