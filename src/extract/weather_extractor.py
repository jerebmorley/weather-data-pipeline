import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class WeatherExtractor:
    def __init__(self, base_url: str):
        self.base_url = base_url

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def fetch_weather_data(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Fetches current weather data from Open-Meteo API.
        """
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "wind_speed_10m",
                "surface_pressure",
                "weather_code",
            ],
        }
        logger.info(f"Fetching weather data for lat:{lat}, lon:{lon}")
        response = requests.get(self.base_url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def save_to_bronze(self, data: Dict[str, Any], bronze_dir: Path) -> Path:
        """
        Saves raw JSON data to the bronze layer partitioned by date.
        """
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        target_dir = bronze_dir / f"date={today}"
        target_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        file_path = target_dir / f"weather_{timestamp}.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        logger.info(f"Raw data saved to {file_path}")
        return file_path
