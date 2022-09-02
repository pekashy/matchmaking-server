import logging
import uuid
from typing import List

import cassandra.query
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement

import schemas.find_game
import schemas.match
import schemas.user

DESIRED_GAME_SIZE = 3  # TODO: Set from config
FALLBACK_GAME_SIZE = 2
LOBBY_TIMEOUT = 10
LOBBY_TIMEOUT_GRACE_PERIOD = 3
BATCH_LIMIT = 20


class MatchDB:
    def __init__(self):
        self.cluster = Cluster(["open-matches-db"], port=9042)
        self.session = self.cluster.connect(keyspace="matches")
        self.session.row_factory = cassandra.query.dict_factory

    def get_matching_ready_games(
            self,
            user: schemas.user.User,
            logger: logging.Logger
    ) -> List[schemas.match.MatchLobby]:
        logger.info(f"Searching ready games for user {user.id}")
        # TODO: ALLOW FILTERING Significantly reduces the perfomance of the request, think about schema improvements
        rows = self.session.execute(
            f"SELECT * FROM matches.lobbies "
            f"WHERE n_users = {DESIRED_GAME_SIZE - 1} "
            f"AND min_table <= {user.user_table} "
            f"AND min_league <= {user.user_league} "
            f"AND max_table > {user.user_table} "
            f"AND max_league > {user.user_league} "
            f"LIMIT {BATCH_LIMIT} ALLOW FILTERING")

        lobbies = []
        for row in rows:
            logger.debug(f"Got matching lobby {str(row)}")
            lobbies.append(schemas.match.MatchLobby.from_dict(row))
        return lobbies

    def get_matching_ready_games_fallback(
            self,
            user: schemas.user.User,
            logger: logging.Logger
    ) -> List[schemas.match.MatchLobby]:
        logger.info(f"Searching fallback ready games for user {user.id}")
        rows = self.session.execute(f"SELECT * FROM matches.lobbies "
                                    f"WHERE n_users => {FALLBACK_GAME_SIZE - 1} "
                                    f"AND user_id <= {user.user_table} "
                                    f"AND min_table <= {user.user_table} "
                                    f"AND min_league <= {user.user_league} "
                                    f"AND max_table > {user.user_table} "
                                    f"AND max_league > {user.user_league} "
                                    f"LIMIT {BATCH_LIMIT} ALLOW FILTERING")

        lobbies = []
        for row in rows:
            logger.debug(f"Got matching lobby for fallback {str(row)}")
            lobbies.append(schemas.match.MatchLobby.from_dict(row))
        return lobbies

    def publish_lobbies(
            self,
            query: schemas.find_game.RequestMessage,
            logger: logging.Logger
    ):
        logger.info(f"Creating empty match for user {query.user.id}")
        insert_lobby = self.session.prepare("INSERT INTO matches.lobbies "
                                            "(lobby_id, host_user_id, users, n_users, min_table, "
                                            "max_table, min_league, max_league) "
                                            "VALUES (?, ?, {user_id: ?, user_table: ?, user_league: ?}, "
                                            "?, ?, ?, ?, ?) USING TTL ?")
        batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
        user: schemas.user.User = query.user
        for lobby in query.possible_lobbies:
            for table_interval in lobby.possible_table_values_interval:
                for league_interval in lobby.possible_league_values_intervals:
                    lobby = schemas.match.MatchLobby(lobby_id=str(uuid.uuid4()), max_table=table_interval[1],
                                                     min_table=table_interval[0], max_league=league_interval[1],
                                                     min_league=league_interval[0], users={query.user},
                                                     host_user_id=query.user.id, n_users=1)
                    try:
                        batch.add(insert_lobby,
                                  (lobby.id, user.id, user.id,
                                   user.user_table, user.user_league, 1,
                                   lobby.min_table, lobby.max_table,
                                   lobby.min_league, lobby.max_league, LOBBY_TIMEOUT))
                        logger.info("Lobby `%s` is registered", lobby.to_json())
                    except Exception as e:
                        logger.error("The cassandra error: {}".format(e))
        self.session.execute(batch)

    def register_in_matching_lobbies(self, user: schemas.user.User, logger: logging.Logger):
        logger.info(f"Registering user {user.id} in lobbies")
        prepared_update_statement = self.session.prepare("UPDATE matches.lobbies "
                                                         "SET n_users = n_users + 1, "
                                                         "users = users + {?} "
                                                         "WHERE min_table <= ? "
                                                         "AND max_table > ? "
                                                         "AND min_league <= ? "
                                                         "AND max_league > ? "
                                                         "AND n_users < ? "
                                                         "AND host_user_id != ?")

        self.session.execute(prepared_update_statement, [user.id, user.user_table,
                                                         user.user_table, user.user_league,
                                                         user.user_league, DESIRED_GAME_SIZE,
                                                         user.id])
