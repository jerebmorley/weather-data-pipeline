from pathlib import Path

import requests_mock

from src.extract.weather_extractor import WeatherExtractor


def test_fetch_weather_data_success():
    extractor = WeatherExtractor("http://fake-api.com")
    mock_response = {
        "latitude": -34.6037,
        "longitude": -58.3816,
        "current": {
            "temperature_2m": 20.5,
            "relative_humidity_2m": 50,
            "wind_speed_10m": 15.0,
            "surface_pressure": 1013.25,
            "weather_code": 0,
            "time": "2023-10-25T14:00:00Z",
        },
    }

    with requests_mock.Mocker() as m:
        m.get("http://fake-api.com", json=mock_response)
        data = extractor.fetch_weather_data(-34.6037, -58.3816)

    assert data["latitude"] == -34.6037
    assert data["current"]["temperature_2m"] == 20.5


def test_save_to_bronze(tmp_path: Path):
    extractor = WeatherExtractor("http://fake-api.com")
    data = {"test": "data"}
    file_path = extractor.save_to_bronze(data, tmp_path)

    assert file_path.exists()
    assert file_path.suffix == ".json"
