from dataclasses import dataclass


@dataclass
class User:
    id: int
    created_at: int
    updated_at: int
    last_seen_at: int
    nickname: str
    online: bool
