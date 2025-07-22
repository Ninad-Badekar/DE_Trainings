from pyspark.sql import SparkSession
import os
import sys

def load_parquet_to_postgres(spark, table_path, table_name, jdbc_url, connection_props):
    print(f"🚚 Loading {table_name} from {table_path}")
    try:
        df = spark.read.parquet(table_path)
        df.write.jdbc(
            url=jdbc_url,
            table=table_name,
            mode="overwrite",  # change to 'append' if you want incremental loads
            properties=connection_props
        )
        print(f"✅ Loaded {table_name} into PostgreSQL")
    except Exception as e:
        print(f"❌ Failed to load {table_name}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: load_to_warehouse.py <gold_base_path>")
        sys.exit(1)

    gold_base = sys.argv[1]  # e.g., /opt/data_lake/gold

    spark = SparkSession.builder \
        .appName("Load to PostgreSQL Warehouse") \
        .config("spark.jars", "/opt/spark-jars/postgresql-42.6.0.jar") \
        .getOrCreate()

    print("🚀 Starting load to Data Warehouse")

    jdbc_url = "jdbc:postgresql://postgres_dw:5432/ipl_warehouse"
    connection_props = {
        "user": "ipl_data",
        "password": "ipl_data",
        "driver": "org.postgresql.Driver"
    }

    tables = [
        "dim_teams",
        "dim_venues",
        "dim_players",
        "fact_matches",
        "fact_deliveries"
        # dim_date can be added if it's part of the Gold pipeline
    ]

    for table in tables:
        table_path = os.path.join(gold_base, table)
        load_parquet_to_postgres(spark, table_path, table, jdbc_url, connection_props)

    print("🎯 All tables loaded to PostgreSQL warehouse.")
    spark.stop()
