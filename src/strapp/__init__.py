"""strapp: a beginner-friendly Streamlit app for ASCE 7-22 load combinations.

The pieces:

* :mod:`strapp.combinations` - the load combination math (no web code).
* :mod:`strapp.simulation` - the random "what if" study.
* :mod:`strapp.handcalc_view` - shows one combination as nice math.
* :mod:`strapp.app` - the Streamlit web page.
"""

import tomllib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from .combinations import (
    Combination,
    asd_combinations,
    evaluate_all,
    get_combinations,
    governing_combination,
    lrfd_combinations,
)
from .simulation import SimulationResult, simulate

# pyproject.toml is the single source of truth for the version. When the package
# is installed we read it from metadata; when the app runs straight from source
# (the package is on sys.path but was never pip-installed) we fall back to
# reading pyproject.toml directly. Bump with `uv version --bump patch|minor|major`.
try:
    __version__ = version("strapp")
except PackageNotFoundError:
    _pyproject = Path(__file__).resolve().parents[2] / "pyproject.toml"
    __version__ = tomllib.loads(_pyproject.read_text(encoding="utf-8"))["project"]["version"]

__all__ = [
    "Combination",
    "SimulationResult",
    "__version__",
    "asd_combinations",
    "evaluate_all",
    "get_combinations",
    "governing_combination",
    "lrfd_combinations",
    "simulate",
]
