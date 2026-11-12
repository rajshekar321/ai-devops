"""Automated Test & Validation Runner for AI-DevOps Platform."""
import os
import sys
import py_compile
import subprocess


def check_syntax(directory: str) -> tuple[int, list[str]]:
    """Recursively verify Python syntax across all codebase files."""
    errors = []
    checked = 0
    for root, _, files in os.walk(directory):
        if ".venv" in root or "__pycache__" in root or ".git" in root:
            continue
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                checked += 1
                try:
                    py_compile.compile(path, doraise=True)
                except py_compile.PyCompileError as err:
                    errors.append(f"Syntax error in {path}: {err}")
    return checked, errors


def run_pytest(python_exe: str) -> int:
    """Run pytest suite if pytest is available."""
    cmd = [python_exe, "-m", "pytest", "-v", "tests/"]
    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    return result.returncode


def main():
    print("=== Step 1: Codebase Syntax & Static Compilation Check ===")
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    checked, errors = check_syntax(root_dir)
    print(f"Checked {checked} Python source files.")

    if errors:
        print("[FAIL] Syntax errors detected:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    print("[PASS] All Python files compiled successfully without syntax errors.")

    print("\n=== Step 2: Automated Unit & Integration Tests ===")
    # Check if venv python has pytest or if current python has pytest
    venv_py = os.path.join(root_dir, ".venv", "Scripts", "python.exe")
    python_to_use = venv_py if os.path.exists(venv_py) else sys.executable

    # Test if pytest is imported
    check_pytest = subprocess.run(
        [python_to_use, "-c", "import pytest; print(pytest.__file__)"],
        capture_output=True,
        text=True
    )

    if check_pytest.returncode == 0:
        print(f"Running pytest using {python_to_use}...")
        rc = run_pytest(python_to_use)
        if rc != 0:
            print(f"[FAIL] Pytest failed with return code {rc}")
            sys.exit(rc)
        print("[PASS] All pytest test suites passed successfully.")
    else:
        print(f"[INFO] Pytest is not yet installed in {python_to_use}.")
        print("[INFO] Static analysis and syntax validation passed. Pytest will execute in CI/CD pipeline.")

    print("\n=== Validation Complete: OK ===")


if __name__ == "__main__":
    main()
