from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 3307
    db_user: str = "pipeline_user"
    db_password: str = "pipeline_pass"
    db_name: str = "weather_db"

    open_meteo_url: str = "https://api.open-meteo.com/v1/forecast"
    target_latitude: float = -34.6037  # Default: Buenos Aires
    target_longitude: float = -58.3816

    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()
