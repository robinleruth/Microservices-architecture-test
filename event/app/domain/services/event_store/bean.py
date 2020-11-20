from app.domain.services.event_store.event_store import EventStore

event_store = EventStore()


async def get_event_store() -> EventStore:
    await event_store.init_redis()
    return event_store
