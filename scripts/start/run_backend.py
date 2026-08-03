"""
run_backend.py

Startet den FastAPI-Server für die Weather App.
"""

from scripts.bootstrap import initialize

initialize()

from uvicorn import run

if __name__ == "__main__":
    run(
        "backend.api:app",
        host="127.0.0.1",
        port=9000,
        reload=True,
    )