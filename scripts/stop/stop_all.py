"""
stop_all.py

Beendet Backend und Streamlit.
"""

from __future__ import annotations

import subprocess


PORTS = (
    9000,
    8501,
)


def stop_port(
    port: int,
) -> None:

    result = subprocess.run(
        ["lsof", "-ti", f":{port}"],
        capture_output=True,
        text=True,
    )

    pid = result.stdout.strip()

    if pid:

        subprocess.run(
            ["kill", pid]
        )

        print(
            f"Port {port}: Prozess {pid} beendet."
        )

    else:

        print(
            f"Port {port}: nichts gefunden."
        )


def main() -> None:

    for port in PORTS:

        stop_port(port)


if __name__ == "__main__":
    main()