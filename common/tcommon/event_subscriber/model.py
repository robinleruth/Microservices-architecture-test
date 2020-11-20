import datetime as dt
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class EventDto:
    aggregate_type: str
    aggregate_id: str
    event_id: str  # uuid
    event_type: str
    created_at: dt.datetime
    event_data: Dict[str, Any]
