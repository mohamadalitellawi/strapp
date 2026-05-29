# CLAUDE.md

Guidance for Claude Code (and other AI agents) working in this repository.

## What this project is

`strapp` is a small **Streamlit** web app that builds **ASCE 7-22** structural
load combinations. It is also a **teaching project**: the `docs/` folder walks a
beginner from an empty folder to a deployed app, in plain English. Two audiences
matter — structural engineers learning Python, and juniors learning the modern
Python workflow. Keep that in mind: prefer clear, simple code and explanations
over clever ones.

> Teaching tool only — the load math is simplified and must not be used for real
> design. Do not present it as production-accurate.

## Tooling

- **Python ≥ 3.13**, managed with **`uv`** (not pip/poetry/conda).
- Lint/format: **ruff**. Types: **ty** (early preview). Tests: **pytest**.

## Common commands

```bash
uv sync                                # install deps into .venv
uv run streamlit run streamlit_app.py  # run the app locally (http://localhost:8501)
uv run strapp                          # run via the installed CLI entry point

uv run ruff format                     # format
uv run ruff check                      # lint  (add --fix to auto-fix)
uv run ty check                        # type-check
uv run pytest                          # tests

# all four checks before sharing:
uv run ruff format && uv run ruff check && uv run ty check && uv run pytest
```

## Layout

```
streamlit_app.py        # root entry: puts src/ on sys.path, calls strapp.app.main
src/strapp/
  combinations.py       # pure load-combination math (no Streamlit/UI imports)
  simulation.py         # NumPy Monte-Carlo "what if" study
  handcalc_view.py      # renders one combination as handcalcs LaTeX
  app.py                # the Streamlit page (Calculator + Simulation tabs)
  cli.py                # the `strapp` command
  _entry.py             # file Streamlit launches
docs/                   # step-by-step teaching guides (00–09 + appendices)
tests/                  # pytest suite (uses Streamlit AppTest)
```

Keep the **math layer pure**: `combinations.py` and `simulation.py` must not
import Streamlit. UI code lives in `app.py` / `handcalc_view.py`.

## Conventions

- Functional style: pure functions over stateful classes where practical.
- Type hints + short docstrings on new functions. Don't retrofit untouched code.
- Default to **no comments**; add one only when the *why* is non-obvious.
- Line length 100. ruff rule set: `E W F I UP B SIM`.

## Critical gotcha — handcalcs rendering

`handcalcs` (with `@handcalc(jupyter_display=False)`) returns a `(latex, value)`
tuple whose LaTeX is already wrapped in `$ ... $`. Render it with
**`st.markdown(latex)`**, never `st.latex(latex)` — `st.latex` adds its own math
mode and double-wraps, showing raw `\begin{aligned}` text. This has bitten us
before. See the appendix cheat sheet, Part 2.

## Versioning

`pyproject.toml` is the **single source of truth** for the version.
`src/strapp/__init__.py` reads it back dynamically (`importlib.metadata`, with a
`tomllib` fallback for source runs). **Never** hand-edit version strings. Bump
with the command, which updates `pyproject.toml` **and** `uv.lock` together:

```bash
uv version --bump patch   # 0.2.2 -> 0.2.3  (fix)
uv version --bump minor   # 0.2.2 -> 0.3.0  (feature)
uv version --bump major   # 0.2.2 -> 1.0.0  (breaking)
```

## Git workflow (git-flow)

- Branch off `develop`: `feature/<name>`, `bugfix/<name>`, `chore/<name>`.
- **Squash-merge** feature/bugfix/chore PRs into `develop`.
- Release: open a `develop -> main` PR and merge with a **merge commit**
  (`gh pr merge --merge`), then **tag** `vX.Y.Z` on `main`.
- After a release, sync `develop` with `main`.
- Full details in `docs/08` and `docs/09`.

Do **not** commit or push unless explicitly asked. Never commit secrets. Don't
run destructive git commands without confirmation.

## Deployment

Streamlit Community Cloud deploys from `main`, entry `streamlit_app.py`, and
installs dependencies from **`uv.lock`** via `uv sync`. There is intentionally
**no `requirements.txt`**. The cloud still prints a *"more than one requirements
file detected"* warning because it also counts `pyproject.toml` — this is
harmless and unavoidable; the logs confirm it uses `uv-sync with uv.lock`. To add
a dependency: `uv add <lib>`, commit, push.

## Docs style

`docs/` is written for beginners in plain English. When editing guides, match
that voice, keep `<angle-bracket>` placeholders generic in the appendices, and
keep command examples copy-pasteable and cross-platform where it matters.
