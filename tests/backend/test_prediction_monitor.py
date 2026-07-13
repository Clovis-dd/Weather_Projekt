from backend.prediction_monitor import PredictionMonitor


def test_monitor_starts_empty():

    monitor = PredictionMonitor()

    metrics = monitor.get_metrics()

    assert metrics["predictions_total"] == 0

    assert metrics["prediction_errors"] == 0

    assert metrics["average_latency_ms"] == 0.0

    assert metrics["last_model_name"] is None



def test_record_success_updates_metrics():

    monitor = PredictionMonitor()

    monitor.record_success(
        latency_ms=120.5,
        model_name="weather_model_test",
    )


    metrics = monitor.get_metrics()


    assert metrics["predictions_total"] == 1

    assert metrics["prediction_errors"] == 0

    assert metrics["average_latency_ms"] == 120.5

    assert metrics["last_latency_ms"] == 120.5

    assert metrics["last_model_name"] == "weather_model_test"

    assert metrics["last_prediction_time"] is not None



def test_record_multiple_successes_calculates_average():

    monitor = PredictionMonitor()


    monitor.record_success(
        latency_ms=100,
        model_name="model_a",
    )


    monitor.record_success(
        latency_ms=200,
        model_name="model_a",
    )


    metrics = monitor.get_metrics()


    assert metrics["predictions_total"] == 2

    assert metrics["average_latency_ms"] == 150.0

    assert metrics["last_latency_ms"] == 200



def test_record_error_increments_error_counter():

    monitor = PredictionMonitor()


    monitor.record_error()


    metrics = monitor.get_metrics()


    assert metrics["prediction_errors"] == 1

    assert metrics["predictions_total"] == 0



def test_error_does_not_change_success_metrics():

    monitor = PredictionMonitor()


    monitor.record_success(
        latency_ms=50,
        model_name="model_test",
    )


    monitor.record_error()


    metrics = monitor.get_metrics()


    assert metrics["predictions_total"] == 1

    assert metrics["prediction_errors"] == 1

    assert metrics["last_model_name"] == "model_test"