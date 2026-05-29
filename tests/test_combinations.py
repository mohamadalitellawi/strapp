"""Tests for the load combination math.

These tests check known numbers from ASCE 7-22 so we can trust the app.
Run them with::

    uv run pytest
"""

from __future__ import annotations

import pytest

from strapp.combinations import (
    Combination,
    asd_combinations,
    evaluate_all,
    get_combinations,
    governing_combination,
    lrfd_combinations,
)


def test_combination_equation_text() -> None:
    combo = Combination("test", "LRFD", {"D": 1.2, "L": 1.6})
    assert combo.equation() == "1.2D + 1.6L"


def test_combination_evaluate_basic() -> None:
    combo = Combination("test", "LRFD", {"D": 1.2, "L": 1.6})
    # 1.2 * 10 + 1.6 * 5 = 12 + 8 = 20
    assert combo.evaluate({"D": 10, "L": 5}) == pytest.approx(20.0)


def test_evaluate_treats_missing_loads_as_zero() -> None:
    combo = Combination("test", "LRFD", {"D": 1.2, "W": 1.0})
    # Wind is not given, so it counts as 0: 1.2 * 10 = 12
    assert combo.evaluate({"D": 10}) == pytest.approx(12.0)


def test_first_lrfd_combination_is_1_4_dead() -> None:
    first = lrfd_combinations()[0]
    assert first.factors == {"D": 1.4}
    assert first.evaluate({"D": 10}) == pytest.approx(14.0)


def test_asd_has_a_plain_dead_only_case() -> None:
    names = {combo.name: combo for combo in asd_combinations()}
    assert names["ASD 1"].factors == {"D": 1.0}


def test_asd_wind_uplift_reduces_dead_load() -> None:
    # ASD 7 is 0.6D + 0.6W, used to check a light structure lifting in wind.
    asd_7 = next(combo for combo in asd_combinations() if combo.name == "ASD 7")
    assert asd_7.factors == {"D": 0.6, "W": 0.6}


def test_get_combinations_both_is_lrfd_plus_asd() -> None:
    total = len(lrfd_combinations()) + len(asd_combinations())
    assert len(get_combinations("both")) == total


def test_get_combinations_is_case_insensitive() -> None:
    assert get_combinations("lrfd") == get_combinations("LRFD")


def test_get_combinations_rejects_unknown_method() -> None:
    with pytest.raises(ValueError, match="Unknown method"):
        get_combinations("nonsense")


def test_evaluate_all_returns_one_pair_per_combination() -> None:
    loads = {"D": 10, "L": 5}
    results = evaluate_all(loads, "LRFD")
    assert len(results) == len(lrfd_combinations())
    assert all(isinstance(total, float) for _, total in results)


def test_governing_is_the_largest_total() -> None:
    loads = {"D": 10, "L": 5, "Lr": 3}
    combo, total = governing_combination(loads, "LRFD")
    every_total = [value for _, value in evaluate_all(loads, "LRFD")]
    assert total == pytest.approx(max(every_total))
    assert combo.evaluate(loads) == pytest.approx(total)


def test_governing_with_only_dead_load_picks_1_4_dead() -> None:
    # With only dead load, 1.4D must be the biggest in LRFD.
    combo, total = governing_combination({"D": 10}, "LRFD")
    assert combo.factors == {"D": 1.4}
    assert total == pytest.approx(14.0)
