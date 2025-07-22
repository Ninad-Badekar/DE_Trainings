CREATE DATABASE IF NOT EXISTS ipl_daily_db;
use ipl_daily_db;

CREATE TABLE IF NOT EXISTS deliveries (
    match_id INT,
    inning INT,
    batting_team VARCHAR(100),
    bowling_team VARCHAR(100),
    overs INT,
    ball INT,
    batter VARCHAR(100),
    bowler VARCHAR(100),
    non_striker VARCHAR(100),
    batsman_runs INT,
    extra_runs INT,
    total_runs INT,
    extra_types varchar(100),
    is_wicket BOOLEAN,
    player_dismissed VARCHAR(100),
    dismissal_kind VARCHAR(100),
    fielder VARCHAR(100)
    );

LOAD DATA INFILE '/var/lib/mysql-files/deliveries.csv'
INTO TABLE deliveries
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

CREATE TABLE IF NOT EXISTS matches (
    id INT PRIMARY KEY,
    season varchar(100),
    city VARCHAR(100),
    date DATE,
    match_type varchar(100),
    player_of_match VARCHAR(100),
    venue VARCHAR(200),
    team1 VARCHAR(100),
    team2 VARCHAR(100),
    toss_winner VARCHAR(100),
    toss_decision VARCHAR(20),
    winner VARCHAR(100),
    result VARCHAR(100),
    result_margin VARCHAR(100),
    target_runs varchar(100),
    target_overs varchar(100),
    super_over varchar(100),
    method varchar(100),
    
    umpire1 VARCHAR(100),
    umpire2 VARCHAR(100)
);

LOAD DATA INFILE '/var/lib/mysql-files/matches.csv'
INTO TABLE matches
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
