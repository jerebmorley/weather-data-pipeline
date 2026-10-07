import logging
from pathlib import Path

from config.settings import settings
from src.extract.weather_extractor import WeatherExtractor
from src.load.db_loader import DatabaseLoader
from src.quality.data_assertions import DataQualityChecker
from src.transform.transformer import WeatherTransformer

logging.basicConfig(
    level=settings.log_level, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


def run_pipeline():
    logger.info("Starting Weather Data Pipeline")

    bronze_dir = Path("data/bronze")

    # 1. Extract
    extractor = WeatherExtractor(base_url=settings.open_meteo_url)
    raw_data = extractor.fetch_weather_data(
        lat=settings.target_latitude, lon=settings.target_longitude
    )
    extractor.save_to_bronze(raw_data, bronze_dir)

    # 2. Transform
    transformer = WeatherTransformer()
    transformed_records = transformer.parse_raw_data(raw_data)

    # 3. Quality Check
    checker = DataQualityChecker()
    checker.run_assertions(transformed_records)

    # 4. Load
    loader = DatabaseLoader(db_url=settings.database_url)
    loader.load_weather_data(transformed_records)

    logger.info("Pipeline executed successfully.")


if __name__ == "__main__":
    run_pipeline()
