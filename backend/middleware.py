"""
backend.middleware

HTTP Middleware Komponenten.
"""

from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
)


class RequestIDMiddleware(
    BaseHTTPMiddleware
):
    """
    Fügt jeder Anfrage eine eindeutige ID hinzu.
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):

        request_id = str(
            uuid4()
        )

        response = await call_next(
            request
        )

        response.headers[
            "X-Request-ID"
        ] = request_id

        return response