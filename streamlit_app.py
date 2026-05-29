"""Start file for running the app.

Streamlit Community Cloud (the free hosting service) looks for a file like this
at the top of the repository. Run it on your own computer with::

    uv run streamlit run streamlit_app.py

Our real code lives in the ``src/`` folder, so we add that folder to the place
Python looks for code, then start the app.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from strapp.app import main  # noqa: E402 - must come after the sys.path line above

main()
