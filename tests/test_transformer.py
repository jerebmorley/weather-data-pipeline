from datetime import datetime

import pytest

from src.transform.transformer import WeatherTransformer


def test_parse_raw_data_valid():
    raw_data = {
        "latitude": -34.6037,
        "longitude": -58.3816,
        "current": {
            "time": "2023-10-25T14:00:00Z",
            "temperature_2m": 20.5,
            "relative_humidity_2m": 50,
            "wind_speed_10m": 15.0,
            "surface_pressure": 1013.25,
            "weather_code": 0,
        },
    }

    transformer = WeatherTransformer()
    result = transformer.parse_raw_data(raw_data)

    assert len(result) == 1
    record = result[0]
    assert record["latitude"] == -34.6037
    assert record["temperature_2m"] == 20.5
    assert isinstance(record["measurement_time"], datetime)
    assert record["measurement_time"].tzinfo is not None


def test_parse_raw_data_missing_keys():
    raw_data = {
        "latitude": -34.6037
        # missing longitude and current
    }
    transformer = WeatherTransformer()
    with pytest.raises(ValueError):
        transformer.parse_raw_data(raw_data)
