# Step 8 — Practice the team workflow (branches and pull requests)

In [Step 6](06_push_to_github.md) you learned the basics of git: commit, push.
This chapter teaches the **team workflow** — how real teams work together
without stepping on each other's toes. It uses **branches** and **pull
requests**. You can practice all of it on your own, with this repo.

> You do not need a team to practice. You play every role yourself: you write
> the code, you open the pull request, and you review and merge it.

## 8.1 The idea in one picture

This project uses a simple, popular plan called **git-flow**. It has three kinds
of branches:

```
main     ──●────────────────────●──────►   stable, "released" code
            \                   /
develop  ────●────●────────●───●──────────►  the code we are working on
                   \      /
feature        ─────●────●─────────────────  one small piece of new work
```

- **main** — the safe, finished code. We only add to it when we make a release.
- **develop** — where all the day-to-day work comes together.
- **feature/xxx** — a short-lived branch for **one** new thing. When it is done,
  it goes back into `develop`.

> **What is a branch?** Think of it as a separate copy of your code where you can
> try things safely. If you break something, `main` and `develop` are untouched.

## 8.2 The rules we set up on GitHub

We already turned on two safety rules for this repo:

1. **`main` is protected.** You cannot push to it directly. Changes must come in
   through a **pull request**. Force-pushes and deleting the branch are blocked.
2. **`develop` is the default branch.** When you open a pull request, it will
   aim at `develop` automatically.

These rules stop common accidents, like overwriting good code by mistake.

## 8.3 What is a pull request (PR)?

A **pull request** is a polite way of saying:

> "Here are my changes on my branch. Please look at them, and if they are good,
> add them into the main code."

A PR shows exactly what changed, lets people comment, and has a big green button
to merge. On GitHub, "merge" means "copy my branch's changes into the target
branch."

## 8.4 Hands-on practice — make one change the proper way

Let's practice the full loop with a tiny, safe change. Follow along.

### 1. Start from an up-to-date `develop`

Always begin new work from the latest `develop`:

```bash
git switch develop      # move onto the develop branch
git pull                # get the newest version from GitHub
```

### 2. Create a feature branch

Give it a short name that says what you are doing. The `feature/` part is a
folder-like prefix we use for all feature branches:

```bash
git switch -c feature/practice-edit
```

`switch -c` means "create a new branch and move onto it."

### 3. Make a small change

Open `README.md` and add a line, or fix a typo in any doc. Save the file.

### 4. Commit your change

```bash
git add README.md
git commit -m "docs: add a practice line to the README"
```

> **Tip — good commit messages.** Start with a short type, then what you did:
> `docs: ...`, `fix: ...`, `feat: ...`. Keep the first line under ~70 letters.

### 5. Push your branch to GitHub

```bash
git push -u origin feature/practice-edit
```

The `-u` part links your local branch to the one on GitHub, so next time you can
just type `git push`.

### 6. Open the pull request

Two ways:

**Website:** GitHub shows a yellow banner with "Compare & pull request." Click
it. Check the **base** is `develop` (it should be, because we made it the
default). Add a title and a short description. Click **Create pull request**.

**Command line** (with the GitHub CLI):

```bash
gh pr create --base develop --fill
```

`--fill` uses your commit message as the PR title and description.

### 7. Review and merge

In a team, a teammate reads your PR and approves it. On your own, you read it
yourself — actually look at the "Files changed" tab. When happy:

- On the website, click **Merge pull request**, then **Confirm merge**.
- Or on the command line:

  ```bash
  gh pr merge --merge --delete-branch
  ```

`--delete-branch` tidies up the finished feature branch for you.

### 8. Update your local copy

Your change is now in `develop` on GitHub. Bring it down to your computer and
clean up:

```bash
git switch develop
git pull
git branch -d feature/practice-edit    # delete the local branch (already merged)
```

🎉 You just did the full professional loop: branch → commit → push → PR →
review → merge → clean up.

## 8.5 Making a release (sending `develop` into `main`)

When `develop` is tested and you are ready to call it "done," you release it by
merging into the protected `main` branch. Because `main` is protected, this also
goes through a pull request:

```bash
# Open a pull request from develop into main
gh pr create --base main --head develop --title "Release v0.1.0" --fill
```

Review it, merge it on GitHub, then mark the release with a **tag** (a label for
this exact version):

```bash
git switch main
git pull
git tag v0.1.0          # name the release
git push origin v0.1.0  # send the tag to GitHub
```

> **What is a tag?** A tag is a permanent bookmark for one commit. `v0.1.0` lets
> you (and others) find the exact code of that release later.

## 8.6 Quick command cheat sheet

| I want to... | Command |
| ------------ | ------- |
| See which branch I am on | `git branch --show-current` |
| List all branches | `git branch -a` |
| Start new work from develop | `git switch develop && git pull && git switch -c feature/xxx` |
| Save my work | `git add . && git commit -m "..."` |
| Send my branch to GitHub | `git push -u origin feature/xxx` |
| Open a PR into develop | `gh pr create --base develop --fill` |
| Merge my PR and delete the branch | `gh pr merge --merge --delete-branch` |
| Update my local develop | `git switch develop && git pull` |

## 8.7 Habits that keep you out of trouble

- **One branch, one job.** Small branches are easy to review and easy to fix.
- **Pull before you branch.** Always start from the newest `develop`.
- **Never work straight on `main` or `develop`.** Always use a feature branch.
- **Write clear commit messages.** Future-you will thank present-you.
- **Read your own PR** before merging. You will catch small mistakes.

## You finished the whole guide!

You now know the complete, modern workflow: build a project, keep it clean, test
it, package it, put it on GitHub the professional way, and ship it online.
Practice this loop a few times and it will become second nature. Well done! 🏗️
