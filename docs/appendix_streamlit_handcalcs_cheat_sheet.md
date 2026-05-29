# Appendix — Streamlit & handcalcs cheat sheet

A quick reference for building a **Streamlit** page and for rendering
**handcalcs** math inside it. Like the command cheat sheet, this is written
**generically** — swap the `<angle bracket>` parts for your own names.

## How to read this sheet

- Everything here is **plain Python**, so it works the **same on macOS and
  Windows 11**. There are no per-platform variations.
- `st` is the usual nickname: `import streamlit as st`.
- Snippets assume you have a DataFrame called `df`, a Plotly figure `fig`, and a
  matplotlib figure `mpl_fig` where relevant.

> **Run any Streamlit app the same way on both systems:**
> `uv run streamlit run <app>.py`

---

# Part 1 — Streamlit

## 1. Running and page setup

| Goal | Code |
| ---- | ---- |
| Run the app | `uv run streamlit run <app>.py` |
| Set tab title, icon, layout (**call first, once**) | `st.set_page_config(page_title="<title>", page_icon="🏗️", layout="wide")` |
| Big page title | `st.title("<title>")` |
| Section heading | `st.subheader("<heading>")` |
| Small grey caption | `st.caption("<note>")` |

> `st.set_page_config(...)` must be the **first** Streamlit call in the script,
> or Streamlit raises an error.

## 2. Text and status messages

| Goal | Code |
| ---- | ---- |
| Write almost anything (text, df, number) | `st.write(<value>)` |
| Markdown (supports `**bold**`, lists, `$$math$$`) | `st.markdown("<markdown>")` |
| Blue info box | `st.info("<message>")` |
| Green success box | `st.success("<message>")` |
| Yellow warning box | `st.warning("<message>")` |
| Red error box | `st.error("<message>")` |

## 3. Layout containers

| Goal | Code |
| ---- | ---- |
| Tabs | `tab_a, tab_b = st.tabs(["A", "B"])` then `with tab_a: ...` |
| Side-by-side columns | `left, right = st.columns(2)` then `with left: ...` |
| Collapsible section | `with st.expander("<label>"): ...` |
| A grouping container | `with st.container(): ...` |
| Put a widget in the sidebar | `st.sidebar.<widget>(...)` or `with st.sidebar: ...` |

## 4. Input widgets

| Goal | Code |
| ---- | ---- |
| Round option buttons | `choice = st.radio("<label>", ["X", "Y", "Z"])` |
| Dropdown | `choice = st.selectbox("<label>", options)` |
| A clickable button | `if st.button("<label>"): ...` |
| Checkbox | `on = st.checkbox("<label>")` |
| Number input | `n = st.number_input("<label>", min_value=0, value=10)` |
| Text input | `text = st.text_input("<label>")` |
| Slider | `x = st.slider("<label>", 0, 100, 50)` |
| **Editable table** (user can add/edit rows) | `edited = st.data_editor(df, num_rows="dynamic")` |

> **Editable table column rules:** shape columns with `st.column_config`, e.g.
> `st.data_editor(df, column_config={"qty": st.column_config.NumberColumn(min_value=0)})`.

## 5. Showing data

| Goal | Code |
| ---- | ---- |
| Read-only table (interactive) | `st.dataframe(df, width="stretch")` |
| Static table | `st.table(df)` |
| A single big number with delta | `st.metric("<label>", value, delta)` |

## 6. Charts

| Goal | Code |
| ---- | ---- |
| Quick built-in bar chart | `st.bar_chart(df)` |
| Quick built-in line chart | `st.line_chart(df)` |
| A Plotly figure | `st.plotly_chart(fig, width="stretch")` |
| A matplotlib figure | `st.pyplot(mpl_fig)` |
| An Altair chart | `st.altair_chart(chart, width="stretch")` |

## 7. Math (LaTeX)

| Goal | Code |
| ---- | ---- |
| Render a **bare** LaTeX expression | `st.latex(r"a^2 + b^2 = c^2")` |
| Render LaTeX already wrapped in `$$...$$` | `st.markdown(r"$$a^2 + b^2 = c^2$$")` |

> **The key difference** (it trips everyone up — see Part 2): `st.latex` wants a
> **bare** expression and adds the math mode itself. `st.markdown` expects you to
> include the `$$ ... $$` fences. Match the call to the string you actually have.

## 8. Files in and out

| Goal | Code |
| ---- | ---- |
| Download a string/bytes as a file | `st.download_button("Download", data=<str/bytes>, file_name="<name>.csv", mime="text/csv")` |
| Upload a file | `uploaded = st.file_uploader("<label>")` |

> `download_button` needs **non-`None`** data. If your serializer can return
> `None` (e.g. `df.to_json()`), guard it: `data = df.to_json() or "[]"`.

