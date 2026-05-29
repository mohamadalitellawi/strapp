# Step 5 — Build and publish the package

A **package** is your code wrapped up so other people can install it with one
command. In this step we **build** the package and learn how to **publish** it to
PyPI (the place Python packages live). We will not actually publish in this
guide, but you will know exactly how.

> You do **not** need to publish to PyPI to put the app online (that is Step 7).
> This step is here so you learn the full, professional workflow.

## 5.1 What does "build" mean?

Building turns your source code into two standard files:

- a **wheel** (`.whl`) — the ready-to-install version.
- a **source distribution** (`.tar.gz`) — the source code in a standard box.

Build them with uv:

```bash
uv build
```

You will see a new `dist/` folder:

```
dist/
├── strapp-0.1.0-py3-none-any.whl
└── strapp-0.1.0.tar.gz
```

## 5.2 The `strapp` command

In `pyproject.toml` we added this:

```toml
[project.scripts]
strapp = "strapp.cli:main"
```

This means: when someone installs the package, they get a new terminal command
called `strapp` that starts the app. Try it after building, in a fresh place:

```bash
uvx --from dist/strapp-0.1.0-py3-none-any.whl strapp
```

(`uvx` runs a command from a package without installing it permanently.)

## 5.3 Version numbers

Your package has a version in `pyproject.toml`: `version = "0.1.0"`. When you
change your code and want to share a new version, raise this number. A common
rule (called *semantic versioning*):

- `0.1.0 -> 0.1.1`: tiny fix.
- `0.1.0 -> 0.2.0`: new feature, nothing broken.
- `0.1.0 -> 1.0.0`: a big or breaking change.

## 5.4 How to publish to PyPI (the steps)

> We are **not** going to run this for real here. But here is exactly how.

1. **Make an account** at [pypi.org](https://pypi.org).

2. **Create an API token** in your PyPI account settings. It looks like
   `pypi-AgEI...`. Keep it secret, like a password.

3. **Test first on TestPyPI** (a practice copy of PyPI) at
   [test.pypi.org](https://test.pypi.org). This is the safe way to learn:

   ```bash
   uv publish --publish-url https://test.pypi.org/legacy/ --token pypi-YOUR-TEST-TOKEN
   ```

4. **Publish for real** to PyPI:

   ```bash
   uv publish --token pypi-YOUR-REAL-TOKEN
   ```

5. After a minute, anyone in the world can install your app:

   ```bash
   uv tool install strapp
   strapp
   ```

### Important notes

- The name `strapp` must be **free** on PyPI. If it is taken, pick another name
  in `pyproject.toml` (for example `strapp-yourname`).
- Once you publish a version number, you **cannot** re-use it. To fix a mistake,
  raise the version and publish again.
- **Never** put your token in your code or on GitHub. Paste it only in the
  command, or store it as an environment variable.

## You are done with Step 5

You can build your package and you know how to publish it. Next we put the code
on GitHub: [Step 6 — Push to GitHub](06_push_to_github.md).
