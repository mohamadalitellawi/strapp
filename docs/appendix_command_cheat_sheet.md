# Appendix — Command cheat sheet (Steps 1–9)

Every terminal command used across the guide, in one place. It is written
**generically** so you can reuse it for any project: replace the parts in
`<angle brackets>` with your own names (for example `<project>`, `<package>`,
`<entry>.py`, `v<X.Y.Z>`).

## How to read this sheet

- 🍎 = **macOS** (Terminal / iTerm, usually the **zsh** or **bash** shell).
- 🪟 = **Windows 11** (**PowerShell** — the recommended shell on Windows).
- A command with **no flag** works the **same on both**. Only where the two
  systems truly differ do you see a 🍎 / 🪟 pair.

> **Good news:** `uv`, `git`, and `gh` are cross-platform. The overwhelming
> majority of commands below are **identical** on macOS and Windows 11. The real
> differences are short and listed in the last section.

---

## A. Platform differences (read this once)

These are the only places the two systems part ways.

### A.1 Installing uv

🍎 **macOS / Linux** (uses `curl` and the shell installer):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

🪟 **Windows 11** (uses PowerShell and the PowerShell installer):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installing, **both** check the same way:

```bash
uv --version
```

### A.2 Setting an environment variable (e.g. a publish token)

🍎 **macOS** (zsh / bash):

```bash
export UV_PUBLISH_TOKEN="<your-token>"
```

🪟 **Windows 11** (PowerShell):

```powershell
$env:UV_PUBLISH_TOKEN = "<your-token>"
```

### A.3 Activating a virtual environment by hand

You rarely need this because `uv run` does it for you — but if you ever want to
activate `.venv` manually:

🍎 **macOS** (zsh / bash):

```bash
source .venv/bin/activate
```

