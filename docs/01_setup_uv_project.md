# Step 1 — Set up the project with uv

In this step we make an empty project come to life. We use **uv**, a fast tool
from a company called **Astral**. It does the jobs that older tools like `pip`
and `virtualenv` used to do, but faster and in one place.

## 1.1 Install uv

If you do not have uv yet, install it (see the
[official guide](https://docs.astral.sh/uv/getting-started/installation/)).
On macOS or Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Check it works:

```bash
uv --version
```

## 1.2 Make the project folder

Pick a name. We use `strapp` (short for "structural app").

```bash
mkdir strapp
cd strapp
```

## 1.3 Start the project

We build this as a small **library** (a reusable piece of code) plus an app.
The `--lib` option sets up a clean folder shape for us:

```bash
uv init --lib --python 3.13
```

This creates:

```
strapp/
├── .python-version      # says "use Python 3.13"
├── .gitignore           # files git should ignore
├── pyproject.toml       # the project's settings file
├── README.md
└── src/strapp/
    ├── __init__.py
    └── py.typed         # says "this package has type hints"
```

> **Why a `src/` folder?** Putting the code inside `src/` is a common, safe
> habit. It stops Python from accidentally importing your code before it is
> properly installed, which avoids confusing bugs.

## 1.4 Add the libraries the app needs

These are the tools the app uses while it runs:

```bash
uv add streamlit numpy pandas matplotlib plotly handcalcs
```

`uv` writes them into `pyproject.toml` and locks the exact versions in a file
called `uv.lock`. The lock file means everyone gets the **same** versions.

## 1.5 Add the developer tools

These tools help us while we build, but the app does not need them to run. So we
put them in a separate "dev" group:

```bash
uv add --dev pytest ruff ty
```

## 1.6 What is `pyproject.toml`?

This one file describes your whole project: its name, version, the libraries it
needs, and settings for tools like ruff and ty. Open it and have a look. Here is
the important part with comments:

```toml
[project]
name = "strapp"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [          # libraries the app needs to run
    "streamlit>=1.58.0",
    "numpy>=2.4.6",
    # ... and so on
]

[tool.ruff]              # settings for the ruff tool (Step 4)
line-length = 100

[tool.ty.environment]    # settings for the ty tool (Step 4)
python-version = "3.13"
```

## 1.7 Run something

`uv run` runs a command inside the project's private environment. Try Python:

```bash
uv run python -c "print('hello from strapp')"
```

The first time, uv quietly creates a `.venv` folder and installs everything.

## You are done with Step 1

You now have a working, empty project. Next we learn the engineering idea behind
the app: [Step 2 — Understand load combinations](02_understanding_load_combinations.md).
