"""The file Streamlit actually runs.

Streamlit runs a file from top to bottom as a script. A script cannot use the
``from .something import ...`` style (that only works inside an imported
package), so here we use the full name ``strapp.app`` instead. This file is what
the ``strapp`` command points at.
"""

from strapp.app import main

main()
