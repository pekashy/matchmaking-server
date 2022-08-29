from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class User:
    id: str
    table: int
    league: int
