from functools import lru_cache

from app.domain.services.event_store.event_store import EventStore


@lru_cache()
def get_event_store() -> EventStore:
    return EventStore()
