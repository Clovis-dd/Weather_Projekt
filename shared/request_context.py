"""
shared.request_context

Verwaltet die aktuelle Request-ID.

Die Request-ID wird genutzt für:

- Logging
- Fehleranalyse
- Request Traceability

Technik:
ContextVar für sichere Nutzung
bei parallelen FastAPI Requests.
"""


from contextvars import (
    ContextVar,
    Token
)



# ======================================================
# Context Variable
# ======================================================


request_id_context: ContextVar[str] = ContextVar(
    "request_id",
    default="-"
)



# ======================================================
# Setzen
# ======================================================


def set_request_id(
    request_id: str
) -> Token:
    """
    Setzt aktuelle Request-ID.

    Returns:
        Token für optionales Zurücksetzen.
    """


    return request_id_context.set(
        str(request_id)
    )



# ======================================================
# Lesen
# ======================================================


def get_request_id() -> str:
    """
    Liefert aktuelle Request-ID.

    Returns:
        Aktuelle ID oder '-'
    """


    return request_id_context.get()



# ======================================================
# Reset
# ======================================================


def reset_request_id(
    token: Token
) -> None:
    """
    Setzt vorherigen Context wieder her.
    """


    request_id_context.reset(
        token
    )