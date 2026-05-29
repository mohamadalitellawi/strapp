---
name: using-uv
description: Use when working in (or setting up) a Python project managed by uv — covers modern uv that older training misses, especially `uv version --bump`, `[dependency-groups]`, the `uv_build` backend, `uv.lock` as the single source of truth, and `uv run`/`uvx`. Reach for this before suggesting pip, virtualenv, `requirements.txt`, `setup.py`, or hand-editing version strings.
---

# Working with uv

`uv` (from Astral) is a single, fast tool that replaces `pip`, `virtualenv`,
`pip-tools`, `pipx`, `poetry`, `pyenv`, and `bump2version`. If a project has a
`uv.lock` file, it is a uv project — **do not reach for `pip` or
`requirements.txt` habits.** Everything below was verified against uv 0.11.17.

## Mental model

- **`pyproject.toml`** declares what you want (deps, version, scripts, tool config).
- **`uv.lock`** records the exact resolved versions. It is committed and is the
  **single source of truth** for what gets installed. Never edit it by hand.
- **`.venv/`** is created and managed for you. You rarely activate it manually.
- **`uv run <cmd>`** is the main entry point: it makes sure the env matches the
  lockfile (auto-syncs and rebuilds the local package), then runs the command.
  You almost never need to `pip install` or `source .venv/bin/activate`.

## Project setup

```bash
uv init --lib --python 3.13   # library-style layout: src/<pkg>/, py.typed
uv init --app                 # app-style layout (no installable package)
uv python install 3.13        # install a Python version uv will use
uv python pin 3.13            # write .python-version
```

## Dependencies — the modern way

```bash
uv add streamlit numpy pandas     # runtime deps -> [project.dependencies]
uv add --dev pytest ruff ty       # dev tools  -> [dependency-groups].dev
uv remove pandas                  # drop a dependency
uv sync                           # install/refresh env from uv.lock
uv lock                           # re-resolve and update uv.lock only
uv lock --upgrade                 # bump deps to newest allowed versions
```

Dev tools go in **`[dependency-groups]`** (PEP 735), the current standard:

```toml
[dependency-groups]
dev = ["pytest>=9.0", "ruff>=0.15", "ty>=0.0.40"]
```

> **Outdated patterns to avoid:** `pip install -r requirements.txt`, a hand-kept
> `requirements.txt`, `[tool.uv] dev-dependencies` (superseded by
> `[dependency-groups]`), and `[project.optional-dependencies]` *for dev tooling*
> (optional-dependencies is for real user-facing extras, not your test/lint set).

## Running things

```bash
uv run python -c "print('hi')"          # python inside the project env
uv run streamlit run streamlit_app.py   # run any installed command
uv run pytest                           # run tests
uv run ruff format && uv run ruff check && uv run ty check && uv run pytest
```

Prefer `uv run python ...` over bare `python`/`python3` — it always uses the
project's own interpreter, identical on macOS, Linux, and Windows.

## Versioning — let uv do it (do NOT hand-edit)

This is the feature most often missed. `uv version --bump` raises the number in
`pyproject.toml` **and** updates `uv.lock` in the same step, so they never drift.

```bash
uv version                       # print current version
uv version --bump patch          # 0.3.2 -> 0.3.3   (fix)
uv version --bump minor          # 0.3.2 -> 0.4.0   (feature)
uv version --bump major          # 0.3.2 -> 1.0.0   (breaking)
uv version --bump minor --dry-run  # preview without writing
# --bump full set: major, minor, patch, stable, alpha, beta, rc, post, dev
```

Keep **one** source of truth for the version: declare it only in
`pyproject.toml` and read it back at runtime instead of duplicating it in code:

```python
# src/<pkg>/__init__.py
from importlib.metadata import PackageNotFoundError, version
try:
    __version__ = version("<pkg>")           # works when installed
except PackageNotFoundError:                  # running straight from source
    import tomllib, pathlib
    _pp = pathlib.Path(__file__).resolve().parents[2] / "pyproject.toml"
    __version__ = tomllib.loads(_pp.read_text())["project"]["version"]
```

This fallback matters: `importlib.metadata.version()` raises
`PackageNotFoundError` when the package is on `sys.path` but was never installed
(e.g. an app imported by file path). We hit and fixed exactly this.

## Build & publish

```bash
uv build                                   # wheel + sdist into dist/
uvx --from dist/<pkg>-X.Y.Z-py3-none-any.whl <cmd>   # try the built CLI, no install
uv publish --token <pypi-token>            # publish to PyPI
uv publish --publish-url https://test.pypi.org/legacy/ --token <token>  # TestPyPI
uvx <tool>                                 # run a tool without installing (= uv tool run)
uv tool install <tool>                     # install a CLI tool globally
```

uv ships its **own build backend** — prefer it over hatchling/setuptools for new
projects:

```toml
[build-system]
requires = ["uv_build>=0.11.17,<0.12.0"]
build-backend = "uv_build"

[project.scripts]
mycli = "mypkg.cli:main"      # installs a `mycli` command
```

## Deployment note

Hosts that auto-detect dependencies (e.g. Streamlit Community Cloud) **prefer
`uv.lock` via `uv sync`** when it is present — installing the exact versions you
tested. So **do not add a `requirements.txt`** to a uv project: it is redundant,
and committing both makes some hosts warn about multiple dependency files. (The
host may still warn because it also counts `pyproject.toml` — that part is
harmless and unavoidable; the log line tells you which file it actually used.)

## Platform differences (the only ones that matter)

| Topic | macOS / Linux | Windows (PowerShell) |
| ----- | ------------- | -------------------- |
| Install uv | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |
| Set env var | `export UV_PUBLISH_TOKEN="..."` | `$env:UV_PUBLISH_TOKEN = "..."` |
| Activate venv by hand | `source .venv/bin/activate` | `.venv\Scripts\Activate.ps1` |

Everything else (`uv add`, `uv run`, `uv build`, `uv version`, ...) is identical
across platforms.

## Quick reference

| Goal | Command |
| ---- | ------- |
| Start a library project | `uv init --lib --python 3.13` |
| Add / remove a runtime dep | `uv add <pkg>` / `uv remove <pkg>` |
| Add a dev tool | `uv add --dev <pkg>` |
| Sync env to the lockfile | `uv sync` |
| Run anything in the env | `uv run <cmd>` |
| Bump the version (+ lockfile) | `uv version --bump patch\|minor\|major` |
| Preview a bump | `uv version --bump <part> --dry-run` |
| Build the package | `uv build` |
| Run a tool without installing | `uvx <tool>` |
| Publish to PyPI | `uv publish --token <token>` |

## Things I (the assistant) tend to get wrong — correct them

- Reaching for `pip install` / `requirements.txt`. Use `uv add` + `uv.lock`.
- Hand-editing the version in `pyproject.toml` or `__init__.py`. Use
  `uv version --bump`, and read the version back via `importlib.metadata`.
- Putting dev tools in `[project.optional-dependencies]` or
  `[tool.uv] dev-dependencies`. Use `[dependency-groups].dev`.
- Defaulting to hatchling/setuptools. For new projects, `uv_build` is simpler.
- Telling users to `source .venv/bin/activate` before running things. `uv run`
  handles the environment for you.
