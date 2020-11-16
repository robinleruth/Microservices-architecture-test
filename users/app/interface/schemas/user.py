from pydantic import BaseModel


class UserIn(BaseModel):
    name: str
    password: str
