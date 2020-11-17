from pydantic import BaseModel


class ClientId(BaseModel):
    client_id: str
