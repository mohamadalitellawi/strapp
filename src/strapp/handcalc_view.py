"""Turn one load combination into nice math, using the handcalcs library.

handcalcs is a tool that shows a formula three ways at once:

    symbols  =  numbers put in  =  the answer

That is exactly how an engineer writes a calculation by hand, so it is great for
learning. The tricky part is that our combinations are built at run time, so we
build a tiny Python function in text, then let handcalcs read and render it.
"""

from __future__ import annotations

import linecache
from collections.abc import Mapping

from handcalcs.decorator import handcalc

from .combinations import Combination


def render_combination(combo: Combination, load_values: Mapping[str, float]) -> tuple[str, float]:
    """Render one combination as LaTeX with handcalcs.

    Args:
        combo: The combination to show.
        load_values: How big each load is, keyed by load letter.

    Returns:
        A ``(latex, total)`` pair. The LaTeX string is ready for
        ``st.latex(...)``. The total is the numeric answer.
    """
    factors = combo.factors
    arg_names = ", ".join(factors)
    expression = " + ".join(f"{factor:g}*{load}" for load, factor in factors.items())

    # Build a small function in text. handcalcs reads a function's source code,
    # so we register the text with linecache to make that source findable.
    source = f"def _combo({arg_names}):\n    U = {expression}\n    return U\n"
    filename = f"<combo:{combo.name}>"
    linecache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)

    namespace: dict[str, object] = {}
    exec(compile(source, filename, "exec"), namespace)  # noqa: S102 - safe: source is built from fixed numbers and load letters

    rendered = handcalc(jupyter_display=False, precision=2)(namespace["_combo"])
    latex, total = rendered(*(load_values.get(load, 0.0) for load in factors))
    return latex, float(total)
