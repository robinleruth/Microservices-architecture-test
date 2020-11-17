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
    scopes_not_allowed: List[str] = field(default_factory=list)

    def has_scopes(self, scopes: List[str]) -> bool:
        s = set(self.scopes_allowed)
        for scope in scopes:
            if scope not in s:
                self.scopes_not_allowed.append(scope)
        if len(self.scopes_not_allowed) > 0:
            return False
        return True
