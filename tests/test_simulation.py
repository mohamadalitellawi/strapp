"""Tests for the random simulation.

Run them with::

    uv run pytest
"""

from __future__ import annotations

import pytest

from strapp.simulation import simulate


def test_simulate_makes_the_right_number_of_samples() -> None:
    result = simulate({"D": (10, 20), "L": (5, 10)}, n_samples=50, seed=1)
    assert len(result.samples) == 50


def test_samples_stay_inside_their_ranges() -> None:
    result = simulate({"D": (10, 20), "L": (5, 10)}, n_samples=100, seed=1)
    assert result.samples["D"].min() >= 10
    assert result.samples["D"].max() <= 20
    assert result.samples["L"].min() >= 5
    assert result.samples["L"].max() <= 10


def test_same_seed_gives_the_same_result() -> None:
    first = simulate({"D": (10, 20)}, n_samples=30, seed=7)
    second = simulate({"D": (10, 20)}, n_samples=30, seed=7)
    assert first.extreme_demand == pytest.approx(second.extreme_demand)
    assert first.samples["Demand"].tolist() == second.samples["Demand"].tolist()


def test_extreme_demand_is_the_biggest_demand() -> None:
    result = simulate({"D": (10, 20), "L": (5, 10)}, n_samples=80, seed=3)
    assert result.extreme_demand == pytest.approx(result.samples["Demand"].max())


def test_extreme_index_points_at_the_worst_row() -> None:
    result = simulate({"D": (10, 20)}, n_samples=40, seed=5)
    worst_row = result.samples.loc[result.extreme_index]
    assert worst_row["Demand"] == pytest.approx(result.extreme_demand)
    assert worst_row["Governing"] == result.extreme_combination


def test_no_loads_is_rejected() -> None:
    with pytest.raises(ValueError, match="at least one load"):
        simulate({}, n_samples=10)


def test_zero_samples_is_rejected() -> None:
    with pytest.raises(ValueError, match="1 or more"):
        simulate({"D": (10, 20)}, n_samples=0)


def test_backwards_range_is_rejected() -> None:
    with pytest.raises(ValueError, match="bigger than"):
        simulate({"D": (20, 10)}, n_samples=10)
