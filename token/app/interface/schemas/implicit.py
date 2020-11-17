from pydantic import BaseModel


class ImplicitIn(BaseModel):
    client_id: str
    redirect_uri: str


class ImplicitOut(ImplicitIn):
    username: str
    password: str
