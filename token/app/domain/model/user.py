from dataclasses import dataclass


@dataclass
class User:
    nickname: str
    id: int = 0
    created_at: int = 0
    updated_at: int = 0
    last_seen_at: int = 0
    online: bool = False
