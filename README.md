# End-to-End Weather Data Pipeline

## 🎯 Project Objective
A production-ready ELT/ETL pipeline for real-time weather monitoring and data quality. It extracts weather data from the Open-Meteo API, persists raw data in a Bronze layer, transforms and validates the data, and loads it into a normalized MySQL 8.0 schema.

## 🏗️ Architecture & Pipeline Flow
The pipeline follows a Medallion Architecture (Bronze -> Silver -> Gold):

1. **Extract (Bronze Layer)**
   - Executed via `src/extract/weather_extractor.py`.
   - Connects to the free Open-Meteo API using a resilient HTTP client (`requests` + `tenacity` for retries/timeouts).
   - Raw JSON responses are saved directly into partitioned local directories simulating a data lake: `data/bronze/date=YYYY-MM-DD/weather_*.json`.

2. **Transform & Quality Checks (Silver Layer)**
   - Executed via `src/transform/transformer.py` and `src/quality/data_assertions.py`.
   - Parses the JSON payload, standardizes timestamps into UTC, and flattens the nested data.
   - Applies strict data contracts: checks if temperature is within valid earthly bounds (-90°C to 60°C), humidity is between 0-100%, and coordinates are valid.

3. **Load (Silver Layer persistence)**
   - Executed via `src/load/db_loader.py`.
   - Connects to the local MySQL database using `SQLAlchemy`.
   - Ensures idempotency: inserts data safely using an `ON DUPLICATE KEY UPDATE` strategy to prevent duplicate records if the pipeline is rerun for the same timestamps.

4. **Analytics (Gold Layer)**
   - Available via `sql/queries/daily_metrics_rollup.sql`.
   - Aggregates the raw measurements using clean CTEs to compute daily average, max, and min temperatures, alongside average wind speeds and humidity.

## 🚀 Quick Start & Walkthrough

### 1. Requirements
- Python 3.10+
- Docker and Docker Compose

### 2. Setup
Clone the repository and prepare the virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```
Prepare the environment variables:
```bash
cp .env.example .env
```

### 3. Run Database Infrastructure
Start the MySQL database and Adminer interface:
```bash
sudo docker compose -f docker/docker-compose.yml up -d
```

### 4. Execute Pipeline
Run the ETL orchestrator:
```bash
python src/main.py
```

### 5. Inspect the Results
1. **Raw Files**: Check the `data/bronze/` folder for your JSON payloads.
2. **Database Data**: Open your browser and go to `http://localhost:8080` to access Adminer.
   - **System:** MySQL
   - **Server:** `mysql`
   - **User:** `pipeline_user`
   - **Password:** `pipeline_pass`
   - **Database:** `weather_db`
   - Explore the `raw_weather` table or run the query from `sql/queries/daily_metrics_rollup.sql` in the SQL Command tab.

## 🛠️ Code Quality Tools
This repository uses strict code quality tools, configured in `pyproject.toml`, `ruff.toml`, and `.sqlfluff`:
- **Python**: Ruff (Linter & Formatter), Pytest, Pylance
- **SQL**: SQLFluff

Run local checks:
```bash
ruff check . --fix
ruff format .
sqlfluff fix sql/
pytest tests/
```

---

## 🛑 Troubleshooting & Challenges Resolved
During the development and initial setup of this project, we encountered several challenges related to environments, permissions, and tool configurations. Below is the detailed log of how we solved them:

### 1. Python Package Building (`hatchling` Metadata Generation Failed)
* **Error**: When running `pip install -e .[dev]`, hatchling failed with `ValueError: Unable to determine which files to ship inside the wheel`.
* **Cause**: Hatchling expects a standard layout (e.g., `src/weather_data_pipeline/`) matching the project name. Because we used a flatter structure (`src/extract`, `src/load`, etc. and a `config/` folder), it didn't know what to package.
* **Solution**: Explicitly defined the packages to include in `pyproject.toml`:
  ```toml
  [tool.hatch.build.targets.wheel]
  packages = ["src", "config"]
  ```

### 2. Docker Compose "Version is Obsolete" Warning
* **Error**: `the attribute version is obsolete, it will be ignored`.
* **Cause**: Modern versions of Docker Compose Specification no longer use or require the `version` field at the top of the YAML file.
* **Solution**: Removed the `version: '3.8'` line from `docker/docker-compose.yml`.

### 3. Docker Daemon Permission Denied
* **Error**: `permission denied while trying to connect to the docker API at unix:///var/run/docker.sock`.
* **Cause**: The user environment (especially common in `snap` installations of Docker on Ubuntu) didn't have the required permissions to speak to the root-owned Docker daemon without `sudo`.
* **Solution**: Advised executing Docker compose with `sudo` (`sudo docker compose up -d`) as an immediate unblocker, and provided the long-term solution of adding the user to the docker group (`sudo usermod -aG docker $USER` and `newgrp docker`).

### 4. MySQL Port Collision (`Address already in use`)
* **Error**: `failed to bind host port 0.0.0.0:3306/tcp: address already in use`.
* **Cause**: The host machine already had a native MySQL or MariaDB service running locally on port 3306, preventing the Docker container from binding to the same port.
* **Solution**: 
  - Updated `docker-compose.yml` to map host port 3307 to container port 3306 (`3307:3306`).
  - Updated `.env.example` and `config/settings.py` so the Python scripts connect via port `3307` by default.

### 5. Code Quality & Linting Violations
After running the initial CI checks, multiple rules were triggered and subsequently fixed:
* **Ruff (E501)**: List of fields in `weather_extractor.py` exceeded the 100-character line limit. Resolved automatically by running `ruff format .`.
* **Ruff (B904)**: Exception chaining was missing in `transformer.py`. Fixed by updating the `raise ValueError(...)` to `raise ValueError(...) from e`.
* **Pytest Warning**: `datetime.utcnow()` was flagged as deprecated in modern Python versions. Refactored the code to use standard UTC-aware objects: `datetime.now(timezone.utc)`.
* **SQLFluff (ST06)**: SQL style rules enforced that simple columns (like `latitude`, `longitude`) must be selected before calculation functions (like `DATE(measurement_time)`). The command `sqlfluff fix sql/` successfully reordered the SELECT statement automatically.
