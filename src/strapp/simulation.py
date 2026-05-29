"""Random "what if" simulation of load combinations.

Real design loads are never known exactly. This module helps you explore that.
It makes many random sets of load values (we call each one a "sample"), then for
every sample it finds the combination that controls the design.

The idea:

1. You give a low and high value for each load (a range).
2. We pick random numbers inside those ranges, many times.
3. For each random sample we find the biggest combination total.
4. We point out the worst sample of all - the extreme case.

This is a simple version of what engineers call a Monte Carlo study.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .combinations import governing_combination


@dataclass(frozen=True)
class SimulationResult:
    """Everything the simulation produced.

    Attributes:
        samples: One row per random sample. Has a column for each load, plus
            ``"Governing"`` (the controlling combination name) and ``"Demand"``
            (its total).
        extreme_index: The row number of the worst (largest demand) sample.
        extreme_demand: The largest demand found.
        extreme_combination: The combination name that controlled the worst sample.
    """

    samples: pd.DataFrame
    extreme_index: int
    extreme_demand: float
    extreme_combination: str


def simulate(
    load_ranges: dict[str, tuple[float, float]],
    n_samples: int = 100,
    method: str = "both",
    seed: int | None = None,
) -> SimulationResult:
    """Run the random simulation.

    Args:
        load_ranges: For each load letter, a ``(low, high)`` pair giving the
            smallest and largest value it might take.
        n_samples: How many random samples to make.
        method: Which design method to use (``"LRFD"``, ``"ASD"`` or ``"both"``).
        seed: A number that makes the random results repeatable. Use the same
            seed to get the same samples again. ``None`` means fully random.

    Returns:
        A :class:`SimulationResult`.

    Raises:
        ValueError: If there are no loads, ``n_samples`` is below 1, or any
            range has its low value above its high value.
    """
    if not load_ranges:
        raise ValueError("Give at least one load with a range.")
    if n_samples < 1:
        raise ValueError("n_samples must be 1 or more.")
    for letter, (low, high) in load_ranges.items():
        if low > high:
            raise ValueError(f"Load {letter}: low value {low} is bigger than high value {high}.")

    rng = np.random.default_rng(seed)
    letters = list(load_ranges)

    # Make the random load values: one column per load, one row per sample.
    columns = {
        letter: rng.uniform(low, high, size=n_samples)
        for letter, (low, high) in load_ranges.items()
    }
    samples = pd.DataFrame(columns)

    # For each sample, find the combination that controls the design.
    governing_names: list[str] = []
    demands: list[float] = []
    for _, row in samples.iterrows():
        load_values = {letter: float(row[letter]) for letter in letters}
        combo, total = governing_combination(load_values, method)
        governing_names.append(combo.name)
        demands.append(total)

    samples["Governing"] = governing_names
    samples["Demand"] = demands

    extreme_index = int(samples["Demand"].idxmax())
    return SimulationResult(
        samples=samples,
        extreme_index=extreme_index,
        extreme_demand=float(samples.loc[extreme_index, "Demand"]),
        extreme_combination=str(samples.loc[extreme_index, "Governing"]),
    )
