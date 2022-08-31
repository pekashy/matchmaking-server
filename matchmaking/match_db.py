import logging
import uuid

from cassandra.cluster import Cluster

import schemas.user


class MatchDB:
    def __init__(self):
        self.cluster = Cluster(['open-matches-db'], port=9042)
        self.session = self.cluster.connect(keyspace='matches')

    def add_match(self, user: schemas.user.User, logger: logging.Logger):
        logger.info(f'Creating empty match for user {user.id}')
        # TODO: CREATE KEYSPACE!
        self.session.execute(
            'INSERT INTO available (match_id, user_id, user_table, user_league) VALUES (%s, %s, %s, %s)',
            ('match-' + str(uuid.uuid4()), user.id, str(user.table), str(user.league)))
