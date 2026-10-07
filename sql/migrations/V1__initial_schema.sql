CREATE TABLE IF NOT EXISTS raw_weather (
    id INT AUTO_INCREMENT PRIMARY KEY,
    latitude DECIMAL(10, 6) NOT NULL,
    longitude DECIMAL(10, 6) NOT NULL,
    measurement_time DATETIME NOT NULL,
    temperature_2m DECIMAL(5, 2),
    relative_humidity_2m INT,
    wind_speed_10m DECIMAL(5, 2),
    surface_pressure DECIMAL(7, 2),
    weather_code INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_measurement (latitude, longitude, measurement_time)
);

CREATE TABLE IF NOT EXISTS daily_weather_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    measurement_date DATE NOT NULL,
    latitude DECIMAL(10, 6) NOT NULL,
    longitude DECIMAL(10, 6) NOT NULL,
    avg_temperature DECIMAL(5, 2),
    max_temperature DECIMAL(5, 2),
    min_temperature DECIMAL(5, 2),
    avg_humidity DECIMAL(5, 2),
    avg_wind_speed DECIMAL(5, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_daily_summary (measurement_date, latitude, longitude)
);
