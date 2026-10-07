WITH daily_stats AS (
    SELECT
        latitude,
        longitude,
        DATE(measurement_time) AS measurement_date,
        AVG(temperature_2m) AS avg_temperature,
        MAX(temperature_2m) AS max_temperature,
        MIN(temperature_2m) AS min_temperature,
        AVG(relative_humidity_2m) AS avg_humidity,
        AVG(wind_speed_10m) AS avg_wind_speed
    FROM raw_weather
    GROUP BY
        DATE(measurement_time),
        latitude,
        longitude
)

SELECT * FROM daily_stats;
