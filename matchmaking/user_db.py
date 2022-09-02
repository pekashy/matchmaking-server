import redis

import schemas.match


class UserDB:
    def __init__(self):
        self.client = redis.Redis(host='userdata', port=6379, db=0)

    def is_user_already_in_game(self, user: schemas.user.User) -> bool:
        user_info_in_db = self.client.get(user.id)

        return user_info_in_db is not None

    def try_commit_match(self, match: schemas.match.MatchLobby) -> bool:
        pipeline = self.client.pipeline()
        for user in match.users:
            pipeline.setnx(user, match.id)
            pipeline.persist(user)

        return pipeline.execute(raise_on_error=False)[0]
