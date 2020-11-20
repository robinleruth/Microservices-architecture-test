from typing import List

from pydantic.main import BaseModel

from app.domain.model.event import Event


class Aggregate(BaseModel):
    aggregate_id: str
    aggregate_type: str
    events: List[Event]
