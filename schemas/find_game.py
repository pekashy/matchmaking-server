from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .common import Message
from .user import User

QUEUE_NAME = "find_game_requests"
QUEUE_URL = "amqp://guest:guest@start-matchmaking-queue:5672"


@dataclass_json
@dataclass
class RequestMessage(Message):
    user: User
    query: str
