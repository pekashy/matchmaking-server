import logging

import match_db
import schemas.find_game
import user_db


class Matcher:
    def __init__(self):
        self.matches: match_db.MatchDB = match_db.MatchDB()
        self.user_infos: user_db.UserDB = user_db.UserDB()

    def find_game(self, logger: logging.Logger, request: schemas.find_game.RequestMessage):
        """
        1. Check if user already has match assigned in result DB
        2. If not, create user match. We create now to protect users from constant match stealing.
        3. Try finding match
        4. If found and still less users, than necessary, update match. Store match in memory. Delete created match.
        5. If fallbacking or match is now complete, add match to queue
        6. Delete match from match_db
        """

        if self.user_infos.is_user_already_in_game(request.user):
            return
        self.matches.add_match(user=request.user, logger=logger)
