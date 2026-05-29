"""strapp: a beginner-friendly Streamlit app for ASCE 7-22 load combinations.

The pieces:

* :mod:`strapp.combinations` - the load combination math (no web code).
* :mod:`strapp.simulation` - the random "what if" study.
* :mod:`strapp.handcalc_view` - shows one combination as nice math.
* :mod:`strapp.app` - the Streamlit web page.
"""

from importlib.metadata import version

from .combinations import (
    Combination,
    asd_combinations,
    evaluate_all,
    get_combinations,
    governing_combination,
    lrfd_combinations,
)
from .simulation import SimulationResult, simulate

# Read the version from the installed package metadata so pyproject.toml stays
# the single source of truth. Bump it with `uv version --bump patch|minor|major`.
__version__ = version("strapp")

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