## 9. State and reruns

The whole script reruns top-to-bottom on every interaction. To remember things
between reruns, use **session state**:

| Goal | Code |
| ---- | ---- |
| Initialise a stored value once | `if "k" not in st.session_state: st.session_state.k = 0` |
| Read / write a stored value | `st.session_state.k += 1` |
| Force an immediate rerun | `st.rerun()` |

## 10. Caching (skip slow repeat work)

| Goal | Code |
| ---- | ---- |
| Cache a function that returns **data** | `@st.cache_data` above the function |
| Cache a function that returns a **resource** (model, db connection) | `@st.cache_resource` above the function |

## 11. Common gotchas

- **Full width:** modern Streamlit uses `width="stretch"`. The old
  `use_container_width=True` is **deprecated** — replace it with `width="stretch"`.
- **`set_page_config` first:** any other `st.*` call before it errors out.
- **Reruns reset variables:** a plain Python variable does **not** survive the
  next interaction — use `st.session_state` for anything that must persist.
- **Widget keys:** if you create similar widgets in a loop, give each a unique
  `key="<unique>"` so Streamlit can tell them apart.

---

# Part 2 — handcalcs inside Streamlit

**handcalcs** renders a calculation three ways at once — the way an engineer
writes it by hand:

```
symbols  =  numbers substituted in  =  the answer
```

## 12. The decorator basics

```python
from handcalcs.decorator import handcalc

@handcalc(jupyter_display=False, precision=2)
def calc(a, b):
    c = a + b
    return c

latex, result = calc(3, 4)   # latex is a string, result == 7
```

| Argument | What it does |
| -------- | ------------ |
| `jupyter_display=False` | **Return** the LaTeX as a string instead of drawing it in a notebook. Use this in Streamlit. |
| `precision=2` | Round numbers in the output to 2 decimals. |

> With `jupyter_display=False`, the decorated function returns a **`(latex,
> value)` tuple** — the LaTeX string first, then the normal return value.

## 13. The one rule for rendering it in Streamlit

handcalcs wraps its output in `$$ ... $$` math fences already. So:

```python
latex, value = calc(3, 4)

st.markdown(latex)   # ✅ CORRECT — markdown treats $$...$$ as a math block
st.latex(latex)      # ❌ WRONG — double-wraps; shows raw \begin{aligned}... text
```

★ Why: `st.latex` adds its **own** math mode, so handing it a string that
already has `$$` breaks the renderer and it falls back to showing the raw
LaTeX source. `st.markdown` renders `$$...$$` as math, which is exactly the
format handcalcs produces.

| You have... | Use | Result |
| ----------- | --- | ------ |
| handcalcs output (`$$`-wrapped) | `st.markdown(latex)` | ✅ rendered math |
| handcalcs output (`$$`-wrapped) | `st.latex(latex)` | ❌ raw `$$\begin{aligned}...` text |
| a bare expression you wrote yourself | `st.latex(r"x^2")` | ✅ rendered math |

## 14. Putting it together (a complete pattern)

```python
import streamlit as st
from handcalcs.decorator import handcalc

@handcalc(jupyter_display=False, precision=2)
def beam_demand(w, L):
    M = w * L**2 / 8
    return M

st.subheader("Step-by-step calculation")
latex, moment = beam_demand(5.0, 6.0)
st.markdown(latex)                       # the math, rendered
st.success(f"Result: {moment:.2f}")      # the number, highlighted
```

## 15. Advanced — rendering a formula built at run time

handcalcs reads a function's **source code**, so a function you build as text at
run time has no source for it to find. The fix is to register the text with
Python's `linecache` before decorating:

```python
import linecache
from handcalcs.decorator import handcalc

source = "def _f(a, b):\n    U = 1.2*a + 1.6*b\n    return U\n"
filename = "<dynamic-calc>"
linecache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)

namespace = {}
exec(compile(source, filename, "exec"), namespace)   # builds _f
latex, value = handcalc(jupyter_display=False, precision=2)(namespace["_f"])(10, 20)
st.markdown(latex)
```

> Only reach for this when the formula itself is decided while the app runs. For
> fixed formulas, the plain decorator in Section 12 is simpler and clearer.

---

## 16. The smallest set to memorise

```python
st.title("...")                       # heading
a, b = st.tabs(["A", "B"])            # tabs
choice = st.radio("...", [...])       # pick one
df2 = st.data_editor(df,              # editable table
                     num_rows="dynamic")
st.dataframe(df2, width="stretch")    # show a table
st.plotly_chart(fig, width="stretch") # show a chart

latex, value = calc(...)              # handcalcs (jupyter_display=False)
st.markdown(latex)                    # render its $$-wrapped math
```
