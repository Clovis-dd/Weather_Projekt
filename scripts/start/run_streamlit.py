"""
run_streamlit.py

Startet den Streamlit-Server für die Weather App.
"""

import sys

from scripts.bootstrap import initialize


initialize()


from streamlit.web.cli import main


sys.argv = [
    "streamlit",
    "run",
    "frontend/app.py",
]


main()