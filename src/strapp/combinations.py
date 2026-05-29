"""ASCE 7-22 structural load combinations.

This module is the "brain" of the app. It has no Streamlit code on purpose, so
you can read it, test it, and reuse it on its own.

A "load combination" is just a recipe. It tells you how much of each load to add
together. For example the recipe ``1.2D + 1.6L`` means:

    take 1.2 times the Dead load, add 1.6 times the Live load.

We support two design methods from the American code ASCE 7-22:

* **LRFD** (Load and Resistance Factor Design) - uses big factors like 1.2 and 1.6.
* **ASD** (Allowable Stress Design) - uses factors closer to 1.0.

NOTE FOR LEARNERS: this code is for teaching only. Do not use it for a real
building. Always check the real code book and a licensed engineer.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

# The short code letter for each load, and a friendly name to show in the app.
LOAD_TYPES: dict[str, str] = {
    "D": "Dead",
    "L": "Live",
    "Lr": "Roof Live",
    "S": "Snow",
    "R": "Rain",
    "W": "Wind",
    "E": "Seismic",
}

# The three "companion" roof loads. In the code they appear as "Lr or S or R",
# meaning you only use one of them at a time. We make a separate combination for
# each choice so a learner can see every case clearly.
_ROOF_LOADS: tuple[str, str, str] = ("Lr", "S", "R")


@dataclass(frozen=True)
class Combination:
    """One load combination recipe.

    Attributes:
        name: A label such as ``"LRFD 2 (Lr)"``.
        method: Either ``"LRFD"`` or ``"ASD"``.
        factors: A map from load letter to its factor, e.g. ``{"D": 1.2, "L": 1.6}``.
    """

    name: str
    method: str
    factors: dict[str, float]

    def equation(self) -> str:
        """Return the recipe as readable text, e.g. ``"1.2D + 1.6L + 0.5Lr"``."""
        return " + ".join(f"{factor:g}{load}" for load, factor in self.factors.items())

    def evaluate(self, load_values: Mapping[str, float]) -> float:
        """Add up the loads using this recipe.

        Args:
            load_values: How big each load is, e.g. ``{"D": 10, "L": 5}``.
                Any load you do not list counts as 0.

        Returns:
            The total demand for this combination.
        """
        return sum(factor * load_values.get(load, 0.0) for load, factor in self.factors.items())


def lrfd_combinations() -> list[Combination]:
    """Build the LRFD (strength design) combinations from ASCE 7-22 Section 2.3.1."""
    combos: list[Combination] = [Combination("LRFD 1", "LRFD", {"D": 1.4})]

    # Equation 2: 1.2D + 1.6L + 0.5(Lr or S or R)
    for roof in _ROOF_LOADS:
        combos.append(Combination(f"LRFD 2 ({roof})", "LRFD", {"D": 1.2, "L": 1.6, roof: 0.5}))

    # Equation 3: 1.2D + 1.6(Lr or S or R) + (1.0L or 0.5W)
    for roof in _ROOF_LOADS:
        combos.append(Combination(f"LRFD 3 ({roof}, L)", "LRFD", {"D": 1.2, roof: 1.6, "L": 1.0}))
        combos.append(Combination(f"LRFD 3 ({roof}, W)", "LRFD", {"D": 1.2, roof: 1.6, "W": 0.5}))

    # Equation 4: 1.2D + 1.0W + 1.0L + 0.5(Lr or S or R)
    for roof in _ROOF_LOADS:
        combos.append(
            Combination(f"LRFD 4 ({roof})", "LRFD", {"D": 1.2, "W": 1.0, "L": 1.0, roof: 0.5})
        )

    # Equation 5: 1.2D + 1.0E + 1.0L + 0.2S
    combos.append(Combination("LRFD 5", "LRFD", {"D": 1.2, "E": 1.0, "L": 1.0, "S": 0.2}))
    # Equation 6: 0.9D + 1.0W
    combos.append(Combination("LRFD 6", "LRFD", {"D": 0.9, "W": 1.0}))
    # Equation 7: 0.9D + 1.0E
    combos.append(Combination("LRFD 7", "LRFD", {"D": 0.9, "E": 1.0}))
    return combos


def asd_combinations() -> list[Combination]:
    """Build the ASD (allowable stress) combinations from ASCE 7-22 Sections 2.4.1 and 2.4.5."""
    combos: list[Combination] = [
        Combination("ASD 1", "ASD", {"D": 1.0}),
        Combination("ASD 2", "ASD", {"D": 1.0, "L": 1.0}),
    ]

    # Equation 3: D + (Lr or S or R)
    for roof in _ROOF_LOADS:
        combos.append(Combination(f"ASD 3 ({roof})", "ASD", {"D": 1.0, roof: 1.0}))

    # Equation 4: D + 0.75L + 0.75(Lr or S or R)
    for roof in _ROOF_LOADS:
        combos.append(Combination(f"ASD 4 ({roof})", "ASD", {"D": 1.0, "L": 0.75, roof: 0.75}))

    # Equation 5: D + 0.6W
    combos.append(Combination("ASD 5", "ASD", {"D": 1.0, "W": 0.6}))

    # Equation 6: D + 0.75L + 0.75(0.6W) + 0.75(Lr or S or R)  ->  0.75 * 0.6 = 0.45 on W
    for roof in _ROOF_LOADS:
        combos.append(
            Combination(f"ASD 6 ({roof})", "ASD", {"D": 1.0, "L": 0.75, "W": 0.45, roof: 0.75})
        )

    # Equation 7: 0.6D + 0.6W
    combos.append(Combination("ASD 7", "ASD", {"D": 0.6, "W": 0.6}))

    # Seismic combinations (Section 2.4.5)
    combos.append(Combination("ASD 8", "ASD", {"D": 1.0, "E": 0.7}))
    combos.append(Combination("ASD 9", "ASD", {"D": 1.0, "E": 0.525, "L": 0.75, "S": 0.75}))
    combos.append(Combination("ASD 10", "ASD", {"D": 0.6, "E": 0.7}))
    return combos


def get_combinations(method: str = "both") -> list[Combination]:
    """Return the combinations for the chosen design method.

    Args:
        method: ``"LRFD"``, ``"ASD"`` or ``"both"`` (case does not matter).

    Returns:
        The matching list of combinations.

    Raises:
        ValueError: If the method name is not one we know.
    """
    choice = method.strip().lower()
    if choice == "lrfd":
        return lrfd_combinations()
    if choice == "asd":
        return asd_combinations()
    if choice == "both":
        return lrfd_combinations() + asd_combinations()
    raise ValueError(f"Unknown method {method!r}. Use 'LRFD', 'ASD' or 'both'.")


def evaluate_all(
    load_values: Mapping[str, float], method: str = "both"
) -> list[tuple[Combination, float]]:
    """Work out the total for every combination.

    Args:
        load_values: How big each load is, keyed by load letter.
        method: Which design method to use (see :func:`get_combinations`).

    Returns:
        A list of ``(combination, total)`` pairs in code order.
    """
    return [(combo, combo.evaluate(load_values)) for combo in get_combinations(method)]


def governing_combination(
    load_values: Mapping[str, float], method: str = "both"
) -> tuple[Combination, float]:
    """Find the combination that controls the design (the largest total).

    Args:
        load_values: How big each load is, keyed by load letter.
        method: Which design method to use (see :func:`get_combinations`).

    Returns:
        The ``(combination, total)`` pair with the biggest total.
    """
    results = evaluate_all(load_values, method)
    return max(results, key=lambda pair: pair[1])
