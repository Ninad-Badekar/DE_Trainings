# 🌦️ Airflow Weather ETL Pipeline

This project implements an ETL (Extract, Transform, Load) pipeline using **Apache Airflow** to collect real-time weather data from the **Open-Meteo API**, process it, and store it in a **PostgreSQL** database.

---

## 📌 Overview

The DAG (Directed Acyclic Graph) performs the following tasks daily:

1. **Extract**: Fetches current weather data for a given location (latitude & longitude) from Open-Meteo.
2. **Transform**: Extracts relevant fields such as temperature, windspeed, and weather code from the API response.
3. **Load**: Saves the transformed data into a PostgreSQL table (`weather_data`), creating the table if it doesn't exist.

---

## 🧱 Tech Stack

| Component       | Description                                      |
|----------------|--------------------------------------------------|
| Apache Airflow | Workflow orchestration tool                     |
| Open-Meteo API | Free API to get real-time and forecast weather  |
| PostgreSQL     | Relational database to store weather data       |
| Python         | Language used to implement the DAG logic        |

---

## 📂 Directory Structure

```bash
Day27/
│
├── dags/
│ └── weather_etl_pipeline.py # The ETL DAG definition
```

---

## ⚙️ Requirements

- Airflow 2.6+
- Python 3.7+
- PostgreSQL (running and accessible)
- Open-Meteo API (no API key required)
- Airflow Connections:
  - `open_meteo_api` (HTTP connection to `https://api.open-meteo.com`)
  - `postgres_default` (PostgreSQL connection configured in Airflow)

---

## 🔌 Airflow Connection Setup

### 1. 📡 HTTP Connection for Open-Meteo API

In Airflow UI, go to **Admin → Connections** and add:

- **Conn Id**: `open_meteo_api`
- **Conn Type**: `HTTP`
- **Host**: `https://api.open-meteo.com`

### 2. 🗃️ PostgreSQL Connection

Use the default or configure your own:

- **Conn Id**: `postgres_default`
- **Conn Type**: `Postgres`
- **Host**: `your_host`
- **Schema**: `your_database`
- **Login**: `your_username`
- **Password**: `your_password`
- **Port**: `5432`

---

## 🧠 DAG Explanation

### DAG Definition

```python
@dag(
    dag_id='weather_etl_pipeline',
    start_date=datetime.now() - timedelta(days=1),
    schedule='@daily',
    catchup=False,
    default_args={'owner': 'airflow'},
    tags=['weather', 'etl']
)
```
- Runs daily

- Starts from yesterday

- No backfilling (catchup=False)

## 🔍 Tasks Breakdown

### 1. `extract_weather_data`

- Uses `HttpHook` to call Open-Meteo API.
- Endpoint:  
```bash
/v1/forecast?latitude=51.5074&longitude=-0.1278&current_weather=true
```
- Returns the JSON payload.

### 2. `transform_weather_data`

Extracts relevant fields:

- `temperature`
- `windspeed`
- `winddirection`
- `weathercode`

Returns a dictionary with clean data.

### 3. `load_weather_data`

- Connects to Postgres using `PostgresHook`
- Creates a `weather_data` table (if it doesn't exist)
- Inserts the transformed data into the table

#### Table schema:

```sql
CREATE TABLE weather_data (
  latitude FLOAT,
  longitude FLOAT,
  temperature FLOAT,
  windspeed FLOAT,
  winddirection FLOAT,
  weathercode INT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```