"""
stop_streamlit.py

Beendet einen laufenden Streamlit-Prozess.
"""

from __future__ import annotations

import subprocess

PORT = 8501


def main() -> None:

    result = subprocess.run(
        ["lsof", "-ti", f":{PORT}"],
        capture_output=True,
        text=True,
    )

    pid = result.stdout.strip()

    if not pid:
        print(
            f"Kein Streamlit auf Port {PORT} gefunden."
        )
        return

    subprocess.run(
        ["kill", pid]
    )

    print(
        f"Streamlit (PID {pid}) wurde beendet."
    )


if __name__ == "__main__":
    main()