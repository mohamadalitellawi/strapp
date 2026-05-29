"""A tiny command line entry point.

Because we list this in ``pyproject.toml`` under ``[project.scripts]``, anyone
who installs the package gets a ``strapp`` command. Running it starts the web app
by handing control to Streamlit.
"""

from __future__ import annotations

import sys
from pathlib import Path

from streamlit.web import cli as streamlit_cli


def main() -> None:
    """Start the Streamlit app from the command line."""
    entry_file = Path(__file__).with_name("_entry.py")
    sys.argv = ["streamlit", "run", str(entry_file)]
    streamlit_cli.main()
