# Step 3 — Build the Streamlit app

Now we write the code. We keep two kinds of code apart:

- **Thinking code** — the math. It has no web parts. (`combinations.py`,
  `simulation.py`.) This makes it easy to test.
- **Drawing code** — the web page. (`app.py`.) It calls the thinking code.

Keeping them apart is a habit that will help you in every project you ever build.

## 3.1 The math: `combinations.py`

This file holds the recipes from Step 2. The key ideas:

- We use a small `Combination` class to hold one recipe: its name, its method
  (LRFD or ASD), and its factors (a map like `{"D": 1.2, "L": 1.6}`).
- `evaluate(...)` adds up the loads for one recipe.
- `governing_combination(...)` finds the recipe with the biggest total.

A tiny taste:

```python
@dataclass(frozen=True)
class Combination:
    name: str
    method: str
    factors: dict[str, float]

    def evaluate(self, load_values):
        # add factor * load for each load, treating missing ones as 0
        return sum(f * load_values.get(name, 0.0) for name, f in self.factors.items())
```

> **Why `@dataclass(frozen=True)`?** It builds a small, read-only object for us
> without lots of boilerplate. `frozen=True` means once made, it cannot be
> changed by accident — safer.

Open `src/strapp/combinations.py` and read it top to bottom. It is short and
fully commented.

## 3.2 The random study: `simulation.py`

This file makes the "what if" study for Tab 2:

1. For each load, you give a **low** and **high** value.
2. We use NumPy to pick random numbers in that range, many times.
3. For each random set, we find the controlling recipe.
4. We report the **worst** set of all.

The important NumPy part:

```python
rng = np.random.default_rng(seed)         # a random number maker
values = rng.uniform(low, high, size=n)   # n random numbers between low and high
```

> **What is a "seed"?** A seed is a starting number for the random maker. If you
> use the same seed, you get the same random numbers again. This makes your
> results repeatable, which is great for teaching and testing.

## 3.3 Nice math with handcalcs: `handcalc_view.py`

`handcalcs` shows a formula three ways at once:

```
symbols  =  numbers put in  =  the answer
```

That is exactly how an engineer writes it by hand. Because our recipes are built
while the app runs, we build a tiny function as text and let handcalcs read it.
You do not need to fully understand this file to use the app — just know it turns
one recipe into pretty math for the screen.

## 3.4 The web page: `app.py`

This is the Streamlit part. Streamlit is wonderful because you write normal
Python from top to bottom, and it becomes a web page. A few building blocks:

| Streamlit call | What it draws |
| -------------- | ------------- |
| `st.title("...")` | A big title. |
| `st.tabs([...])` | Tabs you can click between. |
| `st.radio(...)` | A set of round option buttons. |
| `st.data_editor(df)` | An editable table (you can add rows!). |
| `st.dataframe(df)` | A table to look at. |
| `st.markdown("$$...$$")` | Text, and pretty math when wrapped in `$$` fences. |
| `st.plotly_chart(fig)` | A Plotly chart. |
| `st.pyplot(fig)` | A matplotlib chart. |
| `st.download_button(...)` | A button to download a file. |

### The two tabs

```python
calculator, simulation, about = st.tabs(["Calculator", "Simulation", "About"])
with calculator:
    _calculator_tab()
with simulation:
    _simulation_tab()
```

### Tab 1 — Calculator (the flow)

1. Show a radio to pick the method (LRFD / ASD / both).
2. Show an editable table with example loads. The user can add or change rows.
3. Add up the loads by type (`aggregate_loads`).
4. Work out every recipe (`results_table`).
5. Find and show the controlling recipe (`governing_combination`).
6. Draw the controlling recipe with handcalcs (`st.markdown`).
7. Draw a Plotly bar chart, with the controlling bar in red.
8. Offer CSV and JSON download buttons.

> **Why `st.markdown` and not `st.latex` for the handcalcs math?** handcalcs
> hands back a string already wrapped in `$$ ... $$` math fences. `st.markdown`
> understands `$$` as "this is a math block" and renders it. `st.latex` is for a
> *bare* formula — it adds the math part for you — so giving it the `$$`-wrapped
> string double-wraps it and you just see the raw `\begin{aligned}...` text. Match
> the tool to the string you actually have.

### Tab 2 — Simulation (the flow)

1. Pick the method.
2. Show a table where the user sets a **low** and **high** for each load.
3. Pick how many samples and a random seed.
4. Press **Run simulation**.
5. The app draws a Plotly scatter chart: one dot per random sample. The
   **worst** dot is a red star with an **arrow and a label** pointing at it.
6. A small bar chart shows how often each recipe controlled.
7. A **matplotlib** histogram shows how the worst-case demand is spread out.
   (We use Plotly *and* matplotlib so you see two popular chart libraries.)
8. Download buttons for the full results.

The arrow is made like this:

```python
figure.add_annotation(
    x=worst_x, y=worst_y,
    text="Worst: ...",
    showarrow=True, arrowhead=2,
)
```

## 3.5 Two start files

- `src/strapp/_entry.py` — the file Streamlit actually runs. It uses the full
  name `from strapp.app import main` because Streamlit runs files as scripts.
- `streamlit_app.py` (at the top of the project) — the file you run on your own
  computer and the one Streamlit Community Cloud looks for. It adds the `src`
  folder to the path, then starts the app.

## 3.6 Run it!

```bash
uv run streamlit run streamlit_app.py
```

Your browser opens. Try both tabs. Add a row. Change a number. Press
**Run simulation**. Download a file. 🎉

## You are done with Step 3

The app works. Next we make sure it stays healthy with quality tools:
[Step 4 — Quality: ruff, ty, and tests](04_quality_ruff_ty_tests.md).
