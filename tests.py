from uuid import uuid4

import requests

import schemas.find_game
import schemas.user

CREATE_MATCH_ENDPOINT = "http://localhost:8050/find_game"


def test_create_match():
    query_dict = {
        'possible_lobbies': [
            {
                'possible_table_values_interval':   (7, 7),
                'possible_league_values_intervals': (0, 3)
            }
        ]
    }
    query = schemas.find_game.Query.from_dict(query_dict)
    request = schemas.find_game.RequestMessage(
        corr_id=str(uuid4()),
        user=schemas.user.User(id="player_one", user_table=7, user_league=1),
        query=query,
    )
    headers = {"Content-Type": "application/json"}
    requests.post(url=CREATE_MATCH_ENDPOINT,
                  data=request.to_json(),
                  headers=headers)
