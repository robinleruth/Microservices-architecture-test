from typing import Optional, List

from pydantic import BaseModel


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = None
