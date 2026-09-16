---
name: bootstrap
description: Bootstrap a new Python project with a working pytest harness, git repo, Makefile, and working-agreement AGENTS.md. Use when the user wants to start a new project, scaffold a repo, set up a fresh codebase, get a test loop running from scratch, or says "new project" / "bootstrap" / "scaffold this".
---

Get from an empty directory to a committed project with a passing test run. Target: under 60 seconds.

Never invent the problem domain. This skill creates the harness only — no domain modules, no
guessed abstractions, no placeholder implementation of whatever the user is about to build.

## 1. Settle the target

Infer from the request; ask only what you genuinely cannot:

- **Directory** — if the user named one, use it. Otherwise use the cwd if it is empty, else ask.
- **Package name** — derived from the directory name automatically. Only raise it if the derived name is misleading.

Do not ask about layout, dependencies, or frameworks. The scaffold is opinionated on purpose.

## 2. Run the scaffold

```bash
python3 ~/.cursor/skills/bootstrap/scaffold.py <target_dir>
```

It is idempotent — safe on a dirty or partially set up directory. It creates `pyproject.toml`
(pytest configured), `.gitignore`, `Makefile`, `src/<pkg>/__init__.py`, `tests/test_smoke.py`,
a `.venv` with pytest installed, and a git repo on branch `main`.

If `uv` is missing, fall back to `python3 -m venv .venv && .venv/bin/pip install pytest pytest-timeout`.

## 3. Install the working agreement

```bash
cp ~/.cursor/skills/bootstrap/AGENTS.md <target_dir>/AGENTS.md
```

## 4. Offer test utilities — do not assume

`templates/conftest.py` holds two general-purpose test doubles: an injectable `FakeClock` and a
`run_concurrently` barrier helper. They are only worth adding if the thing being built involves
time or threads.

Ask before copying it, and say plainly that it is generic test infrastructure rather than
anything specific to the problem. If the user declines, or the project has no time or
concurrency dimension, skip it.

```bash
cp ~/.cursor/skills/bootstrap/templates/conftest.py <target_dir>/tests/conftest.py
```

## 5. Prove it and commit

Run the suite and show the real output — never claim it passes without the text.

```bash
cd <target_dir> && make test && git add -A && git commit -m "chore: project scaffold"
```

## 6. Report in three lines

Package name, the test command, and the next action. Nothing else — no summary file, no README,
no description of the directory tree the user can see for themselves.
