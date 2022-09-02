from dataclasses import dataclass
from typing import Set

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class MatchLobby:
    lobby_id: str
    host_user_id: str
    users: Set[str]
    n_users: int
    min_table: int
    max_table: int
    min_league: int
    max_league: int
