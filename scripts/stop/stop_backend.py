"""
stop_backend.py

Beendet einen laufenden FastAPI/Uvicorn-Prozess.
"""

from __future__ import annotations

import subprocess

PORT = 9000


def main() -> None:

    result = subprocess.run(
        ["lsof", "-ti", f":{PORT}"],
        capture_output=True,
        text=True,
    )

    pid = result.stdout.strip()

    if not pid:
        print(f"Kein Backend auf Port {PORT} gefunden.")
        return

    subprocess.run(["kill", pid])

    print(
        f"Backend (PID {pid}) wurde beendet."
    )


if __name__ == "__main__":
    main()