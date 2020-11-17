import datetime as dt
from dataclasses import dataclass


@dataclass
class User:
    id: int
    created_at: dt.datetime
    updated_at: dt.datetime
    last_seen_at: dt.datetime
    nickname: str
    online: bool
