CREATE
KEYSPACE IF NOT EXISTS matches WITH REPLICATION = {
      'class': 'SimpleStrategy',
      'replication_factor': 1
};

DROP TABLE IF EXISTS matches.lobbies;
DROP TYPE IF EXISTS matches.player;

CREATE TABLE matches.lobbies
(
    min_table
    counter,
    min_league
    counter,
    n_users
    counter,
    max_table
    counter,
    max_league
    counter,
    lobby_id
    text,
    host_user_id
    text,
    users
    set<text>,
    PRIMARY KEY(lobby_id)
    );

