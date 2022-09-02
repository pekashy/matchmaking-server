from dataclasses import dataclass
from typing import List, Tuple, Optional

from dataclasses_json import dataclass_json

import schemas.common
import schemas.user

QUEUE_NAME = "find_game_requests"
QUEUE_URL = "amqp://guest:guest@start-matchmaking-queue:5672"


@dataclass_json
@dataclass
class Lobby:
    """
        We are always able to generalize approach
        to n parameters (0, n-1) by creating an array
        of possible intervals of each. But as the task is
        about using only 2 params, lets hardcode them for better
        readability.
    """
    possible_table_values_interval: Tuple[int]
    possible_league_values_intervals: Tuple[int]


@dataclass_json
@dataclass
class Query:
    """
    Lets represent query as a list of regions
    """
    possible_lobbies: List[Lobby]


def parse_query_string(query_string: str) -> Optional[Query]:
    """
    E.G.
    :param query_string: ( 0 < League < 3) AND (Table = 7)
    :return: Query{
                possible_regions: [
                    Region {
                        possible_table_values_interval: (7, 7)
                        possible_league_values_intervals: (0, 3)
                    }
                ]
            }
    """
    # TODO: Let's say we implemented this method :)
    return None


@dataclass_json
@dataclass
class RequestMessage(schemas.common.Message):
    user: schemas.user.User
    query: Query
