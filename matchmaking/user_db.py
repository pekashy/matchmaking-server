import pymongo

import schemas.user


class UserDB:
    def __init__(self):
        self.client = pymongo.MongoClient('userdata', 27017)
        self.users_db = self.client.users_db
        self.users = self.users_db.users

    def is_user_already_in_game(self, user: schemas.user.User) -> bool:
        user_info_in_db = self.users.find_one({'id': user.id})
        if not user_info_in_db:
            return False

        return 'current_match_id' in user_info_in_db
