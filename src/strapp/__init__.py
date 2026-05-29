"""strapp: a beginner-friendly Streamlit app for ASCE 7-22 load combinations.

The pieces:

* :mod:`strapp.combinations` - the load combination math (no web code).
* :mod:`strapp.simulation` - the random "what if" study.
* :mod:`strapp.handcalc_view` - shows one combination as nice math.
* :mod:`strapp.app` - the Streamlit web page.
"""

from .combinations import (
    Combination,
    asd_combinations,
    evaluate_all,
    get_combinations,
    governing_combination,
    lrfd_combinations,
)
from .simulation import SimulationResult, simulate

__version__ = "0.1.2"

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
