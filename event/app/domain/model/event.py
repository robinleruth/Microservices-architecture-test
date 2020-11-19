from typing import Optional, Dict, Any

from pydantic.main import BaseModel


class EventIn(BaseModel):
    aggregate_type: str
    # If no aggregate_id -> first event
    aggregate_id: Optional[str]
    event_type: str
    event_data: Dict[str, Any]


class Event(BaseModel):
    aggregate_type: str
    aggregate_id: str
    event_id: int  # autoincrement
    event_type: str
    event_data: Dict[str, Any]
