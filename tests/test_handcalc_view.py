"""Tests for the handcalcs rendering helper."""

from __future__ import annotations

import pytest

from strapp.combinations import Combination
from strapp.handcalc_view import render_combination


def test_render_returns_latex_and_total() -> None:
    combo = Combination("LRFD 1", "LRFD", {"D": 1.4})
    latex, total = render_combination(combo, {"D": 10})
    assert total == pytest.approx(14.0)
    assert "begin{aligned}" in latex


def test_render_total_matches_evaluate() -> None:
    combo = Combination("test", "LRFD", {"D": 1.2, "L": 1.6, "Lr": 0.5})
    loads = {"D": 10, "L": 5, "Lr": 3}
    _, total = render_combination(combo, loads)
    assert total == pytest.approx(combo.evaluate(loads))
