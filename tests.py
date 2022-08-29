from uuid import uuid4
import requests
import schemas.find_game
import schemas.user

CREATE_MATCH_ENDPOINT = "http://localhost:8050/find_game"


def test_create_match():
    request = schemas.find_game.RequestMessage(
        corr_id=str(uuid4()),
        user=schemas.user.User(id="player_one", table=7, league=1),
        query="(0 < League < 3) AND (Table = 7)")
    headers = {"Content-Type": "application/json"}
    requests.post(url=CREATE_MATCH_ENDPOINT,
                  data=request.to_json(),
                  headers=headers)
