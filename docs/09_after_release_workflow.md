# Step 9 — Life after your first release (fixing bugs and adding features)

You made your first release in [Step 8](08_git_workflow_and_pull_requests.md):
you merged `develop` into `main` and tagged it `v0.1.0`. 🎉

So... what happens **next**? You will find a bug, or think of a new feature, and
you will want to ship it. This chapter shows you the full loop you repeat for
the rest of the project's life.

> Everything here builds on Step 8. If branches and pull requests are still
> fuzzy, read that chapter first.

## 9.1 The one thing people forget: sync `develop` first

Right after a release, `main` has **one commit that `develop` does not** — the
"merge commit" that GitHub made when you merged the release. Here is the picture:

```
main     ──●──────────────●  ← the release merge commit lives here
            \             /
develop  ────●───────────●   ← develop is missing that last commit
```

If you start new work without fixing this, your next release pull request has to
"catch up" on that missing commit, and git can show **confusing fake conflicts**.
The fix is quick and safe. Do it **every time, right after a release**:

```bash
git switch develop      # go to develop
git pull                # get the newest develop from GitHub
git merge main          # bring main's release commit into develop
git push                # send it back up (develop is not protected)
```

> **Will this cause a conflict?** No. Because nothing new has happened on
> `develop` since the release, git just slides `develop` forward to match `main`.
> This clean, no-conflict move is called a **fast-forward**. After it, `develop`
> and `main` point at the exact same code — a perfect, level starting line.

> **Why does this work so smoothly?** Because in Step 8 you released with a
> **merge commit, not a squash** (see Section 8.4). That kept `main` and
> `develop` sharing the same history, which is exactly what lets git
> fast-forward here. This is the payoff for picking the right merge button.

## 9.2 The normal loop: fix a bug or add a feature

This is the same loop from Section 8.5, now that you know to sync first. Whether
it is a bug or a feature, the steps are identical — only the branch name changes.

### 1. Start from a fresh `develop`

```bash
git switch develop
git pull
```

### 2. Make a branch with a clear name

Use `bugfix/` for fixes and `feature/` for new things. The prefix is just a
folder-like label that keeps your branches tidy:

```bash
git switch -c bugfix/snow-load-factor      # a fix
# or
git switch -c feature/wind-uplift-case     # a new feature
```

### 3. Change the code, commit, push

```bash
git add src/strapp/combinations.py
git commit -m "fix: correct the snow load factor"
git push -u origin bugfix/snow-load-factor
```

> **Tip — message prefixes.** `fix:` for a bug, `feat:` for a feature,
> `docs:` for documentation. Keep the first line under ~70 letters.

### 4. Open a pull request into `develop` and squash-merge it

```bash
gh pr create --base develop --fill
gh pr merge --squash --delete-branch
```

Remember the rule from Section 8.4: merging **into `develop`** always uses
**squash**. It turns your little commits into one clean commit on `develop`.

### 5. Tidy your local copy

```bash
git switch develop
git pull
git branch -D bugfix/snow-load-factor      # capital -D after a squash merge
```

> **Why capital `-D`?** A squash merge made a brand-new commit, so git does not
> recognise your old branch as "merged" and the safe `-d` refuses. The capital
> `-D` says "delete it anyway," which is correct — the work is safely in
> `develop`. (Same reason as Section 8.5, Step 8.)

## 9.3 Ship the next release

When `develop` has the fixes and features you want, and you have tested it, you
release it. There are two small steps: **raise the version number**, then merge
`develop` into `main`.

#### Step A — raise the version number (on `develop` first)

Pick which part to raise (see the table below), then let uv do it. Because this
is a change to `develop`, do it on a short branch and merge it in — the same
loop as Section 9.2:

```bash
git switch develop && git pull
git switch -c chore/bump-version
uv version --bump minor     # or patch / major — see the table below
git add pyproject.toml uv.lock
git commit -m "chore: bump version"
git push -u origin chore/bump-version
gh pr create --base develop --fill
gh pr merge --squash --delete-branch
```

