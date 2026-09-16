#!/usr/bin/env python3
"""Bootstrap a Python project with pytest, git, and a Makefile. Idempotent.

usage: scaffold.py [target_dir]   (defaults to cwd)
"""
import re
import subprocess
import sys
from pathlib import Path

FILES = {
    "pyproject.toml": """\
[project]
name = "{pkg}"
version = "0.1.0"
requires-python = ">=3.11"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q --timeout=10"
""",
    ".gitignore": """\
__pycache__/
*.py[cod]
.venv/
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
.DS_Store
""",
    "Makefile": """\
.PHONY: test watch cov clean

test:
\t.venv/bin/pytest

watch:
\t.venv/bin/pytest -q --tb=short -x

cov:
\t.venv/bin/pytest --cov=src --cov-report=term-missing

clean:
\trm -rf .pytest_cache .coverage htmlcov
""",
    "src/{pkg}/__init__.py": "",
    "tests/test_smoke.py": """\
def test_harness_runs():
    assert True
""",
}


def run(cmd: list[str], cwd: Path) -> bool:
    """Run cmd, return True on success. Output suppressed unless it fails."""
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  ! {' '.join(cmd)}\n{r.stderr.strip()}", file=sys.stderr)
    return r.returncode == 0


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    root.mkdir(parents=True, exist_ok=True)
    pkg = re.sub(r"\W|^(?=\d)", "_", root.name).strip("_").lower() or "app"

    for tmpl, body in FILES.items():
        path = root / tmpl.format(pkg=pkg)
        if path.exists():
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body.format(pkg=pkg))
        print(f"  + {path.relative_to(root)}")

    if not (root / ".venv").exists():
        run(["uv", "venv", "--quiet"], root)
    run(["uv", "pip", "install", "--quiet", "pytest", "pytest-timeout", "pytest-cov"], root)

    if not (root / ".git").exists():
        run(["git", "init", "--quiet", "--initial-branch=main"], root)

    ok = run([".venv/bin/pytest", "-q"], root)
    print(f"\n{root}  package={pkg}  tests={'PASS' if ok else 'FAIL'}")
    print("next: make test")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