🪟 **Windows 11** (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

### A.4 Small things to know

| Topic | 🍎 macOS | 🪟 Windows 11 |
| ----- | -------- | ------------- |
| Python program name | often `python3` | `python` |
| List files in a folder | `ls` | `ls` (works in PowerShell) or `dir` |
| Path separator (native) | `/` | `\` — but `/` also works in `uv`, `git`, `gh` |
| Show current folder | `pwd` | `pwd` (works in PowerShell) |

> **Tip:** Prefer `uv run python ...` over `python` / `python3`. It always uses
> the project's own Python, so the name is the same on every machine.

---

## B. Set up a project — uv (Step 1)

| Goal | Command |
| ---- | ------- |
| Check uv is installed | `uv --version` |
| Make and enter a project folder | `mkdir <project>` then `cd <project>` |
| Start a library-style project | `uv init --lib --python <version>` |
| Add runtime libraries | `uv add <package> [<package> ...]` |
| Add developer-only tools | `uv add --dev <package> [<package> ...]` |
| Remove a library | `uv remove <package>` |
| Run anything inside the project | `uv run <command>` |
| Quick Python one-liner | `uv run python -c "print('hello')"` |
| Re-sync the environment to the lock file | `uv sync` |

---

## C. Run the app and check quality (Steps 3–4)

| Goal | Command |
| ---- | ------- |
| Run a Streamlit app | `uv run streamlit run <entry>.py` |
| Find style problems & small bugs | `uv run ruff check` |
| Auto-fix what ruff can | `uv run ruff check --fix` |
| Tidy formatting (spacing, quotes) | `uv run ruff format` |
| Check types | `uv run ty check` |
| Run the tests | `uv run pytest` |
| All four checks before sharing | `uv run ruff format && uv run ruff check && uv run ty check && uv run pytest` |

---

## D. Build, version, and publish (Step 5)

| Goal | Command |
| ---- | ------- |
| Build wheel + source archive into `dist/` | `uv build` |
| Try the built command without installing | `uvx --from <path-to-wheel>.whl <command>` |
| Show the current version | `uv version` |
| Bump a tiny fix | `uv version --bump patch` |
| Bump a new feature | `uv version --bump minor` |
| Bump a breaking change | `uv version --bump major` |
| Preview a bump without writing it | `uv version --bump <part> --dry-run` |
| Publish to TestPyPI (practice) | `uv publish --publish-url https://test.pypi.org/legacy/ --token <token>` |
| Publish to PyPI (real) | `uv publish --token <token>` |
| Install a published tool | `uv tool install <package>` |

> `uv version --bump` raises the number in `pyproject.toml` **and** updates
> `uv.lock` together, so they never drift apart.

---

## E. git basics & first push to GitHub (Step 6)

| Goal | Command |
| ---- | ------- |
| See what changed | `git status` |
| Stage specific files | `git add <file> [<file> ...]` |
| Stage everything | `git add .` |
| Save a commit | `git commit -m "<message>"` |
| Connect to a GitHub repo | `git remote add origin <repo-url>` |
| Rename the current branch to main | `git branch -M main` |
| First push (and remember the link) | `git push -u origin main` |
| Push later changes | `git push` |
| Create the repo with the GitHub CLI | `gh repo create <name> --public --source=. --push` |

---

## F. Updating a deployed app (Step 7)

The whole update is just the save-and-push trio:

```bash
git add .
git commit -m "<what you changed>"
git push
```

The hosting service notices the new commit and redeploys on its own.

---

## G. Branch & pull-request workflow (Step 8)

| Goal | Command |
| ---- | ------- |
| Show the current branch | `git branch --show-current` |
| List all branches (local + remote) | `git branch -a` |
| Move to a branch | `git switch <branch>` |
| Get the newest version of it | `git pull` |
| Start a new branch from here | `git switch -c <type>/<short-name>` |
| Stage & commit your work | `git add <file>` then `git commit -m "<message>"` |
| Push a new branch (and link it) | `git push -u origin <type>/<short-name>` |
| Open a PR into develop | `gh pr create --base develop --fill` |
| Merge a feature PR (squash) | `gh pr merge --squash --delete-branch` |
| Delete a local branch after a squash merge | `git branch -D <branch>` |

> **`-d` vs `-D`:** after a **squash** merge, git does not see the branch as
> "merged" (the squash made a new commit), so the gentle `git branch -d` refuses.
> The capital `git branch -D` deletes it anyway — correct here, because the work
> is safely on the target branch.

---

## H. After-release workflow (Step 9)

| Goal | Command |
| ---- | ------- |
| Sync develop with main after a release | `git switch develop && git pull && git merge main && git push` |
| Start a bug fix | `git switch develop && git pull && git switch -c bugfix/<name>` |
| Start a feature | `git switch develop && git pull && git switch -c feature/<name>` |
| Raise the version (on develop) | `uv version --bump <patch\|minor\|major>` |
| Open the release PR (develop → main) | `gh pr create --base main --head develop --title "Release v<X.Y.Z>" --fill` |
| Merge a release PR (keep a merge commit) | `gh pr merge --merge` |
| Tag the release | `git switch main && git pull && git tag v<X.Y.Z> && git push origin v<X.Y.Z>` |
| Start an emergency hotfix (from main) | `git switch main && git pull && git switch -c hotfix/<name>` |
| Tidy stale remote-tracking refs locally | `git fetch --prune` |

> **Squash vs merge commit:** merge a **feature/bugfix into develop** with
> **squash** (`--squash`); merge **develop into main** for a release with a
> **merge commit** (`--merge`). This keeps long-lived branches sharing history.

---

## I. The smallest set to memorise

If you remember only these, you can do almost everything:

```bash
uv add <package>          # get a library
uv run <command>          # run inside the project
uv run pytest             # test
git switch -c <branch>    # start work
git add . && git commit -m "<msg>"   # save
git push -u origin <branch>          # share
gh pr create --fill       # ask to merge
```
