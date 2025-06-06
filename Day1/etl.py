import requests
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import logging
from datetime import datetime

# ==== Setup Logging ====
logging.basicConfig(
    filename='covid_data_pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ==== Fetch API Data ====
def fetch_api(country="India", lastdays=30):
    try:
        url = f"https://disease.sh/v3/covid-19/historical/{country}?lastdays={lastdays}"
        logging.info(f"Fetching data from API for {country}, last {lastdays} days")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        timeline = data['timeline']
        df_cases = pd.DataFrame(timeline['cases'].items(), columns=['Date', 'Cases'])
        df_deaths = pd.DataFrame(timeline['deaths'].items(), columns=['Date', 'Deaths'])
        df_recovered = pd.DataFrame(timeline['recovered'].items(), columns=['Date', 'Recovered'])

        df = df_cases.merge(df_deaths, on='Date').merge(df_recovered, on='Date')
        df['Date'] = pd.to_datetime(df['Date'])
        
        logging.info("Successfully fetched and structured the data")
        return df
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        raise


# ====  Save to CSV ====
def save_to_csv(df, filename="covid_data.csv"):
    try:
        df.to_csv(filename, index=False)
        logging.info(f"Data saved to CSV: {filename}")
    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")
        raise


# ==== 3. Save to MySQL ====
def save_to_mysql(df, table_name="covid_data"):
    try:
        engine = create_engine("mysql+pymysql://root:ninad123@localhost/de_training")
        df.to_sql(table_name, con=engine, index=False, if_exists='replace')
        logging.info(f"Data saved to MySQL table: {table_name}")
    except Exception as e:
        logging.error(f"Error saving to MySQL: {e}")
        raise


# ==== 4. Perform Aggregations ====
def aggregations(df):
    try:
        logging.info("Performing aggregations")
        total_cases = df['Cases'].iloc[-1] - df['Cases'].iloc[0]
        total_deaths = df['Deaths'].iloc[-1] - df['Deaths'].iloc[0]
        total_recovered = df['Recovered'].iloc[-1] - df['Recovered'].iloc[0]
        avg_daily = df['Cases'].diff().mean()
        max_daily = df['Cases'].diff().max()
        min_daily = df['Cases'].diff().min()

        logging.info(f"Total Cases: {total_cases}")
        logging.info(f"Total Deaths: {total_deaths}")
        logging.info(f"Total Recovered: {total_recovered}")
        logging.info(f"Avg Daily Cases: {avg_daily}")
        logging.info(f"Max Daily Cases: {max_daily}")
        logging.info(f"Min Daily Cases: {min_daily}")

        print("\n--- Aggregation Results ---")
        print(f"Total cases: {total_cases}")
        print(f"Total deaths: {total_deaths}")
        print(f"Total recovered: {total_recovered}")
        print(f"Average daily cases: {avg_daily:.2f}")
        print(f"Max daily cases: {max_daily}")
        print(f"Min daily cases: {min_daily}")
    except Exception as e:
        logging.error(f"Error during aggregation: {e}")
        raise



logging.info("Starting COVID data pipeline")

df = fetch_api("India", 100)
save_to_csv(df)
save_to_mysql(df)
aggregations(df)
logging.info("COVID data pipeline completed successfully")


