import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class DataQualityChecker:
    @staticmethod
    def run_assertions(records: List[Dict[str, Any]]) -> bool:
        """
        Runs quality assertions on the transformed records.
        Returns True if all records pass, raises ValueError otherwise.
        """
        for record in records:
            # Check temperature range (-90 to 60 Celsius)
            temp = record.get("temperature_2m")
            if temp is None or not (-90 <= temp <= 60):
                logger.error(f"Data Quality Issue: Temperature {temp} out of bounds.")
                raise ValueError("Temperature out of bounds.")

            # Check humidity (0 to 100)
            humidity = record.get("relative_humidity_2m")
            if humidity is None or not (0 <= humidity <= 100):
                logger.error(f"Data Quality Issue: Humidity {humidity} out of bounds.")
                raise ValueError("Humidity out of bounds.")

            # Check coordinates
            lat = record.get("latitude")
            lon = record.get("longitude")
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                logger.error(f"Data Quality Issue: Coordinates ({lat}, {lon}) out of bounds.")
                raise ValueError("Coordinates out of bounds.")

        logger.info("All data quality assertions passed.")
        return True
