import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class WeatherTransformer:
    @staticmethod
    def parse_raw_data(raw_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Transforms raw JSON from Open-Meteo into a flattened dictionary suitable for loading.
        """
        try:
            lat = raw_data["latitude"]
            lon = raw_data["longitude"]
            current = raw_data["current"]

            # Open-Meteo returns ISO8601 strings for time
            measurement_time = datetime.fromisoformat(current["time"].replace("Z", "+00:00"))

            transformed = {
                "latitude": lat,
                "longitude": lon,
                "measurement_time": measurement_time,
                "temperature_2m": current["temperature_2m"],
                "relative_humidity_2m": current["relative_humidity_2m"],
                "wind_speed_10m": current["wind_speed_10m"],
                "surface_pressure": current.get("surface_pressure"),
                "weather_code": current.get("weather_code"),
            }
            logger.info("Successfully transformed raw data.")
            return [transformed]
        except KeyError as e:
            logger.error(f"Missing expected key in raw data: {e}")
            raise ValueError(f"Invalid data schema: missing {e}") from e
