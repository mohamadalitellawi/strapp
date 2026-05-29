# Step 4 — Quality: ruff, ty, and tests

Working code is good. Code that **stays** working, that others can read, and
that you can change without fear — that is great. Three tools help us get there.

## 4.1 ruff — style and small bugs

**ruff** reads your code and points out style problems and some common mistakes
(like an import you never use). It is very fast.

Find problems:

```bash
uv run ruff check
```

If it finds things, many can be fixed for you:

```bash
uv run ruff check --fix
```

ruff can also **format** your code so it all looks the same — spacing, line
breaks, quotes:

```bash
uv run ruff format
```

> **Tip:** Run `ruff format` often. You stop thinking about spaces and commas and
> just write code; the tool tidies it.

### Where are the settings?

In `pyproject.toml`:

```toml
[tool.ruff]
line-length = 100        # how long a line may be

[tool.ruff.lint]
select = ["E", "W", "F", "I", "UP", "B", "SIM"]
```

Those letters are rule groups. For example `F` finds real bugs, `I` sorts your
imports, and `UP` suggests newer, cleaner Python.

## 4.2 ty — checking types

A **type** is the kind of a value: a number, a piece of text, a list. Python
lets us write **type hints** to say what we expect:

```python
def evaluate(self, load_values: dict[str, float]) -> float:
    ...
```

This says: `load_values` is a dictionary from text to numbers, and the function
gives back a number. **ty** (another Astral tool) reads these hints and warns you
if something does not match — for example, if you pass text where a number is
expected.

```bash
uv run ty check
```

> ⚠️ **ty is new and in early preview.** It is great for learning and catches
> real mistakes, but it may change or have rough edges. That is fine for a
> teaching project.

### A real example from this project

ty taught us something useful. Our function asked for `dict[str, float]`, but a
test passed `dict[str, int]` (whole numbers). ty complained. The clean fix was to
accept a more general type, `Mapping[str, float]`, which welcomes both. Small
lesson, real improvement.

## 4.3 pytest — automatic tests

A **test** is a small piece of code that checks our real code gives the right
answer. Tests live in the `tests/` folder. Run them all:

```bash
uv run pytest
```

You should see something like `22 passed`.

### What a test looks like

```python
def test_first_lrfd_combination_is_1_4_dead():
    first = lrfd_combinations()[0]
    assert first.factors == {"D": 1.4}          # the recipe is 1.4D
    assert first.evaluate({"D": 10}) == 14.0    # 1.4 * 10 = 14
```

`assert` means "this must be true." If it is not, the test fails and tells you.

### Why test the math and not the web page?

This is why we kept the math separate (Step 3). The math functions are easy to
test: give numbers, check the answer. We also do a light check of the web page
using Streamlit's built-in `AppTest`, which runs the app and makes sure it does
not crash.

## 4.4 Do all checks at once

Before you share your code, run all three:

```bash
uv run ruff format
uv run ruff check
uv run ty check
uv run pytest
```

If all are happy, your code is in good shape.

## You are done with Step 4

Your code is clean, typed, and tested. Next we package it up:
[Step 5 — Build and publish the package](05_build_and_publish_pypi.md).
