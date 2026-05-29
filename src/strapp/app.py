"""The Streamlit web app.

This file draws the web page. It keeps the "drawing" code here and calls the
plain Python "thinking" code in :mod:`strapp.combinations` and
:mod:`strapp.simulation`. Keeping those apart makes each part easy to read.

Run it locally with::

    uv run streamlit run streamlit_app.py
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from matplotlib.figure import Figure

from .combinations import LOAD_TYPES, evaluate_all, governing_combination
from .handcalc_view import render_combination
from .simulation import simulate

# Friendly name -> short code letter, e.g. "Dead" -> "D".
NAME_TO_LETTER: dict[str, str] = {name: letter for letter, name in LOAD_TYPES.items()}
FRIENDLY_NAMES: list[str] = list(LOAD_TYPES.values())

DISCLAIMER = (
    "Teaching tool only. The numbers are simplified and may be incomplete. "
    "Never use this for a real building. Always check ASCE 7 and a licensed engineer."
)


def aggregate_loads(rows: pd.DataFrame) -> dict[str, float]:
    """Add up the magnitudes for each load type.

    Many rows can share a type (for example two dead loads). We sum them so each
    load letter has one total value.

    Args:
        rows: The table from the app, with columns ``"Load Type"`` and ``"Magnitude"``.

    Returns:
        A map from load letter to its total magnitude.
    """
    totals: dict[str, float] = {}
    for _, row in rows.iterrows():
        name = row.get("Load Type")
        magnitude = row.get("Magnitude")
        if name not in NAME_TO_LETTER or pd.isna(magnitude):
            continue
        letter = NAME_TO_LETTER[name]
        totals[letter] = totals.get(letter, 0.0) + float(magnitude)
    return totals


def results_table(load_values: dict[str, float], method: str) -> pd.DataFrame:
    """Build a tidy table of every combination and its total."""
    return pd.DataFrame(
        {
            "Combination": combo.name,
            "Method": combo.method,
            "Equation": combo.equation(),
            "Total": round(total, 2),
        }
        for combo, total in evaluate_all(load_values, method)
    )


def combination_bar_chart(table: pd.DataFrame) -> go.Figure:
    """Draw a bar for each combination total, with the controlling one in red."""
    top = table["Total"].max()
    colors = ["#d62728" if value == top else "#1f77b4" for value in table["Total"]]
    figure = go.Figure(go.Bar(x=table["Combination"], y=table["Total"], marker_color=colors))
    figure.update_layout(
        title="Combination totals (red = controls the design)",
        xaxis_title="Combination",
        yaxis_title="Total demand",
        xaxis_tickangle=-45,
    )
    return figure


def _calculator_tab() -> None:
    st.subheader("Load combination calculator")
    st.write(
        "Type your loads in the table. Give each one a name, choose its type, "
        "and enter how big it is. Use any unit you like, but keep it the same "
        "for every load."
    )

    method = st.radio(
        "Design method",
        options=["both", "LRFD", "ASD"],
        horizontal=True,
        help="LRFD uses big factors. ASD uses factors near 1.0. 'both' shows them together.",
        key="calc_method",
    )

    default_loads = pd.DataFrame(
        [
            {"Load Name": "Floor dead load", "Load Type": "Dead", "Magnitude": 20.0},
            {"Load Name": "Office live load", "Load Type": "Live", "Magnitude": 12.0},
            {"Load Name": "Roof snow", "Load Type": "Snow", "Magnitude": 8.0},
            {"Load Name": "Wind pressure", "Load Type": "Wind", "Magnitude": 6.0},
        ]
    )
    edited = st.data_editor(
        default_loads,
        num_rows="dynamic",
        width="stretch",
        column_config={
            "Load Name": st.column_config.TextColumn("Load Name", required=False),
            "Load Type": st.column_config.SelectboxColumn("Load Type", options=FRIENDLY_NAMES),
            "Magnitude": st.column_config.NumberColumn("Magnitude", min_value=0.0, step=1.0),
        },
        key="calc_editor",
    )

    load_values = aggregate_loads(edited)
    if not load_values:
        st.info("Add at least one load with a type and a magnitude to see results.")
        return

    st.write("**Totals by load type**")
    st.write({f"{letter} ({LOAD_TYPES[letter]})": value for letter, value in load_values.items()})

    table = results_table(load_values, method)
    governing_combo, governing_total = governing_combination(load_values, method)

    st.write("**All combinations**")
    st.dataframe(
        table.style.highlight_max(subset=["Total"], color="#ffd6d6"),
        width="stretch",
        hide_index=True,
    )

    st.success(
        f"Controlling combination: **{governing_combo.name}** "
        f"({governing_combo.equation()}) = **{round(governing_total, 2)}**"
    )

    st.write("**The controlling combination, step by step (handcalcs)**")
    latex, _ = render_combination(governing_combo, load_values)
    st.latex(latex)

    st.plotly_chart(combination_bar_chart(table), width="stretch")

    st.write("**Download your results**")
    left, right = st.columns(2)
    left.download_button(
        "Download CSV",
        data=table.to_csv(index=False).encode("utf-8"),
        file_name="load_combinations.csv",
        mime="text/csv",
    )
    right.download_button(
        "Download JSON",
        data=table.to_json(orient="records", indent=2) or "[]",
        file_name="load_combinations.json",
        mime="application/json",
    )


def simulation_chart(samples: pd.DataFrame, extreme_index: int) -> go.Figure:
    """Plot the demand of every sample and point an arrow at the worst one."""
    figure = go.Figure(
        go.Scatter(
            x=samples.index,
            y=samples["Demand"],
            mode="markers",
            marker={"color": "#1f77b4", "size": 7},
            name="Samples",
        )
    )
    worst = samples.loc[extreme_index]
    figure.add_trace(
        go.Scatter(
            x=[extreme_index],
            y=[worst["Demand"]],
            mode="markers",
            marker={"color": "#d62728", "size": 14, "symbol": "star"},
            name="Worst case",
        )
    )
    figure.add_annotation(
        x=extreme_index,
        y=worst["Demand"],
        text=f"Worst: {worst['Governing']} = {worst['Demand']:.1f}",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40,
        bgcolor="#ffe0e0",
    )
    figure.update_layout(
        title="Governing demand for each random sample",
        xaxis_title="Sample number",
        yaxis_title="Controlling demand",
    )
    return figure


def demand_histogram(samples: pd.DataFrame) -> Figure:
    """Draw a matplotlib histogram showing how the worst-case demand is spread.

    A histogram puts the results into buckets and shows how many fall in each
    bucket. It is a quick way to see the typical demand and how far it can swing.
    """
    figure, axes = plt.subplots()
    axes.hist(samples["Demand"], bins=20, color="#1f77b4", edgecolor="white")
    axes.set_title("How the controlling demand is spread out")
    axes.set_xlabel("Controlling demand")
    axes.set_ylabel("Number of samples")
    return figure


def _simulation_tab() -> None:
    st.subheader("Design simulation (random what-if)")
    st.write(
        "Real loads are never known exactly. Here we try many random sets of "
        "values. For each one we find the combination that controls the design, "
        "then we point out the worst case of all."
    )

    method = st.radio(
        "Design method",
        options=["both", "LRFD", "ASD"],
        horizontal=True,
        key="sim_method",
    )

    st.write("Set a low and high value for each load you want to include.")
    default_ranges = pd.DataFrame(
        [
            {"Load Type": "Dead", "Low": 18.0, "High": 22.0},
            {"Load Type": "Live", "Low": 8.0, "High": 16.0},
            {"Load Type": "Snow", "Low": 4.0, "High": 12.0},
            {"Load Type": "Wind", "Low": 2.0, "High": 10.0},
        ]
    )
    ranges_table = st.data_editor(
        default_ranges,
        num_rows="dynamic",
        width="stretch",
        column_config={
            "Load Type": st.column_config.SelectboxColumn("Load Type", options=FRIENDLY_NAMES),
            "Low": st.column_config.NumberColumn("Low", min_value=0.0, step=1.0),
            "High": st.column_config.NumberColumn("High", min_value=0.0, step=1.0),
        },
        key="sim_editor",
    )

    left, right = st.columns(2)
    n_samples = left.slider("Number of samples", min_value=10, max_value=1000, value=200, step=10)
    seed = right.number_input(
        "Random seed (same number = same result)", min_value=0, max_value=10_000, value=42
    )

    if not st.button("Run simulation", type="primary"):
        st.info("Set your ranges, then press 'Run simulation'.")
        return

    load_ranges: dict[str, tuple[float, float]] = {}
    for _, row in ranges_table.iterrows():
        name = row.get("Load Type")
        low, high = row.get("Low"), row.get("High")
        if name not in NAME_TO_LETTER or pd.isna(low) or pd.isna(high):
            continue
        load_ranges[NAME_TO_LETTER[name]] = (float(low), float(high))

    if not load_ranges:
        st.warning("Add at least one load with a low and high value.")
        return

    try:
        result = simulate(load_ranges, n_samples=int(n_samples), method=method, seed=int(seed))
    except ValueError as error:
        st.error(str(error))
        return

    st.success(
        f"Worst case is sample #{result.extreme_index}: "
        f"**{result.extreme_combination}** = **{result.extreme_demand:.2f}**"
    )
    st.plotly_chart(simulation_chart(result.samples, result.extreme_index), width="stretch")

    st.write("**How often each combination controlled the design**")
    counts = result.samples["Governing"].value_counts().rename_axis("Combination")
    st.bar_chart(counts)

    st.write("**The spread of worst-case demand (matplotlib)**")
    st.pyplot(demand_histogram(result.samples))

    st.write("**All samples**")
    st.dataframe(result.samples.round(2), width="stretch")

    st.write("**Download the simulation**")
    csv_col, json_col = st.columns(2)
    csv_col.download_button(
        "Download CSV",
        data=result.samples.to_csv(index_label="Sample").encode("utf-8"),
        file_name="simulation.csv",
        mime="text/csv",
    )
    json_col.download_button(
        "Download JSON",
        data=result.samples.to_json(orient="records", indent=2) or "[]",
        file_name="simulation.json",
        mime="application/json",
    )


def main() -> None:
    """Draw the whole web page. This is what Streamlit runs."""
    st.set_page_config(page_title="Structural Load Combinations", page_icon="🏗️", layout="wide")
    st.title("🏗️ Structural Load Combinations")
    st.caption(DISCLAIMER)

    calculator, simulation, about = st.tabs(["Calculator", "Simulation", "About"])
    with calculator:
        _calculator_tab()
    with simulation:
        _simulation_tab()
    with about:
        st.write(
            "This small app teaches two things at once: how to build a Streamlit "
            "web app, and how American (ASCE 7-22) load combinations work. "
            "The full step-by-step guide lives in the `docs/` folder of the project."
        )
        st.write(f"NumPy {np.__version__} · pandas {pd.__version__}")


if __name__ == "__main__":
    main()
