from unittest.mock import Mock, patch

import requests

from frontend.backend_client import (
    get_weather,
    BackendConnectionError,
)

from shared.models import WeatherResponse



def test_get_weather_success():

    fake_response = Mock()

    fake_response.status_code = 200

    fake_response.ok = True

    fake_response.headers = {
        "X-Request-ID": "test-id"
    }

    fake_response.json.return_value = {

    "location": {

        "city": "Berlin",

        "country": "DE",

        "country_name": "Germany",

        "latitude": 52.52,

        "longitude": 13.405,

    },

    "weather": {

        "temperature": 20.5,

        "feels_like": 19.8,

        "humidity": 60,

        "pressure": 1015,

        "wind_speed": 4.2,

        "clouds": 30,

        "visibility": 10000,

    },

    "timestamp": "2026-07-13T10:00:00",

    "language": "de",

}


    with patch(
        "frontend.backend_client._session.post",
        return_value=fake_response,
    ) as mock_post:


        result = get_weather(
            "Berlin",
            "de",
        )


    assert isinstance(
        result,
        WeatherResponse,
    )


    assert result.location.city == "Berlin"


    mock_post.assert_called_once()



def test_get_weather_backend_unavailable():

    with patch(
        "frontend.backend_client._session.post",
        side_effect=requests.exceptions.ConnectionError,
    ):


        try:

            get_weather(
                "Berlin"
            )


        except BackendConnectionError as error:

            assert (
                str(error)
                ==
                "Backend nicht erreichbar."
            )


        else:

            assert False, (
                "BackendConnectionError expected"
            )