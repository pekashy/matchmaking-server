from dataclasses import dataclass
from dataclasses_json import dataclass_json
from .user import User
from .common import Message


@dataclass_json
@dataclass
class RequestMessage(Message):
    user: User
    query: str
