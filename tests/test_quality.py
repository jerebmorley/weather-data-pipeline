import pytest

from src.quality.data_assertions import DataQualityChecker


def test_valid_data():
    records = [
        {
            "latitude": -34.6037,
            "longitude": -58.3816,
            "temperature_2m": 25.0,
            "relative_humidity_2m": 60,
        }
    ]
    checker = DataQualityChecker()
    assert checker.run_assertions(records) is True


def test_invalid_temperature():
    records = [
        {
            "latitude": -34.6037,
            "longitude": -58.3816,
            "temperature_2m": 100.0,  # out of bounds
            "relative_humidity_2m": 60,
        }
    ]
    checker = DataQualityChecker()
    with pytest.raises(ValueError, match="Temperature out of bounds"):
        checker.run_assertions(records)
