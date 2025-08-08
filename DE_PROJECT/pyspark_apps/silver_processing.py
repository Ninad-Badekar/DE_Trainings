from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, when
import os
import sys
from datetime import datetime

def normalize_dismissal_kind(df):
    return df.withColumn(
        "dismissal_kind_code",
        when(col("dismissal_kind") == "not_out", 0)
        .when(col("dismissal_kind") == "stumped", 1)
        .when(col("dismissal_kind") == "retired out", 2)
        .when(col("dismissal_kind") == "hit wicket", 3)
        .when(col("dismissal_kind") == "bowled", 4)
        .when(col("dismissal_kind") == "lbw", 5)
        .when(col("dismissal_kind") == "obstructing the field", 6)
        .when(col("dismissal_kind") == "caught and bowled", 7)
        .when(col("dismissal_kind") == "retired hurt", 8)
        .when(col("dismissal_kind") == "caught", 9)
        .when(col("dismissal_kind") == "run out", 10)
        .otherwise(0)  # Default to not_out
    )

def normalize_player_dismissed(df):
    return df.withColumn("player_dismissed", when(col("player_dismissed").isNull(), lit("NA")).otherwise(col("player_dismissed")))

def normalize_extras_type(df):
    return df.withColumn("extra_types", when(col("extra_types").isNull(), lit("NA")).otherwise(col("extra_types")))

def normalize_fielder(df):
    return df.withColumn("fielder", when(col("fielder").isNull(), lit("NA")).otherwise(col("fielder")))

def clean_deliveries(df):
    df = df.dropna(subset=["match_id", "overs", "ball"])
    df = normalize_player_dismissed(df)
    df = normalize_fielder(df)
    df = normalize_dismissal_kind(df)
    df = normalize_extras_type(df)
    return df

def process_to_silver(spark, bronze_path, silver_path, table):
    today = datetime.today()
    bronze_table_path = f"{bronze_path}/mysql/{table}/{today.strftime('%Y/%m/%d')}"
    print(f" Reading from Bronze: {bronze_table_path}")
    df = spark.read.parquet(bronze_table_path)

    if table == "deliveries":
        df = clean_deliveries(df)

    silver_table_path = os.path.join(silver_path, table, today.strftime('%Y/%m/%d'))
    df.write.mode("overwrite").parquet(silver_table_path)
    print(f" Written to Silver: {silver_table_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: silver_processing.py <bronze_base_path> <silver_base_path> <table_name>")
        sys.exit(1)

    bronze_base_path = sys.argv[1]
    silver_base_path = sys.argv[2]
    table_name = sys.argv[3]

    spark = SparkSession.builder.appName("Silver Processing").getOrCreate()
    print(" Starting Silver Processing")
    print(f" Bronze Path : {bronze_base_path}")
    print(f" Silver Path : {silver_base_path}")
    print(f" Table       : {table_name}")

    process_to_silver(spark, bronze_base_path, silver_base_path, table_name)
    spark.stop()
