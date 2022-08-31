CREATE
KEYSPACE IF NOT EXISTS matches WITH REPLICATION = {
      'class': 'SimpleStrategy',
      'replication_factor': 1
};
CREATE TABLE IF NOT EXISTS matches.available
(
    match_id
    text,
    user_id
    text,
    user_table
    text,
    user_league
    text,
    PRIMARY
    KEY
(
    match_id
)
    );
