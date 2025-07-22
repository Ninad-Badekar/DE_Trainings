CREATE SCHEMA IF NOT EXISTS ipl_dw;
SET search_path = ipl_dw;

-- Dimensions
CREATE TABLE dim_player (
  player_id   SERIAL PRIMARY KEY,
  player_name TEXT NOT NULL UNIQUE
);

CREATE TABLE dim_team (
  team_id   SERIAL PRIMARY KEY,
  team_name TEXT NOT NULL UNIQUE
);

CREATE TABLE dim_venue (
  venue_id   SERIAL PRIMARY KEY,
  venue_name TEXT NOT NULL UNIQUE,
  city       TEXT
);

CREATE TABLE dim_date (
  date_id      SERIAL PRIMARY KEY,
  full_date    DATE NOT NULL UNIQUE,
  year         INT NOT NULL,
  month        INT NOT NULL,
  day          INT NOT NULL,
  day_of_week  TEXT NOT NULL
);

CREATE TABLE dim_match (
  match_id         INT PRIMARY KEY,
  date_id          INT NOT NULL REFERENCES dim_date(date_id),
  venue_id         INT REFERENCES dim_venue(venue_id),
  season           INT,
  match_type       TEXT,
  team1_id         INT REFERENCES dim_team(team_id),
  team2_id         INT REFERENCES dim_team(team_id),
  toss_winner_id   INT REFERENCES dim_team(team_id),
  toss_decision    TEXT,
  winner_id        INT REFERENCES dim_team(team_id),
  result           TEXT,
  result_margin    TEXT,
  super_over       BOOLEAN,
  method           TEXT,
  umpire1          TEXT,
  umpire2          TEXT
);

-- Fact table
CREATE TABLE fact_delivery (
  match_id            INT NOT NULL REFERENCES dim_match(match_id),
  inning              INT NOT NULL,
  over                INT NOT NULL,
  ball                INT NOT NULL,
  batting_team_id     INT NOT NULL REFERENCES dim_team(team_id),
  bowling_team_id     INT NOT NULL REFERENCES dim_team(team_id),
  batsman_id          INT NOT NULL REFERENCES dim_player(player_id),
  non_striker_id      INT NOT NULL REFERENCES dim_player(player_id),
  bowler_id           INT NOT NULL REFERENCES dim_player(player_id),
  batsman_runs        INT,
  extra_runs          INT,
  total_runs          INT,
  extras_type         TEXT,
  is_wicket           BOOLEAN,
  player_dismissed_id INT REFERENCES dim_player(player_id),
  dismissal_kind      TEXT,
  fielder_id          INT REFERENCES dim_player(player_id),
  PRIMARY KEY (match_id, inning, over, ball)
);
