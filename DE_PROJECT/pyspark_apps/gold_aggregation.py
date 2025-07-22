from pyspark.sql import SparkSession
from pyspark.sql.functions import col, monotonically_increasing_id
import os
import sys

def create_dim_teams(df_matches):
    teams = df_matches.selectExpr("team1 as team").union(df_matches.selectExpr("team2 as team")).distinct()
    return teams.withColumn("team_id", monotonically_increasing_id()) \
                .withColumnRenamed("team", "team_name")

def create_dim_venues(df_matches):
    venues = df_matches.select("venue", "city").dropDuplicates()
    return venues.withColumn("venue_id", monotonically_increasing_id()) \
                 .withColumnRenamed("venue", "venue_name") \
                 .withColumnRenamed("city", "venue_city")

def create_dim_players(df_deliveries):
    players = df_deliveries.selectExpr("batter as player").union(
        df_deliveries.selectExpr("bowler as player")
    ).union(
        df_deliveries.selectExpr("non_striker as player")
    ).union(
        df_deliveries.selectExpr("player_dismissed as player")
    ).na.drop().dropDuplicates()
    return players.withColumn("player_id", monotonically_increasing_id()) \
                  .withColumnRenamed("player", "player_name")

def create_dim_date(df_matches):
    return df_matches.select("date").dropDuplicates().withColumn("date_id", monotonically_increasing_id())

def create_fact_matches(df_matches, dim_teams, dim_venues):
    m = df_matches.alias("m")
    t = dim_teams.alias("t")
    v = dim_venues.alias("v")

    # Prepare renamed versions for join keys
    t1 = t.select(col("team_id").alias("team1_id"), col("team_name").alias("team1_name"))
    t2 = t.select(col("team_id").alias("team2_id"), col("team_name").alias("team2_name"))
    tw = t.select(col("team_id").alias("toss_winner_id"), col("team_name").alias("toss_winner_name"))
    mw = t.select(col("team_id").alias("match_winner_id"), col("team_name").alias("match_winner_name"))

    return (
        m
        .join(t1, col("m.team1") == col("team1_name"), "left")
        .join(t2, col("m.team2") == col("team2_name"), "left")
        .join(tw, col("m.toss_winner") == col("toss_winner_name"), "left")
        .join(mw, col("m.winner") == col("match_winner_name"), "left")
        .join(v, col("m.venue") == col("v.venue_name"), "left")
        .select(
            col("m.id").alias("match_id"),
            col("m.season"),
            col("m.city"),
            col("m.date"),
            col("v.venue_id"),
            col("v.venue_city"),
            col("m.match_type"),
            col("team1_id"),
            col("team2_id"),
            col("toss_winner_id"),
            col("m.toss_decision"),
            col("match_winner_id"),
            col("m.result"),
            col("m.result_margin"),
            col("m.target_runs"),
            col("m.target_overs"),
            col("m.super_over"),
            col("m.method"),
            col("m.player_of_match"),
            col("m.umpire1"),
            col("m.umpire2")
        )
    )

from pyspark.sql.functions import when, lit

def create_fact_deliveries(df_deliveries):
    # Compute dismissal_kind_code here instead of Silver
    df = df_deliveries.withColumn(
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
        .otherwise(0)
    )

    return df.select(
        "match_id", "inning", "batting_team", "bowling_team", "overs", "ball",
        "batter", "bowler", "non_striker", col("runs_batsman").alias("batsman_runs"),
        "extra_runs", "total_runs", col("extra_types").alias("extras_type"),
        "is_wicket", "player_dismissed", "dismissal_kind", "dismissal_kind_code", "fielder"
    )


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: gold_aggregation.py <silver_base_path> <gold_base_path>")
        sys.exit(1)

    silver_base = sys.argv[1]
    gold_base = sys.argv[2]

    spark = SparkSession.builder.appName("Gold Aggregation").getOrCreate()

    print(" Starting Gold Aggregation")
    print(f" Silver Base: {silver_base}")
    print(f" Gold Base  : {gold_base}")

    # Read silver data
    df_matches = spark.read.option("recursiveFileLookup", "true").parquet(f"{silver_base}/matches")
    df_deliveries = spark.read.option("recursiveFileLookup", "true").parquet(f"{silver_base}/deliveries")

    # Dimensions
    dim_teams = create_dim_teams(df_matches)
    dim_venues = create_dim_venues(df_matches)
    dim_players = create_dim_players(df_deliveries)
    dim_date = create_dim_date(df_matches)

    # Facts
    fact_matches = create_fact_matches(df_matches, dim_teams, dim_venues)
    fact_deliveries = create_fact_deliveries(df_deliveries)

    # Save dimensions
    dim_teams.write.mode("overwrite").parquet(os.path.join(gold_base, "dim_teams"))
    dim_venues.write.mode("overwrite").parquet(os.path.join(gold_base, "dim_venues"))
    dim_players.write.mode("overwrite").parquet(os.path.join(gold_base, "dim_players"))
    dim_date.write.mode("overwrite").parquet(os.path.join(gold_base, "dim_date"))

    # Save facts
    fact_matches.write.mode("overwrite").parquet(os.path.join(gold_base, "fact_matches"))
    fact_deliveries.write.mode("overwrite").parquet(os.path.join(gold_base, "fact_deliveries"))

    print("✅ Gold Aggregation Complete")
    spark.stop()
