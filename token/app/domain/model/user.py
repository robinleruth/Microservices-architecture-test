from dataclasses import dataclass, field
from typing import List


@dataclass
class User:
    nickname: str
    scopes_allowed: List[str] = field(default_factory=list)
    id: int = 0
    created_at: int = 0
    updated_at: int = 0
    last_seen_at: int = 0
    online: bool = False
