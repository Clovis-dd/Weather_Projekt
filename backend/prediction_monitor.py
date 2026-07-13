"""
prediction_monitor.py

Monitoring für ML Predictions.

Verantwortlichkeiten:

- Anzahl Predictions erfassen
- Fehler zählen
- Laufzeiten messen
- letztes Modell speichern
- letzte Prediction speichern

Später erweiterbar für:
- Prometheus
- Grafana
- Application Insights
"""


from __future__ import annotations


from datetime import UTC, datetime
from threading import Lock

from shared.logger import get_logger


logger = get_logger(
    __name__
)



class PredictionMonitor:
    """
    Zentraler Speicher für Prediction-Metriken.
    """


    def __init__(self) -> None:

        self._lock = Lock()

        self.predictions_total = 0

        self.prediction_errors = 0

        self.total_latency_ms = 0.0

        self.last_latency_ms = 0.0

        self.last_prediction_time = None

        self.last_model_name = None



    # ==================================================
    # Prediction erfolgreich
    # ==================================================

    def record_success(
        self,
        *,
        latency_ms: float,
        model_name: str,
    ) -> None:
        """
        Speichert erfolgreiche Prediction.
        """


        with self._lock:

            self.predictions_total += 1

            self.total_latency_ms += latency_ms

            self.last_latency_ms = latency_ms

            self.last_prediction_time = (
                datetime.now(
                    UTC
                )
            )

            self.last_model_name = model_name



        logger.debug(
            "Prediction recorded latency=%.2fms model=%s",
            latency_ms,
            model_name,
        )



    # ==================================================
    # Fehler
    # ==================================================

    def record_error(
        self
    ) -> None:
        """
        Speichert Prediction Fehler.
        """


        with self._lock:

            self.prediction_errors += 1



    # ==================================================
    # Export
    # ==================================================

    def get_metrics(
        self
    ) -> dict:
        """
        Gibt aktuelle Metriken zurück.
        """


        with self._lock:

            average_latency = 0.0


            if self.predictions_total:

                average_latency = (
                    self.total_latency_ms
                    /
                    self.predictions_total
                )


            return {

                "predictions_total":
                    self.predictions_total,


                "prediction_errors":
                    self.prediction_errors,


                "average_latency_ms":
                    round(
                        average_latency,
                        3,
                    ),


                "last_latency_ms":
                    round(
                        self.last_latency_ms,
                        3,
                    ),


                "last_prediction_time":
                    (
                        self.last_prediction_time.isoformat()
                        if self.last_prediction_time
                        else None
                    ),


                "last_model_name":
                    self.last_model_name,

            }



# ======================================================
# Singleton
# ======================================================


prediction_monitor = PredictionMonitor()