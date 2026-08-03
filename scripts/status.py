"""
status.py

Zeigt den Status der Projektkomponenten.
"""

from __future__ import annotations

import socket


SERVICES = {

    "Backend": 9000,

    "Streamlit": 8501,

}


def running(
    port: int,
) -> bool:

    with socket.socket() as sock:

        return sock.connect_ex(
            ("127.0.0.1", port)
        ) == 0


def main() -> None:

    print()

    print("Projektstatus")

    print("-" * 30)

    for name, port in SERVICES.items():

        state = (
            "läuft"
            if running(port)
            else "gestoppt"
        )

        print(
            f"{name:<12} {state} (Port {port})"
        )


if __name__ == "__main__":
    main()