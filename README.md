# 🏗️ strapp — Structural Load Combinations

A small, friendly **Streamlit** web app that builds **ASCE 7-22** load
combinations for structural engineers. It is also a complete, beginner-friendly
**teaching project**: every step from an empty folder to a live website is
written down in plain English in the [`docs/`](docs) folder.

> ⚠️ **Teaching tool only.** The numbers are simplified. Do **not** use this for
> a real building. Always check the real ASCE 7 code book and work with a
> licensed engineer.

---

## What the app does

The app has two tabs:

1. **Calculator** — You type your loads (name, type, and size) into a table.
   The app shows every ASCE 7-22 combination, picks the one that **controls the
   design**, draws the math step by step with **handcalcs**, plots the totals
   with **Plotly**, and lets you **download** the results as CSV or JSON.

2. **Simulation** — Real loads are never known exactly. You give a low and high
   value for each load, and the app makes hundreds of random "what if" cases
   using **NumPy**. For each case it finds the controlling combination, then
   marks the **worst case** on a Plotly chart with an arrow.

## What you will learn

- How to start a Python project with the **Astral** tools: `uv`, `ruff`, `ty`.
- How load combinations (LRFD and ASD) work.
- How to build a Streamlit web app and keep the math separate from the page.
- How to test, lint, type-check, build, and publish a package.
- How to put the code on **GitHub** and run it for free on
  **Streamlit Community Cloud**.

## Quick start

You need [`uv`](https://docs.astral.sh/uv/) installed. Then:

```bash
# 1. Get the code
git clone https://github.com/mohamadalitellawi/strapp.git
cd strapp

# 2. Install everything into a private environment
uv sync

# 3. Run the app
uv run streamlit run streamlit_app.py
```

Your browser opens at <http://localhost:8501>.

## Check the project is healthy

```bash
uv run ruff check      # find style problems
uv run ruff format     # tidy the code
uv run ty check        # check the types (ty is in early preview)
uv run pytest          # run the tests
```

## The teaching guide

Read the guides in order. They take you from nothing to a live website:

| Step | Guide |
| ---- | ----- |
| 0 | [What we are building](docs/00_overview.md) |
| 1 | [Set up the project with uv](docs/01_setup_uv_project.md) |
| 2 | [Understand load combinations](docs/02_understanding_load_combinations.md) |
| 3 | [Build the Streamlit app](docs/03_building_the_streamlit_app.md) |
| 4 | [Quality: ruff, ty, and tests](docs/04_quality_ruff_ty_tests.md) |
| 5 | [Build and publish the package](docs/05_build_and_publish_pypi.md) |
| 6 | [Push to GitHub](docs/06_push_to_github.md) |
| 7 | [Put the app online](docs/07_deploy_streamlit_cloud.md) |
| 8 | [Practice the team workflow: branches & pull requests](docs/08_git_workflow_and_pull_requests.md) |
| 9 | [Life after your first release: bug fixes & features](docs/09_after_release_workflow.md) |

## Project layout

```
strapp/
├── streamlit_app.py        # the start file (run this)
├── pyproject.toml          # project settings, dependencies, ruff + ty config
├── requirements.txt        # used by Streamlit Community Cloud
├── src/strapp/
│   ├── combinations.py     # the load combination math (no web code)
│   ├── simulation.py       # the random "what if" study
│   ├── handcalc_view.py    # shows one combination as nice math
│   ├── app.py              # the Streamlit web page
│   ├── cli.py              # the `strapp` command
│   └── _entry.py           # the file Streamlit runs
├── tests/                  # automatic tests
└── docs/                   # the step-by-step teaching guides
```

## License

[MIT](LICENSE) — free to use, learn from, and share.
