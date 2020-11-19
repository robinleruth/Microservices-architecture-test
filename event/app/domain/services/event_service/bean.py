from functools import lru_cache

from app.domain.services.event_service.event_service import EventService
from app.domain.services.event_store.bean import get_event_store


@lru_cache()
def get_event_service() -> EventService:
    return EventService(get_event_store())
