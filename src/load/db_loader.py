import logging
from typing import Any, Dict, List

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


class DatabaseLoader:
    def __init__(self, db_url: str):
        self.engine: Engine = create_engine(db_url)

    def load_weather_data(self, records: List[Dict[str, Any]]) -> None:
        """
        Loads transformed records into the MySQL database with ON DUPLICATE KEY UPDATE.
        """
        if not records:
            logger.warning("No records to load.")
            return

        insert_query = text("""
            INSERT INTO raw_weather (
                latitude, longitude, measurement_time, temperature_2m,
                relative_humidity_2m, wind_speed_10m, surface_pressure, weather_code
            ) VALUES (
                :latitude, :longitude, :measurement_time, :temperature_2m,
                :relative_humidity_2m, :wind_speed_10m, :surface_pressure, :weather_code
            )
            ON DUPLICATE KEY UPDATE
                temperature_2m = VALUES(temperature_2m),
                relative_humidity_2m = VALUES(relative_humidity_2m),
                wind_speed_10m = VALUES(wind_speed_10m),
                surface_pressure = VALUES(surface_pressure),
                weather_code = VALUES(weather_code)
        """)

        try:
            with self.engine.begin() as conn:
                conn.execute(insert_query, records)
            logger.info(f"Successfully loaded {len(records)} records into the database.")
        except Exception as e:
            logger.error(f"Failed to load records: {e}")
            raise
