import datetime as dt
from dataclasses import dataclass, InitVar, field
from typing import List


@dataclass
class User:
    id: int
    created_at: dt.datetime
    updated_at: dt.datetime
    last_seen_at: dt.datetime
    nickname: str
    online: bool
    scopes_allowed: List[str] = field(default_factory=list)
    scopes: InitVar[str] = field(default='')

    def __post_init__(self, scopes: str):
        self.scopes_allowed = scopes.split(' ')
