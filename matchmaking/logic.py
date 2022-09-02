import logging
import time
from typing import Callable, List

import match_db
import schemas.find_game
import schemas.match
import user_db


class Matcher:
    def __init__(self):
        self.matches: match_db.MatchDB = match_db.MatchDB()
        self.user_infos: user_db.UserDB = user_db.UserDB()

    def _try_connect_to_existing_game(self, user: schemas.user.User,
                                      fetch_matches_func: Callable[
                                          [schemas.user.User, logging.Logger], List[schemas.match.MatchLobby]],
                                      logger: logging.Logger):
        ready_games: List[schemas.match.Match] = fetch_matches_func(user=user, logger=logger)
        logger.info(f"Found {len(ready_games)}")
        for game in ready_games:
            logger.info(f"Trying to commit match {game.id}")
            if self.user_infos.try_commit_match(game):
                return True
        return False

    def find_game(self, request: schemas.find_game.RequestMessage, logger: logging.Logger):
        if self.user_infos.is_user_already_in_game(request.user):
            return
        if self._try_connect_to_existing_game(user=request.user, logger=logger,
                                              fetch_matches_func=self.matches.get_matching_ready_games):
            return
        self.matches.register_in_matching_lobbies(user=request.user, logger=logger)
        self.matches.publish_lobbies(query=request, logger=logger)
        time.sleep(match_db.LOBBY_TIMEOUT)

        # fallback
        self._try_connect_to_existing_game(user=request.user, logger=logger,
                                           fetch_matches_func=self.matches.get_matching_ready_games_fallback)
        '''
            No need to unregister user from matches he registered into, as they are guaranteed to be expired.
            As well as users own lobbies
        '''
