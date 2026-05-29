# Step 6 — Push to GitHub

**GitHub** is a website that stores code. Putting your project there means:

- You have a safe backup.
- Others can read and learn from it.
- Streamlit Community Cloud (Step 7) can read it to run your app.

## 6.1 What is git? What is GitHub?

- **git** is a tool on your computer that records the history of your project.
  Each saved point is called a **commit**.
- **GitHub** is a website that keeps a copy of your git history online.

`uv init` already started git for you. You can check:

```bash
git status
```

## 6.2 Make sure secrets are ignored

Your project has a `.gitignore` file. It lists things git should **not** save,
like the `.venv` folder and build files. Open it and check it includes:

```
.venv
dist/
__pycache__/
```

> **Never** put passwords, API tokens, or secret keys in your project. If you
> have any, add their file names to `.gitignore`.

## 6.3 Save your work as a commit

Stage your files (get them ready) and commit (save the point):

```bash
git add .
git commit -m "First version of the load combination app"
```

The `-m` part is your message — a short note about what changed.

## 6.4 Create the repository on GitHub

You have two easy ways.

### Option A — the GitHub website

1. Go to [github.com](https://github.com) and sign in.
2. Click **New repository**.
3. Name it `strapp`.
4. Choose **Public** (so others can learn from it).
5. Do **not** add a README or license (we already have them).
6. Click **Create repository**.
7. GitHub shows you commands. Use the "push an existing repository" ones:

   ```bash
   git remote add origin https://github.com/YOUR-NAME/strapp.git
   git branch -M main
   git push -u origin main
   ```

### Option B — the GitHub CLI (`gh`)

If you have the [GitHub CLI](https://cli.github.com/) installed:

```bash
gh repo create strapp --public --source=. --push
```

This makes the repo and pushes your code in one step.

## 6.5 Check it worked

Open `https://github.com/YOUR-NAME/strapp` in your browser. You should see all
your files and your README shown nicely on the front page.

## 6.6 Saving changes later

Every time you change something and want to save it online:

```bash
git add .
git commit -m "Describe what you changed"
git push
```

## You are done with Step 6

Your code lives on GitHub. Now the exciting part — putting the app on the
internet: [Step 7 — Put the app online](07_deploy_streamlit_cloud.md).
