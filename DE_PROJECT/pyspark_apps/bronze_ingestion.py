from pyspark.sql import SparkSession
import sys
from datetime import datetime

def log(msg):
    """Logs message to console and to a debug file."""
    print(msg)
    with open("/opt/spark-apps/bronze_debug.log", "a") as log_file:
        log_file.write(msg + "\n")

def ingest_table_to_bronze(spark, jdbc_url, connection_properties, table_name, bronze_base_path):
    """Ingests a MySQL table to the Bronze layer, partitioned by ingestion date."""
    log(f"🚀 Starting ingestion for table: {table_name}")

    try:
        df = spark.read.jdbc(url=jdbc_url, table=table_name, properties=connection_properties)

        row_count = df.count()
        log(f"📊 Row count for '{table_name}': {row_count}")
        df.show(5)

        today = datetime.today()
        year = today.strftime("%Y")
        month = today.strftime("%m")
        day = today.strftime("%d")

        output_path = f"{bronze_base_path}/mysql/{table_name}/{year}/{month}/{day}"
        log(f"📁 Writing data to: {output_path}")

        df.write.mode("overwrite").parquet(output_path)
        log(f"✅ Successfully ingested '{table_name}' to: {output_path}")

    except Exception as e:
        log(f"❌ Error ingesting table '{table_name}': {str(e)}")
        raise

if __name__ == "__main__":
    log("✅ Script started")

    if len(sys.argv) != 6:
        log("❌ Usage: bronze_ingestion.py <jdbc_url> <user> <password> <table_name> <bronze_base_path>")
        sys.exit(-1)

    jdbc_url_arg = sys.argv[1]
    user_arg = sys.argv[2]
    password_arg = sys.argv[3]
    table_name_arg = sys.argv[4]
    bronze_base_path_arg = sys.argv[5]

    log(f"📌 Arguments received:\n"
        f"   JDBC URL     : {jdbc_url_arg}\n"
        f"   User         : {user_arg}\n"
        f"   Table        : {table_name_arg}\n"
        f"   Bronze Path  : {bronze_base_path_arg}")

    log("⚙️  Creating Spark session...")
    spark_session = SparkSession.builder \
    .appName("Bronze Ingestion from MySQL") \
    .config("spark.jars", "/opt/spark-jars/mysql-connector-java-8.0.28.jar") \
    .getOrCreate()


    db_connection_properties = {
        "user": user_arg,
        "password": password_arg,
        "driver": "com.mysql.cj.jdbc.Driver"
    }

    ingest_table_to_bronze(spark_session, jdbc_url_arg, db_connection_properties, table_name_arg, bronze_base_path_arg)

    log("🏁 Ingestion complete. Stopping Spark session.")
    spark_session.stop()