> **Why `uv version --bump` and not editing the number by hand?** It raises the
> number in `pyproject.toml` **and** updates `uv.lock` in one go, so the two can
> never drift apart. Our code reads the version back from `pyproject.toml`
> automatically (see Section 5.3), so there is nothing else to change. Add
> `--dry-run` to preview without writing.

#### Step B — merge `develop` into `main` and tag

Now release it exactly like the first time (Section 8.6):

```bash
git switch develop && git pull   # get the version bump you just merged
gh pr create --base main --head develop --title "Release v0.2.0" --fill
```

Merge it on GitHub with **"Create a merge commit"** — **not** squash. Then tag
the new version (the tag should match the number `uv version` set):

```bash
git switch main
git pull
git tag v0.2.0            # the new version label
git push origin v0.2.0    # send the tag to GitHub
```

Finally, **sync `develop` again** (Section 9.1), because `main` now has a new
release commit. Then you are ready for the next piece of work.

### What number do I give the release?

Versions follow a simple pattern called **semver** (semantic versioning):
`MAJOR.MINOR.PATCH`, like `0.1.1`. The command in Step A picks the part for you:

| What you shipped | Command | Example |
| ---------------- | ------- | ------- |
| A bug fix only | `uv version --bump patch` | `0.1.0` → `0.1.1` |
| A new feature (nothing broken for users) | `uv version --bump minor` | `0.1.1` → `0.2.0` |
| A big change that breaks how people use it | `uv version --bump major` | `0.9.0` → `1.0.0` |

> While you are still below `1.0.0`, the project is saying "early days, things
> may still change." That is perfectly normal for a learning project.

## 9.4 The emergency exception: a hotfix

Sometimes the **live website** is broken right now and you cannot wait for the
normal `develop` cycle. That is a **hotfix**: a fix that goes straight to `main`.

```
main     ──●──────●──●  ← branch from main, fix, merge straight back to main
            \      \  \
develop  ────●──────\──●  ← then merge the same fix down into develop too
```

```bash
git switch main
git pull
git switch -c hotfix/crash-on-empty-table   # branch from main, not develop

# ...make the fix, commit, push...
git push -u origin hotfix/crash-on-empty-table

# PR straight into main (main is protected, so it still needs a PR)
gh pr create --base main --head hotfix/crash-on-empty-table --fill
```

Bump the version with `uv version --bump patch` as part of the fix, merge it
into `main` with a **merge commit**, then **tag that patch version**
(e.g. `v0.1.2`). Last and most important: **merge `main` back into `develop`**
(Section 9.1) so your fix is not lost the next time you release.

> **When is it really a hotfix?** Only when the live app is broken and waiting is
> not an option. For everything else — almost always — use the normal loop in
> Section 9.2. Branching from `main` is the exception, not the habit.

## 9.5 Quick cheat sheet

| I want to... | Commands |
| ------------ | -------- |
| Sync develop after a release | `git switch develop && git pull && git merge main && git push` |
| Start a bug fix | `git switch develop && git pull && git switch -c bugfix/xxx` |
| Start a feature | `git switch develop && git pull && git switch -c feature/xxx` |
| Merge my PR into develop | `gh pr merge --squash --delete-branch` |
| Raise the version number | `uv version --bump patch` (or `minor` / `major`) |
| Cut a release | `gh pr create --base main --head develop --title "Release vX.Y.Z" --fill` |
| Tag the release | `git switch main && git pull && git tag vX.Y.Z && git push origin vX.Y.Z` |

## 9.6 The rhythm to remember

1. **Sync** `develop` with `main` right after every release.
2. **Branch** from `develop` for each fix or feature.
3. **Squash-merge** that branch back into `develop`.
4. **Bump** the version with `uv version --bump` (on `develop`), ready to release.
5. **Release** by merging `develop` into `main` with a merge commit, then **tag**.
6. **Sync** again. Repeat forever.

That five-beat rhythm is the whole professional life of a project. Practice it a
few times on this repo and it will feel automatic. Well done! 🏗️
