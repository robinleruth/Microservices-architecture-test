from dataclasses import dataclass

from app.domain.services.event_store.event_store import EventStore
from app.infrastructure.log import logger


@dataclass
class EventService:
    store: EventStore

    def __post_init__(self):
        logger.info('Init Event Service')
