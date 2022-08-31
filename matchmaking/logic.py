import logging

import match_db
import schemas.find_game


class Matcher:
    def __init__(self):
        self.matches: match_db.MatchDB = match_db.MatchDB()

    def find_game(self, logger: logging.Logger, request: schemas.find_game.RequestMessage):
        self.matches.add_match(user=request.user, logger=logger)
        '''
        1. Check if user already has match assigned in result DB
        2. If not, create user match. We create now to protect users from constant match stealing.
        3. Try finding match
        4. If found and still less users, than necessary, update match. Store match in memory. Delete created match.
        5. If fallbacking or match is now complete, add match to queue
        6. Delete match from match_db
        '''
