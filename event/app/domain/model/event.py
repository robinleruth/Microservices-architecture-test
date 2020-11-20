import datetime as dt
from typing import Optional, Dict, Any

from pydantic.main import BaseModel


class EventIn(BaseModel):
    channel_name: str
    aggregate_type: str
    # If no aggregate_id -> first event
    aggregate_id: Optional[str]
    event_type: str
    event_data: Dict[str, Any]


class Event(BaseModel):
    aggregate_type: str
    aggregate_id: str
    event_id: str  # uuid
    event_type: str
    event_data: Dict[str, Any]
    created_at: dt.datetime
