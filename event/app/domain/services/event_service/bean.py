from app.domain.services.event_service.event_service import EventService
from app.domain.services.event_store.bean import event_store

event_service = EventService(event_store)


async def get_event_service() -> EventService:
    await event_service.init_redis()
    return event_service
