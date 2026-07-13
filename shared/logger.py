"""
Zentrale Logging-Konfiguration.

Features:

- Console Logging
- app.log
- warning.log
- error.log
- Request-ID Integration
"""


import logging


from shared.config import settings
from shared.request_context import get_request_id



# ======================================================
# Filter
# ======================================================


class RequestIdFilter(
    logging.Filter
):
    """
    Fügt jedem LogRecord eine Request-ID hinzu.
    """


    def filter(
        self,
        record: logging.LogRecord
    ) -> bool:

        record.request_id = (
            get_request_id()
        )

        return True



class WarningOnlyFilter(
    logging.Filter
):
    """
    Erlaubt nur WARNING Meldungen.
    """


    def filter(
        self,
        record: logging.LogRecord
    ) -> bool:

        return (
            record.levelno
            ==
            logging.WARNING
        )



# ======================================================
# Logging Setup
# ======================================================


def configure_logging() -> None:
    """
    Initialisiert Logging einmalig.
    """


    root_logger = logging.getLogger()



    if root_logger.handlers:

        return



    settings.LOG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )



    root_logger.setLevel(
        getattr(
            logging,
            settings.LOG_LEVEL.upper(),
            logging.INFO
        )
    )



    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)-8s | "
        "%(name)s | "
        "request_id=%(request_id)s | "
        "%(message)s"
    )



    request_filter = RequestIdFilter()



    # --------------------------------------------------
    # Console
    # --------------------------------------------------


    console = logging.StreamHandler()

    console.setLevel(
        logging.INFO
    )

    console.setFormatter(
        formatter
    )

    console.addFilter(
        request_filter
    )



    # --------------------------------------------------
    # app.log
    # --------------------------------------------------


    app_file = logging.FileHandler(
        settings.APP_LOG_FILE,
        encoding="utf-8"
    )

    app_file.setLevel(
        logging.INFO
    )

    app_file.setFormatter(
        formatter
    )

    app_file.addFilter(
        request_filter
    )



    # --------------------------------------------------
    # warning.log
    # --------------------------------------------------


    warning_file = logging.FileHandler(
        settings.WARNING_LOG_FILE,
        encoding="utf-8"
    )


    warning_file.setLevel(
        logging.WARNING
    )


    warning_file.addFilter(
        WarningOnlyFilter()
    )


    warning_file.setFormatter(
        formatter
    )


    warning_file.addFilter(
        request_filter
    )



    # --------------------------------------------------
    # error.log
    # --------------------------------------------------


    error_file = logging.FileHandler(
        settings.ERROR_LOG_FILE,
        encoding="utf-8"
    )


    error_file.setLevel(
        logging.ERROR
    )


    error_file.setFormatter(
        formatter
    )


    error_file.addFilter(
        request_filter
    )



    # --------------------------------------------------
    # Registrierung
    # --------------------------------------------------


    root_logger.addHandler(
        console
    )

    root_logger.addHandler(
        app_file
    )

    root_logger.addHandler(
        warning_file
    )

    root_logger.addHandler(
        error_file
    )



# ======================================================
# Logger Factory
# ======================================================


def get_logger(
    name: str
) -> logging.Logger:
    """
    Erstellt Modul-Logger.
    """


    configure_logging()


    return logging.getLogger(
        name
    )